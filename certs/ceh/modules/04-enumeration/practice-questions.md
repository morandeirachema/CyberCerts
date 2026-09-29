# Module 04 — Enumeration · Practice Questions

> **Original, concept-based questions** — not exam dumps. Answers are collapsed: decide first, then expand. Target **≥80%**. Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** Enumeration differs from scanning because it:

- A. Only sends ICMP pings
- B. Cracks passwords offline
- C. Is always passive
- D. Actively queries services to extract names — users, shares, groups, configs

<details><summary>Answer</summary>

**D.** Scanning finds open ports/services; **enumeration** establishes active connections to those services to pull out *named* resources (users, shares, groups, machine names). "Scanning finds the door; enumeration reads the nameplate."
</details>

---

**Q2.** Which ports are most associated with **SMB/NetBIOS** enumeration?

- A. 22 and 23
- B. 80 and 443
- C. 137–139 and 445
- D. 161 and 162

<details><summary>Answer</summary>

**C. 137–139 (NetBIOS) and 445 (SMB over TCP).** These are the classic Windows file-sharing enumeration targets (shares, users, sessions).
</details>

---

**Q3.** An **SNMP** enumeration succeeds against a device still using default community strings. Which strings are the usual defaults?

- A. admin / root
- B. guest / anonymous
- C. public (read) and private (read-write)
- D. sa / system

<details><summary>Answer</summary>

**C. `public` and `private`.** SNMP v1/2c send these community strings in cleartext; `private` typically grants write access. **SNMPv3** adds authentication and encryption and is the fix.
</details>

---

**Q4.** What is a **null session**?

- A. A TLS session with no cipher
- B. An unauthenticated SMB/IPC$ connection that can leak users/shares on legacy systems
- C. A DNS query with no answer
- D. An expired Kerberos ticket

<details><summary>Answer</summary>

**B.** A null session connects to `IPC$` with no username/password; on older/misconfigured Windows it exposes users, groups, and shares. Modern systems restrict it — but it's a classic enumeration technique.
</details>

---

**Q5.** Which SMTP command is used to **verify whether a mailbox/user exists**?

- A. HELO
- B. QUIT
- C. DATA
- D. VRFY

<details><summary>Answer</summary>

**D. `VRFY`** (and `EXPN` for lists) asks the mail server to confirm a user — useful for username enumeration when not disabled. `RCPT TO` can serve the same purpose.
</details>

---

**Q6.** Which protocol/port would you enumerate to pull directory objects like users and OUs from Active Directory?

- A. LDAP (389) / LDAPS (636)
- B. NTP (123)
- C. SNMP (161)
- D. TFTP (69)

<details><summary>Answer</summary>

**A. LDAP 389 (LDAPS 636).** LDAP is the query protocol for directory data; anonymous or authenticated binds can enumerate users, groups, and OUs. Restrict anonymous binds to limit this.
</details>

---

**Q7.** `enum4linux` primarily targets which service family?

- A. HTTP web apps
- B. SMB/NetBIOS/RPC on Windows/Samba
- C. SNMP devices
- D. Kerberos KDCs

<details><summary>Answer</summary>

**B.** `enum4linux` wraps SMB/NetBIOS/RPC tools (rpcclient, net, nmblookup) to enumerate users, shares, groups, and password policy from Windows/Samba hosts.
</details>

---

**Q8.** **RID cycling** is a technique to:

- A. Rotate encryption keys
- B. Crack NTLM hashes
- C. Enumerate domain accounts by iterating relative identifiers appended to the domain SID
- D. Flood a switch's CAM table

<details><summary>Answer</summary>

**C.** Each account's SID = domain SID + a **RID**. Iterating RIDs (e.g., 500, 501, 1000…) resolves account names even without a full user list — a common enumeration trick.
</details>

---

**Q9.** Which tool queries **SNMP** to walk a device's MIB?

- A. snmpwalk
- B. smbclient
- C. ldapsearch
- D. dig

<details><summary>Answer</summary>

**A. `snmpwalk`** traverses the SNMP MIB (e.g., `snmpwalk -v2c -c public <ip>`), pulling system, interface, and sometimes user/route data. `smbclient` is SMB, `ldapsearch` is LDAP, `dig` is DNS.
</details>

---

**Q10.** Which account RID is the built-in **Administrator** in Windows?

- A. 0
- B. 500
- C. 1000
- D. 512

<details><summary>Answer</summary>

**B. 500.** The built-in Administrator always has RID 500 (regardless of rename); RID 501 is Guest; 512 is the Domain Admins *group* RID; regular users start around 1000. Handy during RID cycling.
</details>

---

**Q11.** The **best** mitigation against SNMP enumeration is:

- A. Block ICMP
- B. Rename the community string to "public2"
- C. Use SNMPv3 with authentication + encryption (and drop v1/2c)
- D. Disable DNS

<details><summary>Answer</summary>

**C.** SNMPv3 adds auth + privacy; v1/2c community strings are cleartext and guessable. Renaming to another guessable string (B) is security by obscurity.
</details>

---

**Q12.** From a PAM perspective, the highest-value response to enumeration that reveals local admins and service accounts is:

- A. Ignore it — enumeration is harmless
- B. Disable LDAP entirely
- C. Rename the accounts
- D. Onboard those accounts to a vault with rotation (unique local admin per host, gMSA/rotated service accounts)

<details><summary>Answer</summary>

**D.** Enumeration's value is the *reuse* of what it finds. Vaulting + rotating local admins (LAPS-style) and service accounts (gMSA/CPM) removes the payoff — a discovered account is no longer a usable one.
</details>

---

**Q13.** Which service on **123/UDP** can be enumerated for host lists and time-sync relationships?

- A. NTP
- B. SMTP
- C. SNMP
- D. LDAP

<details><summary>Answer</summary>

**A. NTP (123/UDP).** NTP enumeration (e.g., `ntpq`, `ntpdc` monlist on old servers) can reveal connected hosts — and monlist is also a DDoS amplification vector (Module 10).
</details>

---

### Score yourself
- **11–13:** strong — memorize the port↔service and RID facts in [facts.md](facts.md).
- **8–10:** re-drill SNMP versions, null sessions, and SMTP verbs.
- **< 8:** redo the [lab-walkthrough.md](lab-walkthrough.md) with enum4linux/snmpwalk.
