# Module 14 — Hacking Web Applications · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** An attacker posts a comment containing `<script>` on a forum. Every user who later views the thread has their session cookie exfiltrated. Which XSS type is this?

- A. Reflected XSS
- B. Stored (persistent) XSS
- C. DOM-based XSS
- D. Self-XSS

<details><summary>Answer</summary>

**B. Stored (persistent) XSS.** The payload is saved **server-side** (in the comment) and executes for **every** viewer, with no per-victim link required. Reflected XSS echoes the payload straight back from a single request and needs the victim to click a crafted link; DOM-based XSS never reaches the server. **Tell:** "saved" + "every viewer" ⇒ stored.
</details>

---

**Q2.** A victim receives an email link like `https://shop.site/search?q=<script>...</script>`. Clicking it runs the script, which is echoed unencoded in the results page. This is:

- A. Stored XSS
- B. Reflected XSS
- C. CSRF
- D. SSRF

<details><summary>Answer</summary>

**B. Reflected XSS.** The payload is **not stored** — it is reflected back from *this one request* and only fires because the victim **clicked the crafted link**. That per-victim link is the signature of reflected (non-persistent) XSS. CSRF forces an action but doesn't inject script; SSRF targets the server.
</details>

---

**Q3.** A single-page app reads `location.hash` and writes it into the page with `element.innerHTML = ...`. No malicious data ever reaches the web server. Which vulnerability class is this?

- A. Reflected XSS
- B. Stored XSS
- C. DOM-based XSS
- D. Insecure deserialization

<details><summary>Answer</summary>

**C. DOM-based XSS.** The vulnerability lives entirely in **client-side JavaScript**: attacker-controlled DOM data (`location.hash`) flows into a dangerous sink (`innerHTML`). Because the payload **never touches the server**, server-side logs/WAFs may miss it. The fix is safe DOM APIs (`textContent`) and avoiding sinks like `innerHTML`/`eval`.
</details>

---

**Q4.** Your team keeps blocking XSS by stripping `<script>` from inputs, yet payloads keep getting through. What is the **most durable** fix?

- A. A longer input blocklist
- B. Context-aware output encoding plus a Content Security Policy (CSP)
- C. Renaming the vulnerable parameters
- D. Rate-limiting the login page

<details><summary>Answer</summary>

**B. Context-aware output encoding plus a CSP.** XSS is an **output** problem: encode data for the context where it is rendered (HTML body, attribute, JS, URL) and add a CSP to constrain script execution. **Input filtering / blocklists are bypassable** (attribute breakout, event handlers, encoding tricks). Add `HttpOnly` + `SameSite` cookies to blunt session theft.
</details>

---

**Q5.** A web app fetches a URL supplied by the user. An attacker makes it request `http://169.254.169.254/latest/meta-data/` and receives cloud credentials. Which attack is this?

- A. CSRF
- B. SSRF
- C. Stored XSS
- D. Directory traversal

<details><summary>Answer</summary>

**B. SSRF (Server-Side Request Forgery).** The **server** is tricked into making a request to an **internal / link-local** target — here the cloud metadata endpoint `169.254.169.254`. That metadata target is the giveaway. Fixes: egress allow-list, block link-local/internal ranges, and **IMDSv2**. Contrast with CSRF, which tricks the *browser*.
</details>

---

**Q6.** A crafted page auto-submits a hidden form to `bank.site/change-email` while the victim is logged in, changing their account email. No script executes in the victim's session. This is:

- A. SSRF
- B. Stored XSS
- C. CSRF
- D. IDOR

<details><summary>Answer</summary>

**C. CSRF (Cross-Site Request Forgery).** The **victim's browser** is tricked into submitting an authenticated **state-changing** request using its existing session cookie. No injected script is needed. Defenses: **anti-CSRF tokens** and **`SameSite` cookies**. Remember: **CSRF → browser is tricked; SSRF → server is tricked.**
</details>

---

**Q7.** After logging in, a user changes `?invoice_id=5001` to `5002` in the URL and views another customer's invoice. What is this, and which OWASP 2021 category does it map to?

- A. Injection — A03
- B. Insecure Direct Object Reference — A01 Broken Access Control
- C. Security Misconfiguration — A05
- D. SSRF — A10

<details><summary>Answer</summary>

**B. IDOR — A01 Broken Access Control.** Accessing another object by tampering a predictable reference is an **authorization** failure, not an input-validation flaw. It maps to **A01**, the **#1** OWASP 2021 category. Fix = **server-side, per-object authorization checks with deny-by-default** — never rely on the ID being hard to guess.
</details>

---

**Q8.** A parameter `?page=` is exploitable. Supplying `http://attacker.com/shell.txt` causes the server to execute remote code, while `../../../../etc/passwd` reads a local file. Name the two techniques, respectively.

- A. RFI, then LFI
- B. LFI, then RFI
- C. XXE, then SSRF
- D. Directory traversal, then command injection

