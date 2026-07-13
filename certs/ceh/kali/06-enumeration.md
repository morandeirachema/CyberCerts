# 06 — Enumeration

> **What you'll learn:** how to turn the open ports you found with Nmap into a *named inventory* — usernames, shares, groups, machines, and configs — using SMB, SNMP, LDAP, SMTP, and NFS. You'll learn what null sessions and RID cycling are, and why every name you pull out here becomes ammunition for password attacks (ch 10) and Active Directory (ch 11).
> **Prerequisites:** [05 — Scanning with Nmap](05-nmap-scanning.md). ⬅️ [Course index](README.md)

---

## Scanning finds the door, enumeration reads the nameplate
In chapter 05, Nmap told you **which ports are open** and **what service** sits behind each one — "445/tcp open, Samba." That's the door. **Enumeration** is walking up and reading the nameplate: *who* uses this service, what **shares** it offers, which **user accounts** exist, what **groups** they're in, and how it's configured.

Two ideas to lock in first:
- **Enumeration is active.** You are making real requests to the target's services — sometimes anonymously, sometimes with credentials. This is louder than scanning and always lab-only.
- **Names are the prize.** A valid username isn't just trivia — it's half of a login. Chapter 10 (password attacks) and chapter 11 (Active Directory) *start* from the user and share lists you build right here.

This whole chapter maps to **CEH [Module 04](../modules/04-enumeration/)** — read it alongside for the exam theory (port numbers, NetBIOS suffix codes, countermeasures).

### The lab targets
| Target | IP | What we'll enumerate |
|---|---|---|
| Metasploitable2 | `192.168.56.20` | Wide-open Samba (SMB), SNMP, SMTP, NFS — the beginner playground |
| Windows DC `ceh.lab` | `192.168.56.30` | SMB + LDAP; anonymous view vs. authenticated (`jdoe` / `Passw0rd!`) |

### Ports → what you enumerate → tool
| Service | Port(s) | Payoff | Main tool |
|---|---|---|---|
| NetBIOS | 137/UDP, 139/TCP | Names, suffixes, MAC | `nbtscan`, `nmblookup` |
| SMB | 445/TCP | Shares, users, groups, policy | `nxc smb`, `enum4linux-ng`, `smbclient`, `rpcclient` |
| SNMP | 161/UDP | Full device config via the MIB | `snmpwalk` |
| LDAP | 389/TCP (636 LDAPS) | Users, groups, OUs, computers | `ldapsearch` |
| SMTP | 25/TCP | Valid usernames | `smtp-user-enum` |
| NFS | 2049/TCP (111 rpcbind) | Exported file systems | `showmount` |
| NTP | 123/UDP | Connected hosts, time source | `ntpq` |
| IKE / IPsec | 500/UDP | VPN gateway, aggressive mode | `ike-scan` |

Memorize the left two columns — the CEH exam drills these port pairs relentlessly.

---

## SMB / NetBIOS (139/445) — the richest target
**SMB** (Server Message Block) is Windows/Samba file-and-print sharing. **NetBIOS** is the older naming layer that rides on 137–139. On a misconfigured host these hand out an astonishing amount without any password.

### What is a null session?
A **null session** is a login with a **blank username and blank password** to the hidden `IPC$` "inter-process communication" share. Legacy Windows and default Samba (like Metasploitable2) allow it, and once connected you can often list users, groups, shares, and the password policy — **with no credentials at all**. It's the single most important idea in this chapter, and it's the engine inside `enum4linux`.

### Step 1 — NetBIOS names with `nbtscan`
```bash
nbtscan 192.168.56.20              # query one host's NetBIOS name table
nbtscan 192.168.56.0/24           # sweep the whole lab subnet for names
```
You should see the host's **NetBIOS name**, logged-in user, and **MAC address**. The two-digit **suffix codes** (e.g. `<20>` = file server running, `<1C>` = domain controller) tell you the machine's role — the exam loves these.

