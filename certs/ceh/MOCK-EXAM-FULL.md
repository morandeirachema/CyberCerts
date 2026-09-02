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
- A. Nmap version scan  B. Reviewing the target's public LinkedIn and job posts  C. DNS zone transfer  D. Traceroute to the target

**4.** A DNS **SRV** record is most useful to an attacker because it:
- A. Lists mail servers  B. Locates services such as LDAP/Kerberos (finding domain controllers)  C. Stores SPF data  D. Maps IP to hostname

**5.** On a Linux host, a SYN scan to a **filtered** port typically results in:
- A. SYN/ACK  B. RST  C. No response (or ICMP unreachable)  D. FIN

**6.** Which nmap option performs OS fingerprinting?
- A. `-sV`  B. `-O`  C. `-sn`  D. `-p-`

**7.** SNMP enumeration succeeds because a device uses the default read community string:
- A. admin  B. public  C. root  D. cisco

**8.** The built-in Windows Administrator account always has which RID?
- A. 501  B. 512  C. 500  D. 1000

**9.** A credentialed vulnerability scan is preferred because it:
- A. Runs without touching the host  B. Reveals missing patches/configs with fewer false positives  C. Only checks open ports  D. Is faster than a ping sweep

**10.** A CVSS base score of 4.5 (v3) is which severity?
- A. Low  B. Medium  C. High  D. Critical

**11.** Pass-the-Hash is possible against NTLM because NTLM hashes are:
- A. Salted  B. Encrypted with the user's password  C. Unsalted and usable directly for authentication  D. One-time values

**12.** Which attack requires **offline cracking** to succeed?
- A. Pass-the-Ticket  B. Kerberoasting  C. Pass-the-Hash  D. Overpass-the-Hash (using an existing hash to get a TGT)

**13.** A worm's defining characteristic is that it:
- A. Needs a host file  B. Self-replicates across the network without user action  C. Requires the user to open it  D. Cannot propagate

**14.** Which malware component fetches additional stages from the internet?
- A. Dropper  B. Downloader  C. Packer  D. Payload

**15.** Wireshark **display filters** differ from capture filters in that display filters:
- A. Use BPF syntax  B. Are applied after capture to shown packets (e.g., `http.request`)  C. Cannot filter by protocol  D. Only work on UDP

**16.** MAC flooding forces a switch to:
- A. Reboot  B. Behave like a hub (fail open)  C. Enable DAI  D. Drop all frames

**17.** Which social-engineering attack uses SMS as the delivery channel?
- A. Vishing  B. Smishing  C. Whaling  D. Pharming

**18.** In a SYN flood, the attacker exhausts the target by:
- A. Completing many handshakes  B. Sending SYNs and never completing the handshake (half-open connections)  C. Flooding ICMP  D. Sending oversized packets

**19.** Application-level session hijacking most commonly steals:
- A. A TCP sequence number  B. A session cookie/token  C. An ARP entry  D. A DNS record

**20.** An **insertion** attack against an IDS works by:
- A. Flooding the IDS  B. Making the IDS accept a packet the end host will reject  C. Encrypting traffic  D. Disabling logging

**21.** Directory traversal against a web server uses sequences like:
- A. `UNION SELECT`  B. `../../`  C. `<script>`  D. `; whoami`

**22.** Which is a **stored** XSS scenario?
- A. A crafted link echoes input back once  B. A comment saved in the DB executes for every viewer  C. Client-side JS uses `location.hash`  D. A GET parameter reflected in an error

**23.** The best fix for SQL injection is:
- A. A WAF  B. Escaping quotes only  C. Parameterized queries / prepared statements  D. Hiding SQL errors

**24.** The WPA2 four-way handshake lets an attacker:
- A. Decrypt all traffic live  B. Capture material to brute-force the PSK offline  C. Bypass MAC filtering  D. Disable WPS

**25.** Rooting an Android device primarily:
- A. Improves battery  B. Removes the app sandbox / privilege restrictions  C. Encrypts storage  D. Installs MDM

**26.** MQTT operates as:
- A. REST over UDP  B. Publish/subscribe over TCP  C. A file-transfer protocol  D. A routing protocol

