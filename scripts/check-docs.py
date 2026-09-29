#!/usr/bin/env python3
"""Quality gate for the repo's Markdown.

Checks, across all *.md (excluding .git / site / site-src):
  - no ASCII-art diagrams (box-drawing or +--/--+) in prose (fenced code and
    inline code spans are ignored — a shell prompt or tree output is not a diagram);
  - balanced code fences (``` and ~~~);
  - every ```mermaid block starts with a valid diagram type and uses no
    reserved word (end/graph/subgraph) as a node id;
  - flowchart node-label lines fit the box (no over-wide single line — wrap
    long labels with <br/>; run scripts/wrap-mermaid-labels.py to fix);
  - every content page has a "## Sources" section (READMEs and meta files exempt,
    and not enforced inside certs/ceh/, which has its own conventions);
  - no broken internal file links, image links or heading anchors (GitHub slug rules);
  - every flashcards.csv row has exactly 3 non-empty columns (front, back, tags).

Exits non-zero (and lists the problems) if anything fails. Run from anywhere:
    python scripts/check-docs.py
"""
import csv
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKIP = ('.git/', 'site/', 'site-src/', 'node_modules/')

MERMAID_TYPES = (
    'flowchart', 'graph', 'sequenceDiagram', 'erDiagram', 'classDiagram',
    'stateDiagram', 'stateDiagram-v2', 'quadrantChart', 'timeline', 'gantt',
    'mindmap', 'journey', 'pie',
)
SOURCES_EXEMPT = {
    'README.md', 'CLAUDE.md', 'CONTRIBUTING.md', 'CHANGELOG.md',
    'SECURITY.md', 'LICENSE', 'MAINTENANCE.md',
}
# The CEH course (merged from its own repo) follows its own conventions and has
# its own gate (certs/ceh/scripts/validate.py, run by ceh-validate.yml). Its
# links, ASCII-art and Mermaid label widths are checked here too; only the
# per-page "## Sources" rule is not enforced on it.
SOURCES_EXEMPT_DIRS = ('certs/ceh/',)
LINK_SKIP = {'certs/ceh/modules/00-TEMPLATE.md'}  # placeholder paths by design
MAX_LABEL = 44  # chars per <br/> segment of a flowchart node label

ASCII_RE = re.compile(r'[─-╿▀-▟]|\+--|--\+')
LINK_RE = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')   # [text](target) and ![alt](src)
HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)')
FENCE_RE = re.compile(r'^\s*(`{3,}|~{3,})')
CODESPAN_RE = re.compile(r'`[^`\n]*`')
MERMAID_RE = re.compile(r'^```mermaid\n(.*?)^```', re.S | re.M)
NODE_LABEL_RE = re.compile(r'[\[({]+"([^"]*)"')
RESERVED_ID_RE = re.compile(r'\s*(end|subgraph|graph)\s*[\[\(]')
EXTERNAL = ('http://', 'https://', 'mailto:', 'tel:')


def markdown_files():
    return sorted(p for p in glob.glob('**/*.md', recursive=True)
                  if not any(s in (p + '/') for s in SKIP))


def strip_fences(text):
    """Blank out fenced code blocks (``` or ~~~), keeping the line count, so their
    contents are not read as headings, links or ASCII art. Returns the prose and
    whether a fence was left open at end of file."""
    out, closer = [], None
    for line in text.splitlines():
        m = FENCE_RE.match(line)
        if closer is None and m:
            closer = m.group(1)[0] * 3
            out.append('')
        elif closer is not None and line.lstrip().startswith(closer):
            closer = None
            out.append('')
        else:
            out.append('' if closer is not None else line)
    return '\n'.join(out), closer is not None


def slugs(prose):
    """Heading anchor slugs, computed exactly like GitHub (github-slugger):
    lowercase, strip HTML, remove all but [word, space, hyphen], spaces -> '-',
    NO trimming of leading/trailing hyphens (so emoji headings keep their leading
    '-'), and append -1/-2 for duplicates. Matching is exact — no leniency — so a
    link that would 404 on GitHub fails here too."""
    out, counts = set(), {}
    for line in prose.splitlines():
        m = HEADING_RE.match(line)
        if not m:
            continue
        text = re.sub(r'#+\s*$', '', m.group(2).strip()).strip()
        s = re.sub(r'[^\w\- ]', '', re.sub(r'<[^>]+>', '', text.lower())).replace(' ', '-')
        if s in counts:
            counts[s] += 1
            out.add(f"{s}-{counts[s]}")
        else:
            counts[s] = 0
            out.add(s)
    return out


