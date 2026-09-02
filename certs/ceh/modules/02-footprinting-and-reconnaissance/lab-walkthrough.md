# Module 02 — Footprinting & Reconnaissance · Guided Lab Walkthrough

> Passive-first recon. Run WHOIS/OSINT only against **domains you own**, and DNS queries against **your lab DC** (`ceh.lab` @ `192.168.56.30`). Never connect to Shodan results. Each step: command, expected observation, a hint, and the defender/PAM takeaway. Outputs are **representative**. Pairs with [README.md](README.md) · [facts.md](facts.md).

**Goal:** practice the passive→active line — pull public data, enumerate DNS, attempt a zone transfer, then see how a defender shuts recon down.

---

## Part A — WHOIS and DNS records (passive → light active)

### A1. WHOIS (passive)
```bash
whois example.com          # a domain you own or a neutral example
```
**You should see** registrar, name servers, and creation/expiry dates. **Observe:** zero packets touched the target's own servers — this is third-party data.

### A2. Enumerate DNS record types against the lab DC
```bash
dig @192.168.56.30 ceh.lab ANY +noall +answer
dig @192.168.56.30 ceh.lab NS +short
dig @192.168.56.30 ceh.lab MX +short
dig @192.168.56.30 _ldap._tcp.ceh.lab SRV +short      # AD service locator
nslookup -type=SRV _kerberos._tcp.ceh.lab 192.168.56.30
```
**You should see** the zone's NS/MX and the AD **SRV** records that reveal domain controllers and services.

<details><summary>Hint</summary>`_ldap._tcp.dc._msdcs.ceh.lab` SRV records pinpoint DCs. SRV records are gold for mapping an AD environment before you ever scan.</details>

---

## Part B — Zone transfer attempt (the classic misconfig)
```bash
dig @192.168.56.30 ceh.lab AXFR
host -l ceh.lab 192.168.56.30
```
**You should see** either the **entire zone dumped** (transfers left open — a finding) or `Transfer failed` (properly restricted).
```
; Transfer failed.        <-- good: AXFR restricted
```
**Observe:** an open AXFR hands an attacker your whole internal namespace in one command.

**Defender/PAM view:** restrict zone transfers to authorized secondaries; this is basic DNS hygiene that removes a huge recon shortcut.

---

## Part C — OSINT tooling (your own domain only)
```bash
dnsrecon -d ceh.lab -n 192.168.56.30 -a         # -a attempts AXFR too
theHarvester -d example.com -b bing,crtsh,duckduckgo   # a domain you own
# Shodan: query the INDEX only — never connect to a result you don't own
shodan search 'org:"Your Own Org"'               # requires your own API key
```
**You should see** subdomains/hosts from dnsrecon and emails/hosts from theHarvester. **Observe:** how much surface is visible without ever probing the target directly.

<details><summary>Hint</summary>`crtsh` (Certificate Transparency logs) is a powerful passive subdomain source — certificates reveal hostnames orgs forgot were public.</details>

---

## Part D — Defender's view
- Disable/restrict **AXFR** → Part B fails.
- Scrub document **metadata** and remove exposed files → dorking yields less.
- **WHOIS privacy** and minimal DNS records → less OSINT.
- **Attack-surface monitoring** (and, for a PAM shop, **Accounts Discovery/DNA**) finds exposed assets and privileged/service accounts before attackers do.

## What you should conclude
| You did | The control that limits it |
|---|---|
| Pulled WHOIS/OSINT | Minimize public exposure, WHOIS privacy |
| Enumerated DNS + SRV | Split-horizon DNS, least public records |
| Attempted AXFR | Restrict zone transfers |
| Harvested emails/subdomains | Metadata scrubbing, awareness |

## Cleanup
Nothing persistent created. Remove any saved OSINT output you don't need.

## Record it
Note which records/AXFR result you saw in the **My lab log** table in [README.md](README.md); track weak areas in [PROGRESS.md](../../PROGRESS.md).
