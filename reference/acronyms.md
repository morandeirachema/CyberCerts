# Acronyms Reference

> 🔁 This is the **PAM / identity** acronym list. For attack/offensive acronyms, see the
> [CEH acronyms reference](../certs/ceh/reference/acronyms.md).

A comprehensive, exam-oriented reference of the acronyms you will meet across
Privileged Access Management (PAM), the wider identity-security stack, the protocols
and cryptography underneath it, Operational Technology (OT), and the compliance world.
Acronyms are grouped into clearly-headed categories; within each category they are
listed in a table of **Acronym | Expansion | one-line context**.

Where an expansion or behaviour is uncertain or vendor-specific, it is flagged inline
rather than asserted. The concepts behind these acronyms are defined in the
[glossary](glossary.md) and the [foundations](../foundations/) folder; the controls they
describe are collected in the [PAM playbook](../certs/ceh/defender-pam/pam-playbook.md).

> **Vendor certification codes:** every major PAM vendor (CyberArk, BeyondTrust,
> Delinea, WALLIX, One Identity) runs its own administrator / professional / expert
> certification ladder with product-specific codes. Those codes are not listed here —
> see [adjacent certs](../certs/adjacent-certs/README.md) for how to choose one.

---

## a. PAM disciplines & product categories

| Acronym | Expansion | Context / meaning |
|---|---|---|
| **PAM** | Privileged Access Management | Control, vault, broker, record & audit privileged access. The discipline this whole repo is built around. |
| **PASM** | Privileged Account & Session Management | Analyst sub-category of PAM: vaulting credentials + brokering/recording sessions (the core of most PAM platforms). |
| **PEDM** | Privilege Elevation & Delegation Management | Elevate a specific command/application rather than the whole user; least privilege at the action level. |
| **EPM** | Endpoint Privilege Management | Remove local-admin rights on endpoints, grant per-app elevation; usually an agent-based product paired with PAM. |
| **IDaaS** | Identity-as-a-Service | Cloud-delivered SSO/MFA/federation (e.g. Okta, Microsoft Entra ID). |
| **IAG** | Identity & Access Governance | Vendor name for the governance discipline; answers "who *should* have access, and can we prove it?" |
| **IGA** | Identity Governance & Administration | The analyst-preferred name for the same governance discipline as IAG (near-synonyms). |
| **AAPM** | Application-to-Application Password Management | Eliminating hard-coded passwords in scripts/config (DevOps/RPA). *Flag: a marketing term; technically realised via the PAM REST API + vault plugins.* |
| **PAG** | Privileged Access Governance | IGA/IAG governance applied specifically to privileged accounts (pairing an IGA tool + the PAM platform). |
| **SSPR** | Self-Service Password Reset | IDaaS feature letting users reset their own directory password after verification. |

> See [PAM vs IAM/IGA/IDaaS/EPM](../foundations/pam-iam-iga-idaas-epm.md) for how these
> disciplines overlap, and the
> [PAM market landscape](../foundations/pam-market-landscape.md) for who sells what.

---

## b. Identity & access

| Acronym | Expansion | Context / meaning |
|---|---|---|
| **IAM** | Identity & Access Management | The broad foundation: manage digital identities and what they may access for the whole workforce. |
| **SSO** | Single Sign-On | Authenticate once, reach many trusting applications via federation (SAML/OIDC). |
| **MFA** | Multi-Factor Authentication | Require two or more independent factors (know / have / are); the top control against stolen passwords. |
| **2FA** | Two-Factor Authentication | MFA with exactly two factors; the common case of MFA. |
| **AuthN** | Authentication | Proving *who you are*. |
| **AuthZ** | Authorization | Determining *what you may do*. |
| **JIT** | Just-In-Time (access) | Grant privileged access only when needed, for a limited time, then auto-revoke. See [core concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md). |
| **ZSP** | Zero Standing Privileges | End state where no account holds privileged rights at rest; JIT applied everywhere. |
| **SoD** | Separation (Segregation) of Duties | Split a sensitive process so no one person controls all of it; detected as "toxic combinations" in IGA/IAG. |
| **PoLP** | Principle of Least Privilege | Grant the minimum rights needed (NIST SP 800-53 **AC-6**); the foundational rule of access security. |
| **CIEM** | Cloud Infrastructure Entitlement Management | Discover and right-size cloud entitlements/roles for least privilege. |
| **ZTNA** | Zero Trust Network Access | Per-session, per-resource access after verification (vs. a VPN dropping you on the network). |
| **ZTA** | Zero Trust Architecture | The architecture realising Zero Trust; defined in NIST SP 800-207. |
| **RBAC** | Role-Based Access Control | Grant access by assigning users to roles that bundle permissions. |
| **ABAC** | Attribute-Based Access Control | Grant access from attributes/policy (user, resource, context) rather than fixed roles. |
| **A2A** | Application-to-Application | Non-human/machine authentication between apps/services (the use case behind AAPM). |
| **JML** | Joiner-Mover-Leaver | The identity lifecycle (onboarding, role change, offboarding) governed by IAM/IGA. |
| **CIAM** | Customer Identity & Access Management | IAM specialised for external customers/consumers (context). |

