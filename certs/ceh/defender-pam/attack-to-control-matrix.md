# Attack → Control Matrix

The master mapping. Rows are grouped by CEH v13 module; each row pairs an **attack** with the **detection signal** it typically produces and the **control / PAM lever** that defeats or contains it. Every module's *Defender & PAM mapping* section points back here.

> Read it both directions: attack → "what's the defense?" and control → "what does this defeat?" **Bold** entries are the PAM levers detailed in [pam-playbook.md](pam-playbook.md).

---

## 01 — Introduction / methodology

| Attack / concept | Detection signal | Control / PAM lever |
|---|---|---|
| Recon on the org (whole kill chain) | Baseline anomalies across phases | Defense-in-depth, logging, **least privilege** as the default posture |
| Insider misuse of access | Access outside role/hours | **Least privilege**, separation of duties, access reviews |

## 02 — Footprinting & Reconnaissance

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| OSINT / passive footprinting | (largely invisible) | Minimize public exposure, scrub metadata, brand monitoring |
| DNS / WHOIS enumeration | Bulk DNS queries, AXFR attempts | Disable zone transfers, split-horizon DNS |
| Google/Shodan dorking | External scan mentions | Attack-surface management, remove exposed assets |

## 03 — Scanning Networks

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Port/host scanning (nmap) | Many SYNs, sweeps, timing anomalies | IDS/IPS, firewall deny-by-default, network segmentation |
| Banner grabbing / version scan | Probes to service banners | Minimize banners, patch, reduce exposed services |
| Firewall/IDS evasion (fragmentation, decoys) | Fragmented/odd packets | Reassembly-aware IDS, drop invalid packets |

## 04 — Enumeration

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| SMB/NetBIOS enumeration (139/445) | Null-session attempts, share listing | Disable null sessions, restrict SMB, segment |
| SNMP enumeration (161) | Community-string guesses | **SNMPv3** auth+priv, drop v1/2c |
| LDAP enumeration (389) | Anonymous binds, bulk queries | Require auth binds, LDAPS, limit read scope |
| User/AD enumeration | Bulk lookups, RID cycling | Restrict directory reads, monitor recon tools |

## 05 — Vulnerability Analysis

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Automated vuln scanning | Scanner traffic (Nessus/OpenVAS) | Patch/vuln management, authenticated internal scans, segmentation |
| Exploiting unpatched CVEs | Exploit signatures, crashes | Timely patching, virtual patching (WAF/IPS), **least privilege** to limit blast radius |

## 06 — System Hacking

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Password spraying / brute force | 4625 spikes, lockouts, spray pattern | Lockout policy, MFA, **PAM broker + rate limiting** |
| Kerberoasting | 4769 TGS for SPN accts, RC4 | **gMSA**, strong service passwords, AES-only |
| Pass-the-Hash / Pass-the-Ticket | NTLM/ticket anomalies, unusual host | **Tiered admin**, Protected Users, Credential Guard, **LAPS** |
| LSASS dumping (Mimikatz) | Handle to lsass, Sysmon EID 10 | Credential Guard, LSASS PPL, ASR rules, EDR |
| DCSync / NTDS theft | Replication from non-DC (4662), VSS | **Tier 0 isolation**, monitor replication rights, **vault DA creds** |
| Local admin reuse | Same local hash across hosts | **LAPS**, deny lateral logon |
| Persistence (task/service/run key) | New service/task/autorun | **JIT elevation**, allow-listing, change control |

## 07 — Malware Threats

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Trojan / RAT install | New autorun, beacon, odd parent-child | **App allow-listing** (WDAC/AppLocker), no local admin, EDR |
| Ransomware | Mass encrypt, shadow-copy deletion | Immutable/offline backups, **JIT admin**, segmentation, canary files |
| Rootkit / bootkit | Integrity mismatch, unsigned driver | Secure Boot + HVCI, driver block-list, tamper-protected EDR |
| Fileless / LOLBins | Encoded PowerShell from service acct | Script-block logging, constrained language mode, ASR, **remove standing admin** |
| Botnet / C2 beacon | Periodic outbound to rare host | Egress filtering, proxy, DNS monitoring |

## 08 — Sniffing

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| MAC flooding | CAM full, port flooding | **Port security** (MAC limits), sticky MAC |
| ARP poisoning / MITM | Duplicate-IP/changed-MAC, gratuitous ARP | **Dynamic ARP Inspection**, static ARP for gateways |
| Rogue DHCP / starvation | Unexpected offers, pool exhaustion | **DHCP snooping** (trusted ports) |
| LLMNR/NBT-NS poisoning (Responder) | NetNTLM auth to rogue host | Disable LLMNR/NBT-NS, SMB signing, MFA |
| Cleartext credential sniffing | Plaintext creds in capture | Encrypt everything, **PAM session brokering** |

## 09 — Social Engineering

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Phishing / spear-phishing | Reported mails, lookalike domains | Security awareness, DMARC/DKIM/SPF, **phishing-resistant MFA** |
| Pretexting / vishing | Help-desk anomalies | Identity-verification procedures, callback policy |
| Baiting / tailgating (physical) | Badge anomalies, found USB | Physical controls, device-control (block USB), least privilege |
| Business Email Compromise | Payment-change requests | Out-of-band verification, dual authorization |

## 10 — Denial-of-Service

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Volumetric DDoS (UDP/ICMP flood, amplification) | Bandwidth spike, reflected traffic | Upstream scrubbing/CDN, anti-spoofing (BCP38), rate limiting |
| Protocol attacks (SYN flood) | Half-open connections | SYN cookies, connection limits |
| Application-layer (HTTP flood, Slowloris) | Slow/partial requests | WAF, reverse-proxy timeouts, autoscaling |

