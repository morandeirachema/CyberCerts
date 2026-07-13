# CEH v13 — Glossary & Acronym Index

Fast-retrieval definitions for the acronym-dense CEH syllabus. Keep it open while you study — CEH questions frequently hinge on knowing exactly what an acronym expands to and does. `[NN]` points to the most relevant [module](modules/).

> **Seed note.** This index is seeded across all 20 modules with extra depth on the pilot modules (06, 15, 20); it expands as the per-module companions roll out. Missing a term? Add it in a PR.

---

## A
- **AAA** — Authentication, Authorization, Accounting.
- **ADS** — Alternate Data Stream (NTFS); hides data in `file:stream`. Anti-forensics. `[06]`
- **AES** — Advanced Encryption Standard (Rijndael); symmetric block cipher, 128/192/256-bit, FIPS 197. `[20]`
- **APT** — Advanced Persistent Threat; stealthy, persistent, funded actor. `[07]`
- **ARP** — Address Resolution Protocol; no auth → ARP poisoning enables MITM. `[08]`
- **AS-REP roasting** — cracking the AS-REP of accounts with Kerberos pre-auth disabled. `[06]`
- **ASLR** — Address Space Layout Randomization; exploit mitigation.

## B
- **BEC** — Business Email Compromise. `[09]`
- **BLE** — Bluetooth Low Energy; short-range IoT radio. `[18]`
- **bcrypt / scrypt / Argon2 / PBKDF2** — slow, salted password-hashing KDFs. `[20]`
- **Birthday attack** — hash-collision attack, ~2^(n/2) work. `[20]`
- **Botnet** — network of compromised hosts under C2. `[07][10]`

## C
- **C2 / C&C** — Command and Control (attacker infrastructure). `[07]`
- **CA** — Certificate Authority; issues/signs certs in PKI. `[20]`
- **CBC** — Cipher Block Chaining mode; padding-oracle target. `[20]`
- **CCP** — CyberArk Central Credential Provider; removes hardcoded app credentials. `[defender-pam]`
- **CIA** — Confidentiality, Integrity, Availability.
- **CPM** — CyberArk Central Policy Manager; rotates/verifies/reconciles credentials. `[defender-pam]`
- **CRL** — Certificate Revocation List. `[20]`
- **CSRF** — Cross-Site Request Forgery; tricks the **browser** into a state-changing request. `[14]`
- **CVE / CVSS** — Common Vulnerabilities and Exposures / Common Vulnerability Scoring System. `[05]`

## D
- **DAI** — Dynamic ARP Inspection; counters ARP poisoning. `[08]`
- **DCSync** — abuse of AD replication rights to pull hashes (incl. krbtgt) from a DC. `[06]`
- **DES / 3DES** — Data Encryption Standard (56-bit, broken) / Triple DES (legacy). `[20]`
- **DH / ECDHE** — Diffie-Hellman / Ephemeral Elliptic-Curve DH; **key exchange** (ECDHE = forward secrecy). `[20]`
- **DHCP snooping** — switch feature countering rogue DHCP. `[08]`
- **DLP** — Data Loss Prevention.
- **DNP3** — OT/SCADA protocol (utilities), port 20000. `[18]`
- **DoS / DDoS** — Denial / Distributed Denial of Service. `[10]`
- **DPA** — CyberArk Dynamic Privileged Access; agentless JIT/ZSP to VMs & cloud. `[defender-pam]`
- **DSA** — Digital Signature Algorithm; **signatures only**. `[20]`

## E
- **ECB** — Electronic Code Book mode; leaks patterns — never use. `[20]`
- **ECC** — Elliptic Curve Cryptography; RSA-equivalent security, smaller keys. `[20]`
- **EDR** — Endpoint Detection and Response.
- **EPM** — CyberArk Endpoint Privilege Manager; removes local admin, app control, credential-theft blocking. `[defender-pam]`
- **EPV** — CyberArk Enterprise Password Vault (Digital Vault). `[defender-pam]`
- **ESC1–8** — ADCS certificate-abuse techniques (Certified Pre-Owned). `[defender-pam]`

## F
- **FaaS** — Function as a Service (serverless). `[19]`
- **FIDO2 / passkeys** — phishing-resistant authentication. `[09][17]`
- **Forward secrecy** — session keys aren't compromised if the long-term key later is (ephemeral DH). `[20]`

## G
- **GCM** — Galois/Counter Mode; authenticated encryption (confidentiality + integrity). `[20]`
- **gMSA** — Group Managed Service Account; 128-char auto-rotated password → defeats Kerberoasting. `[06]`
- **Golden ticket** — forged TGT signed with the krbtgt hash. `[06]`

## H
- **HIDS / NIDS** — Host / Network Intrusion Detection System. `[12]`
- **HMI** — Human-Machine Interface (OT operator screen). `[18]`
- **HSM** — Hardware Security Module; protects keys (e.g., Vault Server Key). `[20]`
- **HSTS** — HTTP Strict Transport Security. `[11]`

## I
- **IAM** — Identity and Access Management. `[19]`
- **IDOR** — Insecure Direct Object Reference; broken access control (OWASP A01). `[14]`
- **IDS / IPS** — Intrusion Detection (passive) / Prevention (inline block) System. `[12]`
- **IEC 62443** — OT/ICS security standard (zones & conduits). `[18]`
- **IMDS / IMDSv2** — Instance Metadata Service; SSRF steals role creds via 169.254.169.254; IMDSv2 mitigates. `[19]`
- **IoC** — Indicator of Compromise. `[07]`
- **IV** — Initialization Vector (randomizes CBC/CTR). `[20]`

