r"""
Pair two manuscript versions part by part, then compare what each part says.

A manuscript becomes a sequence of blocks: front-matter page anchors,
headings, paragraph chunks, and page breaks. Blocks pair by identity first:
pages by role (halaman pengesahan with halaman pengesahan) and headings by ID
(their \label, or the title slug when a version has no labels). Headings
without a shared ID and paragraph chunks pair by content similarity. Pairing
keeps both reading orders; a part that changed position is compared with its
counterpart at both places and labeled as moved.

Each row of the side-by-side layout then aligns sentences, list items, and
lines. Word-level highlights mark changes inside corresponding sentences;
text without a counterpart gets a pale background.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from itertools import pairwise

from diff_tokens import graphic_end, read_braced_argument, render_group, word_level_render

CONTROL = re.compile(r'\\([a-zA-Z@]+\*?|.)', re.S)
ENVIRONMENT_NAME = re.compile(r'\s*\{([^{}]*)\}')
BLANK_LINE = re.compile(r'\n[ \t]*\n\s*')
HEADING_LEVELS = {"thesischapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}
HEADING_LABEL = re.compile(r'[ \t]*(?:\n[ \t]*)?\\label\{([^{}]*)\}')
# Navigation commands write outline and contents entries; they print nothing.
NAVIGATION = re.compile(r'\\phantomsection\b[ \t]*\n?|\\addcontentsline\{[^{}]*\}\{[^{}]*\}\{[^{}]*\}[ \t]*\n?'
                        r'|\\pdfbookmark(?:\[[^\]]*\])?\{[^{}]*\}\{[^{}]*\}[ \t]*\n?')
LIST_START = re.compile(r'\\begin\{(?:enumerate|itemize|description)\}')
# Text inside these environments is compared as one piece: splitting it would
# break TikZ paths, rows of display math, or verbatim text.
ATOMIC_ENVIRONMENTS = re.compile(
    r'(?:tikzpicture|equation|align|alignat|flalign|multline|gather|displaymath'
    r'|verbatim|lstlisting|minted|tabular|tabularx|longtable|array)\*?')
# A table without a counterpart gets one background, which keeps its rules whole.
TABULAR = re.compile(r'\\begin\{(?:tabular|tabularx|longtable|array)\*?\}')
STANDALONE_ENVIRONMENTS = frozenset({
    "figure", "table", "enumerate", "itemize", "description", "tikzpicture",
    "equation", "align", "alignat", "flalign", "multline", "gather", "displaymath",
    "verbatim", "lstlisting", "minted", "tabular", "tabularx", "longtable", "array",
})
LITERAL_ENVIRONMENTS = frozenset({"verbatim", "lstlisting", "minted"})
# These commands print objects/numbers even when visible_words has no words.
VISIBLE_OBJECT = re.compile(
    r'\\(?:includegraphics|rule|ref|pageref|eqref|autoref|nameref)\*?\b'
    r'|\\begin\{(?:' + '|'.join(sorted(STANDALONE_ENVIRONMENTS - {
        "figure", "table", "enumerate", "itemize", "description"})) + r')\*?\}|\\\[')


def source_key(text):
    """Ignore source line wrapping; retain words, markup and object arguments."""
    return " ".join(text.split())


def content_key(text):
    """Labels/navigation have no visible content; other markup can change it."""
    return source_key(re.sub(r'\\label\{[^{}]*\}', '', NAVIGATION.sub('', text)))


def has_highlight(text):
    return bool(re.search(r'\\(?:delhighlight|inhighlight|delpale|inspale|diffinline|fcolorbox|diffcaptionlabel|diffequationlabel)\b'
                          r'|\\begin\{diffmath\}', text))


def chunk_type(text):
    """Keep prose, lists, figures, tables and equations from pairing by accident."""
    environment = re.match(r'\s*\\begin\{([^{}]+)\}', text)
    if environment:
        name = environment.group(1).rstrip('*')
        if name in ("enumerate", "itemize", "description"):
            return "list"
        if name in STANDALONE_ENVIRONMENTS:
            return name
    if text.lstrip().startswith(r"\["):
        return "displaymath"
    return "prose"


def object_id(text):
    """A figure/table/equation label identifies an object across revisions."""
    if chunk_type(text) in ("prose", "list"):
        return ""
    label = re.search(r'\\label\{([^{}]+)\}', text)
    return label.group(1) if label else ""


def equation_rows(text):
    """Numbered AMS rows; nested matrices/splits do not start extra equations."""
    match = re.search(r'\\begin\{(equation|align|alignat|flalign|gather|multline)\}', text)
    if not match:
        return []
    end = text.rfind(r"\end{" + match.group(1) + "}")
    body = text[match.end():end]
    if match.group(1) in ("equation", "multline"):
        return [] if re.search(r'\\(?:notag|nonumber)\b', body) else [body]
    rows, start, pos, braces, environments = [], 0, 0, 0, []
    while pos < len(body):
        if body[pos] == "\\":
            command = CONTROL.match(body, pos)
            name, stop = command.group(1), command.end()
            if name in ("begin", "end"):
                environment = ENVIRONMENT_NAME.match(body, stop)
                if environment:
                    stop = environment.end()
                    if name == "begin":
                        environments.append(environment.group(1))
                    elif environments:
                        environments.pop()
            elif name == "\\" and not braces and not environments:
                rows.append(body[start:pos])
                start = stop
            pos = stop
            continue
        if body[pos] == "{":
            braces += 1
        elif body[pos] == "}":
            braces -= 1
        pos += 1
    rows.append(body[start:])
    return [row for row in rows if row.strip() and not re.search(r'\\(?:notag|nonumber)\b', row)]

# Pairing weights: identities outweigh content, so a shared page role or
# heading ID anchors the rows even when the text around it was rewritten.
WEIGHT = {"page": 6.0, "heading": 4.0, "chunk": 1.0}
THRESHOLD = {"page": 0.5, "heading": 0.45, "chunk": 0.35}
SENTENCE_THRESHOLD = 0.35
# Pages whose lines average at most this many content words are structured
# (cover, approval) rather than prose (abstract, preface).
LINE_WORDS = 8
# A part that changed position needs an unchanged ID or clearly shared text.
MOVE_THRESHOLD = 0.6

STOPWORDS = frozenset("""
    dan atau di ke dari yang untuk dalam pada terhadap oleh dengan ini itu
    adalah sebagai juga akan tidak serta the of and in for on to an is are
    as by with this that
""".split())
# Layout commands and their arguments carry no visible words.
LAYOUT_COMMAND = re.compile(
    r'\\(?:begin|end)\{[^{}]*\}(?:\[[^\]]*\])?(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})*'
    r'|\\(?:[hv]space|setlength|includegraphics|label|ref|pageref|eqref|fontsize|cellcolor|rule'
    r'|needspace|setcounter|addvspace|makebox|phantomsection|addcontentsline|pdfbookmark)\*?'
    r'(?:\[[^\]]*\])*(?:\{[^{}]*\})*'
    r'|\\[a-zA-Z@]+\*?')
# A line opening with a command outside this set starts a new unit (\noindent,
# \vspace, \hfill); these inline commands continue the prose around them.
BLOCK_LINE = re.compile(r'[ \t]*\\([A-Za-z]+)')
INLINE_COMMANDS = frozenset("""
    textit textbf emph underline uline texttt textsc textsf textrm textup parencite cite textcite
    citeauthor citeyear ref eqref pageref autoref url href footnote mbox ensuremath item
