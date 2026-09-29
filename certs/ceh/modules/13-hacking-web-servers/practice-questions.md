# Module 13 — Hacking Web Servers · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** CEH separates *web-server* hacking from *web-application* hacking. Which finding belongs to the **web-server** module (this one), not the web-app module?

- A. A reflected cross-site scripting (XSS) flaw in a search box
- B. A SQL injection in a login form
- C. An unpatched Apache version exposed by the `Server:` banner
- D. Broken access control letting a user read another user's cart

<details><summary>Answer</summary>

**C. An unpatched Apache version.** The server layer = the HTTP daemon, its OS, config, and patch level. XSS, SQLi, and broken access control are **application-code** issues covered in Module 14. **Exam tell:** if the fix is *patch / reconfigure / remove a default*, it's this module; if the fix is *fix the code*, it's the app module.
</details>

---

**Q2.** An attacker requests `GET /scripts/../../../../etc/passwd` and receives the file contents. Which attack is this?

- A. Directory brute forcing
- B. Web cache poisoning
- C. HTTP response splitting
- D. Directory / path traversal

<details><summary>Answer</summary>

**D. Path traversal.** The `../` sequences escape the document root to read an arbitrary OS file. Don't confuse it with **directory brute forcing**, which *guesses existing* paths (admin panels, backups) rather than escaping the root. Encoded forms like `%2e%2e%2f` are the classic WAF-evasion tell.
</details>

---

**Q3.** During a test you find the `TRACE` method enabled. Which attack does this most directly allow?

- A. Cross-Site Tracing (XST)
- B. WebDAV file upload
- C. SQL injection
- D. Slowloris DoS

<details><summary>Answer</summary>

**A. Cross-Site Tracing (XST).** `TRACE` echoes the request back, letting an attacker read cookies/headers **even when they are marked HttpOnly**. The mitigation is trivially to **disable `TRACE`**. `PUT`/`MOVE` (not `TRACE`) enable WebDAV uploads.
</details>

---

**Q4.** Which pair of HTTP methods, if writable on a WebDAV-enabled directory, most directly leads to remote code execution?

- A. `GET` and `HEAD`
- B. `OPTIONS` and `TRACE`
- C. `PUT` and `MOVE`
- D. `CONNECT` and `PATCH`

<details><summary>Answer</summary>

**C. `PUT` and `MOVE`.** `PUT` writes a file into the doc root; if the extension is executable (or `MOVE` renames it to one), the attacker gets a webshell → RCE. `GET`/`HEAD` only read; `OPTIONS`/`TRACE` are recon/XST. Countermeasure: **disable WebDAV and unused methods**, keep the doc root read-only.
</details>

---

**Q5.** You run `curl -sI http://target` and read the `Server: Apache/2.4.49` line. What is this technique, and what is it *for*?

- A. Banner grabbing — to map the version to publicly documented vulnerabilities
- B. Fuzzing — to find hidden directories
- C. Session hijacking — to steal a cookie
- D. Cache poisoning — to store attacker content

<details><summary>Answer</summary>

