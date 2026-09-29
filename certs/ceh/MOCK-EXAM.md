# CEH v13 — Mixed Final Mock Exam

> **50 original, concept-based questions** drawn across **all 20 modules**, in mixed order — the way the real exam presents them. Not a dump. The **answer key** (with one-line rationale + module reference) is at the bottom — take the test *first*, then score.

> ❓ **Also:** the concept track's [practice questions](exam-prep/practice-questions.md) (by module, with explanations).

## How to take it
- **Time-box it:** the real exam is ~1.9 min/question, so give yourself **~95 minutes** for these 50. Practice the pace.
- **First pass fast, flag the hard ones, second pass on flags** — and never leave a blank (no penalty for guessing).
- Watch qualifiers: **BEST, MOST, FIRST, NOT, EXCEPT.**
- Score with the [scoring guide](#scoring-guide). Log every miss in [PROGRESS.md](PROGRESS.md) and re-drill that module's [`facts.md`](modules/README.md) + [`flashcards.csv`](modules/README.md).
- Tactics reference: [EXAM-STRATEGY.md](EXAM-STRATEGY.md). Term lookups: [GLOSSARY.md](GLOSSARY.md).

---

## Questions

**1.** An attacker reuses a captured NTLM hash to authenticate to a file share without ever recovering the plaintext. This is:
- A. Kerberoasting  B. Offline brute force  C. AS-REP roasting  D. Pass-the-Hash

**2.** Which reconnaissance activity is **passive** (no packets sent to the target)?
- A. WHOIS + Shodan lookups  B. DNS zone transfer against the target's NS  C. Nmap SYN scan  D. Banner grabbing with netcat

**3.** On a Linux target, a `-sX` (XMAS) scan to an **open** port typically returns:
- A. RST  B. SYN/ACK  C. No response  D. ICMP unreachable

**4.** The **best** single defense against SQL injection is:
- A. A WAF  B. Blocklisting the word SELECT  C. Parameterized queries / prepared statements  D. Renaming tables

**5.** Which cipher mode leaks structure because identical plaintext blocks encrypt identically?
- A. GCM  B. CBC  C. CTR  D. ECB

**6.** MAC flooding a switch causes it to:
- A. Reboot  B. Fail open and behave like a hub  C. Block all ports  D. Enable port security

**7.** A worm differs from a virus in that it:
- A. Self-propagates over the network with no user action  B. Requires a host file  C. Cannot spread  D. Only runs in memory

**8.** Kerberoasting cracks the password of:
- A. The user running the attack  B. The krbtgt account  C. A service account with an SPN  D. The domain controller machine account

**9.** In the shared responsibility model, which layer does the **customer always** own, in every service model?
- A. Physical hardware  B. Hypervisor  C. Data and identities  D. Managed-service internals

**10.** SSRF is dangerous in cloud because it can reach:
- A. The public DNS root  B. The instance metadata service at 169.254.169.254  C. The user's browser cache  D. The TLS handshake

**11.** Which control most directly defeats Kerberoasting?
- A. Account lockout  B. gMSA (auto-rotated 128-char service password)  C. BitLocker  D. Disabling SMBv1

**12.** A `SLEEP(5)`-based delay confirms which SQLi type?
- A. UNION-based  B. Error-based  C. Time-based blind  D. Out-of-band

**13.** CSRF and SSRF differ in that:
- A. Both trick the server  B. CSRF tricks the browser; SSRF tricks the server  C. CSRF tricks the server; SSRF tricks the browser  D. They are identical

**14.** The WPA2 4-way handshake is captured primarily to:
- A. Decrypt live traffic instantly  B. Brute-force the PSK offline  C. Deauthenticate clients  D. Crack WPS

**15.** Which nmap flag set is **loudest / most likely to trigger an IDS**?
- A. `-sn`  B. `-sS -T1`  C. `-A -T4`  D. `-sL`

**16.** A digital signature provides all of these **except**:
- A. Integrity  B. Authenticity  C. Non-repudiation  D. Confidentiality

**17.** DCSync abuses which right to pull hashes from a DC without running code on it?
- A. AD replication rights  B. SeDebugPrivilege  C. Local admin on the workstation  D. DNS admin

**18.** Which is a **volumetric/reflection** DDoS technique?
- A. Slowloris  B. SYN flood  C. DNS/NTP/memcached amplification  D. Ping of Death

**19.** IDOR (accessing `?id=1002` to read another user's record) is which OWASP 2021 category?
- A. A01 Broken Access Control  B. A03 Injection  C. A07 Auth Failures  D. A10 SSRF

**20.** Which MITRE ATT&CK term describes *the attacker's goal* (the "why")?
- A. Technique  B. Mitigation  C. Procedure  D. Tactic

**21.** Stored XSS differs from reflected XSS because it:
- A. Never executes  B. Only affects the DOM  C. Requires the victim to click a crafted link  D. Is saved server-side and runs for every viewer

**22.** SNMP v1/2c is insecure primarily because:
- A. Community strings (public/private) are sent in cleartext  B. It uses TCP  C. It requires certificates  D. It only runs on Windows

**23.** Which mitigation counters **ARP poisoning**?
- A. Port security  B. DHCP snooping  C. Dynamic ARP Inspection (DAI)  D. SYN cookies

**24.** A Golden ticket is forged using the hash of:
- A. A service account  B. The current user  C. The local Administrator  D. The krbtgt account

**25.** Which tool is an **open-source** vulnerability scanner?
- A. OpenVAS / Greenbone  B. Nessus  C. Cobalt Strike  D. Burp Suite Pro

**26.** To send a message only the recipient can read, encrypt it with:
- A. Your private key  B. Your public key  C. The recipient's public key  D. The recipient's private key

**27.** Rooting (Android) and jailbreaking (iOS) both:
- A. Improve battery life  B. Remove the vendor's sandbox / code-signing restrictions  C. Encrypt the device  D. Enable MDM

**28.** Which OT protocol runs on **port 502** and typically has no authentication?
- A. DNP3  B. BACnet  C. S7comm  D. Modbus

**29.** The **primary** reason ARP poisoning works is:
- A. ARP is encrypted  B. ARP uses TCP  C. Switches disable ARP  D. ARP has no authentication

**30.** Which nmap scan needs **no root privilege**?
- A. `-sS`  B. `-sX`  C. `-sF`  D. `-sT`

**31.** A padding-oracle attack targets which mode?
- A. ECB  B. CBC  C. GCM  D. CTR

**32.** LLMNR/NBT-NS poisoning with Responder yields a hash you crack with Hashcat mode:
- A. 1000  B. 13100  C. 5600  D. 22000

**33.** MQTT vs CoAP: the correct pairing is:
- A. MQTT = pub/sub over TCP; CoAP = REST over UDP  B. MQTT = REST over UDP; CoAP = pub/sub over TCP  C. Both over TCP  D. Both over UDP

**34.** Which control gives each host a **unique, rotated local-admin password**?
- A. AppLocker  B. LAPS  C. Kerberos armoring  D. LLMNR

**35.** A honeypot that fully emulates services to deeply engage an attacker is:
- A. Low-interaction  B. A tarpit  C. A production honeypot only  D. High-interaction

**36.** The best countermeasure to SMS-OTP interception / SIM swapping is:
- A. Longer SMS codes  B. Security questions  C. Emailing the OTP  D. Phishing-resistant MFA (FIDO2/passkeys)

**37.** In TLS, asymmetric crypto is used to ___ and symmetric to ___:
- A. encrypt bulk data; exchange keys  B. pad; hash  C. sign; compress  D. exchange/agree a session key; encrypt bulk data

**38.** Which is a **fileless / living-off-the-land** technique?
- A. Encoded PowerShell run via a signed system binary  B. Dropping an EXE to disk  C. Formatting the disk  D. A boot-sector virus

**39.** An `iam:PassRole` abuse in AWS is an example of:
- A. Container escape  B. IAM privilege escalation  C. A public bucket  D. SSRF

**40.** Which scan best maps **firewall rules** (filtered vs unfiltered) rather than open/closed?
- A. `-sA` (ACK)  B. `-sS`  C. `-sV`  D. `-O`

**41.** Session fixation is prevented primarily by:
- A. Issuing a **new** session ID upon authentication  B. Longer passwords  C. Disabling cookies entirely  D. Using HTTP instead of HTTPS

**42.** Which password-storage choice is correct?
- A. MD5  B. SHA-256  C. Argon2 / bcrypt / scrypt / PBKDF2  D. Base64

**43.** The Purdue model's **IDMZ (Level 3.5)** exists to:
- A. Run PLCs  B. Separate/broker traffic between IT and OT zones  C. Host the enterprise email  D. Store historian backups only

**44.** Which is an **insertion** attack against an IDS?
- A. Flooding the IDS to fail open  B. Getting the IDS to accept a packet the end host rejects  C. Encrypting all traffic  D. Disabling the firewall

**45.** A MITM on an **unauthenticated** Diffie-Hellman exchange is possible because DH:
- A. Provides no authentication of the parties by itself  B. Is symmetric  C. Uses RSA keys  D. Cannot be intercepted

**46.** Which best reduces the impact of **LSASS credential dumping**?
- A. Credential Guard + LSASS PPL + EDR/ASR  B. Longer usernames  C. Disabling IPv6  D. Enabling LLMNR

**47.** Enumeration differs from scanning in that it:
- A. Only pings hosts  B. Cracks hashes  C. Is always passive  D. Actively queries services to extract names (users, shares, groups)

**48.** Which vulnerability-scan type produces the most accurate, lowest-false-positive results?
- A. Unauthenticated external  B. Passive-only  C. Authenticated / credentialed  D. Ping sweep

**49.** Which pairing of email-security tech to trust model is correct?
- A. PGP → web of trust; S/MIME → X.509 CA  B. PGP → CA hierarchy; S/MIME → web of trust  C. both CA hierarchy  D. both web of trust

**50.** From a PAM standpoint, the single highest-value control against most malware persistence and privilege escalation is:
- A. A longer screensaver timeout  B. Removing standing local-admin rights (least privilege)  C. Renaming the Administrator account  D. Disabling the firewall log

---

## Answer key

> Score first, then read the rationale for any you missed and revisit that module.

| Q | Ans | Why (module) |
|---|---|---|
| 1 | D | Hash used directly, no cracking = Pass-the-Hash (M06) |
| 2 | A | WHOIS/Shodan query third parties, not the target (M02) |
| 3 | C | Open port stays silent to XMAS; closed sends RST (M03) |
| 4 | C | Parameterized queries separate code from data (M15) |
| 5 | D | ECB — the "penguin" mode (M20) |
| 6 | B | CAM overflow → switch fails open like a hub (M08) |
| 7 | A | Worm self-propagates over the network (M07) |
| 8 | C | TGS is encrypted with the service account key (M06) |
| 9 | C | You always own data + identities (M19) |
| 10 | B | SSRF → 169.254.169.254 steals role creds (M14/M19) |
| 11 | B | gMSA removes the crackable service password (M06) |
| 12 | C | Time delay = time-based blind SQLi (M15) |
| 13 | B | CSRF tricks the browser; SSRF tricks the server (M14) |
| 14 | B | Captured handshake → offline PSK crack (M16) |
| 15 | C | `-A -T4` is loud (version+OS+scripts+traceroute) (M03/M12) |
| 16 | D | Signatures give integrity/authenticity/non-repudiation, not confidentiality (M20) |
| 17 | A | DCSync abuses replication rights (M06) |
| 18 | C | Amplification/reflection is volumetric (M10) |
| 19 | A | IDOR = Broken Access Control, A01 (M14) |
| 20 | D | Tactic = the goal; technique = the how (M01) |
| 21 | D | Stored XSS persists and runs for every viewer (M14) |
| 22 | A | v1/2c community strings are cleartext (M04/M08) |
| 23 | C | Dynamic ARP Inspection counters ARP poisoning (M08) |
| 24 | D | Golden ticket = forged TGT signed with krbtgt (M06) |
| 25 | A | OpenVAS/Greenbone is open source (M05) |
| 26 | C | Encrypt with the recipient's public key (M20) |
| 27 | B | Both remove the sandbox/code-signing trust model (M17) |
| 28 | D | Modbus, port 502, no auth by design (M18) |
| 29 | D | ARP has no authentication (M08) |
| 30 | D | `-sT` uses connect(), no root needed (M03) |
| 31 | B | Padding oracle targets CBC (M20) |
| 32 | C | NetNTLMv2 = Hashcat -m 5600 (M08) |
| 33 | A | MQTT = pub/sub over TCP; CoAP = REST over UDP (M18) |
| 34 | B | LAPS = unique rotated local admin per host (M06) |
| 35 | D | High-interaction honeypot fully emulates services (M12) |
| 36 | D | Phishing-resistant MFA beats SMS OTP (M17/M09) |
| 37 | D | TLS hybrid: asymmetric key exchange + symmetric bulk (M20) |
| 38 | A | Encoded PowerShell via a LOLBin = fileless (M07) |
| 39 | B | iam:PassRole abuse = IAM privilege escalation (M19) |
| 40 | A | ACK scan maps filtered vs unfiltered (M03) |
| 41 | A | Reissue the session ID at login (M11) |
| 42 | C | Slow, salted KDFs for passwords (M20/M15) |
| 43 | B | IDMZ brokers IT↔OT traffic (M18) |
| 44 | B | Insertion = IDS accepts a packet the host rejects (M12) |
| 45 | A | DH alone doesn't authenticate the parties (M20) |
| 46 | A | Credential Guard + LSASS PPL + EDR/ASR (M06) |
| 47 | D | Enumeration extracts named resources (M04) |
| 48 | C | Credentialed scans are most accurate (M05) |
| 49 | A | PGP = web of trust; S/MIME = X.509 CA (M20) |
| 50 | B | Remove standing local admin — least privilege (M07/M06/defender-pam) |

---

## Scoring guide

| Score | Read |
|---|---|
| **45–50 (90%+)** | Exam-ready on breadth. Do a timed full-length set and book. |
| **40–44 (80–88%)** | Solid. Re-drill the 2–3 weakest modules' `facts.md` + flashcards. |
| **33–39 (66–78%)** | Around the cut line — study the missed modules' guides and redo their labs before booking. |
| **< 33 (<66%)** | Keep working the module loop; re-take after another pass through the weak areas. |

> This is one 50-question checkpoint, not a predictor of your exact 125-question form. Confirm readiness against official EC-Council practice and the guidance in [EXAM-LOGISTICS.md](EXAM-LOGISTICS.md).
