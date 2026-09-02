# Cheatsheets

Quick-reference material to keep open **during** a lab or the [Practical](../practical/README.md), and to drill in the final weeks. The exam and the labs both reward fast recall of ports, flags, and tool→purpose pairs.

### Knowledge-exam recall
| Sheet | Use it for |
|---|---|
| [ports-and-protocols.md](ports-and-protocols.md) | Well-known ports + which module attacks them |
| [nmap.md](nmap.md) | Scan types, flags, NSE, timing, evasion |
| [metasploit.md](metasploit.md) | msfconsole workflow, Meterpreter, msfvenom |
| [hashcat-john.md](hashcat-john.md) | Hash modes, cracking workflow |
| [one-liners.md](one-liners.md) | Handy enumeration / exploitation one-liners |

### Hands-on / Practical (keep these open while you work)
| Sheet | Use it for |
|---|---|
| [reverse-shells.md](reverse-shells.md) | Get a shell, catch it, upgrade to a full TTY; msfvenom payloads |
| [active-directory.md](active-directory.md) | Kerberoast, PtH, RBCD, ADCS, DCSync — Impacket/NetExec/Certipy |
| [web-sqli.md](web-sqli.md) | Burp/ffuf/sqlmap + XSS/LFI/SQLi payloads |
| [privilege-escalation.md](privilege-escalation.md) | Linux (SUID/sudo/GTFOBins) + Windows (tokens/potato) |
| [wireshark-tcpdump.md](wireshark-tcpdump.md) | Capture + display filters + extract creds/files from a pcap |
| [steg-forensics.md](steg-forensics.md) | Steganography, archive cracking, decode/decrypt |

> Confirm every flag against the tool's own `--help`/man page — versions change. Deeper technique: [`../resources/deep-references.md`](../resources/deep-references.md).
