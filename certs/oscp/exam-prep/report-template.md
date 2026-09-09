# Penetration-test report template

A copy-and-fill skeleton for the report that hands-on exams grade: the OSCP report (which
must let a reader **reproduce** every compromise, with screenshots and proof flags, and can
fail an otherwise-passing attempt), the PNPT report (executive summary, technical findings
with evidence and severity, remediation per finding, tool disclosure) and any real
engagement. Have it filled in *as you go*, never reconstructed afterwards against the clock.

> The structure follows the five-part report taught in the Kali course's
> [notes & reporting](../../ceh/kali/15-notes-and-reporting.md) chapter and the reporting
> guidance in NIST SP 800-115. Check the exam body's current report requirements before you
> sit: [OSCP exam guide](https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide) ·
> [PNPT](https://certifications.tcm-sec.com/pnpt/). Where they specify a format or a section,
> theirs wins.

## How to use it

1. Copy the skeleton below into `report.md` in your engagement folder before the exam starts.
2. Fill **Scope** and **Methodology** immediately; they do not depend on results.
3. Add one **Finding** block per vulnerability the moment you confirm it, evidence first.
4. Write the **Executive summary** last, read it first.
5. Export to the format the exam body requires and check every screenshot is legible and
   every proof value is in plain text as well as in the image.

---

## Skeleton

```markdown
# Penetration Test Report — <client / exam id>

| Item | Value |
|------|-------|
| Tester | <name, candidate id> |
| Engagement dates | <start> to <end> (time zone) |
| Report date | <date> |
| Version | 1.0 |
| Classification | Confidential |

## 1. Executive summary

<Three to six sentences, no tool names: what was tested, the overall risk level, the most
important finding in business terms, and the single most valuable remediation.>

| Severity | Count |
|----------|-------|
| Critical | |
| High | |
| Medium | |
| Low | |
| Informational | |

## 2. Scope and rules of engagement

- **In scope:** <IP ranges, hostnames, URLs, domains, the AD set>
- **Out of scope:** <anything excluded>
- **Authorisation:** <who authorised, reference to the exam or contract>
- **Constraints:** <testing window, forbidden techniques such as denial of service,
  proctoring conditions>
- **Tools permitted / restricted:** <as stated by the exam body>

## 3. Methodology

<The phases followed, in order: information gathering → enumeration → vulnerability
identification → exploitation → post-exploitation and privilege escalation → lateral
movement → reporting. State the standard you aligned to (for example NIST SP 800-115).>

## 4. Attack narrative (per host or per chain)

### 4.1 <hostname / IP>

1. **Enumeration** — what was discovered (ports, services, versions), with the command and
   the relevant output excerpt.
2. **Vulnerability** — what it is and why it is exploitable here.
3. **Exploitation** — the steps taken, in order, so a reader can repeat them; screenshots
   of each decisive step.
4. **Post-exploitation / privilege escalation** — how initial access became full control.
5. **Proof** — `local.txt` / `proof.txt` (or the exam's equivalent) as plain text and as a
   screenshot showing the value together with the host's identity (for example an IP or
   hostname in the same frame).

### 4.2 <next host, or the AD chain: foothold → lateral movement → domain compromise>

## 5. Findings (highest severity first)

### F-01 <title>

| Field | Value |
|-------|-------|
| Severity | Critical / High / Medium / Low / Info |
| CVSS | <vector and score, if used> |
| Affected asset(s) | <host, service, URL> |
| Category | <for example: default credentials, unpatched service, misconfiguration> |

- **Description** — what the weakness is.
- **Evidence** — the excerpt or screenshot that proves it (reference the narrative step).
- **Impact** — what an attacker gains, in business terms as well as technical.
- **Remediation** — the specific fix, plus the compensating control if the fix is slow.
- **References** — vendor advisory, CVE, standard.

### F-02 <title>

## 6. Remediation summary

| Finding | Severity | Remediation | Owner | Priority |
|---------|----------|-------------|-------|----------|
| F-01 | | | | |

## 7. Tool disclosure

| Tool | Purpose | Where used |
|------|---------|-----------|
| | | |

## 8. Appendix

- A. Full scan output files (`nmap -oA` sets, scanner exports)
- B. Additional screenshots
- C. Cleanup performed (accounts, files, services created during testing and their removal)
- D. Glossary for the non-technical reader
```

---

## Checklist before you submit

- [ ] Every compromised host has enumeration → vulnerability → exploitation → proof, in order.
- [ ] Every proof value appears both as text and in a screenshot with the host identity visible.
- [ ] Findings are ordered by severity; each has evidence, impact and a specific remediation.
- [ ] The executive summary contains no tool names and fits on one page.
- [ ] Scope matches the authorisation exactly; nothing outside it is mentioned as tested.
- [ ] Tool disclosure and cleanup sections are complete.
- [ ] The file is in the required format, under any size limit, and named as instructed.

## Where it is used

- [OSCP study plan](study-plan.md) and [exam structure](../00-overview/exam-structure.md).
- [PNPT study plan](../../pnpt/exam-prep/study-plan.md), the
  [reporting & debrief](../../pnpt/topics/05-reporting-and-the-debrief.md) page and the
  [debrief outline](../../pnpt/exam-prep/debrief-outline.md).
- The six-part finding format and the engagement folder layout:
  [Kali chapter 15](../../ceh/kali/15-notes-and-reporting.md); the wider method:
  [engagement methodology & reporting](../../ceh/00-overview/engagement-methodology-and-reporting.md).

## Sources

- OffSec — OSCP+ Exam Guide (report requirements, proof files, separate report window):
  https://help.offsec.com/hc/en-us/articles/360040165632-OSCP-Exam-Guide
- TCM Security — PNPT certification page (2-day report, debrief, tool disclosure):
  https://certifications.tcm-sec.com/pnpt/
- NIST SP 800-115, *Technical Guide to Information Security Testing and Assessment*
  (reporting and evidence handling): https://csrc.nist.gov/pubs/sp/800/115/final
- Section structure: this repo's [Kali chapter 15](../../ceh/kali/15-notes-and-reporting.md).
