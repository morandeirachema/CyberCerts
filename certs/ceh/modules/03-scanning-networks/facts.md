# Module 03 — Scanning Networks · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The TCP three-way handshake
**SYN → SYN/ACK → ACK.** The attacker sends SYN; an **open** port answers **SYN/ACK**; the attacker completes with ACK. A **SYN (half-open) scan stops after SYN/ACK** and sends RST instead of the final ACK — so the connection never fully forms.
- TCP flags to know: **SYN, ACK, FIN, RST, PSH, URG** (and the odd ones ECE/CWR).
- The response triangle: **open → SYN/ACK · closed → RST · filtered → silence / ICMP unreachable.** Memorize it.

## Port states (Nmap verdicts)
| State | Meaning |
|---|---|
| open | A service is actively accepting connections |
| closed | Host reachable, nothing listening on that port |
| filtered | A firewall/filter dropped the probe — no verdict possible |
| open\|filtered | No reply — can't distinguish (Xmas/FIN/NULL/UDP) |
| unfiltered | Reachable, state unknown (ACK scan only) |

## Scan-type matrix (the core exam table)
| Scan | Flag | Packet sent | Open port | Closed port | Notes |
|---|---|---|---|---|---|
| TCP connect | `-sT` | Full handshake | SYN/ACK, completes | RST | No root; noisy, logs a full connection |
| SYN / half-open | `-sS` | SYN only | SYN/ACK (then RST) | RST | **Default**; needs root; stealthier |
| UDP | `-sU` | UDP datagram | app reply / no ICMP | ICMP port unreachable | Slow; needs root |
| FIN | `-sF` | FIN only | **no reply = open\|filtered** | RST | RFC-793 logic |
| NULL | `-sN` | no flags set | **no reply = open\|filtered** | RST | RFC-793 logic |
| Xmas | `-sX` | FIN+PSH+URG | **no reply = open\|filtered** | RST | RFC-793 logic |
| ACK | `-sA` | ACK only | RST = unfiltered | RST = unfiltered | Maps **firewall**, not open ports |
| Idle / zombie | `-sI` | Spoofed via 3rd host | inferred from IPID | inferred from IPID | Fully blind/spoofed source |

> **Key gotcha:** Xmas/FIN/NULL rely on RFC 793. **Windows (and many devices) reply RST to everything**, so these scans report *all* ports `closed` on Windows — they only give useful `open|filtered` results against stack-compliant (usually *nix) targets.

