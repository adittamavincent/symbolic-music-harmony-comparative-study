"""Stage graphics from the compared Git revisions, identified by their bytes."""

import hashlib
import posixpath
import re
import subprocess
from pathlib import Path

GRAPHIC_COMMAND = re.compile(r"\\includegraphics\*?(?![A-Za-z@])")
GRAPHIC_PATH_COMMAND = re.compile(r"\\graphicspath(?![A-Za-z@])")
GRAPHIC_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".eps", ".mps")
TEX_PATH_ESCAPES = re.compile(r"\\([_%#&${} ])")
LITERAL_START = re.compile(r"\\begin\{(verbatim\*?|Verbatim\*?|lstlisting\*?|minted\*?)\}|\\verb\*?(?![A-Za-z@])")


def _mask_comments(text):
    """Keep character positions while hiding commands inside TeX comments."""
    masked = list(text)
    for match in re.finditer(r"%", text):
        pos = match.start()
        slash = pos - 1
        while slash >= 0 and text[slash] == "\\":
            slash -= 1
        if (pos - slash - 1) % 2:
            continue
        end = text.find("\n", pos)
        end = len(text) if end < 0 else end
        masked[pos:end] = " " * (end - pos)
    return "".join(masked)


def _mask_literal_examples(text):
    """Do not load graphic commands printed as code rather than executed."""
    result, pos = list(text), 0
    while match := LITERAL_START.search(_mask_comments("".join(result)), pos):
        if match.group(1):
            end_marker = rf"\end{{{match.group(1)}}}"
            end = text.find(end_marker, match.end())
            end = len(text) if end < 0 else end + len(end_marker)
        else:
            # \verb's next character is its delimiter, including |, +, or !.
            if match.end() >= len(text) or text[match.end()].isspace():
                pos = match.end()
                continue
            delimiter = text[match.end()]
            end = text.find(delimiter, match.end() + 1)
            newline = text.find("\n", match.end() + 1)
            if end < 0 or (newline >= 0 and newline < end):
                end = len(text) if newline < 0 else newline
            else:
                end += 1
        result[match.start():end] = " " * (end - match.start())
        pos = end
    # Masking literals first prevents a verbatim percent from hiding real
    # graphics that follow its closing delimiter on the same source line.
    return _mask_comments("".join(result))


def _group(text, pos, opening="{", closing="}"):
    while pos < len(text) and text[pos].isspace():
        pos += 1
    if pos >= len(text) or text[pos] != opening:
        raise ValueError(f"Expected {opening!r} in graphic command")
    start, depth, braces = pos + 1, 1, 0
    pos += 1
    while pos < len(text):
        char = text[pos]
        if char == "\\":
            pos += 2
            continue
        # Braced option values may contain literal square brackets.
        if opening == "[":
            if char == "{":
                braces += 1
            elif char == "}":
                braces -= 1
        if braces == 0:
            if char == opening:
                depth += 1
            elif char == closing:
                depth -= 1
                if depth == 0:
                    return start, pos, pos + 1
        pos += 1
    raise ValueError(f"Unclosed {opening!r} in graphic command")


def _literal_path(value):
    value = value.strip()
    if value.startswith(r"\detokenize"):
        begin, end, after = _group(value, len(r"\detokenize"))
        if value[after:].strip():
            raise ValueError(f"Unsupported dynamic graphic filename: {value!r}")
        value = value[begin:end]
    else:
        if re.search(r"(?<!\\)[{}$#~]", value):
            raise ValueError(f"Unsupported dynamic graphic filename: {value!r}")
        value = TEX_PATH_ESCAPES.sub(lambda match: match.group(1), value)
        if "\\" in value:
            raise ValueError(f"Unsupported dynamic graphic filename: {value!r}")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        value = value[1:-1]
    if not value or "\n" in value or "\r" in value or "\x00" in value:
        raise ValueError(f"Invalid graphic filename: {value!r}")
    if posixpath.isabs(value):
        raise ValueError(f"Graphic filename must resolve inside the Git revision: {value!r}")
    return value


def _graphic_paths(text, masked):
    paths = []
    for match in GRAPHIC_PATH_COMMAND.finditer(masked):
        start, end, _ = _group(masked, match.end())
        pos = start
        while pos < end:
            while pos < end and masked[pos].isspace():
                pos += 1
            if pos >= end:
                break
            begin, finish, pos = _group(masked, pos)
            paths.append(_literal_path(text[begin:finish]))
    return paths


