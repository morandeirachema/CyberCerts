# 04 — Recon & OSINT

> **What you'll learn:** the difference between passive and active reconnaissance (and why passive leaves no fingerprints), how to read WHOIS records, how to interrogate DNS every way there is (`dig`/`host`/`nslookup`), how to pull a zone transfer off the lab DC, how to discover subdomains and emails with OSINT tools, and how search engines and Shodan fit in — all without touching a system you don't own.
> **Prerequisites:** [03 — Networking basics](03-networking-basics.md). ⬅️ [Course index](README.md)

> **⚖️ Ethics first.** Everything internet-facing in this chapter uses **`example.com`** (a reserved documentation domain that's safe to name) and stands in for **a domain you actually own**. WHOIS, Google, Shodan, and theHarvester reach out to the *public internet* — only ever point them at your own assets. The **DNS and zone-transfer** commands target your isolated lab DC (`192.168.56.30`, zone `ceh.lab`). Recon on anyone else's infrastructure without written permission is a crime.

This chapter is the Kali-hands-on companion to **CEH [Module 02 — Footprinting & Reconnaissance](../modules/02-footprinting-and-reconnaissance/README.md)**. Read that for the exam theory; do the commands here.

---

## Passive vs active reconnaissance

**Reconnaissance** ("recon") is gathering information about a target *before* attacking it. There are two flavours, and the exam tests the line between them constantly:

| | Passive recon | Active recon |
|---|---|---|
| **Definition** | You learn about the target **without sending it any packets** | Your packets **reach the target's own infrastructure** |
| **Examples** | WHOIS, Google, Shodan's cached index, social media, cert-transparency logs | DNS zone transfer (AXFR), traceroute, ping, banner grabbing |
| **Stealth** | Invisible — nothing lands in the target's logs | Leaves traces the target can see and alert on |

The dividing question is simple: **did a packet touch the target?** Asking a public WHOIS server or Shodan's index is passive — you're querying a *third party's* copy of the data. Asking the target's *own* name server for a zone transfer is active — you knocked on their door.

> **The passive → active line.** Good tradecraft is to exhaust passive sources first (nobody can see you), then move to active probing only when you must. This chapter starts passive (WHOIS, OSINT) and ends active (DNS interrogation and AXFR against your lab DC). The very next chapter, [05 — Scanning with Nmap](05-nmap-scanning.md), is *fully* active.

## WHOIS — who owns a domain

**WHOIS** is a public directory of domain and IP registrations. It can leak the registrar, the registrant's name/org, contact emails, name servers, and creation/expiry dates — the seed data for everything else.

```bash
whois example.com          # domain registration details
```
You should see the **registrar**, **name servers** (`Name Server:` lines), and registration **dates**. Modern domains often show a privacy service instead of a real name — that redaction *is* the countermeasure working.

```bash
whois 93.184.216.34        # WHOIS on an IP -> which regional registry / netblock owns it
```
IP WHOIS tells you the **owning organisation** and the **regional registry**: ARIN (North America), RIPE (Europe/Middle East), APNIC (Asia-Pacific), LACNIC (Latin America), AFRINIC (Africa). Handy for finding an org's real IP ranges.

## DNS reconnaissance — the internet's address book

**DNS** (Domain Name System) turns names like `ceh.lab` into IP addresses. Each type of answer it stores is a **record**, and each record type leaks something different:

| Record | Meaning | Recon value |
|---|---|---|
| `A` / `AAAA` | Name → IPv4 / IPv6 address | Maps hosts to IPs |
| `NS` | Authoritative name servers | The servers to try AXFR against |
| `MX` | Mail exchangers | Mail infrastructure, phishing pretext |
| `SOA` | Zone authority + serial number | Primary DNS server, admin email |
| `TXT` | Free text (SPF/DKIM/DMARC, verifications) | Reveals third-party SaaS in use |
| `SRV` | Service locator (`_ldap`, `_kerberos`) | **Finds Active Directory / a domain controller** |
| `PTR` | IP → name (reverse lookup) | Internal naming conventions |

Kali ships three DNS query tools. `dig` is the powerful one, `host` is the quick one, `nslookup` is the classic (and works the same on Windows).

```bash
# --- dig: query the lab DC directly (the @ picks the server to ask) ---
dig @192.168.56.30 ceh.lab A +short      # just the IP(s); +short strips the noise
dig @192.168.56.30 ceh.lab NS +short     # authoritative name servers
dig @192.168.56.30 ceh.lab MX +short     # mail servers
dig @192.168.56.30 ceh.lab SOA           # zone serial + admin contact
dig @192.168.56.30 ceh.lab TXT           # SPF/DKIM/verification strings
dig @192.168.56.30 ceh.lab ANY           # ask for every record type at once
```
You should see the answers under an `;; ANSWER SECTION:`. Because you asked the DC *directly*, this is **light active recon** — the DC sees your query.

```bash
# --- SRV records: how attackers locate Active Directory with zero credentials ---
dig @192.168.56.30 _ldap._tcp.ceh.lab SRV +short
dig @192.168.56.30 _kerberos._tcp.ceh.lab SRV +short
```
You should see the DC's hostname and port (e.g. `389` for LDAP, `88` for Kerberos). Those two records alone announce "there is a domain controller here."

```bash
# --- reverse lookup (PTR): IP back to a name ---
dig @192.168.56.30 -x 192.168.56.30 +short
```

```bash
# --- host: the quick one ---
host ceh.lab 192.168.56.30            # default A/AAAA/MX lookup
host -t NS ceh.lab 192.168.56.30      # -t picks a record type
host -t SRV _ldap._tcp.ceh.lab 192.168.56.30
```

```bash
# --- nslookup: same idea, identical on Windows ---
nslookup -type=MX ceh.lab 192.168.56.30
nslookup -type=SRV _kerberos._tcp.ceh.lab 192.168.56.30
```

## Zone transfer (AXFR) — the classic misconfiguration

A **zone transfer (AXFR)** is meant to copy an entire DNS zone from a primary server to a backup secondary. If a name server is misconfigured to answer AXFR for *anyone*, it hands over **every record in the zone** — a complete internal map — in one request. CEH loves this as the "what did the attacker exploit?" answer.

```bash
dig @192.168.56.30 ceh.lab AXFR      # full zone dump if transfers are open
host -l ceh.lab 192.168.56.30        # same thing via host (-l = list zone)
```
If it's open, you should see **dozens of records** scroll past (every host in `ceh.lab`). If it's locked down you'll see `Transfer failed` or `; Transfer failed.` — that's the *fixed* state. The one-line server fix is to restrict transfers to listed secondaries only.

## Automated DNS enumeration — dnsrecon & dnsenum

Two tools wrap all of the above (record lookups, AXFR attempts, and subdomain brute-forcing) into one run.

```bash
dnsrecon -d ceh.lab -n 192.168.56.30 -a      # -n picks the name server, -a attempts AXFR
```
You should see it enumerate records and report whether the zone transfer succeeded.

```bash
dnsenum --dnsserver 192.168.56.30 ceh.lab    # records, AXFR, and a subdomain brute-force
```

If either isn't installed: `sudo apt install dnsrecon dnsenum`.

## Subdomain discovery — amass & sublist3r

Large orgs have dozens of subdomains (`mail.`, `vpn.`, `dev.`). Each is another way in. These tools find them from **passive sources** (certificate-transparency logs, search engines) — no packets to the target.

```bash
# amass — the thorough one. -passive keeps it 100% passive (no DNS resolution against the target)
amass enum -passive -d example.com

# sublist3r — lighter and faster, pulls from search engines and CT logs
sublist3r -d example.com
```
You should see a list of discovered subdomains. Install with `sudo apt install amass sublist3r` if needed. (Dropping `-passive` from `amass` makes it actively resolve names — that crosses into active recon, so save it for domains you own.)

## theHarvester — emails & subdomains from OSINT

**theHarvester** sweeps public search engines and data sources to collect **email addresses, subdomains, and hostnames** for a domain — great raw material for a social-engineering or phishing assessment. Run it **only against a domain you own**.

```bash
theHarvester -d example.com -b bing,duckduckgo,crtsh
```
- `-d` = the target domain, `-b` = which sources ("backends") to query.
- You should see harvested **emails** and **hosts** grouped at the end of the run.

## recon-ng — the modular OSINT framework

**recon-ng** looks and feels like Metasploit (chapter 09): a console where you load small **modules**, set options, and run them. It's the "framework" answer on the exam. Each module does one OSINT job and stores results in a shared database.

Launch it and load a module:

```bash
recon-ng
```
Then, at the `[recon-ng][default] >` prompt:

```text
marketplace search hackertarget            # find a module
marketplace install recon/domains-hosts/hackertarget   # install it
modules load recon/domains-hosts/hackertarget          # load it
options set SOURCE example.com             # tell it the target
run                                        # execute the module
show hosts                                 # view what it stored
```
The pattern to remember is **load → set options → run → show results**. Type `exit` to quit.

## Google dorking — search engines as a recon tool

**Google dorking** (a.k.a. Google hacking) means using advanced search **operators** to surface exposed files and pages the owner never meant to publish. It's passive — you're searching Google's index, not the target. Type these straight into the search box:

| Operator | Finds |
|---|---|
| `site:` | Pages on one domain — `site:example.com` |
| `filetype:` / `ext:` | Documents — `site:example.com filetype:pdf` |
| `inurl:` | Text in the URL — `inurl:admin site:example.com` |
| `intitle:` | Text in the page title — `intitle:"index of"` |
| `cache:` | Google's cached copy (extra-passive — never hits the site) |
| `-` (minus) | Excludes a term — `site:example.com -www` |

The curated catalogue of these is the **Google Hacking Database (GHDB)**. Keep queries scoped to your own `site:` — hunting other people's exposed files is out of bounds.

## Shodan — the search engine for devices

**Shodan** continuously scans the internet and indexes what it finds (open ports, banners, device types). Searching that **index is passive** — Shodan already did the scanning. Use https://www.shodan.io in the browser:

```text
hostname:example.com        # exposed services on your own domain
net:198.51.100.0/24         # a netblock you own
port:3389 org:"Your Org"    # find your own exposed RDP
```

> **The hard rule:** Shodan lets you *find* devices; it does not let you *touch* them. Search the index freely, but **never connect to a result you don't own** — clicking through to someone else's exposed camera or database is unauthorised access.

## Maltego — visual link analysis (worth knowing)

**Maltego** is a **GUI** (graphical, point-and-click) tool that turns OSINT into a **link-analysis graph** — you drop in a domain, email, or person and it draws the connections (subdomains → IPs → owners → emails). You won't script with it, but the exam wants you to know **Maltego = visual link analysis** as opposed to theHarvester (emails/subdomains) and recon-ng (modular framework). Launch it from the **Applications → Information Gathering** menu in Kali.

## Common beginner mistakes

- **Blurring passive and active.** WHOIS/Google/Shodan = passive; **zone transfer, traceroute, ping, banner grabbing = active**. One wrong verb flips an exam answer — and in real life, decides whether you were seen.
- **Confusing `SOA` and `NS`.** `SOA` holds the zone's serial and *primary* server; `NS` *lists* the authoritative servers. Don't swap them.
- **Pointing OSINT tools at someone else's domain.** theHarvester, amass (non-passive), Shodan, and dorks all reach real infrastructure or real people — your own assets only.
- **Forgetting `+short`.** Raw `dig` output is a wall of text; `+short` gives you just the answer for scripting and grepping.
- **Skipping recon to "get to the hacking."** Recon quality decides how efficient every later phase is. The engagement is won here.

## ✅ Practice task

1. **Passive:** run `whois example.com` and note the registrar, name servers, and whether privacy redaction is on.
2. **DNS map (lab):** against `192.168.56.30`, pull the `NS`, `MX`, `SOA`, and `TXT` records for `ceh.lab` with `dig`. Then grab the `_ldap._tcp.ceh.lab` and `_kerberos._tcp.ceh.lab` `SRV` records — those are how an attacker finds the domain controller with zero credentials.
3. **AXFR test (lab):** run `dig @192.168.56.30 ceh.lab AXFR`. If the whole zone dumps, you just proved the misconfiguration. (Bonus: disable transfers on the DC's DNS and re-run to confirm it now refuses.)
4. **Automate it:** run `dnsrecon -d ceh.lab -n 192.168.56.30 -a` and compare its findings to your manual `dig` results.
5. **OSINT:** run `theHarvester -d example.com -b duckduckgo,crtsh` and note how many subdomains and emails come back.

## Next

➡️ [05 — Scanning with Nmap](05-nmap-scanning.md): now that you know *what* exists, we move fully active — finding live hosts, open ports, and the services behind them.

## Sources

- CEH Module 02 — Footprinting & Reconnaissance: [`../modules/02-footprinting-and-reconnaissance/`](../modules/02-footprinting-and-reconnaissance/README.md)
- WHOIS (Kali Tools) — https://www.kali.org/tools/whois/
- ISC BIND — `dig` / DNS — https://www.isc.org/bind/
- dnsrecon — https://github.com/darkoperator/dnsrecon
- dnsenum (Kali Tools) — https://www.kali.org/tools/dnsenum/
- amass — https://github.com/owasp-amass/amass
- theHarvester — https://github.com/laramies/theHarvester
- recon-ng — https://github.com/lanmaster53/recon-ng
- Maltego — https://www.maltego.com/
- Shodan — https://www.shodan.io/
- Google Hacking Database — https://www.exploit-db.com/google-hacking-database
