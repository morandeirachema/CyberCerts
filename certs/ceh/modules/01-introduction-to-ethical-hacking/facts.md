# Module 01 — Introduction to Ethical Hacking · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The CIA triad (+ two extensions)
| Element | Guarantee | Broken by |
|---|---|---|
| **Confidentiality** | Only authorized parties can read | Sniffing, theft, weak crypto |
| **Integrity** | Data is unaltered / trustworthy | Tampering, MITM |
| **Availability** | Accessible when needed | DoS/DDoS, ransomware |
| Authenticity | Genuinely from who it claims | Spoofing, forged tokens |
| Non-repudiation | Sender can't deny the action | Missing logging/signing |

Security is the balance of **CIA vs. functionality vs. usability** (the security triangle) — more of one usually costs the others.

## The five hacking phases (memorize the order)
**1. Reconnaissance → 2. Scanning → 3. Gaining Access → 4. Maintaining Access → 5. Clearing Tracks.**
Recon splits into **passive** (no contact — OSINT, WHOIS, Google) and **active** (touches the target — ping, DNS interrogation). *A single verb flips the answer: "port scan" = active, "WHOIS" = passive.*

## Attacker classes / hat colors
| Class | Authorized? | Intent |
|---|---|---|
| **White hat** | Yes | Ethical / defensive |
| **Black hat** | No | Malicious |
| **Grey hat** | No | Not clearly malicious, but still unauthorized |
| **Suicide hacker** | No | Cause damage, indifferent to being caught |
| **Script kiddie** | No | Runs others' tools, low skill |
| **Hacktivist** | No | Political / social agenda |
| **State-sponsored / APT** | No | Nation-state, well-resourced, persistent |
| **Insider** | Varies | Trusted access misused |

*"Ethical" hinges on **authorization + scope + reporting**, not on which tools you use.*

## Threat vs. vulnerability vs. risk vs. exploit
| Term | Definition |
|---|---|
| **Threat** | A potential cause of harm (actor/event) |
| **Vulnerability** | A weakness that could be exploited |
| **Exploit** | The actual code/technique that uses a vulnerability |
| **Risk** | Likelihood × impact = **Threat × Vulnerability** (roughly) |
| Exposure | An instance of being susceptible to loss |

## Frameworks — know them by name and shape
- **Cyber Kill Chain** (Lockheed Martin) — **linear**, 7 phases: Recon → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives.
- **MITRE ATT&CK** — a **matrix** of real-world post-compromise **tactics & techniques** (e.g., T1078 Valid Accounts). *Not* linear. Don't conflate it with the kill chain.
- **EC-Council / CEH methodology** — the five-phase model above.

## Assessment types (a classic exam distinction)
| Type | Knowledge given | Simulates |
|---|---|---|
| **Black box** | None | External attacker |
| **Grey box** | Partial | Insider / limited-knowledge attacker |
| **White box** | Full | Full internal review |
| **Vulnerability assessment** | — | *Find & rank* weaknesses (breadth, no exploit) |
| **Penetration test** | — | *Exploit* to prove impact (depth) |
| **Red team** | — | Goal-driven, stealthy — tests **detection & response** |

Attack classifications: **passive vs. active**, **inside vs. outside**.

## Defense-in-depth
Layered controls so no single failure = compromise: **policy/people → physical → perimeter → network → host → application → data**. Assumes any one layer *will* fail.

## Rules of Engagement / scope / authorization
- **Authorization first, always** — a signed *scope & authorization* document (get-out-of-jail authority) is what separates a pentest from a crime.
- **Rules of Engagement (RoE)** define: targets in/out of scope, allowed techniques, timing windows, points of contact, handling of sensitive data, and escalation/stop conditions.
- **Scope creep = out of bounds.** If you find a system you weren't authorized to touch, stop and report it.

## Laws & standards — match the name to what it governs
| Name | Governs |
|---|---|
| **PCI DSS** | Cardholder / payment card data |
| **HIPAA** | US health information (PHI) |
| **GDPR** | EU personal data / privacy |
| **ISO/IEC 27001** | Information security management systems (ISMS) |
| SOX | US financial reporting / integrity |
| CFAA (US) | Unauthorized computer access |
| DMCA | Copyright / anti-circumvention |
| NIST CSF · SP 800-115 | Risk framework · technical testing methodology |

## The one-line PAM angle
Every hacking phase either **targets privileged access or is contained by it** — CEH's whole methodology is the attacker's attempt to defeat *who can do what, when, and with what approval*. Read every later module as "which of my PAM controls does this bypass, and how would I detect it?" See [`../../defender-pam/`](../../defender-pam/).

## Top traps
- **Passive vs. active recon:** WHOIS/Google/DNS = passive; ping/port scan = active. One wrong verb flips it.
- **Kill Chain is linear; ATT&CK is a matrix.** Don't swap them.
- **VA ≠ PT ≠ Red team:** VA finds & ranks (no exploit), PT exploits to prove, Red team tests *detection*.
- **Grey box vs. grey hat:** grey **box** = partial-knowledge test; grey **hat** = an unauthorized-but-not-malicious hacker. Different concepts.
- **Match law → data:** PCI DSS = cards, HIPAA = health, GDPR = EU personal, SOX = financials, CFAA = unauthorized access.
- "Ethical" = **authorization + scope + reporting**, never "used only safe tools."
