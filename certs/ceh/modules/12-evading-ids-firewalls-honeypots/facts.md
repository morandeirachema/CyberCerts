# Module 12 — Evading IDS, Firewalls & Honeypots · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## IDS vs IPS — the one-line split
**IDS = detect + alert (out of band).** **IPS = detect + block, inline in the path.** An IDS watches a copy of the traffic (tap/SPAN) and can only raise an alert; an IPS sits *in* the flow and can drop, reset, or rewrite. Same detection engine, different placement and authority.

## NIDS vs HIDS
| Sensor | Scope | Sees | Blocks? |
|---|---|---|---|
| **NIDS** | Network segment | Packets on the wire (needs tap/SPAN) | No (alert only) |
| **HIDS** | Single host | Local logs, file integrity (FIM), syscalls | No (alert only) |
| **IPS** | Inline | Same view as NIDS, but in the path | **Yes** (drop / reset) |

- NIDS is **blind to encrypted payloads** (it only sees ciphertext) and to what never crosses its segment.
- HIDS sees *inside* the host (log tampering, FIM changes) but nothing off-box.

## Detection methods (classic exam table)
| Method | How it decides | Strength | Weakness |
|---|---|---|---|
| **Signature / misuse** | Match known-bad patterns | Low false positives on known attacks | Blind to 0-day / novel; encryption defeats it |
| **Anomaly / behavior** | Deviation from a learned baseline | Can catch unknown attacks | Noisy; false positives; needs a training baseline |
| **Stateful protocol analysis** | Compare traffic to RFC/protocol state | Catches protocol abuse | Vendor-defined, heavy |

Alert outcomes: **true positive** (real attack flagged), **false positive** (benign flagged — noise), **false negative** (real attack *missed* — the dangerous one), **true negative** (benign, quiet). Anomaly systems trade **more false positives** for the chance to catch unknowns.

## Insertion vs Evasion vs DoS (Ptacek & Newsham)
| Attack on the IDS | Who accepts the packet? | Idea |
|---|---|---|
| **Insertion** | **IDS accepts**, end host **rejects** | Pad the IDS's view with packets the target drops → signature never matches on the IDS |
| **Evasion** | **End host accepts**, IDS **rejects/misses** | Attack reaches the target but never enters IDS reassembly |
| **DoS** | — | Exhaust, blind, or fail-open the IDS (flood, resource starvation) |

Anchor on **"who accepted the packet."** Host rejected but IDS kept it = insertion; host kept it but IDS missed it = evasion.

## Firewall types by OSI layer
| Type | OSI layer | Decides on | Notes |
|---|---|---|---|
| **Packet filter** | 3–4 | IP, port, protocol, flags | Stateless ACLs; no session memory |
| **Stateful inspection** | 3–4 (+state) | Connection state table | Allows return traffic of established flows |
| **Circuit-level gateway** | 5 | TCP handshake / session | SOCKS-style; validates sessions, not payload |
| **Application / proxy** | 7 | Full payload, per-protocol | Terminates & re-originates; deep but slow |
| **NGFW** | 3–7 | App-ID, users, IPS, TLS inspection | DPI + IPS + app awareness combined |

- **DMZ / screened subnet** — a buffer zone for internet-facing services, sandwiched between an outer and inner firewall so a compromise there doesn't reach the internal LAN.
- **Bastion host** — a hardened, exposed host (jump/proxy) built to withstand attack; minimal services, heavy logging.
- **Default-deny** — allow only what is explicitly permitted; the correct posture for both ingress and egress.

## nmap evasion flags — match by symptom
| Flag | Effect | CEH tell |
|---|---|---|
| `-f` / `-ff` | Fragment packets (`-f` ≈ 8-byte, `-ff` ≈ 16-byte) | Break payload across fragments |
| `--mtu <n>` | Custom fragment size — **must be a multiple of 8** | Manual fragmentation |
| `-D <ip1,ME,ip2>` / `-D RND:5` | **Decoys** — spray spoofed source IPs so the real one hides | Many "scanners" at once, one real |
| `-S <ip>` | **Spoof source** address | Different from decoys |
| `-g` / `--source-port <p>` | Spoof source **port** (e.g. 53/80/443) to pass sloppy ACLs | "From port 53" trust bypass |
| `--data-length <n>` | Append `n` random bytes to each packet | Break length-based signatures |
| `--badsum` | Send a **bad TCP/UDP checksum** | Insertion + firewall/IDS fingerprint; host drops it |
| `--spoof-mac <0/vendor/MAC>` | Spoof source MAC (`0` = random) | Layer-2 origin hiding |
| `-T0..T5` | Timing template — `-T0` paranoid / `-T1` sneaky … `-T5` insane | Slow scans dodge rate-based alerts |
| `--scan-delay <t>` | Force a gap between probes | Same goal as low `-T` |

