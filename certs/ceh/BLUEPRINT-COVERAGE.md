# CEH v13 — Blueprint Coverage Matrix

A self-audit of what this repo covers, module by module, against the standard CEH v13 subtopics. Use it to confirm nothing major is missing before you sit the exam, and to find the fastest link to any topic.

> **Verify against the source.** This matrix is cross-referenced to widely-documented CEH v13 module subtopics, **not** a copy of EC-Council's proprietary blueprint. Confirm the authoritative topic list and domain weights in the official [CEH v13 brochure](https://www.eccouncil.org/cehv13-brochure/) and record weights in [EXAM-LOGISTICS.md](EXAM-LOGISTICS.md). ✓ = covered in that module's `README.md` (and its companions).

## Cross-cutting

| Topic | Where |
|---|---|
| **AI-driven ethical hacking** (AI to augment phases; attacking/defending AI, LLM Top 10, adversarial ML) | [AI-IN-ETHICAL-HACKING.md](AI-IN-ETHICAL-HACKING.md) |
| Defender / PAM controls for every attack | [defender-pam/](defender-pam/README.md) |
| Exam tactics, study system | [EXAM-STRATEGY.md](EXAM-STRATEGY.md) |
| Terminology | [GLOSSARY.md](GLOSSARY.md) |

## Per-module coverage

### [01 — Introduction to Ethical Hacking](modules/01-introduction-to-ethical-hacking/README.md)
✓ CIA triad · ✓ hacker classes · ✓ hacking methodology (5 phases) · ✓ Cyber Kill Chain · ✓ MITRE ATT&CK · ✓ Diamond Model · ✓ IoC/TTPs · ✓ threat intelligence · ✓ threat modeling (STRIDE) · ✓ risk management · ✓ pentest types (black/white/grey) · ✓ RoE/scope · ✓ laws & standards (PCI-DSS, HIPAA, GDPR, ISO 27001) · ✓ defense-in-depth

### [02 — Footprinting and Reconnaissance](modules/02-footprinting-and-reconnaissance/README.md)
✓ passive vs active · ✓ WHOIS · ✓ DNS records + AXFR · ✓ Google dorking (GHDB) · ✓ Shodan/Censys · ✓ email/website footprinting · ✓ social-media OSINT · ✓ tools (theHarvester, recon-ng, Maltego, HTTrack) · ✓ countermeasures

### [03 — Scanning Networks](modules/03-scanning-networks/README.md)
✓ TCP 3-way handshake · ✓ scan types (SYN/connect/FIN/NULL/XMAS/ACK/UDP) · ✓ port states · ✓ host discovery · ✓ banner grabbing · ✓ OS/version fingerprinting · ✓ IDS/firewall evasion (fragment/decoy/timing/source-port) · ✓ hping3/masscan · ✓ NSE

### [04 — Enumeration](modules/04-enumeration/README.md)
✓ NetBIOS/SMB · ✓ SNMP (v1/2c/v3) · ✓ LDAP · ✓ NTP · ✓ SMTP · ✓ NFS · ✓ RPC · ✓ VoIP/SIP · ✓ IPsec/IKE · ✓ DNS · ✓ null sessions · ✓ RID cycling · ✓ tools (enum4linux, snmpwalk, ldapsearch, ike-scan)

### [05 — Vulnerability Analysis](modules/05-vulnerability-analysis/README.md)
✓ VA vs pentest · ✓ VA lifecycle · ✓ CVSS · ✓ CVE/CWE/CPE/NVD · ✓ scanner types (network/host/app/db) · ✓ authenticated vs unauthenticated · ✓ active vs passive · ✓ false pos/neg · ✓ Nessus/OpenVAS/Nikto · ✓ risk-based prioritization (EPSS)

### [06 — System Hacking](modules/06-system-hacking/README.md)
✓ methodology (gain→escalate→maintain→clear) · ✓ password attacks (taxonomy) · ✓ Windows cred stores (SAM/LSASS/NTDS) · ✓ PtH/PtT/Kerberoasting/AS-REP/golden/silver · ✓ privilege escalation (Win/Linux) · ✓ buffer overflow · ✓ keyloggers/spyware · ✓ executing applications · ✓ rootkits · ✓ steganography · ✓ NTFS ADS · ✓ clearing logs · ✓ rainbow tables vs salt

### [07 — Malware Threats](modules/07-malware-threats/README.md)
✓ malware categories · ✓ virus vs worm vs trojan · ✓ virus types · ✓ malware components (dropper/downloader/…) · ✓ rootkit levels · ✓ fileless/LOLBins · ✓ APT lifecycle · ✓ ransomware · ✓ static vs dynamic analysis + sandbox · ✓ detection (signature/heuristic/integrity) · ✓ IoCs · ✓ countermeasures

### [08 — Sniffing](modules/08-sniffing/README.md)
✓ passive vs active · ✓ hub vs switch/CAM · ✓ MAC flooding/spoofing · ✓ ARP poisoning · ✓ DHCP starvation/rogue · ✓ DNS poisoning variants · ✓ cleartext protocols · ✓ Wireshark filters · ✓ Responder/LLMNR · ✓ defenses (port security/DHCP snooping/DAI)

### [09 — Social Engineering](modules/09-social-engineering/README.md)
✓ SE types (human/computer/mobile) · ✓ phishing family (spear/whaling/vishing/smishing/pharming/BEC/angler) · ✓ pretexting/baiting/quid pro quo/tailgating/piggybacking · ✓ insider threats · ✓ identity theft · ✓ SE lifecycle · ✓ countermeasures (awareness, DMARC/SPF/DKIM, MFA)

