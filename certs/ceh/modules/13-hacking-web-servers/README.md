# Module 13 — Hacking Web Servers

> **One-liner:** attacking the *server* that serves the app — the HTTP daemon, its OS, its config, and its patch level — not (yet) the application code. For a sysadmin this is the most familiar module: nearly every finding is a hardening, patching, or least-privilege gap you would remediate in production.

## Exam focus

- **Web server architecture**: the stack (OS → HTTP server → app runtime → database → document root) and where each attack lands.
- **Attack classes**: directory/path traversal, misconfiguration, default creds/pages/samples, HTTP response splitting, web cache poisoning, WebDAV abuse, source-code disclosure, patch-management failure, DoS.
- **Server fingerprinting / banner grabbing** and the tools that do it.
- The EC-Council **web-server hacking methodology** (info-gather → footprint → mirror → vuln-scan → exploit).
- Tool → purpose: Nikto (misconfig), gobuster/dirb/ffuf (content discovery), whatweb (fingerprint), nmap `http-*` NSE (enumeration).
- **Countermeasures** — patch cadence, remove defaults/samples, least-privilege service account, disable risky HTTP methods.

## Key concepts

### Web server stack — where attacks land

```
        ┌──────────────────────────────────────────────────────────┐
Client ─┼─▶ HTTP/S  ▶  ┌──────────────────────────────────────────┐ │
        │             │ Web server (Apache / Nginx / IIS)          │ │  ← banner, methods,
        │             │  ├─ document root  (/var/www, wwwroot)     │ │    default pages, WebDAV
        │             │  ├─ modules / handlers (PHP, CGI, .NET)    │ │  ← misconfig, source disclosure
        │             │  └─ runs as service acct (www-data/AppPool)│ │  ← privilege boundary
        │             └──────────────────────────────────────────┘ │
        │                     │                                    │
        │             ┌───────▼────────┐   ┌──────────────────┐    │
        │             │ App / scripts  │──▶│ Database backend │    │  ← creds in config,
        │             └────────────────┘   └──────────────────┘    │    secrets in web root
        │                     │                                    │
        │             ┌───────▼────────┐                           │
        │             │ Operating system / patch level │           │  ← unpatched CVEs, kernel
        │             └────────────────┘                           │
        └──────────────────────────────────────────────────────────┘
```

### Attack taxonomy (classic exam table)

| Attack | What it abuses | Typical evidence |
|---|---|---|
| **Directory / path traversal** | `../../` sequences to escape the doc root | `GET /../../etc/passwd`, encoded `%2e%2e%2f` |
| **Misconfiguration** | Directory listing, verbose errors, sample apps | Exposed `/manager`, `/phpinfo.php`, stack traces |
| **Default credentials / pages** | Shipped admin logins & default content | Tomcat `tomcat:tomcat`, router/admin defaults |
| **HTTP response splitting** | CRLF (`%0d%0a`) injected into a response header | Forged second header/response → cache poison, XSS |
| **Web cache poisoning** | Trick a shared cache into storing attacker content | Unkeyed header reflected + cached |
| **WebDAV abuse** | Writable `PUT`/`MOVE` methods | Upload a webshell to a DAV-enabled dir |
| **Source-code disclosure** | Server returns raw script instead of executing | `.php~`, `.bak`, `::$DATA`, handler misconfig |
| **Patch-management failure** | Known, published vulnerabilities left unpatched | Version banner → matching public exploit |
| **DoS / DDoS** | Exhaust connections/CPU/bandwidth | Slowloris-style, flood, resource starvation |

Related: **HTTP request smuggling** (front-end/back-end desync), **XST** (Cross-Site Tracing via the `TRACE` method), and **directory brute forcing** to find hidden admin/backup paths.

### Fingerprinting the server

- **Banner grabbing** — the `Server:` and `X-Powered-By:` response headers (`curl -I`), though these can be masked.
- **Behavioral fingerprinting** — header order, error-page wording, method handling (the classic "httprint" idea).
- **Automated** — `whatweb`, nmap `http-server-header` / `http-headers` NSE.

