# CEH v13 — Glossary & Acronym Index

Fast-retrieval definitions for the acronym-dense CEH syllabus. Keep it open while you study — many CEH questions hinge on knowing exactly what an acronym expands to and does. `[NN]` points to the most relevant [module](modules/README.md); `[dp]` points to the [defender-pam](defender-pam/README.md) knowledge base.

> Comprehensive across all 20 modules. Missing a term? Add it in a PR.

---

## A
- **AAA** — Authentication, Authorization, Accounting. `[01]`
- **ACK scan** (`-sA`) — maps firewall **filtered vs unfiltered**, not open/closed. `[03]`
- **ADS** — Alternate Data Stream (NTFS); hides data in `file:stream`; anti-forensics. `[06]`
- **AES** — Advanced Encryption Standard (Rijndael); symmetric block cipher, 128/192/256-bit, FIPS 197. `[20]`
- **Amplification/reflection attack** — spoof the victim's IP to a service (DNS/NTP/memcached/SSDP/CLDAP) that replies with a much larger response. `[10]`
- **Anomaly-based IDS** — flags deviations from a learned baseline (vs signature-based). `[12]`
- **APT** — Advanced Persistent Threat; stealthy, persistent, funded actor. `[07]`
- **ARP** — Address Resolution Protocol; no authentication → ARP poisoning enables MITM. `[08]`
- **AS-REP roasting** — cracking the AS-REP of accounts with Kerberos pre-auth disabled. `[06]`
- **ASLR** — Address Space Layout Randomization; exploit mitigation. `[06]`
- **Authenticated scan** — credentialed vulnerability scan; deeper, fewer false positives. `[05]`
- **AXFR** — DNS zone transfer; if open, leaks the whole namespace. `[02]`
- **aircrack-ng** — Wi-Fi capture/crack suite (airmon/airodump/aireplay/aircrack). `[16]`

## B
- **Bluetooth attacks** — bluejacking (spam), bluesnarfing (data theft), bluebugging (device control), BlueBorne (no-pairing exploit chain), KNOB/BIAS (downgrade/impersonation). `[16]`
- **Buffer overflow** — overwriting past a buffer to hijack control flow → code execution; mitigated by DEP/NX, ASLR, stack canaries. `[06]`
- **Banner grabbing** — reading a service's version banner to fingerprint it. `[03]`
- **bcrypt / scrypt / Argon2 / PBKDF2** — slow, salted password-hashing KDFs. `[20]`
- **BEC** — Business Email Compromise. `[09]`
- **Birthday attack** — hash-collision attack, ~2^(n/2) work. `[20]`
- **Black/white/grey-box test** — no / full / partial prior knowledge given to the tester. `[01]`
- **BLE** — Bluetooth Low Energy; short-range IoT radio. `[18]`
- **Bluesnarfing / Bluejacking** — data theft / unsolicited messages over Bluetooth. `[17]`
- **Bootkit** — rootkit that infects the bootloader/MBR/UEFI, loading before the OS. `[07]`
- **Botnet** — network of compromised hosts (handlers/agents) under C2. `[07][10]`

## C
- **C2 / C&C** — Command and Control (attacker infrastructure). `[07]`
- **CA** — Certificate Authority; issues/signs certs in PKI. `[20]`
- **CAM table** — a switch's MAC→port table; overflowing it (MAC flooding) fails it open. `[08]`
- **CBC** — Cipher Block Chaining mode; padding-oracle target. `[20]`
- **CCP** — CyberArk Central Credential Provider; removes hardcoded app credentials. `[dp]`
- **CIA** — Confidentiality, Integrity, Availability. `[01]`
- **CoAP** — Constrained Application Protocol; RESTful over **UDP** (5683), IoT. `[18]`
- **Community string** — SNMP v1/2c cleartext password (public=read, private=write). `[04][08]`
- **CPE** — Common Platform Enumeration; standard product naming. `[05]`
- **CPM** — CyberArk Central Policy Manager; rotates/verifies/reconciles credentials. `[dp]`
- **Credential Guard** — Windows VBS isolation of secrets; blocks LSASS theft. `[06]`
- **CRL** — Certificate Revocation List. `[20]`
- **Cryptanalysis** — recovering plaintext/keys without the key: frequency, linear, differential, side-channel, brute-force/birthday/rainbow. `[20]`
- **CSRF** — Cross-Site Request Forgery; tricks the **browser** into a state-changing request. `[14]`
- **CVE** — Common Vulnerabilities and Exposures; a specific known vuln ID. `[05]`
- **CVSS** — Common Vulnerability Scoring System (0–10 severity). `[05]`
- **CWE** — Common Weakness Enumeration; the weakness *class* (e.g., CWE-89 SQLi). `[05]`

