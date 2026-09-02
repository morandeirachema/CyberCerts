# Nmap Cheatsheet

Nmap is the single most exam-relevant tool. Know the scan types, what packets they send, and the evasion flags. Official reference manual: https://nmap.org/book/man.html

> Run only against your lab: `192.168.56.0/24`, Metasploitable2 `192.168.56.20`.

## Host discovery

```bash
nmap -sn 192.168.56.0/24          # ping sweep (no port scan) — "which hosts are up"
nmap -Pn 192.168.56.20            # skip discovery, treat as up (through firewalls)
nmap -PR 192.168.56.0/24          # ARP scan (fast on local LAN)
nmap -n 192.168.56.20             # no DNS resolution (faster/quieter)
```

## Scan types (know the packets)

| Flag | Scan | Packet / behavior | Needs root? |
|---|---|---|---|
| `-sS` | SYN / "half-open" | SYN; open→SYN/ACK, closed→RST | Yes |
| `-sT` | TCP connect | full 3-way handshake | No |
| `-sU` | UDP | UDP; slow, ICMP port-unreachable = closed | Yes |
| `-sN` | NULL | no flags set | Yes |
| `-sF` | FIN | FIN flag | Yes |
| `-sX` | Xmas | FIN+PSH+URG | Yes |
| `-sA` | ACK | maps firewall rules (filtered vs unfiltered) | Yes |
| `-sI` | Idle/zombie | spoofs via a zombie host (stealth) | Yes |

> NULL/FIN/Xmas rely on RFC 793 behavior — reliable on many *nix stacks, **not** on Windows (which replies RST to everything → shows "closed").

## Service / OS / scripts

```bash
nmap -sV 192.168.56.20            # version detection
nmap -O 192.168.56.20             # OS fingerprint
nmap -A 192.168.56.20             # aggressive: -sV -O + scripts + traceroute
nmap -p- 192.168.56.20            # all 65535 TCP ports
nmap -p 1-1000 --top-ports 100 192.168.56.20
nmap -sC 192.168.56.20            # default NSE scripts (= --script=default)
nmap --script vuln 192.168.56.20  # vuln NSE category
nmap --script smb-enum-shares,smb-os-discovery -p445 192.168.56.20
```

NSE categories: `auth, broadcast, brute, default, discovery, dos, exploit, external, fuzzer, intrusive, malware, safe, version, vuln`. Scripts live in `/usr/share/nmap/scripts/`.

## OT / ICS discovery (Module 18)

```bash
nmap -sV -p 502   --script modbus-discover 127.0.0.1   # Modbus unit IDs / device info
nmap -sV -p 102   --script s7-info         127.0.0.1   # Siemens S7 PLC
nmap -sV -p 44818 --script enip-info       127.0.0.1   # EtherNet/IP (Rockwell)
nmap -sU -p 47808 --script bacnet-info     127.0.0.1   # BACnet (UDP, building automation)
nmap -sV -p 1883  --script mqtt-subscribe  127.0.0.1   # MQTT topics (anonymous)
```

> ⛔ **Only against simulators / devices you own.** A scan that's routine on IT can crash a fragile PLC. On a real assessment, prefer **passive** discovery (span port, Shodan/Censys *index*) and never `-T4`/`-A` an OT segment. Practice these on [`../labs/ot/`](../labs/ot/README.md).

## Timing & performance

```bash
nmap -T0 ... -T5    # paranoid(0) → insane(5); -T4 common for labs
nmap --min-rate 1000 --max-retries 1 192.168.56.20
```

## Firewall / IDS evasion (Module 12)

```bash
nmap -f 192.168.56.20                 # fragment packets
nmap --mtu 16 192.168.56.20           # custom MTU (multiple of 8)
nmap -D RND:10 192.168.56.20          # decoys (hide real source among fakes)
nmap -S <spoofed_ip> ...              # spoof source IP
nmap --source-port 53 192.168.56.20   # come from a "trusted" port
nmap --data-length 25 192.168.56.20   # pad packets
nmap --scan-delay 1s 192.168.56.20    # slow down to dodge thresholds
nmap --spoof-mac 0 192.168.56.20      # random MAC
```

## Output (keep evidence)

```bash
nmap -oN scan.txt 192.168.56.20       # normal
nmap -oG scan.grep 192.168.56.20      # greppable
nmap -oX scan.xml 192.168.56.20       # XML (feeds other tools)
nmap -oA scan 192.168.56.20           # all three at once
```

## Fast recall

- "Half-open / stealth" → **-sS**. "Doesn't need root" → **-sT**.
- "Map the firewall ruleset" → **-sA**. "Most stealthy, uses a third host" → **-sI** (idle).
- "-A" is loud (version+OS+scripts+traceroute) — never the answer to a *stealth* question.
