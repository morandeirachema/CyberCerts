# Module 01 — Introduction to Ethical Hacking · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** A tester performs WHOIS lookups, reviews the target's LinkedIn pages, and reads DNS records from public resolvers — never sending a packet to the target's own systems. Which activity is this?

- A. Active reconnaissance
- B. Passive reconnaissance
- C. Scanning
- D. Enumeration

<details><summary>Answer</summary>

**B. Passive reconnaissance.** No direct contact with the target's infrastructure means passive recon (OSINT). The moment you ping, port-scan, or query the target's *own* DNS server, it becomes **active** recon or scanning. **Exam tell:** watch the verb — "looked up / searched public records" = passive; "scanned / probed" = active.
</details>

---

**Q2.** Which single factor most clearly separates an **ethical hacker** from a black-hat attacker performing the same port scan?

- A. The tools used
- B. Written authorization and defined scope
- C. Whether an exploit succeeds
- D. The attacker's skill level

<details><summary>Answer</summary>

**B. Written authorization and defined scope.** Ethics is about *permission, scope, and reporting* — not tooling. Both may run the same scanner; only one has a signed authorization. Skill (D) and whether an exploit lands (C) are irrelevant to legality, and the tools (A) are identical.
</details>

---

**Q3.** An organization wants a test that measures how well its SOC **detects and responds** to a realistic, goal-driven intrusion. Which engagement fits best?

- A. Vulnerability assessment
- B. Black-box penetration test
- C. Red team engagement
- D. Compliance audit

<details><summary>Answer</summary>

**C. Red team engagement.** Red teaming is objective-driven and stealthy, explicitly testing **detection and response** (the blue team). A vulnerability assessment only finds and ranks weaknesses (no exploitation), and a standard pentest proves impact but isn't primarily about measuring detection. **Trap:** "tests detection/response" is the red-team giveaway.
</details>

---

**Q4.** Which statement correctly distinguishes a **vulnerability assessment** from a **penetration test**?

- A. A VA exploits findings to prove impact; a PT only lists them
- B. A VA finds and ranks weaknesses; a PT exploits them to prove impact
- C. They are the same thing with different names
- D. A PT never requires authorization

<details><summary>Answer</summary>

**B.** VA = **breadth**: identify and prioritize weaknesses without necessarily exploiting them. PT = **depth**: exploit to demonstrate real-world impact. Option A reverses the two — the classic distractor. All authorized testing (including PT) requires written authorization, so D is false.
</details>

---

**Q5.** Using **Risk ≈ Threat × Vulnerability**, which action lowers *risk* even when you cannot remove the threat actor?

- A. Ignoring the vulnerability because the threat is unavoidable
- B. Patching the vulnerability so there is nothing to exploit
- C. Increasing system usability
- D. Renaming the asset

<details><summary>Answer</summary>

**B. Patch the vulnerability.** You rarely control the *threat* (attackers exist), but reducing the *vulnerability* term drives the product — and thus the risk — down. Ignoring it (A) leaves risk unchanged; usability (C) can actually *raise* risk by weakening controls; renaming (D) is cosmetic.
</details>

---

**Q6.** Which set correctly lists the **five phases** of the CEH hacking methodology **in order**?

- A. Scanning → Recon → Gaining Access → Clearing Tracks → Maintaining Access
- B. Recon → Scanning → Gaining Access → Maintaining Access → Clearing Tracks
- C. Recon → Gaining Access → Scanning → Maintaining Access → Clearing Tracks
- D. Weaponization → Delivery → Exploitation → Installation → C2

<details><summary>Answer</summary>

**B. Recon → Scanning → Gaining Access → Maintaining Access → Clearing Tracks.** Option D is the *Cyber Kill Chain* (a different model), and A/C shuffle the order. **Clearing tracks is always last** — it's the anti-forensics/cover step, not something done before gaining access.
</details>

---

**Q7.** How does **MITRE ATT&CK** fundamentally differ from the **Cyber Kill Chain**?

- A. ATT&CK is a linear 7-step sequence; the Kill Chain is a matrix
- B. ATT&CK is a matrix of tactics and techniques; the Kill Chain is a linear phase model
- C. They are identical and interchangeable
- D. The Kill Chain covers only malware, ATT&CK only phishing

<details><summary>Answer</summary>

**B.** The **Kill Chain** (Lockheed Martin) is a **linear** intrusion sequence (Recon → … → Actions on Objectives). **ATT&CK** is a **matrix** of real-world **tactics and techniques** (e.g., T1078). Option A reverses them — the most common trap. They complement each other but are not the same.
</details>

