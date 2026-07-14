#!/usr/bin/env python3
"""Terminal flashcard quiz over the repo's module decks.

Drills the `modules/*/flashcards.csv` decks with self-rating and scoring —
no Anki needed. Examples:
    python3 scripts/quiz.py                 # all decks, shuffled, interactive
    python3 scripts/quiz.py --module 06     # just System Hacking
    python3 scripts/quiz.py --tag kerberos  # cards tagged '...kerberos...'
    python3 scripts/quiz.py --num 20        # a random 20-card round
    python3 scripts/quiz.py --count         # just report deck sizes (non-interactive)
"""
import argparse, csv, pathlib, random, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_cards():
    cards = []
    for f in sorted(ROOT.glob('modules/*/flashcards.csv')):
        mod = f.parent.name
        for row in csv.reader(f.read_text(encoding='utf-8').splitlines()):
            if not row or row[0].startswith('#') or len(row) < 2:
                continue
            front, back = row[0], row[1]
            tag = row[2] if len(row) > 2 else ''
            cards.append({'front': front, 'back': back, 'tag': tag, 'mod': mod})
    return cards

def main():
    ap = argparse.ArgumentParser(description="CEH flashcard quiz")
    ap.add_argument('--module', help="module number, e.g. 06")
    ap.add_argument('--tag', help="filter by tag substring (e.g. kerberos)")
    ap.add_argument('--num', type=int, help="limit to N random cards")
    ap.add_argument('--count', action='store_true', help="report deck sizes and exit")
    args = ap.parse_args()

    cards = load_cards()
    if args.count:
        from collections import Counter
        by = Counter(c['mod'] for c in cards)
        for m, n in sorted(by.items()):
            print(f"  {m}: {n}")
        print(f"total: {len(cards)} flashcards across {len(by)} modules")
        return

    if args.module:
        cards = [c for c in cards if c['mod'].startswith(args.module.zfill(2))]
    if args.tag:
        cards = [c for c in cards if args.tag.lower() in c['tag'].lower()]
    if not cards:
        print("No cards matched that filter."); sys.exit(1)

    random.shuffle(cards)
    if args.num:
        cards = cards[:args.num]

    print(f"\n=== {len(cards)} cards — Enter to flip, [y/n] to score, q to quit ===\n")
    correct, seen, missed = 0, 0, []
    for i, c in enumerate(cards, 1):
        print(f"[{i}/{len(cards)}] ({c['mod']})")
        print(f"  Q: {c['front']}")
        try:
            r = input("  ...Enter to reveal (q=quit) ")
        except (EOFError, KeyboardInterrupt):
            break
        if r.strip().lower() == 'q':
            break
        print(f"  A: {c['back']}")
        try:
            g = input("  Got it? [y/n] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if g == 'q':
            break
        seen += 1
        if g == 'y':
            correct += 1
        else:
            missed.append(c)
        print()

    if seen:
        pct = round(100 * correct / seen)
        print(f"\n=== Score: {correct}/{seen} ({pct}%) ===")
        if missed:
            print("Review these:")
            for c in missed:
                print(f"  - ({c['mod']}) {c['front']}")

if __name__ == '__main__':
    main()
