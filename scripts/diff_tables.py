r"""
Compare two versions of one table: the table, then its rows, then its cells.

The table is the parent. Its environment and column specification are its
layout; when they changed, the caller keeps one background on the whole
table. Otherwise rows pair in order: identical rows anchor the others, and
rows between two anchors pair by position, or by shared words when the two
sides hold different numbers of rows. A row without a counterpart gets a pale
row color. Paired rows compare cell by cell, and only the changed words of a
cell are highlighted. A cell whose change has no word to highlight (format,
span, or an object) gets a cell color, and a paired row whose change no cell
shows (row spacing) gets a row color. A changed rule is drawn in the deleted
or inserted text color.
"""

import re
from dataclasses import dataclass
from difflib import SequenceMatcher

from diff_layout import SENTENCE_THRESHOLD, align_sequences, visible_words
from diff_tokens import read_braced_argument, read_optional_argument, render_group, tone_colors

CONTROL = re.compile(r'\\([A-Za-z@]+\*?|.)', re.S)
ENVIRONMENT_NAME = re.compile(r'\s*\{([^{}]*)\}')
TABLE_START = re.compile(r'\\begin\{(tabular\*?|tabularx|longtable\*?|array)\}')
ROW_END = re.compile(r'\\\\\*?(?:\s*\[[^\]]*\])?|\\tabularnewline(?![A-Za-z])')
# Rules and row commands that precede a row's first cell, with their braced arguments.
RULE = re.compile(r'\s*\\(hline|cline|toprule|midrule|bottomrule|cmidrule|specialrule|addlinespace'
                  r'|morecmidrules|noalign|rowcolor|endfirsthead|endhead|endfoot|endlastfoot)(?![A-Za-z])')
RULE_ARGUMENTS = {"cline": 1, "cmidrule": 1, "specialrule": 3, "noalign": 1, "rowcolor": 1}
MULTICOLUMN = re.compile(r'\\multicolumn(?![A-Za-z])')
MARK = re.compile(r'\\(?:delhighlight|inhighlight|delpale|inspale|diffinline|diffspace|fcolorbox'
                  r'|diffrow|diffcell|diffrule)(?![A-Za-z])|\\begin\{diffmath\}')
RULE_COLORS = ("deltext", "instext")


def source_key(text):
    return " ".join(text.split())


@dataclass
class Row:
    rules: str      # rules and row commands before the first cell, e.g. "\hline\n"
    cells: list     # cell sources between the & separators, spaces included
    end: str        # the row end (\\, \\[2pt], \tabularnewline), or "" after the last row

    @property
    def key(self):
        return source_key(self.rules), tuple(source_key(cell) for cell in self.cells), source_key(self.end)

    @property
    def has_cells(self):
        """False for the rules after the last row end, which start no row."""
        return bool(self.end or any(cell.strip() for cell in self.cells))

    def render(self, rules, color, cells):
        row_color = rf"\diffrow{{{color}}}" if color else ""
        return rules + row_color + "&".join(cells) + self.end


@dataclass
class Table:
    before: str     # source before \begin, e.g. "{\small "
    opening: str    # \begin{tabularx}{\textwidth}{|l|X|}
    rows: list
    closing: str    # \end{tabularx}
    after: str


def leading_rules(text):
    """Length of the rules and row commands that open a row."""
    pos = 0
    while match := RULE.match(text, pos):
        end = match.end()
        try:
            if match.group(1) == "cmidrule":
                end = re.compile(r'\s*(?:\([^)]*\))?').match(text, end).end()
            end = read_optional_argument(text, end)
            for _ in range(RULE_ARGUMENTS.get(match.group(1), 0)):
                _, end = read_braced_argument(text, end)
        except ValueError:
            break
        pos = end
    # Spaces after the last rule stay with the cell, as before a first cell.
    return len(text[:pos].rstrip())