---

**Q8.** A retailer that stores credit-card numbers must comply primarily with which standard?

- A. HIPAA
- B. PCI DSS
- C. GDPR
- D. SOX

<details><summary>Answer</summary>

**B. PCI DSS** governs the storage, processing, and transmission of **cardholder data**. HIPAA covers health information, GDPR covers EU personal data/privacy, and SOX covers financial-reporting integrity. **Exam skill:** match the *data type* to the regulation.
</details>

---

**Q9.** Which regulation would most directly apply to how a company handles the **personal data of EU residents**?

- A. CFAA
- B. HIPAA
- C. GDPR
- D. DMCA

<details><summary>Answer</summary>

**C. GDPR** (General Data Protection Regulation) governs EU personal-data processing and privacy rights. CFAA addresses unauthorized computer access (US), HIPAA covers US health data, and DMCA concerns copyright/anti-circumvention. Region + "personal data" points to GDPR.
</details>

---

**Q10.** In a **grey-box** penetration test, what is provided to the tester?

- A. No prior knowledge at all
- B. Complete source code and full architecture
- C. Partial knowledge, e.g., a standard user account or limited docs
- D. Only physical building access

<details><summary>Answer</summary>

**C. Partial knowledge.** Grey box simulates an attacker (or insider) with *some* information — a low-priv account, network diagram, or credentials. Black box gives **none** (A); white box gives **everything** (B). **Trap:** don't confuse grey *box* (a knowledge level) with a grey *hat* (an attacker class).
</details>

---

**Q11.** Which principle is best described as *"layered controls so that no single failure results in compromise"*?

- A. Least privilege
- B. Defense-in-depth
- C. Non-repudiation
- D. Separation of duties

<details><summary>Answer</summary>

**B. Defense-in-depth.** Multiple overlapping layers (perimeter, network, host, app, data) assume any one layer *will* fail, so another catches the attack. Least privilege and separation of duties are *specific* controls that live *within* those layers; non-repudiation is a CIA-extension goal, not a layering strategy.
</details>

---

**Q12.** Missing or tamper-able audit logs most directly undermine which security property?

- A. Confidentiality
- B. Availability
- C. Non-repudiation
- D. Usability

<details><summary>Answer</summary>

**C. Non-repudiation** — the guarantee that an actor cannot deny having performed an action — depends on trustworthy, immutable logging and signing. Without it, you can't attribute actions. Confidentiality is about *reading* data, availability about *access*, and usability isn't a CIA property. *(This is why immutable, centralized logs are a PAM/SOC staple.)*
</details>

---

**Q13.** During an authorized internal pentest you discover a production system that is **explicitly out of scope** but appears critically vulnerable. What is the correct action per Rules of Engagement?

- A. Exploit it quickly to prove the risk before anyone notices
- B. Stop, do not touch it, and report it to your point of contact
- C. Add it to scope yourself since you already have access
- D. Ignore it entirely and never mention it

<details><summary>Answer</summary>

**B. Stop and report it through the agreed contact.** Touching an out-of-scope system exceeds your authorization (potentially illegal, and voids the engagement). You also shouldn't stay silent — the RoE escalation path exists precisely so findings on unexpected systems get handled properly. You never expand scope unilaterally (C).
</details>

---

**Q14.** An attacker motivated by a **political cause** who defaces a government website to make a statement is best classified as a:

- A. Script kiddie
- B. Hacktivist
- C. State-sponsored actor
- D. Suicide hacker

<details><summary>Answer</summary>

**B. Hacktivist** — hacking driven by a political or social **agenda**. A script kiddie is defined by low skill (uses others' tools), a state-sponsored actor works for a nation-state with heavy resources, and a suicide hacker is one indifferent to getting caught. Motive is the deciding clue here.
</details>

---

**Q15.** Which of the following is a **passive** attack (as opposed to active)?

- A. SQL injection
- B. Traffic sniffing / eavesdropping
- C. A denial-of-service flood
- D. Modifying data in transit (MITM tampering)

<details><summary>Answer</summary>

**B. Traffic sniffing.** A **passive** attack observes without altering the system or data (hard to detect). SQL injection, DoS, and MITM *tampering* all **modify** state or availability, making them **active** attacks. **Rule of thumb:** if the attacker changes or disrupts something, it's active; if they only listen, it's passive.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the assessment-types and frameworks sections of [README.md](README.md).
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
