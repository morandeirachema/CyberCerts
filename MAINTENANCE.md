# Maintenance & verification

How this repo stays accurate over time.

## Automated checks (CI)

| Workflow | When | What it enforces |
|----------|------|------------------|
| [`quality.yml`](.github/workflows/quality.yml) | every push / PR | No ASCII art · balanced code fences · valid Mermaid (and no reserved-word node IDs) · a `## Sources` section on every content page · **zero broken internal links/image links/anchors** · well-formed `flashcards.csv` rows in every hub — via [`scripts/check-docs.py`](scripts/check-docs.py). The merged CEH course (`certs/ceh/`) is link-checked but keeps its own style rules. |
| [`ceh-validate.yml`](.github/workflows/ceh-validate.yml) | every push / PR | The CEH course's own gate, run inside `certs/ceh/`: links, anchors, Mermaid, flashcard CSVs, `py_compile` of its scripts, Docker Compose / Ansible YAML validity, ShellCheck — via [`certs/ceh/scripts/validate.py`](certs/ceh/scripts/validate.py) |
| [`external-links.yml`](.github/workflows/external-links.yml) | weekly + on demand | External URL rot (RFCs, vendor docs) — non-blocking |
| [`docs.yml`](.github/workflows/docs.yml) | every push to `main` | Builds & deploys the MkDocs site |

Run the gates locally before committing:

```bash
python3 scripts/check-docs.py
(cd certs/ceh && python3 scripts/validate.py)
```

## Manual re-verification

Some facts drift (cert exam specs, analyst placements, retirement dates). The per-topic
re-verification checklist lives in
[`CONTRIBUTING.md`](CONTRIBUTING.md#periodic-verification-checklist). Volatile items are
marked **"verify on \<provider\>"** or **"not specified in sources"** inline rather than
asserted.

## Verification status

- **2026-09-02 — repository merge.** The CEH course repo and the non-vendor parts of the
  former WALLIX study hub were merged into this repo; all WALLIX certification material was
  removed and cross-references were made vendor-neutral. Both gates pass. See
  [`CHANGELOG.md`](CHANGELOG.md).
- Last structural check (links/Mermaid/ASCII/Sources): enforced continuously by CI.