def split_rows(body):
    """Rows of a table body, split at top-level & and row ends."""
    rows, cells, start, pos, braces, environments = [], [], 0, 0, 0, 0

    def add_row(end):
        cells.append(body[start:pos])
        cut = leading_rules(cells[0])
        rows.append(Row(cells[0][:cut], [cells[0][cut:], *cells[1:]], end))
        cells.clear()

    while pos < len(body):
        char = body[pos]
        if char == "\\":
            row_end = ROW_END.match(body, pos)
            if row_end and not braces and not environments:
                add_row(row_end.group(0))
                start = pos = row_end.end()
                continue
            control = CONTROL.match(body, pos)
            end = control.end()
            if control.group(1) in ("begin", "end"):
                # Cells of a nested table or list belong to the outer cell.
                environment = ENVIRONMENT_NAME.match(body, end)
                if environment:
                    end = environment.end()
                    environments += 1 if control.group(1) == "begin" else -1
            pos = end
            continue
        if char == "{":
            braces += 1
        elif char == "}":
            braces -= 1
        elif char == "&" and not braces and not environments:
            cells.append(body[start:pos])
            start = pos + 1
        pos += 1
    add_row("")
    return rows


def table_parts(text):
    """The one top-level table in text, or None."""
    start = TABLE_START.search(text)
    if not start:
        return None
    name = start.group(1)
    try:
        pos = start.end()
        if name in ("tabular*", "tabularx"):
            _, pos = read_braced_argument(text, pos)
        pos = read_optional_argument(text, pos)
        _, opening_end = read_braced_argument(text, pos)
    except ValueError:
        return None
    depth = 1
    for match in re.finditer(r'\\(begin|end)\{' + re.escape(name) + r'\}', text[opening_end:]):
        depth += 1 if match.group(1) == "begin" else -1
        if depth == 0:
            closing_start = opening_end + match.start()
            closing_end = opening_end + match.end()
            break
    else:
        return None
    if TABLE_START.search(text, closing_end):
        return None
    return Table(text[:start.start()], text[start.start():opening_end],
                 split_rows(text[opening_end:closing_start]),
                 text[closing_start:closing_end], text[closing_end:])


