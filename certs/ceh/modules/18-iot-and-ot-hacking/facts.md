# Module 18 — IoT and OT Hacking · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## IoT architecture (layered model)
| Layer | What it is | Example |
|---|---|---|
| Edge / Device | The "things" — sensors, actuators, MCUs, firmware | Smart camera, thermostat |
| Access / Gateway | First hop; protocol translation, local aggregation | Home hub, IoT gateway |
| Internet / Communication | Transport to the cloud | Wi-Fi, cellular, LPWAN |
| Middleware | Device mgmt, message brokers, data storage | MQTT broker, cloud IoT core |
| Application | User/business logic | Mobile app, web dashboard |

## The four IoT communication models
**Device-to-Device · Device-to-Cloud · Device-to-Gateway · Back-End Data-Sharing.** (Gateway model adds a local hop that translates protocols; back-end sharing lets multiple services consume the same data.)

## IoT communication protocols (ports + role)
| Protocol | Transport / radio | Port | One-liner |
|---|---|---|---|
| **MQTT** | App messaging over **TCP** | **1883** (TLS **8883**) | Lightweight **publish/subscribe** via a broker; often unauthenticated |
| **CoAP** | **RESTful** over **UDP** | **5683** (DTLS **5684**) | HTTP-like request/response for constrained devices |
| **Zigbee** | IEEE 802.15.4, 2.4 GHz mesh | — (RF) | Low-power mesh home/building automation |
| **BLE** | Bluetooth Low Energy, 2.4 GHz | — (RF) | Short range; GATT profiles; weak pairing |
| **LoRaWAN** | Sub-GHz LPWAN, star-of-stars | — (RF) | **Long-range**, low-power WAN; AppKey/NwkKey |
| **Z-Wave / 6LoWPAN** | Sub-GHz / 802.15.4 + IPv6 | — (RF) | Home mesh / IPv6 over low-power radio |

## OWASP IoT Top 10 & attack surface
The **OWASP IoT Top 10** is the authoritative list of critical IoT weaknesses — cite the official page, don't paraphrase from memory. The perennial **#1 theme is weak / guessable / hardcoded passwords (default creds)**, followed by insecure network services, insecure ecosystem interfaces (web/cloud/mobile), and lack of a secure update mechanism.

**IoT attack-surface areas** (where you probe):
- **Device firmware** — extract with `binwalk`, hunt hardcoded creds/keys.
- **Physical / debug** — UART/JTAG serial console, chip-off.
- **Network services** — exposed Telnet/UPnP/MQTT, default creds.
- **Web/cloud/mobile interface** — auth bypass, insecure API, secrets in the app.
- **Update mechanism** — unsigned firmware, MITM of OTA updates.
- **Ecosystem comms** — sniff/replay Zigbee/BLE, weak pairing.

## Mirai (the archetypal IoT botnet)
Scanned the internet for open **Telnet (23 / 2323)** and tried a built-in list of **default/factory credentials**. Enlisted cameras/DVRs/routers into a botnet for massive **DDoS**; source code was leaked → many variants. **Exam lesson: default creds + exposed management service = mass compromise.**

## OT / ICS vocabulary
| Term | Meaning |
|---|---|
| **ICS** | Industrial Control Systems (umbrella) |
| **SCADA** | Supervisory Control And Data Acquisition — geographically **distributed** monitoring/control |
| **DCS** | Distributed Control System — process control within a **single plant** |
| **PLC** | Programmable Logic Controller — ruggedized computer that **runs the process** |
| **RTU / IED** | Remote Terminal Unit / Intelligent Electronic Device — field controllers |
| **HMI** | Human-Machine Interface — the **operator screen** |
| **Historian** | Time-series database of process values |

