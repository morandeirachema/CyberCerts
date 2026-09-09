# CySA+ (CS0-003) Full-Length Mock Exam (Unofficial)

A **full-length, timed mock exam** for the CompTIA Cybersecurity Analyst (CySA+) **CS0-003**:
**80 multiple-choice questions** in mixed domain order plus **5 performance-based (PBQ)
style scenarios**, all with an answer key that links back to the domain page each item tests.
It is the "timed full mixed set" that step 5 of the hub's
[preparation procedure](../README.md#-prepare-for-it--the-procedure) asks for.

> **Unofficial mock — NOT real CompTIA exam questions.** Every item here is an original study
> aid written for this hub from the concepts on the four [domain pages](../domains/README.md).
> Nothing is drawn from, affiliated with, or endorsed by CompTIA, and nothing reproduces an
> actual exam item. All log excerpts, hostnames, addresses (RFC 5737 documentation ranges such
> as `203.0.113.0/24`) and scan outputs are invented for the exercise.

## Rules

Mirror the real format as the hub records it: CompTIA's CySA+ is **a maximum of 85 questions**
(multiple-choice plus performance-based) in **165 minutes**, passed at **750 on a 100–900
scaled score** — *verify on CompTIA*, see [exam & objectives](../00-overview/exam-and-objectives.md).
This mock has **85 items (80 MCQ + 5 PBQ)**, so sit it in **one uninterrupted, timed 165-minute
block**: no notes, no domain pages open, answer every item (there is no penalty for guessing),
and flag PBQs you find slow to come back to at the end. Do the PBQs first if you want to
rehearse the real ordering — CompTIA typically places them at the start.

> **Pass line for this repo.** CompTIA does not publish a raw percentage, and the 750 scaled
> score cannot be converted to one. The readiness gate in this repo's
> [how to prepare a certification](../../../learning/how-to-prepare-a-cert.md) method — not a
> CompTIA figure — is **85% on a full, timed mock**, with no domain below 80% on the
> [track-it table](../README.md#-track-it). Use that as your pass line here.

## How to score

- **Part A:** 1 point per question — **80 points**.
- **Part B:** each PBQ is worth **4 points**, scored per the rubric in its answer — **20 points**.
- **Total: 100 points**; pass = **85 or more**, with every domain at or above **80%** of its
  points. Anything lower: log the misses in your weak-area log, re-read the linked domain
  section, and re-sit after at least a week (spaced attempt).
- The **domain of each item** is in the answer key, so you can fill the sheet below.

### Score sheet

| Domain | Weight | MCQ items | PBQ points | Points available | Points scored | % |
|---|---|---|---|---|---|---|
| 1 — [Security Operations](../domains/01-security-operations.md) | 33% | 26 | 8 (PBQ 1, PBQ 4) | 34 | ____ | ____% |
| 2 — [Vulnerability Management](../domains/02-vulnerability-management.md) | 30% | 24 | 4 (PBQ 2) | 28 | ____ | ____% |
| 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md) | 20% | 16 | 4 (PBQ 3) | 20 | ____ | ____% |
| 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md) | 17% | 14 | 4 (PBQ 5) | 18 | ____ | ____% |
| **Total** | 100% | **80** | **20** | **100** | ____ | ____% |

The MCQ split (26 / 24 / 16 / 14) follows the published weights (33 / 30 / 20 / 17 percent)
as closely as 80 questions allow.

---

## Part A — Multiple choice (80 questions)

Choose the single BEST answer. Questions are in mixed domain order.

**Q1.** Two sources, `app01` and `dc01`, feed the SIEM. A correlation rule — *interactive logon on a
domain controller followed within 5 minutes by a new member added to Domain Admins* — never
fires, although both events are present in the raw logs and a manual review shows they
happened 40 seconds apart. The analyst notices that `dc01` timestamps run about seven minutes
behind `app01`. What is the MOST likely root cause?

- A. The two sources are not time-synchronized (NTP), so the events cannot be correlated
- B. The SIEM lacks a parser for domain-controller events
- C. The logging level on `dc01` is set too high and floods the rule
- D. The rule's 5-minute window is too short for this attack

**Q2.** Two scans of `web01` on the same day disagree:

```text
[uncredentialed] web01  Medium  OpenSSH 8.2 banner - 3 CVEs (version-based, POTENTIAL)
[credentialed]   web01  --      openssh-server 8.2 with vendor-backported fixes - no missing patches
```

How should the analyst reconcile them?

- A. Average the two severities
- B. Rescan uncredentialed until the finding disappears
- C. Treat the uncredentialed finding as a probable false positive inferred from the banner, trust the credentialed result, and document why
- D. Report the 3 CVEs; the uncredentialed view is what an attacker sees

**Q3.** Incident timeline:

```text
08:03  EDR alert: ransom note dropped on FS-01
08:05  Analyst confirms encryption in progress on two file shares
08:07  Analyst disconnects FS-01 from the network and disables the service account writing the files
08:30  Forensic image of FS-01 memory started
```

Which NIST SP 800-61 activity does the 08:07 entry represent?

- A. Short-term containment
- B. Preparation
- C. Recovery
- D. Eradication

**Q4.** A patch for a critical finding requires a reboot, but the hosting contract guarantees 99.95%
monthly availability and the customer refuses an unscheduled window. Which inhibitor to
remediation is this?

- A. MOU
- B. Proprietary system
- C. Legacy system
- D. SLA

**Q5.** An EDR record from workstation `WS-0417` reads:

```text
2026-03-04T10:12:07Z host=WS-0417 user=j.perez
  parent=WINWORD.EXE (pid 4120)
  child=powershell.exe (pid 4388)
  cmdline="powershell.exe -nop -w hidden -enc SQBFAFgAIAAo..."
```

Which indicator family is this, and what does it MOST likely mean?

- A. Application-related — unexpected output from the word processor
- B. Network-related — beaconing to a command-and-control server
- C. Host-related — a suspicious parent/child process chain suggesting code execution from a document
- D. Host-related — abnormal resource consumption by the word processor

**Q6.** A water-treatment plant asks for vulnerability visibility on its PLC and SCADA network. The
last active scan caused a PLC to reboot. What is the BEST approach?

- A. Repeat the active scan with more concurrent checks to finish faster
- B. Exclude the OT network from the program entirely
- C. Scan from the internet to avoid touching the internal segment
- D. Prefer passive monitoring and read-only checks; run any active scan throttled, in a maintenance window, with system owners present

**Q7.** While a forensic image is taken and a rebuild is prepared, the team applies a temporary
firewall rule blocking the affected subnet from the domain controllers and leaves the affected
server running so the business can operate. This is:

- A. Eradication
- B. Recovery
- C. Long-term containment
- D. Post-incident activity

