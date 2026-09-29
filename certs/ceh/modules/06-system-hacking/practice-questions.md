# Module 06 — System Hacking · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** An attacker obtains a user's NTLM hash and authenticates to a remote SMB share **without cracking it**. Which technique is this?

- A. Kerberoasting
- B. Pass-the-Hash
- C. AS-REP roasting
- D. Offline dictionary attack

<details><summary>Answer</summary>

**B. Pass-the-Hash.** The NT hash is used *directly* to authenticate over NTLM — no plaintext recovery needed. Kerberoasting and AS-REP roasting both require *offline cracking* of the retrieved material, and an offline dictionary attack is by definition a cracking step. **Exam tell:** if the question says the hash is *used directly / not cracked*, it's PtH.
</details>

---

**Q2.** During an AD assessment you request a service ticket for an account with an SPN and crack it offline. What did you crack?

- A. The krbtgt account password
- B. The user's password
- C. The service account's password
- D. The domain controller's machine password

<details><summary>Answer</summary>

**C. The service account's password.** This is **Kerberoasting**: the TGS is encrypted with the *service account's* key, so cracking it yields that account's password. It works because service accounts often have weak, non-expiring passwords and NTLM/RC4 is unsalted. **Fix:** gMSA (128-char auto-rotated) or a CPM-managed long random password, AES-only.
</details>

---

**Q3.** Which control most directly defeats **Kerberoasting**?

- A. Group Managed Service Accounts (gMSA)
- B. Account lockout policy
- C. BitLocker full-disk encryption
- D. Disabling SMBv1

<details><summary>Answer</summary>

**A. gMSA.** Kerberoasting cracks a service-account password offline, so lockout policy (an *online* control) can't stop it. gMSA gives the service account a 128-character, automatically rotated password that is computationally infeasible to crack — removing the payoff. BitLocker and SMBv1 are unrelated.
</details>

---

**Q4.** A **salt** primarily defeats which attack?

- A. Brute-force attacks
- B. Rainbow-table (precomputation) attacks
- C. Pass-the-Ticket
- D. Keylogging

<details><summary>Answer</summary>

**B. Rainbow-table attacks.** A per-hash random salt makes precomputed hash→plaintext tables useless. It does **not** stop brute force or dictionary attacks against a single hash (those recompute per guess anyway). Note NTLM is *unsalted*, which is why it remains crackable.
</details>

---

**Q5.** Which Windows credential store holds **all domain account hashes** and is the target of a DCSync attack?

- A. SAM
- B. LSA secrets
- C. Credential Manager
- D. NTDS.dit

<details><summary>Answer</summary>

**D. NTDS.dit.** It's the AD database on domain controllers containing every domain account's hash. DCSync abuses *replication rights* to pull hashes (including **krbtgt**) from it without touching disk. SAM holds *local* hashes; LSA secrets holds service-account secrets.
</details>

---

**Q6.** What distinguishes a **Golden ticket** from a **Silver ticket**?

- A. Golden forges a TGS; Silver forges a TGT
- B. Golden works only on Linux realms
- C. Golden requires cracking; Silver does not
- D. Golden is signed with the krbtgt hash; Silver is signed with a service account's key

<details><summary>Answer</summary>

**D.** A **Golden ticket** forges a **TGT** using the **krbtgt** hash (domain-wide power); a **Silver ticket** forges a **TGS** for a specific service using that **service account's** key (narrower). Neither requires cracking — both are post-compromise forgeries. After a krbtgt compromise you must rotate krbtgt **twice**.
</details>

---

**Q7.** On a Linux foothold, which single command best reveals what you can run as root for privilege escalation?

- A. `find / -perm -4000`
- B. `sudo -l`
- C. `cat /etc/passwd`
- D. `netstat -tulpn`

<details><summary>Answer</summary>

**B. `sudo -l`** lists the commands the current user may run via sudo (a direct privesc path). `find / -perm -4000` is *also* a privesc check but finds **SUID binaries**, not sudo rights — a good distractor. `/etc/passwd` no longer holds hashes; `netstat` is for listening services.
</details>

---