**27.** The Purdue model's IDMZ (Level 3.5) exists to:
- A. Run PLCs  B. Broker/segment traffic between IT and OT  C. Host email  D. Store backups

**28.** An SSRF that reaches `169.254.169.254` in AWS can steal:
- A. The root password  B. Temporary instance-role credentials  C. The TLS private key  D. The bucket ACL

**29.** Which is the correct email-security trust-model pairing?
- A. PGP → CA hierarchy; S/MIME → web of trust  B. PGP → web of trust; S/MIME → X.509 CA  C. Both CA hierarchy  D. Both web of trust

**30.** Encrypting a file so only Bob can read it requires:
- A. Bob's private key  B. Bob's public key  C. Your private key  D. A shared symmetric key sent in the clear

**31.** MITRE ATT&CK "tactics" represent:
- A. Specific tools  B. The adversary's goal (the why)  C. A CVE  D. A patch

**32.** Which is **not** a phase of the classic hacking methodology?
- A. Reconnaissance  B. Scanning  C. Compilation  D. Maintaining Access

**33.** `theHarvester` is used to:
- A. Crack hashes  B. Gather emails/subdomains/hosts from public sources  C. Scan ports  D. Poison ARP

**34.** Which nmap scan needs no root/admin privilege?
- A. `-sS`  B. `-sT`  C. `-sN`  D. `-sX`

**35.** A null session abuses which service to enumerate users/shares?
- A. HTTP  B. SMB/IPC$  C. SNMP  D. NTP

**36.** Which describes a **false negative** in vulnerability scanning?
- A. Flagging a vuln that isn't there  B. Missing a vulnerability that is actually present  C. A duplicate finding  D. A network timeout

**37.** Kerberoasting yields a crackable ticket because the TGS is encrypted with:
- A. The krbtgt hash  B. The requesting user's password  C. The target service account's key  D. The DC's machine key

**38.** Which control best defeats local-admin hash reuse across many hosts?
- A. AppLocker  B. LAPS  C. LLMNR  D. SMB null sessions

**39.** A rootkit that loads before the OS by infecting the bootloader is a:
- A. User-mode rootkit  B. Bootkit  C. Library rootkit  D. Application rootkit

**40.** Which is a fileless / living-off-the-land technique?
- A. Dropping `evil.exe`  B. Base64-encoded PowerShell executed via a signed binary  C. A boot-sector virus  D. A macro that writes an EXE

**41.** Responder poisons which protocols to capture NetNTLM hashes?
- A. HTTP/HTTPS  B. LLMNR/NBT-NS/mDNS  C. SSH  D. RDP

**42.** Which switch feature counters ARP poisoning?
- A. Port security  B. DHCP snooping  C. Dynamic ARP Inspection  D. STP

**43.** A pretexting attack relies on:
- A. Malware  B. A fabricated scenario to gain trust and extract info  C. A buffer overflow  D. Port scanning

**44.** Tailgating differs from piggybacking in that tailgating implies:
- A. The authorized person knowingly lets you in  B. Following in without the authorized person's awareness/consent  C. Using a stolen badge  D. A phishing email

**45.** Which DDoS category does an HTTP GET/POST flood belong to?
- A. Volumetric  B. Protocol  C. Application-layer  D. Reflection

**46.** DNS amplification is effective because:
- A. DNS uses TCP with handshakes  B. Small spoofed UDP queries yield large responses to the victim  C. DNS is encrypted  D. It requires no spoofing

**47.** Session fixation is prevented by:
- A. Longer passwords  B. Issuing a new session ID upon login  C. Disabling HTTPS  D. Using GET for logins

**48.** Which cookie flag prevents JavaScript from reading a session cookie?
- A. Secure  B. HttpOnly  C. SameSite  D. Domain

**49.** A honeypot that fully emulates an OS and services to deeply engage attackers is:
- A. Low-interaction  B. High-interaction  C. A tarpit  D. A sinkhole

**50.** Which nmap technique hides your real source among fakes?
- A. `-sV`  B. `-D` decoys  C. `-O`  D. `-p-`

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
- A. Two APs with different SSIDs  B. A rogue AP impersonating a legitimate SSID  C. A deauth flood  D. A WPS brute force

**58.** WPA3 resists offline PSK cracking primarily via:
- A. TKIP  B. WEP IVs  C. SAE (Dragonfly) handshake  D. MAC filtering