""".split())
SENTENCE_GAP = re.compile(r'[)\'"]*\s+(?=[A-Z(\\])')
# Abbreviations whose period does not end a sentence.
ABBREVIATIONS = frozenset("""
    al dkk hlm no vol vs dll dsb dr prof cf ca pp ed eds eg ie sn hum sos pd ma mhum msn ssn spd
    jl tbk st
""".split())


def visible_words(text):
    """Lower-case words a reader sees, without layout commands and stopwords."""
    text = LAYOUT_COMMAND.sub(' ', text)
    return [word for word in re.findall(r'[^\W_]{2,}|\d+', text.casefold())
            if word not in STOPWORDS]


def slug(text):
    """ID derived from a heading title, e.g. 'Rumusan Masalah' -> 'rumusan-masalah'."""
    return "-".join(re.findall(r'[^\W_]+', re.sub(r'\\[a-zA-Z@]+\*?', ' ', text).casefold()))


# Front-matter pages pair by role, so pages added between them stay unpaired.
FRONTMATTER_ROLES = {"judul": "cover", "sampul": "cover", "pengesahan": "approval",
                     "abstrak": "abstract-id", "abstract": "abstract-en"}
ROLE_NAMES = {"cover": "HALAMAN JUDUL", "approval": "HALAMAN PENGESAHAN",
              "abstract-id": "ABSTRAK", "abstract-en": "ABSTRACT"}


def frontmatter_identity(text):
    """Match source roles independently of a visible heading or its TeX styling."""
    # A contents entry names the page directly, e.g. HALAMAN PERNYATAAN.
    contents = re.search(r'\\addcontentsline\{toc\}\{[^{}]*\}\{([^{}]*)\}', text)
    if contents:
        title = " ".join(re.sub(r'\\[a-zA-Z]+\*?|[{}]', ' ', contents.group(1)).casefold().split())
        title = title.removeprefix("halaman ")
        return ("frontmatter", FRONTMATTER_ROLES.get(title, title))
    plain = re.sub(r'\\(?:begin|end)\{[^{}]*\}', '', text)
    plain = re.sub(r'\\[a-zA-Z]+\*?', '', plain)
    plain = re.sub(r'[{}]', '', plain).casefold()
    if re.search(r'^\s*abstrak\s*$|\bkata kunci\s*:', plain, re.MULTILINE):
        return ("frontmatter", "abstract-id")
    if re.search(r'^\s*abstract\s*$|\bkeywords\s*:', plain, re.MULTILINE):
        return ("frontmatter", "abstract-en")
    if "halaman pengesahan" in plain:
        return ("frontmatter", "approval")
    if r"\begingroup" in text and ("skripsi" in plain or "cover" in plain):
        return ("frontmatter", "cover")
    return None


@dataclass
class Block:
    kind: str                 # "page", "heading", "chunk", or "break"
    text: str = ""            # chunk source, heading title source, or page display name
    key: str = ""             # page role or heading ID
    prefix: str = ""          # heading command and leading arguments, e.g. r"\thesischapter{I}"
    level: int = 0            # 0 chapter, 1 section, 2 subsection, 3 subsubsection
    numbered: bool = True
    owner: int = -1           # index of the page or heading a chunk belongs to
    items: int = 0            # list items in a chunk that is a list environment
    words: list = field(default_factory=list)
    label: str = ""           # original reference target, retained on its own side


def _at_line_start(text, pos):
    return not text[text.rfind("\n", 0, pos) + 1:pos].strip()


def _parse_heading(text, pos, name):
    """Return (heading block, end) for a heading command at pos, or None."""
    base = name.rstrip("*")
    match = re.compile(r'\\' + base + r'(\*?)[ \t]*(\[[^\]]*\])?[ \t]*').match(text, pos)
    try:
        if base == "thesischapter":
            _, end = read_braced_argument(text, match.end())
            prefix_end = end
            title, end = read_braced_argument(text, end)
        else:
            prefix_end = match.end()
            title, end = read_braced_argument(text, prefix_end)
    except ValueError:
        return None
    label = HEADING_LABEL.match(text, end)
    if label:
        end = label.end()
    key = label.group(1).split(":", 1)[-1] if label else slug(title)
    return Block("heading", title, key, text[pos:prefix_end].rstrip(), HEADING_LEVELS[base],
                 numbered=not match.group(1), words=visible_words(title),
                 label=label.group(1) if label else ""), end


def parse_blocks(text):
    """Split a cleaned manuscript into headings, chunks, and page breaks."""
    blocks = []
    start = pos = braces = groups = 0
    environments = []

    def flush(end):
        chunk = text[start:end].strip()
        if chunk:
            blocks.append(Block("chunk", chunk))

    while pos < len(text):
        char = text[pos]
        if char == "\\":
            control = CONTROL.match(text, pos)
            name, end = control.group(1), control.end()
            if name in ("begin", "end"):
                environment = ENVIRONMENT_NAME.match(text, end)
                if environment:
                    end = environment.end()
                    standalone = environment.group(1).rstrip('*') in STANDALONE_ENVIRONMENTS
                    if name == "begin":
                        if standalone and braces == groups == 0 and not environments:
                            flush(pos)
                            start = pos
                        environments.append(environment.group(1))
                        if environment.group(1).rstrip('*') in LITERAL_ENVIRONMENTS:
                            closing = text.find(r"\end{" + environment.group(1) + "}", end)
                            if closing < 0:
                                raise ValueError(f"Unclosed literal environment: {environment.group(1)}")
                            end = closing
                    elif environments:
                        environments.pop()
                        if standalone and braces == groups == 0 and not environments:
                            flush(end)
                            start = end
            elif name in ("begingroup", "["):
                if name == "[" and braces == groups == 0 and not environments:
                    flush(pos)
                    start = pos
                groups += 1
            elif name in ("endgroup", "]"):
                groups -= 1
                if name == "]" and braces == groups == 0 and not environments:
                    flush(end)
                    start = end
            elif braces == 0 and groups == 0 and not environments:
                if name in ("newpage", "clearpage"):
                    flush(pos)
                    blocks.append(Block("break"))
                    start = end
                elif name == "par":
                    flush(pos)
                    start = end
                elif name.rstrip('*') == "includegraphics" and _at_line_start(text, pos):
                    graphic_stop = graphic_end(text, pos)
                    line_end = text.find('\n', graphic_stop) if graphic_stop is not None else -1
                    if graphic_stop is not None and not text[graphic_stop:line_end if line_end >= 0 else len(text)].strip():
                        flush(pos)
                        start = pos
                        end = graphic_stop
                        flush(end)
                        start = end
                elif name.rstrip("*") in HEADING_LEVELS and _at_line_start(text, pos):
                    heading = _parse_heading(text, pos, name)
                    if heading:
                        flush(pos)
                        blocks.append(heading[0])
                        start = end = heading[1]
            pos = end
            continue
        if char == "{":
            braces += 1
        elif char == "}":
            braces -= 1
        elif char == "\n" and braces == 0 and groups == 0 and not environments:
            blank = BLANK_LINE.match(text, pos)
            if blank:
                flush(pos)
                start = pos = blank.end()
                continue
        pos += 1
    flush(len(text))
    return _attach_owners(_mark_pages(blocks))


def _mark_pages(blocks):
    """Put a role anchor before each front-matter page (text before the first heading)."""
    first_heading = next((i for i, block in enumerate(blocks) if block.kind == "heading"), len(blocks))
    result, page = [], []

    def close_page():
        if any(block.kind == "chunk" for block in page):
            source = "\n\n".join(block.text for block in page)
            role = frontmatter_identity(source)
            contents = re.search(r'\\addcontentsline\{toc\}\{[^{}]*\}\{([^{}]*)\}', source)
            key = role[1] if role else ""
            name = contents.group(1) if contents else ROLE_NAMES.get(key, key.upper())
            result.append(Block("page", name, key))
        result.extend(page)
        page.clear()

    for block in blocks[:first_heading]:
        if block.kind == "break":
            close_page()
            result.append(block)
        else:
            page.append(block)
    close_page()
    return result + blocks[first_heading:]


def _attach_owners(blocks):
    """Drop navigation commands and record which page or heading owns each chunk."""
    result, owner = [], -1
    for block in blocks:
        if block.kind == "chunk":
            block.text = NAVIGATION.sub('', block.text).strip()
            if not block.text:
                continue
            block.owner = owner
            block.words = visible_words(block.text)
            if LIST_START.search(block.text):
                block.items = len(re.findall(r'\\item\b', block.text))
        result.append(block)
        if block.kind in ("page", "heading"):
            owner = len(result) - 1
    return result


class Vectors:
    """Unit-length TF-IDF vectors: words shared by many documents weigh little."""

    def __init__(self, documents):
        counts = [Counter(words) for words in documents]
        frequency = Counter(word for count in counts for word in count)
        total = len(documents)
        self.vectors = []
        for count in counts:
            vector = {word: (1 + math.log(n)) * (math.log((total + 1) / (frequency[word] + 1)) + 1)
                      for word, n in count.items()}
            norm = math.sqrt(sum(weight * weight for weight in vector.values())) or 1.0
            self.vectors.append({word: weight / norm for word, weight in vector.items()})

    def cosine(self, i, j):
        a, b = self.vectors[i], self.vectors[j]
        if len(a) > len(b):
            a, b = b, a
        return sum(weight * b.get(word, 0.0) for word, weight in a.items())


def align_sequences(old_count, new_count, gain):
    """
    Order-preserving alignment maximizing the summed gains of paired items.
    gain(i, j) returns a positive number for an acceptable pair, else None.
    Unpaired items return None for the other side; between two pairs, old
    items precede new items.
    """
    gains = [[gain(i, j) for j in range(new_count)] for i in range(old_count)]
    best = [[0.0] * (new_count + 1) for _ in range(old_count + 1)]
    for i in range(old_count - 1, -1, -1):
        row, below = best[i], best[i + 1]
        for j in range(new_count - 1, -1, -1):
            value = max(below[j], row[j + 1])
            if gains[i][j] is not None:
                value = max(value, below[j + 1] + gains[i][j])
            row[j] = value
    pairs, i, j = [], 0, 0
    while i < old_count or j < new_count:
        if (i < old_count and j < new_count and gains[i][j] is not None
                and best[i][j] == best[i + 1][j + 1] + gains[i][j]):
            pairs.append((i, j))
            i, j = i + 1, j + 1
        elif i < old_count and (j == new_count or best[i][j] == best[i + 1][j]):
            pairs.append((i, None))
            i += 1
        else:
            pairs.append((None, j))
            j += 1
    return pairs


@dataclass
class Fragment:
    core: str                 # sentence, list item, line, or structure source
    tail: str = ""            # whitespace that followed it in the source
    words: list = field(default_factory=list)   # content words, for similarity
    visible: bool = False     # prints any text, even only stopwords ("Oleh:")
    match: "Fragment" = None
    rendered: str = None
    same: int = 0             # words shared with the counterpart


def split_fragments(text):
    """Split a chunk into sentences, list items, lines, and environment markers."""
    cuts, braces, math_mode, atomic = {0}, 0, False, []
    pos = 0
    while pos < len(text):
        char = text[pos]
        if char == "\\":
            control = CONTROL.match(text, pos)
            name, end = control.group(1), control.end()
            if name in ("begin", "end"):
                environment = ENVIRONMENT_NAME.match(text, end)
                env = environment.group(1) if environment else ""
                if environment:
                    end = environment.end()
                if ATOMIC_ENVIRONMENTS.fullmatch(env):
                    if name == "begin":
                        if not atomic and braces == 0:
                            cuts.add(pos)
                        atomic.append(env)
                        if env.rstrip('*') in LITERAL_ENVIRONMENTS:
                            closing = text.find(r"\end{" + env + "}", end)
                            if closing < 0:
                                raise ValueError(f"Unclosed literal environment: {env}")
                            end = closing
                    elif atomic:
                        atomic.pop()
                        if not atomic and braces == 0:
                            cuts.add(end)
                elif not atomic and braces == 0 and not math_mode:
                    # Arguments of an environment start belong to its marker.
                    if name == "begin":
                        end = re.compile(r'(?:\s*\[[^\]]*\])?(?:\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})*').match(text, end).end()
                    cuts.update((pos, end))
            elif name == "[" and not atomic and braces == 0:
                cuts.add(pos)
                atomic.append("[")
            elif name == "]" and atomic and atomic[-1] == "[":
                atomic.pop()
                if not atomic and braces == 0:
                    cuts.add(end)
            elif not atomic and braces == 0 and not math_mode:
                if name == "item":
                    cuts.add(pos)
                elif name in ("\\", "par"):
                    optional = re.compile(r'\*?(?:\s*\[[^\]]*\])?').match(text, end) if name == "\\" else None
                    cuts.add(optional.end() if optional else end)
            pos = end
            continue
        if char == "{":
            braces += 1
        elif char == "}":
            braces -= 1
        elif char == "$" and not atomic:
            math_mode = not math_mode
        elif not atomic and braces == 0 and not math_mode:
            if char == "\n":
                blank = BLANK_LINE.match(text, pos)
                if blank:
                    cuts.add(blank.end())
                else:
                    # A line opening with a layout command (\noindent, \vspace,
                    # \hfill) starts a new unit; inline commands continue prose.
                    command = BLOCK_LINE.match(text, pos + 1)
                    if command and command.group(1) not in INLINE_COMMANDS:
                        cuts.add(command.start(1) - 1)
            elif char in ".?!" and _ends_sentence(text, pos):
                cuts.add(pos + 1)
        pos += 1
    fragments = []
    edges = sorted(cut for cut in cuts if 0 <= cut <= len(text)) + [len(text)]
    for begin, end in pairwise(edges):
        piece = text[begin:end]
        if not piece:
            continue
        core = piece.rstrip()
        if not core:
            if fragments:
                fragments[-1].tail += piece
            continue
        lead = piece[:len(piece) - len(piece.lstrip())]
        if lead and fragments:
            fragments[-1].tail += lead
            core = core.lstrip()
        fragments.append(Fragment(core, piece[len(piece.rstrip()):], visible_words(core),
                                  bool(VISIBLE_OBJECT.search(core) or
                                       re.search(r'[^\W_]', LAYOUT_COMMAND.sub(' ', core)))))
    return fragments


def _ends_sentence(text, pos):
    """True when the punctuation at pos ends a sentence."""
    if not SENTENCE_GAP.match(text, pos + 1):
        return False
    if text[pos] != ".":
        return True
    # Initials (J.S.) and abbreviations (et al., hlm.) do not end a sentence.
    letters = re.search(r'[^\W\d_]+$', text[max(0, pos - 40):pos])
    if not letters:
        return True
    stem = letters.group(0).casefold()
    return len(stem) > 1 and stem not in ABBREVIATIONS


def _printed_text(core):
    """What a fragment prints, without layout commands or line breaks; case kept."""
    text = LAYOUT_COMMAND.sub(' ', re.sub(r'\\\\\*?(?:\[[^\]]*\])?', ' ', core))
    return " ".join(re.sub(r'(?<!\\)[{}]', ' ', text).split())


def _shared_words(old_group, new_group):
    matcher = SequenceMatcher(None, [w for f in old_group for w in f.words],
                              [w for f in new_group for w in f.words], autojunk=False)
    return sum(block.size for block in matcher.get_matching_blocks())


def _render_pair(old_group, new_group, same, tone="strong"):
    """Render paired fragments; groups of two cover a split or merged sentence."""
    for fragment in old_group:
        fragment.match = new_group[0]
    for fragment in new_group:
        fragment.match = old_group[0]
    old_group[0].same, new_group[0].same = same, same
    if len(old_group) == len(new_group) == 1 and old_group[0].core == new_group[0].core:
        old_group[0].rendered = old_group[0].core
        new_group[0].rendered = new_group[0].core
        return
    old_rendered, new_rendered = render_group([f.core for f in old_group], [f.core for f in new_group], tone)
    for fragment, rendered in zip(old_group, old_rendered):
        fragment.rendered = rendered.rstrip(" ")
    for fragment, rendered in zip(new_group, new_rendered):
        fragment.rendered = rendered.rstrip(" ")


def render_unpaired(text, side):
    """Pale highlight for text without a counterpart; tables get one block background."""
    if TABULAR.search(text):
        color = "delpl" if side == "old" else "inspl"
        return f"\\begin{{diffmath}}{{{color}}}\n{text}\n\\end{{diffmath}}"
    pair = word_level_render(text, "", "pale") if side == "old" else word_level_render("", text, "pale")
    return pair[0 if side == "old" else 1].rstrip(" ")


def compare_fragments(old_fragments, new_fragments):
    """
    Pair sentences, list items, and lines by word similarity, in order. A
    sentence may also pair with two consecutive sentences, so a split or a
    merge keeps its shared words. Identical printed text pairs first.
    """
    old = [fragment for fragment in old_fragments if fragment.visible]
    new = [fragment for fragment in new_fragments if fragment.visible]
    old_keys = [_printed_text(f.core) for f in old]
    new_keys = [_printed_text(f.core) for f in new]
    old_sets = [set(f.words) for f in old]
    new_sets = [set(f.words) for f in new]
    cache = {}

    def gain(i, di, j, dj):
        if (i, di, j, dj) in cache:
            return cache[i, di, j, dj]
        value = None
        if di == dj == 1 and old_keys[i] == new_keys[j]:
            value = 1.05 - SENTENCE_THRESHOLD
            cache[i, di, j, dj] = value
            return value
        a = [w for f in old[i:i + di] for w in f.words]
        b = [w for f in new[j:j + dj] for w in f.words]
        if a and b and set().union(*old_sets[i:i + di]) & set().union(*new_sets[j:j + dj]):
            matcher = SequenceMatcher(None, a, b, autojunk=False)
            # A merge must clearly beat pairing the pieces one by one.
            needed = SENTENCE_THRESHOLD + (0.1 if di + dj > 2 else 0.0)
            if matcher.real_quick_ratio() > needed and matcher.quick_ratio() > needed:
                ratio = matcher.ratio()
                # Short lines must agree in most words to count as the same line.
                if ratio > needed and not (min(len(a), len(b)) <= 3 and ratio < 0.66):
                    value = ratio - SENTENCE_THRESHOLD
        cache[i, di, j, dj] = value
        return value

    n, m = len(old), len(new)
    best = [[0.0] * (m + 1) for _ in range(n + 1)]
    choice = {}
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            value, step = best[i + 1][j], (1, 0)
            if best[i][j + 1] > value:
                value, step = best[i][j + 1], (0, 1)
            for di, dj in ((1, 1), (1, 2), (2, 1)):
                if i + di <= n and j + dj <= m:
                    g = gain(i, di, j, dj)
                    if g is not None and best[i + di][j + dj] + g > value:
                        value, step = best[i + di][j + dj] + g, (di, dj)
            best[i][j], choice[i, j] = value, step

    gap_old, gap_new = [], []

    def pair_in_place(a, b):
        # Changes stay pale unless the two share most of their wording.
        same = _shared_words([a], [b])
        similar = 2 * same / max(1, len(a.words) + len(b.words)) > SENTENCE_THRESHOLD
        _render_pair([a], [b], same, "strong" if similar else "pale")

    def close_gap():
        # Between two paired sentences, list items keep their number as an
        # identity: item k pairs with item k. A lone rewritten sentence pairs
        # with the lone sentence that replaced it.
        old_items = [f for f in gap_old if f.core.startswith(r"\item")]
        new_items = [f for f in gap_new if f.core.startswith(r"\item")]
        for a, b in zip(old_items, new_items):
            pair_in_place(a, b)
        old_rest = [f for f in gap_old if f.match is None]
        new_rest = [f for f in gap_new if f.match is None]
        if len(old_rest) == len(new_rest) == 1:
            pair_in_place(old_rest[0], new_rest[0])
        gap_old.clear()
        gap_new.clear()

    i = j = 0
    while i < n or j < m:
        step = choice.get((i, j), (1, 0) if i < n else (0, 1))
        if i >= n:
            step = (0, 1)
        elif j >= m:
            step = (1, 0)
        di, dj = step
        if di and dj:
            close_gap()
            _render_pair(old[i:i + di], new[j:j + dj], _shared_words(old[i:i + di], new[j:j + dj]))
        elif di:
            gap_old.append(old[i])
        else:
            gap_new.append(new[j])
        i, j = i + di, j + dj
    close_gap()
    for side, fragments in (("old", old), ("new", new)):
        for fragment in fragments:
            if fragment.match is None:
                fragment.rendered = render_unpaired(fragment.core, side)


def compare_page(old, new):
    """Compare all words of two structured pages at once, then render line by line."""
    old_rendered, new_rendered = render_group([f.core for f in old], [f.core for f in new])
    for fragment, rendered in zip(old, old_rendered):
        fragment.rendered, fragment.match = rendered.rstrip(" "), new[0]
    for fragment, rendered in zip(new, new_rendered):
        fragment.rendered, fragment.match = rendered.rstrip(" "), old[0]
    old[0].same = new[0].same = _shared_words(old, new)


def render_fragments(fragments):
    return "".join((fragment.rendered if fragment.visible else fragment.core) + fragment.tail
                   for fragment in fragments).strip()


@dataclass
class Row:
    old: list = field(default_factory=list)
    new: list = field(default_factory=list)
    new_page: bool = False


class Comparison:
    """Pair the blocks of two manuscripts and render them as side-by-side rows."""

    def __init__(self, old_text, new_text):
        self.old = parse_blocks(old_text)
        self.new = parse_blocks(new_text)
        self.sides = {"old": self.old, "new": self.new}
        self.object_numbers, self.reference_numbers = {}, {"old": {}, "new": {}}
        self.reference_titles = {"old": {}, "new": {}}
        self._index_numbers()
        self._index_features()
        self.counterpart = {}
        self.moved = set()
        # Identities first: pages by role and headings by ID anchor the rows.
        anchors = self._pair_anchors()
        for i, j in anchors:
            self.counterpart["old", i] = j
            self.counterpart["new", j] = i
        self._find_heading_moves()
        # Then text, only between the same two anchors.
        self.pairs = self._pair_segments(anchors)
        for i, j in self.pairs:
            if i is not None and j is not None:
                self.counterpart["old", i] = j
                self.counterpart["new", j] = i
        self._find_chunk_moves()
        self.fragments = {}
        self.rows = self._build_rows()
        self._compare_rows()

    # Similarity features -------------------------------------------------

    def _index_numbers(self):
        """Track the source's ordinary figure/table and heading counter order."""
        for side, blocks in self.sides.items():
            counters = {"figure": 0, "table": 0, "equation": 0}
            chapter, headings = "", [0, 0, 0]
            for index, block in enumerate(blocks):
                if block.kind == "heading":
                    if block.level == 0:
                        chapter, headings = block.prefix, [0, 0, 0]
                    elif block.numbered:
                        headings[block.level - 1] += 1
                        headings[block.level:] = [0] * (3 - block.level)
                        if block.label:
                            self.reference_numbers[side][block.label] = (chapter, tuple(headings[:block.level]))
                    if block.label:
                        self.reference_titles[side][block.label] = block.text
                elif block.kind == "chunk":
                    kind = chunk_type(block.text)
                    if kind in ("figure", "table"):
                        # Starred captions deliberately carry no number.
                        count = len(re.findall(r'\\caption(?![A-Za-z*])', block.text))
                        if not count:
                            continue
                        counters[kind] += count
                        self.object_numbers[side, index] = counters[kind]
                        for label in re.findall(r'\\label\{([^{}]+)\}', block.text):
                            self.reference_numbers[side][label] = (kind, counters[kind])
                    else:
                        rows = equation_rows(block.text)
                        for row in rows:
                            counters["equation"] += 1
                            for label in re.findall(r'\\label\{([^{}]+)\}', row):
                                self.reference_numbers[side][label] = ("equation", counters["equation"])
                        if rows:
                            self.object_numbers[side, index] = counters["equation"]

    def _number_changed(self, side, index, other_index):
        other_side = "new" if side == "old" else "old"
        return self.object_numbers.get((side, index)) != self.object_numbers.get((other_side, other_index))

    def _index_features(self):
        everything = [("old", i, block) for i, block in enumerate(self.old)] + \
                     [("new", j, block) for j, block in enumerate(self.new)]
        self.position = {}
        titles, units, chunks = [], [], []
        unit_words = {}
        for side, index, block in everything:
            if block.kind == "chunk" and block.owner >= 0:
                unit_words.setdefault((side, block.owner), []).extend(block.words)
        for side, index, block in everything:
            if block.kind == "heading":
                self.position["title", side, index] = len(titles)
                titles.append(block.words)
            if block.kind in ("heading", "page"):
                self.position["unit", side, index] = len(units)
                units.append(unit_words.get((side, index), []))
            if block.kind == "chunk":
                self.position["chunk", side, index] = len(chunks)
                chunks.append(block.words)
        self.vectors = {"title": Vectors(titles), "unit": Vectors(units), "chunk": Vectors(chunks)}
        self.unit_words = unit_words

    def _cosine(self, space, i, j):
        return self.vectors[space].cosine(self.position[space, "old", i], self.position[space, "new", j])

    def heading_scores(self, i, j):
        """Return (score, title similarity, content similarity or None)."""
        a, b = self.old[i], self.new[j]
        title = self._cosine("title", i, j)
        content = (self._cosine("unit", i, j)
                   if self.unit_words.get(("old", i)) and self.unit_words.get(("new", j)) else None)
        if a.key and a.key == b.key:
            return 1.0, title, content
        if content is None:
            return title, title, None
        return max(title, 0.85 * content, (title + content) / 2), title, content

    def score(self, i, j):
        a, b = self.old[i], self.new[j]
        if a.kind != b.kind:
            return 0.0
        if a.kind == "page":
            return 1.0 if a.key == b.key else 0.0
        if a.kind == "heading":
            return self.heading_scores(i, j)[0]
        if chunk_type(a.text) != chunk_type(b.text):
            return 0.0
        if source_key(a.text) == source_key(b.text):
            return 1.1  # exact paragraphs anchor repeated or near-identical passages
        old_id, new_id = object_id(a.text), object_id(b.text)
        if old_id and new_id:
            return 1.0 if old_id == new_id else 0.0
        similarity = self._cosine("chunk", i, j)
        # Lists between the same two anchors compare item by item even when
        # their wording changed: an item number is an identity.
        if a.items and b.items:
            similarity = max(similarity, THRESHOLD["chunk"] + 0.05)
        return similarity

    # Pairing ------------------------------------------------------------

    def _pair_anchors(self):
        """Pair pages and headings in reading order; return the (old, new) pairs."""
        old_anchors = [i for i, block in enumerate(self.old) if block.kind in ("page", "heading")]
        new_anchors = [j for j, block in enumerate(self.new) if block.kind in ("page", "heading")]

        def gain(a, b):
            i, j = old_anchors[a], new_anchors[b]
            kind = self.old[i].kind
            if kind != self.new[j].kind:
                return None
            value = self.score(i, j)
            return WEIGHT[kind] * (value - THRESHOLD[kind]) if value > THRESHOLD[kind] else None

        return [(old_anchors[a], new_anchors[b])
                for a, b in align_sequences(len(old_anchors), len(new_anchors), gain)
                if a is not None and b is not None]

    def _pair_segments(self, anchors):
        """All blocks in reading order: anchor pairs, and paragraphs paired between them."""
        old_items = [i for i, block in enumerate(self.old) if block.kind != "break"]
        new_items = [j for j, block in enumerate(self.new) if block.kind != "break"]
        old_at = {index: position for position, index in enumerate(old_items)}
        new_at = {index: position for position, index in enumerate(new_items)}
        pairs, old_start, new_start = [], 0, 0
        for i, j in anchors + [(None, None)]:
            old_end = old_at[i] if i is not None else len(old_items)
            new_end = new_at[j] if j is not None else len(new_items)
            pairs.extend(self._pair_segment(old_items[old_start:old_end], new_items[new_start:new_end]))
            if i is not None:
                pairs.append((i, j))
            old_start, new_start = old_end + 1, new_end + 1
        return pairs

    def _pair_segment(self, old_items, new_items):
        """Pair paragraphs between two anchor pairs; other blocks stay unpaired."""
        moved_owners = {(side, index) for side, index in self.moved}

        def gain(a, b):
            k, m = old_items[a], new_items[b]
            if self.old[k].kind != "chunk" or self.new[m].kind != "chunk":
                return None
            # Text under a moved heading is compared at the moved heading.
            if ("old", self.old[k].owner) in moved_owners or ("new", self.new[m].owner) in moved_owners:
                return None
            old_owner, new_owner = self.old[k].owner, self.new[m].owner
            if (("old", old_owner) in self.counterpart and self.counterpart["old", old_owner] != new_owner
                    or ("new", new_owner) in self.counterpart and self.counterpart["new", new_owner] != old_owner):
                return None
            value = self.score(k, m)
            return value - THRESHOLD["chunk"] if value > THRESHOLD["chunk"] else None

        # Fix exact paragraph anchors first. A collection of merely similar
        # paragraphs must not displace an unchanged paragraph, particularly
        # when successive paragraphs repeat much of the same vocabulary.
        def keys(side, indices):
            return [(chunk_type(self.sides[side][k].text), source_key(self.sides[side][k].text))
                    if self.sides[side][k].kind == "chunk" else (side, k) for k in indices]

        matcher = SequenceMatcher(None, keys("old", old_items), keys("new", new_items), autojunk=False)
        exact = [(a + offset, b + offset) for a, b, count in matcher.get_matching_blocks()
                 for offset in range(count) if gain(a + offset, b + offset) is not None]
        pairs, old_start, new_start = [], 0, 0
        for a, b in exact + [(len(old_items), len(new_items))]:
            pairs.extend((old_start + i if i is not None else None, new_start + j if j is not None else None)
                         for i, j in align_sequences(a - old_start, b - new_start,
                                                     lambda i, j, oi=old_start, nj=new_start: gain(oi + i, nj + j)))
            if a < len(old_items):
                pairs.append((a, b))
            old_start, new_start = a + 1, b + 1
        return [(old_items[a] if a is not None else None, new_items[b] if b is not None else None)
                for a, b in pairs]

    def _find_heading_moves(self):
        """Pair unpaired headings that changed position: an unchanged ID or clearly shared text."""
        lone_old = [i for i, block in enumerate(self.old) if block.kind == "heading" and ("old", i) not in self.counterpart]
        lone_new = [j for j, block in enumerate(self.new) if block.kind == "heading" and ("new", j) not in self.counterpart]
        candidates = []
        for i in lone_old:
            for j in lone_new:
                value, title, content = self.heading_scores(i, j)
                shared_id = self.old[i].key and self.old[i].key == self.new[j].key
                if shared_id or (content or 0) >= MOVE_THRESHOLD or title >= 0.8 and (content or 0) >= 0.3:
                    candidates.append((2.0 if shared_id else value, i, j))
        self._accept_moves(candidates)

    def _find_chunk_moves(self):
        """A paragraph that moved alone, outside a moved section, with clearly shared text."""
        moved_owners = {(side, index) for side, index in self.moved}
        lone_old = [i for i, j in self.pairs if j is None and self.old[i].kind == "chunk"
                    and ("old", self.old[i].owner) not in moved_owners]
        lone_new = [j for i, j in self.pairs if i is None and self.new[j].kind == "chunk"
                    and ("new", self.new[j].owner) not in moved_owners]
        self._accept_moves([(self.score(i, j), i, j) for i in lone_old for j in lone_new
                            if self.score(i, j) >= MOVE_THRESHOLD])

    def _accept_moves(self, candidates):
        for _, i, j in sorted(candidates, reverse=True):
            if ("old", i) in self.counterpart or ("new", j) in self.counterpart:
                continue
            self.counterpart["old", i] = j
            self.counterpart["new", j] = i
            self.moved.update({("old", i), ("new", j)})

    # Rows -----------------------------------------------------------------

    def operations(self):
        """Pairs in reading order, with each side's page breaks in place."""
        ops, next_old, next_new = [], 0, 0

        def breaks(side, upto):
            blocks = self.sides[side]
            start = next_old if side == "old" else next_new
            return [("break", side, k) for k in range(start, upto) if blocks[k].kind == "break"]

        for i, j in self.pairs:
            if i is not None:
                ops.extend(breaks("old", i))
                next_old = i + 1
            if j is not None:
                ops.extend(breaks("new", j))
                next_new = j + 1
            ops.append(("pair", i, j))
        ops.extend(breaks("old", len(self.old)))
        ops.extend(breaks("new", len(self.new)))
        return ops

    def _build_rows(self):
        """Synchronize every paragraph/object pair, leaving insertions a blank side.

        Structured front matter stays together because font/group/layout scopes
        may span its short lines. Body rows remain breakable paracol content;
        synchronization adds space only up to the taller counterpart.
        """
        rows = []
        new_page, structured = False, False
        for op in self.operations():
            if op[0] == "break":
                new_page = True
                continue
            _, i, j = op
            kind = (self.old[i] if i is not None else self.new[j]).kind
            if kind == "page":
                structured = all(self._structured_page(side, index) for side, index in
                                 (("old", i), ("new", j)) if index is not None)
            elif kind == "heading" or new_page:
                structured = False
            if not rows or new_page or kind != "chunk" or not structured:
                rows.append(Row(new_page=new_page))
            row = rows[-1]
            new_page = False
            if i is not None:
                row.old.append(i)
            if j is not None:
                row.new.append(j)
        return rows

    def _structured_page(self, side, owner):
        fragments = [f for k in self._chunks_of(side, owner)
                     for f in split_fragments(self.sides[side][k].text) if f.visible]
        return bool(fragments) and sum(len(f.words) for f in fragments) <= LINE_WORDS * len(fragments)

    def _chunks_of(self, side, owner):
        return [k for k, block in enumerate(self.sides[side])
                if block.kind == "chunk" and block.owner == owner]

    def _compare_rows(self):
        """Compare sentences within each row, and each moved part with its counterpart."""
        groups = []
        for side, index in sorted(self.moved):
            if side != "old":
                continue
            other = self.counterpart["old", index]
            if self.old[index].kind == "heading":
                # A moved section keeps its unpaired paragraphs with it.
                groups.append(([k for k in self._chunks_of("old", index) if ("old", k) not in self.counterpart],
                               [k for k in self._chunks_of("new", other) if ("new", k) not in self.counterpart]))
            else:
                groups.append(([index], [other]))
        grouped = set()
        for old_chunks, new_chunks in groups:
            # A moved section's children still have paragraph counterparts.
            # Record them so unchanged children receive only the section move
            # marker, rather than being mistaken for deletions and insertions.
            pairs = align_sequences(len(old_chunks), len(new_chunks),
                                    lambda a, b: self.score(old_chunks[a], new_chunks[b])
                                    if self.score(old_chunks[a], new_chunks[b]) > THRESHOLD["chunk"] else None)
            for a, b in pairs:
                left = [old_chunks[a]] if a is not None else []
                right = [new_chunks[b]] if b is not None else []
                if left and right:
                    self.counterpart["old", left[0]] = right[0]
                    self.counterpart["new", right[0]] = left[0]
                self._compare_chunks(left, right)
            grouped.update(("old", k) for k in old_chunks)
            grouped.update(("new", k) for k in new_chunks)
        for row in self.rows:
            # Short lines of a paired front-matter page (cover, approval)
            # compare word by word across the whole page.
            page = (any(self.old[i].kind == "page" for i in row.old)
                    and any(self.new[j].kind == "page" for j in row.new))
            self._compare_chunks([i for i in row.old if self.old[i].kind == "chunk" and ("old", i) not in grouped],
                                 [j for j in row.new if self.new[j].kind == "chunk" and ("new", j) not in grouped],
                                 structured=page)

    def _compare_chunks(self, old_chunks, new_chunks, structured=False):
        old_fragments = {k: split_fragments(self.old[k].text) for k in old_chunks}
        new_fragments = {k: split_fragments(self.new[k].text) for k in new_chunks}
        old_all = [f for k in old_chunks for f in old_fragments[k] if f.visible]
        new_all = [f for k in new_chunks for f in new_fragments[k] if f.visible]
        identical = [self.old[k].text for k in old_chunks] == [self.new[k].text for k in new_chunks]
        if structured and not identical and old_all and new_all and all(
                sum(len(f.words) for f in side) <= LINE_WORDS * len(side) for side in (old_all, new_all)):
            compare_page(old_all, new_all)
            self.fragments.update({("old", k): fragments for k, fragments in old_fragments.items()})
            self.fragments.update({("new", k): fragments for k, fragments in new_fragments.items()})
            return
        # Identical paragraphs need no sentence alignment.
        if identical:
            for k in old_chunks:
                for fragment in old_fragments[k]:
                    fragment.rendered, fragment.same = fragment.core, len(fragment.words)
            for k in new_chunks:
                for fragment in new_fragments[k]:
                    fragment.rendered, fragment.same = fragment.core, len(fragment.words)
        else:
            compare_fragments([f for k in old_chunks for f in old_fragments[k]],
                              [f for k in new_chunks for f in new_fragments[k]])
        self.fragments.update({("old", k): fragments for k, fragments in old_fragments.items()})
        self.fragments.update({("new", k): fragments for k, fragments in new_fragments.items()})

    # Rendering ------------------------------------------------------------

    def heading_label(self, side, index):
        return f"diff{side[0]}{index}"

    def render_heading(self, side, index):
        block = self.sides[side][index]
        other_index = self.counterpart.get((side, index))
        other = (self.new if side == "old" else self.old)[other_index] if other_index is not None else None
        if other is None:
            pair = word_level_render(block.text, "", "pale") if side == "old" else word_level_render("", block.text, "pale")
            title = pair[0] if side == "old" else pair[1]
        elif other.text == block.text or (other.level != block.level and
                                         source_key(other.text).casefold() == source_key(block.text).casefold()):
            title = block.text  # chapter promotion commonly uppercases the same title
        else:
            old, new = (block, other) if side == "old" else (other, block)
            title = word_level_render(old.text, new.text)[0 if side == "old" else 1]
        heading = f"{block.prefix}{{{title.strip()}}}"
        if other is not None and (other.level != block.level or other.numbered != block.numbered):
            heading = r"\diffmoved{tingkat atau penomoran judul diubah}" + "\n" + heading
        if block.level > 0 and block.numbered:
            heading += rf"\label{{{self.heading_label(side, index)}}}"
        if block.label:
            heading += rf"\label{{{block.label}}}"
        if (side, index) in self.moved:
            note = "dipindahkan ke posisi baru" if side == "old" else "dipindahkan dari posisi lama"
            heading = rf"\diffmoved{{{note}}}" + "\n" + heading
        return heading

    def render_block(self, side, index):
        block = self.sides[side][index]
        if block.kind == "heading":
            return self.render_heading(side, index)
        if block.kind == "chunk":
            text = render_fragments(self.fragments[side, index])
            other_index = self.counterpart.get((side, index))
            other_side = "new" if side == "old" else "old"
            other = self.sides[other_side][other_index] if other_index is not None else None
            # Some opaque commands affect layout or print objects but cannot
            # safely enter soul. If word rendering could mark nothing, flag
            # the complete balanced block rather than silently losing the edit.
            changed = other is None or content_key(block.text) != content_key(other.text)
            peer_text = render_fragments(self.fragments[other_side, other_index]) if other is not None else ""
            if (changed and text and not has_highlight(text) and not has_highlight(peer_text)
                    and any(f.visible for f in self.fragments[side, index])):
                color = ("del" if side == "old" else "ins") + ("hl" if other is not None else "pl")
                text = f"\\begin{{diffmath}}{{{color}}}\n{text}\n\\end{{diffmath}}"
            kind = chunk_type(block.text)
            if (kind in ("figure", "table") and (side, index) in self.object_numbers and
                    (changed or self._number_changed(side, index, other_index))):
                color = ("del" if side == "old" else "ins") + ("hl" if other is not None else "pl")
                text = rf"\diffcaptionlabel{{{kind}}}{{{color}}}" + "\n" + text
            elif (kind not in ("figure", "table") and equation_rows(block.text) and
                  other is not None and self._number_changed(side, index, other_index)):
                color = "delhl" if side == "old" else "inshl"
                text = rf"\diffequationlabel{{{color}}}" + "\n" + text
            # A stable target can acquire a different printed number after an
            # earlier insertion. Highlight that resolved reference as well.
            def reference(match):
                key = match.group(2)
                values = self.reference_titles if match.group(1).rstrip('*') == "nameref" else self.reference_numbers
                old_number = values["old"].get(key)
                new_number = values["new"].get(key)
                if old_number is not None and new_number is not None and old_number != new_number:
                    color = "delhl" if side == "old" else "inshl"
                    return rf"\diffinline{{{color}}}{{{match.group(0)}}}"
                return match.group(0)
            text = re.sub(r'\\(ref|eqref|autoref|nameref)\*?\{([^{}]+)\}', reference, text)
            if (side, index) in self.moved:
                note = "dipindahkan ke posisi baru" if side == "old" else "dipindahkan dari posisi lama"
                text = rf"\diffmoved{{{note}}}" + "\n" + text
            return text
        return ""

    def render(self):
        """Return the paracol body for all rows."""
        out = [r"\begin{paracol}{2}"]
        emitted = False
        for row in self.rows:
            if row.new_page and emitted:
                out.extend([r"\end{paracol}", r"\newpage", r"\begin{paracol}{2}"])
            left = "\n\n".join(filter(None, (self.render_block("old", i) for i in row.old)))
            right = "\n\n".join(filter(None, (self.render_block("new", j) for j in row.new)))
            out.extend([r"\begin{leftside}", left, r"\par\end{leftside}", r"\switchcolumn",
                        r"\begin{rightside}", right, r"\par\end{rightside}", r"\switchcolumn*"])
            emitted = True
        out.append(r"\end{paracol}")
        return "\n".join(out)

    # Change map -----------------------------------------------------------

    def unit_counts(self, side, index):
        """Return (words, words shared with the counterpart text) under a page or heading."""
        total = same = 0
        for k in self._chunks_of(side, index):
            for fragment in self.fragments.get((side, k), []):
                total += len(fragment.words)
                same += fragment.same
        return total, same

    def _reference(self, side, index, chapters):
        block = self.sides[side][index]
        if block.kind == "chunk":
            kind = chunk_type(block.text)
            name = {"figure": "Gambar", "table": "Tabel"}.get(kind, "Persamaan")
            number = self.object_numbers.get((side, index))
            caption = re.search(r'\\caption\*?(?:\[[^\]]*\])?\s*(?=\{)', block.text)
            title = read_braced_argument(block.text, caption.end())[0] if caption else ""
            return f"{name}{' ' + str(number) if number is not None else ''}: {title}".rstrip(': ')
        if block.kind == "page":
            return block.text
        if block.level == 0:
            number = re.search(r'\{([^{}]*)\}$', block.prefix)
            return f"BAB {number.group(1) if number else ''} {block.text}".strip()
        if not block.numbered:
            return block.text
        chapter = chapters.get((side, index), "")
        return rf"{chapter}\ref{{{self.heading_label(side, index)}}} {block.text}"

    def change_map(self):
        """Rows for every page, heading, captioned figure and captioned table."""
        chapters, current = {}, {"old": "", "new": ""}
        for side, blocks in self.sides.items():
            for index, block in enumerate(blocks):
                if block.kind == "heading" and block.level == 0:
                    number = re.search(r'\{([^{}]*)\}$', block.prefix)
                    current[side] = f"{number.group(1)}." if number else ""
                elif block.kind == "heading":
                    chapters[side, index] = current[side]
        entries = []
        for op in self.operations():
            if op[0] != "pair":
                continue
            _, i, j = op
            block = self.old[i] if i is not None else self.new[j]
            if block.kind not in ("page", "heading") and not (
                    block.kind == "chunk" and chunk_type(block.text) in ("figure", "table")):
                continue
            if i is not None and ("old", i) in self.moved:
                continue  # listed once, at its new position
            if j is not None and ("new", j) in self.moved:
                i = self.counterpart["new", j]
            entries.append(self._entry(i, j, chapters))
        return entries

    def _entry(self, i, j, chapters):
        left = self._reference("old", i, chapters) if i is not None else ""
        right = self._reference("new", j, chapters) if j is not None else ""
        if i is None:
            return left, right, "baru", None
        if j is None:
            return left, right, "dihapus", None
        a, b = self.old[i], self.new[j]
        if a.kind == "chunk":
            old_total = sum(len(f.words) for f in self.fragments["old", i])
            new_total = sum(len(f.words) for f in self.fragments["new", j])
            old_same = sum(f.same for f in self.fragments["old", i])
            new_same = sum(f.same for f in self.fragments["new", j])
        else:
            old_total, old_same = self.unit_counts("old", i)
            new_total, new_same = self.unit_counts("new", j)
        total = old_total + new_total
        similarity = (old_same + new_same) / total if total else None
        same_title = (a.text == b.text or a.level != b.level and
                      source_key(a.text).casefold() == source_key(b.text).casefold())
        old_chunks = [i] if a.kind == "chunk" else self._chunks_of("old", i)
        new_chunks = [j] if b.kind == "chunk" else self._chunks_of("new", j)
        unchanged = ([content_key(self.old[k].text) for k in old_chunks] == [content_key(self.new[k].text) for k in new_chunks]
                     and all(not self._number_changed("old", k, self.counterpart.get(("old", k))) for k in old_chunks)
                     and not any(has_highlight(self.render_block(side, k)) for side, chunks in
                                 (("old", old_chunks), ("new", new_chunks)) for k in chunks))
        if similarity is None:
            status = "sama" if unchanged else "diubah"
        else:
            status = ("sama" if unchanged else "diubah sedikit" if similarity >= 0.7
                      else "diubah" if similarity >= 0.3 else "ditulis ulang")
        if not same_title and a.kind == "heading":
            status += ", judul diubah"
        if a.level != b.level or a.numbered != b.numbered:
            status += ", struktur judul diubah"
        if ("new", j) in self.moved:
            status = "dipindahkan, " + status
        return left, right, status, similarity

    def overall_similarity(self):
        total = same = 0
        for fragments in self.fragments.values():
            for fragment in fragments:
                total += len(fragment.words)
                same += fragment.same
        return same / total if total else 1.0