## D
- **Diamond Model** — intrusion analysis over four vertices: Adversary, Capability, Infrastructure, Victim. `[01]`
- **DAI** — Dynamic ARP Inspection; counters ARP poisoning. `[08]`
- **DCShadow** — registers a rogue DC to push malicious AD changes. `[dp]`
- **DCSync** — abuse of AD replication rights to pull hashes (incl. krbtgt) from a DC. `[06]`
- **Deauth attack** — 802.11 deauthentication frames to disconnect clients (forces handshake capture). `[16]`
- **DES / 3DES** — Data Encryption Standard (56-bit, broken) / Triple DES (legacy). `[20]`
- **DH / ECDHE** — Diffie-Hellman / Ephemeral EC DH; **key exchange** (ECDHE = forward secrecy). `[20]`
- **DHCP snooping** — switch feature countering rogue DHCP. `[08]`
- **DHCP starvation** — exhausting the DHCP pool to enable a rogue server / DoS. `[08]`
- **DMZ** — demilitarized zone; segmented network for internet-facing services. `[12]`
- **DNP3** — OT/SCADA protocol (utilities), port 20000. `[18]`
- **DNS poisoning** — injecting false DNS records (intranet/internet/proxy/cache variants). `[08]`
- **DoS / DDoS / DRDoS** — Denial / Distributed / Distributed-Reflection Denial of Service. `[10]`
- **DPA** — CyberArk Dynamic Privileged Access; agentless JIT/ZSP to VMs & cloud. `[dp]`
- **Downloader** — malware component that fetches later stages from the internet. `[07]`
- **Dropper** — malware component that writes/installs the payload it already carries. `[07]`
- **DSA** — Digital Signature Algorithm; **signatures only**. `[20]`
- **Dumpster diving** — non-electronic recon by searching discarded materials. `[09]`

## E
- **ECB** — Electronic Code Book mode; leaks patterns — never use. `[20]`
- **ECC** — Elliptic Curve Cryptography; RSA-equivalent security, smaller keys. `[20]`
- **EDR** — Endpoint Detection and Response. `[07]`
- **enum4linux** — SMB/NetBIOS/RPC enumeration tool. `[04]`
- **EPM** — CyberArk Endpoint Privilege Manager; removes local admin, app control, credential-theft blocking. `[dp]`
- **EPV** — CyberArk Enterprise Password Vault (Digital Vault). `[dp]`
- **ESC1–8** — ADCS certificate-abuse techniques (Certified Pre-Owned). `[dp]`
- **Evil twin** — rogue AP impersonating a legitimate SSID to capture clients. `[16]`

## F
- **FaaS** — Function as a Service (serverless). `[19]`
- **False positive / negative** — flagged-but-not-vulnerable / missed-real-vuln (the latter is worse). `[05]`
- **FIDO2 / passkeys** — phishing-resistant authentication. `[09][17]`
- **FIN scan** (`-sF`) — sends a lone FIN; open ports stay silent, closed send RST. `[03]`
- **Footprinting** — gathering target info before attacking (passive + active). `[02]`
- **Forward secrecy** — past sessions stay safe if the long-term key later leaks (ephemeral DH). `[20]`
- **Fraggle** — UDP variant of the Smurf amplification attack. `[10]`