## J
- **JIT** — Just-in-Time (privilege granted for a task, time-boxed). `[06][defender-pam]`

## K
- **KDF** — Key Derivation Function (bcrypt/scrypt/Argon2/PBKDF2). `[20]`
- **Kerberoasting** — request a TGS for an SPN and crack the **service account** password offline. `[06]`
- **krbtgt** — the AD account whose hash signs all TGTs; basis of golden tickets. `[06]`

## L
- **LAPS** — Local Administrator Password Solution; unique rotated local-admin password per host. `[06]`
- **LFI / RFI** — Local / Remote File Inclusion. `[14]`
- **LLMNR / NBT-NS** — name-resolution protocols abused by Responder to capture NetNTLM. `[08]`
- **LOLBin** — Living-Off-the-Land Binary (trusted signed binary abused, e.g. certutil). `[07]`
- **LSASS** — Local Security Authority Subsystem Service; memory holds creds/tickets (Mimikatz target). `[06]`

## M
- **MAM / MDM** — Mobile Application / Device Management. `[17]`
- **MFA** — Multi-Factor Authentication. `[09]`
- **MITM** — Man-in-the-Middle (adversary-in-the-middle). `[08][11]`
- **Modbus** — OT protocol, port 502, no auth by design. `[18]`
- **MQTT** — IoT pub/sub messaging over TCP, port 1883 (TLS 8883). `[18]`

## N
- **NTDS.dit** — the AD database (all domain hashes) on DCs. `[06]`
- **NTLM** — Windows auth protocol; **unsalted** hash → PtH and offline cracking. `[06]`

## O
- **OCSP** — Online Certificate Status Protocol (revocation check). `[20]`
- **OPM** — CyberArk On-Demand Privileges Manager; Vault-controlled Unix `sudo`. `[defender-pam]`
- **OSINT** — Open-Source Intelligence. `[02]`
- **OT / ICS** — Operational Technology / Industrial Control Systems. `[18]`
- **OWASP** — Open Worldwide Application Security Project (Top 10 lists). `[14][15]`

## P
- **PAM** — Privileged Access Management. `[defender-pam]`
- **PAW** — Privileged Access Workstation. `[defender-pam]`
- **PKI** — Public Key Infrastructure (CA/RA/X.509/CRL). `[20]`
- **PLC / RTU / IED** — Programmable Logic Controller / Remote Terminal Unit / Intelligent Electronic Device. `[18]`
- **PtH / PtT** — Pass-the-Hash / Pass-the-Ticket (reuse creds without cracking). `[06]`
- **PSM / PSMP** — CyberArk Privileged Session Manager / for SSH Proxy; brokers + records sessions. `[defender-pam]`
- **PTA** — CyberArk Privileged Threat Analytics; privileged UEBA (Golden Ticket, PtH, DCSync). `[defender-pam]`
- **PVWA** — CyberArk Password Vault Web Access. `[defender-pam]`

## R
- **RA** — Registration Authority (verifies identity in PKI). `[20]`
- **RAT** — Remote Access Trojan. `[07]`
- **RBCD** — Resource-Based Constrained Delegation (Kerberos delegation abuse). `[defender-pam]`
- **RC4** — broken stream cipher; Kerberos RC4 = `0x17` (Kerberoasting tell). `[06][20]`
- **RSA** — asymmetric algorithm; encryption **and** signatures; factorization-based. `[20]`

## S
- **SAM** — Security Account Manager; local Windows hash store. `[06]`
- **SCADA / DCS** — Supervisory Control And Data Acquisition / Distributed Control System. `[18]`
- **Silver ticket** — forged TGS signed with a service account's key. `[06]`
- **SNMP** — Simple Network Management Protocol; v1/2c cleartext community strings, v3 secure. `[04][08]`
- **SPN** — Service Principal Name; the target of Kerberoasting. `[06]`
- **SQLi** — SQL Injection (OWASP A03). `[15]`
- **SSRF** — Server-Side Request Forgery; tricks the **server** (OWASP A10). `[14][19]`
- **Steganography** — hiding the *existence* of a message; detection = steganalysis. `[06][20]`

## T
- **TGT / TGS** — Ticket-Granting Ticket / Ticket-Granting Service ticket (Kerberos). `[06]`
- **TLS** — Transport Layer Security; hybrid crypto (asymmetric key exchange + symmetric AES-GCM). `[20]`
- **Tiering (Tier 0/1/2)** — admin-plane isolation model. `[06][defender-pam]`
- **Trojan** — malware disguised as legitimate software (user runs it). `[07]`

## U
- **UEBA** — User and Entity Behavior Analytics. `[12][defender-pam]`
- **UNION-based SQLi** — appends `UNION SELECT` to return extra data. `[15]`

## V
- **VSS** — Volume Shadow Copy Service (used to grab NTDS.dit). `[06]`
- **Vault (Digital Vault / EPV)** — CyberArk encrypted, tamper-evident credential store. `[defender-pam]`

## W
- **WAF** — Web Application Firewall (partial SQLi/XSS control; bypassable). `[14][15]`
- **WPA2/WPA3** — Wi-Fi Protected Access; WPA3 removes the crackable handshake. `[16]`
- **Worm** — self-propagating malware (no host file, spreads over the network). `[07]`

## X
- **X.509** — certificate format binding identity ↔ public key. `[20]`
- **XSS** — Cross-Site Scripting (stored / reflected / DOM-based). `[14]`
- **XXE** — XML External Entity injection. `[14]`

## Z
- **ZSP** — Zero Standing Privilege (no durable privileged accounts to steal). `[defender-pam]`
- **Zigbee / Z-Wave** — low-power IoT mesh radios. `[18]`