**A. Banner grabbing.** Reading the `Server:` / `X-Powered-By:` headers identifies the software/version, the starting point for **patch-management** analysis (look the version up; don't guess CVE numbers). Note the banner can be masked — **suppression is obscurity, not a control; patching is the control.**
</details>

---

**Q6.** Which tool is the right choice specifically to scan a web server for **known misconfigurations and dangerous defaults**?

- A. gobuster
- B. whatweb
- C. Nikto
- D. wpscan

<details><summary>Answer</summary>

**C. Nikto.** It checks for default files, dangerous methods, missing security headers, and known-issue signatures — but it is **loud, not stealthy**. **gobuster** does content discovery, **whatweb** fingerprints the stack, and **wpscan** is WordPress-specific. Match tool → job.
</details>

---

**Q7.** A request returns the raw contents of `config.php.bak` as text instead of executing it. What class of issue is this?

- A. Directory traversal
- B. HTTP response splitting
- C. Source-code / secret disclosure
- D. DoS

<details><summary>Answer</summary>

**C. Source-code / secret disclosure.** A backup extension (`.bak`, `.old`, `.php~`) or handler misconfig makes the server return the script verbatim — often leaking DB credentials. Fix: **no secrets in the web root**, block backup/dotfile extensions, and vault the secrets. This is why gobuster is run with `-x php,bak,old`.
</details>

---

**Q8.** Which technique injects CRLF (`%0d%0a`) into a **response header** to forge a second response, enabling cache poisoning or header-based XSS?

- A. HTTP request smuggling
- B. Directory traversal
- C. Cross-Site Tracing
- D. HTTP response splitting

<details><summary>Answer</summary>

**D. HTTP response splitting.** CRLF injected *into a response header* lets the attacker start a forged second header/response. Don't confuse it with **request smuggling**, which is a front-end/back-end **desync** of request boundaries. Mitigation: strip/encode CRLF, patch, and validate cache keys.
</details>

---

**Q9.** In the EC-Council web-server hacking methodology, which activity comes **first**?

- A. Vulnerability scanning with Nikto
- B. Information gathering (WHOIS, DNS)
- C. Password cracking of the admin panel
- D. Mirroring the website offline

<details><summary>Answer</summary>

**B. Information gathering.** The order is **info gathering → web-server footprinting → mirror the site → vulnerability scanning → session hijacking → password cracking.** You footprint and enumerate before you ever launch an active scan or crack.
</details>

---

**Q10.** Nikto flags an accessible `/manager` app and a live `/phpinfo.php`. What is the single best remediation theme?

- A. Enable directory listing so the paths are visible
- B. Remove default/sample apps and pages on deployment
- C. Add the paths to the sitemap
- D. Switch from HTTPS to HTTP for testing

<details><summary>Answer</summary>

**B. Remove default/sample apps and pages.** Shipped manager consoles, sample apps, and info pages leak version/config detail and often carry default credentials. Stripping them (plus changing/vaulting any default admin login) is a favorite countermeasure answer. Directory listing should be **disabled**, not enabled.
</details>

---

**Q11.** You confirmed an unpatched, publicly exploitable web-server version. Which control is the *actual* fix (as opposed to buying time)?

- A. Suppress the `Server:` banner
- B. Add a `robots.txt` disallow rule
- C. Rename the admin directory
- D. Establish a patch cadence backed by an accurate inventory

<details><summary>Answer</summary>

**D. Patch cadence + accurate inventory.** Banner suppression, renaming, and `robots.txt` are all **security-by-obscurity** — they don't remove the vulnerability. Only patching (with an inventory so you know *what* to patch) closes it. Virtual/WAF patching is a stopgap, not the fix.
</details>

---

**Q12.** A web server is compromised via an uploaded webshell. Which design choice most limits what the attacker inherits at that moment?

- A. Running the daemon as `root` for reliability
- B. Disabling logging to reduce noise
- C. Storing DB credentials in the web root for convenience
- D. Running the daemon under a dedicated least-privilege service account (`www-data` / IIS AppPool)

<details><summary>Answer</summary>

**D. Least-privilege service account.** The webshell executes **as the service account**, so if that identity is `www-data` / a scoped AppPool — never root/SYSTEM — the attacker inherits almost nothing and must still escalate. Running as root, exposing creds, and killing logs all make it worse.
</details>

---

**Q13.** *(PAM — best defense)* A web app holds its database connection string in `web.config`. What is the strongest PAM-aligned remediation?

- A. Base64-encode the connection string
- B. Deliver the secret at runtime via CyberArk CCP/Conjur and rotate it with CPM
- C. Comment the password out and add it back at deploy time
- D. Store the file outside version control only

<details><summary>Answer</summary>

**B. Deliver at runtime via CCP/Conjur, rotate with CPM.** Removing the **hardcoded** secret means a leaked config file (or a compromised server) yields **no reusable static credential**; CPM rotation limits any window. Base64 is encoding, not protection; the others still leave a static secret on disk.
</details>

---

**Q14.** *(PAM — best defense)* You want an early, reliable signal that an attacker dropped a webshell into the document root. Which control gives it?

- A. File-integrity monitoring (FIM) on the web root
- B. A longer TLS certificate key
- C. Rotating the TLS cipher suites
- D. Enabling the `TRACE` method for auditing

<details><summary>Answer</summary>

**A. File-integrity monitoring on the web root.** A new/modified file in the doc root (the webshell) trips FIM immediately — pair it with a **read-only doc root** and a **least-privilege service account** so the write is both alerted and constrained. TLS key/cipher changes don't detect file writes; enabling `TRACE` *adds* risk (XST).
</details>

---

### Score yourself
- **12–14:** solid — move on, revisit missed items in [facts.md](facts.md).
- **9–11:** re-read the Attack taxonomy and HTTP methods / WebDAV sections.
- **< 9:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
