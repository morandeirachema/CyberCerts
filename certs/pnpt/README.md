<div align="center">

# 🟣 PNPT — Study Hub

### A step-by-step preparation guide for the **TCM Security PNPT**

*Engagement workflow, real diagrams, and exam prep* — a **fully practical** network
penetration test: OSINT → external → Active Directory → report → a **live debrief**.

![Provider](https://img.shields.io/badge/provider-TCM%20Security-red)
![Exam](https://img.shields.io/badge/exam-5--day%20%2B%20report%20%2B%20debrief-1f6feb)
![Style](https://img.shields.io/badge/style-no%20flags%20·%20no%20MCQ-blue)
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
> **Unofficial & no fabrication.** Not affiliated with or endorsed by TCM Security. Exam
> specifics are from TCM's official PNPT page; volatile items (price, exact structure, voucher
> terms) should be re-checked there. Compiled **2026-06-21**.

## 📋 At a glance

| Item | Detail |
|------|--------|
| **Provider** | TCM Security · vendor-neutral |
| **Exam** | **5-day** practical assessment + **2-day** report + a **live 15-minute debrief** |
| **Style** | Fully practical — **no multiple choice, no capture-the-flag flags** |
| **Signature** | The **live debrief**: present & defend your methodology like a consultant |
| **Included** | 1 attempt **+ 1 free retake**, bundled training; non-expiring *(verify on TCM)* |

Full details: **[exam structure](00-overview/exam-structure.md)**.

## 🛠️ Prepare for it — the procedure

This hub is a **preparation guide** for an engagement-style exam: five days of assessment, a
professional report, and a live debrief. The method is the repo-wide
[how to prepare a certification](../../learning/how-to-prepare-a-cert.md); the readiness rule below is this repo's, not
TCM Security's.

1. **Commit** — read [exam structure](00-overview/exam-structure.md) and confirm the current
   bundle, retake and validity terms on [TCM's page](https://certifications.tcm-sec.com/pnpt/).
   Set a date once the AD lab is built and the full workflow has been practised at least once.
2. **Check the entry level** — the plan's prerequisites section and its "PJPT / fundamentals
   first" advice; you need the [CEH](../ceh/README.md) breadth, working Linux CLI skills and
   AD basics ([Windows & AD](../../prerequisites/windows-and-active-directory.md)).
3. **Build the AD lab** — the plan's lab section; the repo's own
   [Ansible AD lab](../ceh/labs/README.md) with its tiered-admin model is a ready target.
4. **Follow the [study plan](exam-prep/study-plan.md)** through the five
   [engagement phases](topics/README.md): OSINT → external → AD exploitation → lateral
   movement → reporting. For each: read the page, do it in the lab, write the finding up.
5. **Rehearse the deliverables** — a full report from your lab notes using a professional
   template, and the **15-minute debrief** spoken aloud to someone, twice. The report and
   debrief are graded; the shell is only the evidence.
6. **Pass the readiness gate** — the full workflow (external foothold → domain compromise)
   completed end-to-end in the lab from your own notes; report and debrief rehearsed; no
   open weak-area row.
7. **Exam week and after** — the plan's exam logistics; then note the certificate's terms,
   and return to the [roadmap](../../learning/roadmap.md). The defender's view of every step
   is the [attack → defense matrix](../../attack-to-defense-matrix.md).

### 📈 Track it

| # | Engagement phase | Read | Done in the lab | Written up |
|---|------------------|:----:|:---------------:|:----------:|
| 1 | [OSINT & reconnaissance](topics/01-osint-and-reconnaissance.md) | ☐ | ☐ | ☐ |
| 2 | [External penetration testing](topics/02-external-penetration-testing.md) | ☐ | ☐ | ☐ |
| 3 | [Active Directory exploitation](topics/03-active-directory-exploitation.md) | ☐ | ☐ | ☐ |
| 4 | [Lateral movement & pivoting](topics/04-lateral-movement-and-pivoting.md) | ☐ | ☐ | ☐ |
| 5 | [Reporting & the debrief](topics/05-reporting-and-the-debrief.md) | ☐ | ☐ | ☐ |

- [ ] AD lab built · full workflow end-to-end `__________` · report drafted · debrief rehearsed ×2
- [ ] Exam booked `__________` · passed `__________`

## 📦 What's inside

| Section | Contents |
|---------|----------|
| **[Overview](00-overview/what-is-pnpt.md)** | [What is PNPT](00-overview/what-is-pnpt.md) · [Exam structure](00-overview/exam-structure.md) |
| **[Engagement phases](topics/README.md)** | The PNPT workflow, phase by phase |
| **[Exam prep](exam-prep/study-plan.md)** | [Study plan](exam-prep/study-plan.md) — lab build, workflow practice, the debrief |

### The engagement phases

| # | Phase | Page |
|---|-------|------|
| 1 | OSINT & reconnaissance | [01-osint-and-reconnaissance.md](topics/01-osint-and-reconnaissance.md) |
| 2 | External penetration testing | [02-external-penetration-testing.md](topics/02-external-penetration-testing.md) |
| 3 | Active Directory exploitation | [03-active-directory-exploitation.md](topics/03-active-directory-exploitation.md) |
| 4 | Lateral movement & pivoting | [04-lateral-movement-and-pivoting.md](topics/04-lateral-movement-and-pivoting.md) |
| 5 | Reporting & the debrief | [05-reporting-and-the-debrief.md](topics/05-reporting-and-the-debrief.md) |

## 🧭 Where it fits

The PNPT is the **budget-friendly, engagement-style** practical cert:

- A realistic lead-in or alternative to [OSCP](../oscp/README.md); more report- and
  consultant-focused than the knowledge-based [CEH](../ceh/README.md).
- **Defender's mirror** → its AD-compromise and lateral-movement focus is exactly what the
  [attack → defense matrix](../../attack-to-defense-matrix.md) and [PAM foundations](../../foundations/README.md)
  exist to prevent and audit.

## 🔗 Quick links

- 🎓 [TCM Security PNPT (official)](https://certifications.tcm-sec.com/pnpt/)
- ⚖️ [Legal & ethics](../ceh/00-overview/legal-and-ethics.md) · 🧪 [Engagement phases](topics/README.md)
- 🧰 [Practice platforms](../../learning/platforms.md)

> PNPT, PJPT and TCM Security are trademarks of TCM Security, used here for identification and
> educational purposes only.