### EC-Council web-server hacking methodology

```
Information    Web server     Mirror the     Vulnerability    Session      Password
gathering  ──▶ footprinting──▶ website     ──▶ scanning    ──▶ hijacking ──▶ cracking
(WHOIS,DNS)    (banner,ports)  (offline copy) (Nikto,NSE)     (if any)     (admin panels)
```

## Key tools

| Tool | Purpose | Reference |
|---|---|---|
| Nikto | Web server misconfig / known-issue scanner | https://github.com/sullo/nikto |
| gobuster | Fast directory/file & DNS brute forcing | https://github.com/OJ/gobuster |
| dirb | Classic recursive content discovery | https://github.com/v0re/dirb |
| ffuf | Flexible fuzzer for content discovery | https://github.com/ffuf/ffuf |
| whatweb | Web technology fingerprinter | https://github.com/urbanadventurer/WhatWeb |
| nmap `http-*` NSE | Enumeration scripts (enum, methods, headers) | https://nmap.org/nsedoc/categories/discovery.html |
| Metasploit | Exploit modules for known server CVEs | https://docs.metasploit.com/ |

## Commands & techniques (lab-ready)

> Targets: **Metasploitable2** (`192.168.56.20`, real Apache with WebDAV/phpMyAdmin/TWiki) and the **DVWA** host (`localhost:8081`). Lab only. See [`../../labs/`](../../labs/).

```bash
# --- Fingerprint & banner grab ---
nmap -sV -p80,443 192.168.56.20                 # service/version detection
curl -sI http://192.168.56.20                   # raw response headers (Server:)
whatweb http://192.168.56.20                    # tech stack fingerprint

# --- nmap http NSE enumeration ---
nmap -p80 --script http-headers,http-methods,http-title,http-enum 192.168.56.20
nmap -p80 --script http-webdav-scan 192.168.56.20     # is WebDAV/PUT enabled?

# --- Misconfiguration & known-issue scan ---
nikto -h http://192.168.56.20                   # default files, dangerous methods, headers
nikto -h http://localhost:8081                  # DVWA host

# --- Content discovery (find hidden admin/backup paths) ---
gobuster dir -u http://192.168.56.20 -w /usr/share/wordlists/dirb/common.txt -x php,bak,old
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
     -u http://192.168.56.20/FUZZ -mc 200,301,302,403

# --- WebDAV: test which methods are writable, then a shell upload path ---
davtest -url http://192.168.56.20/dav/          # probes PUT/MOVE/exec per extension
# cadaver http://192.168.56.20/dav/             # interactive DAV client (PUT webshell)

# --- Path traversal probe (encoded ../) ---
curl -s "http://192.168.56.20/mutillidae/index.php?page=../../../../etc/passwd"

# --- Enabled HTTP methods (TRACE = XST risk, PUT/DELETE = upload/delete) ---
curl -s -X OPTIONS -i http://192.168.56.20
```

## Lab exercise

1. **Fingerprint first.** Run `whatweb`, `curl -I`, and `nmap -sV` against `192.168.56.20`. Record the exact server/version banner — this is the "patch-management" starting point (map the version to publicly documented issues; do **not** guess CVE numbers, look them up).
2. **Find the misconfigs.** Run Nikto against both targets and triage: default files, directory listing, dangerous methods (`PUT`, `TRACE`), missing security headers.
3. **Brute the tree.** Use gobuster with `-x php,bak,old` to hunt backup/source files (`config.php.bak` style source disclosure) and hidden admin panels.
4. **WebDAV path (Metasploitable2).** Confirm `/dav/` accepts `PUT` with `davtest`, then reason through how an attacker turns a writable DAV dir into code execution via an uploaded script.
5. **Fix it like a sysadmin.** For one finding, write the remediation: patch, disable the module/method, remove the sample app, or drop the service account's privileges.