**Q8.** A firewall log shows the following for `web01` (203.0.113.10), a public web server that should
only accept inbound HTTPS and talk to the internal database:

```text
2026-03-04 02:14:31 ALLOW TCP src=203.0.113.10:51544 dst=198.51.100.77:4444 host=web01
2026-03-04 02:14:31 ALLOW TCP src=203.0.113.10:51545 dst=198.51.100.77:4444 host=web01
2026-03-04 02:14:32 ALLOW TCP src=203.0.113.10:51546 dst=198.51.100.77:4444 host=web01
```

Which indicator is present and what does it MOST likely suggest?

- A. Host-related — unauthorized software installed on the database
- B. Application-related — an unusual outbound connection from an application server reaching attacker infrastructure
- C. Network-related — a bandwidth spike consistent with a DDoS against the server
- D. Application-related — new accounts created in the web application

**Q9.** Sales laptops are rarely connected to the VPN and are often powered off during the nightly
scan window, so they never appear in the results. Which deployment choice fixes this?

- A. Agent-based scanning
- B. Agentless network scanning from the data centre
- C. Passive scanning
- D. External scanning

**Q10.** A shared research system is operated by a partner university under an agreement stating that
only the partner's staff may apply changes. Which inhibitor applies?

- A. MOU (memorandum of understanding)
- B. Degrading functionality
- C. Business-process interruption
- D. Legacy system

**Q11.** The CISO asks the threat-intelligence team for a briefing to the board on how ransomware
activity against the organisation's sector is expected to evolve over the next year. Which
level of cyber threat intelligence is being requested?

- A. Technical IoC feed
- B. Tactical
- C. Strategic
- D. Operational

**Q12.** The board asks, "What can an attacker on the internet actually see of us?" Which scan gives
the most direct answer?

- A. External uncredentialed scan of the edge
- B. Agent-based scan of every workstation
- C. Container image scan
- D. Internal credentialed scan

**Q13.** The team rebuilds the compromised server from a known-good image, closes the exploited
vulnerability and disables the accounts the attacker created. Which phase is this?

- A. Detection and analysis
- B. Eradication
- C. Containment
- D. Recovery

**Q14.** Proxy logs show several workstations connecting to `cdn-update-check.example`, a domain nobody
in IT recognises. The analyst wants to know how old the domain is, who registered it, and
whether it has a poor reputation before doing anything else. Which technique category fits?

- A. Packet capture
- B. DNS / whois and reputation lookups
- C. Endpoint memory analysis
- D. Sandboxing

**Q15.** A manufacturing controller runs an operating system that left vendor support years ago; no
patch exists for the reported CVE. What is the inhibitor, and what should the analyst
recommend?

- A. SLA; patch anyway
- B. Governance; skip change control
- C. MOU; renegotiate the contract
- D. Legacy system; compensating controls (segmentation, monitoring) or documented risk acceptance

**Q16.** A finding carries `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:N`. Which statement is correct?

- A. No privileges are required to exploit it
- B. User interaction is required
- C. Availability impact is High
- D. Scope is changed — a successful exploit affects resources beyond the vulnerable component

**Q17.** A user reports a suspicious PDF attachment. The analyst wants to observe what the file actually
does when opened without risking a production host. Which technique is MOST appropriate?

- A. Search the file name on a search engine
- B. Detonate the file in an isolated sandbox and record its behavior
- C. Open the file on the analyst's workstation with antivirus enabled
- D. Run `strings` on the file and stop there

**Q18.** A rebuilt server is ready to go back into production. What does the Recovery activity still
require before the incident can move to post-incident work?

- A. Validate the system is clean, return it in a controlled way and monitor closely for recurrence
- B. Delete all logs to start fresh
- C. Nothing — rebuilding is sufficient
- D. Hold the lessons-learned meeting first

**Q19.** Public exploit code is released for a CVE that was already in the backlog. Which CVSS metric
group changes as a result?

- A. Base
- B. Environmental
- C. None — CVSS scores never change after publication
- D. Temporal / Threat

**Q20.** Two detection rules exist. Rule R1 matches the SHA-256 hash of a known dropper. Rule R2
matches *a non-browser process writing an executable to a user temp folder and immediately
spawning it*. The attacker recompiles the dropper, changing its hash. Which rule still fires,
and why?

- A. Both — the SIEM automatically updates hashes
- B. R1 — hash-based indicators of compromise are the most durable
- C. R2 — it describes an indicator of attack (behavior), which survives artifact changes
- D. Neither — both depend on the original binary

**Q21.** A vendor-locked network appliance cannot be modified by the customer, and the vendor promises
a fix "next quarter". Which inhibitor is this?

- A. SLA
- B. Proprietary system
- C. Legacy system
- D. Scan coverage

**Q22.** Finding X: CVSS base 9.8 on a lab VM with no network route to production or the internet.
Finding Y: CVSS base 6.5 on the public payment web server. With no other data, which should
be fixed first, and why?

- A. X — the higher base score always wins
- B. X — lab systems are usually less patched
- C. Neither — both are below the Critical band
- D. Y — environmental context (exposure and asset value) outranks raw base severity

**Q23.** An analyst arrives at a running, suspected-compromised server. Following the order of
volatility, which evidence should be captured FIRST?

- A. A full disk image
- B. Last month's backup tapes
- C. Archived syslog on the SAN
- D. The contents of RAM and current network connections

**Q24.** A CTI report says an actor targeting the organisation's sector performs Kerberoasting
(MITRE ATT&CK T1558.003). No alert has fired. What is the correct FIRST step of a threat hunt?

- A. Block all outbound traffic from the domain controllers
- B. Form a hypothesis such as "if this actor Kerberoasted us, the domain-controller logs would show unusual bursts of service-ticket requests from one account" and query for it
- C. Run an uncredentialed vulnerability scan of the domain controllers
- D. Wait for the SIEM to raise a Kerberos alert

**Q25.** A scanner reports two findings with CVSS v3.x base scores of **6.9** and **7.0**. Which
severity labels apply?

- A. 6.9 Low, 7.0 Medium
- B. Both High
- C. Both Medium
- D. 6.9 Medium, 7.0 High

**Q26.** The only available fix for a finding removes a feature the finance team's month-end workflow
depends on. Which inhibitor is this?

- A. Order of volatility
- B. Scan coverage
- C. MOU
- D. Degrading functionality

**Q27.** After three days a hunt for a suspected lateral-movement technique finds no evidence. What
should STILL happen before the hunt is closed?

- A. Nothing — a negative hunt is wasted effort and should not be documented
- B. Reduce the logging level on the hosts that were hunted to save storage
- C. Document the queries, refine or close the hypothesis, and turn the coverage gained into a new automated detection
- D. Escalate to incident response anyway to be safe

