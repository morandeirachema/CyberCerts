# Module 01 — Introduction to Ethical Hacking

> **One-liner:** the vocabulary, laws, methodology, and control frameworks that the rest of CEH is built on. Low on tools, high on definitions — and the exam tests those definitions precisely.

## Exam focus

- The **elements of information security**: Confidentiality, Integrity, Availability (CIA) — plus Authenticity and Non-repudiation.
- **Attacker classes / hat colors** and **threat actor types** (script kiddie, hacktivist, state-sponsored, insider, APT).
- The **Cyber Kill Chain**, **MITRE ATT&CK**, and the difference between them.
- **Hacking phases** (the methodology the whole course follows).
- **Types of assessment**: black/grey/white box; vulnerability assessment vs. penetration test vs. red team.
- **Attack classifications**: passive vs. active; inside vs. outside.
- **Defense-in-depth**, risk terms (threat, vulnerability, risk, exposure), and **why authorization/scope is everything**.
- Key **laws & standards** by name (you match the name to what it governs).

## Key concepts

### The five hacking phases (memorize the order)

```
┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌────────────────────┐
│ 1. Recon      │─▶│ 2. Scanning   │─▶│ 3. Gaining    │─▶│ 4. Maintaining│─▶│ 5. Clearing Tracks │
│ (footprint)   │  │ (enumerate)   │  │    Access     │  │    Access     │  │ (cover evidence)   │
└───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘  └────────────────────┘
```

Reconnaissance splits into **passive** (no direct contact — OSINT, WHOIS) and **active** (touching the target — ping, scan).

### CIA triad and extensions

| Element | Meaning | Broken by |
|---|---|---|
| Confidentiality | Only authorized parties can read | Sniffing, theft, weak crypto |
| Integrity | Data unaltered / trustworthy | Tampering, MITM |
| Availability | Accessible when needed | DoS/DDoS, ransomware |
| Authenticity | Genuinely from who it claims | Spoofing, forged tokens |
| Non-repudiation | Sender can't deny the action | Missing logging/signing |

### Attacker classes

Black hat (malicious), White hat (authorized/ethical), Grey hat (in-between/unauthorized-but-not-malicious), plus **suicide hackers, script kiddies, hacktivists, cyber terrorists, state-sponsored, insiders**.

### Assessment types (a classic exam distinction)

| Type | Goal | Knowledge given |
|---|---|---|
| Black box | Simulate external attacker | None |
| Grey box | Partial insider | Some |
| White box | Full review | Complete |
| Vulnerability assessment | *Find & rank* weaknesses (breadth) | — |
| Penetration test | *Exploit* to prove impact (depth) | — |
| Red team | Goal-based, stealthy, tests detection/response | — |

### Frameworks & methodologies to know by name

- **Cyber Kill Chain** (Lockheed Martin): Recon → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives.
- **MITRE ATT&CK**: a matrix of real-world **tactics & techniques** (post-compromise knowledge base). Different from the linear kill chain.
- **EC-Council hacking methodology / CEH methodology** — the phase model above.
- Standards you match by name: **ISO/IEC 27001**, **NIST CSF**, **PCI DSS**, **HIPAA**, **GDPR**, **SOX**, **DMCA**, and (US) the **Computer Fraud and Abuse Act (CFAA)**.

## Key tools

This module is conceptual; the "tools" are frameworks and references.

| Reference | Purpose | Link |
|---|---|---|
| MITRE ATT&CK | Tactics/techniques matrix | https://attack.mitre.org/ |
| Lockheed Cyber Kill Chain | Intrusion phases model | https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html |
| NIST CSF | Risk-based control framework | https://www.nist.gov/cyberframework |
| NIST SP 800-115 | Technical assessment methodology | https://csrc.nist.gov/pubs/sp/800/115/final |

## Commands & techniques (lab-ready)

No offensive commands here — instead, set up your **rules of engagement** discipline now. Create a scope file you will honor for every lab session:

```bash
# In your lab working dir, define scope explicitly (a habit the exam rewards conceptually)
cat > ~/lab-scope.txt <<'EOF'
AUTHORIZED TARGETS ONLY:
  192.168.56.10  kali (self)
  192.168.56.20  metasploitable2
  192.168.56.30  dc01
  127.0.0.1:8081-8084  docker web range
OUT OF SCOPE: everything else. No internet targets. No prod.
EOF
```

## Lab exercise

1. Read your own [`../../labs/topology.md`](../../labs/topology.md) and write, in one paragraph, a **rules-of-engagement** statement: what is in scope, what is explicitly out, and what you would do if you found a system you didn't expect.
2. Map three attacks you already know (from your sysadmin work) onto the **five phases** above.
3. Open MITRE ATT&CK and find the technique IDs for "Kerberoasting" (T1558.003) and "Valid Accounts" (T1078) — you'll revisit these in Modules 04 and 06.

**What you should observe:** the CEH methodology is just a disciplined, *authorized* version of the intrusion process attackers use — and every phase has a matching defensive control you likely already run.

## Defender & PAM mapping

| Concept | Detection signal | Control / PAM lever |
|---|---|---|
| Unauthorized access attempt | Failed logons, anomalous auth | Least privilege, MFA, PAM session brokering |
| Privileged misuse | Privileged session recording gaps | PAM session recording, just-in-time (JIT) access, approval workflows |
| Non-repudiation | Missing/immutable logs | Centralized logging, signed audit trails, tamper-evident SIEM |
| Scope/authorization | N/A (process) | Change control, documented RoE, break-glass procedures |

> **Your edge:** as a PAM practitioner you already think in terms of *who can do what, when, and with what approval*. CEH's whole methodology is the attacker's attempt to defeat exactly that. Read every later module as "which of my controls does this bypass, and how would I detect it?"

## Exam tips & gotchas

- **VA vs. PT vs. Red Team** is a frequent question — VA = find & rank (no exploit required), PT = exploit to prove, Red team = objective-driven and tests *detection*.
- **Passive vs. active recon**: WHOIS/Google/DNS lookups = passive; ping/port scan = active. A single wrong verb (e.g., "scanning") flips the answer.
- Kill Chain is **linear/pre-and-post**; ATT&CK is a **matrix of techniques** — don't conflate them.
- Match **law → purpose**: PCI DSS (cardholder data), HIPAA (health), SOX (financial reporting), GDPR (EU personal data), CFAA (US unauthorized access).
- "Ethical" hinges on **authorization + scope + reporting**, not on the tools used.

## Sources

- EC-Council CEH learning framework — https://www.eccouncil.org/cybersecurity-exchange/ethical-hacking/ceh-learning-framework/
- MITRE ATT&CK — https://attack.mitre.org/
- Lockheed Martin Cyber Kill Chain — https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html
- NIST SP 800-115 (Technical Guide to Information Security Testing) — https://csrc.nist.gov/pubs/sp/800/115/final
- NIST Cybersecurity Framework — https://www.nist.gov/cyberframework

---
### 📝 My lab log (fill in)
| Date | Target | Command | Result / notes |
|---|---|---|---|
|  |  |  |  |