## G
- **GCM** — Galois/Counter Mode; authenticated encryption (confidentiality + integrity). `[20]`
- **gMSA** — Group Managed Service Account; 128-char auto-rotated password → defeats Kerberoasting. `[06]`
- **gobuster / ffuf** — web content/directory brute-forcers. `[13][14]`
- **Golden ticket** — forged TGT signed with the krbtgt hash (domain-wide). `[06]`
- **Google dorking** — advanced search operators (site:, filetype:, inurl:) to find exposed data. `[02]`

## H
- **hashcat** — GPU hash-cracking tool (modes: 1000 NTLM, 5600 NetNTLMv2, 13100 Kerberos, 22000 WPA). `[06]`
- **HIDS / NIDS** — Host / Network Intrusion Detection System. `[12]`
- **HMI** — Human-Machine Interface (OT operator screen). `[18]`
- **Honeypot** — decoy system; low-interaction (emulated) vs high-interaction (full). `[12]`
- **HSM** — Hardware Security Module; protects keys (e.g., the Vault Server Key). `[20][dp]`
- **HSTS** — HTTP Strict Transport Security. `[11]`
- **Hydra / Medusa** — online credential brute-force tools. `[06]`

## I
- **IAM** — Identity and Access Management. `[19]`
- **IKE** — Internet Key Exchange (IPsec VPN); aggressive mode is enumerable via ike-scan (500/UDP). `[04]`
- **IoC (Indicator of Compromise)** — forensic artifact of a breach (malicious IP/hash/domain, C2 beacon); email/network/host/behavioral categories. `[01][07]`
- **IDOR** — Insecure Direct Object Reference; broken access control (OWASP A01). `[14]`
- **IDS / IPS** — Intrusion Detection (passive) / Prevention (inline block) System. `[12]`
- **IEC 62443** — OT/ICS security standard (zones & conduits). `[18]`
- **IMDS / IMDSv2** — Instance Metadata Service; SSRF steals role creds via 169.254.169.254; IMDSv2 mitigates. `[19]`
- **Insertion attack** — make the IDS accept a packet the end host rejects (padding its view). `[12]`
- **`information_schema`** — DB view enumerated in SQLi for tables/columns (Oracle differs). `[15]`
- **IoC** — Indicator of Compromise. `[07]`
- **IV** — Initialization Vector (randomizes CBC/CTR; WEP's IV reuse is its downfall). `[16][20]`

## J
- **Jailbreaking** — removing iOS sandbox/code-signing restrictions (Android = rooting). `[17]`
- **JIT** — Just-in-Time privilege (granted per task, time-boxed). `[06][dp]`
- **John the Ripper** — CPU hash-cracking tool. `[06]`

## K
- **Keylogger** — captures keystrokes; hardware (inline/USB) or software (kernel/API hooks). `[06]`
- **KDF** — Key Derivation Function (bcrypt/scrypt/Argon2/PBKDF2). `[20]`
- **Kerberoasting** — request a TGS for an SPN and crack the **service account** password offline. `[06]`
- **Kill chain** — Lockheed Martin's 7-stage attack model. `[01]`
- **krbtgt** — AD account whose hash signs all TGTs; basis of golden tickets. `[06]`
- **kube-bench / kube-hunter** — Kubernetes CIS-benchmark / pentest tools. `[19]`

## L
- **LAPS** — Local Administrator Password Solution; unique rotated local-admin password per host. `[06]`
- **LFI / RFI** — Local / Remote File Inclusion. `[14]`
- **LLMNR / NBT-NS** — legacy name-resolution protocols abused by Responder to capture NetNTLM. `[08]`
- **LDAP / LDAPS** — directory query protocol, 389 / 636. `[04]`
- **LOLBin** — Living-Off-the-Land Binary (trusted signed binary abused, e.g. certutil). `[07]`
- **LSASS** — Local Security Authority Subsystem Service; memory holds creds/tickets (Mimikatz target). `[06]`

## M
- **MAC flooding** — overflow the CAM table so the switch fails open. `[08]`
- **macof** — tool that performs MAC flooding. `[08]`
- **MAM / MDM / UEM** — Mobile Application / Device / Unified Endpoint Management. `[17]`
- **Metamorphic virus** — rewrites its own code each generation (no static signature). `[07]`
- **MFA** — Multi-Factor Authentication. `[09]`
- **Mimikatz** — Windows credential/ticket extraction tool. `[06]`
- **Mirai** — IoT botnet spread via Telnet default creds → DDoS. `[18]`
- **MITM** — Man-in-the-Middle (adversary-in-the-middle). `[08][11]`
- **Modbus** — OT protocol, port 502, no auth by design. `[18]`
- **MQTT** — IoT pub/sub messaging over TCP, 1883 (TLS 8883). `[18]`

## N
- **NAC** — Network Access Control; enforces posture/identity (802.1X) before network access; evaded via MAC spoofing / MAB. `[12]`
- **NetBIOS** — legacy Windows naming/session service (137–139). `[04]`
- **NTDS.dit** — the AD database (all domain hashes) on DCs. `[06]`
- **NTLM** — Windows auth protocol; **unsalted** hash → PtH and offline cracking. `[06]`
- **Nikto** — open-source web server vulnerability scanner. `[05][13]`
- **nmap** — the network scanner; scan types + NSE. `[03]`
- **Non-repudiation** — proof a party performed an action and can't deny it (from signatures). `[01][20]`
- **NVD** — National Vulnerability Database (enriches CVEs with CVSS/CPE). `[05]`
- **Null session** — unauthenticated SMB/IPC$ connection leaking users/shares on legacy systems. `[04]`

## O
- **OCSP** — Online Certificate Status Protocol (revocation check). `[20]`
- **OpenVAS / GVM** — open-source vulnerability scanner (Greenbone). `[05]`
- **OPM** — CyberArk On-Demand Privileges Manager; Vault-controlled Unix `sudo`. `[dp]`
- **OSINT** — Open-Source Intelligence. `[02]`
- **OT / ICS** — Operational Technology / Industrial Control Systems. `[18]`
- **OWASP** — Open Worldwide Application Security Project (Top 10 lists). `[14][15]`

## P
- **Padding oracle** — CBC-mode attack that decrypts byte-by-byte via padding error leaks. `[20]`
- **PAM** — Privileged Access Management. `[dp]`
- **PAW** — Privileged Access Workstation. `[dp]`
- **PKI** — Public Key Infrastructure (CA/RA/X.509/CRL). `[20]`
- **PLC / RTU / IED** — Programmable Logic Controller / Remote Terminal Unit / Intelligent Electronic Device. `[18]`
- **PMK / PTK** — Pairwise Master / Transient Key in the WPA2 handshake. `[16]`
- **Polymorphic virus** — mutates its encrypted body (changing decryptor) each time. `[07]`
- **Port security** — limits MACs per switch port; counters MAC flooding. `[08]`
- **Privilege escalation** — vertical (higher privilege) or horizontal (same level, another user). `[06]`
- **PtH / PtT** — Pass-the-Hash / Pass-the-Ticket (reuse creds without cracking). `[06]`
- **PSM / PSMP** — CyberArk Privileged Session Manager / for SSH Proxy; brokers + records sessions. `[dp]`
- **PTA** — CyberArk Privileged Threat Analytics; privileged UEBA (Golden Ticket, PtH, DCSync). `[dp]`
- **PVWA** — CyberArk Password Vault Web Access. `[dp]`

## Q
- **Quid pro quo** — social-engineering attack offering a "service" in exchange for info/access. `[09]`

## R
- **RA** — Registration Authority (verifies identity in PKI). `[20]`
- **Rainbow table** — precomputed hash→plaintext lookup; defeated by salting. `[06][20]`
- **RAT** — Remote Access Trojan. `[07]`
- **RBCD** — Resource-Based Constrained Delegation (Kerberos delegation abuse). `[dp]`
- **RC4** — broken stream cipher; Kerberos RC4 = `0x17` (Kerberoasting tell); WEP/old TLS. `[06][20]`
- **Reconnaissance** — phase 1: information gathering (passive/active). `[01][02]`
- **Responder** — LLMNR/NBT-NS/mDNS poisoner that captures NetNTLM hashes. `[08]`
- **RID cycling** — enumerating accounts by iterating relative IDs on the domain SID (RID 500 = Administrator). `[04]`
- **RoE** — Rules of Engagement; the authorized scope/methods/timing of a test. `[01]`
- **Rogue AP / Rogue DHCP** — unauthorized access point / DHCP server used for MITM. `[08][16]`
- **Rootkit** — hides presence/privilege (user, kernel, boot, hypervisor, firmware levels). `[07]`
- **RSA** — asymmetric algorithm; encryption **and** signatures; factorization-based. `[20]`

## S
- **Spyware** — covertly monitors and exfiltrates user activity (screen/audio/files). `[07]`
- **STRIDE** — threat-modeling categories: Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege. `[01]`
- **SAE** — Simultaneous Authentication of Equals; WPA3's handshake (fixes offline PSK crack). `[16]`
- **SAM** — Security Account Manager; local Windows hash store. `[06]`
- **Salt** — per-hash random value; defeats rainbow tables. `[06][20]`
- **SCADA / DCS** — Supervisory Control And Data Acquisition / Distributed Control System. `[18]`
- **Session fixation** — forcing a known session ID pre-login; fixed by reissuing the ID at auth. `[11]`
- **Session hijacking** — taking over a valid session (network-level or application-level). `[11]`
- **Silver ticket** — forged TGS signed with a service account's key. `[06]`
- **Signature-based IDS** — matches known-bad patterns (vs anomaly-based). `[12]`
- **Slowloris** — application-layer DoS holding many partial HTTP connections open. `[10]`
- **Smishing / Vishing / Whaling** — SMS phishing / voice phishing / exec-targeted phishing. `[09]`
- **Smurf** — ICMP amplification via broadcast (spoofed victim). `[10]`
- **SNMP** — Simple Network Management Protocol; v1/2c cleartext, v3 secure (161). `[04][08]`
- **Shodan / Censys** — search engines indexing internet-exposed devices (query the index — passive). `[02][18]`
- **SPN** — Service Principal Name; the target of Kerberoasting. `[06]`
- **SQLi** — SQL Injection (OWASP A03); in-band/blind/OOB. `[15]`
- **SSRF** — Server-Side Request Forgery; tricks the **server** (OWASP A10). `[14][19]`
- **Steganography** — hiding the *existence* of a message; detection = steganalysis. `[06][20]`
- **SYN scan** (`-sS`) — half-open scan (default, needs root). `[03]`
- **SYN flood / SYN cookies** — half-open connection flood / the stateless mitigation. `[10]`

## T
- **Tailgating / Piggybacking** — following someone through a door without / with their awareness. `[09]`
- **Threat intelligence** — evidence-based threat knowledge; strategic / tactical / operational / technical. `[01]`
- **TTPs** — Tactics, Techniques, and Procedures (how an actor operates; the ATT&CK backbone). `[01]`
- **TGT / TGS** — Ticket-Granting Ticket / Ticket-Granting Service ticket (Kerberos). `[06]`
- **theHarvester** — OSINT tool for emails/subdomains/hosts. `[02]`
- **Tiering (Tier 0/1/2)** — admin-plane isolation model. `[06][dp]`
- **TKIP** — WPA's cipher (deprecated; WPA2 uses AES-CCMP). `[16]`
- **TLS** — Transport Layer Security; hybrid crypto (asymmetric key exchange + symmetric AES-GCM). `[20]`
- **Trojan** — malware disguised as legitimate software (user runs it). `[07]`
- **Tunneling** — smuggling traffic inside an allowed protocol (DNS/ICMP/HTTP) to evade a firewall. `[12]`

## U
- **UEBA** — User and Entity Behavior Analytics. `[12][dp]`
- **UNION-based SQLi** — appends `UNION SELECT` to return extra data (needs matching column count/types). `[15]`
- **Unquoted service path** — Windows privesc via a service path with spaces and no quotes. `[06]`

## V
- **VA** — Vulnerability Assessment (find & rank; a pentest proves impact). `[05]`
- **Vault (Digital Vault / EPV)** — CyberArk encrypted, tamper-evident credential store. `[dp]`
- **VeraCrypt / LUKS / FileVault** — full-disk/volume encryption tools. `[20]`
- **Virus** — malware that attaches to a host file and usually needs the user to run it. `[07]`
- **VSS** — Volume Shadow Copy Service (used to grab NTDS.dit). `[06]`

## W
- **Web API attacks** — BOLA/IDOR, broken auth, mass assignment, excessive data exposure (OWASP API Top 10). `[14]`
- **Webhook** — user-defined HTTP callback; risks: SSRF, missing signature verification, replay. `[14]`
- **WAF** — Web Application Firewall (partial SQLi/XSS control; bypassable via encoding). `[14][15]`
- **War driving** — searching for Wi-Fi networks while moving. `[16]`
- **WEP / WPA / WPA2 / WPA3** — Wi-Fi security: WEP (broken RC4/IV), WPA (TKIP), WPA2 (AES-CCMP), WPA3 (SAE). `[16]`
- **Worm** — self-propagating malware (no host file, spreads over the network). `[07]`
- **WPS** — Wi-Fi Protected Setup; PIN is brute-forceable (Pixie-Dust) — disable it. `[16]`

## X
- **X.509** — certificate format binding identity ↔ public key. `[20]`
- **XMAS scan** (`-sX`) — sets FIN+PSH+URG flags; open ports stay silent (not on Windows). `[03]`
- **XSS** — Cross-Site Scripting (stored / reflected / DOM-based). `[14]`
- **XXE** — XML External Entity injection. `[14]`

## Z
- **Zero-day** — a vulnerability with no patch, unknown to the vendor. `[01]`
- **Zigbee / Z-Wave** — low-power IoT mesh radios. `[18]`
- **Zone transfer** — see **AXFR**. `[02]`
- **ZSP** — Zero Standing Privilege (no durable privileged accounts to steal). `[dp]`

---

## AI & ML security
Terms for [AI-IN-ETHICAL-HACKING.md](AI-IN-ETHICAL-HACKING.md) — CEH v13's AI-driven ethical hacking.
- **Adversarial example / evasion** — perturbed input that causes misclassification (test-time attack).
- **Data / model poisoning** — corrupting training data or the model to implant a backdoor (training-time attack).
- **Model extraction** — querying a model enough to clone its behavior/weights.
- **Model inversion** — reconstructing sensitive training data from model outputs.
- **Membership inference** — determining whether a record was in the training set (privacy leak).
- **Prompt injection** — malicious instructions overriding the system prompt; **direct** (typed) or **indirect** (hidden in ingested content).
- **Jailbreaking (LLM)** — bypassing a model's safety guardrails.
- **Excessive agency** — an AI agent granted more tools/permissions than it should have.
- **Insecure output handling** — trusting LLM output that flows into shell/SQL/eval → classic injection.
- **OWASP LLM Top 10** — the top risks for LLM applications (prompt injection, data disclosure, poisoning, …).
- **MITRE ATLAS** — ATT&CK-style knowledge base for adversarial ML.
- **NIST AI RMF** — AI Risk Management Framework.
