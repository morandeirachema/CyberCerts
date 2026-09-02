# CEH Practical — Hands-On Skills Checklist

> The Practical tests whether you can *do* things fast. Go down this list and honestly rate each skill: **✅ can do cold in a few minutes / ⚠️ need notes / ❌ can't yet**. Drill every ⚠️ and ❌ against your [lab](../labs/README.md) using [drills.md](drills.md) and the recipes in [challenge-playbooks.md](challenge-playbooks.md). If you can check every box without looking anything up, you're ready.

> Each skill links to where it's taught: `[K##]` = [Kali course](../kali/README.md) chapter, `[M##]` = [module](../modules/README.md).

## Discovery & enumeration
- [ ] Discover live hosts on a subnet and full-port scan a target with output saved `[K05][M03]`
- [ ] Identify service versions and OS from a scan, and pick the next step `[K05]`
- [ ] Enumerate SMB: list shares, connect anonymously, pull a file `[K06][M04]`
- [ ] Enumerate users/groups from SMB/LDAP/RPC (incl. RID cycling) `[K06]`
- [ ] Enumerate SNMP (`snmpwalk`), SMTP users (`VRFY`), NFS exports `[K06]`
- [ ] Grab and interpret banners (FTP/SSH/HTTP) `[K05]`

## Passwords & hashes
- [ ] Identify an unknown hash type (`hashid`) `[K10]`
- [ ] Crack MD5/SHA1/NTLM/bcrypt with hashcat (right `-m` mode) `[K10][M06]`
- [ ] Crack `/etc/shadow` with john (`unshadow`) `[K10]`
- [ ] Online brute force a service (SSH, or an HTTP login form) with hydra `[K10]`
- [ ] Build a targeted wordlist (`cewl`, `crunch`) and apply rules `[K10]`

## Web & SQL
- [ ] Fingerprint a web app and discover hidden content (`whatweb`, `ffuf`/`gobuster`) `[K08][M13]`
- [ ] Find and exploit XSS, and read a file via LFI/traversal `[K08][M14]`
- [ ] Upload a web shell and get command execution `[K08][M13]`
- [ ] Do SQLi by hand: detect, count columns, UNION, dump a specific value `[M15]`
- [ ] Automate SQLi with sqlmap to extract a named value `[K08][M15]`

## Exploitation & privilege escalation
- [ ] Find a public exploit for a version (`searchsploit`) and use it `[K07]`
- [ ] Get a shell with Metasploit and upgrade to Meterpreter `[K09][M06]`
- [ ] Build and catch a payload with msfvenom + multi/handler `[K09]`
- [ ] Linux privesc: `sudo -l`, SUID (`find / -perm -4000`), linpeas `[K14][M06]`
- [ ] Windows privesc: `whoami /priv`, winpeas, `getsystem` `[K14]`
- [ ] Loot credentials from a foothold (hashdump, config files, history) `[K14]`

## Active Directory
- [ ] Enumerate the domain and read attack paths in BloodHound `[K11][M06]`
- [ ] Kerberoast an SPN account and crack it `[K11]`
- [ ] AS-REP roast a no-preauth account `[K11]`
- [ ] Pass-the-Hash to a shell (`impacket-psexec`, `evil-winrm -H`) `[K11]`
- [ ] DCSync to pull a hash with a privileged account `[K11]`

## Sniffing, wireless & forensics-style tasks
- [ ] Extract cleartext credentials from a pcap (Follow TCP Stream) `[K12][M08]`
- [ ] Find a transferred file / secret inside a capture `[K12]`
- [ ] Capture and crack a WPA2 handshake (`aircrack`/`hashcat -m 22000`) `[K13][M16]`
- [ ] Extract hidden data from an image/file (steganography) `[M06]`

## Cryptography & encoding
- [ ] Recognize and decode base64/hex/ROT/URL encodings `[M20]`
- [ ] Identify a cipher/hash and crack or decrypt it `[M20]`
- [ ] Use `openssl` and `gpg` to decrypt/verify given a key `[M20]`

## Speed & workflow (the meta-skills that pass the exam)
- [ ] Keep a clean notes file + `nmap -oA` output without thinking about it `[K15]`
- [ ] Match any challenge question to a recipe in [challenge-playbooks.md](challenge-playbooks.md) `[K—]`
- [ ] Know when to **skip and return** rather than sink 40 minutes `[README](README.md)`
- [ ] Read the answer's exact format (case, no trailing spaces) before submitting `[README](README.md)`

---

## How to use this list
1. Rate every box today — be honest.
2. For each ❌/⚠️, open the linked chapter/module, then do the matching [drill](drills.md) **under a timer**.
3. Re-rate weekly. When the whole list is ✅ cold, book the Practical.

> A pass is roughly 14 of 20 challenges — but the challenges are *timed*. The goal isn't "can I eventually do this," it's "can I do this in under ~18 minutes, repeatably."
