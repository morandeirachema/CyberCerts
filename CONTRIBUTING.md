# Contributing

This repo is an **unofficial, source-grounded, vendor-neutral study hub** for a sysadmin
moving toward a Privileged Access Management (PAM) architect role. Contributions are
welcome — but accuracy is the whole point of the project, so please follow these rules.

## The one hard rule: no fabrication

**Never invent facts, figures, dates, URLs, product behaviors, or exam questions
presented as real.** Every factual claim must either:

- trace to a cited official source (exam-body pages, standards bodies, RFCs, vendor docs), or
- be clearly labeled as a pedagogical example, estimate, or "suggested" value.

If you don't know something, write **"not specified in sources"** — do not guess. Flag
any uncertainty inline. Practice questions must be original and carry the disclaimer that
they are unofficial study aids, not real exam content — **never exam dumps**.

## Scope

- **In scope:** vendor-neutral PAM / identity-security knowledge, the protocols beneath it,
  and study hubs for vendor-neutral or exam-body certifications (EC-Council, CompTIA,
  OffSec, TCM Security, ISC2, cloud-provider security certs).
- **Out of scope by design:** vendor PAM certification tracks (WALLIX, CyberArk,
  Palo Alto Networks, …). Vendors may appear as market facts (analyst placements) or as a
  clearly labelled worked architecture example, never as a certification hub.

## Sourcing

- Prefer the **exam body's official pages** for cert specifics (EC-Council, CompTIA, OffSec,
  TCM Security, ISC2, Microsoft, AWS). Use reputable sources (NIST, MITRE ATT&CK, RFCs,
  ENISA, standards bodies, analyst press) for general topics.
- **Every content page ends with a `## Sources` section** listing the URLs actually used.
  (The CEH course under `certs/ceh/` follows its own conventions — see below.)
- When citing a PDF whose served version differs from its URL label, note the served version.

## Page conventions

- Start with an `# H1` title, a 1–2 sentence intro, and a short "Learning objectives" or
  key-points list where it fits.
- Lean into the three things this repo is built around: **concepts** explained from first
  principles, **flows** (diagrams — see the Diagrams rule below), and **acronyms** (expand
  every acronym on first use, e.g. "Privileged Access Management (PAM)").
- Use tables, lists, and fenced code blocks. Write **dates absolute** (e.g. `2026-09-02`).
- **Cross-link with relative paths.** Top-level folders are siblings, so use
  `../<folder>/<file>.md`; from inside a cert hub, count the depth (`../../../` from
  `certs/<hub>/<section>/`).
- No author or tool attribution anywhere in files **or commit messages**.

### Diagrams — always Mermaid, never ASCII art

Author **every diagram as a GitHub-rendered [Mermaid](https://mermaid.js.org/) block**
(` ```mermaid `). Do **not** use ASCII / box-drawing art. Pick the fitting type:

| Use for | Mermaid type |
|---------|--------------|
| Processes, architecture, topologies, decision trees | `flowchart TD` / `LR` |
| Protocol / message exchanges between parties | `sequenceDiagram` |
| Data models / entity relationships | `erDiagram` |
| 2×2 analyst positioning | `quadrantChart` |
| Time-phased roadmaps | `timeline` |

Syntax rules so it renders on GitHub: quote labels containing spaces/special characters
(`id["Text (parens), a/b"]`), use `<br/>` for line breaks, keep node IDs alphanumeric, and
never use reserved words (`end`, `graph`, `subgraph`) as IDs. Leave genuine
code/CLI/config blocks as code. Translate faithfully — never invent steps or facts.

**Boxes must fit their text.** Keep each node-label line short (≈ ≤ 36 characters) and
**wrap long labels with `<br/>`**. Run **`python scripts/wrap-mermaid-labels.py`** to
auto-wrap them; the quality gate (`scripts/check-docs.py`) fails on over-wide flowchart labels.

## Two gates, two conventions

| Area | Gate | Conventions |
|------|------|-------------|
| Whole repo | [`scripts/check-docs.py`](scripts/check-docs.py) (workflow `quality.yml`) | Rules above: Mermaid only, no ASCII, fit-to-text labels, zero broken links/anchors, well-formed `flashcards.csv` rows; a `## Sources` per content page everywhere except `certs/ceh/` |
| `certs/ceh/` (the merged CEH course) | [`certs/ceh/scripts/validate.py`](certs/ceh/scripts/validate.py) (workflow `ceh-validate.yml`) + link-checking by `check-docs.py` | Its own structure: per-module `README` + `facts.md` + `practice-questions.md` + `flashcards.csv` + `lab-walkthrough.md`; see [`certs/ceh/KNOWN-LIMITATIONS.md`](certs/ceh/KNOWN-LIMITATIONS.md) and [`certs/ceh/scripts/README.md`](certs/ceh/scripts/README.md) |

Run both locally before committing:

```bash
python3 scripts/check-docs.py
(cd certs/ceh && python3 scripts/validate.py)
```

## Adding a new page

1. Put it in the right folder. Shared fundamentals stay at the root (`foundations/`,
   `prerequisites/`, `protocols/`, `reference/`, `learning/`); each certification is its own
   hub under `certs/` (`certs/ceh/`, `certs/security-plus/`, `certs/cysa-plus/`,
   `certs/pentest-plus/`, `certs/oscp/`, `certs/pnpt/`, `certs/adjacent-certs/`).
2. Add a row for it in that folder's `README.md` index (and in `mkdocs.yml` if it should
   appear in the site nav).
3. If it's a new certification hub, mirror an existing hub's structure
   (`00-overview/` → `domains/` → `exam-prep/` → `reference/`), add it to
   `certs/README.md`, and place it on the path in the root `README.md` and
   `learning/roadmap.md`.
4. Add any new authoritative URLs to `reference/sources.md`.

## Periodic verification checklist

Some facts drift over time. Re-check these against primary sources before relying on them,
and update the affected pages + their `## Sources`:

- [ ] **Exam versions and codes** — CEH v13 (312-50), Security+ SY0-701, CySA+ CS0-003,
      PenTest+ PT0-003, OSCP/OSCP+ (PEN-200), PNPT, CISSP; check for newer versions and
      retirement dates on each provider's site.
- [ ] **Exam logistics** (question counts, durations, cut scores, prices) — verify on the
      provider before booking; the CEH hub's `EXAM-LOGISTICS.md` is the model.
- [ ] **Analyst placements (change yearly):** Gartner Magic Quadrant for PAM and
      KuppingerCole Leadership Compass for PAM — update `foundations/pam-market-landscape.md`.
- [ ] **Cloud certs** flagged as time-sensitive in `certs/adjacent-certs/`: Microsoft
      **SC-500** (successor to AZ-500, retired 2026-08-31) and the AWS Security specialty (SCS-C03).
- [ ] **CompTIA exam versions:** CySA+ CS0-003 → CS0-004 (CS0-003 English retires
      2026-12-22) and Security+ SY0-701 → SY0-801 (SY0-801 launches around 2026-11-17).
- [ ] **Regulations** in `reference/compliance-and-standards.md` — NIS2 transposition
      status, DORA, ISO 27001 edition.

## License & disclaimer

By contributing you agree to license your contribution under the repository's
[LICENSE](LICENSE). This project is **not affiliated with or endorsed by** EC-Council,
CompTIA, OffSec, TCM Security, ISC2, or any PAM vendor; certification and product names
are trademarks of their respective owners and are used here for identification and
educational purposes only.
