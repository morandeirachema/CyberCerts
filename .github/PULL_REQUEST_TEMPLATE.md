<!-- Thanks for contributing. Please confirm the checklist below. -->

## What this changes

Briefly describe the addition/fix and which page(s) it touches.

## Checklist

- [ ] **No fabrication** — every factual claim is cited (or clearly marked as a pedagogical
      example / "not specified in sources"). See `CONTRIBUTING.md`.
- [ ] Each new/changed page ends with a **`## Sources`** section.
- [ ] Diagrams are **Mermaid**, never ASCII art.
- [ ] Acronyms are expanded on first use; cross-links are **relative** and resolve.
- [ ] I ran both gates locally and they pass: `python3 scripts/check-docs.py` and
      `(cd certs/ceh && python3 scripts/validate.py)`.
- [ ] Nothing vendor-certification-specific (WALLIX / CyberArk / Palo Alto tracks) was added — see the scope note in `CONTRIBUTING.md`.