def _git_tree(ref):
    result = subprocess.run(["git", "ls-tree", "-r", "--name-only", "-z", ref], capture_output=True, check=False)
    if result.returncode:
        raise ValueError(f"Cannot read graphics tree at Git revision {ref!r}")
    return set(result.stdout.decode("utf-8", errors="surrogateescape").split("\x00")) - {""}


def _resolve_graphic(filename, ref, paths, root, graphic_paths):
    has_extension = bool(posixpath.splitext(filename)[1])

    def matches(candidate):
        candidate = posixpath.normpath(candidate)
        variants = [candidate] if has_extension else [candidate, *(candidate + ext for ext in GRAPHIC_EXTENSIONS)]
        return {path for path in variants if path in paths}

    def choose(candidates):
        found = set().union(*(matches(candidate) for candidate in candidates)) if candidates else set()
        if len(found) > 1:
            raise ValueError(f"Ambiguous graphic {filename!r} at {ref}: {', '.join(sorted(found))}")
        return next(iter(found)) if found else None

    # A local explicit name takes precedence over names in other directories.
    for candidates in (
        [posixpath.join(root, filename)],
        [filename],
        [posixpath.join(root, folder, filename) for folder in graphic_paths],
        [posixpath.join(posixpath.dirname(path), filename) for path in sorted(paths) if path.endswith(".cls")],
    ):
        resolved = choose(candidates)
        if resolved:
            return resolved
    basenames = {posixpath.basename(filename)}
    if not has_extension:
        basenames.update(posixpath.basename(filename) + ext for ext in GRAPHIC_EXTENSIONS)
    found = {path for path in paths if posixpath.basename(path) in basenames}
    if len(found) == 1:
        return next(iter(found))
    if found:
        raise ValueError(f"Ambiguous graphic {filename!r} at {ref}: {', '.join(sorted(found))}")
    raise ValueError(f"Missing graphic {filename!r} at {ref} (manuscript root {root!r})")


def _graphic_extension(source_path, data):
    # Choose by file bytes when possible, so a renamed asset keeps its identity.
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"%PDF-"):
        return ".pdf"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"%!PS"):
        return ".eps"
    extension = posixpath.splitext(source_path)[1].lower()
    return ".jpg" if extension == ".jpeg" else extension


def stage_graphics(ref, text, outdir, manuscript_root=""):
    """Rewrite literal includegraphics paths to snapshots read only from Git.

    ``manuscript_root`` may be the template directory or its .tex/.template
    path. Identical bytes share a staged name even when their source names
    differ; changes to a file at the same source name therefore compare too.
    """
    root = str(manuscript_root).replace("\\", "/")
    if root.endswith((".tex", ".template")):
        root = posixpath.dirname(root)
    masked = _mask_literal_examples(text)
    commands = list(GRAPHIC_COMMAND.finditer(masked))
    if not commands:
        return text
    paths = _git_tree(ref)
    graphic_paths = _graphic_paths(text, masked)
    replacements, snapshots = [], {}
    for match in commands:
        pos = match.end()
        while pos < len(masked) and masked[pos].isspace():
            pos += 1
        while pos < len(masked) and masked[pos] == "[":
            _, _, pos = _group(masked, pos, "[", "]")
            while pos < len(masked) and masked[pos].isspace():
                pos += 1
        begin, end, _ = _group(masked, pos)
        filename = _literal_path(text[begin:end])
        source_path = _resolve_graphic(filename, ref, paths, root, graphic_paths)
        if source_path not in snapshots:
            result = subprocess.run(["git", "show", f"{ref}:{source_path}"], capture_output=True, check=False)
            if result.returncode:
                raise ValueError(f"Cannot read graphic {source_path!r} at {ref}")
            data = result.stdout
            extension = _graphic_extension(source_path, data)
            if not extension:
                raise ValueError(f"Graphic {source_path!r} at {ref} has no identifiable file extension")
            staged = f"diff-assets/{hashlib.sha256(data).hexdigest()}{extension}"
            target = Path(outdir) / staged
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            snapshots[source_path] = staged
        replacements.append((begin, end, snapshots[source_path]))
    for begin, end, staged in reversed(replacements):
        text = text[:begin] + staged + text[end:]
    return text