def render_change_map(comparison, left_name, right_name):
    """A full-width table of paired pages, headings, figures and tables."""
    def cell(text):
        return text if text else r"\textemdash"

    lines = [
        r"\section*{PETA PERUBAHAN}",
        rf"\noindent Kiri: \texttt{{{left_name}}}\quad Kanan: \texttt{{{right_name}}}\par",
        rf"\noindent Kata yang sama di kedua versi: {round(100 * comparison.overall_similarity())}\% "
        r"dari seluruh kata teks.\par",
        r"\noindent\diffkey{delpl}{inspl}{Warna pucat: teks tanpa padanan (dihapus, baru, atau ditulis ulang).}\quad "
        r"\diffkey{delhl}{inshl}{Warna tegas: perubahan pada teks atau objek yang berpasangan.}\par",
        r"\noindent Paragraf identik menjadi patokan; paragraf lainnya dipasangkan menurut kemiripan isi "
        r"di antara bagian yang bersesuaian. Sisipan dan penghapusan menyisakan sisi kosong. "
        r"Label gambar dan tabel berwarna bila isi atau nomornya berubah. Persentase kata sama "
        r"mengukur kemiripan kata; perubahan format atau objek tetap diberi status berubah.\par",
        r"\medskip",
        r"\begin{longtable}{@{}p{0.35\linewidth}p{0.35\linewidth}p{0.17\linewidth}r@{}}",
        r"\textbf{Kiri} & \textbf{Kanan} & \textbf{Status} & \textbf{Kata sama}\\ \hline",
        r"\noalign{\smallskip}",
        r"\endhead",
    ]
    for left, right, status, similarity in comparison.change_map():
        percent = f"{round(100 * similarity)}\\%" if similarity is not None else r"\textemdash"
        lines.append(f"{cell(left)} & {cell(right)} & {status} & {percent}\\\\")
    lines.extend([r"\end{longtable}", r"\newpage"])
    return "\n".join(lines)