**59.** On iOS, jailbreaking removes:
- A. The battery limit  B. Sandbox and code-signing restrictions  C. The SIM lock only  D. MDM enrollment

**60.** Insecure data storage on mobile means secrets sit in:
- A. The Secure Enclave  B. SharedPreferences/plist/SQLite/logs in cleartext  C. Encrypted Keychain  D. A remote HSM

**61.** Mirai spread mainly by:
- A. Exploiting a browser 0-day  B. Trying default Telnet credentials on IoT devices  C. Phishing emails  D. SQL injection

**62.** Which OT protocol runs on TCP port 502?
- A. DNP3  B. Modbus  C. S7comm  D. BACnet

**63.** In Kubernetes, which component stores secrets and, if exposed unauthenticated, means full compromise?
- A. kubelet  B. etcd  C. kube-proxy  D. the dashboard

**64.** IMDSv2 mitigates SSRF credential theft by:
- A. Encrypting the disk  B. Requiring a session token (PUT) and honoring a hop limit  C. Blocking all metadata  D. Rotating the instance ID

**65.** A padding-oracle attack specifically targets:
- A. ECB  B. CBC  C. GCM  D. CTR

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
- A. Financial motive  B. A political/social cause  C. Nation-state backing  D. Curiosity only

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
- A. Self-replicates  B. Poses as legitimate software the user installs  C. Needs no user action  D. Only infects boot sectors

**79.** Which protocol swap removes cleartext credential sniffing for remote admin?
- A. Telnet → FTP  B. Telnet → SSH  C. HTTP → HTTP/2  D. SNMPv2c → SNMPv1

**80.** Business Email Compromise (BEC) is best mitigated by:
- A. Antivirus  B. Out-of-band verification of payment/detail changes  C. A faster mail server  D. Longer passwords

**81.** Which is a **protocol** DoS attack?
- A. HTTP flood  B. SYN flood  C. DNS amplification  D. Slowloris

**82.** TCP sequence-number prediction enables:
- A. A UDP flood  B. Network-level session hijacking  C. XSS  D. Phishing

**83.** A firewall that inspects and remembers connection state is a:
- A. Packet filter (stateless)  B. Stateful firewall  C. Proxy only  D. Hub

**84.** Uploading `shell.php` to a poorly validated upload form yields:
- A. A CSRF token  B. A web shell → remote code execution  C. An SSRF  D. A DoS

**85.** CSRF is best mitigated by:
- A. Input encoding  B. Anti-CSRF tokens + SameSite cookies  C. Rate limiting only  D. Disabling cookies

**86.** sqlmap flag to test whether the DB account is a DBA:
- A. `--dbs`  B. `--is-dba`  C. `--batch`  D. `--tables`

**87.** A deauthentication attack is used to:
- A. Crack WEP instantly  B. Force clients to reconnect so the handshake can be captured  C. Disable WPS  D. Spoof a MAC

**88.** Which mobile analysis is **static**?
- A. Running the app and hooking with Frida  B. Decompiling the APK with jadx and reading the manifest  C. Capturing live API calls  D. Fuzzing at runtime

**89.** CoAP is best described as:
- A. Pub/sub over TCP  B. RESTful over UDP for constrained devices  C. A serial protocol  D. A routing protocol

**90.** A misconfigured public S3 bucket is an example of OWASP/cloud:
- A. Injection  B. Security misconfiguration / broken access to storage  C. SSRF  D. Cryptographic failure

**91.** ECC is favored on mobile/IoT because it offers:
- A. Larger keys for the same strength  B. Equivalent strength with smaller keys (less compute)  C. No key at all  D. Symmetric speed

**92.** Which mode provides authenticated encryption (confidentiality + integrity)?
- A. ECB  B. CBC  C. GCM  D. CTR

**93.** A zero-day is a vulnerability that:
- A. Is fully patched  B. Has no available patch and is unknown to the vendor  C. Only affects hardware  D. Is a false positive

**94.** Which is the **first** thing to establish before any authorized test?
- A. The exploit  B. Written authorization / scope (Rules of Engagement)  C. The report template  D. The payload

