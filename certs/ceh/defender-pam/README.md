# Defender & PAM Mapping

This is the retention engine of the repo. Every offensive technique in the CEH modules is mapped here to the **detection signal** it produces and the **defensive / PAM control** that neutralizes it — so you learn the attack *through* the control you already operate as a sysadmin with a Privileged Access Management background.

| File | Contents |
|---|---|
| [attack-to-control-matrix.md](attack-to-control-matrix.md) | Master table: attack → detection → control, grouped by CEH module. Every module's "Defender & PAM mapping" section links here. |
| [pam-playbook.md](pam-playbook.md) | The PAM control set (vaulting, JIT, tiering, gMSA, LAPS, session brokering) and which attacks each one defeats. |

## How to use these

1. After reading a module, open the matrix and find its rows. Cover the **Control** column and try to name the defense for each attack from memory.
2. Then cover the **Attack** column and, given a control (e.g. "gMSA"), name what it defeats. The exam and real interviews both ask it both ways.
3. Use the [pam-playbook.md](pam-playbook.md) to connect single controls to the *many* attacks they cover — that's how you compress 20 modules into a handful of load-bearing ideas.

> **Framing.** CEH is an offensive exam, but almost every question has a "best defense" flavor somewhere in the domain. If you can state the control, you can usually eliminate two wrong answers instantly. The PAM lens — *reduce standing privilege, broker and record access, rotate secrets, segment tiers* — is the single most reusable answer key across the whole blueprint.
