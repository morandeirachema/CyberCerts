# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **documentation-first study hub** for a systems administrator moving toward a
**Privileged Access Management (PAM) architect** role. It is **vendor-neutral**: PAM is
taught as a discipline, and the certification hubs are exam-body certs (EC-Council CEH,
CompTIA, OffSec, TCM Security, ISC2, cloud providers). It was formed on 2026-09-02 by merging
two earlier repos: a multi-cert hub (formerly *WallixCerts*) and a standalone *CEH* course
repo (now `certs/ceh/`, history preserved).

**Scope decision to respect:** vendor PAM certification tracks — **WALLIX, CyberArk,
Palo Alto Networks** — are deliberately **excluded** and must not be re-added. Vendors may
appear only as market facts (`foundations/pam-market-landscape.md`) or as a clearly
labelled worked architecture example (`certs/ceh/defender-pam/pam-architecture.md`).

**The owner's path:** WALLIX certs are behind them; **CEH is the current/next cert**, chosen
to learn the fundamentals. The root `README.md` and `learning/roadmap.md` are organised as a
*professional skill path* (four levels, ten competencies, certs as milestones), not a cert
list — keep that framing when editing them.

## Folder layout

- **`certs/`** — one self-contained hub per certification, each with its own `README.md`:
  - **`certs/ceh/`** (primary) — two layers in one folder: the *concept pages*
    (`00-overview/`, `domains/`, `tools/`, `exam-prep/`, `career/`, `reference/`,
    `labs/building-a-ceh-lab.md`, `labs/practice-ranges.md`) and the *full course* merged
    from the CEH repo (`modules/NN-*/` with `README` + `facts.md` + `practice-questions.md`
    + `flashcards.csv` + `lab-walkthrough.md`, `kali/`, `labs/` infra, `practical/`,
    `defender-pam/`, `ot-security/`, `cheatsheets/`, `resources/`, `scripts/`, and the
    top-level `ROADMAP.md`, `STUDY-PLAN.md`, `EXAM-*.md`, `MOCK-EXAM*.md`, `RAPID-FIRE.md`,
    `GLOSSARY.md`, `PROGRESS.md`, `KNOWN-LIMITATIONS.md`, `AI-*.md`, `BLUEPRINT-COVERAGE.md`,
    `KALI-TUTORIAL.md`).
  - `certs/security-plus/`, `certs/cysa-plus/`, `certs/pentest-plus/` (CompTIA),
    `certs/oscp/` (OffSec), `certs/pnpt/` (TCM Security), `certs/adjacent-certs/`
    (one-page overviews: CISSP, cloud security, plus short orientations).
- **Shared fundamentals at root**: `foundations/` (PAM concepts, threats, market) →
  `prerequisites/` (Linux, the PAM engineer's CLI, Windows/AD, networking, crypto) →
  `protocols/` (Kerberos, AD, LDAP, RADIUS, TLS, SSH, SAML, OIDC mechanisms), plus
  `reference/` (glossary, acronyms, compliance, sources), `learning/` (roadmap, platforms)
  and `attack-to-defense-matrix.md` (CEH attacks ↔ PAM controls, MITRE ATT&CK IDs).
- `scripts/` (quality gate, Mermaid wrapper, site builder), `.github/workflows/`, `mkdocs.yml`.

Cross-folder links are relative (`../<folder>/<file>.md`; from `certs/<hub>/<section>/` the
root is `../../../`). The root `README.md` is the whole-repo map and `certs/README.md`
indexes the hubs.

## Two gates, two conventions

| Area | Gate | Run |
|------|------|-----|
| Everything except `certs/ceh/` | `scripts/check-docs.py` (`quality.yml`): no ASCII art, balanced fences, valid Mermaid with fit-to-text labels, a `## Sources` section per content page, zero broken links/anchors | `python3 scripts/check-docs.py` |
| `certs/ceh/` | `certs/ceh/scripts/validate.py` (`ceh-validate.yml`, runs with `working-directory: certs/ceh`): links, anchors, Mermaid, flashcard CSVs; plus py_compile, docker compose config, Ansible YAML, ShellCheck | `cd certs/ceh && python3 scripts/validate.py` |

`check-docs.py` still **link-checks** `certs/ceh/` (so cross-links between the two layers
stay valid) but does not apply its style rules there (`STYLE_EXEMPT_DIRS`); the CEH
template `modules/00-TEMPLATE.md` is skipped for links. Run **both** gates before committing.

## Sourcing discipline (most important)

**NO FABRICATION is a hard rule** (the repo owner insists): never invent facts, figures,
dates, URLs, product behaviors, or exam questions presented as real. Every claim traces to a
cited source or is clearly labeled as a pedagogical example/estimate.

- Exam specifics come from the exam body (EC-Council, CompTIA, OffSec, TCM, ISC2, Microsoft,
  AWS). Where a fact is unknown, write **"not specified in sources"**. The CEH hub
  deliberately does **not** print blueprint domain weights (public sources disagree).
- Practice questions are **original**, never dumps.
- Every content page outside `certs/ceh/` ends with a **Sources** list of the URLs used.

## Conventions

- **Diagrams are always Mermaid, never ASCII art.** Quote labels with special chars, use
  `<br/>` for line breaks (each line ≤ ~36–44 chars; `scripts/wrap-mermaid-labels.py`
  auto-wraps), alphanumeric node IDs, no reserved words (`end`, `graph`, `subgraph`) as IDs.
- **Offensive content stays conceptual/defensive** — countermeasures and written-authorization
  framing, never weaponized how-tos; hands-on work goes to the isolated `certs/ceh/labs/`.
- **Dates** are written absolute (e.g. "2026-09-02"), not relative.
- **Commits:** do not include any author/tool attribution lines (no "Co-Authored-By",
  no Claude references) — repo-wide convention.
- When adding a page: put it in the right hub/section, add it to that folder's `README.md`
  index and (if it belongs in the site nav) to `mkdocs.yml`; new sources go to
  `reference/sources.md`. New cert hubs also go on the path in the root `README.md`,
  `certs/README.md` and `learning/roadmap.md`.