**95.** Website mirroring (e.g., HTTrack) supports footprinting by:
- A. Cracking logins  B. Creating an offline copy to analyze without hitting the live site  C. Poisoning DNS  D. Flooding the server

**96.** A masscan is chosen over nmap when you need:
- A. Deep NSE scripting  B. Very fast, internet-scale port sweeps  C. OS fingerprinting  D. Version detection

**97.** LDAP anonymous binds can leak:
- A. Encryption keys  B. Directory objects (users, groups, OUs)  C. Firewall rules  D. Disk contents

**98.** A CVSS **environmental** metric adjusts the score based on:
- A. Global averages  B. The specific organization's context/impact  C. The exploit author  D. The vendor's name

**99.** Overpass-the-Hash (pass-the-key) uses an NT hash to:
- A. Decrypt the disk  B. Request a legitimate Kerberos TGT  C. Crack the password  D. Poison ARP

**100.** Which best reduces the blast radius of any single compromised admin credential?
- A. A longer password  B. Tiered administration + JIT (no standing privilege)  C. Antivirus  D. Disabling IPv6

**101.** A polymorphic virus evades signatures by:
- A. Rewriting its entire code each run  B. Mutating its encrypted body with a changing decryptor  C. Hiding in slack space  D. Infecting the boot sector

**102.** Which capture confirms a cleartext credential leak?
- A. A TLS ClientHello  B. An FTP `PASS` command visible in the packet bytes  C. An encrypted SSH stream  D. A DNS query

**103.** Angler phishing specifically abuses:
- A. Phone calls  B. Fake customer-support accounts on social media  C. USB drops  D. QR codes only

**104.** A SYN cookie defends against:
- A. ARP poisoning  B. SYN floods  C. XSS  D. DNS poisoning

**105.** RST/FIN hijacking operates at which level?
- A. Application  B. Network (TCP)  C. Physical  D. Presentation

**106.** DNS tunneling is used to:
- A. Speed up DNS  B. Exfiltrate data / C2 through an allowed protocol  C. Encrypt DNS  D. Block queries

**107.** WebDAV misconfigured to allow `PUT` can let an attacker:
- A. Only read files  B. Upload a web shell to the server  C. Crash the DB  D. Sniff traffic

**108.** Which tool automates web-app request tampering via an intercepting proxy?
- A. Nikto  B. Burp Suite  C. Hydra  D. Nessus

**109.** Second-order SQL injection means the payload:
- A. Executes immediately  B. Is stored and executed later by a different query  C. Only works over HTTPS  D. Requires DBA

**110.** Which is a WPS weakness an attacker exploits?
- A. AES  B. The 8-digit PIN's brute-forceable design (Pixie-Dust)  C. SAE  D. 802.1X

**111.** MobSF is used to:
- A. Root a phone  B. Perform automated static + dynamic mobile app analysis  C. Flash firmware  D. Spoof GPS

**112.** In OT security, a unidirectional gateway (data diode) enforces:
- A. Two-way encrypted tunnels  B. Traffic flow in one direction only (e.g., OT → IT)  C. Wireless meshing  D. Password rotation

**113.** Container escape most often abuses:
- A. A read-only rootfs  B. A privileged container / mounted docker.sock / excess capabilities  C. Network policy  D. Pod Security Standards

**114.** Which cloud tool is an AWS **exploitation** framework?
- A. ScoutSuite  B. Prowler  C. Pacu  D. Trivy

**115.** A birthday attack finds a hash collision in roughly:
- A. 2^n  B. 2^(n/2)  C. n²  D. n log n

**116.** BitLocker commonly seals its key using:
- A. A remote CA  B. The TPM  C. A password only  D. A web of trust

**117.** Which is TRUE about TLS 1.3?
- A. It re-added RC4  B. It mandates forward secrecy (ephemeral DH) and removed RSA key transport  C. It removed all symmetric ciphers  D. It requires WEP

**118.** Steganography differs from cryptography because it:
- A. Scrambles content  B. Hides the very existence of the message  C. Is always stronger  D. Only works on text

**119.** The "principle of least privilege" means:
- A. Everyone is admin for convenience  B. Users/services get only the rights their role needs  C. No one can log in  D. All access is logged

**120.** Which detection signal most specifically indicates Kerberoasting?
- A. 4625 spikes  B. 4769 TGS requests for SPN accounts using RC4  C. 4740 lockouts  D. 1102 log cleared