def pair_rows(old_rows, new_rows):
    """Order-preserving (old, new) row pairs; None marks a row without a counterpart."""
    words = {id(row): visible_words(" ".join(row.cells)) for row in old_rows + new_rows}

    def related(a, b):
        # Rows at the same place still need a shared word or cell to be one row.
        if a.has_cells != b.has_cells:
            return False
        shared_cells = {key for key in a.key[1] if key} & {key for key in b.key[1] if key}
        return not a.has_cells or bool(shared_cells or set(words[id(a)]) & set(words[id(b)]))

    def gain(a, b):
        if not related(a, b):
            return None
        ratio = SequenceMatcher(None, words[id(a)], words[id(b)], autojunk=False).ratio()
        return ratio - SENTENCE_THRESHOLD if ratio > SENTENCE_THRESHOLD or not a.has_cells else None

    pairs = []
    matcher = SequenceMatcher(None, [row.key for row in old_rows], [row.key for row in new_rows], autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old, new = old_rows[i1:i2], new_rows[j1:j2]
        if tag == "equal" or (len(old) == len(new) and all(map(related, old, new))):
            pairs.extend(zip(range(i1, i2), range(j1, j2)))
            continue
        pairs.extend((i1 + a if a is not None else None, j1 + b if b is not None else None)
                     for a, b in align_sequences(len(old), len(new),
                                                 lambda a, b, old=old, new=new: gain(old[a], new[b])))
    return pairs


def cell_parts(cell):
    """(before, content, after): a \\multicolumn keeps its span and format outside the content."""
    core = cell.strip()
    lead, trail = cell[:len(cell) - len(cell.lstrip())], cell[len(cell.rstrip()):]
    if MULTICOLUMN.match(core):
        try:
            _, pos = read_braced_argument(core, MULTICOLUMN.match(core).end())
            _, pos = read_braced_argument(core, pos)
            content, end = read_braced_argument(core, pos)
            if not core[end:].strip():
                start = end - 1 - len(content)
                return lead + core[:start], content, core[end - 1:] + trail
        except ValueError:
            pass
    return lead, core, trail


def color_cell(cell, color):
    before, content, after = cell_parts(cell)
    return rf"{before}\diffcell{{{color}}}{content}{after}"


def render_cell(old_cell, new_cell, tone):
    """Highlight the changed words of a paired cell, else color the whole cell."""
    if source_key(old_cell) == source_key(new_cell):
        return old_cell, new_cell
    old_before, old_content, old_after = cell_parts(old_cell)
    new_before, new_content, new_after = cell_parts(new_cell)
    if source_key(old_before + old_after) == source_key(new_before + new_after):
        (left,), (right,) = render_group([old_content], [new_content], tone)
        left, right = left.rstrip(" "), right.rstrip(" ")
        # Blocks cannot sit inside a cell; an unmarked change needs the cell color.
        if "diffmath" not in left + right and MARK.search(left + right):
            return old_before + left + old_after, new_before + right + new_after
    old_color, new_color = tone_colors(tone)
    return color_cell(old_cell, old_color), color_cell(new_cell, new_color)


def color_rules(rules, color):
    if not rules.strip():
        return rules
    return rf"\diffrule{{{color}}}{{{rules}}}"


def render_row(old_row, new_row, tone):
    """Render a paired row: rules, then cells paired by column."""
    old_rules, new_rules = old_row.rules, new_row.rules
    if source_key(old_rules) != source_key(new_rules):
        old_rules, new_rules = color_rules(old_rules, RULE_COLORS[0]), color_rules(new_rules, RULE_COLORS[1])
    old_cells, new_cells = list(old_row.cells), list(new_row.cells)
    old_pale, new_pale = tone_colors("pale")
    matcher = SequenceMatcher(None, old_row.key[1], new_row.key[1], autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        # A \multicolumn can change the count; extra cells have no counterpart.
        for i, j in zip(range(i1, i2), range(j1, j2)):
            old_cells[i], new_cells[j] = render_cell(old_cells[i], new_cells[j], tone)
        for i in range(i1 + min(i2 - i1, j2 - j1), i2):
            old_cells[i] = color_cell(old_cells[i], old_pale)
        for j in range(j1 + min(i2 - i1, j2 - j1), j2):
            new_cells[j] = color_cell(new_cells[j], new_pale)
    old_color = new_color = ""
    if old_row.has_cells and not MARK.search("".join([old_rules, new_rules, *old_cells, *new_cells])):
        old_color, new_color = tone_colors(tone)
    return old_row.render(old_rules, old_color, old_cells), new_row.render(new_rules, new_color, new_cells)


def render_unpaired_row(row, side):
    """A row without a counterpart: a pale row, or colored rules after the last row."""
    if not row.has_cells:
        return color_rules(row.rules, RULE_COLORS[side == "new"])
    return row.render(row.rules, tone_colors("pale")[side == "new"], row.cells)


def render_table(old_text, new_text, tone="strong"):
    """
    Return (old, new) with row and cell highlights. Return None unless each
    text is one table and both share the table layout and surrounding source;
    the caller then marks the table as a whole.
    """
    old, new = table_parts(old_text), table_parts(new_text)
    if not old or not new or any(source_key(getattr(old, part)) != source_key(getattr(new, part))
                                 for part in ("before", "opening", "closing", "after")):
        return None
    if [row.key for row in old.rows] == [row.key for row in new.rows]:
        return old_text, new_text
    old_rendered = [row.render(row.rules, "", row.cells) for row in old.rows]
    new_rendered = [row.render(row.rules, "", row.cells) for row in new.rows]
    for i, j in pair_rows(old.rows, new.rows):
        if i is None:
            new_rendered[j] = render_unpaired_row(new.rows[j], "new")
        elif j is None:
            old_rendered[i] = render_unpaired_row(old.rows[i], "old")
        elif old.rows[i].key != new.rows[j].key:
            old_rendered[i], new_rendered[j] = render_row(old.rows[i], new.rows[j], tone)
    return (old.before + old.opening + "".join(old_rendered) + old.closing + old.after,
            new.before + new.opening + "".join(new_rendered) + new.closing + new.after)
