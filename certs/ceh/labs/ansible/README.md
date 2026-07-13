# Windows AD / PAM lab (Ansible)

Builds a Domain Controller (`ceh.lab`) with a **tiered administration model** — the PAM structure you already run — so you can practice enumeration, Kerberoasting, and credential-access attacks against it *and* watch the controls (tiering, Protected Users) contain them.

This is the highest-value lab for a PAM/sysadmin: you attack your own reference design.

## What you must provide

Ansible configures Windows; it does not create the VMs. Provide two Windows VMs (free evaluation ISOs):

- **Windows Server 2022 (eval)** → `dc01`, host-only IP `192.168.56.30`
  - Download: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022
- **Windows 10/11 (eval)** → `ws01`, host-only IP `192.168.56.31` (optional but recommended)
  - Download: https://www.microsoft.com/en-us/evalcenter/

## Setup steps

1. **Install the collections** (on Kali or your host):
   ```bash
   ansible-galaxy collection install microsoft.ad ansible.windows community.windows
   ```
2. **Enable WinRM on each Windows VM** (run in an elevated PowerShell on the VM). Use Ansible's official helper script:
   - Script + guide: https://docs.ansible.com/ansible/latest/os_guide/windows_setup.html
   ```powershell
   # On each Windows VM (lab only — this opens WinRM):
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   $url = "https://raw.githubusercontent.com/ansible/ansible-documentation/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
   iwr -useb $url | iex
   ```
3. **Store the admin password in Ansible Vault** (never plaintext):
   ```bash
   ansible-vault create group_vars/windows/vault.yml
   # add:
   #   vault_admin_password: "<local admin password>"
   #   vault_safe_mode_password: "<DSRM password>"
   #   vault_user_password: "<initial account password>"
   ```
4. **Run it:**
   ```bash
   ansible-playbook -i inventory.ini ad-lab.yml --ask-vault-pass
   ```

## What you get

```
Domain ceh.lab (NetBIOS CEH)
├── OU=Tier0     t0-admin        (+ Protected Users)   ← forest control
├── OU=Tier1     t1-svradmin, svc-sql (Kerberoastable) ← server admins
├── OU=Tier2     t2-helpdesk                            ← workstation admins
└── OU=Standard  jdoe                                   ← normal user
```

## Practice loop (attack ➜ observe control)

| Step | Attack (from Kali) | Control you should see working |
|---|---|---|
| Enumerate | `enum4linux-ng 192.168.56.30`, `ldapsearch`, `rpcclient` | Least-privilege limits what an anon/low-priv user sees |
| Kerberoast | Request `svc-sql` TGS, crack offline | Strong/managed service passwords (gMSA) defeat cracking |
| Cred theft | Attempt to reuse `t0-admin` creds on Tier 2 | **Tiering + Protected Users** block the lateral path |

Full mapping: [`../../defender-pam/attack-to-control-matrix.md`](../../defender-pam/attack-to-control-matrix.md)

## Cleanup

Snapshot the VMs before you start so you can roll back. To rebuild the directory objects, delete the OUs or restore the snapshot.

> Microsoft evaluation editions expire (typically 180 days). Re-arm or rebuild as needed; this is a throwaway lab.
