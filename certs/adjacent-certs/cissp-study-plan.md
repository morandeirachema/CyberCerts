# CISSP study plan and tracker

A domain-by-domain plan for the ISC2 CISSP, built on the repo-wide
[preparation method](../../learning/how-to-prepare-a-cert.md) and the facts on the
[CISSP overview](cissp.md). The exam is CAT (100–150 items, up to 3 hours, 700/1000 scaled
per the overview; *verify on isc2.org*), answered from the **risk manager's** viewpoint.
This repo has no CISSP domain pages, so the plan points at the official outline for the
content and at the repo for the parts it already teaches (identity, PAM, protocols,
compliance).

> Weeks and hours are this repo's suggestion for a working professional at roughly 8–10
> hours a week, not an ISC2 requirement. ISC2 publishes the domain weights in the official exam
> outline (effective 2024-04-15): D1 16%, D2 10%, D3 13%, D4 13%, D5 13%, D6 12%, D7 13%,
> D8 10%. Re-check them there before you start and record them in the tracker below.

## Before Week 1

- [ ] **Route decided:** the five-year experience requirement (two domains), the one-year
  waiver, or the Associate of ISC2 route ([overview](cissp.md#prerequisites--experience)).
- [ ] **Official exam outline** downloaded from isc2.org; domain weights written into the
  tracker; every sub-topic self-scored 0–3.
- [ ] **Mindset note** pinned to the desk: *think like the risk manager, not the engineer;
  people and process before technology; the best answer protects the organisation, not
  the system.*
- [ ] Target exam date `__________`.

## The schedule

| Week | Domain | Repo material that already covers part of it | Milestone — you can… |
|------|--------|-----------------------------------------------|----------------------|
| **1–2** | 1 · Security and Risk Management | [compliance & standards](../../reference/compliance-and-standards.md) (NIS2, ISO 27001, IEC 62443, DORA, PCI DSS) · [PAM vs IAM / IGA](../../foundations/pam-iam-iga-idaas-epm.md) · [legal & ethics](../ceh/00-overview/legal-and-ethics.md) | run a qualitative risk assessment on paper; explain due care vs due diligence; map one regulation to controls |
| **3** | 2 · Asset Security | [privileged accounts & credentials](../../foundations/privileged-accounts-and-credentials.md) (classification of accounts and secrets) | classify data and assets, state handling requirements per class, and the retention / destruction rules |
| **4–5** | 3 · Security Architecture and Engineering | [cryptography & PKI](../../prerequisites/cryptography-and-pki.md) · [TLS](../../protocols/tls.md) · [least privilege / JIT / Zero Trust](../../foundations/core-concepts-least-privilege-jit-zero-trust.md) · [PAM reference architecture](../ceh/defender-pam/pam-architecture.md) | explain security models and secure design principles; choose a cryptographic primitive per requirement; explain a PKI end to end |
| **6** | 4 · Communication and Network Security | [networking & protocols](../../prerequisites/networking-and-protocols.md) · [SSH](../../protocols/ssh.md) · [RADIUS](../../protocols/radius.md) · [CEH sniffing](../ceh/domains/08-sniffing.md) and [evasion](../ceh/domains/12-evading-ids-firewalls-honeypots.md) | design a segmented network with the right control at each boundary; explain secure protocol choices |
| **7** | 5 · Identity and Access Management | [what is PAM](../../foundations/what-is-pam.md) · [Kerberos](../../protocols/kerberos.md) · [SAML](../../protocols/saml.md) · [OIDC](../../protocols/oidc-oauth2.md) · [Windows & AD](../../prerequisites/windows-and-active-directory.md) · [PAM playbook](../ceh/defender-pam/pam-playbook.md) | explain identification, authentication, authorisation and accountability; federation vs SSO; the access-control models; the privileged-access lifecycle |
| **8** | 6 · Security Assessment and Testing | [engagement methodology & reporting](../ceh/00-overview/engagement-methodology-and-reporting.md) · [CEH vulnerability analysis](../ceh/domains/05-vulnerability-analysis.md) · [PenTest+ engagement management](../pentest-plus/domains/01-engagement-management.md) | design an assessment programme: what to test, how often, by whom; read a test report as the manager |
| **9** | 7 · Security Operations | [CySA+ hub](../cysa-plus/README.md) (operations, incident response) · [detection engineering](../ceh/defender-pam/detection-engineering.md) · [Linux logging](../../prerequisites/linux-essentials-for-pam.md) | run an incident from detection to lessons learned; explain BCP / DR concepts; state logging and monitoring requirements |
| **10** | 8 · Software Development Security | [CEH web application](../ceh/domains/14-hacking-web-applications.md) and [SQL injection](../ceh/domains/15-sql-injection.md) pages (the attacks the controls prevent) | place security in each SDLC phase; explain secure coding controls and software acquisition risk |
| **11–12** | Review and mocks | the whole tracker; the weak-area log | pass the readiness gate |

Each week: read the outline's sub-topics for the domain, study them from your chosen
official or reputable guide, then close the book and answer a practice set for that domain,
log every miss, and drill the log with spacing. Answer every practice item **as the risk
manager** and note when your engineer's instinct chose differently.

## Readiness gate (repo rule, not ISC2's)

- [ ] Every domain ≥ 80% on a second, spaced practice set.
- [ ] A timed, full-length practice test ≥ 85%, answered at CAT pace (do not linger; CAT
  does not allow going back).
- [ ] You can explain, for any control, the *why* in risk terms and the *who* in governance
  terms.
- [ ] No open weak-area row older than a week.

## Tracker

| # | Domain | Weight (from the outline) | Self-score before | Read | Practice 1 | Practice 2 (spaced) |
|---|--------|:-------------------------:|:-----------------:|:----:|:----------:|:-------------------:|
| 1 | Security and Risk Management | ____ | __ | ☐ | ____% | ____% |
| 2 | Asset Security | ____ | __ | ☐ | ____% | ____% |
| 3 | Security Architecture and Engineering | ____ | __ | ☐ | ____% | ____% |
| 4 | Communication and Network Security | ____ | __ | ☐ | ____% | ____% |
| 5 | Identity and Access Management | ____ | __ | ☐ | ____% | ____% |
| 6 | Security Assessment and Testing | ____ | __ | ☐ | ____% | ____% |
| 7 | Security Operations | ____ | __ | ☐ | ____% | ____% |
| 8 | Software Development Security | ____ | __ | ☐ | ____% | ____% |

- [ ] Route confirmed · outline downloaded · exam date `__________`
- [ ] Full-length timed practice: ____% · exam booked `__________` · passed `__________`
- [ ] Endorsement submitted · CPE and annual maintenance fee deadlines calendared

## Sources

- ISC2 CISSP page: https://www.isc2.org/certifications/cissp
- ISC2 CISSP Certification Exam Outline (domains and current weights):
  https://www.isc2.org/certifications/cissp/cissp-certification-exam-outline
- ISC2 CISSP Experience Requirements:
  https://www.isc2.org/certifications/cissp/cissp-experience-requirements
- Exam format facts: this repo's [CISSP overview](cissp.md), which cites isc2.org; the
  week counts and thresholds are this repo's own suggestion, *not specified in sources*.
