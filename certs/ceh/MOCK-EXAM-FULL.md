# CEH v13 — Full-Length Mock Exam (125 questions)

> **125 original, concept-based questions** across **all 20 modules**, in mixed order — matching the real exam's length and format. Not a dump. The **answer key** (letter + one-line rationale + module) is at the bottom: take it under exam conditions first, then score.

## How to take it
- **Full exam simulation:** **240 minutes** for 125 questions (~1.9 min each). Sit it in one timed block, no notes.
- **First pass fast, flag the hard ones, second pass on flags** — never leave a blank (no penalty for guessing).
- Watch qualifiers: **BEST, MOST, FIRST, NOT, EXCEPT.**
- Score with the [scoring guide](#scoring-guide); the real cut score is variable (~60–85%). Log misses in [PROGRESS.md](PROGRESS.md).
- Shorter checkpoint: [MOCK-EXAM.md](MOCK-EXAM.md) (50 Q). Tactics: [EXAM-STRATEGY.md](EXAM-STRATEGY.md). Terms: [GLOSSARY.md](GLOSSARY.md).

---

## Questions

**1.** Which element of the CIA triad does ransomware most directly attack?
- A. Confidentiality  B. Integrity  C. Availability  D. Non-repudiation

**2.** A tester is given no prior knowledge of the target's internals. This engagement is:
- A. White-box  B. Grey-box  C. Black-box  D. Crystal-box

**3.** Which is a **passive** footprinting activity?
- A. Nmap version scan  B. Traceroute to the target  C. DNS zone transfer  D. Reviewing the target's public LinkedIn and job posts

**4.** A DNS **SRV** record is most useful to an attacker because it:
- A. Lists mail servers  B. Stores SPF data  C. Locates services such as LDAP/Kerberos (finding domain controllers)  D. Maps IP to hostname

**5.** On a Linux host, a SYN scan to a **filtered** port typically results in:
- A. SYN/ACK  B. RST  C. No response (or ICMP unreachable)  D. FIN

**6.** Which nmap option performs OS fingerprinting?
- A. `-sV`  B. `-sn`  C. `-O`  D. `-p-`

**7.** SNMP enumeration succeeds because a device uses the default read community string:
- A. admin  B. public  C. root  D. cisco

**8.** The built-in Windows Administrator account always has which RID?
- A. 501  B. 512  C. 500  D. 1000

**9.** A credentialed vulnerability scan is preferred because it:
- A. Runs without touching the host  B. Only checks open ports  C. Reveals missing patches/configs with fewer false positives  D. Is faster than a ping sweep

**10.** A CVSS base score of 4.5 (v3) is which severity?
- A. Low  B. Medium  C. High  D. Critical

**11.** Pass-the-Hash is possible against NTLM because NTLM hashes are:
- A. Salted  B. Encrypted with the user's password  C. Unsalted and usable directly for authentication  D. One-time values

**12.** Which attack requires **offline cracking** to succeed?
- A. Kerberoasting  B. Pass-the-Ticket  C. Pass-the-Hash  D. Overpass-the-Hash (using an existing hash to get a TGT)

**13.** A worm's defining characteristic is that it:
- A. Needs a host file  B. Cannot propagate  C. Requires the user to open it  D. Self-replicates across the network without user action

**14.** Which malware component fetches additional stages from the internet?
- A. Dropper  B. Payload  C. Packer  D. Downloader

**15.** Wireshark **display filters** differ from capture filters in that display filters:
- A. Use BPF syntax  B. Are applied after capture to shown packets (e.g., `http.request`)  C. Cannot filter by protocol  D. Only work on UDP

**16.** MAC flooding forces a switch to:
- A. Reboot  B. Drop all frames  C. Enable DAI  D. Behave like a hub (fail open)

**17.** Which social-engineering attack uses SMS as the delivery channel?
- A. Vishing  B. Smishing  C. Whaling  D. Pharming

**18.** In a SYN flood, the attacker exhausts the target by:
- A. Sending SYNs and never completing the handshake (half-open connections)  B. Completing many handshakes  C. Flooding ICMP  D. Sending oversized packets

**19.** Application-level session hijacking most commonly steals:
- A. A TCP sequence number  B. A session cookie/token  C. An ARP entry  D. A DNS record

**20.** An **insertion** attack against an IDS works by:
- A. Flooding the IDS  B. Encrypting traffic  C. Making the IDS accept a packet the end host will reject  D. Disabling logging

**21.** Directory traversal against a web server uses sequences like:
- A. `../../`  B. `UNION SELECT`  C. `<script>`  D. `; whoami`

**22.** Which is a **stored** XSS scenario?
- A. A crafted link echoes input back once  B. A comment saved in the DB executes for every viewer  C. Client-side JS uses `location.hash`  D. A GET parameter reflected in an error

**23.** The best fix for SQL injection is:
- A. A WAF  B. Escaping quotes only  C. Parameterized queries / prepared statements  D. Hiding SQL errors

**24.** The WPA2 four-way handshake lets an attacker:
- A. Decrypt all traffic live  B. Capture material to brute-force the PSK offline  C. Bypass MAC filtering  D. Disable WPS

**25.** Rooting an Android device primarily:
- A. Improves battery  B. Installs MDM  C. Encrypts storage  D. Removes the app sandbox / privilege restrictions

**26.** MQTT operates as:
- A. REST over UDP  B. A file-transfer protocol  C. Publish/subscribe over TCP  D. A routing protocol

**27.** The Purdue model's IDMZ (Level 3.5) exists to:
- A. Run PLCs  B. Store backups  C. Host email  D. Broker/segment traffic between IT and OT

**28.** An SSRF that reaches `169.254.169.254` in AWS can steal:
- A. Temporary instance-role credentials  B. The root password  C. The TLS private key  D. The bucket ACL

**29.** Which is the correct email-security trust-model pairing?
- A. PGP → CA hierarchy; S/MIME → web of trust  B. PGP → web of trust; S/MIME → X.509 CA  C. Both CA hierarchy  D. Both web of trust

**30.** Encrypting a file so only Bob can read it requires:
- A. Bob's public key  B. Bob's private key  C. Your private key  D. A shared symmetric key sent in the clear

**31.** MITRE ATT&CK "tactics" represent:
- A. Specific tools  B. The adversary's goal (the why)  C. A CVE  D. A patch

**32.** Which is **not** a phase of the classic hacking methodology?
- A. Reconnaissance  B. Scanning  C. Compilation  D. Maintaining Access

**33.** `theHarvester` is used to:
- A. Crack hashes  B. Scan ports  C. Gather emails/subdomains/hosts from public sources  D. Poison ARP

**34.** Which nmap scan needs no root/admin privilege?
- A. `-sT`  B. `-sS`  C. `-sN`  D. `-sX`

**35.** A null session abuses which service to enumerate users/shares?
- A. HTTP  B. NTP  C. SNMP  D. SMB/IPC$

**36.** Which describes a **false negative** in vulnerability scanning?
- A. Missing a vulnerability that is actually present  B. Flagging a vuln that isn't there  C. A duplicate finding  D. A network timeout

**37.** Kerberoasting yields a crackable ticket because the TGS is encrypted with:
- A. The krbtgt hash  B. The requesting user's password  C. The target service account's key  D. The DC's machine key

**38.** Which control best defeats local-admin hash reuse across many hosts?
- A. AppLocker  B. LAPS  C. LLMNR  D. SMB null sessions

**39.** A rootkit that loads before the OS by infecting the bootloader is a:
- A. User-mode rootkit  B. Application rootkit  C. Library rootkit  D. Bootkit

**40.** Which is a fileless / living-off-the-land technique?
- A. Dropping `evil.exe`  B. A macro that writes an EXE  C. A boot-sector virus  D. Base64-encoded PowerShell executed via a signed binary

**41.** Responder poisons which protocols to capture NetNTLM hashes?
- A. HTTP/HTTPS  B. RDP  C. SSH  D. LLMNR/NBT-NS/mDNS

**42.** Which switch feature counters ARP poisoning?
- A. Port security  B. DHCP snooping  C. Dynamic ARP Inspection  D. STP

**43.** A pretexting attack relies on:
- A. A fabricated scenario to gain trust and extract info  B. Malware  C. A buffer overflow  D. Port scanning

**44.** Tailgating differs from piggybacking in that tailgating implies:
- A. The authorized person knowingly lets you in  B. Following in without the authorized person's awareness/consent  C. Using a stolen badge  D. A phishing email

**45.** Which DDoS category does an HTTP GET/POST flood belong to?
- A. Volumetric  B. Protocol  C. Application-layer  D. Reflection

**46.** DNS amplification is effective because:
- A. DNS uses TCP with handshakes  B. Small spoofed UDP queries yield large responses to the victim  C. DNS is encrypted  D. It requires no spoofing

**47.** Session fixation is prevented by:
- A. Longer passwords  B. Issuing a new session ID upon login  C. Disabling HTTPS  D. Using GET for logins

**48.** Which cookie flag prevents JavaScript from reading a session cookie?
- A. Secure  B. Domain  C. SameSite  D. HttpOnly

**49.** A honeypot that fully emulates an OS and services to deeply engage attackers is:
- A. High-interaction  B. Low-interaction  C. A tarpit  D. A sinkhole

**50.** Which nmap technique hides your real source among fakes?
- A. `-sV`  B. `-p-`  C. `-O`  D. `-D` decoys

**51.** IDOR is fundamentally a failure of:
- A. Encryption  B. Authorization (access control)  C. Input encoding  D. Rate limiting

**52.** Which OWASP 2021 category covers SSRF?
- A. A01  B. A03  C. A07  D. A10

**53.** Command injection is confirmed when input like `; id` causes the server to:
- A. Return a 404  B. Execute an OS command  C. Redirect  D. Log out

**54.** In MSSQL, which feature can turn SQLi into OS command execution?
- A. `INTO OUTFILE`  B. `xp_cmdshell`  C. `information_schema`  D. `LOAD_FILE`

**55.** A blind SQLi that changes page content on true/false conditions is:
- A. Error-based  B. UNION-based  C. Boolean-based blind  D. Out-of-band

**56.** WEP is broken chiefly because of:
- A. AES weakness  B. Weak/repeating IVs with RC4  C. SAE  D. 802.11w

**57.** An evil twin attack is:
- A. A rogue AP impersonating a legitimate SSID  B. Two APs with different SSIDs  C. A deauth flood  D. A WPS brute force

**58.** WPA3 resists offline PSK cracking primarily via:
- A. TKIP  B. WEP IVs  C. SAE (Dragonfly) handshake  D. MAC filtering

**59.** On iOS, jailbreaking removes:
- A. The battery limit  B. MDM enrollment  C. The SIM lock only  D. Sandbox and code-signing restrictions

**60.** Insecure data storage on mobile means secrets sit in:
- A. The Secure Enclave  B. Encrypted Keychain  C. SharedPreferences/plist/SQLite/logs in cleartext  D. A remote HSM

**61.** Mirai spread mainly by:
- A. Trying default Telnet credentials on IoT devices  B. Exploiting a browser 0-day  C. Phishing emails  D. SQL injection

**62.** Which OT protocol runs on TCP port 502?
- A. DNP3  B. BACnet  C. S7comm  D. Modbus

**63.** In Kubernetes, which component stores secrets and, if exposed unauthenticated, means full compromise?
- A. kubelet  B. the dashboard  C. kube-proxy  D. etcd

**64.** IMDSv2 mitigates SSRF credential theft by:
- A. Encrypting the disk  B. Requiring a session token (PUT) and honoring a hop limit  C. Blocking all metadata  D. Rotating the instance ID

**65.** A padding-oracle attack specifically targets:
- A. ECB  B. CTR  C. GCM  D. CBC

**66.** Passwords should be stored with:
- A. MD5  B. SHA-256  C. Argon2/bcrypt/scrypt/PBKDF2  D. ROT13

**67.** Which algorithm performs key exchange only?
- A. RSA  B. AES  C. Diffie-Hellman  D. DSA

**68.** A digital signature does **not** provide:
- A. Integrity  B. Authenticity  C. Confidentiality  D. Non-repudiation

**69.** Which best describes defense-in-depth?
- A. A single strong firewall  B. Multiple layered controls so one failure isn't fatal  C. Encrypting one server  D. Disabling logging

**70.** During which phase does an attacker clear event logs?
- A. Reconnaissance  B. Scanning  C. Gaining Access  D. Covering Tracks / Maintaining Access

**71.** A hacktivist is best defined by:
- A. A political/social cause  B. Financial motive  C. Nation-state backing  D. Curiosity only

**72.** Which Google dork finds exposed spreadsheets on a domain?
- A. `related:`  B. `site:example.com filetype:xlsx`  C. `cache:`  D. `link:`

**73.** An ACK scan (`-sA`) is used mainly to:
- A. Detect service versions  B. Determine filtered vs unfiltered (firewall mapping)  C. Crack passwords  D. Find subdomains

**74.** `enum4linux` targets which family of services?
- A. SMB/NetBIOS/RPC  B. SNMP only  C. HTTP  D. Kerberos

**75.** Which standard names the *type* of weakness (e.g., CWE-79 for XSS)?
- A. CVE  B. CVSS  C. CWE  D. CPE

**76.** DCSync is detected by which pattern?
- A. Many 4625 failures  B. Replication (4662) requested by a non-DC account  C. A single 4624 logon  D. DNS AXFR

**77.** LSASS memory is targeted to extract:
- A. Disk encryption keys only  B. Logged-on credentials and Kerberos tickets  C. Browser history  D. Firewall rules

**78.** A trojan differs from a virus because a trojan:
- A. Self-replicates  B. Only infects boot sectors  C. Needs no user action  D. Poses as legitimate software the user installs

**79.** Which protocol swap removes cleartext credential sniffing for remote admin?
- A. Telnet → SSH  B. Telnet → FTP  C. HTTP → HTTP/2  D. SNMPv2c → SNMPv1

**80.** Business Email Compromise (BEC) is best mitigated by:
- A. Out-of-band verification of payment/detail changes  B. Antivirus  C. A faster mail server  D. Longer passwords

**81.** Which is a **protocol** DoS attack?
- A. HTTP flood  B. Slowloris  C. DNS amplification  D. SYN flood

**82.** TCP sequence-number prediction enables:
- A. A UDP flood  B. Network-level session hijacking  C. XSS  D. Phishing

**83.** A firewall that inspects and remembers connection state is a:
- A. Packet filter (stateless)  B. Stateful firewall  C. Proxy only  D. Hub

**84.** Uploading `shell.php` to a poorly validated upload form yields:
- A. A CSRF token  B. A DoS  C. An SSRF  D. A web shell → remote code execution

**85.** CSRF is best mitigated by:
- A. Anti-CSRF tokens + SameSite cookies  B. Input encoding  C. Rate limiting only  D. Disabling cookies

**86.** sqlmap flag to test whether the DB account is a DBA:
- A. `--dbs`  B. `--tables`  C. `--batch`  D. `--is-dba`

**87.** A deauthentication attack is used to:
- A. Crack WEP instantly  B. Force clients to reconnect so the handshake can be captured  C. Disable WPS  D. Spoof a MAC

**88.** Which mobile analysis is **static**?
- A. Decompiling the APK with jadx and reading the manifest  B. Running the app and hooking with Frida  C. Capturing live API calls  D. Fuzzing at runtime

**89.** CoAP is best described as:
- A. Pub/sub over TCP  B. A routing protocol  C. A serial protocol  D. RESTful over UDP for constrained devices

**90.** A misconfigured public S3 bucket is an example of OWASP/cloud:
- A. Security misconfiguration / broken access to storage  B. Injection  C. SSRF  D. Cryptographic failure

**91.** ECC is favored on mobile/IoT because it offers:
- A. Larger keys for the same strength  B. Symmetric speed  C. No key at all  D. Equivalent strength with smaller keys (less compute)

**92.** Which mode provides authenticated encryption (confidentiality + integrity)?
- A. ECB  B. CBC  C. GCM  D. CTR

**93.** A zero-day is a vulnerability that:
- A. Is fully patched  B. Only affects hardware  C. Has no available patch and is unknown to the vendor  D. Is a false positive

**94.** Which is the **first** thing to establish before any authorized test?
- A. The exploit  B. The report template  C. Written authorization / scope (Rules of Engagement)  D. The payload

**95.** Website mirroring (e.g., HTTrack) supports footprinting by:
- A. Creating an offline copy to analyze without hitting the live site  B. Cracking logins  C. Poisoning DNS  D. Flooding the server

**96.** A masscan is chosen over nmap when you need:
- A. Deep NSE scripting  B. Very fast, internet-scale port sweeps  C. OS fingerprinting  D. Version detection

**97.** LDAP anonymous binds can leak:
- A. Directory objects (users, groups, OUs)  B. Encryption keys  C. Firewall rules  D. Disk contents

**98.** A CVSS **environmental** metric adjusts the score based on:
- A. Global averages  B. The vendor's name  C. The exploit author  D. The specific organization's context/impact

**99.** Overpass-the-Hash (pass-the-key) uses an NT hash to:
- A. Decrypt the disk  B. Poison ARP  C. Crack the password  D. Request a legitimate Kerberos TGT

**100.** Which best reduces the blast radius of any single compromised admin credential?
- A. A longer password  B. Antivirus  C. Tiered administration + JIT (no standing privilege)  D. Disabling IPv6

**101.** A polymorphic virus evades signatures by:
- A. Mutating its encrypted body with a changing decryptor  B. Rewriting its entire code each run  C. Hiding in slack space  D. Infecting the boot sector

**102.** Which capture confirms a cleartext credential leak?
- A. A TLS ClientHello  B. A DNS query  C. An encrypted SSH stream  D. An FTP `PASS` command visible in the packet bytes

**103.** Angler phishing specifically abuses:
- A. Fake customer-support accounts on social media  B. Phone calls  C. USB drops  D. QR codes only

**104.** A SYN cookie defends against:
- A. ARP poisoning  B. SYN floods  C. XSS  D. DNS poisoning

**105.** RST/FIN hijacking operates at which level?
- A. Network (TCP)  B. Application  C. Physical  D. Presentation

**106.** DNS tunneling is used to:
- A. Speed up DNS  B. Encrypt DNS  C. Exfiltrate data / C2 through an allowed protocol  D. Block queries

**107.** WebDAV misconfigured to allow `PUT` can let an attacker:
- A. Upload a web shell to the server  B. Only read files  C. Crash the DB  D. Sniff traffic

**108.** Which tool automates web-app request tampering via an intercepting proxy?
- A. Nikto  B. Nessus  C. Hydra  D. Burp Suite

**109.** Second-order SQL injection means the payload:
- A. Is stored and executed later by a different query  B. Executes immediately  C. Only works over HTTPS  D. Requires DBA

**110.** Which is a WPS weakness an attacker exploits?
- A. AES  B. The 8-digit PIN's brute-forceable design (Pixie-Dust)  C. SAE  D. 802.1X

**111.** MobSF is used to:
- A. Root a phone  B. Perform automated static + dynamic mobile app analysis  C. Flash firmware  D. Spoof GPS

**112.** In OT security, a unidirectional gateway (data diode) enforces:
- A. Two-way encrypted tunnels  B. Password rotation  C. Wireless meshing  D. Traffic flow in one direction only (e.g., OT → IT)

**113.** Container escape most often abuses:
- A. A privileged container / mounted docker.sock / excess capabilities  B. A read-only rootfs  C. Network policy  D. Pod Security Standards

**114.** Which cloud tool is an AWS **exploitation** framework?
- A. ScoutSuite  B. Prowler  C. Pacu  D. Trivy

**115.** A birthday attack finds a hash collision in roughly:
- A. 2^n  B. n log n  C. n²  D. 2^(n/2)

**116.** BitLocker commonly seals its key using:
- A. The TPM  B. A remote CA  C. A password only  D. A web of trust

**117.** Which is TRUE about TLS 1.3?
- A. It re-added RC4  B. It requires WEP  C. It removed all symmetric ciphers  D. It mandates forward secrecy (ephemeral DH) and removed RSA key transport

**118.** Steganography differs from cryptography because it:
- A. Hides the very existence of the message  B. Scrambles content  C. Is always stronger  D. Only works on text

**119.** The "principle of least privilege" means:
- A. Everyone is admin for convenience  B. No one can log in  C. Users/services get only the rights their role needs  D. All access is logged

**120.** Which detection signal most specifically indicates Kerberoasting?
- A. 4625 spikes  B. 4740 lockouts  C. 4769 TGS requests for SPN accounts using RC4  D. 1102 log cleared

**121.** A grey-hat hacker is one who:
- A. Always has authorization  B. Acts without clear authorization but not purely maliciously  C. Is always nation-state  D. Never uses tools

**122.** Which is the correct order in the vulnerability-management lifecycle?
- A. Assess → Risk-rank → Remediate → Verify → Monitor  B. Remediate → Assess → Monitor  C. Verify → Assess → Remediate  D. Monitor → Remediate → Assess

**123.** An attacker sends a crafted packet with a low TTL so the IDS sees it but the target never does. This is:
- A. An insertion attack  B. An evasion attack  C. A DoS  D. A honeypot

**124.** Which is the strongest answer to "how do we stop admin credentials being sniffed or keylogged?"
- A. Broker sessions so the credential is injected server-side and never touches the endpoint/wire  B. Longer passwords  C. Antivirus  D. Disable DNS

**125.** In PKI, the component that verifies an applicant's identity before a certificate is issued is the:
- A. RA  B. CA  C. CRL  D. OCSP responder

---

## Answer key

> Score first, then study the rationale for each miss and revisit that module.

| Q | Ans | Why (module) | Q | Ans | Why (module) |
|---|---|---|---|---|---|
| 1 | C | Ransomware denies access (M20/M07) | 64 | B | IMDSv2 token + hop limit (M19) |
| 2 | C | No prior knowledge = black-box (M01) | 65 | D | Padding oracle → CBC (M20) |
| 3 | D | Public profiles = passive OSINT (M02) | 66 | C | Slow salted KDFs (M20) |
| 4 | C | SRV locates LDAP/Kerberos = DCs (M02) | 67 | C | DH = key exchange only (M20) |
| 5 | C | Filtered = no response/ICMP (M03) | 68 | C | Signatures aren't confidentiality (M20) |
| 6 | C | `-O` = OS detection (M03) | 69 | B | Layered controls (M01) |
| 7 | B | Default read community = public (M04) | 70 | D | Log clearing = covering tracks (M06) |
| 8 | C | Administrator RID = 500 (M04) | 71 | A | Hacktivist = cause-driven (M01) |
| 9 | C | Credentialed = deeper, fewer FPs (M05) | 72 | B | filetype dork (M02) |
| 10 | B | 4.0–6.9 = Medium (M05) | 73 | B | ACK maps filtered/unfiltered (M03) |
| 11 | C | NTLM unsalted, hash reusable (M06) | 74 | A | enum4linux = SMB/NetBIOS/RPC (M04) |
| 12 | A | Kerberoasting cracks svc pwd (M06) | 75 | C | CWE = weakness type (M05) |
| 13 | D | Worm self-propagates (M07) | 76 | B | Replication from non-DC (M06) |
| 14 | D | Downloader fetches stages (M07) | 77 | B | LSASS holds creds/tickets (M06) |
| 15 | B | Display filters post-capture (M08) | 78 | D | Trojan = disguised, user-run (M07) |
| 16 | D | CAM overflow → fail open (M08) | 79 | A | Telnet → SSH (M08) |
| 17 | B | SMS phishing = smishing (M09) | 80 | A | Out-of-band verify (M09) |
| 18 | A | Half-open connections (M10) | 81 | D | SYN flood = protocol (M10) |
| 19 | B | Steal the session token (M11) | 82 | B | Seq prediction = net hijack (M11) |
| 20 | C | IDS accepts, host rejects (M12) | 83 | B | Stateful firewall (M12) |
| 21 | A | `../../` traversal (M13) | 84 | D | Upload → web shell = RCE (M13/M14) |
| 22 | B | Stored XSS runs for all (M14) | 85 | A | Anti-CSRF tokens + SameSite (M14) |
| 23 | C | Parameterized queries (M15) | 86 | D | `--is-dba` (M15) |
| 24 | B | Handshake → offline PSK crack (M16) | 87 | B | Deauth forces handshake (M16) |
| 25 | D | Rooting removes sandbox (M17) | 88 | A | jadx decompile = static (M17) |
| 26 | C | MQTT = pub/sub over TCP (M18) | 89 | D | CoAP = REST over UDP (M18) |
| 27 | D | IDMZ brokers IT↔OT (M18) | 90 | A | Public bucket = misconfig (M19) |
| 28 | A | Instance-role creds via IMDS (M19) | 91 | D | ECC = smaller keys (M20) |
| 29 | B | PGP=WoT, S/MIME=X.509 (M20) | 92 | C | GCM = authenticated (M20) |
| 30 | A | Recipient's public key (M20) | 93 | C | 0-day = no patch/unknown (M01) |
| 31 | B | Tactic = the goal (M01) | 94 | C | Authorization/scope first (M01) |
| 32 | C | "Compilation" isn't a phase (M01) | 95 | A | Offline mirror to analyze (M02) |
| 33 | C | theHarvester = OSINT (M02) | 96 | B | masscan = fast/scale (M03) |
| 34 | A | `-sT` needs no root (M03) | 97 | A | LDAP leaks directory objects (M04) |
| 35 | D | Null session via SMB/IPC$ (M04) | 98 | D | Environmental = org context (M05) |
| 36 | A | Missed real vuln = FN (M05) | 99 | D | Overpass-the-Hash → TGT (M06) |
| 37 | C | Encrypted with svc account key (M06) | 100 | C | Tiering + JIT (M06/dp) |
| 38 | B | LAPS = unique local admin (M06) | 101 | A | Polymorphic mutates encryption (M07) |
| 39 | D | Bootkit loads pre-OS (M07) | 102 | D | FTP PASS in cleartext (M08) |
| 40 | D | Encoded PS via signed binary (M07) | 103 | A | Angler = fake support accounts (M09) |
| 41 | D | LLMNR/NBT-NS/mDNS (M08) | 104 | B | SYN cookies vs SYN flood (M10) |
| 42 | C | DAI counters ARP poisoning (M08) | 105 | A | RST/FIN = network level (M11) |
| 43 | A | Pretext = fabricated scenario (M09) | 106 | C | DNS tunneling = exfil/C2 (M12) |
| 44 | B | Tailgating = without awareness (M09) | 107 | A | WebDAV PUT → web shell (M13) |
| 45 | C | HTTP flood = app-layer (M10) | 108 | D | Burp intercepting proxy (M14) |
| 46 | B | Small spoofed UDP → big reply (M10) | 109 | A | Second-order = stored then run (M15) |
| 47 | B | Reissue session ID at login (M11) | 110 | B | WPS PIN brute force (M16) |
| 48 | D | HttpOnly blocks JS cookie read (M11) | 111 | B | MobSF static+dynamic (M17) |
| 49 | A | High-interaction honeypot (M12) | 112 | D | Data diode = one-way flow (M18) |
| 50 | D | `-D` decoys (M03/M12) | 113 | A | Privileged/docker.sock/caps (M19) |
| 51 | B | IDOR = broken authorization (M14) | 114 | C | Pacu = AWS exploitation (M19) |
| 52 | D | SSRF = A10 (M14) | 115 | D | Birthday ≈ 2^(n/2) (M20) |
| 53 | B | Executes an OS command (M14) | 116 | A | BitLocker + TPM (M20) |
| 54 | B | xp_cmdshell (MSSQL) (M15) | 117 | D | TLS1.3 forward secrecy, no RSA transport (M20) |
| 55 | C | Boolean-based blind (M15) | 118 | A | Stego hides existence (M20/M06) |
| 56 | B | WEP weak IV + RC4 (M16) | 119 | C | Only needed rights (M01) |
| 57 | A | Evil twin = rogue SSID clone (M16) | 120 | C | 4769 RC4 for SPNs (M06) |
| 58 | C | WPA3 SAE (M16) | 121 | B | Grey-hat = unclear authz, not malicious (M01) |
| 59 | D | Jailbreak removes sandbox/signing (M17) | 122 | A | Assess→rank→remediate→verify→monitor (M05) |
| 60 | C | Cleartext prefs/plist/logs (M17) | 123 | A | Low-TTL = insertion (M12) |
| 61 | A | Mirai = Telnet default creds (M18) | 124 | A | Broker the session (M08/dp) |
| 62 | D | Modbus = 502 (M18) | 125 | A | RA verifies identity (M20) |
| 63 | D | etcd stores secrets (M19) | | | |

---

## Scoring guide

| Score (of 125) | % | Read |
|---|---|---|
| **113+** | 90%+ | Strong across the board — you're exam-ready on knowledge. |
| **100–112** | 80–89% | Comfortable. Re-drill the 2–3 weakest modules, then book. |
| **88–99** | 70–79% | Above most cut scores but not by much — close the weak-module gaps first. |
| **75–87** | 60–69% | Near/around the variable cut line — more study before booking. |
| **< 75** | <60% | Keep working the module loop; re-take after another pass. |

> The real CEH cut score is **variable (~60–85%)** by question form — treat anything under ~80% here as "keep studying." This is a knowledge checkpoint, not a guarantee. Confirm readiness against official EC-Council practice and [EXAM-LOGISTICS.md](EXAM-LOGISTICS.md).
