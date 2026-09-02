# Deep Drill Packs

Where [`../drills.md`](../drills.md) is a quick 15-challenge sampler, these are **deep per-domain packs** — 8–12 Practical-style challenges each, every one with a **full step-by-step solution walkthrough** (commands + expected output + the exact answer), progressing from easy to hard. Solve under a timer; expand the solution only when done or stuck.

> **Setup:** the [lab](../../labs/README.md) running, and the [challenge-lab](../challenge-lab/README.md) generated (`../challenge-lab/setup-challenges.sh`) for the stego/pcap/crypto/hash packs. Recipes: [`../challenge-playbooks.md`](../challenge-playbooks.md).

| Pack | Drills what | Uses |
|---|---|---|
| [01 — Recon & scanning](01-recon-scanning.md) | Fingerprint hosts: OS, versions, FQDN, ports | lab |
| [02 — Enumeration](02-enumeration.md) | SMB/SNMP/LDAP/SMTP/NFS, users, shares | lab |
| [03 — Web & SQLi](03-web-and-sqli.md) | XSS, LFI, upload→RCE, cmd injection, SQLi | Docker web |
| [04 — Passwords & hashes](04-passwords-and-hashes.md) | Crack every hash type, online + offline | challenge-lab + lab |
| [05 — Active Directory](05-active-directory.md) | Kerberoast, AS-REP, RBCD, ADCS, DCSync, PtH | AD lab |
| [06 — PCAP forensics](06-pcap-forensics.md) | Extract creds/files/values from captures | challenge-lab + lab |
| [07 — Wireless](07-wireless.md) | Capture + crack WPA2, identify AP details | own AP / sample cap |
| [08 — Stego & crypto](08-stego-and-crypto.md) | steghide/exif/binwalk, decode/decrypt | challenge-lab |
| [09 — Exploitation & privesc](09-exploitation-privesc.md) | Get a shell, escalate, loot a file | lab |

## How to use
1. Pick a pack matching a weak area from your [skills checklist](../skills-checklist.md).
2. **Timer on.** Solve each challenge from the [recipes](../challenge-playbooks.md), not the solution.
3. Score ✅/⚠️/❌; re-drill anything not ✅ under time.
4. When every pack is ✅, take a full [simulated exam](../exams/README.md).
