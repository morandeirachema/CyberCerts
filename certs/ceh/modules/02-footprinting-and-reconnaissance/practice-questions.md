# Module 02 — Footprinting and Reconnaissance · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** An analyst runs a WHOIS lookup and browses Google's `cache:` of the target's site, but sends **no traffic** to the target's own servers. How is this classified?

- A. Active footprinting
- B. Passive footprinting
- C. Scanning
- D. Enumeration

<details><summary>Answer</summary>

**B. Passive footprinting.** No packet reaches the target's infrastructure — WHOIS queries a registry and `cache:` returns Google's stored copy. The dividing line the exam tests: *did a packet touch the target's own systems?* If not, it's passive. **Tell:** WHOIS, Google, Shodan, and cached pages are always passive.
</details>

---

**Q2.** Which activity is **active** footprinting?

- A. Querying a public WHOIS server
- B. Searching Shodan for the target's exposed services
- C. Requesting a DNS zone transfer from the target's name server
- D. Reading the target's LinkedIn page

<details><summary>Answer</summary>

**C. Zone transfer (AXFR).** You are asking the target's *own* name server to hand over its zone — a packet reaches their infrastructure. WHOIS, Shodan, and LinkedIn are all passive (third-party sources). **Also active:** traceroute, ping, and banner grabbing.
</details>

---

**Q3.** An attacker successfully runs `dig @ns.target.com target.com AXFR` and receives every A, MX, NS, and SRV record for the zone. What was exploited?

- A. A buffer overflow in BIND
- B. A DNS server configured to allow zone transfers to any host
- C. A poisoned resolver cache
- D. An expired TLS certificate

<details><summary>Answer</summary>

**B. An open zone transfer.** AXFR is meant to sync a primary to its listed **secondaries**; a server that answers *anyone* is misconfigured and dumps the entire internal DNS map in one request. **Fix:** restrict transfers to named secondary IPs (one line). This is CEH's favorite "what did the attacker exploit?" answer.
</details>

---

**Q4.** Which DNS record type most directly helps an attacker **locate a domain controller** with no credentials?

- A. MX
- B. PTR
- C. SRV
- D. TXT

<details><summary>Answer</summary>

**C. SRV.** Service-locator records like `_ldap._tcp` and `_kerberos._tcp` advertise where AD services live, pointing straight at the DC. MX names mail servers, PTR does reverse lookups, and TXT holds SPF/DKIM/verification strings. **PAM takeaway:** keep AD DNS internal-only so these never face the internet.
</details>

---

**Q5.** A record holds the zone's **serial number and the primary name server / admin email**. Which record is it?

- A. NS
- B. SOA
- C. CNAME
- D. A

<details><summary>Answer</summary>

**B. SOA (Start of Authority).** It carries the primary NS, the responsible-party email, the serial, and the refresh/retry/expire timers. **NS** lists the authoritative servers — a classic swap trap. **CNAME** is an alias; **A** maps a host to IPv4.
</details>

---

**Q6.** Which Google dork returns only **PDF files** hosted on `example.com`?

- A. `inurl:example.com pdf`
- B. `site:example.com filetype:pdf`
- C. `cache:example.com/*.pdf`
- D. `intitle:example.com filetype:pdf`

<details><summary>Answer</summary>

**B. `site:example.com filetype:pdf`.** `site:` scopes to one domain; `filetype:` (or `ext:`) restricts by document type — the standard combo for hunting exposed documents. `inurl:` matches URL text, `cache:` fetches a stored copy, and `intitle:` matches the page title.
</details>

---

**Q7.** Which operator finds pages whose **title** contains a phrase, useful for spotting exposed directory listings like `index of`?

- A. `inurl:`
- B. `intitle:`
- C. `site:`
- D. `link:`

<details><summary>Answer</summary>

**B. `intitle:`** matches text in the page `<title>` — e.g. `intitle:"index of" "backup"`, a GHDB pattern for exposed listings. `inurl:` matches the URL, `site:` scopes to a domain, and `link:` finds pages linking to a target. The curated catalog of these is the **Google Hacking Database (GHDB)**.
</details>

---

**Q8.** You need to find **internet-exposed devices** for a target by their service banners (e.g. `hostname:example.com`, `net:198.51.100.0/24`). Which engine is purpose-built for this?

