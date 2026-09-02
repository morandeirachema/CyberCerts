# Module 04 — Enumeration · Guided Lab Walkthrough

> Enumerate **only your own lab** (see [`../../labs/topology.md`](../../labs/topology.md)). Each step: command, expected observation, a hint, and the defender/PAM takeaway. Outputs are **representative**. Pairs with [README.md](README.md) · [facts.md](facts.md).

**Goal:** pull *names* from live services — SMB shares/users, SNMP data, SMTP users — then see how onboarding accounts removes the payoff.

**Targets:** Metasploitable2 `192.168.56.20` (SMB/Samba, SNMP, SMTP) · Windows DC `192.168.56.30`.

---

## Part A — SMB / NetBIOS enumeration
```bash
nmblookup -A 192.168.56.20                    # NetBIOS names
smbclient -L //192.168.56.20 -N               # list shares (null session)
enum4linux -a 192.168.56.20 | tee enum.txt    # users, shares, groups, policy
```
**You should see** shares (e.g., `tmp`, `IPC$`) and a user list. **Observe:** on Metasploitable2 the **null session** leaks users/shares without any credentials.

<details><summary>Hint</summary>If `enum4linux` is missing, use `enum4linux-ng`. `rpcclient -U "" -N 192.168.56.20` then `enumdomusers` does the RID-based user enumeration manually.</details>

## Part B — SNMP enumeration
```bash
snmpwalk -v2c -c public 192.168.56.20 | head -40   # walk the MIB with default community
snmpwalk -v2c -c public 192.168.56.20 1.3.6.1.2.1.25.4.2.1.2   # running processes
```
**You should see** system description, interfaces, and possibly process/route data. **Observe:** the default community string `public` is cleartext and grants read access — SNMPv3 is the fix.

## Part C — SMTP user enumeration
```bash
nc -nv 192.168.56.20 25
# then type:
#   VRFY root
#   VRFY msfadmin
#   VRFY nosuchuser
```
**You should see** `252`/`250` for existing users and `550` for non-existent ones — leaking valid usernames.

<details><summary>Hint</summary>Automate with `smtp-user-enum -M VRFY -U users.txt -t 192.168.56.20`. If VRFY is disabled, try `RCPT TO`.</details>

## Part D — Turn off the payoff (defender/PAM view)
- Disable **null sessions** and anonymous SMB → Part A yields nothing.
- Move to **SNMPv3** (drop v1/2c) → Part B fails.
- Disable **VRFY/EXPN** → Part C fails.
- **Onboard** every discovered **local admin** (unique rotated password, LAPS-style) and **service account** (gMSA/CPM) → the names you enumerated are no longer *reusable* credentials. See [attack-to-control-matrix.md](../../defender-pam/attack-to-control-matrix.md).

## What you should conclude
| You enumerated | The control that removes the value |
|---|---|
| SMB shares/users via null session | Disable null sessions/anonymous SMB |
| SNMP data via `public` | SNMPv3 auth+privacy |
| SMTP users via VRFY | Disable VRFY/EXPN |
| Local admins / service accounts | Vault + rotate (LAPS / gMSA / CPM) |

## Cleanup
```bash
rm -f enum.txt users.txt
```

## Record it
Log the users/shares you found in the **My lab log** table in [README.md](README.md); track weak areas in [PROGRESS.md](../../PROGRESS.md).
