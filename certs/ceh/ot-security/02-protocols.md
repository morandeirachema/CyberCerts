# 02 — OT Protocols and Their (Missing) Security

> Level 2. The industrial protocols, what each is for, and the recurring flaw: most were designed for **trusted, isolated, deterministic** networks and have **no authentication and no encryption**. The defense is the network, not the protocol.

← Back to the [ladder](README.md) · Practice these on the [OT lab](../labs/ot/README.md)

## Why they're insecure by design

These protocols were born in the 1970s–90s on serial links and air-gapped LANs. Identity and crypto add latency, complexity, and failure modes that a hard-real-time control loop couldn't tolerate — and the network was *assumed* trusted. Then IT/OT convergence ([01](01-foundations.md)) put them on routable, reachable networks, exposing a protocol that will happily obey **anyone** who can send it a packet.

Three failure classes show up everywhere:
- **No authentication** → any host can issue commands (read *and* write).
- **No integrity/encryption** → traffic can be sniffed, spoofed, and replayed.
- **No authorization** → a "read" client and a "stop the motor" client look identical to the device.

## The protocols at a glance

| Protocol | Port | Transport | Domain | Built-in security | Secure variant |
|---|---|---|---|---|---|
| **Modbus/TCP** | 502 | TCP | Generic industrial | **None** | Modbus/TLS (rare) |
| **DNP3** | 20000 | TCP/UDP | Electric & water utilities | **None** | DNP3 Secure Authentication (SAv5) |
| **S7comm / S7comm-plus** | 102 | TCP (COTP/TPKT) | Siemens S7 PLCs | Weak (plus adds anti-replay) | — |
| **EtherNet/IP (CIP)** | 44818 / 2222 | TCP / UDP | Rockwell / Allen-Bradley | **None** | CIP Security |
| **PROFINET** | — (L2, DCP) | Ethernet L2 | Factory automation (Siemens/PI) | **None** | PROFINET Security |
| **BACnet** | 47808 | UDP | Building automation | **None** | BACnet/SC (Secure Connect) |
| **OPC UA** | 4840 | TCP | Modern interop | **Yes** (authn, signing, encryption) | native |
| **MQTT** | 1883 / 8883 | TCP | IoT messaging (pub/sub) | None / TLS | MQTT over TLS (8883) |
| **CoAP** | 5683 / 5684 | UDP | Constrained IoT (REST) | None / DTLS | CoAP over DTLS (5684) |

## Deep dives

### Modbus — the "hello world" of ICS insecurity
The simplest and most widespread. A client (master) sends a **function code** + data to a server (slave). There is no session, no login, no checksum-as-security.

Key function codes (the read/write danger):

| FC | Operation | Risk |
|---|---|---|
| 1 / 2 | Read coils / discrete inputs | Recon |
| **3** / 4 | Read holding / input registers | Recon — read process state |
| **5** | Write single coil | **Control** — flip an output |
| **6** | Write single register | **Control** — change a setpoint |
| **15 / 16** | Write multiple coils / registers | **Control** — bulk change |

> **Detection lever:** on a normal segment, IT should never send Modbus **write** codes (5/6/15/16) to OT. A protocol-aware firewall or OT-IDS that alerts on unexpected writes is one of the highest-value OT detections. [FrostyGoop](03-threats.md) (2024) weaponized exactly this — Modbus/TCP over 502 to manipulate heating controllers.

You can watch all of this safely on the [OT lab](../labs/ot/README.md): FC3 read, then FC6 write, with no authentication step at all.

### DNP3 — utilities' workhorse
Distributed Network Protocol 3, dominant in North American **electric and water** SCADA. Richer than Modbus (time-stamped events, unsolicited responses) but historically **unauthenticated**. The standard defines **Secure Authentication (SAv5)** — challenge/response over the existing link — but adoption is low and it adds no confidentiality (still cleartext). [Industroyer](03-threats.md) spoke DNP3 (and IEC 60870-5-101/104, IEC 61850) to trip breakers.

### S7comm — Siemens PLCs
The protocol Siemens S7-300/400 PLCs use (over ISO-on-TCP, port 102). Original S7comm had **no real authentication**; **Stuxnet** rode it to reprogram PLCs. Newer **S7comm-plus** (S7-1200/1500) added anti-replay/integrity, but researchers have repeatedly bypassed it — treat it as *obfuscation*, not security.