---

## c. Protocols & directory services

| Acronym | Expansion | Context / meaning |
|---|---|---|
| **SSH** | Secure Shell | Encrypted remote-shell/file protocol (TCP 22); a primary PAM proxy protocol (with SFTP/sub-systems). |
| **SFTP** | SSH File Transfer Protocol | File transfer over SSH; a controllable SSH sub-protocol in a PAM proxy. |
| **RDP** | Remote Desktop Protocol | Microsoft graphical remote-desktop protocol (TCP 3389); proxied and recorded by PAM. |
| **VNC** | Virtual Network Computing | Cross-platform graphical remote-control protocol; a common PAM proxy protocol. |
| **LDAP** | Lightweight Directory Access Protocol | Directory query/auth protocol (e.g. Active Directory, port 389). |
| **LDAPS** | LDAP over SSL/TLS | Encrypted LDAP (port 636). |
| **AD** | Active Directory | Microsoft's directory service; the key external authentication source for PAM, IDaaS and EPM products. |
| **RADIUS** | Remote Authentication Dial-In User Service | AAA / network-auth protocol (UDP 1812); common MFA "second-factor" channel. |
| **TACACS+** | Terminal Access Controller Access-Control System Plus | Cisco AAA protocol for device administration (separates authN/authZ/accounting). |
| **SAML** | Security Assertion Markup Language | XML-based SSO/federation standard (v2.0); a PAM web portal can act as a SAML Service Provider. |
| **OIDC** | OpenID Connect | Identity layer on top of OAuth 2.0 for SSO; supported by most PAM portals (Authorization Code Flow) and IDaaS platforms. |
| **OAuth** | Open Authorization | Delegated-authorization framework (v2.0) underlying OIDC. |
| **SCIM** | System for Cross-domain Identity Management | Standard for provisioning/deprovisioning users & groups across apps (v2.0). |
| **SNMP** | Simple Network Management Protocol | Monitoring protocol (v2c/v3) supported by PAM appliances for health/metrics. |
| **Syslog** | System Logging Protocol | Standard event-logging transport (port 514); how PAM forwards events to a SIEM. |
| **NLA** | Network Level Authentication | RDP pre-authentication (default on in most RDP proxies) that authenticates before a full session. |
| **Kerberos** | (not an acronym) | Ticket-based network authentication protocol; used in PAM RDP/directory integration. |
| **TELNET** | Telecommunication Network | Legacy unencrypted remote-terminal protocol; proxied/recorded by PAM (common in OT). |
| **RLOGIN** | Remote Login | Legacy Unix remote-login protocol; still proxied by some PAM products. |
| **DNS** | Domain Name System | Name-to-IP resolution; relevant to target addressing (FQDN) and appliance networking. |
| **FQDN** | Fully Qualified Domain Name | A complete host name; one way to define a PAM device/target. |
| **CIDR** | Classless Inter-Domain Routing | IP subnet notation (e.g. `10.0.0.0/24`); one way to define a PAM device by subnet. |

---

## d. Cryptography & PKI

