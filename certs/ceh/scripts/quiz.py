#!/usr/bin/env python3
"""Terminal flashcard quiz over the repo's module decks.

Drills the `modules/*/flashcards.csv` decks with self-rating and scoring —
no Anki needed. Examples:
    python3 scripts/quiz.py                 # all decks, shuffled, interactive
    python3 scripts/quiz.py --module 06     # just System Hacking
    python3 scripts/quiz.py --tag kerberos  # cards tagged '...kerberos...'
    python3 scripts/quiz.py --num 20        # a random 20-card round
    python3 scripts/quiz.py --count         # just report deck sizes (non-interactive)
    python3 scripts/quiz.py --deck ../security-plus/exam-prep/flashcards.csv   # drill any deck
"""
import argparse, csv, pathlib, random, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

def load_cards(deck_paths=None):
    """Load cards from the CEH module decks, or from explicit --deck paths.

    deck_paths (if given) are flashcards.csv files resolved relative to the
    current working directory; the CEH module globs are then skipped entirely.
    """
    if deck_paths:
        files = [pathlib.Path(p) for p in deck_paths]
    else:
        files = sorted(ROOT.glob('modules/*/flashcards.csv'))
    cards = []
    for f in files:
        # For module decks the folder name (e.g. '06-system-hacking') is the label;
        # for an explicit --deck the hub folder (e.g. 'security-plus') is more useful.
        mod = f.parent.parent.name if deck_paths else f.parent.name
        for row in csv.reader(f.read_text(encoding='utf-8').splitlines()):
            if not row or row[0].startswith('#') or len(row) < 2:
                continue
            front, back = row[0], row[1]
            tag = row[2] if len(row) > 2 else ''
            cards.append({'front': front, 'back': back, 'tag': tag, 'mod': mod})
    return cards

def drill(cards):
    """Run one interactive round. Returns (correct, seen, missed[])."""
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
    return correct, seen, missed


def main():
    ap = argparse.ArgumentParser(description="CEH flashcard quiz")
    ap.add_argument('--deck', action='append', metavar='PATH',
                    help="path to a flashcards.csv (relative to the current dir); "
                         "repeatable. Drills these decks instead of the CEH modules.")
    ap.add_argument('--module', help="module number, e.g. 06")
    ap.add_argument('--tag', help="filter by tag substring (e.g. kerberos)")
    ap.add_argument('--num', type=int, help="limit to N random cards")
    ap.add_argument('--seed', type=int, help="fixed shuffle seed (reproducible round)")
    ap.add_argument('--count', action='store_true', help="report deck sizes and exit")
    ap.add_argument('--list-tags', action='store_true', help="list all tags with counts and exit")
    args = ap.parse_args()

    cards = load_cards(args.deck)
    if args.count:
        from collections import Counter
        by = Counter(c['mod'] for c in cards)
        for m, n in sorted(by.items()):
            print(f"  {m}: {n}")
        print(f"total: {len(cards)} flashcards across {len(by)} modules")
        return
    if args.list_tags:
        from collections import Counter
        tags = Counter(t for c in cards for t in c['tag'].split())
        for t, n in sorted(tags.items()):
            print(f"  {n:4}  {t}")
        print(f"total: {len(tags)} distinct tags")
        return

    if args.module:
        cards = [c for c in cards if c['mod'].startswith(args.module.zfill(2))]
    if args.tag:
        cards = [c for c in cards if args.tag.lower() in c['tag'].lower()]
    if not cards:
        print("No cards matched that filter."); sys.exit(1)

    random.seed(args.seed)   # None => nondeterministic; an int => reproducible
    random.shuffle(cards)
    if args.num and args.num > 0:
        cards = cards[:args.num]

    correct, seen, missed = drill(cards)
    if seen:
        pct = round(100 * correct / seen)
        print(f"\n=== First-pass score: {correct}/{seen} ({pct}%) ===")

    # Offer to re-drill just the misses until the pile is empty (spaced-ish repetition).
    while missed:
        try:
            again = input(f"\nRe-drill the {len(missed)} you missed? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if again != 'y':
            break
        random.shuffle(missed)
        _, _, missed = drill(missed)

    if missed:
        print("Still to review:")
        for c in missed:
            print(f"  - ({c['mod']}) {c['front']}")
    elif seen:
        print("All caught up — nothing left to review.")

if __name__ == '__main__':
    main()
