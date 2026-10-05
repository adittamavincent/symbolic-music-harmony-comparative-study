r"""
Compare the bibliographies of two manuscript versions.

Entries cited on one side only are boxed as deleted or added; changed fields
of shared entries are colored. Each source prints in its own synchronized row
so that an added or removed source leaves the other column blank.
"""

import re


def plain_bib(value):
    return " ".join(re.sub(r'\\[a-zA-Z]+|[{}\\]', '', value or "").casefold().split())


def extract_citation_keys(text, suffix=""):
    matches = re.findall(r'\\(?:parencite|cite|textcite|citeauthor|citeyear|nocite)\*?(?:\[[^\]]*\])*\{([^}]+)\}', text)
    keys = set()
    for match in matches:
        for key in match.split(','):
            k = key.strip()
            if k:
                keys.add(k + suffix if k != "*" else k)
    return sorted(list(keys))

def parse_bib(content):
    entries = {}
    idx = 0
    while True:
        idx = content.find('@', idx)
        if idx == -1: break
        brace_idx = content.find('{', idx)
        if brace_idx == -1: break
        entry_type = content[idx+1:brace_idx].strip()
        comma_idx = content.find(',', brace_idx)
        if comma_idx == -1: break
        key = content[brace_idx+1:comma_idx].strip()
        balance = 1
        pos = comma_idx + 1
        while pos < len(content) and balance > 0:
            if content[pos] == '{': balance += 1
            elif content[pos] == '}': balance -= 1
            pos += 1
        if balance == 0:
            fields_text = content[comma_idx+1:pos-1]
            entries[key] = {
                'type': entry_type,
                'fields_text': fields_text,
                'raw': content[idx:pos]
            }
        idx = pos
    return entries

def parse_fields_text(text):
    fields = {}
    idx = 0
    while idx < len(text):
        eq_idx = text.find('=', idx)
        if eq_idx == -1: break
        name = text[idx:eq_idx].strip().split(',')[-1].strip().lower()
        idx = eq_idx + 1
        while idx < len(text) and text[idx] in ' \t\n\r': idx += 1
        if idx == len(text): break
        if text[idx] == '{':
            balance = 1
            pos = idx + 1
            while pos < len(text) and balance > 0:
                if text[pos] == '{': balance += 1
                elif text[pos] == '}': balance -= 1
                pos += 1
            val = text[idx+1:pos-1]
            fields[name] = val
            idx = pos
        elif text[idx] == '"':
            pos = idx + 1
            while pos < len(text) and text[pos] != '"': pos += 1
            val = text[idx+1:pos]
            fields[name] = val
            idx = pos + 1
        else:
            pos = idx
            while pos < len(text) and text[pos] not in ',\n}': pos += 1
            val = text[idx:pos].strip()
            fields[name] = val
            idx = pos
    return fields

# Biber parses these fields itself; a color macro breaks names, dates, and URLs.
# A changed value stays parseable; the renderer flags the whole modified entry.
BIB_PARSED_FIELDS = {
    "author", "editor", "editora", "editorb", "editorc", "translator",
    "annotator", "commentator", "introduction", "foreword", "afterword",
    "bookauthor", "holder", "shortauthor", "shorteditor", "namea", "nameb",
    "namec", "date", "year", "month", "urldate", "eventdate", "origdate",
    "url", "doi", "eprint", "file", "verba", "verbb", "verbc", "ids",
    "crossref", "xref", "related", "keywords", "langid", "pages", "isbn", "issn",
    "edition", "volume", "volumes", "number", "chapter", "part", "pagetotal",
    "pagination", "bookpagination", "publisher", "location", "address",
    "institution", "organization", "language", "options", "entryset",
}


def selected_keys(entries, keys):
    """Resolve nocite's wildcard against this side's own bibliography."""
    return set(entries) if "*" in keys else set(keys)