### [10 — Denial-of-Service](modules/10-denial-of-service/README.md)
✓ DoS vs DDoS vs DRDoS · ✓ categories (volumetric/protocol/app) · ✓ SYN/UDP/ICMP floods · ✓ amplification/reflection · ✓ Smurf/Fraggle · ✓ Slowloris · ✓ botnets (handler/agent) · ✓ tools (hping3/LOIC/HOIC) · ✓ mitigations (scrubbing/BCP38/SYN cookies)

### [11 — Session Hijacking](modules/11-session-hijacking/README.md)
✓ network vs application level · ✓ TCP seq prediction/desync/RST-FIN · ✓ token theft (XSS/sidejacking) · ✓ session fixation · ✓ predictable IDs · ✓ CSRF relationship · ✓ tools (Burp/ettercap) · ✓ defenses (cookie flags, rotation, TLS/HSTS)

### [12 — Evading IDS, Firewalls & Honeypots](modules/12-evading-ids-firewalls-honeypots/README.md)
✓ IDS vs IPS · ✓ HIDS/NIDS · ✓ signature vs anomaly · ✓ insertion/evasion/DoS · ✓ firewall types · ✓ nmap evasion flags · ✓ tunneling (HTTP/DNS/ICMP) · ✓ NAC & endpoint evasion · ✓ honeypot types · ✓ Snort/Suricata · ✓ detecting honeypots

### [13 — Hacking Web Servers](modules/13-hacking-web-servers/README.md)
✓ web-server vs web-app · ✓ attack methodology · ✓ Apache/Nginx/IIS · ✓ misconfig/default files/source disclosure · ✓ directory traversal · ✓ HTTP methods/WebDAV · ✓ banner grabbing · ✓ tools (Nikto/gobuster/wpscan) · ✓ patch management · ✓ countermeasures

### [14 — Hacking Web Applications](modules/14-hacking-web-applications/README.md)
✓ methodology · ✓ OWASP Top 10 (2021) · ✓ XSS (stored/reflected/DOM) · ✓ CSRF vs SSRF · ✓ IDOR/access control · ✓ command injection · ✓ LFI/RFI · ✓ file upload · ✓ XXE · ✓ deserialization · ✓ broken auth/session · ✓ web APIs/webhooks · ✓ web shells · ✓ Burp/ZAP

### [15 — SQL Injection](modules/15-sql-injection/README.md)
✓ root cause · ✓ types (error/UNION/boolean/time/OOB) · ✓ UNION requirements · ✓ auth bypass · ✓ information_schema · ✓ MSSQL xp_cmdshell / MySQL OUTFILE · ✓ sqlmap · ✓ WAF evasion · ✓ second-order · ✓ defenses (parameterized queries)

### [16 — Hacking Wireless Networks](modules/16-hacking-wireless-networks/README.md)
✓ 802.11 · ✓ WEP/WPA/WPA2/WPA3 (ciphers) · ✓ 4-way handshake (PMK/PTK) · ✓ offline PSK crack · ✓ evil twin/rogue AP · ✓ deauth · ✓ WPS/Pixie-Dust · ✓ aircrack-ng suite · ✓ **Bluetooth hacking** (bluejacking/snarfing/bugging/BlueBorne) · ✓ 802.1X/EAP-TLS · ✓ 802.11w

### [17 — Hacking Mobile Platforms](modules/17-hacking-mobile-platforms/README.md)
✓ Android vs iOS architecture · ✓ OWASP Mobile Top 10 (2024) · ✓ rooting/jailbreaking · ✓ app-flaw quartet · ✓ insecure storage/comms · ✓ mobile malware/repackaging · ✓ SMS-OTP/SIM swap · ✓ MDM/MAM/UEM · ✓ tools (MobSF/Frida/apktool/adb) · ✓ mobile security guidelines

### [18 — IoT and OT Hacking](modules/18-iot-and-ot-hacking/README.md)
✓ IoT architecture/comms models · ✓ IoT protocols+ports (MQTT/CoAP/Zigbee/BLE/LoRaWAN) · ✓ OWASP IoT Top 10 · ✓ Mirai · ✓ IoT attack surface · ✓ OT/ICS vocab (SCADA/PLC/RTU/HMI) · ✓ OT protocols (Modbus/DNP3/S7comm) · ✓ Purdue model · ✓ IEC 62443 · ✓ firmware analysis

### [19 — Cloud Computing](modules/19-cloud-computing/README.md)
✓ IaaS/PaaS/SaaS · ✓ deployment models · ✓ NIST 800-145 · ✓ shared responsibility · ✓ containers/Kubernetes + ports · ✓ serverless/FaaS · ✓ public bucket · ✓ IAM privesc · ✓ IMDS SSRF + IMDSv2 · ✓ container escape · ✓ tools (ScoutSuite/Prowler/Pacu/kube-bench/Trivy)

### [20 — Cryptography](modules/20-cryptography/README.md)
✓ symmetric vs asymmetric · ✓ AES/DES/3DES/RC4/Blowfish/Twofish · ✓ RSA/DH/ECC/ElGamal/DSA · ✓ block modes (ECB/CBC/CTR/GCM) · ✓ hashing (MD5/SHA/RIPEMD) · ✓ KDFs · ✓ PKI/X.509/CRL/OCSP · ✓ digital signatures · ✓ TLS handshake · ✓ disk/email encryption · ✓ **cryptanalysis** (linear/differential/side-channel) · ✓ crypto attacks · ✓ steganography

---

## Known scope notes
- **Domain weights are intentionally not printed** — public sources conflict; get the official blueprint PDF and record them yourself in [EXAM-LOGISTICS.md](EXAM-LOGISTICS.md).
- This repo teaches **concepts and hands-on skills**, not exam items. Pair it with official EC-Council practice.
- If EC-Council revises v13 subtopics, update this matrix and the affected module.
