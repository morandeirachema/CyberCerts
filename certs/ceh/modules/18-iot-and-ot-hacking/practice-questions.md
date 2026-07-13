# Module 18 — IoT and OT Hacking · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** An IoT sensor publishes readings to a broker, and a dashboard subscribes to receive them. The messaging is lightweight and rides over **TCP**. Which protocol and model is this?

- A. CoAP, request/response over UDP
- B. MQTT, publish/subscribe over TCP
- C. DNP3, master/outstation over TCP
- D. BACnet, client/server over UDP

<details><summary>Answer</summary>

**B. MQTT, publish/subscribe over TCP.** MQTT uses a **broker** with a **pub/sub** model on **1883** (TLS **8883**). CoAP is the RESTful-over-UDP option (5683). The *broker + publish/subscribe + TCP* triad is the MQTT fingerprint. **Trap:** swap a single word (TCP↔UDP, pub/sub↔request/response) and the answer flips to CoAP.
</details>

---

**Q2.** Which statement correctly contrasts **CoAP** with **MQTT**?

- A. CoAP is publish/subscribe over TCP; MQTT is RESTful over UDP
- B. CoAP is RESTful over UDP (port 5683); MQTT is publish/subscribe over TCP (port 1883)
- C. Both run over TCP on port 1883
- D. CoAP requires a broker; MQTT is brokerless

<details><summary>Answer</summary>

**B.** **CoAP = RESTful request/response over UDP, port 5683** (DTLS 5684). **MQTT = publish/subscribe over TCP, port 1883** (TLS 8883, broker-based). This TCP/UDP + pub-sub/REST swap is the single most-tested distinction in the module.
</details>

---

**Q3.** A utility SCADA system uses a protocol on **TCP port 20000** to talk to substation devices. Which protocol is it?

- A. Modbus
- B. S7comm
- C. DNP3
- D. EtherNet/IP

<details><summary>Answer</summary>

**C. DNP3** (port **20000**) is common in **electric and water utilities**. Modbus = **502**, S7comm = **102** (Siemens), EtherNet/IP = **44818** (Rockwell/Allen-Bradley). Like most legacy OT protocols, DNP3 ships with **no built-in authentication or encryption**.
</details>

---

**Q4.** Match the protocol to its default port. Which pairing is **wrong**?

- A. Modbus → 502
- B. S7comm → 102
- C. BACnet → 47808
- D. OPC UA → 44818

<details><summary>Answer</summary>

**D is wrong.** **OPC UA = 4840**; **44818** is **EtherNet/IP** (Rockwell/Allen-Bradley). The others are correct: Modbus 502, S7comm 102 (Siemens), BACnet 47808/UDP (building automation). OPC UA is also the outlier that is **security-capable** (can authenticate and encrypt) — unlike the legacy protocols.
</details>

---

**Q5.** In the **Purdue model**, at which level do the **PLCs, RTUs, and IEDs** that run the control logic live?

- A. Level 0
- B. Level 1
- C. Level 2
- D. Level 3

<details><summary>Answer</summary>

**B. Level 1 (Basic control).** L0 = physical process (sensors/actuators/motors/valves), **L1 = PLC/RTU/IED**, L2 = HMI/SCADA servers, L3 = site ops/historian. Attacks flow *down* toward L0/L1, so safety depends on keeping IT and people out of the lower levels.
</details>

---

**Q6.** What sits at Purdue **Level 3.5**, and what is its purpose?

- A. Level 3.5 is the physical process layer where sensors report
- B. The IDMZ — the OT/IT boundary hosting jump hosts, proxies, and brokers
- C. The enterprise ERP zone
- D. The PLC control layer

<details><summary>Answer</summary>

**B. The IDMZ (Industrial DMZ).** L3.5 is the **boundary between OT (L0–L3) and IT (L4–L5)**. It hosts jump hosts, proxies, and message brokers so no IT system or human reaches the control layers directly. This is where PAM belongs — make a brokered jump host the *only* ingress into OT.
</details>

---

**Q7.** The **Mirai** botnet compromised hundreds of thousands of IoT devices. What was its primary infection technique?

- A. Exploiting a zero-day in MQTT brokers
- B. Scanning for open Telnet (23/2323) and trying default/factory credentials
- C. Cracking WPA2 on smart-home Wi-Fi
- D. MITM of unsigned OTA firmware updates

<details><summary>Answer</summary>

**B.** Mirai scanned the internet for open **Telnet (23/2323)** and tried a built-in list of **default credentials**, enlisting cameras/DVRs/routers into a **DDoS** botnet. **Exam lesson: default creds + an exposed management service = mass compromise.** The fix class is disable Telnet, change/rotate defaults, and vault device credentials.
</details>

---

**Q8.** In an ICS, which component is the **operator-facing screen** used to monitor and issue commands to the process?

- A. PLC
- B. Historian
- C. HMI
- D. RTU

<details><summary>Answer</summary>

**C. HMI (Human-Machine Interface).** It is the operator's screen (typically at Purdue L2 with SCADA servers). The **PLC** is the field controller running the logic (L1); the **Historian** is the time-series database of process values (L3); the **RTU** is a remote field controller. Don't confuse the operator screen (HMI) with the controller (PLC).
</details>