**Q28.** The analyst hashes a disk image immediately after acquisition and again after it is copied to
the evidence server; the hashes match. What does this establish?

- A. That the disk can be wiped
- B. The evidence's integrity — it has not changed — supporting chain of custody
- C. The attacker's identity
- D. The image contains no malware

**Q29.** Two CVEs both score CVSS base 8.1 and neither is in the CISA KEV catalog. EPSS gives one a
score of 0.91 and the other 0.03. How should the analyst use this?

- A. Prioritize the 0.03 CVE — lower EPSS means harder to detect
- B. Ignore EPSS; base score is the only official measure
- C. Prioritize the 0.91 CVE — EPSS estimates the probability of exploitation in the next 30 days
- D. Wait until one enters KEV

**Q30.** To work a single alert, analysts switch between six consoles: SIEM, EDR, ticketing,
threat-intel portal, firewall manager and cloud console. Which efficiency goal directly
addresses this?

- A. An information sharing and analysis center (ISAC) membership
- B. Passive vulnerability scanning
- C. A higher logging level on every source
- D. A single pane of glass built on tool integration via APIs

**Q31.** The CISO wants one chart for the monthly leadership deck that shows whether the vulnerability
program is improving. Which metric fits BEST?

- A. The CVSS vector of last month's worst finding
- B. The full list of open CVE identifiers
- C. The raw scanner XML export
- D. The number of open critical/high findings over time

**Q32.** What does inclusion of a CVE in the CISA Known Exploited Vulnerabilities (KEV) catalog
establish?

- A. A patch is not yet available
- B. The vulnerability only affects government systems
- C. The CVE has a CVSS score of at least 9.0
- D. Exploitation has been confirmed in the wild, and U.S. federal agencies have a remediation due date

**Q33.** The SOC is introducing SOAR. Which task is the BEST candidate to automate fully?

- A. Determining the full scope of a confirmed intrusion
- B. Enriching every alert's source IP with geo-IP, whois and reputation data and attaching the result to the ticket
- C. Writing the lessons-learned report
- D. Deciding whether to isolate the CFO's laptop during a suspected compromise

**Q34.** Which three factors does the page say drive an incident's severity and therefore its
prioritization and escalation?

- A. CVSS base, EPSS and KEV status
- B. Attack vector, attack complexity and privileges required
- C. Number of alerts, number of analysts and time of day
- D. Functional impact, information impact and recoverability

**Q35.** A zero-day in the organisation's internet-facing VPN appliance is being exploited in the wild
and the vendor has no patch. What is the BEST immediate response?

- A. Accept the risk permanently
- B. Wait for the patch; nothing can be done without it
- C. Run an aggressive active scan of the appliance
- D. Apply compensating controls now — restrict access, add IPS/WAF virtual patching, increase monitoring — and track the patch

**Q36.** The organisation now enforces TLS for all internal traffic. Network sensors that previously
detected web-shell uploads by content now see only metadata. What should the SOC plan for?

- A. Disable TLS on internal segments so the sensors work again
- B. Replace the sensors with a vulnerability scanner
- C. Move all detection to threat-intel feeds
- D. Decryption/inspection points at network chokepoints, and metadata-based analytics where decryption is not possible

**Q37.** An audit finds that 40% of the estate has never been scanned. Which program metric exposes
this?

- A. MTTR
- B. Dwell time
- C. Scan coverage
- D. Reopen rate

**Q38.** Mapping the Cyber Kill Chain to MITRE ATT&CK, the *Actions on Objectives* stage corresponds
MOST closely to which ATT&CK tactics?

- A. Initial Access
- B. Collection, Exfiltration and Impact
- C. Persistence and Defense Evasion
- D. Reconnaissance and Resource Development

**Q39.** An annual security-awareness program is introduced to reduce phishing-driven credential loss.
Which control category is this?

- A. Managerial
- B. Physical
- C. Operational
- D. Technical

**Q40.** After a single workstation was compromised, the attacker reached the backup servers directly
over SMB with nothing in the path to observe or stop it. Which architectural control BOTH
limits blast radius AND creates chokepoints where traffic can be monitored?

- A. Network segmentation
- B. Single sign-on (SSO)
- C. Time synchronization
- D. Data loss prevention (DLP)

**Q41.** The organisation adopts a Zero Trust architecture. From the analyst's point of view, what is
the MOST significant change?

- A. Logs no longer need to be time-synchronized
- B. Less telemetry, because the network location no longer matters
- C. Vulnerability scanning becomes unnecessary
- D. More identity-anchored telemetry and clearly defined policy-enforcement points to monitor

**Q42.** The operations team runs a monthly patch cycle: test, schedule, deploy, verify by re-scan.
Which control category does the *cycle itself* belong to?

- A. Technical
- B. Operational
- C. Physical
- D. Managerial

**Q43.** During post-incident work the team has the malware's hashes, its C2 domains and a registry key
it used. What should be done with them?

- A. Archive them with the ticket and take no further action
- B. Publish them in the customer notification
- C. Use them to attribute the attack to a nation-state
- D. Generate IoCs, push them into detection tooling and share them with peers or an ISAC

**Q44.** Findings closed last quarter keep reappearing on the same hosts a few weeks after remediation.
Which metric captures this, and what does it usually indicate?

- A. MTTD; slow detection
- B. SLA compliance; contracts are too strict
- C. Scan coverage; too few hosts scanned
- D. Vulnerability recurrence/reopen rate; fixes are not sticking (for example configuration drift)

**Q45.** A control raises this alert: an employee emailed a spreadsheet to a personal webmail address
containing roughly 3,800 sixteen-digit values matching a payment-card pattern. Which control
category produced the alert and what data class is at stake?

- A. Data loss prevention (DLP); cardholder data
- B. Endpoint detection and response (EDR); protected health information (PHI)
- C. A web application firewall; source code
- D. SOAR; personally identifiable information (PII)

**Q46.** Badge readers and cameras are installed on the cabinet housing the plant's OT controllers.
Which control category is this?

- A. Technical
- B. Managerial
- C. Physical
- D. Operational

**Q47.** Which description of a lessons-learned meeting matches NIST SP 800-61 practice?

- A. Attended only by executives
- B. Held six months later, focused on assigning blame
- C. Held promptly and blameless, asking what happened, how well the response worked and what to change
- D. Replaced by the compliance report

**Q48.** `db02` has run at 98% CPU for five days. An unfamiliar process launched from `/tmp` maintains
outbound connections on TCP 3333 to 203.0.113.61. The database itself is idle. What is the
MOST likely explanation?

- A. Cryptomining implant
- B. A scheduled backup
- C. Legitimate database index rebuild
- D. A DDoS against the database