### Step 2 — Host info with NetExec (`nxc`)
**NetExec** (`nxc`, the modern successor to CrackMapExec) is the Swiss-army knife of AD enumeration. The first line already summarizes the box:
```bash
nxc smb 192.168.56.20             # OS, hostname, domain, SMB signing, SMBv1?
```
You should see one green line: OS version, computer name, domain/workgroup, and whether **SMB signing** is required and **SMBv1** is enabled (both are weaknesses when off/on).

Now use a **null session** (`-u '' -p ''` = empty user, empty password) to pull names:
```bash
nxc smb 192.168.56.20 -u '' -p '' --shares      # list shares + your access
nxc smb 192.168.56.20 -u '' -p '' --users       # domain/local user accounts
nxc smb 192.168.56.20 -u '' -p '' --groups      # groups (find the admins)
```
Against the **domain controller**, the anonymous view is usually locked down, so use the lab credentials you were issued:
```bash
# Authenticated enumeration of the DC — far richer output
nxc smb 192.168.56.30 -u jdoe -p 'Passw0rd!' --users --groups --shares
```

**Password spraying** — testing *one* password against *many* users — also lives in `nxc`. Feed it a userlist (e.g. the names you just enumerated) and one password; `--continue-on-success` keeps going after the first hit:
```bash
nxc smb 192.168.56.30 -u users.txt -p 'Passw0rd!' --continue-on-success
```
A `[+]` means valid creds. This is the bridge to chapter 10 — but spray gently in the lab: too many failures can **lock accounts**.

### Step 3 — The classic all-in-one: `enum4linux-ng`
`enum4linux-ng` is a modern rewrite of the legendary `enum4linux`: it automates null-session SMB/RPC queries and prints structured (JSON-friendly) output.
```bash
enum4linux-ng -A 192.168.56.20    # -A = do everything: users, groups, shares, RID cycle, policy
```
You should see sections for **users** (with RIDs), **groups**, **shares**, the **password policy**, and OS info — all pulled anonymously. This one command is often your whole SMB enumeration.

### Step 4 — Browse shares with `smbclient`
`smbclient` is the SMB equivalent of an FTP client.
```bash
smbclient -L //192.168.56.20/ -N          # -L = list shares, -N = no password (null session)
smbclient //192.168.56.20/tmp -N          # connect to the 'tmp' share anonymously
# at the smb:\> prompt:  ls  ,  get <file>  ,  cd <dir>  ,  exit
```
You should see a share list (`tmp`, `IPC$`, `print$`…). Any share you can enter without a password is a finding.

### Step 5 — MS-RPC and RID cycling with `rpcclient`
`rpcclient` speaks the Windows RPC protocol over SMB. Start a null session, then run queries at its prompt:
```bash
rpcclient -U "" -N 192.168.56.20          # -U "" empty user, -N no password
```
```text
rpcclient $> enumdomusers                 # list users + their RIDs
rpcclient $> enumdomgroups                # list groups
rpcclient $> querydominfo                 # domain / policy info
rpcclient $> lookupnames administrator    # translate a name -> SID
```

**What is RID cycling?** Every account has a **SID** (security identifier) ending in a **RID** (relative identifier): Administrator is always **500**, Guest **501**, and real users start at **1000**. Even when `enumdomusers` is blocked, you can often ask "who is RID 500? 501? 1000? 1001?" one by one and rebuild the user list. That's **RID cycling** — `enum4linux-ng` does it automatically, and `rpcclient` does it manually with `lookupsids`:
```text
rpcclient $> lookupsids S-1-5-21-1004336348-1177238915-682003330-500
```
Swap the last number to walk RIDs. The names you recover feed straight into chapters 10 and 11.

---

