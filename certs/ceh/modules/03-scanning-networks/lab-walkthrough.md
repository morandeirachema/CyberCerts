# Module 03 — Scanning Networks · Guided Lab Walkthrough

> Scan **only your own lab** (`192.168.56.0/24` — see [`../../labs/topology.md`](../../labs/topology.md)). Each step: command, expected observation, a hint, and the defender/PAM takeaway. Outputs are **representative**. Pairs with [README.md](README.md) · [facts.md](facts.md).

**Goal:** map a target end-to-end — discover it, enumerate ports with different scan types, read the responses, fingerprint services/OS, and try one evasion.

**Target:** Metasploitable2 `192.168.56.20` (Linux — flag scans behave textbook here).

---

## Part A — Host discovery
```bash
sudo nmap -sn 192.168.56.0/24            # ping sweep: who's up
sudo nmap -sn -PR 192.168.56.0/24        # ARP-only (fast/reliable on local LAN)
```
**You should see** the lab hosts listed as `Host is up`. **Observe:** `-PR` (ARP) is the most reliable on a LAN because ARP can't be firewalled off-subnet.

---

## Part B — Core scan types and their responses
```bash
nmap -sT 192.168.56.20                   # connect scan (no root)
sudo nmap -sS 192.168.56.20              # SYN / half-open (default)
sudo nmap -sU --top-ports 25 192.168.56.20   # UDP (slow — keep it bounded)
```
**You should see** open TCP ports like `21/ftp, 22/ssh, 80/http, 139/445 smb, 3306/mysql`. **Observe:** `-sT` and `-sS` return the same open set here, but `-sS` never completes the handshake (fewer app logs). UDP is slow and shows `open|filtered` for silent services.

<details><summary>Hint</summary>Bound UDP with `--top-ports` or `-p` — a full UDP scan can take ages due to ICMP rate-limiting.</details>

## Part C — Flag scans (read the responses)
```bash
sudo nmap -sX 192.168.56.20              # XMAS
sudo nmap -sF 192.168.56.20              # FIN
sudo nmap -sN 192.168.56.20              # NULL
sudo nmap -sA 192.168.56.20              # ACK (firewall mapping)
```
**You should see** open ports report `open|filtered` (no response) and closed ports report `closed` (RST) — the RFC-793 behavior. **Observe:** run the same `-sX` against a Windows lab host and it reports everything `closed` — Windows RSTs regardless, the classic caveat.

## Part D — Fingerprint services and OS
```bash
sudo nmap -sV -O 192.168.56.20           # version + OS
nmap -sC 192.168.56.20                   # default NSE scripts
nmap --script smb-os-discovery -p445 192.168.56.20
```
**You should see** concrete versions (e.g., `vsftpd 2.3.4`, `OpenSSH 4.7p1`) and an OS guess — the raw material for the next module's exploit selection.

## Part E — One evasion technique
```bash
sudo nmap -sS -f 192.168.56.20           # fragment packets
sudo nmap -sS -D 192.168.56.15,ME 192.168.56.20   # decoys
```
**Observe:** same results, but the probes are fragmented / mixed with decoys — harder for a signature IDS to attribute. Compare with the IDS view in Module 12.

**Defender/PAM view:** scanning is how an attacker finds your admin ingress. Close direct admin ports and force sessions through a broker (Module 03 deep-dive → [PSM/PSMP](../../defender-pam/pam-architecture.md)); alert on sweeps near Tier 0.

## What you should conclude
| You did | Takeaway |
|---|---|
| `-sn`/`-PR` | Discover hosts before scanning ports |
| `-sT` vs `-sS` | Same result, different stealth/logging |
| Flag scans | Open = silent, closed = RST (not on Windows) |
| `-sV -O` | Versions drive exploit selection |
| `-f`/`-D` | Evasion changes attribution, not results |

## Cleanup
Nothing persistent created.

## Record it
Log the open-port set and any surprising fingerprint in the **My lab log** table in [README.md](README.md); track weak areas in [PROGRESS.md](../../PROGRESS.md).
