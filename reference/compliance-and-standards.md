# Compliance & Standards — How PAM Maps to the Frameworks

Privileged Access Management does not satisfy any framework on its own, but it directly
**supports** a recurring set of expectations that nearly every security regulation and
standard imposes: **control who has privileged access, enforce least privilege, require
strong authentication, and produce a tamper-resistant audit trail of privileged
activity**. This page maps the major frameworks to those expectations and shows how PAM
helps address them.

> **No-overstatement note (read first):** Most of these frameworks describe *outcomes* and
> *controls* (e.g. "limit and monitor privileged access"), not named products or vendors.
> Where a clause clearly requires something, this page says so; where it is an enabling
> control rather than an explicit mandate, the wording is "**supports / helps address**".
> Always confirm specific clause obligations against the official text for your scope.

For acronym expansions see [acronyms.md](acronyms.md); for the concepts (least privilege,
SoD, non-repudiation, JIT) see
[core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

---

## How PAM connects to compliance (the common thread)

Almost every framework below expects, in some form:

1. **Identify & restrict privileged access** — least privilege, remove standing/shared
   admin rights → PAM brokers access and removes the need to know target passwords.
2. **Strong authentication** for privileged/remote access → PAM gateway requires MFA.
3. **Accountability & traceability** — attribute actions to a named individual, log and
   retain evidence → PAM session recording + per-user attribution = non-repudiation.
4. **Credential protection** — protect, rotate and avoid hard-coding secrets → PAM vaulting
   and rotation; AAPM for application secrets.
5. **Monitoring & review** — detect anomalies, review who has access → PAM real-time
   monitoring, SIEM forwarding, and governance (IAG) access reviews.

---

## Framework-by-framework mapping

| Framework | Scope / Region | Relevant privileged-access expectation | How PAM helps |
|---|---|---|---|
| **NIS2** (Directive (EU) 2022/2555) | EU; essential & important entities (broad sectors) | Risk-management measures incl. access control, MFA, incident handling, and accountability of management; strong emphasis on traceability and securing administrative/remote access. | PAM enforces least privilege & JIT, requires MFA, records & audits all privileged sessions, and feeds SIEM for incident detection. |
| **ISO/IEC 27001** (+ 27002 controls) | International; any organisation (ISMS) | Access control & privileged-access management are explicit themes (27002:2022 controls incl. **8.2 privileged access rights**, **5.15 access control**, **8.15 logging**, **8.5 secure authentication**). Certification requires managing and reviewing them. | PAM operationalises privileged-access-rights restriction, secure authentication (MFA), logging of privileged activity, and supports access reviews via IGA/IAG. |
| **ISA/IEC 62443** | International; OT / ICS (industrial) | Zones & conduits, identification & authentication control (FR1), use control (FR2), and least-privilege/role-based access for OT; control and audit of remote & maintenance access. | Agentless PAM brokers and records OT access (incl. third-party maintenance), enforces least privilege/JIT, and segments at the IT/OT boundary. See [PAM for OT](../certs/ceh/ot-security/05-pam-for-ot.md). |
| **DORA** (Regulation (EU) 2022/2554) | EU; financial entities & their ICT providers | ICT risk management incl. strong access control, least privilege, segregation of duties, logging, and oversight of third-party/ICT-provider access. | PAM controls & records privileged and third-party access, enforces least privilege & SoD, and provides the audit trail; IGA/IAG adds access certification. |
| **GDPR** (Regulation (EU) 2016/679) | EU; processors/controllers of personal data | Art. 32 "appropriate technical & organisational measures" — confidentiality, integrity, access control over personal data; accountability (Art. 5) and breach handling. *(PAM is an enabling control, not a named GDPR requirement.)* | PAM restricts and records who can access systems holding personal data, vaults credentials, and provides accountability evidence — **supporting** Art. 32 security-of-processing. |
| **PCI DSS** (v4.0.1) | Global; entities handling payment-card data | Restrict access by business need-to-know & least privilege (Req. 7), unique IDs & strong auth incl. **MFA** (Req. 8), and log/monitor all access (Req. 10) — explicit on privileged users. | PAM gives each admin a unique identity, enforces MFA & least privilege to the cardholder environment, and records/forwards privileged-session logs for Req. 10. |
| **SOX** (Sarbanes-Oxley Act, 2002) | USA; public companies' financial reporting | Internal controls over financial reporting (Sec. 404) — access controls, segregation of duties, and audit trails over financial systems are core to the IT general controls auditors test. | PAM enforces SoD/approval workflows, restricts & records privileged access to financial systems, and produces the audit trail; IAG supports access recertification. *(SOX names no specific technology.)* |
| **NIST CSF** (2.0) | International (US-origin); voluntary framework | Outcomes across **Govern, Identify, Protect, Detect, Respond, Recover** — Protect includes identity management, authentication & access control (PR.AA) and least privilege. | PAM delivers Protect (identity/authN/access control, least privilege) and feeds Detect (monitoring/logging) and Respond (session termination, forensic recordings). |
| **NIST SP 800-53** (Rev. 5) | USA; federal systems (and widely adopted) | Control families incl. **AC-2** account mgmt, **AC-3** access enforcement, **AC-5** SoD, **AC-6** least privilege, **AU** audit & accountability, **IA** identification & authentication. | PAM directly implements AC-5/AC-6 (SoD, least privilege), AC-2 (privileged account mgmt), AU (session audit) and IA (MFA at the gateway). |
| **NIST SP 800-82** (Rev. 3) | USA; OT / ICS security guidance | Guidance for securing ICS/OT incl. access control, remote access, and least privilege adapted to operational constraints. | Agentless OT PAM secures remote/maintenance access without agents on PLCs. |
| **NIST SP 800-171** (Rev. 3) | USA; CUI in non-federal systems (e.g. defense supply chain) | Protecting Controlled Unclassified Information via access control, least privilege, MFA and audit/accountability requirements. | PAM enforces least privilege & MFA and records privileged activity over systems holding CUI, supporting the AC/AU/IA requirement families. |
| **HIPAA** (Security Rule) | USA; healthcare (covered entities & business associates) | Safeguards for electronic PHI incl. access control (unique user ID, emergency access, automatic logoff), audit controls, and authentication. | PAM provides unique privileged IDs, **break-glass** emergency access, session timeout/termination, audit controls (recording/logging) and strong authentication over systems holding ePHI. |
| **NERC CIP** | North America; bulk electric system (power utilities) | Mandatory controls incl. electronic access control & monitoring (CIP-005), system security & logging (CIP-007), and management of interactive remote access (incl. intermediate systems & encryption/MFA). | PAM acts as the intermediate system for interactive remote access, enforces MFA/encryption, and records & monitors privileged sessions to BES cyber systems. |

> **Cross-checks before citing a mandate:** PCI DSS Req. 7/8/10 and NERC CIP-005/007 *do*
> explicitly address privileged access, MFA and logging. NIS2, ISO 27001 and 62443 require
> the *outcomes* (least privilege, authentication, traceability) without naming PAM
> products. GDPR, SOX and HIPAA treat PAM as an **enabling** control supporting broader
> obligations, not as a named requirement. Verify the precise clause for your scope.

---

## Product & vendor security certifications (context)

Distinct from the customer compliance frameworks above, **PAM products and vendors may
themselves hold security certifications**. Procurement teams — especially in the EU
public sector and critical infrastructure — often use these as a shortlist gate, so it
helps to recognise them.

| Certification | Body / Region | What it is |
|---|---|---|
| **ANSSI CSPN** (Certification de Sécurité de Premier Niveau) | ANSSI, France | France's *first-level* security certification — a time-boxed evaluation of a product against a defined security target. |
| **BSI BSZ** (Beschleunigte Sicherheitszertifizierung) | BSI, Germany | Germany's *accelerated* security certification, conceptually comparable to CSPN; mutually recognised with CSPN under a Franco-German agreement since late 2025. |
| **ISO/IEC 27001:2022** | Accredited certification body (international) | Certifies the vendor's own **ISMS** (organisational security management), not a specific product feature. Most PAM vendors hold it. |
| **Common Criteria / EAL** | International (ISO/IEC 15408) | Internationally-recognised product security evaluation with assurance levels EAL1–7. |
| **FIPS 140-2/3** | NIST, USA | Validation of cryptographic modules; commonly cited by US-centric vendors. |

> **Reading a vendor's claims:** always check *which product and version* the
> certification covers, and whether it is a product evaluation (CSPN, BSZ, CC) or a
> company-level management certification (ISO 27001). Marketing labels such as
> "Cybersecurity Made in Europe" are **positioning**, not certifications. For example,
> WALLIX holds ANSSI CSPN and BSI BSZ on its PAM product, while no Common Criteria EAL
> level for it is confirmed in public sources. See the
> [PAM market landscape](../foundations/pam-market-landscape.md) for how this plays into
> vendor differentiation.

---

## See also

- [Acronyms](acronyms.md) — every framework and body expanded.
- [Glossary](glossary.md) — least privilege, SoD, non-repudiation, break-glass, etc.
- [Core concepts: least privilege, JIT, Zero Trust](../foundations/core-concepts-least-privilege-jit-zero-trust.md)
- [PAM threat landscape](../foundations/pam-threat-landscape.md)
- [PAM market landscape](../foundations/pam-market-landscape.md)
- [PAM for OT](../certs/ceh/ot-security/05-pam-for-ot.md)

---

## Sources

- **NIS2** Directive (EU) 2022/2555 (official text): https://eur-lex.europa.eu/eli/dir/2022/2555/oj · ENISA NIS2 resources: https://www.enisa.europa.eu/topics/nis-directive
- **ISO/IEC 27001:2022**: https://www.iso.org/standard/27001 · ISO/IEC 27002:2022 controls: https://www.iso.org/standard/75652.html
- **ISA/IEC 62443** series (ISA overview): https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards
- **DORA** Regulation (EU) 2022/2554 (official text): https://eur-lex.europa.eu/eli/reg/2022/2554/oj
- **GDPR** Regulation (EU) 2016/679, Art. 32: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- **PCI DSS** v4.0.1 (PCI Security Standards Council): https://www.pcisecuritystandards.org/document_library/
- **SOX** — Sarbanes-Oxley Act of 2002 (Sec. 404): https://www.govinfo.gov/app/details/PLAW-107publ204
- **NIST Cybersecurity Framework 2.0**: https://www.nist.gov/cyberframework
- **NIST SP 800-53 Rev. 5** (AC/AU/IA families): https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- **NIST SP 800-82 Rev. 3** (OT security): https://csrc.nist.gov/pubs/sp/800/82/r3/final
- **NIST SP 800-171 Rev. 3** (protecting CUI): https://csrc.nist.gov/pubs/sp/800/171/r3/final
- **HIPAA Security Rule** (HHS): https://www.hhs.gov/hipaa/for-professionals/security/index.html
- **NERC CIP** standards (CIP-005, CIP-007): https://www.nerc.com/pa/Stand/Pages/CIPStandards.aspx
- **FIPS 140-3** (NIST CMVP): https://csrc.nist.gov/projects/cryptographic-module-validation-program
- **ANSSI CSPN**: https://cyber.gouv.fr/la-certification-de-securite-de-premier-niveau-cspn · WALLIX CSPN announcement: https://www.wallix.com/news/wallix-bastion-honored-again-cspn-certification
- **BSI BSZ**: https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Zertifizierung-und-Anerkennung/ · WALLIX dual-certification PR: https://www.wallix.com/press/wallix-achieves-dual-certifications-in-germany-and-france-reinforcing-its-position-as-a-trusted-european-cybersecurity/
