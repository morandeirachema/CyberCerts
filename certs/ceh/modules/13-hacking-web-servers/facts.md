# Module 13 — Hacking Web Servers · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## Web server vs web application (know the boundary)
This module = the **server layer**: the HTTP daemon, its OS, config, and patch level. The **app code** (XSS, SQLi, auth logic) is **Module 14**. CEH separates them deliberately. Nearly every finding here is a **hardening, patching, or least-privilege** gap — not a code bug.

## The web-server stack — where each attack lands
| Layer | Example | Attack that lands here |
|---|---|---|
| Document root | `/var/www`, `wwwroot` | Default pages, WebDAV upload, directory listing |
| Modules / handlers | PHP, CGI, .NET | Misconfig, source-code disclosure |
| Service account | `www-data`, IIS **AppPool** | Privilege boundary — a webshell inherits *this* |
| OS / patch level | kernel, daemon CVEs | Unpatched known vulnerabilities |
| DB / config backend | connection strings | Secrets in web root, creds in config |

## Attack taxonomy (classic exam table)
| Attack | Abuses | Tell |
|---|---|---|
| **Directory / path traversal** | `../../` to escape doc root | `GET /../../etc/passwd`, encoded `%2e%2e%2f` |
| **Misconfiguration** | Listing, verbose errors, samples | `/manager`, `/phpinfo.php`, stack traces |
| **Default creds / pages** | Shipped logins & content | Tomcat `tomcat:tomcat`, admin defaults |
| **HTTP response splitting** | CRLF (`%0d%0a`) into a header | Forged 2nd response → cache poison / XSS |
| **Web cache poisoning** | Shared cache stores attacker content | Unkeyed header reflected + cached |
| **WebDAV abuse** | Writable `PUT`/`MOVE` | Upload a webshell to a DAV dir |
| **Source-code disclosure** | Raw script returned, not run | `.php~`, `.bak`, `::$DATA` |
| **Patch-management failure** | Known unpatched CVE | Version banner → public exploit |
| **DoS / DDoS** | Exhaust connections/CPU/bw | Slowloris, flood, resource starvation |

Related: **HTTP request smuggling** (front/back-end desync) · **XST** (Cross-Site Tracing via `TRACE`) · **directory brute forcing** (guessing existing paths — *not* traversal).

## HTTP methods to watch
- **`PUT` / `DELETE`** → upload/delete files (WebDAV) → webshell path.
- **`TRACE`** → **XST**, reads cookies/headers even with HttpOnly → **disable it**.
- **`OPTIONS`** → lists enabled methods (recon).
- `curl -X OPTIONS -i <url>` reveals the `Allow:` set.

## Fingerprinting / banner grabbing
- **Banner grab** = read `Server:` / `X-Powered-By:` response headers (`curl -I`). Can be masked.
- **Behavioral fingerprint** = header order, error wording, method handling (httprint idea).
- **Automated**: `whatweb`, nmap `http-server-header` / `http-headers` NSE.
- **Banner suppression is obscurity, not a control** — patching is the control.

## EC-Council web-server hacking methodology (in order)
**Information gathering → Web-server footprinting → Mirror the site → Vulnerability scanning → Session hijacking → Password cracking.**

## Tool → job (match them, don't swap)
| Tool | Job |
|---|---|
| **Nikto** | Known-issue / misconfig scan (loud, not stealthy) |
| **nmap `http-*` NSE** | Enumeration (`http-methods`, `http-headers`, `http-enum`, `http-webdav-scan`) |
| **gobuster / dirb / ffuf** | Content discovery (find hidden admin/backup paths) |
| **whatweb** | Tech-stack fingerprint |
| **wpscan** | WordPress-specific enumeration (users, plugins, versions) |
| **davtest / cadaver** | Probe & abuse WebDAV `PUT` |
| **Metasploit** | Exploit modules for known server CVEs |

## Countermeasures (favorite answers)
- **Patch cadence + accurate inventory** — the real fix for known-vuln findings.
- **Remove default samples/pages** and change/vault default admin creds.
- **Least-privilege service account** (never root/SYSTEM) so a webshell inherits almost nothing.
- **Disable WebDAV & unused methods** (`TRACE`, `PUT`); read-only doc root.
- **No secrets in the web root**; block dotfiles/backups; **FIM** on the doc root.
- Canonicalize/validate paths + WAF for traversal.

## The one-line PAM answer key
- Hardcoded app-pool / service creds → **deliver at runtime via CCP/AAM** (no static secret to steal).
- Secrets in `web.config` / files → **centralize & rotate in Conjur**.
- Over-privileged web service account → **CPM-managed least-privilege service identity**, rotated.
- Compromised web server → with CCP at runtime, a leaked config yields **no reusable static secret**.
- Uploaded webshell → **FIM on doc root** trips the alert; least-privilege account contains it.

## Top traps
- **Web server (Module 13) vs web application (Module 14)** — server/config/patch vs app code.
- **Directory traversal** (read files outside doc root) ≠ **directory brute forcing** (guess existing paths).
- **HTTP response splitting** = CRLF into a **response header** ≠ **request smuggling** (front/back-end desync).
- **XST** abuses **`TRACE`**; mitigation is simply disabling `TRACE`.
- **Banner suppression ≠ patching** — it's obscurity, not a control.
- **Nikto** = misconfig scan; **gobuster/ffuf** = content discovery; **whatweb** = fingerprint. Match tool→job.
- A webshell runs as the **service account** (`www-data`/AppPool), not root — that boundary is the point of least privilege.
