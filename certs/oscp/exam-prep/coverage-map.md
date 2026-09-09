# OSCP / OSCP+ (PEN-200) — Coverage Map

This page is **Step 2** of the repo's [how to prepare a certification](../../../learning/how-to-prepare-a-cert.md)
method: the **contract between you and the exam**. For OSCP the contract is different from a
knowledge exam: OffSec publishes no weighted domain list, the exam *is* the lab, and the
authoritative scope is the **PEN-200 course outline** plus the **OSCP+ exam guide**. This map
lists everything this hub teaches, grouped by the hub's six skill areas (a teaching breakdown,
[not an OffSec-defined syllabus](../topics/README.md)), so you can line it up against OffSec's
own outline and see what is covered, what is thin, and what is missing.

The rows are the **section headings that exist in this hub's six skill-area pages** — nothing
more. Official module numbers or names are **not** reproduced here (the hub does not carry
OffSec's outline, and this page will not invent it), so the first column is yours to fill.

**How to fill it in:**

1. Open the official **PEN-200 course outline** on OffSec's course page
   (https://www.offsec.com/courses/pen-200/ — linked from
   [what is OSCP](../00-overview/what-is-oscp.md)) and the
   [OSCP+ exam guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide).
   Whether OffSec offers the outline as a PDF or a web page is not specified in this hub's
   sources — record whatever identifier OffSec uses (module number or module name).
2. Walk the outline module by module. For each one, find the matching row below and write the
   module identifier in the first column. One module may span several rows, and one row may
   cover several modules — record all of them.
3. Any module with **no matching row** goes in the [gaps table](#gaps-you-found) at the end,
   marked **"gap"**, with a note on where you will learn it. Expect gaps: this hub is
   conceptual and defence-mapped by design (no exploit code, no weaponised playbooks), so the
   hands-on depth comes from the course labs and
   [authorised practice platforms](../../../learning/platforms.md).
4. Then score every row **0–3** (the scale is in
   [Step 3 of the method](../../../learning/how-to-prepare-a-cert.md#step-3--self-assess)).
   For a hands-on exam, *Practised?* means **done on a machine, from your own notes, and
   written up** — not read.

> There are no per-skill weights: the exam's only published split is by **points**
> (AD set of 3 machines = 40, three standalone machines = 60, 70 to pass) — see
> [exam structure](../00-overview/exam-structure.md#how-the-100-points-are-distributed).
> That makes skill areas 5 and 6 (and 4, which every machine needs) the highest-value rows.

## How to use

- **Before studying:** fill the first column and the self-score column; the zeros and ones are
  your syllabus, and a 3 means *cold, under time, from your notes*.
- **During the study loop:** after each skill-area page, revisit its rows — raise the score,
  tick *Practised?* only after a machine, and use *Notes* for the machine name and the date.
- **Before booking:** the readiness gate in the [hub README](../README.md) needs the AD set
  end-to-end, a mixed standalone set, a full report and a 24-hour dress rehearsal; every row
  here should be at 2 or 3 first.
- **Where a row has a `↳`**, it is a subsection of the row above it; score it separately only if
  the outline treats it as its own module.
- Rows link straight to the section, so this page doubles as the hub's fastest index.

## Coverage map

### Skill area 1 — Enumeration & information gathering

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | Passive vs. active reconnaissance | [S1 → section](../topics/01-enumeration-and-information-gathering.md#passive-vs-active-reconnaissance) | __ | ☐ | |
| ____ | The enumeration workflow | [S1 → section](../topics/01-enumeration-and-information-gathering.md#the-enumeration-workflow) | __ | ☐ | |
| ____ | Port and service enumeration | [S1 → section](../topics/01-enumeration-and-information-gathering.md#port-and-service-enumeration) | __ | ☐ | |
| ____ | Per-service deep dives | [S1 → section](../topics/01-enumeration-and-information-gathering.md#per-service-deep-dives) | __ | ☐ | |
| ____ | Tools and their purpose | [S1 → section](../topics/01-enumeration-and-information-gathering.md#tools-and-their-purpose) | __ | ☐ | |

### Skill area 2 — Web application attacks

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | The common root cause | [S2 → section](../topics/02-web-application-attacks.md#the-common-root-cause) | __ | ☐ | |
| ____ | The web attack surface (defense view) | [S2 → section](../topics/02-web-application-attacks.md#the-web-attack-surface-defense-view) | __ | ☐ | |
| ____ | The attack classes | [S2 → section](../topics/02-web-application-attacks.md#the-attack-classes) | __ | ☐ | |
| ____ | ↳ SQL injection (SQLi) | [S2 → subsection](../topics/02-web-application-attacks.md#sql-injection-sqli) | __ | ☐ | |
| ____ | ↳ File inclusion — LFI and RFI | [S2 → subsection](../topics/02-web-application-attacks.md#file-inclusion--lfi-and-rfi) | __ | ☐ | |
| ____ | ↳ Unrestricted file upload | [S2 → subsection](../topics/02-web-application-attacks.md#unrestricted-file-upload) | __ | ☐ | |
| ____ | ↳ Command injection | [S2 → subsection](../topics/02-web-application-attacks.md#command-injection) | __ | ☐ | |
| ____ | ↳ Directory (path) traversal | [S2 → subsection](../topics/02-web-application-attacks.md#directory-path-traversal) | __ | ☐ | |
| ____ | ↳ Authentication / access bypass | [S2 → subsection](../topics/02-web-application-attacks.md#authentication--access-bypass) | __ | ☐ | |
| ____ | Tools and their purpose | [S2 → section](../topics/02-web-application-attacks.md#tools-and-their-purpose) | __ | ☐ | |
| ____ | Defense in depth | [S2 → section](../topics/02-web-application-attacks.md#defense-in-depth) | __ | ☐ | |

### Skill area 3 — Password & client-side attacks

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | Two ways in: credentials and the client | [S3 → section](../topics/03-password-and-client-side-attacks.md#two-ways-in-credentials-and-the-client) | __ | ☐ | |
| ____ | Password attacks | [S3 → section](../topics/03-password-and-client-side-attacks.md#password-attacks) | __ | ☐ | |
| ____ | ↳ Online attacks — guessing against a live service | [S3 → subsection](../topics/03-password-and-client-side-attacks.md#online-attacks--guessing-against-a-live-service) | __ | ☐ | |
| ____ | ↳ Offline attacks — cracking captured hashes | [S3 → subsection](../topics/03-password-and-client-side-attacks.md#offline-attacks--cracking-captured-hashes) | __ | ☐ | |
| ____ | ↳ Why long + unique beats "complex" | [S3 → subsection](../topics/03-password-and-client-side-attacks.md#why-long--unique-beats-complex) | __ | ☐ | |
| ____ | Client-side attacks (concept) | [S3 → section](../topics/03-password-and-client-side-attacks.md#client-side-attacks-concept) | __ | ☐ | |
| ____ | Defenses (layered) | [S3 → section](../topics/03-password-and-client-side-attacks.md#defenses-layered) | __ | ☐ | |
| ____ | Tools and their purpose | [S3 → section](../topics/03-password-and-client-side-attacks.md#tools-and-their-purpose) | __ | ☐ | |

### Skill area 4 — Privilege escalation (Linux & Windows)

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | The mental model: enumerate, then escalate | [S4 → section](../topics/04-privilege-escalation.md#the-mental-model-enumerate-then-escalate) | __ | ☐ | |
| ____ | Linux privilege escalation — what to look for and why | [S4 → section](../topics/04-privilege-escalation.md#linux-privilege-escalation--what-to-look-for-and-why) | __ | ☐ | |
| ____ | Windows privilege escalation — what to look for and why | [S4 → section](../topics/04-privilege-escalation.md#windows-privilege-escalation--what-to-look-for-and-why) | __ | ☐ | |
| ____ | The unifying defense: least privilege and PAM | [S4 → section](../topics/04-privilege-escalation.md#the-unifying-defense-least-privilege-and-pam) | __ | ☐ | |

### Skill area 5 — Active Directory attacks

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | The AD attack chain — and where defenses sit | [S5 → section](../topics/05-active-directory-attacks.md#the-ad-attack-chain--and-where-defenses-sit) | __ | ☐ | |
| ____ | Enumeration — the recon stage | [S5 → section](../topics/05-active-directory-attacks.md#enumeration--the-recon-stage) | __ | ☐ | |
| ____ | Credential attacks (conceptual) | [S5 → section](../topics/05-active-directory-attacks.md#credential-attacks-conceptual) | __ | ☐ | |
| ____ | Lateral movement | [S5 → section](../topics/05-active-directory-attacks.md#lateral-movement) | __ | ☐ | |
| ____ | Domain compromise | [S5 → section](../topics/05-active-directory-attacks.md#domain-compromise) | __ | ☐ | |
| ____ | Why this maps cleanly to defense | [S5 → section](../topics/05-active-directory-attacks.md#why-this-maps-cleanly-to-defense) | __ | ☐ | |

### Skill area 6 — Pivoting & tunneling

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | Why an attacker pivots | [S6 → section](../topics/06-pivoting-and-tunneling.md#why-an-attacker-pivots) | __ | ☐ | |
| ____ | Forwarding concepts (no commands) | [S6 → section](../topics/06-pivoting-and-tunneling.md#forwarding-concepts-no-commands) | __ | ☐ | |
| ____ | The defense: segmentation and controlled admin paths | [S6 → section](../topics/06-pivoting-and-tunneling.md#the-defense-segmentation-and-controlled-admin-paths) | __ | ☐ | |
| ____ | Pivot vs. jump host — same shape, opposite intent | [S6 → section](../topics/06-pivoting-and-tunneling.md#pivot-vs-jump-host--same-shape-opposite-intent) | __ | ☐ | |

### Cross-cutting exam skills

| Official objective # (record from the PDF) | Topic area (as covered here) | Where | Self-score 0–3 | Practised? | Notes |
|---|---|---|:---:|:---:|---|
| ____ | How the 100 points are distributed (AD set 40, standalone 60) | [Exam structure](../00-overview/exam-structure.md#how-the-100-points-are-distributed) | __ | ☐ | |
| ____ | Proof flags: local.txt and proof.txt | [Exam structure](../00-overview/exam-structure.md#proof-flags-localtxt-and-prooftxt) | __ | ☐ | |
| ____ | The report: a deliverable you can fail on | [Exam structure](../00-overview/exam-structure.md#the-report-a-deliverable-you-can-fail-on) | __ | ☐ | |
| ____ | Proctoring and integrity | [Exam structure](../00-overview/exam-structure.md#proctoring-and-integrity) | __ | ☐ | |


## Gaps you found

One row per official objective that has **no matching row above**. Decide where you will learn it (another page in this repo, the exam body's own material, a lab) and add that source to your plan.

| Official objective | What is missing | Where you will learn it |
|---|---|---|
| | | |
| | | |
| | | |

## Sources

- OffSec — PEN-200 / OSCP official course page (course outline, fully hands-on): https://www.offsec.com/courses/pen-200/
- OffSec — OSCP+ Exam Guide / Exam FAQ (100 points, 70 to pass, AD set = 40, report window, proctoring): https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide
- This hub: [what is OSCP](../00-overview/what-is-oscp.md) · [exam structure](../00-overview/exam-structure.md) · [skill areas index](../topics/README.md) · [S1](../topics/01-enumeration-and-information-gathering.md) · [S2](../topics/02-web-application-attacks.md) · [S3](../topics/03-password-and-client-side-attacks.md) · [S4](../topics/04-privilege-escalation.md) · [S5](../topics/05-active-directory-attacks.md) · [S6](../topics/06-pivoting-and-tunneling.md)
- Method: [how to prepare a certification](../../../learning/how-to-prepare-a-cert.md) (Step 2, coverage map) · worked example: [CEH blueprint coverage](../../ceh/BLUEPRINT-COVERAGE.md)