**What you should observe:** almost every web-server finding is a **configuration or patch** problem, not a code bug — which is exactly why this module maps so cleanly onto standard hardening and change control.

## Defender & PAM mapping

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Path/directory traversal | `../`, `%2e%2e`, `/etc/passwd` in URI logs; WAF hits | Canonicalize/validate paths; run web root on its own mount; WAF |
| Default creds / pages / samples | Access to `/manager`, `/phpinfo`, sample apps | Remove samples on deploy; **change/vault default admin creds**; no shipped logins |
| Misconfiguration (listing, verbose errors) | Directory-index responses, stack traces in logs | Hardening baseline (CIS), disable listing, generic error pages |
| WebDAV upload / risky methods | `PUT`/`MOVE`/`TRACE` in logs, new files in doc root | Disable WebDAV & unused methods; read-only doc root; FIM on web root |
| Source-code / secret disclosure | Requests for `.bak`/`.old`/`.git`, config in web root | **No secrets in web root**; secrets manager/vault; block dotfiles/backups |
| HTTP response splitting / cache poison | CRLF (`%0d%0a`) in params, odd cache hits | Encode/strip CRLF in headers; validate cache keys; patch |
| Unpatched known vuln | Version banner → public exploit; exploit attempts | **Patch cadence + inventory**; suppress version banners; virtual patching |
| Webshell / RCE persistence | New file in doc root, web user spawning shells | **Least-privilege service account** (www-data/AppPool, never root/SYSTEM); allow-listing; EDR |
| DoS against the server | Connection-table saturation, slow requests | Rate limiting, reverse proxy, connection timeouts |

> **PAM playbook for this module:** treat the web server as a **privileged service, not a person**. Run the daemon under a **dedicated least-privilege service account** (`www-data`, an IIS AppPool identity — never root/Administrator/SYSTEM) so a webshell inherits almost nothing. Keep **secrets out of the web root** and in a vault, enforce a **patch cadence with an accurate inventory** (banner suppression buys time, it is not a fix), and put **file-integrity monitoring** on the document root so an uploaded shell trips an alert. Remove default samples and disable unused HTTP methods as part of your build baseline.

## Exam tips & gotchas

- **Web server vs web application** hacking: this module = the *server/config/patch* layer; Module 14 = the *app code* (XSS, SQLi, etc.). CEH separates them deliberately.
- **Directory traversal** (read files outside doc root via `../`) is not the same as **directory brute forcing** (guessing existing paths) — different intents.
- **HTTP response splitting** = CRLF injection **into a response header**; it enables cache poisoning and header-based XSS. Don't confuse with request smuggling (front-end/back-end desync).
- **XST** abuses the `TRACE` method to read cookies/headers even with HttpOnly — mitigation is simply disabling `TRACE`.
- **Nikto** finds *known issues & misconfig*; it is loud/not stealthy. **gobuster/dirb/ffuf** do *content discovery*. **whatweb** *fingerprints*. Match tool→job.
- **Banner suppression is obscurity, not a control** — patching is the control.
- Default-credential and default-page removal is a favorite countermeasure answer.

## Sources

- OWASP Web Security Testing Guide — https://owasp.org/www-project-web-security-testing-guide/
- Nikto — https://github.com/sullo/nikto
- ffuf — https://github.com/ffuf/ffuf
- nmap HTTP scripts (NSE) — https://nmap.org/nsedoc/categories/discovery.html
- Apache HTTP Server security tips — https://httpd.apache.org/docs/current/misc/security_tips.html
- MITRE ATT&CK: Exploit Public-Facing Application (T1190) — https://attack.mitre.org/techniques/T1190/
- MITRE ATT&CK: Server Software Component: Web Shell (T1505.003) — https://attack.mitre.org/techniques/T1505/003/

---
### 📝 My lab log (fill in)
| Date | Target | Command | Result / notes |
|---|---|---|---|
|  |  |  |  |