<details><summary>Answer</summary>

**A. RFI, then LFI.** Pulling and executing a **remote** file is **Remote File Inclusion (RFI)** — it usually requires `allow_url_include=On`. Reading a **local** file via `../` sequences is **Local File Inclusion (LFI)** / directory traversal. **Mnemonic: Remote = RFI (remote URL), Local = LFI (local path).**
</details>

---

**Q9.** On a file-upload form with no server-side validation, an attacker uploads `shell.php` containing `<?php system($_GET['c']); ?>` and browses to it. What is the immediate impact?

- A. Reflected XSS in the upload page
- B. A web shell giving remote command execution (RCE)
- C. A CSRF token bypass
- D. An SSRF into the storage backend

<details><summary>Answer</summary>

**B. A web shell → RCE.** An **unrestricted file upload** that lets an executable script land in a web-served, executable directory yields a **web shell** and full command execution. Controls: validate type **server-side**, store uploads **off the web root**, disable execution in the upload directory, and randomize file names.
</details>

---

**Q10.** A "ping" tool runs `ping <user_input>`. Submitting `127.0.0.1; id` returns the output of `id`. Which flaw is this, and what is the primary fix?

- A. XSS — output encoding
- B. Command injection — avoid the shell / pass arguments safely, don't rely on a blocklist
- C. IDOR — authorization checks
- D. XXE — disable external entities

<details><summary>Answer</summary>

**B. Command injection.** User input reaches an OS shell and the `;` chains a second command. The durable fix is **not a blocklist** — it's **avoiding shell execution entirely** or passing arguments through a safe API (no shell metacharacter interpretation), plus a **least-privilege service account** so the payoff is small.
</details>

---

**Q11.** An application accepts a serialized object from the client and reconstructs it without validation, allowing an attacker to trigger code execution. Which OWASP 2021 category best fits?

- A. A01 Broken Access Control
- B. A03 Injection
- C. A08 Software & Data Integrity Failures
- D. A10 SSRF

<details><summary>Answer</summary>

**C. A08 Software & Data Integrity Failures.** **Insecure deserialization** lives under **A08**. Never deserialize untrusted data; if you must, use integrity checks / signing and type allow-lists. (Don't confuse it with A03 Injection — deserialization has its own home in the 2021 list.)
</details>

---

**Q12.** Match the vulnerability to its OWASP 2021 category. Which pairing is **correct**?

- A. XSS → A10 SSRF
- B. SSRF → A03 Injection
- C. XSS → A03 Injection; SSRF → A10
- D. IDOR → A05 Security Misconfiguration

<details><summary>Answer</summary>

**C. XSS → A03 Injection; SSRF → A10.** In OWASP 2021, **XSS is folded into A03 Injection**, while **SSRF is its own standalone category, A10**. IDOR belongs to **A01 Broken Access Control**, not A05. Knowing these exact placements is a common exam discriminator.
</details>

---

**Q13.** You see this in an XML request body: `<!DOCTYPE foo [<!ENTITY x SYSTEM "file:///etc/passwd">]> <foo>&x;</foo>`. What attack is being attempted?

- A. Insecure deserialization
- B. XXE (XML External Entity)
- C. Reflected XSS
- D. RFI

<details><summary>Answer</summary>

**B. XXE.** Declaring an **external entity** that references `file:///etc/passwd` (or an internal URL) is the classic **XML External Entity** attack — it enables local file read, **SSRF**, and DoS. Fix: **disable DTDs / external entity resolution** in the XML parser. XXE is typically classed under **A05 Security Misconfiguration**.
</details>

---

**Q14.** An app assigns a session ID *before* login and does not rotate it afterward, so an attacker who plants a known ID can hijack the authenticated session. This is:

- A. Session fixation (broken authentication / session management)
- B. DOM-based XSS
- C. CSRF
- D. Command injection

<details><summary>Answer</summary>

**A. Session fixation.** Because the session ID is **not regenerated on login**, an attacker who fixes a known ID rides the victim's authenticated session — an **A07 Identification & Authentication Failures** problem. Fix: **rotate the session ID on authentication**, set `HttpOnly`/`Secure`/`SameSite`, expire idle sessions, and add MFA.
</details>

---

**Q15.** In the CEH web-app methodology, what is the correct role of an intercepting proxy such as Burp Suite or OWASP ZAP?

- A. It replaces manual testing with a fully automated scan
- B. It captures requests so you can tamper one parameter at a time and observe responses; automation only confirms
- C. It is only useful for encrypting traffic
- D. It patches vulnerabilities server-side

<details><summary>Answer</summary>

**B.** The proxy is where you **understand** the app: intercept a request, send it to **Repeater**, change **one parameter at a time**, and read the response. Automated tools (Scanner, sqlmap, commix) **confirm** findings — they don't replace the manual, proxy-driven loop that reveals *why* something is exploitable.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the XSS types, CSRF-vs-SSRF, and OWASP Top 10 sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