def diff_bib_files(bib1_str, bib2_str, keys1, keys2):
    e1 = parse_bib(bib1_str)
    e2 = parse_bib(bib2_str)
    out1 = []
    out2 = []
    keys1, keys2 = selected_keys(e1, keys1), selected_keys(e2, keys2)

    def render_entry(entry, key, fields, version, status, counterpart=None):
        values = []
        for name, value in sorted(fields.items()):
            # These fields hold the renderer's private side/status metadata.
            if name in ("keywords", "userc"):
                continue
            if (counterpart is not None and value != counterpart.get(name)
                    and name not in BIB_PARSED_FIELDS):
                color = "bibdelcolor" if version == "v1" else "bibinscolor"
                value = rf"{{\{color} {value}}}"
            values.append(f"{name} = {{{value}}}")
        values.append(f"keywords = {{{version}}}")
        if status:
            values.append(f"userc = {{{status}}}")
        return f"@{entry['type']}{{{key},\n  " + ",\n  ".join(values) + "\n}"

    for key in sorted(keys1 | keys2):
        left, right = key in keys1 and key in e1, key in keys2 and key in e2
        fields1 = parse_fields_text(e1[key]['fields_text']) if left else {}
        fields2 = parse_fields_text(e2[key]['fields_text']) if right else {}
        changed = left and right and (
            fields1 != fields2 or e1[key]['type'].casefold() != e2[key]['type'].casefold())
        if left:
            status = "moddel" if changed else "" if right else "del"
            out1.append(render_entry(e1[key], key, fields1, "v1", status, fields2 if right else None))
        if right:
            status = "modins" if changed else "" if left else "ins"
            out2.append(render_entry(e2[key], key, fields2, "v2", status, fields1 if left else None))
    return "\n".join(out1), "\n".join(out2)

def bibliography_rows(bib1_str, bib2_str, keys1, keys2):
    """
    Order cited sources by author, year, and title. Each row holds one source
    on both sides, so an added or removed source leaves the other side blank.
    """
    e1, e2 = parse_bib(bib1_str), parse_bib(bib2_str)
    keys1, keys2 = selected_keys(e1, keys1), selected_keys(e2, keys2)
    rows = []
    for key in set(keys1) | set(keys2):
        left, right = key in keys1 and key in e1, key in keys2 and key in e2
        if not (left or right):
            continue
        fields = parse_fields_text((e2 if right else e1)[key]['fields_text'])
        names = fields.get("author") or fields.get("editor")
        # Sort by family names: "Family, Given" or "Given Family".
        families = [name.split(",")[0] if "," in name else name.split()[-1]
                    for name in re.split(r'\s+and\s+', names.strip())] if names else [fields.get("title", "")]
        rows.append(((plain_bib(" ".join(families)), fields.get("year") or fields.get("date", ""),
                      plain_bib(fields.get("title")), key), key, left, right))
    return [(key, left, right) for _, key, left, right in sorted(rows)]


def render_bibliography_rows(rows, v1_keys, v2_keys):
    """Print each source in its own synchronized row of the two columns."""
    # Rows already resolved wildcard citations to this side's actual entries.
    left_keys = [key + "_v1" for key, left, _ in rows if left]
    right_keys = [key for key, _, right in rows if right]
    out = [f"\\nocite{{{', '.join(left_keys)}}}" if left_keys else "",
           f"\\nocite{{{', '.join(right_keys)}}}" if right_keys else "",
           r"\begin{paracol}{2}", r"\section*{DAFTAR PUSTAKA}", r"\switchcolumn",
           r"\section*{DAFTAR PUSTAKA}", r"\switchcolumn*"]
    for index, (key, left, right) in enumerate(rows):
        for side, present, entry in (("left", left, key + "_v1"), ("right", right, key)):
            if present:
                out.append(rf"\defbibcheck{{diff{side}{index}}}{{\iffieldequalstr{{entrykey}}{{{entry}}}{{}}{{\skipentry}}}}")
                # A box keeps an entry's own glue from shifting the row.
                out.append(r"\noindent\begin{minipage}[t]{\linewidth}"
                           rf"\printbibliography[heading=none, check=diff{side}{index}]"
                           r"\end{minipage}\par\vspace{4pt}")
            out.append(r"\switchcolumn" if side == "left" else r"\switchcolumn*")
    out.append(r"\end{paracol}")
    return "\n".join(out)