## 11 — Session Hijacking

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Session token theft / prediction | Reused/parallel sessions, IP jumps | HttpOnly+Secure+SameSite cookies, rotate on auth, short TTL |
| TCP/network session hijack | Sequence anomalies, RST bursts | Encrypted transport (TLS/SSH), **PAM session isolation** |
| MITM downgrade | Stripped TLS, cert warnings | HSTS, cert pinning, encryption everywhere |

## 12 — Evading IDS, Firewalls & Honeypots

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| IDS evasion (fragmentation, encoding, timing) | Fragmented/obfuscated payloads | Traffic normalization, TLS inspection, behavioral detection |
| Firewall tunneling (DNS/ICMP/HTTP tunnel) | Odd protocol volumes | Egress allow-list, protocol inspection, DNS monitoring |
| Honeypot fingerprinting | Interaction with decoys | Well-built honeypots, deception layering |

## 13 — Hacking Web Servers

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Web server misconfig / default files | Access to admin/default paths | Hardening baselines, remove defaults, patch |
| Directory traversal / source disclosure | `../` patterns, dotfile access | Input validation, run web root least-privilege |
| Web server DoS / defacement | Content change, error spikes | WAF, file-integrity monitoring, **least-privilege service account** |

## 14 — Hacking Web Applications

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| XSS (stored/reflected/DOM) | Script payloads in inputs, CSP reports | Output encoding, **CSP**, HttpOnly/SameSite, WAF |
| Injection (command / SQL — see M15) | Error strings, metacharacters, RCE | Parameterization, avoid shell exec, **least-privilege app account** |
| IDOR / broken access control | Sequential-ID access to others' data | Server-side authorization, deny-by-default |
| SSRF | Requests to internal/link-local IPs | Egress allow-list, block metadata endpoint, IMDSv2 |
| Unrestricted upload → web shell | New script in upload dir | Store off web root, validate type, no-exec upload dir |

## 15 — SQL Injection

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| SQLi (error/union/blind/OOB) | SQL errors, tautologies, sqlmap traffic | **Parameterized queries / prepared statements**, WAF |
| Data exfiltration via SQLi | Large/odd result sets | Least-privilege DB account, network egress limits |
| SQLi → RCE (`xp_cmdshell`, `INTO OUTFILE`) | DB spawning shell/writing files | Disable dangerous features, **least-privilege DB service account** |

## 16 — Hacking Wireless Networks

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| WPA2 handshake capture + crack | Deauth floods, rogue captures | **WPA3**, long passphrase, 802.1X/EAP-TLS |
| Evil twin / rogue AP | Duplicate SSID, signal anomalies | WIPS, 802.1X, certificate-based auth |
| WPS PIN attack | WPS brute force | Disable WPS |
| Deauth DoS | 802.11 deauth frames | 802.11w (management frame protection) |

## 17 — Hacking Mobile Platforms

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Rooted/jailbroken device | Attestation/Play Integrity fail | **MDM conditional access** — block compromised devices |
| Insecure data storage | Secrets in prefs/plist/logs | Keystore/Keychain, MAM containerization |
| Insecure comms / no pinning | MITM succeeds | TLS + cert pinning, network security config |
| SMS OTP intercept / SIM swap | Auth from new device | **Phishing-resistant MFA** (FIDO2/passkeys) over SMS |

## 18 — IoT & OT Hacking

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Default/weak IoT creds | Logins with vendor defaults | Change defaults, unique creds, **vault + rotate** |
| Unpatched firmware exploit | Known-CVE probes | Firmware updates, network segmentation, isolate OT |
| Insecure protocols (Modbus, MQTT, etc.) | Cleartext control traffic | Segment OT/IT, unidirectional gateways, monitor |
| OT/ICS manipulation | Abnormal control commands | Zones/conduits (IEC 62443), **JIT + brokered** vendor access |

## 19 — Cloud Computing

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Misconfigured storage (public bucket) | Public-access flags, anon reads | CSPM, block-public-access, encryption |
| Over-privileged IAM / key leakage | Unused perms, leaked keys, odd API calls | **Least-privilege IAM**, **JIT/short-lived creds**, no long-lived keys |
| SSRF → cloud metadata theft | Requests to 169.254.169.254 | IMDSv2, egress control, role-scoping |
| Cloud lateral movement / privilege esc | Role-chaining, new admin roles | Permission boundaries, guardrails, **PAM for cloud (CIEM)** |

## 20 — Cryptography

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Weak cipher / hash use (MD5, DES, ECB) | Legacy algorithm negotiation | Strong algorithms (AES-GCM, SHA-2/3), disable legacy |
| Offline hash cracking | (post-theft) | Salting + slow KDFs (bcrypt/argon2), protect hash stores |
| MITM / downgrade on TLS | Downgrade attempts, bad certs | TLS 1.2+/1.3, HSTS, cert pinning, PKI hygiene |
| Key mismanagement | Hardcoded/leaked keys | **Vault keys (KMS/HSM)**, rotate, separation of duties |

---

## The five controls that cover the most ground

If you memorize nothing else, memorize what these defeat — they recur across the whole matrix (details in [pam-playbook.md](pam-playbook.md)):

1. **Least privilege + no standing local admin** → malware persistence, privilege escalation, web-shell pivots.
2. **Tiering + JIT elevation** → Pass-the-Hash, lateral movement, ransomware blast radius.
3. **Vault + rotate secrets (+ gMSA/LAPS)** → Kerberoasting, local-admin reuse, leaked cloud keys, IoT defaults.
4. **Phishing-resistant MFA** → phishing, session hijacking, SMS-OTP/SIM-swap, credential stuffing.
5. **Encrypt + segment + broker sessions** → sniffing, MITM, OT exposure, cleartext credential theft.
