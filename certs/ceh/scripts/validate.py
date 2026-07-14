#!/usr/bin/env python3
"""Repo integrity checks for the CEH study repo.

Verifies, across every tracked Markdown file:
  - relative links resolve to a real file
  - in-page #anchors match a heading
  - ```mermaid blocks start with a valid diagram type
  - flashcards.csv data rows have exactly 3 columns
Exits non-zero if anything fails (so CI goes red). Run from the repo root:
    python3 scripts/validate.py
"""
import re, sys, csv, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_LINKCHECK = {"modules/00-TEMPLATE.md"}  # template uses paths valid only once copied
MERMAID_TYPES = ("flowchart", "graph", "sequenceDiagram", "classDiagram",
                 "stateDiagram", "erDiagram", "pie", "mindmap", "gantt",
                 "journey", "timeline")
LINK = re.compile(r'\[[^\]]+\]\(([^)]+)\)')
HEAD = re.compile(r'^#{1,6} (.+)$', re.M)

def anchorize(h):
    return '#' + re.sub(r'[^a-z0-9 -]', '', h.strip().lower()).replace(' ', '-')

def main():
    md = [p for p in ROOT.rglob('*.md') if '.git' not in p.parts]
    errors = []
    for f in md:
        rel = f.relative_to(ROOT).as_posix()
        txt = f.read_text(encoding='utf-8')
        anchors = {anchorize(h) for h in HEAD.findall(txt)}
        for m in LINK.finditer(txt):
            target = m.group(1).strip()
            if target.startswith(('http://', 'https://', 'mailto:')):
                continue
            if target.startswith('#'):
                if target not in anchors:
                    errors.append(f"{rel}: bad anchor {target}")
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

    cards = 0
    for f in ROOT.rglob('flashcards.csv'):
        for row in csv.reader(f.read_text(encoding='utf-8').splitlines()):
            if not row or row[0].startswith('#'):
                continue
            cards += 1
            if len(row) != 3:
                errors.append(f"{f.relative_to(ROOT)}: csv row has {len(row)} cols -> {row}")

    print(f"checked {len(md)} markdown files, {cards} flashcards")
    if errors:
        print(f"\nFAILED ({len(errors)} issue(s)):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("OK — 0 broken links, 0 bad anchors, 0 bad mermaid, 0 malformed CSV rows")

if __name__ == '__main__':
    main()
