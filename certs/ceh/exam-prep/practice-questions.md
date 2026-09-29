# CEH v13 Practice Questions (Unofficial)

A bank of **50+ multiple-choice practice questions** organised by module/topic, each with the correct answer and a short explanation. They are study aids built around standard, documented Certified Ethical Hacker (CEH) v13 concepts.

> ❓ **More questions in the course layer:** per-module [practice questions](../modules/README.md), the [50-question mock](../MOCK-EXAM.md), the [125-question full mock](../MOCK-EXAM-FULL.md) and the [200-question rapid-fire bank](../RAPID-FIRE.md).

> **Unofficial practice questions — NOT real EC-Council exam questions.** These are pedagogical study aids written for this hub to rehearse documented CEH concepts. They are not drawn from, affiliated with, or endorsed by EC-Council, and they do not reproduce any actual exam item. The real exam is **125 questions in 4 hours**; the passing mark is a scaled cut-score (roughly 60–85%).

## How to use these

1. **Cover the answers.** Read the question, commit to an option, *then* reveal the answer line below it.
2. **Read the explanation even when you are right** — the reasoning is the point, not the letter.
3. **Track misses by module.** If you miss two or more in a module, re-read that module before moving on.
4. **Simulate pressure.** In your final week, answer in blocks under a timer (the real exam averages ~1.9 minutes per question).
5. **Pair with the** [12-week study plan](../STUDY-PLAN.md) **schedule and the** [cheat-sheet.md](cheat-sheet.md) **for the facts these questions lean on.**

> **Acronyms** are expanded on first use throughout. A consolidated list lives in [../reference/acronyms.md](../reference/acronyms.md).

---

## Module 1 — Introduction to Ethical Hacking

**Q1.** What single requirement most clearly separates an ethical hacker from a malicious attacker performing identical actions?
- A. Explicit written authorisation and a defined scope
- B. Use of automated tools
- C. Working only at night
- D. Holding a certification

**Answer: A.** The same packets are legal or criminal depending on authorisation. Written permission and a defined scope (Rules of Engagement) are what make the activity lawful.

**Q2.** Which sequence lists the 5 phases of ethical hacking in the correct order?
- A. Scanning → Reconnaissance → Gaining Access → Clearing Tracks → Maintaining Access
- B. Gaining Access → Reconnaissance → Scanning → Maintaining Access → Clearing Tracks
- C. Reconnaissance → Gaining Access → Scanning → Maintaining Access → Clearing Tracks
- D. Reconnaissance → Scanning → Gaining Access → Maintaining Access → Clearing Tracks

**Answer: D.** You gather information, probe for openings, exploit, persist, then erase evidence. This order underpins the whole methodology.

**Q3.** A "white-hat" hacker is best described as someone who:
- A. Attacks systems for personal financial gain
- B. Operates in a legal grey area without permission but with good intent
- C. Tests systems with the owner's permission to improve security
- D. Only writes malware for research

**Answer: C.** White-hats operate with authorisation. The "grey area without permission" describes a grey-hat; financially motivated attack describes a black-hat.

**Q4.** In the Cyber Kill Chain, which stage involves delivering a weaponised payload to the target (for example, via a phishing email)?
- A. Reconnaissance
- B. Weaponization
- C. Delivery
- D. Actions on Objectives

**Answer: C.** Delivery is the transmission of the weaponised payload. Weaponization is *building* it; Reconnaissance precedes both.

---

## Module 2 — Footprinting and Reconnaissance

**Q5.** Which activity is **passive** reconnaissance?
- A. Running an Nmap port scan against the target
- B. Reviewing the target's public WHOIS and LinkedIn data
- C. Performing a DNS zone transfer attempt
- D. Banner grabbing on port 80

**Answer: B.** Passive recon gathers information without touching the target's systems. Scanning, zone-transfer attempts, and banner grabbing all send packets to the target (active).

