# Module 04 — Enumeration · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## What enumeration *is*
**Active** extraction of *names* from services scanning already found: users, groups, shares, machines, and configs. Scanning finds the open door; enumeration reads the nameplate. You are making anonymous or authenticated **requests** to a live service — so it is never passive.

**Flow:** open ports (Module 03) → identify service + version → query it (anon / default creds) → extract NAMES (users, shares, groups, configs) → feed Module 05/06.

## Protocol → default port (drill these cold)
| Service | Port(s) | Enumeration payoff |
|---|---|---|
| NetBIOS name | 137/UDP | Names, suffixes, MAC |
| NetBIOS datagram | 138/UDP | Browser / service info |
| NetBIOS session | 139/TCP | SMB over NetBIOS, null sessions |
| SMB (direct) | 445/TCP | Shares, users, groups, policy |
| SNMP | 161/UDP (traps **162**) | Full config via the MIB |
| LDAP / LDAPS | 389/TCP, **636**/TCP | Users, groups, OUs, computers |
| Global Catalog | 3268 / 3269 | Forest-wide AD objects |
| NFS | 2049/TCP | Exported file systems |
| SMTP | 25/TCP | Valid usernames (VRFY/EXPN) |
| DNS | 53 (TCP zone transfer / UDP query) | Hostnames, records, internal IPs |
| NTP | 123/UDP | Hosts, internal IPs, OS/time data |
| RPC endpoint mapper | 135/TCP | Service → port mapping |
| Kerberos | 88/TCP-UDP | User existence, AS-REP roasting |

## NetBIOS & SMB
- **NetBIOS** = legacy name service on **137/138/139**; **SMB direct** = **445/TCP** (no NetBIOS needed).
- Enumerate the NetBIOS **name table** with `nbtstat -A <ip>` (Windows) or `nmblookup -A <ip>` / `nbtscan` (Linux).
- **NetBIOS suffix codes** identify the service behind a name:

| Suffix (hex) | Meaning |
|---|---|
| `<00>` | Workstation service (computer name) |
| `<20>` | File Server (SMB) service running |
| `<1C>` | Domain controllers / group |
| `<1B>` | Domain master browser (PDC) |
| `<1D>` | Master browser |

## Null (anonymous) session
- Connect to `\\host\IPC$` with an **empty username AND empty password**.
- Historically dumps users, groups, shares, and password policy **without credentials**.
- It is the engine behind **enum4linux**; legacy Windows and misconfigured Samba allow it.
- Kill it with `RestrictAnonymous` / `RestrictAnonymousSAM`.

## RID cycling
- Every account has a **SID** ending in a **RID**; the built-in **Administrator is RID 500**, **Guest is 501**, first normal user starts at **1000**.
- Even if listing users is blocked, you can **cycle RIDs** (500, 501, 1000, 1001…) and resolve each to a name — automated by `enum4linux` / `rpcclient` (`lookupsids`).

## SNMP
- **`public`** = default **read-only** community; **`private`** = default **read-write**.
- Read-write + default string = you can *reconfigure* the device, not just read it. "Which string gives **write**?" → **`private`**.
- The **MIB** (Management Information Base) is the tree of queryable objects; `snmpwalk` traverses it.
- **v1 / v2c send the community string in cleartext**; **v3 adds authentication + encryption** (the secure version).
- Brute community strings with `onesixtyone`; useful OIDs: processes `1.3.6.1.2.1.25.4.2`, installed software `1.3.6.1.2.1.25.6.3`.

## LDAP
- **389** = LDAP, **636** = LDAPS (TLS); **3268/3269** = Global Catalog (forest-wide).
- An **anonymous bind** (empty DN) can dump users, groups, OUs, and computers from AD.
- `ldapsearch -x -H ldap://<dc> -s base namingContexts` finds the **base DN**; then filter `(objectClass=user)` / `(objectClass=group)`.

