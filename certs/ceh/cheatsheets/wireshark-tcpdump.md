# Wireshark & tcpdump

Capture and read traffic; extract creds and files from a `.pcap`. Pairs with [Module 08](../modules/08-sniffing/README.md) and the [PCAP forensics drills](../practical/drills/06-pcap-forensics.md). **Own lab segment only.**

## tcpdump (CLI capture)
```bash
sudo tcpdump -D                                  # list interfaces
sudo tcpdump -i eth0 -w cap.pcap                 # capture to file
sudo tcpdump -i eth0 -nn -A 'tcp port 80'        # print ASCII, no name res
sudo tcpdump -i eth0 'host 192.168.56.20 and port 21'   # BPF capture filter
sudo tcpdump -r cap.pcap                         # read a saved capture
```
**Capture filters use BPF** (`tcp port 80`, `host x`, `net 192.168.56.0/24`, `udp`) — different syntax from Wireshark display filters.

## Wireshark — the essentials
- **Follow stream:** right-click a packet → *Follow → TCP/HTTP Stream* (reassembles a conversation — where cleartext creds appear).
- **Export files:** *File → Export Objects → HTTP / SMB / TFTP*.
- **Protocol hierarchy:** *Statistics → Protocol Hierarchy* (what's in the capture).
- **Credentials:** older Wireshark: *Tools → Credentials*; or `tshark -z credentials`.

## Wireshark display filters (post-capture)
```
http.request                      # all HTTP requests
http.request.method == "POST"     # form submissions
ftp.request.command == "PASS"     # FTP passwords (cleartext)
ftp || telnet || http             # cleartext protocols
tcp.port == 445 || smb2           # SMB
dns                               # DNS queries
tcp.flags.syn == 1 && tcp.flags.ack == 0    # SYN (scan/flood)
ip.addr == 192.168.56.20          # a host
tcp.stream eq 5                   # one conversation
frame contains "password"         # byte search
```

## tshark (Wireshark on the CLI)
```bash
tshark -r cap.pcap -Y 'http.request.method=="POST"' -T fields -e http.file_data
tshark -r cap.pcap -Y 'ftp.request.command=="USER" or ftp.request.command=="PASS"' -T fields -e ftp.request.arg
tshark -r cap.pcap -z io,phs -q                  # protocol hierarchy
tshark -r cap.pcap --export-objects http,./out   # carve HTTP files
tshark -r cap.pcap -z credentials -q             # extracted creds
```

## Common pcap-challenge answers
| You need | Do this |
|---|---|
| Login creds | Follow TCP/HTTP Stream on the FTP/HTTP conversation |
| A transferred file | Export Objects, or carve with `foremost`/`binwalk` on the pcap |
| A NetNTLMv2 hash | filter `ntlmssp`; extract and crack `hashcat -m 5600` |
| Which host/protocol | Protocol Hierarchy / Conversations |

> NetworkMiner (GUI) auto-extracts files, creds, and hosts from a pcap: https://www.netresec.com/?page=NetworkMiner · Wireshark filters — https://www.wireshark.org/docs/dfref/