**Q6.** "Google dorking" refers to:
- A. Brute-forcing Google account passwords
- B. Poisoning Google's search index
- C. Using advanced search operators to surface exposed or sensitive information
- D. Scanning Google's IP ranges

**Answer: C.** Operators such as `site:`, `filetype:`, and `intitle:` narrow searches to expose documents and pages an organisation did not intend to publicise.

**Q7.** A WHOIS lookup is most useful for discovering:
- A. Open TCP ports on a web server
- B. Active user sessions
- C. The operating-system version of a host
- D. Domain registration, registrar, and (sometimes) contact details

**Answer: D.** WHOIS returns registration metadata. Port/OS data come from scanning, not WHOIS.

**Q8.** Which DNS record type maps a hostname to an IPv4 address and is a common footprinting target?
- A. MX
- B. A
- C. TXT
- D. CNAME

**Answer: B.** An **A** record maps a name to an IPv4 address. MX is for mail exchangers, TXT for arbitrary text (such as SPF), CNAME for aliases.

---

## Module 3 — Scanning Networks

**Q9.** A TCP **SYN scan** (half-open scan) is considered relatively stealthy because it:
- A. Uses encryption to hide the probe
- B. Sends no packets to the target
- C. Never completes the three-way handshake, so fewer full connections are logged
- D. Spoofs the destination address

**Answer: C.** The scanner sends SYN, receives SYN/ACK, then sends RST instead of ACK — the connection is never fully established, so some logging is avoided.

**Q10.** In a TCP scan, an open port typically responds to a SYN with which flags set?
- A. RST
- B. URG/PSH
- C. FIN
- D. SYN/ACK

**Answer: D.** An open port answers a SYN with SYN/ACK. A closed port replies with RST.

**Q11.** Which scan sends packets with the FIN, PSH, and URG flags all set?
- A. NULL scan
- B. ACK scan
- C. Xmas scan
- D. Connect scan

**Answer: C.** The Xmas scan lights up FIN, PSH, and URG ("like a Christmas tree"). A NULL scan sends no flags at all.

**Q12.** What is the main downside of a TCP **full-connect** scan compared with a SYN scan?
- A. It completes the handshake and is therefore more likely to be logged
- B. It cannot detect open ports
- C. It only works over UDP
- D. It requires no privileges yet is stealthier

**Answer: A.** A full-connect scan finishes the handshake, making it reliable but noisy and easily logged. (It does, however, work without raw-socket privileges.)

**Q13.** Which technique determines a remote host's operating system by analysing subtle differences in its TCP/IP stack responses?
- A. OS fingerprinting
- B. Banner grabbing
- C. ARP poisoning
- D. War driving

**Answer: A.** OS fingerprinting infers the OS from stack behaviour (TTL, window size, flag handling). Banner grabbing reads service banners, which is related but distinct.

---

## Module 4 — Enumeration

**Q14.** Enumeration differs from scanning primarily in that it:
- A. Only identifies which hosts are alive
- B. Requires no connection to the target
- C. Is always passive
- D. Actively extracts detailed resources such as usernames, shares, and services

**Answer: D.** Enumeration establishes active connections to pull specific resources (user accounts, shares, group names), going deeper than the "what is open" of scanning.

**Q15.** A DNS **zone transfer** (AXFR) can be dangerous to an organisation because it may:
- A. Crash the DNS server
- B. Reveal a full list of internal hostnames and addresses if misconfigured
- C. Encrypt all DNS traffic
- D. Redirect the domain to a new registrar

**Answer: B.** If a server permits unauthorised AXFR, an attacker can download the entire zone, exposing the internal naming map.

**Q16.** Which protocol, when left with default community strings like "public", is a classic enumeration target?
- A. SNMP
- B. SMTP
- C. NTP
- D. HTTP

**Answer: A.** Simple Network Management Protocol (SNMP) with default read community strings (e.g., "public") leaks device and network configuration data.