## Tunneling — carry the attack inside an allowed channel
- **HTTP(S) tunneling** — wrap traffic in web requests through a permissive proxy/port 80/443.
- **DNS tunneling** — encode data in long, high-entropy TXT/`A` queries to an attacker domain (**iodine**, **dnscat2**).
- **ICMP tunneling** — hide payload in echo-request/reply data (**Loki**, **ptunnel**).
- Encryption/tunneling **defeats signature IDS** (it can't read the payload) but still leaves a **behavioral shape** — volume, entropy, beaconing — that anomaly/flow analysis and egress filtering can catch.

## Honeypots
| Axis | Options |
|---|---|
| Interaction | **Low** (emulated services — honeyd, Dionaea) · **Medium** · **High** (real OS/services — honeynet, richer data, more risk) |
| Purpose | **Production** (early-warning inside your net) · **Research** (study attacker TTPs) |
| Special | **Tarpit** (LaBrea — slows scanners), **pure** honeypot (full real system) |

- **Low-interaction = emulated** (safer, less data). **High-interaction = real systems** (richer data, more risk of being used as a pivot).
- **Detecting a honeypot** (attacker's view): unrealistically open/consistent services, canned banners, abnormal latency/tarpit stalling, VM/sandbox artifacts, no real user activity.
- Names to know: **honeyd**, **T-Pot** (multi-honeypot platform), **Cowrie/Kippo** (SSH), **KFSensor**, **Dionaea**.

## Snort & Suricata
- **Snort** — signature NIDS/IPS; modes = **sniffer**, **packet logger**, **NIDS**. Console alert mode: `snort -A console -q -c snort.conf -i eth0`.
- **Suricata** — multi-threaded IDS/IPS, **Snort-rule compatible**, emits **EVE JSON** (`eve.json`); read alerts with `jq 'select(.event_type=="alert")'`.
- **Rule anatomy:** **header** = action · protocol · src IP/port · direction · dst IP/port; **options** = `msg`, `content`, `sid`, `rev`. Snort actions: `alert`, `log`, `pass`, and (inline) `drop` / `reject`.

## PAM angle (privileged lens)
- Network IDS is evaded by **blending into traffic** — but privileged **behavior** is much harder to fake. **PTA (Privileged Threat Analytics)** is the behavioral/UEBA layer for the *identity* plane; it pattern-matches Golden Ticket / DCSync / PtH activity that signature network IDS cannot see.
- Evasion techniques lean on **log tampering / anti-forensics**. The **Digital Vault audit is tamper-evident and append-only**, so an attacker who blinds the network sensor still leaves an intact privileged audit trail.
- **Blinding a sensor is itself an attack:** run HIDS/EDR on every jump/bastion host and **alert when a log source goes silent**.
- **Default-deny egress** on the admin plane stops a foothold from tunneling out over DNS/HTTP/ICMP.
- **Deception around Tier 0** — a fake privileged share, service account, or admin host is the cheapest high-fidelity tripwire; any interaction with it is malicious by definition.

## Top traps
- **IDS detects, IPS blocks.** HIDS/NIDS are *detection* only; only **IPS** sits inline and drops.
- **Insertion vs evasion** flips easily — anchor on **who accepted the packet** (IDS-accepted = insertion; host-accepted = evasion).
- **False negative** is the dangerous miss (real attack, no alert); false positive is just noise.
- Flag→purpose: **`-D` = decoys**, **`-S` = spoofed source**, **`-g`/`--source-port` = source-port spoofing**, **`-f` = fragmentation**. Don't swap them.
- **`--mtu` must be a multiple of 8** (`-f` ≈ 8, `-ff` ≈ 16).
- **Encryption defeats signature IDS, not anomaly/flow analysis** — the behavioral tail still shows.
- **Low-interaction = emulated services; high-interaction = real systems.**
- **Proxy/application firewall = Layer 7; packet filter = Layer 3–4.** Match by layer.
- `--badsum` is dropped by the **end host**, so the target reports nothing — that gap is the **insertion** concept.
