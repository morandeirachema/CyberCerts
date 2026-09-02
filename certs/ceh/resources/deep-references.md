# Deep Technical References

Where to go *past* exam-concept depth into real tradecraft. These are the community-standard, well-known technical references — use them to turn "I recognize this attack" into "I can execute and defend it." Practice only against your own [lab](../labs/README.md) or authorized targets.

> The module `README.md` **Sources** sections link topic-specific pages; this is the master index of the canon.

## The canon (bookmark all of these)

| Reference | Use it for | Link |
|---|---|---|
| **HackTricks** | The single best hands-on methodology wiki — per-port, per-service, per-privesc | https://book.hacktricks.xyz/ |
| **PayloadsAllTheThings** | Copy-adaptable payloads for every web/injection/AD attack | https://github.com/swisskyrepo/PayloadsAllTheThings |
| **The Hacker Recipes** | Clear, correct AD/Kerberos/NTLM attack reference | https://www.thehacker.recipes/ |
| **GTFOBins** | Unix binaries abused for privesc / bypass | https://gtfobins.github.io/ |
| **LOLBAS** | Windows living-off-the-land binaries/scripts | https://lolbas-project.github.io/ |
| **PortSwigger Web Security Academy** | Free, hands-on web-app labs (best-in-class) | https://portswigger.net/web-security |
| **OWASP Cheat Sheet Series** | Authoritative defensive guidance per vuln class | https://cheatsheetseries.owasp.org/ |
| **MITRE ATT&CK** | Tactics/techniques taxonomy + detections | https://attack.mitre.org/ |
| **MITRE ATLAS** | Adversarial-ML equivalent of ATT&CK | https://atlas.mitre.org/ |
| **Atomic Red Team** | Runnable tests that emit the telemetry you learn to detect | https://github.com/redcanaryco/atomic-red-team |

## By domain

**Active Directory / identity (Modules 04, 06)**
- The Hacker Recipes — AD: https://www.thehacker.recipes/ad/
- SpecterOps *Certified Pre-Owned* (ADCS ESC1–8): https://posts.specterops.io/certified-pre-owned-d95910965cd2
- BloodHound (attack-path mapping): https://bloodhound.readthedocs.io/
- Impacket (secretsdump, GetUserSPNs, ntlmrelayx): https://github.com/fortra/impacket
- Certipy (ADCS abuse & audit): https://github.com/ly4k/Certipy
- Microsoft — Securing privileged access: https://learn.microsoft.com/en-us/security/privileged-access-workstations/overview

**Web (Modules 13, 14, 15)**
- PortSwigger Academy + Web Security Testing Guide (WSTG): https://owasp.org/www-project-web-security-testing-guide/
- OWASP Top 10 / API Top 10: https://owasp.org/Top10/ · https://owasp.org/API-Security/

**Exploitation / privesc (Module 06)**
- GTFOBins · LOLBAS (above)
- PEASS-ng (linpeas/winpeas privesc scanners): https://github.com/peass-ng/PEASS-ng
- Exploit-DB / searchsploit: https://www.exploit-db.com/

**Cloud / container (Module 19)**
- HackTricks Cloud: https://cloud.hacktricks.xyz/
- Kubernetes hardening (NSA/CISA): https://media.defense.gov/2022/Aug/29/2003066362/-1/-1/0/CTR_KUBERNETES_HARDENING_GUIDANCE_1.2_20220829.PDF

**Detection engineering (defender lens)**
- Sigma rules: https://github.com/SigmaHQ/sigma
- Atomic Red Team (above) · MITRE ATT&CK Data Sources: https://attack.mitre.org/datasources/

**Practice ranges (safe, authorized)**
- Hack The Box: https://www.hackthebox.com/ · TryHackMe: https://tryhackme.com/
- VulnHub (downloadable VMs): https://www.vulnhub.com/

> **How to use these with this repo:** finish a module → run its [lab-walkthrough](../modules/README.md) → then open the matching HackTricks / Hacker Recipes page and go one level deeper on the same target. The repo gives you the map and the "why"; these give you the full tradecraft.