def link_target(raw):
    """Normalise a captured link target: strip <angle brackets> and a trailing
    "title", leaving just the path/URL."""
    t = raw.strip()
    if t.startswith('<') and t.endswith('>'):
        return t[1:-1].strip()
    return t.split(' ')[0]


def check_style(f, text, prose, unclosed):
    issues = []
    for i, line in enumerate(prose.splitlines(), 1):
        if ASCII_RE.search(CODESPAN_RE.sub('', line)):
            issues.append(f"ASCII art: {f}:{i}")
            break

    if unclosed:
        issues.append(f"Unbalanced code fences: {f}")

    for m in MERMAID_RE.finditer(text):
        body = m.group(1)
        first = next((x.strip() for x in body.splitlines() if x.strip()), '')
        if not first.startswith(MERMAID_TYPES):
            issues.append(f"Bad Mermaid header: {f}: {first[:40]!r}")
        for line in body.splitlines():
            if RESERVED_ID_RE.match(line):
                issues.append(f"Reserved word as Mermaid node id: {f}: {line.strip()[:40]}")
        # Flowchart node boxes should fit their text: no over-wide single label line.
        if first.startswith(('flowchart', 'graph')):
            for label in NODE_LABEL_RE.findall(body):
                for seg in label.split('<br/>'):
                    if len(seg) > MAX_LABEL and ' ' in seg.strip():
                        issues.append(f"Over-wide Mermaid label (wrap with <br/>): {f}: {seg[:48]!r}")

    if (not f.startswith(SOURCES_EXEMPT_DIRS)
            and os.path.basename(f) not in SOURCES_EXEMPT
            and not re.search(r'(?im)^#+\s*sources\b', text)):
        issues.append(f"Missing Sources section: {f}")
    return issues


def check_links(f, prose, slugmap):
    issues = []
    d = os.path.dirname(f)
    for ln, line in enumerate(prose.splitlines(), 1):
        for raw in LINK_RE.findall(CODESPAN_RE.sub('', line)):
            tgt = link_target(raw)
            if not tgt or tgt.startswith(EXTERNAL):
                continue
            path, _, anchor = tgt.partition('#')
            target = f if path == '' else os.path.normpath(os.path.join(d, path))
            if not os.path.exists(target):
                issues.append(f"Broken link: {f}:{ln} -> {tgt}")
            elif anchor and target in slugmap and anchor not in slugmap[target]:
                issues.append(f"Broken anchor: {f}:{ln} -> {tgt}")
    return issues


def check_flashcards():
    issues, cards = [], 0
    for f in sorted(glob.glob('**/flashcards.csv', recursive=True)):
        if any(s in (f + '/') for s in SKIP):
            continue
        with open(f, encoding='utf-8', newline='') as fh:
            for n, row in enumerate(csv.reader(fh), 1):
                if not row or row[0].startswith('#'):
                    continue
                cards += 1
                if len(row) != 3 or not all(c.strip() for c in row):
                    issues.append(f"Bad flashcard row (need 3 non-empty columns): {f}:{n}")
    return issues, cards


def main():
    os.chdir(ROOT)
    md = markdown_files()
    parsed = {}
    for f in md:
        text = open(f, encoding='utf-8').read()
        prose, unclosed = strip_fences(text)
        parsed[f] = (text, prose, unclosed)
    slugmap = {f: slugs(prose) for f, (_, prose, _) in parsed.items()}

    issues = []
    for f, (text, prose, unclosed) in parsed.items():
        issues += check_style(f, text, prose, unclosed)
        if f not in LINK_SKIP:
            issues += check_links(f, prose, slugmap)
    card_issues, cards = check_flashcards()
    issues += card_issues

    if issues:
        print(f"❌ {len(issues)} issue(s) found:\n")
        for i in issues:
            print("  -", i)
        sys.exit(1)

    print(f"✅ {len(md)} markdown files and {cards} flashcards pass: no ASCII, balanced fences, "
          "valid Mermaid (fit-to-text labels), Sources present, 0 broken links/anchors.")


if __name__ == '__main__':
    main()