## SNMP (161/UDP) — the default-community goldmine
**SNMP** (Simple Network Management Protocol) lets admins read a device's whole configuration. Access is gated by a **community string** (a shared password). The catch: the defaults are almost universal — **`public` = read-only, `private` = read-write** — and v1/v2c send them in **cleartext**.

`snmpwalk` traverses the **MIB** (Management Information Base — the tree of everything the device will tell you):
```bash
snmpwalk -v2c -c public 192.168.56.20                        # -v2c version, -c public community; walk everything
snmpwalk -v2c -c public 192.168.56.20 1.3.6.1.2.1.25.4.2     # running processes
snmpwalk -v2c -c public 192.168.56.20 1.3.6.1.2.1.25.6.3     # installed software
```
You should see a flood of lines: hostname, interfaces, routes, **running processes**, and **installed software** — a free map of the box. If you don't know the community string, brute-force it:
```bash
onesixtyone -c /usr/share/wordlists/snmp.txt 192.168.56.20   # try common community strings
```
Think about `private`: with the read-write string you could *reconfigure* the device, not just read it.

---

## LDAP (389/TCP) — reading the directory
**LDAP** (Lightweight Directory Access Protocol) is how you query a directory service like **Active Directory** — users, groups, computers, and OUs (organizational units). Some servers permit an **anonymous bind** (query with no login). `ldapsearch` is the client; `-x` means "simple (anonymous) authentication."

First find the **base DN** (the top of the directory tree) — for `ceh.lab` it's `DC=ceh,DC=lab`:
```bash
ldapsearch -x -H ldap://192.168.56.30 -s base namingContexts   # ask the server for its base DN
```
Then search for users and groups:
```bash
# Anonymous: users' logon names
ldapsearch -x -H ldap://192.168.56.30 -b "DC=ceh,DC=lab" "(objectClass=user)" sAMAccountName
# Anonymous: group names
ldapsearch -x -H ldap://192.168.56.30 -b "DC=ceh,DC=lab" "(objectClass=group)" cn
```
Modern AD often blocks anonymous binds, so authenticate with your lab creds for the full picture:
```bash
ldapsearch -x -H ldap://192.168.56.30 -D "jdoe@ceh.lab" -w 'Passw0rd!' \
  -b "DC=ceh,DC=lab" "(objectClass=user)" sAMAccountName
```
The delta between the anonymous and authenticated results *is* the hardening lesson. Accounts with a **servicePrincipalName (SPN)** are the golden find — they're **Kerberoast** targets in chapter 11.

---

## SMTP (25/TCP) — validating usernames for free
A mail server will often tell you whether an account exists, via three verbs: **`VRFY`** (verify a user), **`EXPN`** (expand a mailing list), and **`RCPT TO`** (name a recipient). All three leak valid usernames. Try it by hand first with `nc` (netcat):
```bash
nc -nv 192.168.56.20 25
# then type:
#   VRFY root        -> 250/252 = user exists, 550 = no such user
#   RCPT TO:<root>   -> the most reliable modern check
```
Then automate it with `smtp-user-enum` and a username wordlist:
```bash
smtp-user-enum -M VRFY -U /usr/share/wordlists/metasploit/unix_users.txt -t 192.168.56.20
```
- `-M VRFY` = use the VRFY method  ·  `-U` = username list  ·  `-t` = target
You should see `exists` next to real accounts (`root`, `postgres`, `user`…). Every confirmed name is one you no longer have to guess in chapter 10.

---

## NFS (2049/TCP) — exported file systems
**NFS** (Network File System) shares folders to other machines. `showmount` asks which folders (**exports**) are offered and to whom:
```bash
showmount -e 192.168.56.20        # -e = list exports
```
You should see paths and their allowed hosts. An export offered to `*` (everyone) is a red flag — in the lab you can mount it read-only to browse:
```bash
sudo mkdir -p /mnt/nfs
sudo mount -t nfs 192.168.56.20:/ /mnt/nfs -o nolock   # lab only; swap /export for the real path
ls -la /mnt/nfs
```