| Acronym | Expansion | Context / meaning |
|---|---|---|
| **TLS** | Transport Layer Security | Modern encryption-in-transit protocol (successor to SSL); secures HTTPS/LDAPS, etc. |
| **SSL** | Secure Sockets Layer | Legacy predecessor to TLS; the term persists colloquially ("SSL certificate"). |
| **PKI** | Public Key Infrastructure | The system of CAs, certificates and revocation that binds keys to identities. |
| **CA** | Certificate Authority | Trusted issuer that signs digital certificates. |
| **CSR** | Certificate Signing Request | A request (containing a public key) submitted to a CA to obtain a certificate. |
| **CRL** | Certificate Revocation List | A published list of revoked certificates; checked for X.509 client-certificate auth. |
| **OCSP** | Online Certificate Status Protocol | Real-time certificate-revocation check (alternative to a CRL). |
| **AES** | Advanced Encryption Standard | Symmetric cipher; PAM vaults typically use **AES-256** (encryption at rest/in transit). |
| **RSA** | Rivest–Shamir–Adleman | Public-key algorithm; PAM products default to large RSA keys (≥ 3072-bit; 4096 for rotated SSH keys). |
| **ECDSA** | Elliptic Curve Digital Signature Algorithm | Elliptic-curve signature algorithm; supported for SSH key generation by PAM vaults. |
| **ECC** | Elliptic Curve Cryptography | The family of curve-based public-key crypto (e.g. ECDSA). |
| **DSA** | Digital Signature Algorithm | Older signature algorithm; still offered for SSH key generation (RSA/ECDSA preferred). |
| **SHA** | Secure Hash Algorithm | Cryptographic hash family; **SHA-2** is the current standard. |
| **LUKS** | Linux Unified Key Setup | Linux disk-encryption standard (dm-crypt); typical encryption at rest for Linux-based appliances. |
| **TOTP** | Time-based One-Time Password | OTP derived from a shared secret + current time (RFC 6238); the most common MFA factor. |
| **HOTP** | HMAC-based One-Time Password | Counter-based OTP (RFC 4226); the precursor to TOTP. |
| **OTP** | One-Time Password | A single-use code; delivered via TOTP/HOTP, SMS, or email. |
| **HMAC** | Hash-based Message Authentication Code | Keyed-hash integrity/authentication construct underlying HOTP/TOTP. |
| **FIDO** | Fast IDentity Online | Passwordless/strong-auth standards body & protocols (FIDO U2F, **FIDO2**). |
| **FIDO2** | FIDO second-generation standard | Phishing-resistant auth using hardware keys (e.g. YubiKey) via WebAuthn + CTAP. |
| **WebAuthn** | Web Authentication | W3C browser API for FIDO2 hardware-key authentication; a common IDaaS MFA option. |
| **CTAP** | Client to Authenticator Protocol | The FIDO2 companion to WebAuthn linking browser/OS to the security key. |
| **GPG** | GNU Privacy Guard | OpenPGP implementation; used to encrypt vault exports and sign appliance images. |
| **PGP** | Pretty Good Privacy | The encryption standard GPG implements (OpenPGP). |

> **Crypto policy note:** many PAM appliances offer a selectable cryptographic level;
> European buyers typically look for alignment with the **SOG-IS agreed cryptographic
> mechanisms**. See [protocols](../protocols/) for the underlying primitives.

---

## e. OT / industrial

| Acronym | Expansion | Context / meaning |
|---|---|---|
| **OT** | Operational Technology | Hardware/software that monitors & controls physical processes (factories, utilities); the domain of PAM-for-OT. |
| **IT** | Information Technology | The conventional enterprise computing domain; contrasted with OT at the IT/OT boundary. |
| **ICS** | Industrial Control System | Umbrella term for control systems (SCADA, DCS, PLCs) running industrial processes. |
| **SCADA** | Supervisory Control And Data Acquisition | Systems that supervise and acquire data from geographically distributed industrial assets. |
| **DCS** | Distributed Control System | Process-control system with controllers distributed across a plant (context). |
| **PLC** | Programmable Logic Controller | Ruggedised industrial computer controlling machinery; an OT target (cannot host agents → agentless PAM). |
| **RTU** | Remote Terminal Unit | Field device that collects telemetry and relays it to SCADA; an OT target. |
| **HMI** | Human-Machine Interface | Operator screen/console for an industrial process; an OT target often reached over RDP/VNC. |
| **DMZ** | Demilitarized Zone | A buffer network between trust zones; an **Industrial DMZ** sits between IT and OT (Purdue Level 3.5) where a PAM jump host lives. |
| **IIoT** | Industrial Internet of Things | Networked industrial sensors/devices (context for OT attack surface). |
| **Modbus** | (not an acronym) | Common industrial protocol; can be encapsulated in an SSH tunnel by a PAM proxy for traceable PLC access. |
| **LPM** | Loi de Programmation Militaire | France's military-programming law imposing security obligations on critical operators. |

