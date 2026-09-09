# Security+ (SY0-701) Full Mock Exam (Unofficial)

A **full-length, timed mock exam** for the CompTIA Security+ (SY0-701) certification: **85 multiple-choice questions** in mixed domain order, followed by **5 performance-based (PBQ) style scenarios** rendered as text tasks. Every item is an **original study aid written for this hub** and grounded in the five [domain pages](../domains/README.md); none is a real or reconstructed CompTIA exam item. The answer key is at the end, in its own section, so you can cover it.

> **Unofficial mock, not CompTIA content.** Not affiliated with or endorsed by CompTIA. The real exam format quoted below comes from CompTIA's official Security+ page as recorded in this hub's [exam & objectives](../00-overview/exam-and-objectives.md) page; *verify volatile details on CompTIA* before you book: https://www.comptia.org/en-us/certifications/security/

## Rules

The real SY0-701 exam is a **maximum of 90 questions** (multiple-choice plus performance-based), **90 minutes** long, with a passing score of **750 on a 100 to 900 scaled scale**. This mock mirrors that shape: 85 MCQ plus 5 PBQ scenarios = 90 items. **Sit it in one timed block of 90 minutes**, closed book, no pausing, no looking at the domain pages. Answer every item; there is no penalty for guessing. The PBQs are placed at the end here so the numbering stays simple, but on the real exam they typically open the test and eat the clock, so a fair rehearsal is to do **Part B first**, then Part A, and stop at 90 minutes wherever you are.

> **Pass line for this repo's readiness gate: 85%.** That threshold comes from the repo's own [how to prepare a certification](../../../learning/how-to-prepare-a-cert.md) method and the hub [README](../README.md), **not** from CompTIA. CompTIA's 750 is a *scaled* score with an undisclosed raw mapping; it is not "85% correct". The 85% rule is deliberately conservative so that a pass here leaves margin on the real exam.

## How to score