**Q8.** Which Hashcat mode cracks **NTLM** hashes?

- A. `-m 0`
- B. `-m 100`
- C. `-m 1000`
- D. `-m 13100`

<details><summary>Answer</summary>

**C. `-m 1000`.** Memorize the set: `0`=MD5, `100`=SHA1, `1000`=NTLM, `13100`=Kerberos TGS-REP (Kerberoasting), `5600`=NetNTLMv2 (Responder), `22000`=WPA.
</details>

---

**Q9.** A SOC analyst sees a burst of **4769** events requesting service tickets with **RC4 (0x17)** encryption for several SPN accounts. What is the most likely activity?

- A. Password spraying
- B. Pass-the-Hash
- C. DCSync
- D. Kerberoasting

<details><summary>Answer</summary>

**D. Kerberoasting.** Event 4769 = TGS request; a spike for SPN accounts, especially forcing weak **RC4**, is the classic signature. Password spraying shows as many **4625** failures; DCSync shows **4662** replication from a non-DC; PtH shows NTLM **4624** type-3 logons from unusual hosts.
</details>

---

**Q10.** Which attack abuses **replication rights** to extract hashes from a domain controller *without running code on it*?

- A. DCSync
- B. Pass-the-Ticket
- C. Overpass-the-Hash
- D. Kerberoasting

<details><summary>Answer</summary>

**A. DCSync.** It impersonates a DC and requests replication of secrets (using `DS-Replication-Get-Changes-All`), so it needs no code execution on the DC. Detection: **4662** with the replication GUIDs from a **non-DC** account. Control: restrict replication rights, Tier 0 isolation.
</details>

---

**Q11.** Which technique provides *unique* local administrator passwords per host to stop lateral movement via a shared local admin hash?

- A. LAPS
- B. AppLocker
- C. Kerberos armoring
- D. LLMNR

<details><summary>Answer</summary>

**A. LAPS** (Local Administrator Password Solution) randomizes and rotates each machine's local admin password and stores it in AD/Entra. This kills "one local admin hash works everywhere" reuse. AppLocker is app allow-listing; the others are unrelated.
</details>

---

**Q12.** Data hidden in an **NTFS Alternate Data Stream** is associated with which phase?

- A. Scanning
- B. Gaining Access
- C. Maintaining Access / Clearing tracks (anti-forensics)
- D. Reconnaissance

<details><summary>Answer</summary>

**C.** ADS (`file.txt:hidden.exe`) hides content to evade casual inspection — an anti-forensics / persistence technique in the later phases, not initial access.
</details>

---

**Q13.** Vertical privilege escalation means:

- A. Accessing another user's account at the same privilege level
- B. Gaining a *higher* privilege level than currently held
- C. Moving laterally to another host
- D. Escalating network bandwidth

<details><summary>Answer</summary>

**B.** Vertical = **higher** privilege (user → admin/root). Horizontal = same level, *different* user (option A). Don't confuse the two.
</details>

---

**Q14.** Why is **Pass-the-Ticket** not stopped by resetting a user's password?

- A. It reuses an existing Kerberos ticket, which remains valid until expiry
- B. It only targets local accounts
- C. It cracks the password offline first
- D. It requires no authentication at all

<details><summary>Answer</summary>

**A.** PtT reuses a stolen **TGT/TGS**, valid until it expires regardless of a password change. That's why Protected Users, short ticket lifetimes, and (for krbtgt) double rotation matter. It does *not* involve cracking.
</details>

---

**Q15.** Which combination best reduces the impact of **LSASS credential dumping** with Mimikatz?

- A. Longer user passwords only
- B. Enabling LLMNR
- C. Disabling IPv6
- D. Credential Guard + LSASS PPL + EDR/attack-surface-reduction

<details><summary>Answer</summary>

**D.** Credential Guard isolates secrets in a virtualized container, LSASS runs as a Protected Process (PPL), and EDR/ASR rules block the handle-open to lsass. Longer passwords don't stop *dumping* a logged-on credential; disabling IPv6 and enabling LLMNR are irrelevant (LLMNR *on* is actually a risk).
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the Hash & ticket attacks and Windows credential-store sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
