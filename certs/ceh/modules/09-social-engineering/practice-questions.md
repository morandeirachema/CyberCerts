# Module 09 — Social Engineering · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** An attacker sends a text message to a target's phone: "Your bank card is locked — tap https://secure-bank.co to reactivate." Which technique is this?

- A. Vishing
- B. Pharming
- C. Whaling
- D. Smishing

<details><summary>Answer</summary>

**D. Smishing.** Smishing is phishing delivered over **SMS** and is classed as **mobile-based**. Vishing would be a *voice call*; whaling is an *email* aimed at an executive; pharming needs no message at all — it poisons name resolution. **Tell:** channel = text message ⇒ smishing.
</details>

---

**Q2.** A finance clerk receives an email that appears to come from the CEO: "I'm in a board meeting — wire $48,000 to this new supplier today, keep it confidential." No malware, no link. What is this?

- A. Baiting
- B. Business Email Compromise (BEC)
- C. Pharming
- D. Quid pro quo

<details><summary>Answer</summary>

**B. Business Email Compromise.** BEC impersonates a trusted executive or vendor to authorize a **fraudulent wire transfer or invoice change** — it weaponizes authority and urgency, not a payload. That's why it slips past antivirus. **Controls:** DMARC/SPF/DKIM to block spoofing, plus an out-of-band callback to verify payment changes.
</details>

---

**Q3.** An attacker follows an employee through a secured door **while the employee holds it open for them, believing they belong**. Which term fits best?

- A. Tailgating
- B. Impersonation
- C. Shoulder surfing
- D. Piggybacking

<details><summary>Answer</summary>

**D. Piggybacking.** Piggybacking = the authorized person *knowingly* grants entry ("hold the door"). **Tailgating** is the near-twin where the badge-holder is *unaware* they're being followed. The consent distinction is the whole question — memorize it.
</details>

---

**Q4.** A caller tells a help-desk agent: "This is Dave from IT — I need to fix your mailbox, just read me your current password." Which two techniques are combined?

- A. Pharming and baiting
- B. Impersonation and pretexting (via vishing)
- C. Dumpster diving and eavesdropping
- D. Whaling and smishing

<details><summary>Answer</summary>

**B. Impersonation and pretexting, delivered by vishing.** The attacker *impersonates* IT and invents a *pretext* (a mailbox fix) over a **voice call** (vishing) to justify the request. Human-based attacks routinely stack these. **Control:** help-desk scripts that never accept a password and verify identity out-of-band.
</details>

---

**Q5.** An attacker leaves USB drives labeled "Q3 Layoffs" in the office parking lot, hoping someone plugs one in. Which technique is this, and what human trait does it exploit?

- A. Quid pro quo — reciprocity
- B. Reverse SE — helpfulness
- C. Baiting — curiosity/greed
- D. Pharming — habit

<details><summary>Answer</summary>

**C. Baiting — curiosity/greed.** Baiting *dangles an item* (an infected USB or "free" download) and waits for the victim to take it. Contrast **quid pro quo**, which offers a *service in exchange* — a transaction. Both trade on desire; baiting is the physical/dropped item.
</details>

---

**Q6.** A victim types their bank's correct URL but a poisoned `hosts` file silently sends them to a look-alike site that harvests their login. No link was clicked. What is this?

- A. Pharming
- B. Spear-phishing
- C. Smishing
- D. Angler phishing

<details><summary>Answer</summary>

**A. Pharming.** Pharming redirects a *legitimate* address via **DNS or hosts-file poisoning** — the user does everything right and still lands on a fake page. This is the key difference from phishing, which relies on tricking the victim into clicking a *bad* link. **Controls:** DNSSEC, protected resolvers, HSTS, file-integrity monitoring on `hosts`.
</details>

---

**Q7.** Which attack is a **subset** of spear-phishing, defined solely by *who* it targets?

- A. Vishing
- B. Whaling
- C. Baiting
- D. Pharming

<details><summary>Answer</summary>

**B. Whaling.** Whaling is spear-phishing aimed specifically at **executives / high-value "big fish."** Spear-phishing is targeted-but-general; whaling narrows the target to the C-suite. The others are different channels or techniques entirely.
</details>

---

**Q8.** During a physical assessment you recover printed org charts and old password sticky-notes from the office trash. Which technique, and which bucket?

- A. Eavesdropping — computer-based
- B. Baiting — mobile-based
- C. Dumpster diving — human-based
- D. Pharming — computer-based

