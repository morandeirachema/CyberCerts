# Module 01 — Introduction to Ethical Hacking · Guided Lab Walkthrough

> A foundational, hands-on exercise: this module has no exploitation — instead you **stand up and validate your isolated lab**, write the **authorization/scope** that makes everything after it legal, and practice **mapping an attack to a framework**. Do this once; it underpins every other module. Pairs with [README.md](README.md) · [facts.md](facts.md).

**Goal:** prove your lab is isolated, produce a scope/Rules-of-Engagement note, and place a real technique on the Cyber Kill Chain and MITRE ATT&CK.

**Targets:** the lab from [`../../labs/`](../../labs/) — Kali `192.168.56.10`, Metasploitable2 `192.168.56.20`, Windows DC `192.168.56.30`.

---

## Part A — Stand up and VALIDATE isolation

### A1. Confirm the lab hosts are reachable
```bash
for ip in 20 30; do ping -c1 -W1 192.168.56.$ip >/dev/null && echo "192.168.56.$ip UP" || echo "192.168.56.$ip DOWN"; done
```
**You should see** both targets `UP`.

### A2. Prove the lab is ISOLATED (the critical step)
```bash
# from a lab VM, the lab segment must NOT reach the internet or your home LAN:
ping -c1 -W1 8.8.8.8 && echo "WARNING: lab can reach the internet" || echo "GOOD: no internet route"
ip route                       # confirm only the 192.168.56.0/24 host-only route for lab traffic
```
**You should see** `GOOD: no internet route` from the isolated segment. **Observe:** isolation is what makes aggressive testing safe — a misfired exploit or a real malware sample can't escape.

<details><summary>Hint</summary>In VirtualBox, the attacker/target NICs should be on a **Host-Only** or **Internal** network, not NAT/Bridged, for the lab segment. A second NAT NIC for updates is fine only if it's a separate, non-target interface.</details>

**Defender/PAM view:** isolation is segmentation (Module 08/18) applied to your own range — the same control you'd demand around Tier 0 in [pam-architecture.md](../../defender-pam/pam-architecture.md).

---

## Part B — Write your scope / Rules of Engagement
Create `scope.md` in your lab notes (a habit that keeps you legal and focused):
```markdown
# Engagement scope (LAB)
- Authorization: I own this lab; testing is self-authorized and isolated.
- In scope:  192.168.56.0/24 (Kali .10, Metasploitable2 .20, DC .30)
- Out of scope: any address outside 192.168.56.0/24; the host OS; the internet
- Window: anytime (personal lab)
- Methods: recon, scanning, exploitation, post-ex on in-scope hosts only
- Handling: loot/captures stay in git-ignored folders; no real PII
- Emergency stop: power off the VMs
```
**Observe:** a real engagement's RoE also names client contacts, blackout windows, and legal sign-off. The discipline — *define scope before you touch anything* — is identical.

---

## Part C — Map a technique to the frameworks
Take one technique you'll use later (e.g., **Kerberoasting**, Module 06) and place it:

| Framework | Where it lands |
|---|---|
| 5-phase methodology | Gaining Access (credential access) |
| Cyber Kill Chain | Exploitation → Actions on Objectives |
| MITRE ATT&CK | Tactic: Credential Access · Technique: **T1558.003** Kerberoasting |

**You should conclude:** frameworks give you a shared vocabulary — you can describe *what* an attacker did (technique), *why* (tactic), and *where in the campaign* (kill-chain phase). Defenders use the same map to place detections.

<details><summary>Hint</summary>Browse <https://attack.mitre.org/> and find the technique ID for another attack you know (e.g., Phishing = T1566). Getting comfortable navigating ATT&CK pays off across the whole exam.</details>

---

## What you should conclude
| You did | Why it matters |
|---|---|
| Verified lab isolation | Safe, legal testing; nothing escapes |
| Wrote a scope/RoE note | Authorization + focus = the ethical core of the cert |
| Mapped a technique to frameworks | Shared language for attack and defense |

## Cleanup
Nothing to clean — keep `scope.md` with your lab notes.

## Record it
Note your isolation check and framework mapping in the **My lab log** table in [README.md](README.md); track weak areas in [PROGRESS.md](../../PROGRESS.md).
