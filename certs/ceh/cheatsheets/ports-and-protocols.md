# Ports & Protocols Cheatsheet

Memorize these — CEH tests port↔service recognition directly, and enumeration questions hinge on knowing what runs where. Column "Module" points to where it's attacked in this repo.

## Most-tested well-known ports

| Port | Proto | Service | Notes / attack angle | Module |
|---|---|---|---|---|
| 20/21 | TCP | FTP | Cleartext creds; anonymous login | 02, 08 |
| 22 | TCP | SSH | Brute force; key auth | 06 |
| 23 | TCP | Telnet | Cleartext — sniffable | 08 |
| 25 | TCP | SMTP | User enum (VRFY/EXPN); relay | 04 |
| 53 | TCP/UDP | DNS | Zone transfer (AXFR) on TCP; enum | 02, 04 |
| 67/68 | UDP | DHCP | Starvation, rogue DHCP | 08 |
| 69 | UDP | TFTP | No auth; config theft | 04 |
| 80 | TCP | HTTP | Web attacks; cleartext | 13, 14 |
| 88 | TCP/UDP | Kerberos | Kerberoasting, AS-REP roast | 06 |
| 110 | TCP | POP3 | Cleartext mail | 08 |
| 111 | TCP/UDP | RPC/portmapper | NFS/rpc enum | 04 |
| 123 | UDP | NTP | Amplification/reflection DoS | 10 |
| 135 | TCP | MSRPC | Windows RPC enum | 04 |
| 137/138 | UDP | NetBIOS name/datagram | NetBIOS enum | 04 |
| 139 | TCP | NetBIOS session (SMB over NetBIOS) | Null sessions | 04 |
| 143 | TCP | IMAP | Cleartext mail | 08 |
| 161/162 | UDP | SNMP | Default communities public/private | 04 |
| 389 | TCP/UDP | LDAP | Directory enum | 04 |
| 443 | TCP | HTTPS | TLS web; still app-attackable | 14, 20 |
| 445 | TCP | SMB (direct) | Shares, PtH, EternalBlue-class | 04, 06 |
| 464 | TCP/UDP | kpasswd | Kerberos password change | 06 |
| 500 | UDP | IKE/IPsec | VPN enum | 03 |
| 514 | UDP | Syslog | Log tampering target | 06 |
| 587 | TCP | SMTP submission | Auth mail | 04 |
| 636 | TCP | LDAPS | LDAP over TLS | 04 |
| 993/995 | TCP | IMAPS/POP3S | TLS mail | 08 |
| 1433 | TCP | MSSQL | DB attacks; svc accounts | 15 |
| 1521 | TCP | Oracle DB | DB attacks | 15 |
| 1723 | TCP | PPTP VPN | Weak VPN | 03 |
| 2049 | TCP/UDP | NFS | `showmount`, exports | 04 |
| 3268/3269 | TCP | AD Global Catalog / over TLS | Forest-wide LDAP | 04 |
| 3306 | TCP | MySQL/MariaDB | DB attacks | 15 |
| 3389 | TCP | RDP | Brute force; BlueKeep-class | 06 |
| 5432 | TCP | PostgreSQL | DB attacks | 15 |
| 5900 | TCP | VNC | Weak/no auth remote | 06 |
| 5985/5986 | TCP | WinRM / over TLS | Remote PowerShell, PtH | 06 |
| 6379 | TCP | Redis | Often unauth | 04 |
| 8080/8443 | TCP | HTTP/HTTPS alt | Proxies, app servers | 13, 14 |
| 27017 | TCP | MongoDB | Often unauth | 04 |

## ICS / OT & IoT protocol ports (Module 18)

Most of these have **no authentication or encryption by design** — the control is segmentation, not the protocol. Practice them locally with [`../labs/ot/`](../labs/ot/).

| Port | Proto | Service | Notes / attack angle | Module |
|---|---|---|---|---|
| 102 | TCP | S7comm (Siemens S7) | PLC comms; no auth | 18 |
| 502 | TCP | Modbus/TCP | Read (FC3) + **write** (FC6/16) registers, no auth | 18 |
| 1883 | TCP | MQTT | IoT pub/sub broker, frequently anonymous | 18 |
| 2222 | UDP | EtherNet/IP (implicit I/O) | Rockwell/Allen-Bradley CIP | 18 |
| 4840 | TCP | OPC UA | Modern, secure-*capable* interop | 18 |
| 5683 | UDP | CoAP | RESTful IoT over UDP (DTLS **5684**) | 18 |
| 8883 | TCP | MQTT over TLS | The secured form of 1883 | 18 |
| 20000 | TCP/UDP | DNP3 | Electric/water utilities | 18 |
| 44818 | TCP | EtherNet/IP (explicit) | Rockwell/Allen-Bradley CIP | 18 |
| 47808 | UDP | BACnet | Building automation | 18 |

> **Traps:** MQTT is **pub/sub over TCP**; CoAP is **REST over UDP** — one wrong word (TCP↔UDP, pub/sub↔request/response) flips the answer. Modbus/DNP3/S7comm assume a **trusted network** — no identity, no crypto.

## Handshakes & flags (memorize)

- **TCP three-way handshake:** `SYN → SYN/ACK → ACK`. Teardown: `FIN/ACK`.
- **TCP flags:** SYN, ACK, FIN, RST, PSH, URG (mnemonic: *Unskilled Attackers Pester Real Security Folks* → URG ACK PSH RST SYN FIN).
- **nmap scan → flags sent:**
  - SYN (`-sS`): SYN; open=SYN/ACK, closed=RST.
  - Connect (`-sT`): full handshake.
  - NULL (`-sN`): no flags. FIN (`-sF`): FIN. Xmas (`-sX`): FIN+PSH+URG. (open|filtered = no reply; closed = RST — only reliable on non-Windows stacks.)
  - ACK (`-sA`): maps firewall rules (stateful vs stateless), not open/closed.

## ICMP types worth knowing

| Type | Meaning |
|---|---|
| 0 / 8 | Echo reply / request (ping) |
| 3 | Destination unreachable (codes: 0 net, 1 host, 3 port) |
| 5 | Redirect |
| 11 | Time exceeded (traceroute) |