**Q17.** NetBIOS enumeration over SMB is most associated with discovering:
- A. Wireless access points
- B. TLS certificate chains
- C. Windows shares, sessions, and user/machine names
- D. Cloud storage buckets

**Answer: C.** NetBIOS/SMB enumeration exposes Windows file shares, logged-on users, and machine names.

---

## Module 5 — Vulnerability Analysis

**Q18.** The Common Vulnerability Scoring System (CVSS) base score expresses:
- A. The financial cost of a breach
- B. The patch release date
- C. The number of affected hosts
- D. The intrinsic severity of a vulnerability on a 0.0–10.0 scale

**Answer: D.** CVSS base scores rate severity from 0.0 to 10.0, independent of any specific environment.

**Q19.** A CVSS base score of **8.1** falls into which severity band?
- A. Low
- B. Medium
- C. High
- D. Critical

**Answer: C.** The standard CVSS v3.x bands are None (0.0), Low (0.1–3.9), Medium (4.0–6.9), High (7.0–8.9), Critical (9.0–10.0). 8.1 is High.

**Q20.** A vulnerability scanner reports a flaw that does not actually exist on the target. This is a:
- A. True positive
- B. True negative
- C. False negative
- D. False positive

**Answer: D.** A false positive is a reported issue that is not real. A *false negative* — a missed real issue — is the more dangerous error.

---

## Module 6 — System Hacking

**Q21.** A **rainbow table** attack speeds up password cracking by:
- A. Guessing passwords in real time over the network
- B. Sniffing cleartext credentials
- C. Exploiting a buffer overflow
- D. Using precomputed hash-to-plaintext lookup tables

**Answer: D.** Rainbow tables trade storage for speed by precomputing hashes. A unique per-password **salt** defeats them, which is why salting is standard.

**Q22.** Which attack tries every possible combination of characters until the password is found?
- A. Brute-force attack
- B. Dictionary attack
- C. Hybrid attack
- D. Rainbow-table attack

**Answer: A.** Brute force is exhaustive. A dictionary attack uses a wordlist; a hybrid mixes a wordlist with mutations.

**Q23.** Hiding data inside an image file so its very existence is concealed is called:
- A. Encryption
- B. Hashing
- C. Steganography
- D. Tokenisation

**Answer: C.** Steganography conceals the *existence* of a message (e.g., inside image pixels). Encryption conceals the *content* but not that a message exists.

**Q24.** Moving from a standard user account to administrative/root rights on a compromised host is:
- A. Lateral movement
- B. Privilege escalation
- C. Pivoting
- D. Defense evasion

**Answer: B.** Privilege escalation raises the attacker's rights vertically. Lateral movement and pivoting move *across* systems at a similar privilege level.

---

## Module 7 — Malware Threats

**Q25.** Which malware type requires a host file or program to attach to and needs user action to spread?
- A. Worm
- B. Virus
- C. Logic bomb
- D. Rootkit

**Answer: B.** A virus attaches to a host file and typically needs the user to run it. A **worm** self-propagates across networks without user action.

**Q26.** A rootkit's defining characteristic is that it:
- A. Encrypts files for ransom
- B. Records keystrokes only
- C. Floods a network with traffic
- D. Hides its presence and maintains privileged, stealthy access

**Answer: D.** Rootkits subvert the system to conceal processes, files, and access, often at the kernel level, to maintain stealthy control.

**Q27.** Examining malware behaviour by executing it in a sandbox is:
- A. Static analysis
- B. Heuristic hashing
- C. Signature analysis
- D. Dynamic analysis

**Answer: D.** Dynamic analysis runs the sample and observes behaviour. Static analysis inspects the file without executing it.

---

## Module 8 — Sniffing

**Q28.** ARP poisoning enables a man-in-the-middle attack on a switched LAN by:
- A. Overflowing the switch CAM table
- B. Associating the attacker's MAC address with a victim's IP address
- C. Forging DNS responses
- D. Spoofing TLS certificates

