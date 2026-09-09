<div align="center">

# 🔴 OSCP / OSCP+ — Study Hub

### A step-by-step preparation guide for the **OffSec OSCP / OSCP+ (PEN-200)**

*Methodology, skill areas, real diagrams, and exam prep* — the benchmark **hands-on
penetration-testing** certification: you must actually compromise live machines, then report.

![Course](https://img.shields.io/badge/course-PEN--200-red)
![Exam](https://img.shields.io/badge/exam-24h%20hands--on%20%2B%20report-1f6feb)
![Pass](https://img.shields.io/badge/pass-70%2F100-blue)
![Diagrams](https://img.shields.io/badge/diagrams-Mermaid-ff3670)
![Use](https://img.shields.io/badge/use-educational%20%26%20authorized%20only-orange)

</div>

---

> [!WARNING]
> **Educational & authorized use only.** Offensive techniques are explained **conceptually**
> for understanding, methodology, and defense — no weaponized step-by-step playbooks or
> exploit code. Use them only against systems you own or are **explicitly authorized in
> writing** to test. See the CEH hub's [legal & ethics](../ceh/00-overview/legal-and-ethics.md).

> [!NOTE]
> **Unofficial & no fabrication.** Not affiliated with or endorsed by OffSec. Exam specifics
> are from OffSec's PEN-200 page and OSCP+ exam guide; volatile items (price, exact structure,
> CPE/validity) should be re-checked there. Compiled **2026-06-21**.

## 📋 At a glance

| Item | Detail |
|------|--------|
| **Provider / course** | OffSec · PEN-200 (Penetration Testing with Kali Linux) |
| **Exam** | **24-hour** proctored hands-on + **~24-hour** report window |
| **Scoring** | **100 points**, **70 to pass** · AD set (3 machines) = 40 · 3 standalone = 60 · **no bonus** (since 1 Nov 2024) |
| **OSCP vs OSCP+** | OSCP doesn't expire; **OSCP+** (current AD-inclusive exam) expires **3 years**, maintained via CPE *(verify)* |
| **Style** | Fully hands-on — *"Try Harder"* |

Full details: **[exam structure](00-overview/exam-structure.md)**.

## 🛠️ Prepare for it — the procedure

This hub is a **preparation guide** for a fully hands-on exam: there is nothing to memorise
and everything to rehearse. The method is the repo-wide
[how to prepare a certification](../../learning/how-to-prepare-a-cert.md); the readiness rule below is this repo's, not
OffSec's.

1. **Commit** — read [exam structure](00-overview/exam-structure.md) (24-hour exam, 100
   points, 70 to pass, the AD set worth 40) and confirm the current course bundle, lab time
   and retake terms on [OffSec's page](https://www.offsec.com/courses/pen-200/). Set a date
   only after Phase 3 of the plan is under way.
2. **Check the entry level** — you should already hold the [CEH](../ceh/README.md) or
   [PenTest+](../pentest-plus/README.md) breadth and be comfortable on the Linux CLI
   ([prerequisites](../../prerequisites/README.md)). Self-score the six skill areas 0–3.
3. **Follow the [study plan](exam-prep/study-plan.md)** — Phase 1 fundamentals, Phase 2
   privilege escalation and AD, Phase 3 practice machines. For each
   [skill area](topics/README.md): read the page, then do it on a machine in an authorised
   range ([platforms](../../learning/platforms.md), the [CEH lab](../ceh/labs/README.md)),
   and write the finding up as if for the report.
4. **Build the methodology and the notes** — a fixed enumeration checklist per service, a
   note template per machine, screenshots of every `local.txt` / `proof.txt`. The plan's
   note-taking section is the standard.
5. **Pass the readiness gate** — the AD set (three machines) end-to-end without hints inside
   a self-imposed time box; a mixed set of standalone machines at the exam's difficulty
   solved from your own notes; a full report written from those notes; one dress rehearsal
   of the full 24-hour window with sleep scheduled in.
6. **Exam week** — proctoring set-up test, ID, report template ready, machine list and
   time budget written down; the plan's exam-day logistics and tips.
7. **After** — submit the report inside the window; note the OSCP+ renewal rule from
   OffSec; go back to the [roadmap](../../learning/roadmap.md). The defender's mirror of
   everything you just did is the [attack → defense matrix](../../attack-to-defense-matrix.md).

### 📈 Track it

| # | Skill area | Read | Machines done | Written up | Cold, under time |
|---|-----------|:----:|:-------------:|:----------:|:----------------:|
| 1 | [Enumeration & information gathering](topics/01-enumeration-and-information-gathering.md) | ☐ | ____ | ☐ | ☐ |
| 2 | [Web application attacks](topics/02-web-application-attacks.md) | ☐ | ____ | ☐ | ☐ |
| 3 | [Password & client-side attacks](topics/03-password-and-client-side-attacks.md) | ☐ | ____ | ☐ | ☐ |
| 4 | [Privilege escalation](topics/04-privilege-escalation.md) | ☐ | ____ | ☐ | ☐ |
| 5 | [Active Directory attacks](topics/05-active-directory-attacks.md) | ☐ | ____ | ☐ | ☐ |
| 6 | [Pivoting & tunneling](topics/06-pivoting-and-tunneling.md) | ☐ | ____ | ☐ | ☐ |

- [ ] Note template and enumeration checklist written · AD set solved end-to-end `__________`
- [ ] 24-hour dress rehearsal done · report drafted · exam booked `__________` · passed `__________`

## 📦 What's inside

| Section | Contents |
|---------|----------|
| **[Overview](00-overview/what-is-oscp.md)** | [What is OSCP](00-overview/what-is-oscp.md) · [Exam structure](00-overview/exam-structure.md) |
| **[Skill areas](topics/README.md)** | The PEN-200 practical skills (not official "domains") |
| **[Exam prep](exam-prep/study-plan.md)** | [Study plan](exam-prep/study-plan.md) — methodology, practice, the report |

### The skill areas

| # | Skill | Page |
|---|-------|------|
| 1 | Enumeration & information gathering | [01-enumeration-and-information-gathering.md](topics/01-enumeration-and-information-gathering.md) |
| 2 | Web application attacks | [02-web-application-attacks.md](topics/02-web-application-attacks.md) |
| 3 | Password & client-side attacks | [03-password-and-client-side-attacks.md](topics/03-password-and-client-side-attacks.md) |
| 4 | Privilege escalation (Linux & Windows) | [04-privilege-escalation.md](topics/04-privilege-escalation.md) |
| 5 | Active Directory attacks | [05-active-directory-attacks.md](topics/05-active-directory-attacks.md) |
| 6 | Pivoting & tunneling | [06-pivoting-and-tunneling.md](topics/06-pivoting-and-tunneling.md) |

## 🧭 Where it fits

OSCP is the **hands-on depth** milestone on the offensive track:

- **After** the breadth of [CEH](../ceh/README.md) / [PenTest+](../pentest-plus/README.md) and
  often the practical [PNPT](../pnpt/README.md).
- **Defender's mirror** → the AD-attack and privilege-escalation focus is exactly what the
  [attack → defense matrix](../../attack-to-defense-matrix.md) and [PAM foundations](../../foundations/README.md)
  defend against — strong attacker context for PAM practitioners.

## 🔗 Quick links

- 🎓 [OffSec PEN-200 / OSCP (official)](https://www.offsec.com/courses/pen-200/)
- ⚖️ [Legal & ethics](../ceh/00-overview/legal-and-ethics.md) · 🧪 [Skill areas](topics/README.md)
- 🧰 [Practice platforms](../../learning/platforms.md)

> OSCP, OSCP+, OffSec and PEN-200 are trademarks of OffSec, used here for identification and
> educational purposes only.
