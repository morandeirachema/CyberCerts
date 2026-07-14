# scripts/

Small helper tools for the repo (stdlib Python — no dependencies).

| Script | What it does |
|---|---|
| [`quiz.py`](quiz.py) | **Terminal flashcard quiz** over the module decks — self-rate, get a score, review misses. No Anki needed. |
| [`validate.py`](validate.py) | **Repo integrity check** — verifies links, in-page anchors, Mermaid blocks, and flashcard CSVs. Run before committing; CI runs it on every push. |
| [`build_anki.py`](build_anki.py) | **Build an Anki `.apkg`** from the module decks (one subdeck per module). Needs `pip install genanki`. |

## Quiz
```bash
python3 scripts/quiz.py                 # all 20 decks, shuffled
python3 scripts/quiz.py --module 06     # just System Hacking
python3 scripts/quiz.py --tag kerberos  # cards tagged with 'kerberos'
python3 scripts/quiz.py --num 20        # a quick 20-card round
python3 scripts/quiz.py --count         # deck sizes only (no quiz)
```

## Build Anki deck
```bash
pip install genanki
python3 scripts/build_anki.py           # -> anki-decks/ceh-v13.apkg (git-ignored)
```
Prefer no dependency? `quiz.py` or import each `flashcards.csv` into Anki directly.

## Validate
```bash
python3 scripts/validate.py             # exits non-zero if anything is broken
```
The same check runs in GitHub Actions ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) on every push, so broken links or malformed decks fail the build.

> Lab-provisioning scripts live under [`../labs/scripts/`](../labs/scripts/); the practical challenge generator is [`../practical/challenge-lab/setup-challenges.sh`](../practical/challenge-lab/).
