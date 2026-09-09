# Cloud security study plan and tracker

A hands-on plan for the cloud-security milestone, built on the repo-wide
[preparation method](../../learning/how-to-prepare-a-cert.md) and the facts on the
[cloud security overview](cloud-security.md). It is organised by **capability areas**, not by
a vendor's domain list, because the exam guides are the source of truth for domains and
weights and they change: AZ-500 retired on 2026-08-31 with SC-500 as its successor, and AWS
moved from SCS-C02 to SCS-C03 (*verify both on the provider pages*). Record the current
domains and weights from the guide you download in the tracker below.

> The provider study guides list the exact skills measured. Pull the current one first:
> [SC-500 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-500) ·
> [AWS SCS-C03 exam guide](https://docs.aws.amazon.com/aws-certification/latest/examguides/security-specialty-03.html).
> Weeks and hours are this repo's suggestion, not a provider requirement.

## Before Week 1

- [ ] **Platform chosen** for the estate you actually run: Azure (SC-500) or AWS (Security
  Specialty); CCSP / CCSK only if the goal is vendor-neutral breadth.
- [ ] **Official exam guide** downloaded; domains and weights written into the tracker;
  every skill self-scored 0–3.
- [ ] **A cloud account you own**, on the free tier, with billing alerts set. Everything
  below is done in it. Delete what you build at the end of each week.
- [ ] Target exam date `__________`.

## The schedule

The capability areas below are the ones both the Azure page's *skills assessed* list and the
AWS page's domain examples name (identity and access; networking and infrastructure;
compute, storage and data protection; detection, logging and response; governance). Map
each area to the exact domain in your guide.

| Week | Capability area | Build it yourself (in your own account) | On-prem equivalent in this repo | Milestone — you can… |
|------|-----------------|------------------------------------------|----------------------------------|----------------------|
| **1–2** | **Identity and access** | Roles and role assignments, least-privilege policies, conditional access or IAM conditions, privileged-role activation with approval and expiry, break-glass accounts, workload / managed identities, access reviews | [what is PAM](../../foundations/what-is-pam.md) · [least privilege / JIT / Zero Trust](../../foundations/core-concepts-least-privilege-jit-zero-trust.md) · [OIDC / OAuth 2.0](../../protocols/oidc-oauth2.md) · [SAML](../../protocols/saml.md) | explain why standing privileged roles are the cloud's domain-admin problem and show JIT activation working |
| **3** | **Secrets and keys** | Key vault / secrets manager, key rotation, envelope encryption, who can read which secret and how it is logged | [privileged accounts & credentials](../../foundations/privileged-accounts-and-credentials.md) · [cryptography & PKI](../../prerequisites/cryptography-and-pki.md) | rotate a secret without downtime and prove in the log who read it |
| **4** | **Network and infrastructure** | Virtual networks, security groups / NSGs, private endpoints, bastion or session-based admin access instead of public SSH / RDP, WAF in front of a test app | [networking & protocols](../../prerequisites/networking-and-protocols.md) · [SSH](../../protocols/ssh.md) · [PAM reference architecture](../ceh/defender-pam/pam-architecture.md) | reach an admin shell only through the broker path and show the public path is closed |
| **5** | **Compute, storage and data protection** | Hardened images, patch baselines, storage with encryption and no public access, database with private access and audited admin logins, backup and restore | [Linux essentials](../../prerequisites/linux-essentials-for-pam.md) · [CEH cloud module](../ceh/domains/19-cloud-computing.md) | find and fix a public bucket / container and an over-privileged compute identity |
| **6** | **Detection, logging and response** | Central logging, activity / CloudTrail-style audit, alerts on privileged-role activation and policy changes, the platform's security posture and SIEM services, one incident runbook | [detection engineering](../ceh/defender-pam/detection-engineering.md) · [CySA+ security operations](../cysa-plus/domains/01-security-operations.md) · [blue-team lab](../ceh/labs/blue-team-lab.md) | trigger a privileged action and show the alert, the log line and the response step |
| **7** | **Governance and compliance** | Policy-as-code guardrails, tagging, landing-zone / organisation structure, compliance dashboards, shared-responsibility boundaries per service model | [compliance & standards](../../reference/compliance-and-standards.md) · [PAM vs IAM / IGA](../../foundations/pam-iam-iga-idaas-epm.md) | state the shared-responsibility boundary for IaaS, PaaS and SaaS and enforce one guardrail |
| **8** | Review and mocks | Rebuild the Week 1 and Week 6 exercises from memory | the weak-area log | pass the readiness gate |

Each week: read the guide's skills for the area, build them, then answer the provider's
official practice assessment items for that area (where one exists), log every miss, drill
with spacing. Reading alone does not pass these exams.

## Readiness gate (repo rule, not the provider's)

- [ ] Every domain in your guide ≥ 80% on a second, spaced practice set.
- [ ] A timed full practice assessment ≥ 85%.
- [ ] Every hands-on exercise above rebuilt once from memory.
- [ ] No open weak-area row older than a week.

## Tracker

| Domain (copy from your exam guide) | Weight | Self-score before | Built | Practice 1 | Practice 2 (spaced) |
|------------------------------------|:------:|:-----------------:|:-----:|:----------:|:-------------------:|
| | ____ | __ | ☐ | ____% | ____% |
| | ____ | __ | ☐ | ____% | ____% |
| | ____ | __ | ☐ | ____% | ____% |
| | ____ | __ | ☐ | ____% | ____% |
| | ____ | __ | ☐ | ____% | ____% |
| | ____ | __ | ☐ | ____% | ____% |

- [ ] Platform chosen · guide downloaded · account and billing alerts ready · exam date `__________`
- [ ] Timed full practice: ____% · exam booked `__________` · passed `__________`
- [ ] Renewal rule noted from the provider and calendared

## Sources

- Microsoft SC-500 study guide: https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/sc-500
- Microsoft AZ-500 page, including the retirement notice: https://learn.microsoft.com/en-us/credentials/certifications/azure-security-engineer/
- AWS Certified Security – Specialty: https://aws.amazon.com/certification/certified-security-specialty/
- AWS SCS-C03 exam guide: https://docs.aws.amazon.com/aws-certification/latest/examguides/security-specialty-03.html
- ISC2 CCSP: https://www.isc2.org/certifications/ccsp · Cloud Security Alliance CCSK:
  https://cloudsecurityalliance.org/education/ccsk
- Exam facts: this repo's [cloud security overview](cloud-security.md). Capability areas
  are drawn from the skills lists cited there; the week counts and thresholds are this
  repo's own suggestion, *not specified in sources*.
