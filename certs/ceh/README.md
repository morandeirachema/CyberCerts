# CEH v13 — Study, Labs & Exam Prep

![CEH](https://img.shields.io/badge/CEH-v13%20(312--50)-1f6feb)
![Modules](https://img.shields.io/badge/modules-20%2F20-2da44e)
![Practice questions](https://img.shields.io/badge/practice%20questions-287-e3651d)
![Flashcards](https://img.shields.io/badge/flashcards-620-e3651d)
![Lens](https://img.shields.io/badge/lens-Defender%20%2B%20CyberArk%20PAM-8250df)
![No dumps](https://img.shields.io/badge/no-exam%20dumps-6e7781)

A self-built, **no-fabrications** study repository for the **EC-Council Certified Ethical Hacker (CEH) v13** certification, written from the perspective of a **systems administrator with a Privileged Access Management (PAM) background**.

Every module ties the offensive technique you must learn for the exam back to the **defensive and PAM controls you already understand** — so you learn attacks *through* the controls you manage. It's a complete self-study system: **read → lab → self-test → drill → track.**

> **⚖️ Ethics & scope.** Everything here is for authorized learning only: your own self-hosted lab (see [`labs/`](labs/)), EC-Council's official ranges, or systems you have **written permission** to test. Never point these tools or techniques at systems you do not own or are not explicitly authorized to assess. Unauthorized access is a crime in most jurisdictions.

---

## Contents

- [Start here — pick your path](#start-here--pick-your-path)
- [Why this repo is different](#why-this-repo-is-different)
- [At a glance](#at-a-glance)
- [Quick start](#quick-start)
- [The study loop](#the-study-loop)
- [The 20 modules](#the-20-modules-official-ceh-v13-order)
- [The Defender / PAM lens](#the-defender--pam-lens)
- [Exam facts](#exam-facts-verify-against-ec-council-before-you-book)
- [Repository map](#repository-map)
- [Official references](#official-ec-council-references)

---

## Start here — pick your path

This repo is big; start where you fit and follow the trail.

> 🧭 **Want the whole journey?** [`ROADMAP.md`](ROADMAP.md) sequences everything into a **beginner→master** ladder — foundations → theory → tools → hands-on labs → exams → *beyond CEH* (HTB/OSCP, specializations, red + blue) — with checkpoints and a self-assessment matrix.

- 🌱 **New to Linux / hacking** — begin with the [`kali/`](kali/) course (chapter [00](kali/00-getting-started.md)), which teaches Linux, the terminal, and every tool from zero. Stand up the [lab](labs/), then work the [modules](modules/) in order.
- ⏱️ **Know the tech, need the cert** — read [`EXAM-STRATEGY.md`](EXAM-STRATEGY.md), then per module skim the guide, drill its `facts.md` + `practice-questions.md` + `flashcards.csv`, and check yourself with the [50-](MOCK-EXAM.md) and [125-question](MOCK-EXAM-FULL.md) mocks. Use [`BLUEPRINT-COVERAGE.md`](BLUEPRINT-COVERAGE.md) to confirm coverage.
- 🛡️ **Sysadmin / PAM engineer** — start with the [`defender-pam/`](defender-pam/) knowledge base and [identity attack paths](defender-pam/identity-attack-paths.md), run the [`labs/capstone.md`](labs/capstone.md) chain to see attack→control end-to-end, then skim the modules for the offensive detail.
- 🤖 **Curious about v13's AI focus** — read [`AI-IN-ETHICAL-HACKING.md`](AI-IN-ETHICAL-HACKING.md) and study with [`AI-STUDY-WORKFLOW.md`](AI-STUDY-WORKFLOW.md).
- 🏆 **Going for CEH Master (the hands-on Practical)** — work the [`practical/`](practical/) section: a skills checklist, challenge playbooks, and timed drills for the 6-hour performance exam.

---

## Why this repo is different

- **Every attack is paired with its control.** Each module has a Defender & PAM mapping, and a CyberArk-centered [knowledge base](defender-pam/) sits behind it (reference architecture, AD/Entra identity attack paths, detection engineering). If you can name the control, you can usually eliminate two wrong answers instantly.
- **Built for active recall, not re-reading.** Every module ships a one-page facts sheet, original practice questions with explanations, Anki-ready flashcards, and a guided lab — plus a dedicated [exam-strategy](EXAM-STRATEGY.md) guide.
- **Runnable on infrastructure you control.** Docker web targets + Vagrant VMs + an Ansible **tiered-admin / PAM** Active Directory lab.
- **Covers CEH v13's AI-driven ethical hacking.** A dedicated [AI doc](AI-IN-ETHICAL-HACKING.md) covers using AI across the phases *and* attacking/defending AI systems — and a [blueprint coverage matrix](BLUEPRINT-COVERAGE.md) documents every module's subtopics so you can verify nothing's missing.
- **No exam dumps, no invented facts.** Practice questions are self-authored to teach concepts; every external claim links to an official source.

### What this repo is *not*
- Not a brain dump of exam questions — dumps violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certifications revoked.
- Not a replacement for the official courseware. Confirm every blueprint weight and policy against EC-Council directly (links at the bottom).

---

## At a glance

| | |
|---|---|
| 🧭 **Learning roadmap** | [beginner→master ladder](ROADMAP.md) sequencing the whole repo + what to do after CEH |
| 📘 **Module guides** | 20 — full concept coverage in official CEH v13 order |
| 🗂️ **Study companions** | 80 files — every module has `facts.md`, `practice-questions.md`, `flashcards.csv`, `lab-walkthrough.md` |
| ❓ **Practice questions** | 287 original, concept-based, with collapsible explanations |
| 🃏 **Flashcards** | 620 Anki-ready cards, tagged per module |
| 🛡️ **Defender/PAM knowledge base** | attack→control matrix · PAM playbook · CyberArk architecture · identity attack paths · detection engineering · CyberArk mapping |
| 🧪 **Lab** | Docker web targets + Vagrant (Kali + Metasploitable) + Ansible **AD/ADCS** lab with planted attack paths + a chained [capstone](labs/capstone.md) engagement |
| 🐉 **Kali** | a [beginner→mastery course](kali/) (17 chapters, from "what is Linux" to attacking AD) + a one-page [reference](KALI-TUTORIAL.md), all against the lab |
| 🧠 **AI study workflow** | copy-paste [AI-tutor prompts](AI-STUDY-WORKFLOW.md) wired to the repo (Socratic quiz, miss→flashcards, Feynman check) |
| 🏆 **CEH Practical** | hands-on [CEH Master prep](practical/): skills checklist, challenge playbooks, timed lab drills |
| 🎯 **Exam prep** | strategy guide, glossary/acronym index, **50- + 125-question mocks + a 200-question rapid-fire bank**, 12-week plan, progress tracker |
| 🤖 **AI-driven hacking** | AI across each phase + attacking/defending AI (LLM Top 10, adversarial ML) — CEH v13's headline topic |
| 🧭 **Coverage matrix** | per-module subtopic checklist mapped to where each topic is covered |

---

## Quick start

```bash
# 1) get the repo
git clone https://github.com/morandeirachema/CEH.git && cd CEH

# 2) confirm eligibility + current blueprint, then stand up the lab
#    (read EXAM-LOGISTICS.md, then follow labs/README.md)
cd labs && ./scripts/setup.sh        # Docker web targets; see labs/README.md for VMs

# 3) read the study system once, then start Module 01
#    open EXAM-STRATEGY.md, then modules/01-introduction-to-ethical-hacking/
```

New here? Read [`EXAM-STRATEGY.md`](EXAM-STRATEGY.md) first — it explains *how* to use the companions (active recall + spaced repetition), which is what actually moves the score.

---

## The study loop

Work each module in this order. The companion files (linked from the top of every module's `README.md`) are built to be used in exactly this sequence.

```mermaid
flowchart LR
    R["1. READ<br/>module guide"] --> L["2. LAB<br/>lab-walkthrough.md"]
    L --> M["3. MAP<br/>Defender & PAM section"]
    M --> T["4. TEST<br/>practice-questions.md"]
    T --> D["5. DRILL<br/>flashcards.csv → Anki"]
    D --> K["6. TRACK<br/>PROGRESS.md"]
    K -.->|"spaced repetition"| F["facts.md<br/>final-week cram"]
    F -.-> R
```

1. **Read** the module `README.md` — concepts + exam-testable facts.
2. **Lab** the `lab-walkthrough.md` against **your** targets; record results in the module's lab-log table.
3. **Map** the Defender & PAM section — your retention hook (deep dives in [`defender-pam/`](defender-pam/)).
4. **Test** with `practice-questions.md`; aim for ≥80% before moving on.
5. **Drill** `flashcards.csv` (import into Anki — the `#tags` line groups cards by module).
6. **Track** in [`PROGRESS.md`](PROGRESS.md); log every miss in the weak-area table and re-test it first next session.

Keep [`GLOSSARY.md`](GLOSSARY.md) open for acronym lookups. Once you've worked several modules, take the [`MOCK-EXAM.md`](MOCK-EXAM.md) — 50 mixed questions — as a checkpoint, and the full-length [`MOCK-EXAM-FULL.md`](MOCK-EXAM-FULL.md) — 125 questions in 240 minutes — as a timed dress rehearsal before booking. In the final weeks, drill each module's one-page [`facts.md`](modules/), the [`cheatsheets/`](cheatsheets/), and the practice platforms in [`resources/practice-labs.md`](resources/practice-labs.md).

---

### 🐉 Learning the tools (Kali Linux)

Two companions to the modules, depending on where you are:

| Resource | For | Contents |
|---|---|---|
| [`kali/`](kali/) — **beginner→mastery course** | Newcomers | 17 chapters, zero Linux assumed: getting started · Linux · terminal · networking · then every phase (recon → nmap → enumeration → web → Metasploit → passwords → AD → wireless → post-ex → reporting) + troubleshooting |
| [`KALI-TUTORIAL.md`](KALI-TUTORIAL.md) — **one-page reference** | Quick lookups | The whole toolset in one scannable page, grouped by phase, with a tool→module map |

New to the command line? Start the course at [chapter 00](kali/00-getting-started.md). Just need a command? Use the reference.

## The 20 modules (official CEH v13 order)

Each folder contains the **guide** plus its four study companions — `facts.md` · `practice-questions.md` · `flashcards.csv` · `lab-walkthrough.md` (linked from the top of every module README).

| # | Module | Open |
|---|---|---|
| 01 | Introduction to Ethical Hacking | [→](modules/01-introduction-to-ethical-hacking/) |
| 02 | Footprinting and Reconnaissance | [→](modules/02-footprinting-and-reconnaissance/) |
| 03 | Scanning Networks | [→](modules/03-scanning-networks/) |
| 04 | Enumeration | [→](modules/04-enumeration/) |
| 05 | Vulnerability Analysis | [→](modules/05-vulnerability-analysis/) |
| 06 | System Hacking | [→](modules/06-system-hacking/) |
| 07 | Malware Threats | [→](modules/07-malware-threats/) |
| 08 | Sniffing | [→](modules/08-sniffing/) |
| 09 | Social Engineering | [→](modules/09-social-engineering/) |
| 10 | Denial-of-Service | [→](modules/10-denial-of-service/) |
| 11 | Session Hijacking | [→](modules/11-session-hijacking/) |
| 12 | Evading IDS, Firewalls, and Honeypots | [→](modules/12-evading-ids-firewalls-honeypots/) |
| 13 | Hacking Web Servers | [→](modules/13-hacking-web-servers/) |
| 14 | Hacking Web Applications | [→](modules/14-hacking-web-applications/) |
| 15 | SQL Injection | [→](modules/15-sql-injection/) |
| 16 | Hacking Wireless Networks | [→](modules/16-hacking-wireless-networks/) |
| 17 | Hacking Mobile Platforms | [→](modules/17-hacking-mobile-platforms/) |
| 18 | IoT and OT Hacking | [→](modules/18-iot-and-ot-hacking/) |
| 19 | Cloud Computing | [→](modules/19-cloud-computing/) |
| 20 | Cryptography | [→](modules/20-cryptography/) |

---

## The Defender / PAM lens

The retention engine of the repo, centered on **CyberArk** for the PAM-engineering reader. Because so many CEH answers are "what's the *best* control," this doubles as a fast filter: prefer the option that **reduces standing privilege, brokers/records access, rotates the secret, or segments the tier**.

| Doc | What it gives you |
|---|---|
| [attack-to-control-matrix.md](defender-pam/attack-to-control-matrix.md) | Master table: attack → detection → control, grouped by module |
| [pam-playbook.md](defender-pam/pam-playbook.md) | The PAM control set (vault, JIT, tiering, gMSA, LAPS, session brokering) and what each defeats |
| [pam-architecture.md](defender-pam/pam-architecture.md) | CyberArk reference architecture + Zero-Standing-Privilege maturity model |
| [identity-attack-paths.md](defender-pam/identity-attack-paths.md) | Kerberoasting, delegation abuse, DCSync, ADCS ESC1–8, golden/silver tickets, Entra token theft |
| [detection-engineering.md](defender-pam/detection-engineering.md) | Windows event IDs, Sigma rules, KQL/Splunk queries, CyberArk PTA signals |
| [cyberark-attack-mapping.md](defender-pam/cyberark-attack-mapping.md) | CyberArk component ↔ CEH attack it defeats (both lookup directions) |

---

## Exam facts (verify against EC-Council before you book)

The values below are consistent across multiple public sources as of **2026-07-13**, but exam policy changes — always confirm on the official pages linked at the bottom.

### CEH (Knowledge) exam — the multiple-choice test

| Item | Value |
|---|---|
| Exam code | **312-50** (v13 → 312-50v13) |
| Questions | **125** multiple choice |
| Duration | **4 hours** (240 minutes) |
| Passing score | **Variable cut score, ~60–85%** depending on the difficulty of your question form |
| Delivery | Pearson VUE or ECC Exam Center (VUE Testing) |
| Courseware | **20 modules**, launched **23 September 2024**, Exam Blueprint **v5.0** |

### CEH (Practical) exam — the hands-on test (separate, optional, earns "CEH Master")

| Item | Value |
|---|---|
| Format | Hands-on challenges in EC-Council's iLabs / Cyber Range |
| Challenges | **20** real-world challenges |
| Duration | **6 hours** |
| Result | Passing both the Knowledge exam and the Practical earns the **CEH Master** designation |

> **Prepping the Practical?** The [`practical/`](practical/) section has a skills checklist, challenge playbooks (question→recipe), and timed lab drills for the hands-on exam.

> ⚠️ **Blueprint domains vs. modules.** EC-Council groups the 20 modules into a smaller set of scored *domains* in Blueprint v5.0. Public sources report the exact per-domain percentages **inconsistently**, so this repo does **not** print made-up weights. Download the official blueprint PDF and record the real weights in [`EXAM-LOGISTICS.md`](EXAM-LOGISTICS.md) yourself.

---

## Repository map

```mermaid
flowchart TD
    CEH["CEH/"]
    README["README.md — you are here"]
    ROADMAP["ROADMAP.md — beginner→master ladder"]
    STRATEGY["EXAM-STRATEGY.md — study system + test-day tactics"]
    MOCK["MOCK-EXAM.md — 50-question checkpoint"]
    MOCKFULL["MOCK-EXAM-FULL.md — 125-question full-length exam"]
    RAPIDFIRE["RAPID-FIRE.md — 200-question drill bank (20 sets of 10)"]
    AICEH["AI-IN-ETHICAL-HACKING.md — AI-driven hacking (v13)"]
    COVERAGE["BLUEPRINT-COVERAGE.md — subtopic coverage matrix"]
    KALI["KALI-TUTORIAL.md — one-page Kali reference"]
    KALICOURSE["kali/ — beginner→mastery Kali course (17 chapters)"]
    AIWF["AI-STUDY-WORKFLOW.md — AI-tutor study system"]
    GLOSSARY["GLOSSARY.md — acronym / term index"]
    STUDY["STUDY-PLAN.md — 12-week plan"]
    EXAM["EXAM-LOGISTICS.md — eligibility, cost, scheduling, ECE"]
    PROGRESS["PROGRESS.md — personal tracker"]
    MODULES["modules/ — 20 module folders"]
    MODFILE["each: README + facts + practice-questions + flashcards + lab-walkthrough"]
    DEFENDER["defender-pam/ — matrix, playbook, CyberArk architecture, identity paths, detection"]
    LABS["labs/ — Docker + Vagrant + Ansible AD/PAM lab"]
    PRACTICAL["practical/ — CEH Practical (hands-on) prep"]
    CHEATSHEETS["cheatsheets/ — ports, nmap, metasploit, hashcat, one-liners"]
    RESOURCES["resources/ — official links, tools, practice platforms"]
    CEH --> README
    CEH --> ROADMAP
    CEH --> STRATEGY
    CEH --> MOCK
    CEH --> MOCKFULL
    CEH --> RAPIDFIRE
    CEH --> AICEH
    CEH --> COVERAGE
    CEH --> KALI
    CEH --> KALICOURSE
    CEH --> AIWF
    CEH --> GLOSSARY
    CEH --> STUDY
    CEH --> EXAM
    CEH --> PROGRESS
    CEH --> MODULES
    MODULES --> MODFILE
    CEH --> DEFENDER
    CEH --> LABS
    CEH --> PRACTICAL
    CEH --> CHEATSHEETS
    CEH --> RESOURCES
```

---

### Everything here (clickable index)

**Orient:** [Roadmap (beginner→master)](ROADMAP.md) · [Blue-team lab (detect the attacks)](labs/blue-team-lab.md)

**Study the theory:** [Modules 01–20](modules/) · [Study plan (12 weeks)](STUDY-PLAN.md) · [Exam strategy](EXAM-STRATEGY.md) · [Glossary](GLOSSARY.md) · [Blueprint coverage](BLUEPRINT-COVERAGE.md) · [Progress tracker](PROGRESS.md) · [Exam logistics](EXAM-LOGISTICS.md)

**Learn the tools & do labs:** [Kali course (beginner→mastery)](kali/) · [Kali one-page reference](KALI-TUTORIAL.md) · [Lab environment](labs/) · [Capstone chain](labs/capstone.md) · [Cheatsheets](cheatsheets/)

**Pass the exams:** [Mock exam — 50 Q](MOCK-EXAM.md) · [Full mock — 125 Q](MOCK-EXAM-FULL.md) · [Rapid-fire bank — 200 Q](RAPID-FIRE.md) · [CEH Practical prep](practical/) · [Challenge generator](practical/challenge-lab/) · [Drill packs](practical/drills/) · [Simulated exams](practical/exams/)

**Go deeper:** [Defender / PAM (CyberArk)](defender-pam/) · [Identity attack paths](defender-pam/identity-attack-paths.md) · [Detection engineering](defender-pam/detection-engineering.md) · [AI-driven hacking](AI-IN-ETHICAL-HACKING.md) · [AI study workflow](AI-STUDY-WORKFLOW.md) · [Deep references](resources/deep-references.md) · [Resources](resources/)

---

## Official EC-Council references

- CEH program home — https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/
- CEH v13 brochure / syllabus PDF — https://www.eccouncil.org/cehv13-brochure/
- CEH learning framework — https://www.eccouncil.org/cybersecurity-exchange/ethical-hacking/ceh-learning-framework/
- EC-Council Continuing Education (ECE) policy — https://cert.eccouncil.org/ece-policy.html
- Exam via Pearson VUE — https://home.pearsonvue.com/eccouncil

> Anything about weights, eligibility, cost, or policy that you cannot confirm on the links above should be treated as **unverified** and not relied on for booking decisions.