---

## NTP (123) and IKE (500) — the quick ones
Round out the blueprint with two services the exam samples:

- **NTP (123/UDP)** — the time service can leak the list of clients it talks to and its upstream source:
```bash
ntpq -c rv 192.168.56.20          # read variables: version, sync source
ntpq -c peers 192.168.56.20       # NTP peers / connected hosts
```
- **IKE (500/UDP)** — the negotiation phase of an IPsec VPN. `ike-scan` fingerprints the gateway and detects insecure **aggressive mode** (needs root for the raw UDP socket):
```bash
sudo ike-scan 192.168.56.30       # identify an IKE/VPN gateway
sudo ike-scan -A 192.168.56.30    # -A = probe aggressive mode (weaker, leaks a hash)
```

---

## Common beginner mistakes
- **Confusing scanning with enumeration.** Nmap finding `445 open` is *scanning*; pulling the user list off it is *enumeration*. The exam tests this distinction directly.
- **Wrong quoting on empty creds.** A null session is `-u '' -p ''` (two single quotes = empty string), not omitting the flags. Put the password `Passw0rd!` in **single quotes** so the shell doesn't eat the `!`.
- **Forgetting SNMP is UDP.** If `snmpwalk` hangs, the port may be filtered or the community string wrong — try `onesixtyone` before giving up.
- **Not saving output.** These commands dump a lot. Redirect it: `enum4linux-ng -A 192.168.56.20 > smb-20.txt` (see [chapter 01](01-linux-essentials.md)). You'll need those names later.
- **Spraying too hard.** Password spraying in `nxc` can **lock accounts** in AD. One password across users, then wait — never a fast loop in the lab.
- **Stopping at anonymous.** Always compare the anonymous view with the authenticated one — the difference is exactly what a defender should be closing.

## ✅ Practice task
1. **SMB null session:** run `enum4linux-ng -A 192.168.56.20` and save it. Record the **users + RIDs** and **shares** it dumped *with no credentials* — that's the null-session weakness in action.
2. **NetExec:** run `nxc smb 192.168.56.20 -u '' -p '' --users`, then the authenticated `nxc smb 192.168.56.30 -u jdoe -p 'Passw0rd!' --users --groups --shares`. Note what the domain controller hides from anonymous users.
3. **RID cycling:** in `rpcclient -U "" -N 192.168.56.20`, run `enumdomusers`, then translate one name with `lookupnames <user>`.
4. **SNMP:** `snmpwalk -v2c -c public 192.168.56.20` — find one running process and one installed package in the output.
5. **SMTP + LDAP + NFS:** confirm `root` exists with `smtp-user-enum -M VRFY`, list users on the DC with `ldapsearch -x`, and list NFS exports with `showmount -e 192.168.56.20`. Build a single `users.txt` from everything you found — that file is your input to chapter 10.

## Next
➡️ [07 — Vulnerability analysis](07-vulnerability-analysis.md): taking the services and versions you enumerated and matching them to known vulnerabilities with nikto, searchsploit, and OpenVAS.

## Sources
- CEH Module 04 — Enumeration (this course): [`../modules/04-enumeration/`](../modules/04-enumeration/)
- NetExec (nxc) official wiki — https://www.netexec.wiki/
- enum4linux-ng — https://github.com/cddmp/enum4linux-ng
- Samba (smbclient / rpcclient) man pages — https://www.samba.org/
- Net-SNMP (snmpwalk) — http://www.net-snmp.org/
- OpenLDAP (ldapsearch) — https://www.openldap.org/
- smtp-user-enum — https://github.com/pentestmonkey/smtp-user-enum
- ike-scan — https://github.com/royhills/ike-scan
- HackTricks — Pentesting SMB / SNMP / LDAP — https://book.hacktricks.xyz/
- MITRE ATT&CK: Account Discovery (T1087) — https://attack.mitre.org/techniques/T1087/
