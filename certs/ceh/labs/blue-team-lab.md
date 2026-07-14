# Blue-Team Lab — Attack It, Then Detect It

The rest of the repo teaches you to *break in*. This lab makes the [detection-engineering](../defender-pam/detection-engineering.md) theory **doable**: you run the [capstone](capstone.md) attacks, then hunt your own footprints in the logs. Understanding both sides is the master-level skill — and the repo's whole premise (every attack has a control) becomes real when you *see* the attack fire.

> **Prereqs:** the Windows [AD lab](ansible/) running (dc01 `192.168.56.30`, ws01 `192.168.56.31`). Everything here runs on **your own lab**. This is defensive tooling — safe to run anywhere you own.

## Setup the sensors (once)

**1. Sysmon** — the single best free endpoint sensor. Install on dc01 and ws01:
```powershell
# on each Windows host (admin PowerShell):
Invoke-WebRequest https://download.sysinternals.com/files/Sysmon.zip -OutFile Sysmon.zip; Expand-Archive Sysmon.zip
Invoke-WebRequest https://raw.githubusercontent.com/SwiftOnSecurity/sysmon-config/master/sysmonconfig-export.xml -OutFile sysmon.xml
.\Sysmon\Sysmon64.exe -accepteula -i sysmon.xml
# logs land in: Applications and Services Logs > Microsoft > Windows > Sysmon > Operational
```

**2. Windows audit policy** — make sure the events exist (on the DC):
```powershell
auditpol /set /subcategory:"Kerberos Service Ticket Operations" /success:enable /failure:enable   # 4769
auditpol /set /subcategory:"Directory Service Access" /success:enable                              # 4662 (DCSync)
auditpol /set /subcategory:"Logon" /success:enable /failure:enable                                 # 4624/4625
auditpol /set /subcategory:"Process Creation" /success:enable                                      # 4688
# enable command-line in 4688 + PowerShell script-block logging via GPO (Admin Templates)
```

**3. (Optional) Hunt at scale with Sigma** — apply community detection rules to the EVTX offline:
```bash
# on Kali, after copying the .evtx off the host:
# Chainsaw (fast EVTX + Sigma):  https://github.com/WithSecureLabs/chainsaw
chainsaw hunt Security.evtx -s sigma/ --mapping mappings/sigma-event-logs-all.yml
# or Zircolite:  https://github.com/wagga40/Zircolite
```

---

## The exercises — run the attack, then catch it

For each: run the attack from the capstone, then run the hunt query on the target, confirm the signal, and note the fix. Use `Get-WinEvent` on the host, or copy the EVTX to Kali and Sigma-hunt it.

### 1. Kerberoasting → event 4769 (RC4)
**Attack:** capstone Stage 2 (`impacket-GetUserSPNs ... -request`).
**Hunt (on dc01):**
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4769} |
  Where-Object { $_.Message -match 'Ticket Encryption Type:\s+0x17' -and $_.Message -notmatch '\$' } |
  Select-Object TimeCreated, @{n='Account';e={($_.Message -split 'Account Name:\s+')[1].Split("`n")[0]}}
```
**Signal:** TGS requests (4769) for a user SPN using **RC4 (0x17)**. **Fix:** gMSA / AES-only. → [detection-engineering.md](../defender-pam/detection-engineering.md).

### 2. AS-REP roasting → event 4768 (no pre-auth)
**Attack:** `impacket-GetNPUsers`. **Hunt:** 4768 with pre-auth type `0`. **Fix:** require Kerberos pre-auth.

### 3. DCSync → event 4662 from a non-DC
**Attack:** capstone Stage 5 (`impacket-secretsdump ... -just-dc-user krbtgt`).
**Hunt (on dc01):**
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4662} |
  Where-Object { $_.Message -match '1131f6aa-9c07-11d1-f79f-00c04fc2dcd2' }   # DS-Replication-Get-Changes
```
**Signal:** replication (4662 with the replication GUID) requested by a **user**, not a DC computer account. **Fix:** replication rights only on DCs; Tier 0 isolation.

### 4. Pass-the-Hash / lateral movement → event 4624 type 3 NTLM
**Attack:** `impacket-psexec -hashes` / `evil-winrm -H` to ws01.
**Hunt (on ws01):**
```powershell
Get-WinEvent -FilterHashtable @{LogName='Security';Id=4624} |
  Where-Object { $_.Message -match 'Logon Type:\s+3' -and $_.Message -match 'Authentication Package:\s+NTLM' }
```
Plus Sysmon **EID 1** (process create) for `psexesvc`/service install (7045). **Fix:** LAPS, tiering, Protected Users.

### 5. LSASS credential dumping → Sysmon EID 10
**Attack:** Mimikatz / `procdump lsass` on a host.
**Hunt:**
```powershell
Get-WinEvent -LogName 'Microsoft-Windows-Sysmon/Operational' |
  Where-Object { $_.Id -eq 10 -and $_.Message -match 'lsass.exe' -and $_.Message -match 'GrantedAccess:\s+0x1010|0x1410|0x1438' }
```
**Signal:** a non-system process opening a handle to **lsass.exe**. **Fix:** Credential Guard, LSASS PPL, EDR/ASR.

### 6. Covering tracks → event 1102 (log cleared)
**Attack:** `wevtutil cl Security`.
**Hunt:** `Get-WinEvent -FilterHashtable @{LogName='Security';Id=1102}` — clearing the log *is itself* a high-signal event. **Fix:** forward logs off-host to a SIEM so clearing the local copy doesn't help.

### 7. Encoded PowerShell / LOLBins → event 4104 + Sysmon 1
**Attack:** an encoded PowerShell one-liner or a `certutil` download.
**Hunt:**
```powershell
Get-WinEvent -LogName 'Microsoft-Windows-PowerShell/Operational' |
  Where-Object { $_.Id -eq 4104 -and $_.Message -match 'FromBase64String|IEX|DownloadString|-enc' }
```
**Fix:** script-block logging (you just used it), constrained language mode, ASR.

---

## Debrief — the both-sides view
| Attack (capstone) | Primary detection | The control that prevents it |
|---|---|---|
| Kerberoasting | 4769 RC4 for SPNs | gMSA / AES-only |
| AS-REP roasting | 4768 no-preauth | require pre-auth |
| DCSync | 4662 replication from non-DC | replication rights on DCs only |
| Pass-the-Hash | 4624 type-3 NTLM, 7045 | LAPS + tiering + Protected Users |
| LSASS dumping | Sysmon 10 handle to lsass | Credential Guard + PPL + EDR |
| Log clearing | 1102 | ship logs off-host |
| Encoded PowerShell | 4104 | script-block logging + CLM + ASR |

**What you should conclude:** every offensive win in this repo leaves a signal, and every signal maps to a preventive control. Run the [capstone](capstone.md) once as the attacker and once as the defender — hunting your own attack teaches detection better than any reading. This is the [PTA/UEBA behavioral layer](../defender-pam/detection-engineering.md) done by hand.

## Sources
- Sysmon (Sysinternals): https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
- SwiftOnSecurity Sysmon config: https://github.com/SwiftOnSecurity/sysmon-config
- Sigma rules: https://github.com/SigmaHQ/sigma · Chainsaw: https://github.com/WithSecureLabs/chainsaw
- Microsoft — Events to monitor (appendix L): https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/plan/appendix-l--events-to-monitor
- Wazuh (free SIEM/XDR, optional): https://wazuh.com/