**Answer: B.** By sending forged Address Resolution Protocol (ARP) replies, the attacker maps a target IP to their own Media Access Control (MAC) address, so traffic flows through them.

**Q29.** MAC flooding aims to:
- A. Encrypt switch traffic
- B. Spoof an IP address
- C. Disable the wireless radio
- D. Overwhelm a switch's CAM table so it floods frames like a hub

**Answer: D.** When the Content-Addressable Memory (CAM) table is full, many switches "fail open" and broadcast frames, letting the attacker sniff traffic.

**Q30.** Passive sniffing is generally only effective on:
- A. A switched network with port security
- B. A hub-based or already-mirrored network segment
- C. An encrypted VPN tunnel
- D. A wireless network with WPA3

**Answer: B.** Passive sniffing works where traffic is already visible (a hub or a mirror/SPAN port). Switched networks require active techniques like ARP poisoning.

---

## Module 9 — Social Engineering

**Q31.** A targeted phishing email crafted for a specific high-value individual (such as a CFO) is called:
- A. Vishing
- B. Spear phishing
- C. Smishing
- D. Pharming

**Answer: B.** Spear phishing targets specific individuals. *Whaling* is spear phishing aimed at senior executives; vishing is voice-based; smishing is SMS-based.

**Q32.** Following an authorised employee through a secure door without badging in is:
- A. Pretexting
- B. Quid pro quo
- C. Baiting
- D. Tailgating

**Answer: D.** Tailgating (piggybacking) exploits physical courtesy to bypass access control. The strongest defence is security awareness and physical controls like mantraps.

**Q33.** Leaving a malware-loaded USB drive in a parking lot hoping someone plugs it in is an example of:
- A. Baiting
- B. Vishing
- C. Shoulder surfing
- D. Dumpster diving

**Answer: A.** Baiting relies on curiosity/greed around a physical or digital "bait". Endpoint controls that block autorun and unknown USB devices mitigate it.

---

## Module 10 — Denial-of-Service

**Q34.** What distinguishes a DDoS from a DoS attack?
- A. DDoS uses encryption
- B. DDoS only targets web servers
- C. DDoS originates from many distributed, often botnet-controlled, sources
- D. DDoS is always volumetric

**Answer: C.** A Distributed Denial-of-Service uses many sources (commonly a botnet), making it harder to block and far higher in volume than a single-source DoS.

**Q35.** A SYN flood is best categorised as which type of DoS attack?
- A. Application-layer
- B. Protocol/state-exhaustion
- C. Volumetric reflection
- D. Logic bomb

**Answer: B.** A SYN flood exhausts the target's connection-state resources by leaving half-open TCP connections — a protocol/state-exhaustion attack.

**Q36.** A network of compromised machines controlled by an attacker to launch coordinated attacks is a:
- A. Honeynet
- B. Botnet
- C. Sinkhole
- D. Subnet

**Answer: B.** A botnet is a collection of "bots" (zombies) under a command-and-control (C2) infrastructure, frequently used for DDoS and spam.

---

## Module 11 — Session Hijacking

**Q37.** Stealing a valid session token to impersonate an authenticated user is:
- A. Privilege escalation
- B. ARP poisoning
- C. Session hijacking
- D. SQL injection

**Answer: C.** Session hijacking takes over an established session via a stolen or predicted token. Binding sessions to attributes and using secure, HttpOnly cookies over TLS reduces the risk.

**Q38.** Which control most directly reduces the risk of session-token theft over the network?
- A. Enforcing TLS/encryption end-to-end
- B. Disabling ICMP
- C. Increasing the MTU
- D. Using a faster CPU

**Answer: A.** Transport Layer Security (TLS) encrypts the token in transit, defeating sniffing-based hijacking. Cleartext sessions are trivially captured.

---

## Module 12 — Evading IDS, Firewalls, and Honeypots