> See the OT discussion in [PAM for OT](../certs/ceh/ot-security/05-pam-for-ot.md).

---

## f. Compliance, standards & bodies

| Acronym | Expansion | Context / meaning |
|---|---|---|
| **NIS2** | Network and Information Security Directive 2 | EU directive (2022/2555) raising cybersecurity obligations for essential/important entities. |
| **IEC** | International Electrotechnical Commission | Standards body publishing IEC 62443 (with ISA), IEC 27001 alignment, etc. |
| **ISA** | International Society of Automation | Co-author of the ISA/IEC 62443 OT-security series. |
| **62443** | ISA/IEC 62443 | The leading **OT/ICS** security standard series (zones & conduits, security levels). |
| **DORA** | Digital Operational Resilience Act | EU regulation (2022/2554) on ICT operational resilience for the financial sector. |
| **GDPR** | General Data Protection Regulation | EU regulation (2016/679) on personal-data protection; drives access control & auditability. |
| **ISO** | International Organization for Standardization | Standards body; co-publishes ISO/IEC 27001 with the IEC. |
| **ISO 27001** | ISO/IEC 27001 | International standard for Information Security Management Systems (ISMS); most PAM vendors hold 27001:2022. |
| **ISMS** | Information Security Management System | The managed framework of policies/controls that ISO 27001 certifies. |
| **PCI DSS** | Payment Card Industry Data Security Standard | Card-data protection standard; strict on privileged access, MFA, logging & unique IDs. |
| **SOX** | Sarbanes-Oxley Act | US law on financial reporting integrity; drives access controls & SoD over financial systems. |
| **HIPAA** | Health Insurance Portability and Accountability Act | US healthcare law; its Security Rule governs access control & audit of electronic PHI. |
| **PHI** | Protected Health Information | The health data HIPAA protects (context). |
| **NERC CIP** | North American Electric Reliability Corporation — Critical Infrastructure Protection | Mandatory standards for the North American bulk electric system (strong on electronic access & logging). |
| **NIST** | National Institute of Standards and Technology | US body publishing the CSF and the SP 800 series. |
| **CSF** | Cybersecurity Framework | NIST's voluntary framework (Identify/Protect/Detect/Respond/Recover, + Govern in CSF 2.0). |
| **SP** | Special Publication | NIST document series (e.g. **SP 800-53**, **SP 800-82**, **SP 800-171**, **SP 800-207**). |
| **ANSSI** | Agence nationale de la sécurité des systèmes d'information | France's national cybersecurity agency; issues the **CSPN** certification. |
| **BSI** | Bundesamt für Sicherheit in der Informationstechnik | Germany's federal cybersecurity office; issues the **BSZ** certification. |
| **CSPN** | Certification de Sécurité de Premier Niveau | ANSSI's first-level security certification; a national product certification PAM products may hold. |
| **BSZ** | Beschleunigte Sicherheitszertifizierung | BSI's accelerated security certification; mutually recognised with ANSSI CSPN since late 2025. |
| **ENISA** | European Union Agency for Cybersecurity | EU agency supporting cybersecurity policy/implementation (e.g. NIS2 guidance). |
| **SOG-IS** | Senior Officials Group — Information Systems Security | European group behind crypto-evaluation agreements (the "agreed cryptographic mechanisms" list). |
| **CC** | Common Criteria | International security-evaluation framework (ISO/IEC 15408). |
| **EAL** | Evaluation Assurance Level | Common Criteria assurance rating (EAL1–7). |
| **CIS** | Center for Internet Security | Publisher of the CIS Controls / Benchmarks (hardening guidance; context). |

> Full mapping of how PAM supports each of these is in
> [compliance & standards](compliance-and-standards.md).

---

## g. Operations & infrastructure

