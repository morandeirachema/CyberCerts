# Known Limitations & How to Verify

Read this once before you rely on the repo. It's here so you study with the right guardrails — not to undersell the material, but to be honest about what it is and where to double-check.

## How this repo was built
This is a **self-built study kit, substantially AI-assisted** (drafted with an AI coding agent, then organized and cross-linked). It is **structurally validated** on every change — [`scripts/validate.py`](scripts/validate.py) / CI check that links, anchors, Mermaid diagrams, and flashcard decks are all well-formed — but it has **not** been line-by-line expert-reviewed. Treat it as a strong, well-organized study companion, **not** an infallible reference.

## What to verify against a primary source
Trust these areas *only* after confirming them yourself:

| Topic | Verify against | Why |
|---|---|---|
| **Exam logistics** — question count, duration, **cut score**, blueprint domain weights, eligibility, cost | [EC-Council](https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/) only | Policy changes; the repo deliberately **does not print** made-up domain weights (see [EXAM-LOGISTICS.md](EXAM-LOGISTICS.md)) |
| **Command syntax & flags** | the tool's own `--help` / `man` page | Tools change between versions; a flag here may differ on your Kali build |
| **CVE / CVSS specifics** | [NVD](https://nvd.nist.gov/) | Scores and details get revised |
| **Vendor product features** (CyberArk, Microsoft, cloud) | the vendor's docs | Named components/features evolve; the repo links `docs.cyberark.com`, `learn.microsoft.com`, etc. |
| **A practice-question answer you disagree with** | the module guide + the primary source | The questions are original/concept-based; an occasional imperfect stem is possible — treat a dispute as a prompt to check, not gospel |

## Lab & drill answers are *representative*, not guaranteed
- **Exact answers:** Metasploitable2 facts, the DVWA/Juice Shop labs, and the [challenge-lab](practical/challenge-lab/README.md) artifacts (stego/pcap/crypto/hashes) are deterministic — the answers in the drills are correct.
- **Representative answers:** the **Windows AD lab** is one *you* build with *your own* passwords and eval-VM build. So AD drill/exam answers (service-account passwords, exact NT hashes, OS build strings, port counts) are **illustrative** — always read *your own* tool output. The drills say this throughout.

## Practice questions are original — not exam dumps
Every question (module `practice-questions.md`, the [mocks](MOCK-EXAM-FULL.md), the [rapid-fire bank](RAPID-FIRE.md)) is **self-authored to teach concepts**. They are **not** real or leaked exam items — using dumps violates the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and can revoke your cert. The point is understanding, not memorizing an item bank.

## What this repo is *not*
- Not a replacement for **official EC-Council courseware** or **hands-on time** on authorized ranges.
- Not a guarantee of a pass — it's a comprehensive scaffold; the reps are on you.
- Not authorization to attack anything. **Every technique is for your own lab or systems you have written permission to test.** Unauthorized access is a crime.

## Found an error? Fix it
This is exactly the kind of repo that improves with corrections:
1. Edit the file.
2. Run `python3 scripts/validate.py` (must pass).
3. Commit / open a PR. CI re-validates automatically.

> **Bottom line:** use it as your map and your drill ground — but for any fact you'll stake a decision on (a command you'll run on a real engagement, an exam date you'll book, a CVSS you'll report), confirm it at the source. That habit is itself part of becoming good at this.
