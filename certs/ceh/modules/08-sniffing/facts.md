# Module 08 — Sniffing · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## Passive vs. active sniffing
| Type | Where it works | Why |
|---|---|---|
| **Passive** | Hub, or a **SPAN port / network TAP** | The medium already copies every frame to you — you just listen |
| **Active** | **Switch** | The switch forwards unicast only to the destination port, so you must *inject* traffic to redirect frames to yourself |

Switches are why passive sniffing stopped being "enough" — the exam loves this pivot.

## Hub vs. switch and the CAM table
- A **hub** repeats every frame out every port → trivially sniffable (passive).
- A **switch** learns **MAC → port** mappings in its **CAM (content-addressable memory) / MAC address table** and forwards each unicast frame only to the port that owns the destination MAC.
- Defeating the switch = making it forward *your way* → the active-attack list below.

## Active sniffing attacks (the core list)
| Attack | Mechanism | Result |
|---|---|---|
| **MAC flooding** (`macof`) | Flood the switch with bogus source MACs until the CAM table overflows | Switch **fails open** → floods all ports **like a hub** |
| **MAC spoofing** | Clone a legitimate host's MAC | Bypass MAC/port filtering; hijack that port's traffic |
| **ARP poisoning** | Forge ARP replies mapping gateway IP → attacker MAC (and victim IP → attacker MAC) | **MITM** — victim traffic flows through you |
| **DHCP starvation** | Exhaust the DHCP pool with spoofed MAC requests | DoS; clears the way for a rogue DHCP server |
| **Rogue DHCP** | Attacker's DHCP server answers a request first | Pushes malicious **gateway/DNS** → MITM |
| **DNS poisoning** | Inject false DNS records/responses | Redirect victims to attacker hosts |

**MAC flooding fails the switch *open* — memorize "fail-open = behaves like a hub."** That is the entire point of the attack.

## ARP poisoning → MITM (the reason to memorize)
- **ARP has no authentication.** A host accepts an unsolicited ("gratuitous") ARP reply and updates its cache — no proof required.
- So a forged reply saying *"the gateway's IP is at my MAC"* silently reroutes the victim's traffic through the attacker.
- With **IP forwarding on**, the victim stays online and never notices → true man-in-the-middle.
- **Encryption is the safety net:** you can be MITM'd at L2 and still hand over only ciphertext if the session is TLS/SSH.

## DHCP attacks
- **DHCP starvation** = spoof many MACs, lease every address → pool exhausted (a DoS setup move).
- **Rogue DHCP** = attacker server races the real one; if it wins the DISCOVER→OFFER, it dictates the victim's **default gateway and DNS** → MITM.
- Counter: **DHCP snooping** — only *trusted* ports may send DHCP offers.

## DNS poisoning variants
| Variant | Where it happens |
|---|---|
| **Intranet** DNS spoofing | On the LAN (usually riding an ARP MITM) |
| **Internet** DNS spoofing | Attacker-controlled resolver on a rogue box |
| **Proxy-server** DNS poisoning | Malicious proxy set in browser settings |
| **DNS cache** poisoning | Forged records injected into a resolver's cache |

## Cleartext protocols to flag (know the secure swap)
| Insecure | Port | Encrypted replacement |
|---|---|---|
| Telnet | 23 | **SSH** (22) |
| FTP | 21 | **SFTP** (22) / **FTPS** (990) |
| HTTP | 80 | **HTTPS/TLS** (443) |
| SMTP / POP3 / IMAP | 25 / 110 / 143 | **+TLS** (587 or 465 / 995 / 993) |
| SNMPv1 / v2c | 161 | **SNMPv3** (auth + priv) |
| LDAP | 389 | **LDAPS** (636) |

- **SNMP community strings** ("public" / "private") ride in **cleartext** on v1/v2c; **SNMPv3** adds authentication + privacy.
- If you can read a credential in the packet bytes, the protocol was unencrypted — the fix is always "encrypt the transport," not "add a firewall rule."

## Wireshark — display vs. capture filters (do not confuse the syntax)
| | **Capture filter** | **Display filter** |
|---|---|---|
| When | *Before* capture (limits what's saved) | *After* capture (limits what's shown) |
| Syntax | **BPF** (libpcap) | Wireshark expression language |
| Example | `tcp port 80` / `host 192.168.56.20` | `http.request` / `ftp.request.command == "PASS"` |

- Display-filter greatest hits: `http.authbasic`, `ftp.request.command == "PASS"`, `telnet`, `tcp.port == 23`, `http.request.method == "POST"`.
- Capture filters use **BPF** (`tcp port 80`, `not arp`); the two grammars are *not* interchangeable.

## Responder → NetNTLMv2 → crack
- **Responder** poisons **LLMNR / NBT-NS** (and mDNS) name-resolution requests: when a Windows host fails DNS and broadcasts "who is `\\fileserv01`?", Responder answers *"me,"* and the victim authenticates to the attacker.
- The captured material is a **NetNTLMv2** challenge/response hash.
- Crack it offline with **`hashcat -m 5600`**.
- Kill the path: **disable LLMNR and NBT-NS**, enforce **SMB signing**, require MFA.

## Defenses — match the control to the attack
| Attack | Control |
|---|---|
| **MAC flooding** | **Port security** (limit MACs per port, sticky-MAC) |
| **ARP poisoning** | **Dynamic ARP Inspection (DAI)** + static ARP for gateways |
| **Rogue DHCP / starvation** | **DHCP snooping** (trusted ports only) + port security |
| **Responder (LLMNR/NBT-NS)** | Disable LLMNR/NBT-NS, SMB signing, MFA |
| **Cleartext sniffing** | Encrypt everything (SSH/TLS/SNMPv3) + broker privileged sessions |

The clean mapping to memorize: **port security → MAC flooding · DHCP snooping → rogue DHCP · DAI → ARP poisoning.**

## The legitimate way to sniff
A **SPAN port / port mirroring** or a **network TAP** feeds a copy of traffic to an IDS/analyzer. Know these as *sanctioned monitoring*, not attacks.

## PAM angle — sniffing's real prize is a privileged credential
- Admin sessions are the **juiciest** sniffing target, so **never let a privileged credential cross the network in a form the endpoint can read.**
- **Broker admin sessions through a PAM proxy (PSM/PSMP):** the target password is **injected server-side**, the session is **TLS-tunneled and recorded**, so a LAN sniffer or an ARP MITM captures only ciphertext — the credential is **never on the wire** on the admin's endpoint.
- Pair with: disable legacy cleartext protocols, enforce SMB signing, turn LLMNR/NBT-NS off → the **Responder → hash-crack** path dies too.

## Top traps
- **Passive sniffing needs a hub or SPAN/TAP; you need *active* sniffing on a switch.** Don't say passive works on a switch.
- **MAC flooding fails the switch *open*** (it acts like a hub) — that's the goal, not a side effect.
- **ARP poisoning works because ARP has no authentication** — the single most-tested "why."
- **Match the defense:** port security ↔ MAC flooding, DHCP snooping ↔ rogue DHCP, DAI ↔ ARP poisoning. Swapping these is the classic distractor.
- **Display filter (`http.request`) ≠ capture filter (`tcp port 80`, BPF)** — different grammars.
- **SNMPv1/2c community strings are cleartext**; SNMPv3 is the fix.
- Responder captures **NetNTLMv2**, cracked with **`hashcat -m 5600`** (not `-m 1000` NTLM, not `-m 13100` Kerberos).
- **SPAN port / TAP = legitimate**, not an attack.