**Q49.** Two different CVEs in two different products both map to CWE-89. What does that tell the
analyst?

- A. The two CVEs are duplicates and one should be removed
- B. Both have the same CVSS score
- C. Both are in the CISA KEV catalog
- D. Both are instances of the same weakness class (SQL injection), so the root cause should be addressed through secure coding in the SDLC

**Q50.** What is the significance of formally *declaring* an incident?

- A. It authorises the customer notification wording
- B. It replaces escalation
- C. It ends the response
- D. It starts the response clock and the notification obligations, based on criteria defined in advance

**Q51.** A protocol-aware proxy logs an SSH handshake on TCP/443 from a workstation to an external
host. What does this indicator suggest and to which family does it belong?

- A. Application-related — an injection attempt against the proxy
- B. Host-related — unauthorized software on the proxy
- C. Network-related — a benign bandwidth spike
- D. Network-related — a protocol on a non-standard port, suggesting evasion or tunneling

**Q52.** An adversary who has already exploited a host installs a backdoor service so access survives a
reboot. Which Cyber Kill Chain stage is this?

- A. Exploitation
- B. Actions on Objectives
- C. Installation
- D. Delivery

**Q53.** The CSIRT runs a phishing tabletop exercise, updates the call tree and provisions out-of-band
communications. Which phase are these activities?

- A. Preparation
- B. Detection and analysis
- C. Containment, eradication and recovery
- D. Post-incident activity

**Q54.** Windows security logs show:

```text
Task Scheduler: task "\Microsoft\Windows\UpdateCheck2" created
  action=C:\Users\Public\svc.exe  trigger=at logon  author=CORP\m.alvarez  time=23:57:41
```

`m.alvarez` is a sales user with no admin duties. Which conclusion is BEST supported?

- A. A benign OS update task
- B. A network-related indicator of beaconing
- C. A likely persistence mechanism (host-related indicator: unusual scheduled task)
- D. A DLP policy violation

**Q55.** The communications lead drafts a public statement about a breach. Who should review it BEFORE
release?

- A. Legal and public relations
- B. The ISAC
- C. The scanner vendor
- D. Only the SOC analyst who found it

**Q56.** An analyst knows the C2 IP used in one incident and searches all other logs for the same
address to discover further compromised hosts. In Diamond Model terms this is:

- A. Pivoting on the adversary vertex
- B. Pivoting on the victim vertex
- C. Pivoting on the infrastructure vertex
- D. Applying the Cyber Kill Chain

**Q57.** A web server was set to log only `error`-level messages to save disk. During an investigation
the analyst cannot find the directory brute-forcing (hundreds of `404`s) that preceded the
compromise. Which log-ingestion concept explains the gap?

- A. Time synchronization
- B. Enrichment
- C. Logging level set too low, hiding the attack
- D. Normalization

**Q58.** A SIEM alert fires. The analyst validates it as a true positive, classifies it as an insider
data-theft case and starts a timeline. Which phase is this?

- A. Detection and analysis
- B. Eradication
- C. Recovery
- D. Preparation

**Q59.** A scanner reports:

```text
[High] Reflected input in parameter "q" returned unencoded: <script>alert(1)</script>
       URL: https://shop.example/search?q=...
```

What weakness class is this and which scanner class found it?

- A. Cross-site scripting (XSS, CWE-79) — a web application scanner
- B. A misconfigured storage bucket — a cloud infrastructure scanner
- C. SQL injection (CWE-89) — a network scanner
- D. A missing OS patch — an infrastructure scanner

**Q60.** Searching `src_ip=203.0.113.45` in the SIEM returns firewall hits but none of the Windows
logon events that carry the same address in a field named `IpAddress`. Which ingestion step is
missing?

- A. Threat hunting
- B. Sandboxing
- C. Time synchronization
- D. Log aggregation and normalization to common field names

**Q61.** Personal data of EU residents was exfiltrated. Which external party has a legally mandated,
time-bound notification, and what caution does the hub attach to the deadline?