**Q39.** A signature-based Intrusion Detection System (IDS) primarily detects:
- A. Traffic matching known attack patterns
- B. Any deviation from a learned baseline
- C. Encrypted traffic content
- D. Only insider threats

**Answer: A.** Signature-based IDS matches known patterns and so misses novel attacks. Anomaly-based IDS flags deviations from a baseline but generates more false positives.

**Q40.** A honeypot is best described as:
- A. A decoy system designed to attract and study attackers
- B. A hardened production server
- C. A firewall rule set
- D. An encrypted backup vault

**Answer: A.** Honeypots lure attackers to a controlled decoy so defenders can observe techniques and divert activity away from real assets.

**Q41.** Splitting a malicious payload across many small IP fragments to slip past inspection is:
- A. Fragmentation evasion
- B. Tunnelling
- C. Source routing
- D. Banner grabbing

**Answer: A.** Fragmentation evasion exploits inconsistent reassembly between the IDS and the host. Proper reassembly/normalisation on the sensor counters it.

---

## Module 13–14 — Hacking Web Servers and Web Applications

**Q42.** In the OWASP Top 10, an attack that injects malicious script into pages viewed by other users is:
- A. SQL injection
- B. Server-Side Request Forgery
- C. Cross-Site Scripting (XSS)
- D. Security misconfiguration

**Answer: C.** Open Web Application Security Project (OWASP) classifies Cross-Site Scripting under Injection. Output encoding and a Content Security Policy mitigate it.

**Q43.** Accessing files outside the web root using sequences like `../../etc/passwd` is:
- A. Directory/path traversal
- B. Cross-Site Request Forgery
- C. Clickjacking
- D. DNS poisoning

**Answer: A.** Path traversal abuses unsanitised file paths to escape the intended directory. Input validation and canonicalisation prevent it.

**Q44.** Leaving default credentials, verbose error pages, or unnecessary services enabled falls under which OWASP Top 10 category?
- A. Cryptographic Failures
- B. Identification and Authentication Failures
- C. Vulnerable and Outdated Components
- D. Security Misconfiguration

**Answer: D.** Security Misconfiguration covers insecure defaults, unnecessary features, and revealing errors. Hardening baselines address it.

---

## Module 15 — SQL Injection

**Q45.** The single most effective defence against SQL injection is:
- A. Using parameterised queries (prepared statements)
- B. Hiding the database version
- C. Renaming database tables
- D. Disabling JavaScript

**Answer: A.** Parameterised queries separate code from data so user input can never be interpreted as SQL. Input validation and least privilege are supporting controls.

**Q46.** A SQL-injection technique where the attacker infers data from the application's true/false behaviour rather than visible output is:
- A. Blind (inferential) injection
- B. In-band (error-based) injection
- C. Out-of-band injection
- D. Union-based injection

**Answer: A.** Blind injection extracts data through observed behaviour (responses or timing) when no direct output is returned.

---

## Module 16 — Hacking Wireless Networks

**Q47.** Which wireless security protocol is broken and should never be used today?
- A. WPA2
- B. WPA3
- C. WEP
- D. WPA2-Enterprise

**Answer: C.** Wired Equivalent Privacy (WEP) uses weak RC4 keying and is trivially cracked. WPA2/WPA3 are the modern choices.

**Q48.** An "evil twin" attack works by:
- A. Cloning a MAC address on a switch
- B. Flooding the CAM table
- C. Standing up a rogue access point that mimics a legitimate SSID
- D. Injecting SQL into a captive portal

**Answer: C.** The evil twin advertises a familiar Service Set Identifier (SSID) so victims connect to the attacker's access point, enabling interception.

**Q49.** A deauthentication attack against Wi-Fi clients is used to:
- A. Encrypt traffic
- B. Force clients to disconnect (and often reconnect, exposing handshakes)
- C. Increase signal strength
- D. Assign new IP addresses

**Answer: B.** Deauth frames knock clients off, useful for capturing the reconnection handshake or driving them to an evil twin. WPA3 and management-frame protection reduce this.