<details><summary>Answer</summary>

**C. Dumpster diving — human-based.** It's a physical, non-electronic collection technique feeding the **Research** phase of the lifecycle. It sits in the human-based bucket alongside shoulder surfing and impersonation. **Control:** shredding / media-sanitization and clean-desk policy.
</details>

---

**Q9.** An attacker plants a rumor of a "network problem," then poses as support so the victim *calls them* for help and hands over credentials during the "fix." What is this?

- A. Reverse social engineering
- B. Quid pro quo
- C. Tailgating
- D. Whaling

<details><summary>Answer</summary>

**A. Reverse social engineering.** The defining trait: the **victim initiates contact**. The attacker seeds a problem, advertises themselves as the fix, and waits to be approached — which lowers the victim's guard because *they* asked. Quid pro quo is close but the *attacker* makes the first offer.
</details>

---

**Q10.** A phished user enters their password into a fake portal, but the attacker still cannot log in because a hardware security key is required. Which countermeasure defeated the attack?

- A. Account lockout policy
- B. Phishing-resistant MFA (FIDO2/WebAuthn)
- C. A longer password policy
- D. Antivirus on the endpoint

<details><summary>Answer</summary>

**B. Phishing-resistant MFA (FIDO2/WebAuthn).** The harvested password becomes worthless because authentication is bound to a hardware key that a fake site can't relay. This is the exam's favored *technical* control for credential phishing. Lockout and longer passwords do nothing once the password is already given up.
</details>

---

**Q11.** On a "best countermeasure to social engineering" question with these choices, which is almost always correct on the exam?

- A. Security awareness training combined with MFA
- B. A next-generation firewall
- C. Full-disk encryption
- D. An intrusion prevention system

<details><summary>Answer</summary>

**A. Security awareness training combined with MFA.** SE targets people, so the durable answer pairs *human* defense (training, reporting culture) with *technical* backstops (MFA). Perimeter/host tech (firewall, IPS, FDE) never fully solves a human-trust attack — a favorite distractor pattern.
</details>

---

**Q12.** Which set of email controls most directly stops an attacker from **spoofing your CEO's sending domain** in a BEC email?

- A. SPF, DKIM, and DMARC
- B. TLS 1.3 and HSTS
- C. WPA3 and 802.1X
- D. NAC and VLAN segmentation

<details><summary>Answer</summary>

**A. SPF, DKIM, and DMARC.** Together they authenticate the sending domain and tell receivers to reject unaligned mail — shutting down exact-domain spoofing used in whaling/BEC. TLS/HSTS protect web transport; the others are network/wireless controls, unrelated to sender spoofing.
</details>

---

**Q13.** A compromised employee account is now being used by an attacker inside the network. Which insider-threat category is this, and which control detects it best?

- A. Malicious — firewall rules
- B. Negligent — password complexity
- C. Compromised — privileged session recording + UEBA
- D. Professional/mole — antivirus

<details><summary>Answer</summary>

**C. Compromised — privileged session recording + UEBA.** A phished user turned into the attacker's tool is the **compromised** insider. Because they use *valid* credentials, behavioral analytics (off-hours, out-of-role access) and session recording detect them, not the perimeter. Least privilege + JIT shrink what they can reach.
</details>

---

**Q14.** In the social engineering attack lifecycle, gathering OSINT, dumpster-diving, and studying org charts belongs to which phase?

- A. Play
- B. Exit
- C. Research
- D. Hook

<details><summary>Answer</summary>

**C. Research.** The lifecycle is **Research → Hook → Play → Exit.** Research is the reconnaissance/information-gathering phase that fuels a believable pretext. *Hook* is first contact/rapport; *Play* exploits the trust; *Exit* is the clean escape.
</details>

---

**Q15.** A help desk receives an urgent call requesting a **privileged account** password reset — no ticket, lots of pressure. Which control most directly prevents a successful pretext here?

- A. A stronger password complexity requirement
- B. A longer screen-lock timeout
- C. Enabling LLMNR on the network
- D. Out-of-band identity verification (callback + secondary factor + approval) for privileged resets

<details><summary>Answer</summary>

**D. Out-of-band identity verification for privileged resets.** The help desk is a top SE target because it can hand over Tier 0. Requiring a callback, a secondary factor, and manager approval means a pretext alone can't satisfy the proof bar. Complexity/timeouts don't address *who* is asking.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the phishing-family and human-based technique tables.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