- A. Law enforcement; no deadline exists
- B. The scanner vendor; within one business day
- C. The ISAC; immediately
- D. The regulatory/supervisory body; notify within the prescribed window (GDPR's 72-hour rule — verify the exact figure for your jurisdiction)

**Q62.** A report lists a publicly readable storage bucket and an IAM role with wildcard permissions
attached to a workload. Which scanner class produced it?

- A. Passive network scanner
- B. Web application scanner
- C. Container image scanner
- D. Cloud infrastructure scanner (CSPM)

**Q63.** The team wants to pull the network cable on a host actively talking to a C2 server. What
should the containment decision weigh?

- A. Whether the CVSS score is above 7.0
- B. Evidence preservation, service availability and the risk of tipping off the adversary
- C. The lessons-learned schedule
- D. Only the cost of the network cable

**Q64.** A regional bank wants threat data shared specifically among its financial-sector peers,
including early warnings about campaigns hitting similar institutions. Which source fits BEST?

- A. A commercial vulnerability scanner
- B. An information sharing and analysis center (ISAC)
- C. A SOAR playbook
- D. The CVSS specification

**Q65.** The cost of fixing a Medium finding on a non-critical internal system exceeds the risk it
poses. Who may formally decide to live with it, and what must accompany the decision?

- A. The auditor; a compliance report
- B. The risk owner; documented, time-bounded sign-off that is revisited
- C. The scanner vendor; a suppression rule
- D. The analyst; a note in the ticket

**Q66.** The incident involves a crime. Why coordinate with law enforcement rather than simply wiping
and rebuilding?

- A. To obtain a compliance report
- B. To have them patch the systems
- C. To preserve evidence and avoid compromising any investigation
- D. To reduce the CVSS environmental score

**Q67.** An IoC feed entry added in 2023 flags an IP address that now belongs to a large cloud
provider's shared range; the rule floods the SOC with alerts on legitimate traffic. What CTI
principle was neglected?

- A. Strategic intel should never be automated
- B. OSINT is always unreliable
- C. IoAs should be converted into IoCs
- D. Intel must be scored for confidence and aged for timeliness and relevance

**Q68.** A seized laptop was left unlogged on an analyst's desk over the weekend before being imaged.
What is the consequence?

- A. The chain of custody is broken, undermining the evidence's defensibility
- B. The incident must be re-declared
- C. None, as long as the hash later matches
- D. The order of volatility was followed correctly

**Q69.** A patch was deployed on Tuesday. When should the finding be closed in the tracker?

- A. At the next quarterly compliance report
- B. When the deployment tool reports success
- C. After a re-scan verifies the vulnerability is gone
- D. As soon as the change ticket is approved

**Q70.** Leadership is worried about firmware-level malware that loads before the operating system.
Which hardware concepts establish whether a machine booted into a trustworthy state?

- A. NTP and syslog
- B. TPM and UEFI Secure Boot (hardware root of trust)
- C. DLP and tokenization
- D. SOAR and SIEM

**Q71.** Customers whose data was affected must be notified. Which content is appropriate?

- A. The CVSS vector of the exploited flaw
- B. The SIEM correlation rule that detected the attack
- C. Clear, plain-language facts: what happened, what data was affected and what they should do
- D. The full packet capture and malware hashes

**Q72.** Developers want to find design-level flaws in a new payment feature before any code is
written. Which practice fits, and where in the SDLC?

- A. Credentialed scanning, in production
- B. Penetration testing, after release
- C. Threat modeling, during design
- D. Container image scanning, at build

**Q73.** Authentication logs for one account:

```text
09:02:11 UTC  login OK  user=a.ruiz  src=203.0.113.88  geo=Madrid, ES     mfa=push-approved
09:41:52 UTC  login OK  user=a.ruiz  src=198.51.100.23 geo=Singapore, SG  mfa=push-approved
```

Which indicator is this and what should the analyst suspect?

- A. Nothing — MFA approval proves both logins are legitimate
- B. Account anomaly (impossible travel); compromised valid credentials, even though MFA was approved
- C. Application-related error output; a fuzzing attempt
- D. Network beaconing; a C2 channel

**Q74.** Which term names the defined team that is trained and empowered to respond when an incident is
declared?

- A. ISAC
- B. CSIRT (Computer Security Incident Response Team)
- C. Risk committee
- D. Change advisory board

**Q75.** A full active scan of a branch office over its saturated WAN link during business hours caused
a two-hour outage of the branch's line-of-business application. Which scan-planning factors
were ignored?

- A. Credential management
- B. Bandwidth/performance limits and scan timing
- C. CVE and CWE mapping
- D. Regulatory requirements and segmentation

**Q76.** An analyst receives an unknown binary found in a user's Downloads folder. What is the
appropriate FIRST, low-risk step?

- A. Execute it on the analyst workstation to see what happens
- B. Delete it and close the ticket
- C. Compute its SHA-256, check hash reputation, and inspect it with `file` and `strings`
- D. Email it to the whole SOC for opinions

**Q77.** The same incident produces a report for the responders and a briefing for the executive
committee. Which pairing is correct?

- A. Both audiences receive the raw SIEM export
- B. Executives receive nothing until the lessons-learned meeting
- C. Responders: risk and budget impact; executives: full IoC list and EDR queries
- D. Responders: technical timeline, IoCs and remediation steps; executives: business risk, impact and the decisions needed

**Q78.** An administrator account is confirmed compromised. What does *determining scope* mean in
incident management?

- A. Estimating the attacker's budget
- B. Identifying every affected system, account and data set
- C. Choosing which SIEM to buy
- D. Writing the executive summary

**Q79.** A breach is traced to a vulnerability the scanner never reported. Which combination BEST
reduces the chance of this outcome recurring?

- A. Scan less often to reduce load
- B. Rely on the CVSS base score alone
- C. Use multiple tools, credentialed scans and manual testing
- D. Suppress more findings to reduce noise

**Q80.** The public website is defaced with a political slogan; nothing was stolen and no ransom was
demanded. Which threat-actor type is MOST consistent with this?

- A. Malicious insider
- B. Nation-state APT
- C. Hacktivist
- D. Organized crime

---

## Part B — Performance-based scenarios (5 items)

Text-based stand-ins for the interactive PBQs. Each has a bounded answer set; write your
answers down before checking the key.

### PBQ 1 — Read the log, name the indicator and the ATT&CK tactic (Domain 1)

Eight consolidated SIEM lines from one morning. Internal hosts use private addresses; the
external address is from a documentation range. `m.alvarez` is a sales analyst whose
workstation is `ws-231` and who works from the `\\fs-02\sales` share every day.

```text
1  2026-05-12 07:58:02  dc01    Logon OK   user=svc_backup  src=10.20.30.41  type=Service
2  2026-05-12 07:58:40  dc01    Logon OK   user=m.alvarez   src=10.20.30.77  type=Network
3  2026-05-12 08:01:15  ws-231  Process    parent=explorer.exe  child=OUTLOOK.EXE
4  2026-05-12 08:03:22  ws-231  Process    parent=EXCEL.EXE  child=cmd.exe  cmdline="cmd /c powershell -w hidden -File %TEMP%\a.ps1"
5  2026-05-12 08:03:29  proxy   GET        http://198.51.100.9/a.txt  src=ws-231  bytes=412000
6  2026-05-12 08:04:01  ws-231  SchTask    created "\Updater"  action=%TEMP%\a.exe  trigger=logon  author=m.alvarez
7  2026-05-12 08:05:00  ws-231  NetConn    dst=198.51.100.9:443  interval=60s  count=12
8  2026-05-12 08:10:00  fs-02   File read  user=m.alvarez  path=\\fs-02\sales\Q2-forecast.xlsx
```

**Tasks**

1. List the line numbers that are indicators of potentially malicious activity.
2. For each, give the indicator **family** (network / host / application).
3. For lines 4, 6 and 7, give the MITRE ATT&CK **tactic** from this set: Initial Access,
   Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access,
   Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact.

### PBQ 2 — Prioritize the remediation worklist (Domain 2)

Six validated findings. Rank them 1 (fix first) to 6 and give a one-line justification for
each. All values are invented for the exercise.

| ID | CVSS v3.1 base | EPSS | In CISA KEV? | Exposure | Asset criticality |
|---|---|---|---|---|---|
| V1 | 9.8 | 0.05 | No | Isolated test lab, no route to production or internet | Low |
| V2 | 7.5 | 0.92 | Yes | Internet-facing VPN gateway | High |
| V3 | 8.8 | 0.40 | No | Internet-facing customer web application | High |
| V4 | 5.3 | 0.01 | No | Internal file server | Medium |
| V5 | 9.1 | 0.12 | Yes | Internal domain controller (not internet-facing) | Critical |
| V6 | 6.5 | 0.70 | No | Internet-facing marketing site | Low |

### PBQ 3 — Order the incident-response actions (Domain 3)

Scenario: a finance user clicked a phishing link, entered credentials, and an attacker created
a mailbox forwarding rule and attempted a fraudulent wire transfer. The actions below are
shuffled. Put them in the order they belong in the NIST SP 800-61 life cycle and label each
with its phase (Preparation / Detection & Analysis / Containment / Eradication / Recovery /
Post-Incident Activity).

- **A.** Hold a blameless lessons-learned meeting and update the phishing playbook.
- **B.** Disable the compromised account and revoke its active sessions.
- **C.** Confirm the alert is a true positive by reviewing the mailbox-rule audit log and the login source.
- **D.** Run the yearly phishing tabletop exercise and keep the CSIRT call tree current.
- **E.** Reset the password, re-enrol MFA, and remove the malicious forwarding rule and any tokens the attacker created.
- **F.** Restore the user's mailbox access and monitor the account for anomalous sign-ins.
- **G.** Push the attacker's sender domain and login IP into detection tooling and share them with the sector ISAC.
- **H.** Determine scope: which other users received the same email and whether any of them clicked.

### PBQ 4 — Match each SIEM alert to the correct triage action (Domain 1)

Assign exactly one action to each alert.

**Actions**

1. Detonate the file in a sandbox.
2. Escalate as a credential compromise: disable the account and start the IR playbook.
3. Close as a false positive and tune the rule.
4. Confirm the traffic content with packet capture, then decide.
5. Isolate the host with EDR and escalate to incident response.
6. Enrich and investigate (whois/DNS, reputation, user context) before deciding.

**Alerts**

- **A1.** Nightly backup job `bk-agent` trips the "mass file read" rule on `FS-01` at 02:00; identical volume for the last 90 nights.
- **A2.** EDR: `WINWORD.EXE` spawned `powershell.exe -enc` on `WS-0417`; PowerShell then wrote `svc.exe` to `C:\Users\Public` and started it.
- **A3.** Proxy: one user visited the newly-seen domain `login-secure-portal.example` once, 2 KB transferred, no download.
- **A4.** Mail gateway quarantined `invoice_0392.xlsm` with an unrecognised macro; the hash is unknown to every reputation service.
- **A5.** NetFlow: a workstation sends 512-byte UDP packets to 203.0.113.200:53 exactly every 30 seconds for six hours; the resolver is not that address.
- **A6.** Impossible travel: `a.ruiz` had MFA-approved logins from Madrid and Singapore 40 minutes apart, then a new inbox rule forwarding mail to an external address.

### PBQ 5 — Executive summary or technical report? (Domain 4)

The same incident produces two documents: a one-page **executive summary** for the leadership
committee and a **technical report** for responders and system owners. Place each content item
in the document it belongs to.

1. Full timeline with hostnames, process IDs and file hashes.
2. Business impact: six hours of order-processing downtime and an estimated cost band.
3. Whether customer data was affected and which regulator notification is due, and by when.
4. IoC list (hashes, domains, IPs) formatted for SIEM import.
5. The root cause in one sentence and the decision leadership must make (fund the MFA rollout).
6. The EDR queries used to scope the intrusion.
7. Mean time to detect and mean time to respond for this incident against last quarter's figures.
8. Step-by-step eradication actions performed on each host.
9. Three prioritised recommendations, each with an owner and a rough cost.
10. The CVSS vector of the exploited vulnerability.

---

## Answer key

Do not read this until the 165 minutes are up. Each entry gives the answer, a short
explanation, the domain number and the page to re-read.

### Part A

- **Q1 — A.** Cross-source correlation depends on a shared clock; a 7-minute skew pushes the pair outside the rule's window. Time synchronization (NTP) is the log-ingestion fundamental the page flags for exactly this failure. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q2 — C.** Credentialed scans read patch levels from inside and are more accurate; banner-based "potential" findings are the classic false positive, which is suppressed only after confirmation and documented. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q3 — A.** Isolating a host and disabling an account to stop the spread is short-term containment, which buys time before eradication. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q4 — D.** A service-level agreement's uptime commitment limits downtime windows for patching. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q5 — C.** A document application spawning a hidden, encoded PowerShell is the classic host-related parent/child anomaly the page lists as likely code execution. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q6 — D.** Fragile OT/ICS targets can be knocked over by the scan itself; the page's mitigations are passive discovery, read-only checks, throttling and scheduled maintenance windows. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q7 — C.** Long-term containment applies temporary fixes so the business keeps running while eradication is prepared. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q8 — B.** The page lists unusual outbound connections from an application server as an application-related indicator: the app reaching attacker infrastructure, here on an unexpected port. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q9 — A.** Agent-based scanning runs locally and reports in, suiting mobile and intermittent hosts that a central agentless scanner cannot reach. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q10 — A.** A memorandum of understanding between parties can constrain who may touch a system or when. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q11 — C.** Strategic CTI is long-term, risk-and-trend level intelligence for leadership; tactical is TTPs/IoCs the SOC actions, operational covers campaigns and intent. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q12 — A.** An external scan shows the attack surface an outsider can reach; uncredentialed mimics that outsider's view. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q13 — B.** Eradication removes the root cause: delete malware, close the vulnerability, disable compromised accounts, rebuild from known-good images. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q14 — B.** Domain age, registrant and reputation are exactly what DNS/whois and threat-intel reputation lookups answer; the page groups them as the infrastructure-investigation technique. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q15 — D.** Legacy systems may have no patch at all; when remediation is blocked the answer is compensating controls or risk acceptance, reported to the risk owner. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q16 — D.** `S:C` means scope changed; `PR:L` means low privileges are needed, `A:N` means no availability impact and `UI:N` means no user interaction. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q17 — B.** Sandboxing detonates a sample in isolation to observe behavior safely; static file analysis (hashes, strings) complements it but does not show behavior. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q18 — A.** Recovery restores normal operation, validates cleanliness, monitors for recurrence and returns systems in a controlled way. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q19 — D.** Exploit-code maturity is a Temporal/Threat metric that evolves over time; Base metrics are intrinsic and Environmental is set by the organisation. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q20 — C.** An IoA describes the technique, not a swappable artifact, so it survives recompilation; an IoC such as a hash is invalidated by a single byte change. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q21 — B.** Proprietary, vendor-locked systems cannot be modified by the customer; you wait on the vendor. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q22 — D.** CVSS measures severity, not risk; the page's key point is that a Critical on an isolated box can rank below a Medium on a public, business-critical server after environmental context. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q23 — D.** Order of volatility: registers/cache, RAM, network state, running processes, then disk, then logs/archives, then physical media. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q24 — B.** Threat hunting is hypothesis-driven: start from intel or an ATT&CK technique, state what evidence would exist if it happened, then test the data. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q25 — D.** CVSS v3.x bands: 4.0–6.9 Medium, 7.0–8.9 High; the boundary falls exactly between these two scores. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q26 — D.** A fix that breaks compatibility or removes a feature the business relies on is the "degrading functionality" inhibitor. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q27 — C.** The page's hunt loop ends in "turn finding into a new detection" whether or not evidence is found; every hunt should harden detection. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q28 — B.** Hashing proves integrity so evidence is defensible; with chain-of-custody records it shows who handled it and that it was unaltered. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q29 — C.** EPSS gives a 0–1 probability of exploitation in the wild within 30 days; it answers "how likely" where CVSS answers "how bad". *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q30 — D.** A single pane of glass is one consolidated view so analysts stop tool-hopping; it is achieved by integrating SIEM, EDR, ticketing and intel through APIs. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q31 — D.** The trend line of open criticals/highs is the metric the page says leadership watches; raw findings belong with remediation teams. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q32 — D.** KEV lists CVEs confirmed exploited in the wild with a federal remediation due date; a KEV entry is no longer hypothetical and jumps the queue. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q33 — B.** Automate the repetitive and deterministic (enrichment, ticket creation, known-bad blocking) and keep human judgment for scoping, analysis and decisions. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q34 — D.** Incident severity is judged by functional impact, information impact and recoverability, not by one number. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q35 — D.** When you cannot patch, compensating controls (segmentation, tighter rules, monitoring, virtual patching) reduce exploitability while the vulnerability remains. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q36 — D.** Encryption protects confidentiality but blinds the analyst; the page's answer is planned decryption/inspection points or reliance on metadata, never weakening encryption. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q37 — C.** Scan coverage is the percentage of the estate actually being scanned. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q38 — B.** The page's mapping pairs Actions on Objectives with Collection, Exfiltration and Impact; Installation maps to Persistence/Defense Evasion and Delivery to Initial Access. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q39 — A.** The page lists the security awareness program under managerial (administrative/governance) controls. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q40 — A.** Segmentation divides the network into zones so one compromise cannot freely reach others, and the zone boundaries are natural monitoring chokepoints. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q41 — D.** Zero Trust authenticates and authorizes every request continuously, producing identity-anchored telemetry and explicit enforcement points the SOC can watch. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q42 — B.** Patch cycles and configuration reviews are operational controls executed by people day to day; the deployed patch is a technical control. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q43 — D.** IoC generation is a post-incident activity: turn findings into indicators for detection and share them with peers/ISACs. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q44 — D.** Recurrence/reopen rate asks "are fixes sticking?"; recurring findings point to drift from the secure baseline. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q45 — A.** DLP monitors sensitive data (PII, PHI, cardholder data) leaving the environment; a bulk card-number pattern in outbound mail is its textbook trigger. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q46 — C.** Locks, badges, cameras and secure facilities for critical/OT assets are physical controls. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q47 — C.** The lessons-learned meeting is held promptly, is blameless, and feeds changes to the plan, playbooks and controls. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q48 — A.** Sustained abnormal resource consumption from an unknown process with outbound connections is the host-related indicator the page ties to cryptomining or a runaway implant. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q49 — D.** CWE catalogs weakness types (the class/root cause); CVE identifies a specific instance in a specific product. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q50 — D.** Incident declaration is the formal classification point that starts the clock and triggers notification duties under predefined criteria. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q51 — D.** Activity on a non-standard port (a protocol running where it should not) is a network-related evasion indicator. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q52 — C.** Installation is the stage where persistence (a backdoor) is dropped; C2 and actions on objectives follow. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q53 — A.** Preparation is everything done before an incident: plan, playbooks, CSIRT, communication plan, tooling, training and tabletops. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q54 — C.** Unusual registry or scheduled-task entries are the host-related indicators of persistence; an executable in a public folder created at night by a non-admin is not a system update. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q55 — A.** Legal reviews privilege, liability and obligations, and PR manages the narrative; both review external messaging first. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q56 — C.** The Diamond Model's four vertices are adversary, capability, infrastructure and victim; reusing a known C2 address to find other victims pivots on infrastructure. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q57 — C.** Logging level is the verbosity captured; too low hides attacks, too high buries them. Recon requests are informational, not errors. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q58 — A.** Detection and analysis is where you validate the alert, triage and classify by type, determine scope and impact, and document a timeline. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q59 — A.** Reflected unencoded script input is XSS (CWE-79), an OWASP Top 10 issue that web-application scanners find by actively testing inputs. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q60 — D.** Normalization maps many formats to common fields so one query spans firewalls, hosts and apps; without it the same value hides under different field names. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q61 — D.** Regulators require breach notification within prescribed deadlines such as GDPR's 72 hours; the page marks the exact window as verify. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q62 — D.** Misconfigured storage, over-broad IAM and posture drift are cloud-infrastructure / Cloud Security Posture Management findings. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q63 — B.** The page names exactly these containment trade-offs; immediate isolation can destroy volatile evidence and alert the adversary. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q64 — B.** ISACs are sector-specific communities that share threat data among members. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q65 — B.** Risk acceptance is a formal, documented, time-bounded decision by the risk owner, and it is revisited rather than forgotten. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q66 — C.** Law enforcement is engaged when a crime has occurred, coordinating to preserve evidence and the investigation. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q67 — D.** The page stresses confidence levels and timeliness/relevance: intel must be scored and aged, not trusted blindly. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q68 — A.** Chain of custody requires an unbroken record of who handled evidence and when; an unlogged gap breaks it. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q69 — C.** The lifecycle ends with re-scan and verify; patch management is test, schedule, deploy, verify by re-scan. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q70 — B.** The Trusted Platform Module, UEFI/Secure Boot and a hardware root of trust are the concepts the page names for a trustworthy boot state. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q71 — C.** Match the message to the audience: clear plain-language facts for customers, technical detail for responders, risk and impact for leadership. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q72 — C.** Threat modeling asks "what can go wrong here?" during design so flaws are found before code ships; secure SDLC bakes security into each phase. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q73 — B.** Impossible-travel logins are the account anomaly the page lists; modern intrusions ride valid credentials, and an approved push does not rule out the user approving a fraudulent prompt. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q74 — B.** Preparation includes defining a CSIRT, the team that carries out the response. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q75 — B.** CompTIA's scan-planning factors include bandwidth/performance limits and scan timing; both were violated here. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q76 — C.** File analysis starts with hashes, type, strings and metadata plus hash reputation; behavior is observed later in a sandbox, never on a production workstation. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*
- **Q77 — D.** Technical detail goes to responders; leadership needs risk and impact to decide budget and risk acceptance. *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*
- **Q78 — B.** Scope identifies every affected asset, account and data set; impact then captures the business consequence. *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*
- **Q79 — C.** That outcome is a false negative, the most dangerous validation result; the page's mitigations are multiple tools, credentialed scans and manual testing. *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*
- **Q80 — C.** Hacktivists are motivated by ideology and favour visible acts like defacement; organized crime seeks money, APTs seek long-term access. *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*

### Part B

**PBQ 1** *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*

- Indicators: **lines 4, 5, 6 and 7**. Lines 1–3 and 8 are normal (a service logon, a network
  logon, Explorer launching the mail client, a sales user opening a file on the sales share
  used every day — worth reviewing when the incident is scoped, but not an indicator on its
  own).
- Families: **4 host** (suspicious parent/child chain: a spreadsheet launching a hidden
  PowerShell), **5 network** (download of a payload from an unknown external host — you may
  also argue application, since it is the proxy that saw it), **6 host** (unusual scheduled
  task created for persistence), **7 network** (fixed 60-second interval to one external
  host: beaconing).
- Tactics: **line 4 Execution**, **line 6 Persistence**, **line 7 Command and Control**.
- Scoring: 1 point for the correct set of lines, 1 for the families, 2 for the three tactics
  (all three correct for both points, two of three for one point).

**PBQ 2** *(Domain 2 — [Vulnerability Management](../domains/02-vulnerability-management.md))*

Expected order and justification, following the page's prioritization flow (KEV, then EPSS,
then CVSS with environmental context — exposure and asset value):