## How each scan reads "open" vs "closed"
- **Connect / SYN:** open = **SYN/ACK**, closed = **RST**. (SYN just doesn't finish the handshake.)
- **FIN / NULL / Xmas:** open (or filtered) = **no reply**; closed = **RST**. So *silence* is the "maybe open" signal here — the inverse of a connect scan.
- **ACK:** never finds open ports — a returned **RST = unfiltered**, silence/ICMP = **filtered**. It's a firewall-rule mapper.
- **UDP:** no reply = **open|filtered**; **ICMP type 3 code 3 (port unreachable) = closed**; app-layer reply = open.

## Host discovery vs port scan vs detection (CEH keeps these distinct)
- **`-sn`** = ping sweep / host discovery **only, no port scan** ("which hosts are up").
- **`-sn -PR`** = **ARP** ping — fastest and most reliable **on the local LAN** (ARP can't be firewalled on-segment).
- **`-Pn`** = **skip discovery**, treat host as up (use when ICMP is blocked). Do **not** confuse `-Pn` (no discovery) with `-sn` (discovery only).
- Other probes: `-PS` (SYN ping), `-PA` (ACK ping), `-PE` (ICMP echo), `-PU` (UDP ping).

## Fingerprinting
- **Banner grabbing** = active fingerprinting: read the service banner. `nc -nv <ip> <port>` or `nmap -sV --script=banner`.
- **`-sV`** = service/version detection (probes the app to name the software + version).
- **`-O`** = OS detection via TCP/IP stack fingerprinting (TTL, window size, TCP options).
- **`-A`** = aggressive = `-sV -O -sC` + traceroute. **`-sC`** = default NSE scripts (`--script=default`).

## IDS / firewall evasion flags
| Flag | Technique | Effect |
|---|---|---|
| `-f` (or `--mtu`) | Fragmentation | Splits probes into tiny IP fragments to slip past simple packet inspection |
| `-D d1,d2,ME` | Decoys | Spoofs extra source IPs so your real IP hides in the noise |
| `-g` / `--source-port` | Source-port spoof | Send from a trusted port (e.g. **53/DNS**, 80) to bypass sloppy filters |
| `-S` + `-e` | Spoof source address | Forge the source IP (needs to sniff replies elsewhere) |
| `--data-length <n>` | Pad payload | Adds random bytes so probe size doesn't match known scanner signatures |
| `--badsum` | Bad TCP/UDP checksum | Well-behaved stacks drop it; a reply reveals a firewall/IPS answering |
| `-T0..T5` | Timing template | Slow scans (`-T0/-T1`) evade rate-based IDS; fast (`-T4/-T5`) is loud |
| `--randomize-hosts`, `--spoof-mac`, `--ttl` | Misc obfuscation | Reorder targets, forge MAC, set TTL |

## Timing templates
| Template | Name | Use |
|---|---|---|
| `-T0` | paranoid | Serial, very slow — max IDS evasion |
| `-T1` | sneaky | Slow, low footprint |
| `-T2` | polite | Reduced bandwidth |
| `-T3` | normal | Default |
| `-T4` | aggressive | Fast — good on a LAN/lab |
| `-T5` | insane | Fastest, may lose accuracy |

## Other tools
- **hping3** — hand-crafts single packets with full flag control: `-S` SYN, `-A` ACK, `-F` FIN, `-8` scan mode. Great for firewall testing and one-off probes.
- **masscan** — asynchronous, internet-scale port scanner; **must** be rate-limited (`--rate`); Nmap-like syntax but far faster and blunter.
- **Zenmap** — Nmap GUI + topology view. **netcat (`nc`)** — manual banner grabbing / raw connections.

## The one-line PAM answer key
- Scan finds open admin ports (RDP/SSH/WinRM) → **close direct admin ingress; broker every session through PSM/PSMP** so there's nothing to connect to directly.
- Scan discovers the PAM stack (PVWA/Vault) → **harden + segment the Tier 0 control plane**.
- Recon staged before lateral movement → **JIT access (DPA)** so there's no standing session to reach.
- Cross-tier port-scan pattern → **alert (IDS + PTA)**; a Tier 2 host scanning Tier 0 management ports is never normal.
- Durable posture: **segmentation** (a scan from a low tier shouldn't even reach Tier 0 ports) + **least exposure** (fewer open ports = smaller map).

## Top traps
- **`-sn` ≠ `-Pn`.** `-sn` = discovery only (no ports); `-Pn` = no discovery (skip ping, scan ports anyway).
- **`-sS` needs root; `-sT` does not** — but `-sT` completes the handshake and gets logged. "Stealth" = SYN.
- **Xmas/FIN/NULL report everything `closed` on Windows** because Windows RSTs regardless of RFC 793. Favorite trick question.
- **No reply means `open|filtered`** for Xmas/FIN/NULL/UDP — **not** "closed". A **RST means closed**.
- **ACK scan maps the firewall** (filtered vs unfiltered) — it can *never* tell you a port is open.
- **UDP closed = ICMP port unreachable**; UDP silence = open|filtered. UDP scanning is slow.
- **Idle/zombie (`-sI`)** = fully spoofed source, inferred via the zombie's **IPID** — needs a host with predictable/incremental IPID.
- `--source-port 53` and `-g 53` are the same idea: masquerade as DNS to slip past trust-by-port filters.