---

## Module 17–19 — Mobile, IoT/OT, and Cloud

**Q50.** In the cloud **shared-responsibility model** for Infrastructure as a Service (IaaS), the customer is generally responsible for:
- A. The physical data-centre security
- B. The hypervisor
- C. The guest operating system, applications, and data configuration
- D. The underlying network hardware

**Answer: C.** Under IaaS, the provider secures the physical and virtualisation layers; the customer secures the OS, apps, and data. Misconfiguration on the customer side is a leading cloud breach cause.

**Q51.** A common, high-impact weakness in IoT and OT devices is:
- A. Excessive use of TLS
- B. Hard-coded or default credentials that are rarely changed
- C. Too-frequent firmware updates
- D. Mandatory multi-factor authentication

**Answer: B.** Internet of Things (IoT) and Operational Technology (OT) devices frequently ship with default/hard-coded credentials and seldom get patched, making them easy targets.

**Q52.** SCADA systems are most associated with which environment?
- A. Consumer mobile apps
- B. Cloud billing
- C. Public DNS resolution
- D. Industrial control and critical-infrastructure operations

**Answer: D.** Supervisory Control and Data Acquisition (SCADA) systems monitor and control industrial processes (power, water, manufacturing), a core OT concern.

---

## Module 20 — Cryptography

**Q53.** Which best describes symmetric encryption?
- A. It uses a public/private key pair
- B. It requires a certificate authority
- C. It produces a fixed-length irreversible digest
- D. It uses the same secret key to encrypt and decrypt

**Answer: D.** Symmetric ciphers (such as the Advanced Encryption Standard, AES) use one shared key. Asymmetric crypto uses a key *pair*; hashing is the irreversible-digest option.

**Q54.** A hash function such as SHA-256 is primarily used to provide:
- A. Integrity via a fixed-length, one-way digest
- B. Confidentiality of large files
- C. Key exchange over an untrusted channel
- D. Non-repudiation by itself

**Answer: A.** Hashes give integrity: same input → same digest, and the process is one-way. Encryption (not hashing) provides confidentiality.

**Q55.** In asymmetric cryptography, to send a confidential message you encrypt it with the recipient's:
- A. Private key
- B. Public key
- C. Symmetric session key only
- D. Hash

**Answer: B.** Encrypting with the recipient's *public* key means only their *private* key can decrypt it. (Signing, by contrast, uses the sender's private key.)

**Q56.** Public Key Infrastructure (PKI) primarily exists to:
- A. Generate random passwords
- B. Bind public keys to verified identities via certificates and a trust chain
- C. Encrypt disks at rest
- D. Detect intrusions

**Answer: B.** PKI uses Certificate Authorities (CAs) to issue and validate certificates that bind public keys to identities, establishing trust.

---

## Where to go next

- [../STUDY-PLAN.md](../STUDY-PLAN.md) — the week-by-week schedule these questions support.
- [cheat-sheet.md](cheat-sheet.md) — ports, scan types, CVSS bands, and tools to memorise.
- [../00-overview/what-is-ceh.md](../00-overview/what-is-ceh.md) — program and credential overview.
- [../reference/acronyms.md](../reference/acronyms.md) — full acronym list.

## Sources

- EC-Council, Certified Ethical Hacker (CEH) v13 module structure and concepts — https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/
- OWASP, OWASP Top 10 web application security risks — https://owasp.org/www-project-top-ten/
- FIRST.org, Common Vulnerability Scoring System (CVSS) specification and severity bands — https://www.first.org/cvss/
- Sibling hub page: [../00-overview/what-is-ceh.md](../00-overview/what-is-ceh.md)
- Verified ground truth for this study hub (CEH v13; 312-50v13; 125 Q / 4 h; scaled 60–85% pass; 20 modules; 5 phases).
- These practice questions are original study aids for this hub and are **not** EC-Council exam items.