### EtherNet/IP & CIP — Rockwell/Allen-Bradley
EtherNet/IP carries the **Common Industrial Protocol (CIP)** — explicit messaging on TCP **44818**, implicit real-time I/O on UDP **2222**. No native security; **CIP Security** (TLS/DTLS + identity) is the ODVA add-on, still sparsely deployed. [PIPEDREAM](03-threats.md) targeted CIP-speaking devices.

### PROFINET — factory automation
Siemens/PI's real-time Ethernet protocol. Discovery/config uses **DCP** (Discovery and Configuration Protocol) at **layer 2** — so it's not "port-scannable" like TCP; you enumerate it on the local segment. Unauthenticated by default; **PROFINET Security** is the emerging hardening.

### BACnet — building automation
Runs buildings: HVAC, lighting, access, elevators (UDP **47808**). Devices announce themselves (Who-Is/I-Am) with no auth. **BACnet/SC (Secure Connect)** adds TLS-based security over WebSockets — the modern fix.

### OPC UA — the one built right
The modern, vendor-neutral interoperability standard — and the **security-capable** one: user/application authentication, message signing, and encryption, with certificate-based trust. The catch: it ships with a **"None" security mode** that many integrators leave on for convenience. *OPC UA done right is secure; OPC UA in "None" mode is just another cleartext protocol.*

### MQTT & CoAP — the IoT edge
Not ICS proper, but the **IoT** side of Module 18 and increasingly present in OT via IIoT sensors:
- **MQTT** — lightweight **publish/subscribe** over TCP via a broker. Frequently **anonymous**: subscribe to `#` (wildcard) to read everything, publish to inject anything. Secure form is **TLS on 8883** + broker auth.
- **CoAP** — HTTP-like **request/response** over **UDP** for constrained devices; secured with **DTLS** on 5684.

> **Exam/interview trap:** MQTT = **pub/sub over TCP**; CoAP = **REST over UDP**. One wrong word flips the answer.

## Attacking OT protocols (patterns, not exploits)
1. **Enumerate** — passively (span port, Shodan/Censys *index*) or, only on gear you own, active NSE (`modbus-discover`, `s7-info`, `enip-info`, `bacnet-info`) — see the [nmap cheatsheet](../cheatsheets/nmap.md).
2. **Read** — pull registers/points to understand the process (FC3, DNP3 reads).
3. **Replay / spoof** — capture a legitimate command and resend it; forge sensor values.
4. **Unauthorized command** — the payoff: a write that opens a valve, trips a breaker, or changes a setpoint.
5. **DoS** — many controllers fall over under malformed or high-rate traffic (a scan can be a DoS).

## Defending OT protocols
- **Segment** so the protocol is only reachable from where it must be ([Purdue](01-foundations.md), [IEC 62443 conduits](04-defense.md)).
- **Read-only where possible**; a protocol-aware firewall/DPI that **denies write function codes from IT**.
- **Prefer secure variants** (OPC UA with security *on*, DNP3-SA, CIP Security, BACnet/SC) when the gear supports them.
- **Monitor** with passive OT network detection — unexpected writes, new masters, engineering-mode changes ([04](04-defense.md)).
- **Broker every human/vendor path** through a jump host; vault the device credentials ([05](05-pam-for-ot.md)).

## ✅ Checkpoint
- Name the port and one-line purpose of Modbus, DNP3, S7comm, EtherNet/IP, BACnet, and OPC UA.
- Explain, by Modbus function code, the difference between a recon read and a control write — and which one IT should never send to OT.
- Say which of these protocols is security-capable and what commonly undermines it in practice.

## Sources
- Modbus specifications — https://modbus.org/specs.php
- DNP3 (DNP Users Group) — https://www.dnp.org/
- ODVA — EtherNet/IP & CIP Security — https://www.odva.org/technology-standards/distinct-cip-services/cip-security/
- PROFINET (PI) — https://www.profibus.com/technology/profinet
- BACnet / BACnet Secure Connect (ASHRAE) — http://www.bacnet.org/
- OPC UA security (OPC Foundation) — https://opcfoundation.org/about/opc-technologies/opc-ua/
- MITRE ATT&CK for ICS — https://attack.mitre.org/matrices/ics/
- Nmap ICS NSE (`modbus-discover`) — https://nmap.org/nsedoc/scripts/modbus-discover.html

---
Next: [03 — Threats & incidents](03-threats.md) →
