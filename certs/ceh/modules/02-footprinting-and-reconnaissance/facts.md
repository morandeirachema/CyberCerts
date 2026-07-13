# Module 02 — Footprinting and Reconnaissance · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The one line that decides the answer
**Passive = no packet touches the target's own infrastructure. Active = a packet does.** WHOIS, Google, Shodan, Censys, and cached pages are passive; DNS **zone transfer**, traceroute, ping, banner grabbing, and email tracing are active. One verb flips the answer.

## Footprinting types (what you are building)
| Type | Example data | Feeds |
|---|---|---|
| Network | IP ranges, ASN, netblocks, name servers | Scanning scope |
| DNS | A/MX/NS/TXT/SRV records, subdomains | Host discovery |
| System | OS hints, tech stack, banners | Vuln analysis |
| Org / People | Employees, emails, roles | Social engineering |
| Website | Directory tree, comments, metadata | Web attacks |
| Email | Header trails, recipient location | Tracking / phishing |
| Competitive intel | Products, finances, partners | Business context |

## WHOIS & regional registries
- WHOIS returns **registrar, registrant, admin/tech contacts, name servers, and registration/expiry dates** — all passive.
- **Match registry to region:** ARIN (North America), RIPE NCC (Europe/Middle East), APNIC (Asia-Pacific), LACNIC (Latin America), AFRINIC (Africa).
- Registrar **privacy/redaction** hides contact data — the countermeasure to WHOIS harvesting.

## DNS record types the exam expects
| Record | Purpose | Recon value |
|---|---|---|
| A / AAAA | Hostname → IPv4 / IPv6 | Map hosts |
| NS | Authoritative name servers | Find AXFR targets |
| MX | Mail exchangers | Mail infra, phishing pretext |
| SOA | Zone authority + serial | Primary DNS, admin email |
| CNAME | Alias | Cloud/SaaS fingerprints |
| TXT | SPF/DKIM/DMARC, verification | Third-party services in use |
| SRV | Service locator (`_ldap`, `_kerberos`) | **AD discovery** |
| PTR | IP → hostname (reverse) | Internal naming schemes |

## Zone transfer (AXFR)
A **zone transfer** copies an **entire** DNS zone from primary to secondary. If a name server answers AXFR to *anyone*, it hands over every record — a full internal map. It is a **misconfiguration** and the classic "what did the attacker exploit?" answer. A normal query returns **one** record; AXFR returns the **whole zone**.

## Google Dorking operators (memorize)
| Operator | Finds |
|---|---|
| `site:` | Pages on one domain |
| `filetype:` / `ext:` | Documents (pdf, xlsx, conf, bak) |
| `intitle:` / `allintitle:` | Text in the page title |
| `inurl:` / `allinurl:` | Text in the URL |
| `cache:` | Google's cached copy (passive) |
| `link:` / `related:` | Linked / similar sites |
| `-term` | Exclude a term |

The **Google Hacking Database (GHDB)** on Exploit-DB is the curated catalog of these dorks.

## Search-engine device intel
- **Shodan** — searches internet-**exposed devices/services** by banner (`hostname:`, `net:`, `port:`, `org:`). Passive — you query Shodan's cache, not the target.
- **Censys** — internet host + **TLS certificate** search; great for cert-transparency and asset discovery. Also passive.

## Tool → purpose (know the pairing)
| Tool | Role |
|---|---|
| **theHarvester** | Emails / subdomains / hosts from OSINT sources |
| **Recon-ng** | Modular OSINT **framework** (marketplace of modules) |
| **Maltego** | **Link-analysis / graphing** of entities and relationships |
| **HTTrack** | **Offline website mirroring** for local analysis |
| **dnsrecon / dnsenum** | Automated DNS enumeration + AXFR attempt |
| **whois / dig / nslookup** | Registrar lookup / DNS record queries |

## Other techniques
- **Email tracking:** read-receipts and tracking pixels/web-bugs reveal when/where a mail was opened and the reader's IP; mail **headers** trace the delivery path and originating servers.
- **Website mirroring (HTTrack):** pulls a full offline copy so you hunt HTML comments, internal paths, and emails **without hammering the live site** — a stealth/efficiency motive, not just convenience.
- **Social-media / OSINT:** LinkedIn/job posts leak tech stack, org charts, and email formats; feed employee names + email pattern into phishing pretexts.

## Countermeasures
- Registrar **privacy/redaction**; role-based generic contacts, not personal admins.
- **Disable/restrict zone transfers** to listed secondaries; **split-horizon** (internal-only) DNS so AD `_ldap`/`_kerberos` SRV records never face the internet.
- Remove **index-of** listings, scrub document **metadata**, `robots`/auth on sensitive dirs.
- Minimize the public footprint; **monitor certificate-transparency** logs and your own presence in Shodan/Censys.
- Security-awareness + generic role mailboxes to blunt email/employee harvesting.

## PAM angle
Footprinting is the attacker doing **your asset inventory for you.** The single worst leak for a PAM environment is a **public SRV/AXFR trail pointing straight at Tier 0** — keep AD DNS internal-only, scrub service-account secrets from public repos/docs, then **discover and vault** every privileged identity before an attacker OSINTs it first.

## Top traps
- **Passive vs. active** is the #1 trap: zone transfer / traceroute / ping / banner grab = **active**; WHOIS / Google / Shodan / `cache:` = **passive**.
- **AXFR = whole zone**; a normal DNS query = one record. AXFR is the *misconfiguration* answer.
- **SOA** holds the serial + primary NS; **NS** lists authoritative servers — don't swap them.
- **theHarvester** = emails/subdomains; **Maltego** = graphs; **Recon-ng** = framework. Don't mix the roles.
- `cache:` is passive (Google's copy); fetching the **live** page is active.
- Match the **registry to its region** (ARIN/RIPE/APNIC/LACNIC/AFRINIC).
