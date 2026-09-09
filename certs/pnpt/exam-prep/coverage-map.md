# PNPT — Coverage Map

This page is **Step 2** of the repo's [how to prepare a certification](../../../learning/how-to-prepare-a-cert.md)
method: the **contract between you and the exam**. For the PNPT the contract is an
engagement, not a question bank: TCM Security describes what the assessment covers on the
official PNPT page, and the exam is graded on the **report** and the **live debrief**. This
map lists everything this hub teaches, grouped by the hub's five engagement phases, so you
can line it up against TCM's own description and see what is covered, what is thin, and what
is missing.

The rows are the **section headings that exist in this hub's five phase pages** — nothing
more. TCM's own item numbering or wording is **not** reproduced here (the hub does not carry
it, and this page will not invent it), so the first column is yours to fill.

**How to fill it in:**

1. Open the official **PNPT page** (https://certifications.tcm-sec.com/pnpt/ — linked from
   [what is PNPT](../00-overview/what-is-pnpt.md)) and note every area TCM says the exam
   covers; if the bundled training courses publish a syllabus, use that too (whether they do
   is not specified in this hub's sources). Write each item as TCM words it.
2. Walk that list item by item. For each one, find the matching row below and write TCM's
   item in the first column. One item may span several rows, and one row may cover several
   items — record all of them.
3. Any item with **no matching row** goes in the [gaps table](#gaps-you-found) at the end,
   marked **"gap"**, with a note on where you will learn it. The hub's own
   [engagement scope table](../00-overview/what-is-pnpt.md#the-engagement-scope-conceptual)
   lists *AV / egress bypass* as its own phase; here it sits inside Phase 4 — check whether
   TCM treats it separately.
4. Then score every row **0–3** (the scale is in
   [Step 3 of the method](../../../learning/how-to-prepare-a-cert.md#step-3--self-assess)).
   For an engagement-style exam, *Practised?* means **done in your AD lab, from your own
   notes, and written up as a finding** — not read.

> TCM publishes no domain weights for the PNPT *(not specified in sources)*; the phases
> below are the hub's teaching order, which follows the engagement workflow
> (see [how the phases map to the exam](../topics/README.md#how-the-phases-map-to-the-exam)).

## How to use

- **Before studying:** fill the first column and the self-score column; the zeros and ones are
  your syllabus. Phases 3 and 4 are where a sysadmin's AD knowledge pays off — and where the
  defender's mirror in the [attack → defense matrix](../../../attack-to-defense-matrix.md) is
  most useful for the debrief.
- **During the study loop:** after each phase page, revisit its rows — raise the score, tick
  *Practised?* only after the lab, and use *Notes* for the finding you wrote up.
- **Before booking:** the readiness gate in the [hub README](../README.md) needs the full
  workflow (external foothold → domain compromise) end-to-end in the lab, a report drafted and
  the debrief rehearsed twice; every row here should be at 2 or 3 first.
- **Where a row has a `↳`**, it is a subsection of the row above it; score it separately only if
  TCM's list treats it as its own item.
- Rows link straight to the section, so this page doubles as the hub's fastest index.

## Coverage map

### Phase 1 — OSINT & reconnaissance

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | What OSINT is | [P1 → section](../topics/01-osint-and-reconnaissance.md#what-osint-is) | __ | ☐ | |
| ____ | What an attacker gathers | [P1 → section](../topics/01-osint-and-reconnaissance.md#what-an-attacker-gathers) | __ | ☐ | |
| ____ | The attacker's external view | [P1 → section](../topics/01-osint-and-reconnaissance.md#the-attackers-external-view) | __ | ☐ | |
| ____ | Tools by purpose | [P1 → section](../topics/01-osint-and-reconnaissance.md#tools-by-purpose) | __ | ☐ | |
| ____ | Defense — reducing what attackers can see | [P1 → section](../topics/01-osint-and-reconnaissance.md#defense--reducing-what-attackers-can-see) | __ | ☐ | |

### Phase 2 — External penetration testing

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | What external testing assesses | [P2 → section](../topics/02-external-penetration-testing.md#what-external-testing-assesses) | __ | ☐ | |
| ____ | Finding and assessing internet-facing services | [P2 → section](../topics/02-external-penetration-testing.md#finding-and-assessing-internet-facing-services) | __ | ☐ | |
| ____ | Password attacks against external services (concept) | [P2 → section](../topics/02-external-penetration-testing.md#password-attacks-against-external-services-concept) | __ | ☐ | |
| ____ | Gaining an initial foothold | [P2 → section](../topics/02-external-penetration-testing.md#gaining-an-initial-foothold) | __ | ☐ | |
| ____ | Defense — hardening the perimeter | [P2 → section](../topics/02-external-penetration-testing.md#defense--hardening-the-perimeter) | __ | ☐ | |

### Phase 3 — Active Directory exploitation

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | Why AD is the target | [P3 → section](../topics/03-active-directory-exploitation.md#why-ad-is-the-target) | __ | ☐ | |
| ____ | AD enumeration | [P3 → section](../topics/03-active-directory-exploitation.md#ad-enumeration) | __ | ☐ | |
| ____ | Credential-attack concepts | [P3 → section](../topics/03-active-directory-exploitation.md#credential-attack-concepts) | __ | ☐ | |
| ____ | Domain Controller compromise (concept) | [P3 → section](../topics/03-active-directory-exploitation.md#domain-controller-compromise-concept) | __ | ☐ | |
| ____ | Defense — how PAM, tiering, and detection stop the chain | [P3 → section](../topics/03-active-directory-exploitation.md#defense--how-pam-tiering-and-detection-stop-the-chain) | __ | ☐ | |

### Phase 4 — Lateral movement & pivoting

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | Three kinds of movement | [P4 → section](../topics/04-lateral-movement-and-pivoting.md#three-kinds-of-movement) | __ | ☐ | |
| ____ | Pivoting and tunneling (concept) | [P4 → section](../topics/04-lateral-movement-and-pivoting.md#pivoting-and-tunneling-concept) | __ | ☐ | |
| ____ | AV and egress bypass — how detection works (not how to evade) | [P4 → section](../topics/04-lateral-movement-and-pivoting.md#av-and-egress-bypass--how-detection-works-not-how-to-evade) | __ | ☐ | |
| ____ | Defense — containing movement | [P4 → section](../topics/04-lateral-movement-and-pivoting.md#defense--containing-movement) | __ | ☐ | |

### Phase 5 — Reporting & the debrief

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | Why reporting is graded | [P5 → section](../topics/05-reporting-and-the-debrief.md#why-reporting-is-graded) | __ | ☐ | |
| ____ | Report structure | [P5 → section](../topics/05-reporting-and-the-debrief.md#report-structure) | __ | ☐ | |
| ____ | ↳ Findings and CVSS | [P5 → subsection](../topics/05-reporting-and-the-debrief.md#findings-and-cvss) | __ | ☐ | |
| ____ | The live debrief | [P5 → section](../topics/05-reporting-and-the-debrief.md#the-live-debrief) | __ | ☐ | |
| ____ | ↳ Preparing for it | [P5 → subsection](../topics/05-reporting-and-the-debrief.md#preparing-for-it) | __ | ☐ | |
| ____ | Defense angle | [P5 → section](../topics/05-reporting-and-the-debrief.md#defense-angle) | __ | ☐ | |

### Cross-cutting exam skills

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | The 5-day assessment | [Exam structure](../00-overview/exam-structure.md#phase-1--the-5-day-assessment) | __ | ☐ | |
| ____ | The 2-day report | [Exam structure](../00-overview/exam-structure.md#phase-2--the-2-day-report) | __ | ☐ | |
| ____ | The live 15-minute debrief | [Exam structure](../00-overview/exam-structure.md#phase-3--the-live-15-minute-debrief) | __ | ☐ | |
| ____ | Tooling and retake policy | [Exam structure](../00-overview/exam-structure.md#tooling-and-retake-policy) | __ | ☐ | |


## Gaps you found

One row per official objective that has **no matching row above**. Decide where you will learn it (another page in this repo, the exam body's own material, a lab) and add that source to your plan.

| Official objective | What is missing | Where you will learn it |
|---|---|---|
| | | |
| | | |
| | | |

## Sources

- TCM Security — PNPT certification page: <https://certifications.tcm-sec.com/pnpt/>
- This hub: [what is PNPT](../00-overview/what-is-pnpt.md) · [exam structure](../00-overview/exam-structure.md) · [engagement phases index](../topics/README.md) · [P1](../topics/01-osint-and-reconnaissance.md) · [P2](../topics/02-external-penetration-testing.md) · [P3](../topics/03-active-directory-exploitation.md) · [P4](../topics/04-lateral-movement-and-pivoting.md) · [P5](../topics/05-reporting-and-the-debrief.md)
- Method: [how to prepare a certification](../../../learning/how-to-prepare-a-cert.md) (Step 2, coverage map) · worked example: [CEH blueprint coverage](../../ceh/BLUEPRINT-COVERAGE.md)