## NTP (123/UDP)
- NTP enumeration reveals **hosts connected to the time server**, their internal IPs, and OS/time data — handy for mapping an internal network.
- Tools: `ntpq`, `ntpdc`, `ntptrace`; classic queries `ntpq -c readlist`, `ntpq -c peers`, `ntpdc -c monlist` (the `monlist` command also enabled a famous amplification DDoS).

## SMTP (25/TCP) user enumeration
- **`VRFY <user>`** = verifies a user exists.
- **`EXPN <list>`** = expands a mailing list into its members.
- **`RCPT TO:<user>`** = checks a recipient; the most reliable modern check.
- Reply codes: **250 / 252 = exists**, **550 = no such user**. Automate with `smtp-user-enum`.

## DNS enumeration
- **Zone transfer (AXFR)** = the jackpot: a misconfigured server hands over the **entire zone** (all hostnames, IPs, records).
- `dig axfr <domain> @<nameserver>` or `nslookup` → `ls -d <domain>`; broader recon with `dnsrecon` / `dnsenum` / `fierce`.
- Record types to know: **A / AAAA** (host), **MX** (mail), **NS** (nameservers), **SOA** (zone authority), **CNAME** (alias), **TXT** (SPF/misc), **PTR** (reverse), **SRV** (service locators — great for AD).

## Tools → purpose
| Tool | Does |
|---|---|
| `nbtstat` / `nbtscan` / `nmblookup` | NetBIOS name-table query |
| `enum4linux` (`-ng`) | All-in-one SMB/NetBIOS: users, shares, RID cycle, policy |
| `smbclient -L //host -N` | List SMB shares over a null session |
| `rpcclient -U "" -N` | Null-session MS-RPC: `enumdomusers`, `enumdomgroups`, `querydominfo` |
| `snmpwalk` (net-snmp) | Walk the SNMP MIB |
| `onesixtyone` | Brute SNMP community strings |
| `ldapsearch` (OpenLDAP) | LDAP / AD directory queries |
| `showmount -e` | List NFS exports |
| `smtp-user-enum` | SMTP username enumeration |
| `dig` / `dnsrecon` / `dnsenum` | DNS records + zone transfer |
| `NetExec` (ex-CrackMapExec) | Multi-protocol AD enumeration |

## The PAM / defender angle (your edge)
Enumeration is a **checklist of anonymous-access hardening** — exactly what a PAM/sysadmin owns. The worst outcome is enumeration that **names your privileged groups and service accounts before a single credential is spent**.
- Onboard every enumerated **local admin** → unique, CPM/LAPS-rotated password per host (or remove it with EPM).
- Onboard every enumerated **service account (SPN)** → vault + rotate, or convert to **gMSA** so its name is no longer a Kerberoast target (Module 06).
- Disable **null sessions**, remove **default SNMP strings** (use v3), disable **anonymous LDAP bind**, disable **SMTP VRFY/EXPN**, restrict **DNS zone transfers**.
- **Tier your OUs** so a low-priv enumerator can't see Tier 0.

## Top traps
- **Enumeration is active**, not passive — you query the target's services directly. Don't confuse it with scanning (scanning finds open ports; enumeration extracts names/accounts/shares).
- **SNMP: `public` = read-only, `private` = read-write.** The "which gives write access?" answer is **`private`**.
- **SNMPv3** is the secure version; **v1/v2c community strings travel in cleartext.**
- **Null session** = `IPC$` with blank user **and** blank password (both empty).
- **SMTP verbs:** VRFY = verify user, EXPN = expand list, RCPT TO = check recipient — all leak valid usernames.
- **LDAPS is 636**, not 389; Global Catalog is **3268/3269**.
- **`showmount -e`** lists NFS exports (`-a` lists who's mounted).
- **RID 500 = Administrator** regardless of the account's renamed name — RID cycling defeats account renaming.
- **DNS AXFR** (zone transfer) leaks the whole zone; a single-record query does not.
