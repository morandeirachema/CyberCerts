#!/usr/bin/env python3
"""Build an Anki .apkg deck from the module flashcards.

Produces one package with a subdeck per module ("CEH v13::06 System Hacking"),
so it imports as a clean, browsable tree. Requires the `genanki` library:

    pip install genanki
    python3 scripts/build_anki.py                 # -> anki-decks/ceh-v13.apkg
    python3 scripts/build_anki.py out/mine.apkg   # custom output path

The .apkg is a binary and is git-ignored — regenerate it any time.
Prefer no dependencies? Use scripts/quiz.py, or import each flashcards.csv
directly (File > Import, comma-separated, allow HTML).
"""
import csv, pathlib, sys, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

try:
    import genanki
except ImportError:
    sys.exit("genanki not installed. Run:  pip install genanki\n"
             "(or use scripts/quiz.py / import the .csv files into Anki directly)")

MODEL = genanki.Model(
    1607392319, "CEH Flashcard",
    fields=[{"name": "Front"}, {"name": "Back"}],
    templates=[{"name": "Card 1",
                "qfmt": "{{Front}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Back}}'}],
)

def pretty(dirname):
    num, *rest = dirname.split("-")
    return f"{num} " + " ".join(w.capitalize() for w in rest)

def main():
    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "anki-decks" / "ceh-v13.apkg"
    out.parent.mkdir(parents=True, exist_ok=True)
    decks, total = [], 0
    for f in sorted(ROOT.glob("modules/*/flashcards.csv")):
        name = f.parent.name
        deck_id = 2_000_000_000 + int(re.match(r"(\d+)", name).group(1))
        deck = genanki.Deck(deck_id, f"CEH v13::{pretty(name)}")
        for row in csv.reader(f.read_text(encoding="utf-8").splitlines()):
            if not row or row[0].startswith("#") or len(row) < 2:
                continue
            tags = [re.sub(r"[^A-Za-z0-9_]", "_", t) for t in (row[2].split() if len(row) > 2 else [])]
            deck.add_note(genanki.Note(model=MODEL, fields=[row[0], row[1]], tags=tags))
            total += 1
        decks.append(deck)
    genanki.Package(decks).write_to_file(str(out))
    print(f"wrote {out}  ({total} cards across {len(decks)} module subdecks)")
    print("Import in Anki: File > Import > select the .apkg")

if __name__ == "__main__":
    main()