---

**Q9.** Which statement best distinguishes **SCADA**, **DCS**, and **PLC**?

- A. They are three names for the same device
- B. SCADA = distributed supervisory monitoring; DCS = in-plant process control; PLC = the field controller both use
- C. SCADA runs the logic; PLC supervises multiple plants; DCS is a database
- D. DCS is geographically distributed; SCADA is confined to one plant

<details><summary>Answer</summary>

**B.** **SCADA** = geographically **distributed** supervisory monitoring/control; **DCS** = process control within a **single plant**; **PLC** = the ruggedized **field controller** that actually runs the logic (used by both SCADA and DCS). Option D swaps the SCADA/DCS scope — a classic trap.
</details>

---

**Q10.** Which standard defines OT security in terms of **zones and conduits**, grouping assets by trust and allowing traffic only through controlled pathways?

- A. OWASP IoT Top 10
- B. IEC 62443
- C. PCI DSS
- D. NIST 800-53 AC family

<details><summary>Answer</summary>

**B. IEC 62443** (ISA/IEC 62443). Assets of equal trust/risk go into a **zone**; traffic between zones is permitted only through a defined **conduit**. Practically: deny IT→OT by default, allow-list only, and pair with unidirectional gateways. The OWASP IoT Top 10 is for IoT device weaknesses, not OT zoning.
</details>

---

**Q11.** You subscribe to `#` on an unauthenticated MQTT broker and instantly see every device's messages, then publish a spoofed reading that a controller accepts. Which OWASP IoT theme does this illustrate?

- A. Insecure network services (no authentication on the broker)
- B. Physical debug-port exposure
- C. Insecure OTA update mechanism
- D. Weak RF pairing

<details><summary>Answer</summary>

**A. Insecure network services.** The broker requires no authentication, so `#` (the multi-level wildcard) lets anyone **read every topic** and **inject** on any topic — a trust failure, not a code bug. The control is to require broker auth/TLS and, at the architecture level, segment and broker access (PAM). It maps to the same default/weak-credential family that tops the OWASP IoT Top 10.
</details>

---

**Q12.** A Modbus client reads and writes a PLC's registers with **no login and no encryption**. What is the primary reason, and the correct defense?

- A. The engineer forgot to enable Modbus's built-in TLS; enable it
- B. Modbus has no authentication/encryption by design; the defense is network segmentation, not the protocol
- C. The PLC firmware is out of date; patch it to add auth
- D. Modbus authenticates by MAC address; spoof-protect the switch

<details><summary>Answer</summary>

**B.** Legacy OT protocols like **Modbus assume a trusted, isolated network** — they have **no built-in auth or crypto**, so there is nothing to "turn on." The durable defense is **segmentation, IEC 62443 zones/conduits, and brokered access**, keeping writes off the wire from untrusted sources. (OPC UA is the modern, security-capable alternative.)
</details>

---

**Q13.** Which reconnaissance approach lets you gauge how many Modbus or MQTT devices are exposed on the internet **without connecting to any of them**?

- A. Nmap SYN scan of the target's /16
- B. Query the Shodan/Censys index (passive)
- C. `mosquitto_sub -t '#'` against each host
- D. Modbus FC3 read against each host

<details><summary>Answer</summary>

**B. Query the Shodan/Censys index.** Shodan and Censys maintain a **pre-built index** of internet-exposed devices, so searching (e.g. `port:502`) returns a **count and metadata** without you touching any device — passive recon. Options A, C, D are all *active* connections to systems you don't own, which is exactly what OT safety forbids.
</details>

---

**Q14.** A vendor needs occasional remote access to a PLC at Purdue L1. Which design aligns with the module's PAM guidance?

- A. Give the vendor a standing site-to-site VPN straight to the PLC subnet
- B. Time-boxed, VPN-less Remote Access brokered through a jump host in the IDMZ, with MFA and session recording
- C. Publish the PLC's HMI to the internet behind a strong password
- D. Share the PLC's default credentials over email for the maintenance window

<details><summary>Answer</summary>

**B.** No human or vendor touches L0/L1 directly. Route the vendor through a **jump host in the IDMZ (L3.5)** using **time-boxed (JIT) Remote Access**, **MFA**, and **session recording** — never a standing VPN to the plant floor. CyberArk mapping: **Remote Access** for vendors, **PSM/PSMP** as the sole ingress, **CPM** to vault/rotate the device credential.
</details>

---

**Q15.** The recurring #1 weakness across the OWASP IoT Top 10 — and the root cause behind Mirai — is:

- A. Lack of a secure update mechanism
- B. Weak, guessable, or hardcoded (default) passwords
- C. Insecure data transfer without TLS
- D. Insufficient privacy protection

<details><summary>Answer</summary>

**B. Weak/guessable/hardcoded (default) passwords.** It is the perennial top IoT weakness and the exact vector Mirai exploited over Telnet. Others (insecure update, insecure data transfer, privacy) are real but secondary. Fix class: change/rotate defaults, disable Telnet, and **vault + rotate device credentials** (PAM/CPM). Cite the official OWASP page rather than paraphrasing on the job.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the protocol/port table and the Purdue-model + IEC 62443 sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