1. Mark each MCQ right or wrong from the [answer key](#answer-key). One point each, 85 points.
2. Score each PBQ **all-or-nothing** (1 point each, 5 points): a single mis-placed item is a miss, because that is how a drag-and-drop item feels on the day. If you want a finer signal, note partial credit separately, but use the all-or-nothing figure for the gate.
3. Total out of 90. **Gate: 77 or more (85%)** in one timed sitting.
4. Fill in the score sheet by domain (each key entry names its domain). Any domain below 80% goes back into the study rotation, per the hub's procedure, even if the total passes.
5. Read the explanation for every miss **and** for every item you guessed. Log the concept, not the letter, in your weak-area list.

### Score sheet

| Domain | MCQ items | PBQ items | Correct | % |
| --- | --- | --- | --- | --- |
| 1 · General Security Concepts (12%) | 10 | PBQ 4, PBQ 5 | ____ / 12 | ____% |
| 2 · Threats, Vulnerabilities & Mitigations (22%) | 19 | PBQ 2 | ____ / 20 | ____% |
| 3 · Security Architecture (18%) | 15 | PBQ 3 | ____ / 16 | ____% |
| 4 · Security Operations (28%) | 24 | PBQ 1 | ____ / 25 | ____% |
| 5 · Security Program Management & Oversight (20%) | 17 | (none) | ____ / 17 | ____% |
| **Total** | **85** | **5** | ____ / 90 | ____% |

The MCQ split (10 / 19 / 15 / 24 / 17) follows the published domain weights (12 / 22 / 18 / 28 / 20 percent) as closely as 85 whole questions allow.

---

## Part A: multiple-choice questions (85)

Pick the **single best** answer. Watch the qualifiers (BEST, MOST, FIRST).

**Q1.** A network administrator is hardening a core switch. Which change BEST reduces the management-plane attack surface?
- A. Enable SNMPv1 for monitoring
- B. Increase the MAC address table size
- C. Add a second uplink for redundancy
- D. Replace Telnet with SSH and disable unused ports

**Q2.** An organization is targeted over many months by a well-funded, highly sophisticated external group whose apparent goal is to quietly copy research data. Which threat actor is MOST likely responsible?
- A. Unskilled attacker
- B. Hacktivist
- C. Nation-state actor
- D. Shadow IT

**Q3.** A file server is valued at $50,000. A ransomware event would destroy 20% of its value, and such events are expected twice a year. What is the Annualized Loss Expectancy (ALE)?
- A. $5,000
- B. $10,000
- C. $20,000
- D. $100,000

**Q4.** A firewall protects a payment-processing segment where letting unchecked traffic through is considered worse than an outage. Which failure mode should the firewall be configured for?
- A. Fail-open
- B. Tap mode
- C. Passive
- D. Fail-closed

**Q5.** A legacy manufacturing application cannot support multi-factor authentication. The security team requires all administrative access to pass through a monitored jump host instead. Which control type BEST describes the jump host?
- A. Corrective
- B. Directive
- C. Compensating
- D. Deterrent

**Q6.** A vulnerability report lists a finding with a severity of 9.8. Which standard produced that number?
- A. CVE
- B. CWE
- C. CVSS
- D. SCAP

**Q7.** An employee receives a phone call from someone claiming to be the help desk who asks them to read out their password so a "ticket can be closed." Which technique is this?
- A. Vishing
- B. Smishing
- C. Whaling
- D. Pharming

**Q8.** A governance document states that all passwords must be at least 14 characters and rotated only after a suspected compromise. Which document type is this?
- A. Guideline
- B. Policy
- C. Standard
- D. Procedure

**Q9.** A company uses a SaaS collaboration suite. An employee shares a confidential folder with an external address by mistake. Under the shared responsibility model, who is responsible for that exposure?
- A. The cloud provider, because it operates the application
- B. Neither; SaaS exposures are covered by the provider's SLA
- C. Both equally, because SaaS splits responsibility down the middle
- D. The customer, because data and access configuration are always the customer's responsibility

**Q10.** An organization wants domain administrators to hold elevated rights only for the duration of an approved task, with no standing privilege. Which PAM capability BEST meets this need?
- A. Single sign-on
- B. Discretionary access control
- C. Just-in-time access
- D. Federation

**Q11.** Authentication logs show one common password being tried once against hundreds of different user accounts, with almost no lockouts. Which attack is this?
- A. Brute force
- B. Dictionary attack against one account
- C. Password spraying
- D. Rainbow-table attack

**Q12.** In a Zero Trust architecture, which component sits in the data plane and actually allows, blocks, and monitors the connection to a resource?
- A. Policy Engine
- B. Policy Administrator
- C. Policy Enforcement Point
- D. Adaptive identity service

**Q13.** A business impact analysis states that the order-entry system must be running again within four hours of a failure. Which metric does "four hours" define?
- A. RTO
- B. RPO
- C. MTBF
- D. ARO

**Q14.** A mail administrator wants receiving servers to be able to verify that a message was not altered in transit and genuinely originated from the company's mail system, using a cryptographic signature. Which mechanism provides this?
- A. SPF
- B. DLP
- C. DMARC
- D. DKIM

**Q15.** A company wants every device to authenticate before the switch grants it any network access, using a central RADIUS server. Which standard should be deployed on the switch ports?
- A. IEEE 802.1X
- B. IPsec
- C. SD-WAN
- D. SNMPv3

**Q16.** A web application reflects a search term back into the page without encoding it, and an attacker can make script run in other users' browsers. Which defense MOST directly fixes the flaw?
- A. Parameterized queries
- B. Output encoding and input validation
- C. Full-disk encryption
- D. Disabling the HttpOnly cookie flag

**Q17.** A workstation is confirmed to be infected and is actively scanning the internal network. According to the incident-response lifecycle, what should the responder do FIRST?
- A. Reimage the workstation
- B. Restore user files from backup
- C. Hold a lessons-learned meeting
- D. Isolate the workstation from the network

**Q18.** A systems administrator configures the backups, encryption, and access permissions that protect the HR database, but does not decide its classification. Which data role does the administrator hold?
- A. Data owner
- B. Data controller
- C. Data custodian
- D. Data subject

**Q19.** When a user digitally signs a document, which key is used to create the signature?
- A. The recipient's public key
- B. The certificate authority's private key
- C. The signer's private key
- D. A shared symmetric session key

**Q20.** A company stores customer records in a cloud region located in another country and is told that those records are now subject to that country's laws. Which concept is at work?
- A. Data sovereignty
- B. Geofencing
- C. Tokenization
- D. Data masking

**Q21.** An organization wants strong control over smartphones it issues to staff while still allowing limited personal use of the device. Which deployment model fits BEST?
- A. BYOD
- B. Air-gapped
- C. CYOD
- D. COPE

**Q22.** A user's account logs in from one continent and, twenty minutes later, from another. Which indicator of compromise does this describe?
- A. Resource consumption
- B. Impossible travel
- C. Out-of-cycle logging
- D. Blocked content

**Q23.** Two organizations want to record a shared, non-binding intention to cooperate on threat-intelligence sharing before any formal contract exists. Which agreement type is MOST appropriate?
- A. SLA
- B. MSA
- C. MOU
- D. SOW

**Q24.** A small security team wants a cheap, high-leverage control that stops malware on endpoints from reaching known command-and-control domains. Which capability BEST fits?
- A. DNS filtering
- B. File integrity monitoring
- C. NetFlow collection
- D. SAST

**Q25.** Which statement correctly describes a security implication of containerization compared with virtual machines?
- A. Containers each run their own kernel, so isolation is stronger
- B. Containers require a hypervisor, which becomes the main target
- C. Containers cannot be affected by image provenance issues
- D. Containers share the host OS kernel, so a kernel vulnerability can affect all of them

**Q26.** The finance team receives an email that appears to come from the CFO, instructing an urgent wire transfer to a new supplier account. Which attack is this MOST likely?
- A. Business email compromise
- B. Watering-hole attack
- C. Typosquatting
- D. Smishing

**Q27.** A security team plants a fake API key in a source-code repository and configures an alert if it is ever used. Which deception technique is this?
- A. Honeypot
- B. Honeynet
- C. Honeyfile
- D. Honeytoken

**Q28.** A development team wants to find security flaws by inspecting source code before the application is ever run. Which technique should they use?
- A. Dynamic analysis
- B. Sandboxing
- C. Fuzzing
- D. Static analysis

**Q29.** After a risk assessment, leadership decides to cancel a planned feature that would have stored biometric data, eliminating the risk entirely. Which risk strategy is this?
- A. Accept
- B. Mitigate
- C. Transfer
- D. Avoid

**Q30.** Malware spreads from server to server across the network with no user interaction and without attaching itself to another file. Which malware type is this?
- A. Virus
- B. Trojan
- C. Worm
- D. Logic bomb

**Q31.** A security team needs a monitoring device on a critical link that can never introduce latency or become a point of failure, even if the device itself crashes. Which placement should they choose?
- A. Inline, active
- B. Inline, passive
- C. Tap or monitor port, passive
- D. Inline, fail-open

**Q32.** In a classified environment, documents carry labels such as "Secret," and users cannot change who may read a file even if they created it. Which access-control model is in use?
- A. MAC
- B. DAC
- C. RBAC
- D. ABAC

**Q33.** An organization keeps patching on schedule, reviews access quarterly, and tests backups monthly, so that it can show it takes reasonable ongoing steps to protect its assets. Which concept does this BEST demonstrate?
- A. Due diligence
- B. Risk transfer
- C. Attestation
- D. Due care

**Q34.** A phishing email says "Your mailbox will be deleted in one hour unless you confirm your password now." Which social-engineering principle is being exploited?
- A. Consensus
- B. Familiarity
- C. Urgency
- D. Authority

**Q35.** During evidence acquisition on a running server suspected of compromise, which source should be captured FIRST?
- A. The backup tapes
- B. The system's RAM
- C. The hard disk image
- D. The printed network diagram

**Q36.** A relying party needs to check, in real time, whether one specific certificate has been revoked, without downloading a full list. Which mechanism should it use?
- A. CRL
- B. OCSP
- C. RA
- D. Key escrow

**Q37.** A company can tolerate a recovery time of several hours after a data-center loss and wants to keep costs moderate. Its chosen recovery site has hardware and connectivity in place but requires the latest data to be loaded before it can run. Which site type is this?
- A. Hot site
- B. Multicloud
- C. Cold site
- D. Warm site

**Q38.** Public kiosks keep getting unapproved software installed by visitors. Which mitigation MOST directly prevents any program that is not explicitly approved from running?
- A. Network segmentation
- B. Application allow listing
- C. Patch management
- D. Encryption at rest

**Q39.** A security tool baselines each user's normal working hours and data-access patterns, then flags a payroll clerk who suddenly downloads thousands of records at 3 a.m. Which capability is this?
- A. UEBA
- B. NAC
- C. WAF
- D. SPF

**Q40.** A risk workshop rates each risk as Low, Medium, or High on a colored heat map without assigning monetary values. Which type of risk analysis is this?
- A. Qualitative
- B. Quantitative
- C. Continuous
- D. Ad-hoc

**Q41.** A marketing department signs up for an online file-sharing service and stores customer lists there without informing IT. Which threat actor category does this represent?
- A. Insider threat with malicious intent
- B. Hacktivist
- C. Organized crime
- D. Shadow IT

**Q42.** A company is replacing its WPA2 wireless network. Which WPA3 feature specifically strengthens the handshake against offline password-guessing attacks?
- A. SAE
- B. PEAP
- C. NetFlow
- D. SCAP

**Q43.** An e-commerce site is being hit with injection and cross-site scripting attempts. Which device is purpose-built to inspect HTTP traffic and block these attacks?
- A. Layer 4 firewall
- B. Load balancer
- C. Web application firewall
- D. Jump server

**Q44.** A company wants a contractual guarantee that it may inspect a cloud vendor's security controls itself rather than relying on the vendor's questionnaire answers. Which clause should it require?
- A. Non-disclosure clause
- B. Conflict-of-interest clause
- C. Rules of engagement
- D. Right-to-audit clause

**Q45.** A flaw in a hypervisor lets code running inside a guest virtual machine execute on the host. Which vulnerability is this?
- A. VM escape
- B. Buffer overflow
- C. Directory traversal
- D. Resource reuse

**Q46.** A vulnerability scanner reports a critical flaw on a server, but the administrator believes the affected component is not installed. What should happen NEXT in the vulnerability-management process?
- A. Apply an emergency patch immediately
- B. Validate the finding to confirm whether it is a false positive
- C. Decommission the server
- D. File a risk exception

**Q47.** A change to a database cluster fails during its maintenance window and the service will not start. Which change-management element should the team now execute?
- A. Impact analysis
- B. Standard operating procedure for the next change
- C. Change Advisory Board approval
- D. Backout plan

**Q48.** Who is responsible for assigning the classification level of a set of financial records and defining its acceptable use?
- A. Data owner
- B. Data custodian
- C. Data processor
- D. Data steward

**Q49.** Attackers compromise an industry association's website that engineers from a target company visit daily, so that visitors are served malware. Which attack is this?
- A. Watering-hole attack
- B. Pharming
- C. Typosquatting
- D. Pretexting

**Q50.** Analysts want a record of which internal host communicated with which external address, when, and how much data moved, without capturing packet contents. Which data source provides this?
- A. NetFlow
- B. Packet capture
- C. Application logs
- D. Vulnerability scan

**Q51.** Which networking approach separates the control plane (decisions) from the data plane (forwarding) so that the network can be programmed centrally by software?
- A. Physical networking
- B. Port security
- C. Load balancing
- D. Software-defined networking

**Q52.** A man-in-the-middle forces a client and server to negotiate an older, weaker TLS version even though both support a stronger one. Which attack is this?
- A. Collision attack
- B. Birthday attack
- C. Downgrade attack
- D. Replay attack

**Q53.** An organization requires managers to confirm every quarter that each of their reports still needs the access they hold. Which IAM practice is this?
- A. Identity proofing
- B. Attestation (access review)
- C. Provisioning
- D. Interoperability

**Q54.** A storage array is advertised as running an average of 50,000 hours between failures. Which metric is being quoted?
- A. MTTR
- B. MTBF
- C. RTO
- D. RPO

**Q55.** A company wants a single device in front of its web servers to terminate TLS and distribute client requests to them. Which appliance does this?
- A. Forward proxy
- B. Sensor
- C. IDS
- D. Reverse proxy

**Q56.** The legal department anticipates litigation over a security incident. Which action must the organization take FIRST regarding relevant electronic records?
- A. Place the records under legal hold to preserve them
- B. Delete records older than the retention period
- C. Export the records to the opposing party
- D. Reimage the affected systems

**Q57.** Attackers gain access to a company's network by first compromising the managed service provider that administers its servers. Which threat vector is this?
- A. Removable media
- B. Supply chain
- C. Image-based
- D. Voice call

**Q58.** A user who normally signs in from the office is prompted for an additional authentication factor when signing in from a new country. Which Zero Trust concept is this?
- A. Implicit trust zone
- B. Threat scope reduction
- C. Adaptive identity
- D. Policy Administrator

**Q59.** An organization wants engineers to use a domain-admin credential to run a task without ever seeing the password itself. Which PAM capability provides this?
- A. Password vaulting with check-out
- B. Single sign-on
- C. Rule-based access control
- D. Identity proofing

**Q60.** A security team writes a pre-scripted set of response steps to follow specifically when ransomware is detected. Which document is this?
- A. Acceptable use policy
- B. Standard
- C. Guideline
- D. Playbook

**Q61.** Which statement BEST describes the security priorities of an ICS/SCADA environment that controls a water-treatment process?
- A. Confidentiality outranks everything; patch immediately
- B. Availability and safety often outrank confidentiality; isolate it from IT networks and patch cautiously
- C. It should share a flat network with office workstations for easier monitoring
- D. It should be moved to a public SaaS platform to gain provider patching

**Q62.** Antivirus runs clean, but a server keeps re-establishing an outbound connection after every reboot and hides certain processes from the process list. Which malware type is MOST likely present?
- A. Bloatware
- B. Rootkit
- C. Ransomware
- D. Keylogger

**Q63.** A company wants laptops to be checked for a current patch level and running EDR before they are allowed onto the corporate LAN. Which capability provides this?
- A. DLP
- B. DKIM
- C. XDR
- D. NAC

**Q64.** A security dashboard tracks the number of critical vulnerabilities older than 30 days and escalates when the count climbs past a set level. Which risk-management concept is that metric?
- A. Risk register
- B. Exposure factor
- C. Key risk indicator
- D. Risk appetite

**Q65.** An application checks that a user may access a file and then, a moment later, opens it, but an attacker swaps the file in between the check and the use. Which vulnerability class is this?
- A. Race condition (TOC/TOU)
- B. Memory injection
- C. Malicious update
- D. Jailbreaking

**Q66.** A mail administrator has SPF and DKIM in place and now wants to tell receiving servers to reject messages that fail those checks, and to receive reports about them. Which mechanism should be added?
- A. DMARC
- B. A secure email gateway
- C. FIM
- D. SNMPv3

**Q67.** Two branch offices need an encrypted site-to-site tunnel that authenticates and encrypts IP packets between their routers. Which technology is the standard choice?
- A. IPsec
- B. SASE
- C. TLS
- D. 802.1X

**Q68.** A data center posts prominent signs stating that CCTV is in operation and that the area is monitored. Which control type BEST describes the signage?
- A. Corrective
- B. Deterrent
- C. Compensating
- D. Detective

**Q69.** A web developer wants session cookies to be unreadable by client-side scripts so that a script injection cannot steal them. Which cookie attribute should be set?
- A. Secure
- B. Expires
- C. SameSite
- D. HttpOnly

**Q70.** A disgruntled developer leaves code in a payroll system that will delete records if their user account is ever removed from the directory. Which malware type is this?
- A. Trojan
- B. Worm
- C. Logic bomb
- D. Spyware

**Q71.** A company has an umbrella agreement with a consultancy. It now needs a document that lists the specific deliverables, tasks, and timeline for one particular project under that agreement. Which document is needed?
- A. MSA
- B. SOW
- C. BPA
- D. NDA

**Q72.** A security team wants to be alerted immediately if a critical system binary or configuration file on a server changes unexpectedly. Which capability provides this?
- A. File integrity monitoring
- B. DNS filtering
- C. Web filtering
- D. Log aggregation

**Q73.** An organization provisions its cloud environment from versioned templates. A reviewer notes that any mistake in a template is replicated to every environment built from it, and that secrets must never be hard-coded in it. Which architecture model is being described?
- A. Serverless
- B. On-premises
- C. Microservices
- D. Infrastructure as Code

**Q74.** Users typing the correct address of their bank are silently redirected to a fraudulent copy because DNS records were poisoned. Which attack is this?
- A. Typosquatting
- B. Pharming
- C. Vishing
- D. Brand impersonation

**Q75.** A SOC receives hundreds of similar alerts a day and wants the routine ones enriched with context and, when a defined condition is met, the affected host isolated automatically. Which technology BEST fits?
- A. SIEM only
- B. SOAR
- C. NetFlow
- D. SCAP

**Q76.** An organization feeds live telemetry into an automated system that re-evaluates its risk posture in near real time rather than at fixed intervals. Which assessment type is this?
- A. One-time
- B. Recurring
- C. Ad-hoc
- D. Continuous

**Q77.** A security manager compares the organization's current controls against the NIST Cybersecurity Framework to identify which controls are missing and to plan remediation. Which activity is this?
- A. Gap analysis
- B. Penetration test
- C. Change management
- D. Tabletop exercise

**Q78.** A small office wants one appliance that bundles firewall, IDS/IPS, antivirus, content filtering, and VPN. Which product category is this, and what is its main drawback?
- A. NGFW; it cannot inspect application content
- B. Layer 4 firewall; it has no port filtering
- C. WAF; it only protects web applications
- D. UTM; it can become a single point of failure

**Q79.** A photo-printing site asks for permission to read a user's cloud photos without the user handing over their cloud password. Which framework provides this delegated authorization?
- A. LDAP
- B. SAML
- C. OAuth 2.0
- D. RADIUS

**Q80.** During an investigation, analysts find that the security event log on a compromised server contains no entries at all for the two days around the intrusion. Which indicator of compromise is this?
- A. Concurrent session usage
- B. Missing logs
- C. Impossible travel
- D. Account lockout

**Q81.** After deploying MFA and segmentation, a company estimates that some chance of credential compromise still remains. What is that remaining risk called?
- A. Inherent risk
- B. Residual risk
- C. Risk appetite
- D. Risk threshold

**Q82.** A critical vulnerability cannot be patched because the vendor's fix breaks a business application. The business owner and security lead formally document and sign off on leaving it unpatched with monitoring in place. Which remediation option is this?
- A. Compensating control only
- B. Decommissioning
- C. Insurance
- D. Exception/exemption

**Q83.** A database service must keep running if one node fails, with the surviving node taking over the failed node's state. Which resilience technique provides this?
- A. Load balancing
- B. Clustering
- C. Platform diversity
- D. Generator backup

**Q84.** Two users choose the same password, yet their stored password hashes differ. Which technique explains this?
- A. Key escrow
- B. Salting
- C. Tokenization
- D. Steganography

**Q85.** A company hires testers and gives them full network diagrams, source code, and credentials so the test is as thorough and efficient as possible. Which pentest type is this?
- A. Unknown environment
- B. Partially known environment
- C. Known environment
- D. Physical

---

## Part B: performance-based scenarios (5)

Text versions of the drag-and-drop, ordering, and matching tasks the real exam uses. Write your answers down before checking.

### PBQ 1: Order the incident-response lifecycle

A managed detection service has just alerted you to a suspicious process on a finance workstation. Put the seven phases of the incident-response lifecycle, listed here out of order, into the correct sequence (1 to 7).

| Letter | Phase |
| --- | --- |
| A | Eradication |
| B | Lessons learned |
| C | Preparation |
| D | Containment |
| E | Detection |
| F | Recovery |
| G | Analysis |

Answer format: a sequence of seven letters.

### PBQ 2: Match the observation to the attack

Match each observation (1 to 6) to the single attack type from the list that BEST explains it. Each attack type is used at most once; two are distractors.

Observations:

1. Over a ten-minute window, 300 different user accounts each receive exactly one failed login using the password `Winter2026!`.
2. A single account receives 4,000 failed logins in a row, each with a different candidate password, until it locks out.
3. A web-server log shows a request whose search parameter contains `' OR 1=1 --`, followed by an unusually large database response.
4. A workstation makes a small outbound HTTPS connection to the same unknown external address every 60 seconds, day and night.
5. A public web server's request rate rises a thousandfold from many source addresses and the service becomes unreachable to customers.
6. A user reports that a "shared document" link in an email led to a page that looked like the corporate login portal but had a look-alike domain.

Attack types: **(a)** brute force · **(b)** password spraying · **(c)** SQL injection · **(d)** cross-site scripting · **(e)** command-and-control beaconing · **(f)** distributed denial of service · **(g)** phishing · **(h)** ARP poisoning

Answer format: 1 to 6, each with one letter.

### PBQ 3: Build the firewall rule set

A DMZ web server at `203.0.113.10` must:

- accept HTTPS (TCP 443) from any source;
- accept SSH (TCP 22) only from the management network `10.0.9.0/24`;
- accept nothing else.

The firewall evaluates rules **top-down, first match wins**, and has **no implicit deny**: the deployed rule set itself must enforce "accept nothing else." From the candidate rules below, select the rules needed and put them in a correct order. Unselected rules are not deployed.

| Rule | Action | Source | Destination | Protocol/Port |
| --- | --- | --- | --- | --- |
| R1 | Allow | any | 203.0.113.10 | TCP 22 |
| R2 | Allow | 10.0.9.0/24 | 203.0.113.10 | TCP 22 |
| R3 | Allow | any | 203.0.113.10 | TCP 443 |
| R4 | Deny | any | 203.0.113.10 | any |
| R5 | Allow | any | 203.0.113.10 | any |
| R6 | Allow | 10.0.9.0/24 | 203.0.113.10 | TCP 3389 |

Answer format: an ordered list of rule IDs (for example `R9, R8, R7`).

### PBQ 4: Classify the controls

For each control (1 to 8), give its **category** (Technical, Managerial, Operational, Physical) and its single BEST-fitting **type** (Preventive, Deterrent, Detective, Corrective, Compensating, Directive).

1. A bollard line in front of the data-center entrance.
2. A quarterly security-awareness training session delivered by the security team.
3. A SIEM correlation rule that alerts on ten failed logins in a minute.
4. An acceptable-use policy that all staff must sign.
5. Restoring a file server from last night's backup after a ransomware event.
6. A firewall rule that blocks inbound Telnet.
7. A sign reading "Area under video surveillance" at the loading dock.
8. A legacy SCADA controller that cannot be patched is placed on an isolated network segment behind strict firewall rules.

Answer format: eight rows of `category / type`.

### PBQ 5: Pick the cryptographic primitive

For each requirement (1 to 8), choose the single BEST-fitting item from the list. Each item is used at most once; two are distractors.

Requirements:

1. Let a user confirm that a downloaded installer was not altered, using a published fixed-length digest.
2. Encrypt a multi-terabyte backup quickly.
3. Prove to a third party that a specific person approved a contract and cannot later deny it.
4. Let a browser and a server agree on a session key over an untrusted network without a pre-shared secret.
5. Store user passwords so that identical passwords produce different stored values and offline cracking is slowed.
6. Replace stored card numbers with values that have no exploitable meaning, keeping the real values in a separate vault.
7. Check in real time whether a single presented certificate has been revoked.
8. Hide the very existence of a message inside an image file.

Items: **(a)** AES · **(b)** SHA-256 hash · **(c)** digital signature · **(d)** Diffie-Hellman / ECDHE key exchange · **(e)** salted hash with key stretching · **(f)** tokenization · **(g)** OCSP · **(h)** steganography · **(i)** CRL · **(j)** data masking

Answer format: 1 to 8, each with one letter.

---

## Answer key

Cover this section until you have finished the timed sitting. Each entry gives the answer, a short explanation, the domain number, and the domain page.

### Part A answers

| # | Ans. | Explanation | Dom. | Page |
| --- | --- | --- | --- | --- |
| Q1 | D | Hardening network devices means disabling unused ports/services and using secure protocols (SSH, not Telnet); SNMPv1 is the insecure version. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q2 | C | Highly sophisticated, well-resourced, patient, and after espionage/exfiltration describes a nation-state or APT actor. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q3 | C | SLE = AV × EF = 50,000 × 0.2 = $10,000; ALE = SLE × ARO = 10,000 × 2 = $20,000 per year. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q4 | D | Fail-closed blocks traffic on failure, prioritizing security over availability; fail-open would let unchecked traffic through. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q5 | C | A compensating control is the substitute used when the ideal control (MFA) is not feasible; the domain page uses exactly this jump-host example. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q6 | C | CVSS is the 0 to 10 severity score; CVE is the identifier of a specific flaw; CWE is the weakness category. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q7 | A | Vishing is phishing by voice call; smishing is by SMS and whaling targets executives. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q8 | C | Standards are the specific, measurable, mandatory rules (such as a password standard) that make a policy enforceable. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q9 | D | Under every service model the customer owns its data and identity/access configuration; a mis-shared folder is a customer-side misconfiguration. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q10 | C | Just-in-time access grants elevated rights only when needed and revokes them afterwards, eliminating standing privilege. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q11 | C | Password spraying tries one password against many accounts, staying under lockout thresholds; brute force hammers one account. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q12 | C | The Policy Enforcement Point is the data-plane gate that allows, blocks, and monitors; the Policy Engine and Policy Administrator are control plane. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q13 | A | RTO is the maximum time to restore a service; RPO is acceptable data loss; MTBF is reliability. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q14 | D | DKIM signs outgoing messages so receivers can verify integrity and origin; SPF lists authorized sending IPs; DMARC adds policy and reporting. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q15 | A | IEEE 802.1X is port-based network access control; it carries EAP and typically authenticates against RADIUS. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q16 | B | This is cross-site scripting; the named defenses are output encoding, input validation, and a Content Security Policy. Parameterized queries fix SQL injection. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q17 | D | Containment (isolating the host) comes before eradication and recovery; lessons learned is last. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q18 | C | The custodian implements and maintains the technical controls; the owner sets classification; the controller decides the purpose of processing. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q19 | C | A digital signature is the hash of the message encrypted with the signer's private key; anyone verifies it with the signer's public key. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q20 | A | Data sovereignty means data is subject to the laws of the country where it is physically stored. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q21 | D | COPE (corporate-owned, personally enabled) gives strong control with some personal use; BYOD is employee-owned; CYOD is a pick from an approved list. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q22 | B | Impossible travel is two logins from far-apart locations too close together in time, a classic indicator of compromise. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q23 | C | An MOU is a less formal, often non-binding statement of intent; an MSA is the umbrella contract, an SOW the specific job, an SLA a performance guarantee. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q24 | A | DNS filtering blocks resolution of known-bad domains and is described as a cheap, high-leverage control against command-and-control traffic. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q25 | D | Containers share the host OS kernel, so isolation is weaker than VMs and a kernel flaw can affect every container; image provenance also matters. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q26 | A | Business email compromise impersonates a trusted executive or partner to trigger fraudulent payments. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q27 | D | A honeytoken is fake data (a bogus credential or API key) seeded so that any use signals a leak; a honeyfile is a decoy file, a honeypot a decoy system. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q28 | D | Static code analysis (SAST) inspects source without running it; dynamic analysis (DAST) and fuzzing test the running application. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q29 | D | Avoidance eliminates the risk by not doing the activity; mitigation adds controls, transfer shifts it, acceptance tolerates it. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q30 | C | A worm self-replicates across networks without a host file or user action; a virus needs a host file; a trojan is disguised. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q31 | C | A tap/monitor device receives a copy of traffic out of band and cannot disrupt flow; inline devices can block but can also bottleneck or fail. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q32 | A | Mandatory access control uses system-enforced labels and clearances that users cannot change; DAC lets the owner decide. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q33 | D | Due care is the reasonable, ongoing effort to protect assets; due diligence is the investigation done before acting. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q34 | C | A deadline that pressures the victim to act without thinking exploits urgency (closely related to scarcity). | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q35 | B | Evidence is acquired in order of volatility: memory before disk before backups. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q36 | B | OCSP checks one certificate's revocation status in real time; a CRL is a downloaded signed list of revoked certificates. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q37 | D | A warm site has hardware and connectivity but needs data loaded; recovery takes hours at medium cost. Hot is near-instant and costly; cold is days and cheapest. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q38 | B | Application allow listing permits only approved software to run (deny by default). | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q39 | A | User and Entity Behavior Analytics baselines normal behavior and flags anomalies such as unusual data access. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q40 | A | Qualitative analysis uses subjective ratings and heat maps; quantitative uses money and probability (SLE/ALE/ARO). | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q41 | D | Shadow IT is internal staff deploying unsanctioned technology for convenience; it is not malicious but creates risk. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q42 | A | WPA3 introduces SAE (Simultaneous Authentication of Equals) to protect the handshake against offline password guessing. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q43 | C | A web application firewall is a Layer 7 firewall specialized to block web attacks such as injection and cross-site scripting. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q44 | D | A right-to-audit clause is the contractual right to inspect the vendor's controls yourself. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q45 | A | VM escape is breaking out of a guest to the host, the high-impact virtualization vulnerability. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q46 | B | Analysis and validation confirm a finding is real (and weed out false positives) before remediation. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q47 | D | The backout (rollback) plan is the defined way to revert a failed change. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q48 | A | The data owner is the senior accountable role that assigns classification and acceptable use. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q49 | A | A watering-hole attack compromises a site the target group is known to visit. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q50 | A | NetFlow records metadata about flows (who talked to whom, how much) without packet contents. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q51 | D | Software-defined networking separates the control plane from the data plane for central, programmable control; its controller becomes a high-value target. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q52 | C | A downgrade attack forces a weaker protocol or cipher; collision and birthday attacks target hashes. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q53 | B | Attestation is the periodic access review (recertification) confirming each person still needs their access. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q54 | B | MTBF is the average time between failures (reliability); MTTR is the average repair time. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q55 | D | A reverse proxy fronts servers and enables load balancing and TLS termination; a forward proxy mediates outbound user traffic. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q56 | A | A legal hold is the formal duty to preserve potentially relevant data once litigation is anticipated. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q57 | B | Compromise via a vendor or managed service provider is the supply-chain vector. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q58 | C | Adaptive identity adjusts authentication strength to risk and context, such as step-up MFA from a new country. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q59 | A | Password vaulting lets users check out a privileged credential without ever seeing the secret. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q60 | D | A playbook is a procedure: pre-written response steps for a specific incident type such as ransomware. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q61 | B | For ICS/SCADA, availability and safety often outrank confidentiality; legacy protocols and rare patching mean isolation from IT networks is the key control. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q62 | B | A rootkit hides deep in the OS to evade detection and maintain persistence. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q63 | D | Network Access Control enforces posture and identity checks before a device joins the network. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q64 | C | A key risk indicator is a metric that signals rising risk; the domain page uses the unpatched-critical-systems count as its example. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q65 | A | A time-of-check to time-of-use race condition is an application vulnerability where state changes between the check and the use. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q66 | A | DMARC builds on SPF and DKIM, tells receivers what to do on failure, and adds reporting. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q67 | A | IPsec authenticates and encrypts IP packets and is the common basis for site-to-site VPNs. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q68 | B | Visible "CCTV in use" signage discourages an attacker: a deterrent control (the camera itself is detective). | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q69 | D | HttpOnly prevents script access to the cookie; Secure restricts it to HTTPS. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q70 | C | A logic bomb is dormant code that triggers on a condition or event. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q71 | B | A statement of work (or work order) lists the specific deliverables and timeline under a master service agreement. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q72 | A | File integrity monitoring alerts when critical files change unexpectedly. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q73 | D | Infrastructure as Code builds from declarative templates; a template flaw is replicated everywhere and secrets must not be hard-coded. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q74 | B | Pharming redirects users from a legitimate site to a fake one, for example via DNS poisoning; typosquatting relies on misspelled domains. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q75 | B | SOAR runs playbooks that enrich alerts and automate containment such as isolating a host. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q76 | D | A continuous assessment is ongoing, automated, near-real-time monitoring of risk. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q77 | A | A gap analysis compares the current posture with a target framework, identifies missing controls, and produces a remediation plan. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q78 | D | Unified Threat Management bundles many functions into one appliance; the stated drawback is a single point of failure. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q79 | C | OAuth 2.0 grants delegated authorization; OIDC adds an identity layer on top; SAML is XML-based web SSO. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q80 | B | Missing logs are a listed indicator of compromise: an attacker covering tracks. | 2 | [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md) |
| Q81 | B | Residual risk is what remains after treatment. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |
| Q82 | D | An exception/exemption is a risk-accepted remediation option with formal sign-off. | 4 | [Domain 4](../domains/04-security-operations.md) |
| Q83 | B | Clustering groups nodes that share state and fail over for a failed peer; load balancing distributes active traffic. | 3 | [Domain 3](../domains/03-security-architecture.md) |
| Q84 | B | Salting adds random data to each input before hashing, so identical passwords give different hashes and rainbow tables fail. | 1 | [Domain 1](../domains/01-general-security-concepts.md) |
| Q85 | C | A known-environment (white-box) test gives the tester full information for an efficient, thorough test. | 5 | [Domain 5](../domains/05-security-program-management-oversight.md) |

### Part B answers

**PBQ 1 (Domain 4, [Domain 4](../domains/04-security-operations.md)):** **C, E, G, D, A, F, B**, that is Preparation → Detection → Analysis → Containment → Eradication → Recovery → Lessons learned. This is the lifecycle as drawn on the domain page; the practical trap is placing containment before analysis or lessons learned anywhere but last.

**PBQ 2 (Domain 2, [Domain 2](../domains/02-threats-vulnerabilities-mitigations.md)):**

| Obs. | Answer | Why |
| --- | --- | --- |
| 1 | (b) password spraying | One password, many accounts, staying under lockout thresholds. |
| 2 | (a) brute force | Many candidate passwords against a single account until lockout. |
| 3 | (c) SQL injection | Crafted SQL in an input parameter followed by an oversized data response. |
| 4 | (e) command-and-control beaconing | Regular, small outbound connections to one unknown address are the beaconing indicator. |
| 5 | (f) distributed denial of service | Resource consumption and inaccessibility from many sources. |
| 6 | (g) phishing | A lure email leading to a credential-harvesting page on a look-alike domain. |

Distractors (d) cross-site scripting and (h) ARP poisoning are not used.

**PBQ 3 (Domain 3, [Domain 3](../domains/03-security-architecture.md)):** **R3, R2, R4** (R2 and R3 may be swapped; R4 must be last). R3 allows HTTPS from anywhere; R2 allows SSH only from `10.0.9.0/24`; R4 is the explicit deny-all that enforces "nothing else." R1 is wrong because it opens SSH to any source; R5 allows everything; R6 opens RDP, which was never required. Because first match wins, placing R4 above the allows would block all traffic.

**PBQ 4 (Domain 1, [Domain 1](../domains/01-general-security-concepts.md)):**

| # | Control | Category / type |
| --- | --- | --- |
| 1 | Bollards | Physical / Preventive |
| 2 | Awareness training session | Operational / Preventive |
| 3 | SIEM failed-login rule | Technical / Detective |
| 4 | Acceptable-use policy | Managerial / Directive |
| 5 | Restore from backup | Technical / Corrective |
| 6 | Firewall rule blocking Telnet | Technical / Preventive |
| 7 | "Under video surveillance" sign | Physical / Deterrent |
| 8 | Isolating the unpatchable SCADA controller | Technical / Compensating |

Notes: the domain page lists security-awareness training as operational (carried out by people) and policies as managerial; a sign is both deterrent and directive, and with a surveillance wording the BEST single fit is deterrent. Row 8 is the compensating pattern the Domain 1 page flags ("legacy system can't support X"): the ideal control (patching) is not feasible, so isolation and segmentation stand in for it, which is exactly what the Domain 4 hardening table prescribes for ICS/SCADA. Segmentation is preventive in nature, but a control deployed specifically because the primary control is impossible is BEST typed as compensating.

**PBQ 5 (Domain 1, [Domain 1](../domains/01-general-security-concepts.md)):**

| Req. | Answer | Why |
| --- | --- | --- |
| 1 | (b) SHA-256 hash | A one-way fixed-length digest verifies integrity. |
| 2 | (a) AES | Symmetric encryption is fast and suited to bulk data. |
| 3 | (c) digital signature | Private-key signing gives integrity, authenticity, and non-repudiation. |
| 4 | (d) Diffie-Hellman / ECDHE | Asymmetric key exchange agrees a session key without a pre-shared secret. |
| 5 | (e) salted hash with key stretching | Salting defeats rainbow tables; stretching (bcrypt, PBKDF2, scrypt, Argon2) slows brute force. |
| 6 | (f) tokenization | A meaningless token replaces the value; the mapping lives in a secure vault. |
| 7 | (g) OCSP | Real-time revocation check of a single certificate; a CRL is a downloaded list. |
| 8 | (h) steganography | Hides the existence of data inside another medium. |

Distractors (i) CRL and (j) data masking are not used.

---

## Where to go next

- [practice-questions.md](practice-questions.md) — the per-domain question bank to drill any domain that scored below 80% here.
- [cheat-sheet.md](cheat-sheet.md) — the facts behind the misses, in one page.
- [study-plan.md](study-plan.md) — where this mock sits in the seven-week schedule.
- [../domains/README.md](../domains/README.md) — the five domain pages every answer above links to.
- [../README.md](../README.md) — the hub's preparation procedure and readiness gate.

## Sources

- CompTIA — Security+ (SY0-701) official certification page (max 90 questions, MCQ + PBQ, 90 minutes, 750 on a 100–900 scale, five domains and weightings): https://www.comptia.org/en-us/certifications/security/
- Sibling hub pages the items are grounded in: [../00-overview/exam-and-objectives.md](../00-overview/exam-and-objectives.md) · [../domains/01-general-security-concepts.md](../domains/01-general-security-concepts.md) · [../domains/02-threats-vulnerabilities-mitigations.md](../domains/02-threats-vulnerabilities-mitigations.md) · [../domains/03-security-architecture.md](../domains/03-security-architecture.md) · [../domains/04-security-operations.md](../domains/04-security-operations.md) · [../domains/05-security-program-management-oversight.md](../domains/05-security-program-management-oversight.md)
- The 85% pass line is this repo's readiness rule from [../../../learning/how-to-prepare-a-cert.md](../../../learning/how-to-prepare-a-cert.md), not a CompTIA figure.
- Verified ground truth for this hub: SY0-701; max 90 questions (MCQ + PBQ); 90 minutes; passing 750 on a 100–900 scale; domain weights 12 / 22 / 18 / 28 / 20 percent.
- Every item here is an original study aid written for this hub and is **not** a CompTIA exam item.