1. **V2** — in KEV (confirmed exploited), highest EPSS, internet-facing, high-value asset: every
   factor points the same way.
2. **V5** — in KEV on a critical asset; internal exposure keeps it just behind V2, but a
   confirmed-exploited flaw on a domain controller cannot wait.
3. **V3** — not in KEV, but internet-facing, high-value and a 8.8 base with a material EPSS.
4. **V6** — internet-facing with high exploitation probability, but a low-value asset and a
   Medium base score.
5. **V1** — a 9.8 base score is severity, not risk: the asset is isolated with no route out and
   low value, so environmental context pushes it down.
6. **V4** — lowest severity, negligible EPSS, internal, medium value.

Scoring: 2 points if positions 1–4 match, 1 point if V2 and V5 hold positions 1–2 and V1 is not
in the top three, 1 further point for a justification that names KEV, EPSS and exposure/asset
value. Two swaps are accepted with a written reason: V3 and V6 (V6's higher EPSS against V3's
higher severity and asset value — the page's flow elevates high EPSS, so either order is
defensible), and V1 and V4 (a 9.8 on a box that is patched anyway during the next lab rebuild
is a defensible fifth or sixth).

**PBQ 3** *(Domain 3 — [Incident Response and Management](../domains/03-incident-response-and-management.md))*

