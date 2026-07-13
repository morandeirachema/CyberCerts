# Defender & PAM Mapping

This is the retention engine of the repo. Every offensive technique in the CEH modules is mapped here to the **detection signal** it produces and the **defensive / PAM control** that neutralizes it — so you learn the attack *through* the control you already operate as a sysadmin with a Privileged Access Management background.

| File | Contents |
|---|---|
| [attack-to-control-matrix.md](attack-to-control-matrix.md) | Master table: attack → detection → control, grouped by CEH module. Every module's "Defender & PAM mapping" section links here. |
| [pam-playbook.md](pam-playbook.md) | The PAM control set (vaulting, JIT, tiering, gMSA, LAPS, session brokering) and which attacks each one defeats. |
| [pam-architecture.md](pam-architecture.md) | **CyberArk-centered reference architecture** — Vault, PVWA, CPM, PSM/PSMP, PTA, EPM, Conjur/CCP, DPA, Remote Access — the access flow, the Zero-Standing-Privilege maturity model, discovery/onboarding, break-glass, and hardening the PAM stack. |
| [identity-attack-paths.md](identity-attack-paths.md) | **AD & Entra attack paths** — Kerberoasting, delegation abuse, DCSync/DCShadow, ADCS ESC1–8, golden/silver/diamond tickets, Entra token theft — each with detection + the control that breaks it. |
| [detection-engineering.md](detection-engineering.md) | **Detection layer** — Windows event IDs, Sysmon, Sigma rules, KQL/Splunk queries, and CyberArk PTA/Vault signals per attack. |
| [cyberark-attack-mapping.md](cyberark-attack-mapping.md) | **CyberArk component → CEH attack** it defeats (both lookup directions), plus onboarding/rotation reality. |

> **Which doc when.** Studying a module → start with the [matrix](attack-to-control-matrix.md). Want the *why* behind a control → [pam-playbook](pam-playbook.md). Building/operating the stack → [pam-architecture](pam-architecture.md). Red-team AD/Entra depth → [identity-attack-paths](identity-attack-paths.md). Hunting/SOC → [detection-engineering](detection-engineering.md). Translating to your CyberArk stack → [cyberark-attack-mapping](cyberark-attack-mapping.md).

## How to use these

1. After reading a module, open the matrix and find its rows. Cover the **Control** column and try to name the defense for each attack from memory.
2. Then cover the **Attack** column and, given a control (e.g. "gMSA"), name what it defeats. The exam and real interviews both ask it both ways.
3. Use the [pam-playbook.md](pam-playbook.md) to connect single controls to the *many* attacks they cover — that's how you compress 20 modules into a handful of load-bearing ideas.

> **Framing.** CEH is an offensive exam, but almost every question has a "best defense" flavor somewhere in the domain. If you can state the control, you can usually eliminate two wrong answers instantly. The PAM lens — *reduce standing privilege, broker and record access, rotate secrets, segment tiers* — is the single most reusable answer key across the whole blueprint.
