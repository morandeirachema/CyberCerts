#!/usr/bin/env python3
"""Repo integrity checks for the CEH study repo.

Verifies, across every tracked Markdown file (fenced code blocks are excluded,
so shell `#comments` and example `[links](...)` inside ``` fences are ignored):
  - relative links resolve to a real file
  - in-page #anchors match a heading, using GitHub's slug rules: lowercase,
    punctuation dropped, spaces -> hyphens, underscores kept, and duplicate
    headings get a -1 / -2 suffix
  - ```mermaid blocks start with a valid diagram type
  - every flashcards.csv under certs/ceh/ has rows of exactly 3 columns, none empty

Exits non-zero if anything fails (so CI goes red). Run from certs/ceh/:
    python3 scripts/validate.py
    python3 scripts/validate.py --selftest   # unit-test the slug logic and exit
"""
import re, sys, csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_LINKCHECK = {"modules/00-TEMPLATE.md"}  # template paths are valid only once copied
MERMAID_TYPES = ("flowchart", "graph", "sequenceDiagram", "classDiagram",
                 "stateDiagram", "erDiagram", "pie", "mindmap", "gantt",
                 "journey", "timeline")
LINK = re.compile(r'!?\[[^\]]*\]\(([^)]+)\)')      # [text](target) and ![alt](src)
HEAD = re.compile(r'^#{1,6}\s+(.+?)\s*$', re.M)    # ATX headings, one per line
FENCE = re.compile(r'^(\s*)(`{3,}|~{3,})')         # opening/closing code fence
SCHEME = re.compile(r'^[a-zA-Z][\w+.-]*:')         # http:, https:, mailto:, tel: ...
TITLE = re.compile(r'''^(\S+)\s+["'].*["']\s*$''')  # target "Optional title"


def strip_fences(txt):
    """Blank out fenced code blocks so their contents aren't read as headings or
    links. Line count is preserved so nothing else shifts."""
    out, closer = [], None
    for line in txt.splitlines():
        m = FENCE.match(line)
        if closer is None and m:
            closer = m.group(2)[0] * 3          # remember ``` vs ~~~
            out.append('')
        elif closer is not None and line.lstrip().startswith(closer):
            closer = None
            out.append('')
        else:
            out.append('' if closer is not None else line)
    return '\n'.join(out)


def anchorize(text):
    """GitHub slug for a single heading (before de-duplication): lowercase, drop
    everything but word chars / spaces / hyphens (underscores are word chars and
    survive), then spaces -> hyphens."""
    text = re.sub(r'\s+#+\s*$', '', text.strip())      # drop ATX closing '##'
    return re.sub(r'[^\w -]', '', text.lower()).replace(' ', '-')


def heading_slugs(prose):
    """Every '#anchor' GitHub would emit for `prose`, matching its -1/-2 suffixing
    of duplicate headings (first 'Setup' -> #setup, second -> #setup-1, ...)."""
    counts, slugs = {}, set()
    for raw in HEAD.findall(prose):
        base = anchorize(raw)
        n = counts.get(base, 0)
        counts[base] = n + 1
        slugs.add('#' + (base if n == 0 else f"{base}-{n}"))
    return slugs


def link_target(raw):
    """Normalise a captured link target: strip <angle brackets> and a trailing
    "title", leaving just the URL/path."""
    t = raw.strip()
    if t.startswith('<') and t.endswith('>'):
        t = t[1:-1].strip()
    m = TITLE.match(t)
    return m.group(1) if m else t


def check_markdown(md):
    errors = []
    for f in md:
        rel = f.relative_to(ROOT).as_posix()
        txt = f.read_text(encoding='utf-8')
        prose = strip_fences(txt)                       # ignore code-block contents
        anchors = heading_slugs(prose)
        for m in LINK.finditer(prose):
            target = link_target(m.group(1))
            if not target:
                continue
            if target.startswith('#'):
                if target not in anchors:
                    errors.append(f"{rel}: bad anchor {target}")
                continue
            if SCHEME.match(target):                    # external / non-file scheme
                continue
            if rel in SKIP_LINKCHECK:
                continue
            path = target.split('#', 1)[0]
            if path and not (f.parent / path).resolve().exists():
                errors.append(f"{rel}: broken link -> {target}")
        for m in re.finditer(r'```mermaid\n(.*?)```', txt, re.DOTALL):
            first = (m.group(1).strip().splitlines() or [''])[0].strip()
            if not first.startswith(MERMAID_TYPES):
                errors.append(f"{rel}: bad mermaid type {first!r}")
    return errors


def check_flashcards():
    errors, warnings, cards = [], [], 0
    for f in sorted(ROOT.rglob('flashcards.csv')):
        if '.git' in f.parts:
            continue
        rel = f.relative_to(ROOT).as_posix()
        seen = set()
        for row in csv.reader(f.read_text(encoding='utf-8').splitlines()):
            if not row or row[0].startswith('#'):
                continue
            cards += 1
            if len(row) != 3:
                errors.append(f"{rel}: csv row has {len(row)} cols -> {row}")
                continue
            if not row[0].strip() or not row[1].strip():
                errors.append(f"{rel}: empty front/back -> {row}")
            if row[0] in seen:
                warnings.append(f"{rel}: duplicate front -> {row[0]!r}")
            seen.add(row[0])
    return errors, warnings, cards


def selftest():
    """Prove the slug logic matches real GitHub anchors (from headings actually
    in this repo) so CI catches any regression in anchorize/heading_slugs."""
    ok = True
    cases = {
        "Quick Start": "#quick-start",
        "6. Exploitation — Metasploit Framework (Module 06)":
            "#6-exploitation--metasploit-framework-module-06",
        "5. Web Application Hacking (Modules 13–15)":
            "#5-web-application-hacking-modules-1315",
        "`local_exploit_suggester` — find your privesc path":
            "#local_exploit_suggester--find-your-privesc-path",
    }
    for text, want in cases.items():
        got = '#' + anchorize(text)
        if got != want:
            ok = False
            print(f"  FAIL anchorize({text!r}) = {got!r}, want {want!r}")
    dup = heading_slugs("# Setup\n## Setup\n### Setup\n")
    for want in ("#setup", "#setup-1", "#setup-2"):
        if want not in dup:
            ok = False
            print(f"  FAIL duplicate-heading slug {want!r} missing from {sorted(dup)}")
    fenced = heading_slugs(strip_fences("# Real Heading\n```bash\n# not a heading\n```\n"))
    if "#real-heading" not in fenced or "#not-a-heading" in fenced:
        ok = False
        print(f"  FAIL code-fence heading leak: {sorted(fenced)}")
    print("selftest OK" if ok else "selftest FAILED")
    return ok


def main():
    if '--selftest' in sys.argv[1:]:
        sys.exit(0 if selftest() else 1)

    md = [p for p in ROOT.rglob('*.md') if '.git' not in p.parts]
    errors = check_markdown(md)
    card_errors, warnings, cards = check_flashcards()
    errors += card_errors

    print(f"checked {len(md)} markdown files, {cards} flashcards")
    for w in warnings:
        print("  war: ", w)
    if errors:
        print(f"\nFAILED ({len(errors)} issue(s)):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("OK — 0 broken links, 0 bad anchors, 0 bad mermaid, 0 malformed CSV rows")


if __name__ == '__main__':
    main()