| Order | Action | Phase |
|---|---|---|
| 1 | D — tabletop exercise and current call tree | Preparation |
| 2 | C — validate the alert as a true positive | Detection & Analysis |
| 3 | H — determine scope (who else received/clicked) | Detection & Analysis |
| 4 | B — disable the account and revoke sessions | Containment |
| 5 | E — reset password, re-enrol MFA, remove the rule and tokens | Eradication |
| 6 | F — restore access and monitor for recurrence | Recovery |
| 7 | G — generate IoCs, push to detection, share with the ISAC | Post-Incident Activity |
| 8 | A — blameless lessons-learned meeting, update the playbook | Post-Incident Activity |

G and A may be swapped: both are post-incident activities. C and H may also be swapped when
the analyst scopes before fully validating; the essential points are that Preparation comes
first, containment precedes eradication, and lessons learned/IoC generation close the loop.
Scoring: 2 points for the phases all labelled correctly, 2 points for the order (allowing the
two swaps above).

**PBQ 4** *(Domain 1 — [Security Operations](../domains/01-security-operations.md))*

| Alert | Action | Why |
|---|---|---|
| A1 | 3 | Same benign job, same volume, every night for 90 days: a false positive to tune out and document. |
| A2 | 5 | A document app spawning encoded PowerShell that drops and runs an executable is a true positive in progress: isolate and escalate. |
| A3 | 6 | A single small visit to a newly-seen domain is suspicious, not conclusive: enrich (domain age, whois, reputation, what the user was doing) before acting. |
| A4 | 1 | An unknown macro document with no reputation data is exactly what sandbox detonation is for. |
| A5 | 4 | Fixed-interval packets to a non-resolver on port 53 look like beaconing or DNS tunneling; packet capture confirms the content before isolation. |
| A6 | 2 | Impossible travel plus a forwarding rule is the signature of compromised valid credentials: disable the account and start the IR playbook. |

