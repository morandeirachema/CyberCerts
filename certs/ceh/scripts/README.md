# scripts/

Small helper tools for the repo (stdlib Python — no dependencies).

| Script | What it does |
|---|---|
| [`quiz.py`](quiz.py) | **Terminal flashcard quiz** over the module decks — self-rate, get a score, review misses. No Anki needed. |
| [`validate.py`](validate.py) | **Repo integrity check** — verifies links, in-page anchors, Mermaid blocks, and flashcard CSVs. Run before committing; CI runs it on every push. |
| [`build_anki.py`](build_anki.py) | **Build an Anki `.apkg`** from the module decks (one subdeck per module). Needs `pip install genanki`. |

## Quiz
```bash
python3 scripts/quiz.py                    # all 20 decks, shuffled
python3 scripts/quiz.py --module 06        # just System Hacking
python3 scripts/quiz.py --tag kerberos     # cards tagged with 'kerberos'
python3 scripts/quiz.py --num 20 --seed 7  # a reproducible 20-card round
python3 scripts/quiz.py --list-tags        # every tag with a card count
python3 scripts/quiz.py --count            # deck sizes only (no quiz)
```
At the end of a round it offers to **re-drill just the cards you missed**, looping until the pile is empty.

## Build Anki deck
```bash
pip install genanki
python3 scripts/build_anki.py           # -> anki-decks/ceh-v13.apkg (git-ignored)
```
Notes carry a **stable GUID** (module + front), so re-importing a regenerated deck updates existing cards in place instead of creating duplicates. Prefer no dependency? `quiz.py`, or import each `flashcards.csv` into Anki directly.

## Validate
```bash
python3 scripts/validate.py             # exits non-zero if anything is broken
python3 scripts/validate.py --selftest  # unit-test the link/anchor slug logic only
```
Link and anchor checks follow GitHub's own slug rules (fenced code blocks are ignored, underscores are kept, and duplicate headings get a `-1`/`-2` suffix). The same check runs in GitHub Actions ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)) on every push — alongside `py_compile`, the slug self-test, `docker compose config`, Ansible YAML parsing, and ShellCheck — so broken links, malformed decks, or a broken script fail the build.

> Lab-provisioning scripts live under [`../labs/scripts/`](../labs/scripts/); the practical challenge generator is [`../practical/challenge-lab/setup-challenges.sh`](../practical/challenge-lab/).