**121.** A grey-hat hacker is one who:
- A. Always has authorization  B. Acts without clear authorization but not purely maliciously  C. Is always nation-state  D. Never uses tools

**122.** Which is the correct order in the vulnerability-management lifecycle?
- A. Remediate → Assess → Monitor  B. Assess → Risk-rank → Remediate → Verify → Monitor  C. Verify → Assess → Remediate  D. Monitor → Remediate → Assess

**123.** An attacker sends a crafted packet with a low TTL so the IDS sees it but the target never does. This is:
- A. An evasion attack  B. An insertion attack  C. A DoS  D. A honeypot

**124.** Which is the strongest answer to "how do we stop admin credentials being sniffed or keylogged?"
- A. Longer passwords  B. Broker sessions so the credential is injected server-side and never touches the endpoint/wire  C. Antivirus  D. Disable DNS

**125.** In PKI, the component that verifies an applicant's identity before a certificate is issued is the:
- A. CA  B. RA  C. CRL  D. OCSP responder

---

## Answer key

> Score first, then study the rationale for each miss and revisit that module.

| Q | Ans | Why (module) | Q | Ans | Why (module) |
|---|---|---|---|---|---|
| 1 | C | Ransomware denies access (M20/M07) | 64 | B | IMDSv2 token + hop limit (M19) |
| 2 | C | No prior knowledge = black-box (M01) | 65 | B | Padding oracle → CBC (M20) |
| 3 | B | Public profiles = passive OSINT (M02) | 66 | C | Slow salted KDFs (M20) |
| 4 | B | SRV locates LDAP/Kerberos = DCs (M02) | 67 | C | DH = key exchange only (M20) |
| 5 | C | Filtered = no response/ICMP (M03) | 68 | C | Signatures aren't confidentiality (M20) |
| 6 | B | `-O` = OS detection (M03) | 69 | B | Layered controls (M01) |
| 7 | B | Default read community = public (M04) | 70 | D | Log clearing = covering tracks (M06) |
| 8 | C | Administrator RID = 500 (M04) | 71 | B | Hacktivist = cause-driven (M01) |
| 9 | B | Credentialed = deeper, fewer FPs (M05) | 72 | B | filetype dork (M02) |
| 10 | B | 4.0–6.9 = Medium (M05) | 73 | B | ACK maps filtered/unfiltered (M03) |
| 11 | C | NTLM unsalted, hash reusable (M06) | 74 | A | enum4linux = SMB/NetBIOS/RPC (M04) |
| 12 | B | Kerberoasting cracks svc pwd (M06) | 75 | C | CWE = weakness type (M05) |
| 13 | B | Worm self-propagates (M07) | 76 | B | Replication from non-DC (M06) |
| 14 | B | Downloader fetches stages (M07) | 77 | B | LSASS holds creds/tickets (M06) |
| 15 | B | Display filters post-capture (M08) | 78 | B | Trojan = disguised, user-run (M07) |
| 16 | B | CAM overflow → fail open (M08) | 79 | B | Telnet → SSH (M08) |
| 17 | B | SMS phishing = smishing (M09) | 80 | B | Out-of-band verify (M09) |
| 18 | B | Half-open connections (M10) | 81 | B | SYN flood = protocol (M10) |
| 19 | B | Steal the session token (M11) | 82 | B | Seq prediction = net hijack (M11) |
| 20 | B | IDS accepts, host rejects (M12) | 83 | B | Stateful firewall (M12) |
| 21 | B | `../../` traversal (M13) | 84 | B | Upload → web shell = RCE (M13/M14) |
| 22 | B | Stored XSS runs for all (M14) | 85 | B | Anti-CSRF tokens + SameSite (M14) |
| 23 | C | Parameterized queries (M15) | 86 | B | `--is-dba` (M15) |
| 24 | B | Handshake → offline PSK crack (M16) | 87 | B | Deauth forces handshake (M16) |
| 25 | B | Rooting removes sandbox (M17) | 88 | B | jadx decompile = static (M17) |
| 26 | B | MQTT = pub/sub over TCP (M18) | 89 | B | CoAP = REST over UDP (M18) |
| 27 | B | IDMZ brokers IT↔OT (M18) | 90 | B | Public bucket = misconfig (M19) |
| 28 | B | Instance-role creds via IMDS (M19) | 91 | B | ECC = smaller keys (M20) |
| 29 | B | PGP=WoT, S/MIME=X.509 (M20) | 92 | C | GCM = authenticated (M20) |
| 30 | B | Recipient's public key (M20) | 93 | B | 0-day = no patch/unknown (M01) |
| 31 | B | Tactic = the goal (M01) | 94 | B | Authorization/scope first (M01) |
| 32 | C | "Compilation" isn't a phase (M01) | 95 | B | Offline mirror to analyze (M02) |
| 33 | B | theHarvester = OSINT (M02) | 96 | B | masscan = fast/scale (M03) |
| 34 | B | `-sT` needs no root (M03) | 97 | B | LDAP leaks directory objects (M04) |
| 35 | B | Null session via SMB/IPC$ (M04) | 98 | B | Environmental = org context (M05) |
| 36 | B | Missed real vuln = FN (M05) | 99 | B | Overpass-the-Hash → TGT (M06) |
| 37 | C | Encrypted with svc account key (M06) | 100 | B | Tiering + JIT (M06/dp) |
| 38 | B | LAPS = unique local admin (M06) | 101 | B | Polymorphic mutates encryption (M07) |
| 39 | B | Bootkit loads pre-OS (M07) | 102 | B | FTP PASS in cleartext (M08) |
| 40 | B | Encoded PS via signed binary (M07) | 103 | B | Angler = fake support accounts (M09) |
| 41 | B | LLMNR/NBT-NS/mDNS (M08) | 104 | B | SYN cookies vs SYN flood (M10) |
| 42 | C | DAI counters ARP poisoning (M08) | 105 | B | RST/FIN = network level (M11) |
| 43 | B | Pretext = fabricated scenario (M09) | 106 | B | DNS tunneling = exfil/C2 (M12) |
| 44 | B | Tailgating = without awareness (M09) | 107 | B | WebDAV PUT → web shell (M13) |
| 45 | C | HTTP flood = app-layer (M10) | 108 | B | Burp intercepting proxy (M14) |
| 46 | B | Small spoofed UDP → big reply (M10) | 109 | B | Second-order = stored then run (M15) |
| 47 | B | Reissue session ID at login (M11) | 110 | B | WPS PIN brute force (M16) |
| 48 | B | HttpOnly blocks JS cookie read (M11) | 111 | B | MobSF static+dynamic (M17) |
| 49 | B | High-interaction honeypot (M12) | 112 | B | Data diode = one-way flow (M18) |
| 50 | B | `-D` decoys (M03/M12) | 113 | B | Privileged/docker.sock/caps (M19) |
| 51 | B | IDOR = broken authorization (M14) | 114 | C | Pacu = AWS exploitation (M19) |
| 52 | D | SSRF = A10 (M14) | 115 | B | Birthday ≈ 2^(n/2) (M20) |
| 53 | B | Executes an OS command (M14) | 116 | B | BitLocker + TPM (M20) |
| 54 | B | xp_cmdshell (MSSQL) (M15) | 117 | B | TLS1.3 forward secrecy, no RSA transport (M20) |
| 55 | C | Boolean-based blind (M15) | 118 | B | Stego hides existence (M20/M06) |
| 56 | B | WEP weak IV + RC4 (M16) | 119 | B | Only needed rights (M01) |
| 57 | B | Evil twin = rogue SSID clone (M16) | 120 | B | 4769 RC4 for SPNs (M06) |
| 58 | C | WPA3 SAE (M16) | 121 | B | Grey-hat = unclear authz, not malicious (M01) |
| 59 | B | Jailbreak removes sandbox/signing (M17) | 122 | B | Assess→rank→remediate→verify→monitor (M05) |
| 60 | B | Cleartext prefs/plist/logs (M17) | 123 | B | Low-TTL = insertion (M12) |
| 61 | B | Mirai = Telnet default creds (M18) | 124 | B | Broker the session (M08/dp) |
| 62 | B | Modbus = 502 (M18) | 125 | B | RA verifies identity (M20) |
| 63 | B | etcd stores secrets (M19) | | | |

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