| Acronym | Expansion | Context / meaning |
|---|---|---|
| **HA** | High Availability | Resilient configuration avoiding single points of failure; for PAM usually DB replication + multiple proxies. See [PAM architecture](../certs/ceh/defender-pam/pam-architecture.md). |
| **DR** | Disaster Recovery | The capability to restore service after a major outage/disaster. |
| **DRP** | Disaster Recovery Plan | The documented procedure executing DR (objectives, steps, roles). |
| **RPO** | Recovery Point Objective | Max acceptable data loss (time) in a disaster — relevant to what the PAM replication covers. |
| **RTO** | Recovery Time Objective | Max acceptable downtime before service is restored. |
| **SIEM** | Security Information and Event Management | Central log/event correlation platform; PAM forwards events via Syslog. See [detection engineering](../certs/ceh/defender-pam/detection-engineering.md). |
| **SOAR** | Security Orchestration, Automation and Response | Automates incident response on top of SIEM (context for API-driven PAM actions). |
| **UEBA** | User and Entity Behavior Analytics | Anomaly detection from user/entity behaviour; increasingly bundled with PAM session analytics. |
| **API** | Application Programming Interface | Programmatic interface; every serious PAM platform exposes a **REST API** for automation. |
| **REST** | Representational State Transfer | The architectural style of most PAM HTTP/JSON APIs. |
| **JSON** | JavaScript Object Notation | The data format used by PAM REST APIs. |
| **ETL** | Extract, Transform, Load | Data-integration pattern; IGA tools use an ETL to consolidate identity data from many sources. |
| **OVA** | Open Virtual Appliance / Open Virtualization Archive | Packaged virtual-machine image; the usual format for PAM appliance and lab images. |
| **OVF** | Open Virtualization Format | The standard an OVA packages a VM in. |
| **VM** | Virtual Machine | Software-emulated computer; PAM components ship as virtual appliances for major hypervisors/clouds. |
| **ISO** | ISO disk image | A bootable image; appliances are also distributed as signed ISOs. *(Distinct from ISO the standards body.)* |
| **GUI** | Graphical User Interface | The PAM admin web GUI. |
| **CLI** | Command-Line Interface | Text command interface; e.g. appliance replication/maintenance CLIs. |
| **LVM** | Logical Volume Manager | Linux volume manager; appliances store data/recordings on LVM, extendable for retention. |
| **DRBD** | Distributed Replicated Block Device | Block-level replication; used by some older appliance HA designs, now mostly replaced by DB replication. |
| **SLA** | Service Level Agreement | Contractual availability/performance commitment (PAM SaaS offerings typically promise 99.9 % uptime). |
| **SaaS** | Software-as-a-Service | Cloud subscription delivery model; every major PAM vendor now offers a SaaS edition. |
| **MSP** | Managed Service Provider | Outsourced IT/security provider; a common channel for PAM SaaS. |
| **ITSM** | IT Service Management | Ticketing/service platforms integrated for approval workflows & IGA remediation. |
| **KPI** | Key Performance Indicator | Metric surfaced in PAM dashboards for audit/activity reporting. |
| **DC** | Domain Controller | Active Directory server; EPM agents and PAM directory integrations contact the closest DC. |
| **GPO** | Group Policy Object | Windows/AD policy mechanism; EPM products often distribute policy in an AD/GPO-style manner. |
| **MMC** | Microsoft Management Console | Windows admin console; some EPM products are managed via an MMC snap-in. |

---

## See also

- [Glossary](glossary.md) — plain-language definitions of the concepts behind these acronyms.
- [Compliance & standards](compliance-and-standards.md) — how PAM maps to each framework.
- [PAM vs IAM/IGA/IDaaS/EPM](../foundations/pam-iam-iga-idaas-epm.md)
- [Core concepts: least privilege, JIT, Zero Trust](../foundations/core-concepts-least-privilege-jit-zero-trust.md)
- [PAM market landscape](../foundations/pam-market-landscape.md)
- [Adjacent certs](../certs/adjacent-certs/README.md) — vendor certification ladders.

---

## Sources

- NIST SP 800-53 Rev. 5 (AC-6 least privilege): https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- NIST Cybersecurity Framework 2.0: https://www.nist.gov/cyberframework
- ISA/IEC 62443 series overview (ISA): https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards
- IETF — TOTP (RFC 6238): https://www.rfc-editor.org/rfc/rfc6238 · HOTP (RFC 4226): https://www.rfc-editor.org/rfc/rfc4226
- FIDO Alliance — FIDO2 / WebAuthn / CTAP: https://fidoalliance.org/fido2/
- ANSSI — CSPN: https://cyber.gouv.fr/la-certification-de-securite-de-premier-niveau-cspn
- BSI — BSZ (Beschleunigte Sicherheitszertifizierung): https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Zertifizierung-und-Anerkennung/
- Gartner — PAM glossary (PASM/PEDM): https://www.gartner.com/en/information-technology/glossary/privileged-access-management-pam
