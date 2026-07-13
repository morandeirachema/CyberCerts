# PAM Playbook

The PAM/defender control set, each entry framed as: *what it is → what attacks it defeats → how you'd operate it*. This is the "control → attack" direction of the [attack-to-control-matrix.md](attack-to-control-matrix.md), written for someone who runs these controls for a living and wants them as an answer key for the exam.

> The unifying idea of PAM: **reduce standing privilege to near-zero, broker and record every privileged access, and rotate the secrets that remain.** Almost every CEH attack that "wins" does so by finding *standing* privilege or a *reusable* secret. Take those away and the technique still runs but stops paying off.

---

## 1. Least privilege / no standing local admin

- **What it is:** users and services hold only the rights their role needs; no one is a permanent local admin on their workstation, and no service runs as Domain Admin "to make it work."
- **Defeats:** most malware persistence and rootkit installs (Module 07), privilege escalation footholds (06), web-shell → host pivot (13/14), and dramatically shrinks blast radius everywhere.
- **Operate it:** remove users from local Administrators, use LAPS for the break-glass local admin, scope service accounts tightly, review access regularly.

## 2. Just-in-Time (JIT) elevation

- **What it is:** privilege is granted **for a task, for a short window, then revoked** — no standing admin sitting idle to be stolen.
- **Defeats:** Pass-the-Hash/Ticket value (06), stolen-admin-token reuse (11), ransomware that relies on grabbing existing admin rights (07), cloud role abuse (19).
- **Operate it:** request → approve → time-boxed grant → auto-revoke; log every elevation. Pair with number-matching MFA on the approval.

## 3. Tiered administration (Tier 0/1/2)

- **What it is:** admin planes are separated so a credential from a lower tier can never authenticate to a higher one. Tier 0 (identity: DCs, ADCS, PAM) is isolated from Tier 1 (servers) and Tier 2 (workstations).
- **Defeats:** lateral movement and privilege escalation via credential reuse (06), the whole "workstation compromise → Domain Admin" path.
- **Operate it:** dedicated admin accounts per tier, Privileged Access Workstations (PAWs), Protected Users group, logon-restriction policies, Authentication Policies/Silos.

## 4. Credential vaulting + rotation

- **What it is:** privileged credentials live in a vault, are checked out (or injected) rather than known, and rotate automatically — including after each use for the most sensitive.
- **Defeats:** leaked/hardcoded secrets (14/19/20), local-admin reuse (06), IoT/OT default creds (18), long-lived cloud keys (19).
- **Operate it:** no human knows the password; the PAM broker injects it. Rotate on a schedule and on check-in. Store API keys/certs in a KMS/HSM.

## 5. gMSA for service accounts

- **What it is:** Group Managed Service Accounts use **128-character, automatically-rotated** passwords the OS manages.
- **Defeats:** **Kerberoasting** (06) — the crackable-service-password attack simply has nothing crackable left.
- **Operate it:** convert SPN-bearing service accounts to gMSA; where impossible, enforce very long random passwords and AES-only Kerberos.

## 6. LAPS (Local Administrator Password Solution)

- **What it is:** every machine gets a **unique, rotated** local administrator password stored in AD/Entra.
- **Defeats:** local-admin **hash/password reuse** and lateral movement via a shared local admin (06/08).
- **Operate it:** deploy LAPS, restrict who can read the passwords, audit reads.

## 7. Phishing-resistant MFA

- **What it is:** FIDO2/passkeys or certificate-based auth that can't be replayed or relayed, replacing SMS/OTP.
- **Defeats:** phishing and credential theft (09), session/token replay (11), SMS-OTP interception and SIM swap (17), credential stuffing.
- **Operate it:** enforce for all privileged access; use number-matching to kill MFA-fatigue; remove SMS as a factor for admins.

## 8. Privileged session brokering, isolation & recording

- **What it is:** admins connect **through** a PAM proxy that injects the target credential server-side, isolates the session from the endpoint, and records it. The admin's machine never holds the target secret.
- **Defeats:** credential sniffing/MITM (08/11), keyloggers on the endpoint stealing admin creds (07), and gives you the audit trail for detection.
- **Operate it:** route RDP/SSH/web-admin through the broker; disable direct admin paths; retain session recordings.

## 9. Network segmentation & egress control

- **What it is:** flat networks become zoned; only required traffic crosses boundaries; outbound is allow-listed.
- **Defeats:** scanning/lateral spread (03/06), C2 beaconing and tunneling (07/12), SSRF-to-metadata (14/19), OT exposure (18).
- **Operate it:** micro-segment critical assets, isolate OT (IEC 62443 zones/conduits), block egress by default, monitor DNS.

## 10. Logging, monitoring & detection

- **What it is:** the visibility layer — you can't defend what you can't see. Feeds every "detection signal" column in the matrix.
- **Defeats:** nothing on its own, but it's the prerequisite for catching every attack early — and PAM session logs are among the highest-signal sources you have.
- **Operate it:** centralize logs, alert on the signals in the matrix (4625/4769/4662, LSASS access, gratuitous ARP, egress anomalies), and baseline privileged behavior.

---

## Quick "control defeats attack" recall table

| PAM control | Signature attack it kills |
|---|---|
| gMSA | Kerberoasting |
| LAPS | Local-admin hash reuse |
| Tiering + Protected Users | Pass-the-Hash lateral movement |
| JIT elevation | Standing-admin theft / ransomware rights |
| Vault + rotate | Leaked/hardcoded/default secrets |
| Phishing-resistant MFA | Phishing, SIM-swap, token replay |
| Session brokering | Endpoint credential theft / sniffing |
| Segmentation + egress control | C2 beaconing, SSRF, OT exposure |

> **Exam heuristic:** when a question asks for the *best* mitigation, prefer the answer that **removes the privilege or secret the attack depends on** over the one that merely detects it. Prevention beats detection in CEH's "best answer" logic — but if prevention isn't offered, pick the strongest detection/monitoring option.