- A. Maltego
- B. HTTrack
- C. Shodan
- D. Recon-ng

<details><summary>Answer</summary>

**C. Shodan** indexes internet-facing devices/services by banner and supports filters like `hostname:`, `net:`, `port:`, and `org:`. It is **passive** — you query Shodan's cache, not the target. **Censys** is the close cousin, adding TLS-certificate search. Maltego graphs relationships; HTTrack mirrors sites; Recon-ng is a module framework.
</details>

---

**Q9.** Which tool is designed to gather **emails, subdomains, and hostnames** from public OSINT sources?

- A. theHarvester
- B. HTTrack
- C. Wireshark
- D. Nikto

<details><summary>Answer</summary>

**A. theHarvester** pulls emails, subdomains, and hosts from search engines, certificate transparency, and other OSINT feeds. HTTrack mirrors websites, Wireshark sniffs traffic, and Nikto scans web servers. **Tool→role pairing is heavily tested — memorize it.**
</details>

---

**Q10.** A pentester builds a visual **link-analysis graph** connecting a company's domains, people, and email addresses. Which tool fits?

- A. Recon-ng
- B. Maltego
- C. dnsrecon
- D. Censys

<details><summary>Answer</summary>

**B. Maltego** specializes in graphing entities and their relationships (transforms). **Recon-ng** is a *modular framework* for OSINT collection, **dnsrecon** automates DNS enumeration, and **Censys** searches hosts/certs. Don't confuse the graphing tool (Maltego) with the framework (Recon-ng).
</details>

---

**Q11.** Why do attackers use **HTTrack** to mirror a site offline instead of browsing it live?

- A. It bypasses authentication automatically
- B. It lets them study source, comments, and paths without repeatedly hitting the live server
- C. It decrypts HTTPS traffic
- D. It is the only way to view HTML source

<details><summary>Answer</summary>

**B.** A local mirror means you can hunt HTML comments, internal paths, and email addresses in the source **without hammering the live site** — a stealth and efficiency motive. It neither bypasses auth nor decrypts TLS, and any browser can view source.
</details>

---

**Q12.** Which **regional internet registry** would you query for IP allocation data covering **Europe and the Middle East**?

- A. ARIN
- B. APNIC
- C. RIPE NCC
- D. LACNIC

<details><summary>Answer</summary>

**C. RIPE NCC.** Match registry to region: **ARIN** (North America), **RIPE NCC** (Europe/Middle East), **APNIC** (Asia-Pacific), **LACNIC** (Latin America), **AFRINIC** (Africa). Expect a "which registry serves region X" item.
</details>

---

**Q13.** An attacker embeds a **tracking pixel** in an email to the target. What does this reveal?

- A. The recipient's password
- B. When the mail was opened and the reader's approximate IP/location
- C. The mail server's private key
- D. The domain's zone file

<details><summary>Answer</summary>

**B.** An email tracking pixel / web-bug fires when the message is opened, leaking the **open time and the reader's IP/approximate location** (and sometimes client info). It's an *active* recon technique. Reading the mail **headers** separately traces the delivery path and originating servers.
</details>

---

**Q14.** A defender wants to stop attackers from copying the **entire internal DNS zone**. Which control is most direct?

- A. Enforce HSTS on the web server
- B. Restrict zone transfers to listed secondary name servers
- C. Rotate the TLS certificate
- D. Enable account lockout

<details><summary>Answer</summary>

**B. Restrict zone transfers** to the named secondary IPs (and prefer split-horizon / internal-only DNS for AD). That single change turns an open AXFR into a refusal. HSTS, cert rotation, and lockout address unrelated risks. **Verify by re-running `dig ... AXFR` and confirming a refusal.**
</details>

---

**Q15.** Which pairing is **correct**?

- A. `cache:` is active; a live page fetch is passive
- B. WHOIS is active; zone transfer is passive
- C. Shodan is passive; traceroute is active
- D. Ping is passive; Censys is active

<details><summary>Answer</summary>

**C. Shodan is passive; traceroute is active.** Shodan queries a third-party cache (passive); traceroute sends packets toward the target (active). `cache:` is passive and a live fetch is active (A is reversed); WHOIS is passive and AXFR is active (B is reversed); ping is active and Censys is passive (D is reversed).
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the DNS record types and passive-vs-active sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