Scoring: 4 points for six correct, 3 for five, 2 for four, 1 for three, 0 below that.

**PBQ 5** *(Domain 4 — [Reporting and Communication](../domains/04-reporting-and-communication.md))*

- **Executive summary:** 2, 3, 5, 7, 9 — business impact, regulatory exposure and deadlines,
  the root cause and the decision required, response metrics against trend, and prioritised
  recommendations with owners and cost. Leadership decides budget and risk acceptance; it needs
  risk and impact in plain language.
- **Technical report:** 1, 4, 6, 8, 10 — the detailed timeline, importable IoCs, scoping
  queries, per-host eradication steps and the CVSS vector belong with responders and system
  owners who act on technical detail.

Scoring: 4 points for all ten placed correctly, 3 for nine, 2 for eight, 1 for seven, 0 below
that. Item 7 (MTTD/MTTR) may reasonably appear in both; accept either placement.

---

## Where to go next

- [practice-questions.md](practice-questions.md) — the per-domain question bank to drill the
  domains you scored under 80% here.
- [study-plan.md](study-plan.md) — where this mock sits in the seven-week schedule.
- [../reference/glossary.md](../reference/glossary.md) — the SOC vocabulary the items lean on.
- [../README.md](../README.md) — the hub's preparation procedure and readiness gate.

## Sources

- CompTIA — Cybersecurity Analyst (CySA+) CS0-003 official certification page (max 85
  questions, MCQ + PBQ, 165 minutes, 750 on a 100–900 scale, domain weights 33 / 30 / 20 / 17
  percent): <https://www.comptia.org/en-us/certifications/cybersecurity-analyst/>
- MITRE ATT&CK — adversary tactics and techniques (tactic names used in PBQ 1 and Q-items):
  <https://attack.mitre.org/>
- Sibling domain pages this mock is written from:
  [Domain 1 — Security Operations](../domains/01-security-operations.md) ·
  [Domain 2 — Vulnerability Management](../domains/02-vulnerability-management.md) ·
  [Domain 3 — Incident Response and Management](../domains/03-incident-response-and-management.md) ·
  [Domain 4 — Reporting and Communication](../domains/04-reporting-and-communication.md)
- Hub pages for the exam format and the readiness rule:
  [../00-overview/exam-and-objectives.md](../00-overview/exam-and-objectives.md) ·
  [../../../learning/how-to-prepare-a-cert.md](../../../learning/how-to-prepare-a-cert.md)
- The 85% pass line and the 80%-per-domain rule are this repo's own readiness thresholds, not
  CompTIA figures. All questions are original study aids and are **not** CompTIA exam items.