## OT protocols (most have NO auth/encryption by design)
| Protocol | Port | Domain |
|---|---|---|
| **Modbus** (TCP) | **502** | Generic industrial; trivially read/write |
| **DNP3** | **20000** | Electric / water utilities |
| **S7comm** | **102** | Siemens S7 PLCs |
| **EtherNet/IP (CIP)** | **44818** | Rockwell / Allen-Bradley |
| **BACnet** | **47808/UDP** | Building automation |
| **OPC UA** | **4840** | Modern, **security-capable** interoperability |

Modbus/DNP3/S7comm assume a **trusted network** — no login, no crypto. **OPC UA is the one modern option that can authenticate/encrypt.**

## The Purdue model (levels 0–5 + IDMZ)
| Level | Zone | What lives there |
|---|---|---|
| **L5** | IT / Enterprise | Corporate IT, internet-facing |
| **L4** | IT / Site business | ERP, email, IT services |
| **L3.5** | **IDMZ** | The OT/IT boundary — jump hosts, proxies, brokers |
| **L3** | OT / Site ops | MES, historians, patch/AV, engineering workstations |
| **L2** | OT / Area supervisory | **HMI, SCADA servers** |
| **L1** | OT / Basic control | **PLCs, RTUs, IEDs** run the logic |
| **L0** | OT / Physical process | **Sensors, actuators, motors, valves** |

Attacks flow **down**; safety comes from keeping people and IT **out** of the lower levels. **IT/OT convergence** (remote access, cloud historians) flattened these zones — which is exactly why segmentation and brokered access matter.

## IEC 62443 — zones & conduits
ISA/IEC 62443 is the ICS security standard. Group assets into **zones** (equal trust/risk) and allow traffic only through defined **conduits** (controlled pathways). Deny IT→OT by default; allow-list only. Pair with **unidirectional gateways / data diodes** so telemetry flows **up** while control can never flow **down**.

## Key tools
- **Shodan / Censys** — search a pre-built **index** of internet-exposed devices (passive; you query the index, you never connect to a result).
- **Nmap** — port/service discovery + ICS NSE scripts (e.g. `modbus-discover`).
- **binwalk** — firmware carving / filesystem extraction.
- **pymodbus** — Python Modbus client/server; talk to a simulator.
- **Wireshark** — dissect MQTT / Modbus / DNP3.

## The PAM angle (why this is a privileged-access problem)
- **Vault + rotate device credentials** (PLC/HMI/RTU) — kills the Mirai default-cred class. CyberArk component: **CPM**.
- **Broker every human/remote path through a jump host in the IDMZ** — PSM/PSMP as the **sole ingress** into the OT DMZ, aligned to IEC 62443 conduits. No one touches L0/L1 directly.
- **Remote Access for vendors** — VPN-less, time-boxed (JIT), MFA, session recording — never a standing VPN to the plant floor.
- Treat OT as **crown-jewel Tier 0**; use unidirectional gateways so monitoring pulls data **up** while nothing pushes control **down**.

## Top traps
- **MQTT = pub/sub over TCP (1883/8883); CoAP = REST over UDP (5683/5684).** One wrong word (TCP↔UDP, pub-sub↔request-response) flips the answer.
- **Ports:** Modbus **502**, DNP3 **20000**, S7comm **102**, EtherNet/IP **44818**, BACnet **47808/UDP**, OPC UA **4840**.
- **SCADA vs DCS vs PLC:** SCADA = distributed supervisory monitoring; DCS = in-plant process control; PLC = the field controller both use.
- **Purdue levels:** L0 process, L1 PLC/RTU, L2 HMI/SCADA, L3 site ops/historian, **L3.5 = IDMZ**, L4/L5 = IT.
- **Modbus/DNP3/S7comm have no built-in auth or encryption** — the defense is the *network*, not the protocol. **OPC UA** is the secure-capable one.
- **Mirai = Telnet + default creds → DDoS.** Default IoT passwords at scale ⇒ think Mirai.
- Shodan/Censys query an **index** — passive recon; you never connect to the result.
