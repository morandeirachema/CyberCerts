# The CEH Practice Kit — what to practise with, and when

Everything you need to *do* CEH rather than read it, in the order the
[12-week plan](../STUDY-PLAN.md) uses it: the repo's own lab and drills first (free, offline,
already wired to the modules), then the external platforms that add targets the lab cannot.
All of it is legal, authorised practice — **never practise on anything outside these
environments or your own lab** ([legal & ethics](../00-overview/legal-and-ethics.md)).

> 🧪 **See also:** [labs/practice-ranges.md](../labs/practice-ranges.md) for the sourced
> description of each online range, and the repo-wide [platforms](../../../learning/platforms.md)
> list for every stage of the path.

## 1. In this repo (start here — free, offline)

| Practise… | With | Covers |
|-----------|------|--------|
| **Tool fluency** (terminal, nmap, enumeration, Metasploit, passwords, AD, sniffing, wireless) | [Kali course](../kali/README.md) chapters 00–15 · [cheatsheets/](../cheatsheets/README.md) | Every module's commands |
| **Web targets** | Docker lab ([labs/README.md](../labs/README.md)): DVWA, OWASP Juice Shop, WebGoat, bWAPP — `certs/ceh/labs/scripts/setup.sh` | Modules 13, 14, 15 |
| **Network targets** | Vagrant layer: Kali attacker + Metasploitable2 on a host-only network ([vagrant/README.md](../labs/vagrant/README.md)) | Modules 02–08, 10–12 |
| **Active Directory** | Ansible AD lab with a tiered-admin model ([ansible/README.md](../labs/ansible/README.md)) | Modules 04, 06; the identity attack paths |
| **The full attack chain** | [Capstone](../labs/capstone.md): recon → Kerberoast → delegation → ADCS → DCSync, then re-run with the fixes | Modules 03–06 end-to-end |
| **Detecting your own attack** | [Blue-team lab](../labs/blue-team-lab.md) | The Defender & PAM lens |
| **Module-by-module hands-on** | Each `modules/NN-*/lab-walkthrough.md` ([modules/](../modules/README.md)) with a lab-log table to fill | All 20 |
| **Practical-style tasks under time** | [practical/drills/](../practical/drills/README.md) (9 domain packs) · [challenge lab](../practical/challenge-lab/README.md) generates stego / pcap / crypto / hash / archive challenges · [challenge playbooks](../practical/challenge-playbooks.md) | CEH Practical |
| **Dress rehearsal** | [Simulated Practical exams](../practical/exams/README.md): 20 challenges, 6 hours, answer key | CEH Practical |
| **OT / ICS targets** | [OT lab](../labs/ot/README.md) | Module 18 |
| **Recall** | `python3 scripts/quiz.py --module 06` (terminal flashcards, re-drills misses) · `python3 scripts/build_anki.py` (Anki deck) — [scripts/](../scripts/README.md) | All 20 |
| **Exam-style questions** | Per-module `practice-questions.md` · [concept-track questions](../exam-prep/practice-questions.md) · [50-question mock](../MOCK-EXAM.md) · [125-question timed mock](../MOCK-EXAM-FULL.md) · [200-question rapid-fire bank](../RAPID-FIRE.md) | Knowledge exam |

## 2. External platforms, by what they add

| Platform | Cost | Use it for | Modules |
|----------|------|-----------|---------|
| **EC-Council iLabs · CEH Engage · CEH Compete** — https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh/ | Paid (part of the CEH program; verify what your bundle includes) | The official range aligned to the curriculum; Engage is a four-phase mock engagement; Compete is monthly CTFs. The closest thing to the Practical's environment. | All; Practical |
| **PortSwigger Web Security Academy** — https://portswigger.net/web-security | Free | Best-in-class interactive web labs: injection, XSS, auth, access control, SSRF. Do the apprentice and practitioner labs for the web modules. | 13, 14, 15 |
| **TryHackMe** — https://tryhackme.com/ | Free tier + subscription | Guided rooms and learning paths; good for the unfamiliar attacker-side topics (OSINT, privilege escalation, AD basics) and for a gentle start if Kali is new. | 02–06, 09 |
| **Hack The Box** and **HTB Academy** — https://www.hackthebox.com/ | Free tier + subscription | Realistic boxes once the lab feels easy; Academy modules for structured enumeration, web and AD depth. | 03–06, 13–15 |
| **VulnHub** — https://www.vulnhub.com/ | Free | Downloadable vulnerable VMs to add to your own hypervisor when Metasploitable is exhausted. | 03–06 |
| **OverTheWire (Bandit → Natas)** — https://overthewire.org/wargames/ | Free | Command-line and web fundamentals through progressive SSH challenges; ideal before the Kali course if the terminal is new. | Foundations |
| **picoCTF** — https://picoctf.org/ | Free | CTF-style puzzles: crypto, forensics, stego, web — the same task types the Practical uses. | 07, 20; Practical |
| **LetsDefend** — https://letsdefend.io/ · **CyberDefenders** — https://cyberdefenders.org/ | Free tier + subscription | Blue-team cross-training: read the telemetry the attacks produce. Pairs with the blue-team lab and your PAM background. | Defender lens; 12 |
| **MITRE ATT&CK Navigator** — https://mitre-attack.github.io/attack-navigator/ | Free | Map every technique you practise to its ID and the control that stops it. | All |

## 3. Week by week (matches the plan)

| Plan weeks | Practise with |
|------------|---------------|
| 0 | Lab up (`setup.sh`, `vagrant up`); OverTheWire Bandit if the terminal is new; Kali chapters 00–05 |
| 1–2 (recon, scanning, enumeration) | Metasploitable2 from Kali; TryHackMe recon rooms; drill pack [01](../practical/drills/01-recon-scanning.md) and [02](../practical/drills/02-enumeration.md) |
| 3 (vuln analysis, system hacking) | AD lab up; first capstone run; drill packs [04](../practical/drills/04-passwords-and-hashes.md), [05](../practical/drills/05-active-directory.md), [09](../practical/drills/09-exploitation-privesc.md) |
| 4–6 (malware, sniffing, social engineering, DoS, hijacking, evasion) | Lab-segment captures; drill pack [06](../practical/drills/06-pcap-forensics.md); blue-team lab: detect the Week 3 capstone |
| 7–8 (web servers, web apps, SQLi) | DVWA, Juice Shop, WebGoat, bWAPP; PortSwigger apprentice + practitioner labs; drill pack [03](../practical/drills/03-web-and-sqli.md) |
| 9 (wireless, mobile) | Your own access point only; drill pack [07](../practical/drills/07-wireless.md); an Android emulator |
| 10–11 (IoT/OT, cloud, crypto, AI) | OT lab; a free-tier cloud account you own; challenge lab for hashes, stego and crypto; drill pack [08](../practical/drills/08-stego-and-crypto.md) |
| 12 (review) | 50-question mock, 125-question timed mock, rapid-fire bank; second capstone run with fixes applied |
| 13–14 (Practical, optional) | All drill packs under time; Simulated Practical exams 01 and 02; EC-Council iLabs / Engage if your bundle includes them |

## 4. Exam-style question practice

Prefer sources that **teach** (an explanation per answer) and confirm they target CEH v13.
The banks in this repo are original and mapped to the modules; track every score and every
miss in [PROGRESS.md](../PROGRESS.md). Braindump sites that sell real exam items violate the
EC-Council Candidate Agreement and can get a certification revoked — this repo does not link
to them.

> If a platform ever asks you to attack a target outside its own scope, stop — that is the
> line between practice and a crime.
