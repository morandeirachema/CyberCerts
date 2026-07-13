# Module 11 — Session Hijacking · Guided Lab Walkthrough

> Step-by-step against **DVWA in your own Docker lab** ([`../../labs/docker-compose.yml`](../../labs/docker-compose.yml)) behind **Burp Suite** — never a site you don't own. Each step: action/command, what you should see, an observation, a hint, and the defender/PAM takeaway. Outputs are **representative**.

**Goal:** prove that an authenticated session cookie *is* a bearer credential — capture it (Part A), **ride** it from a second browser without logging in (Part B), then test whether the app is vulnerable to **session fixation** (Part C).

**Target:** DVWA at `http://localhost:8081`. Set **DVWA Security = Low** to start. Proxy your browser through **Burp** (`127.0.0.1:8080`, Proxy → Intercept). The cookie of interest is **`PHPSESSID`** (plus DVWA's `security` cookie).

---

## Part A — Capture the session cookie (app-level theft)

### A1. Proxy the browser through Burp
Configure the browser to use `127.0.0.1:8080`, then in Burp turn **Proxy → Intercept off** and watch **HTTP history**.

**You should see** requests to `localhost:8081` flowing through Burp's HTTP history.

**Observe:** Burp now sees every request/response — this is the "in the path" position an app-level attacker needs.

<details><summary>Hint: no traffic in Burp</summary>Confirm the browser proxy points at Burp's listener and that Intercept is **off** (Intercept-on will pause every request). For HTTPS targets you'd also install Burp's CA; DVWA on plain HTTP needs no CA.</details>

**Defender/PAM view:** any proxy/MITM in the path can read cookies sent in cleartext — the first reason to enforce **TLS everywhere + HSTS**.

### A2. Log in and capture PHPSESSID
Log into DVWA (`admin` / `password`). In Burp **HTTP history**, click a request to `localhost:8081` and read the **Cookie** header; also check the login response's **Set-Cookie**.

**You should see** something like:
```
Set-Cookie: PHPSESSID=8f3a1c9b2e7d4a6f5c0b1234abcd5678; path=/
Cookie: PHPSESSID=8f3a1c9b2e7d4a6f5c0b1234abcd5678; security=low
```

**Observe:** the `PHPSESSID` value is the **entire proof of identity** for this logged-in session. Note whether it carries **HttpOnly** / **Secure** flags (Low DVWA typically does not).

<details><summary>Hint: which cookie matters?</summary>`PHPSESSID` is the PHP session identifier — that's the bearer token. `security` just holds DVWA's difficulty level. Copy the `PHPSESSID` value exactly, no surrounding spaces.</details>

**Defender/PAM view:** a token with no **HttpOnly** is readable by injected script (XSS); with no **Secure** it leaks over any non-TLS hop. Flag both findings.

---

## Part B — Ride the session from a second browser (the hijack)

### B1. Reuse the stolen cookie
Open a **second browser or an incognito/private window** (a fresh session with **no login**). Browse to `http://localhost:8081/`. You'll be unauthenticated. Now set the cookie to the captured value — via a cookie-editor extension, DevTools (**Application → Cookies**), or by replaying a request in **Burp Repeater** with the stolen `Cookie: PHPSESSID=...` header.

**You should see** an authenticated DVWA page load (e.g. the Welcome/index) **without ever submitting credentials**.

**Observe:** you are now **riding the victim's session**. No password, no MFA — possession of the cookie *is* the identity. This is application-level session hijacking.

<details><summary>Hint: still redirected to login</summary>The value is stale or mistyped. Re-capture a fresh `PHPSESSID` from Part A, ensure you also set `security=low`, and confirm the original session hasn't been logged out. In Burp Repeater, send a GET to an authenticated page with the stolen Cookie header and read the response body.</details>

**Defender/PAM view:** the server can't tell the two browsers apart — the token isn't bound to client, IP, or device. Controls: **bind the session** to client attributes/MFA, **rotate on privilege change**, **short idle timeouts**, and alert on the **same session ID appearing from a new IP/User-Agent**. In PAM, the session runs on the **broker (PSM)** so there is **no endpoint token to lift** in the first place.

---

## Part C — Session-fixation test (set a known ID before login)

### C1. Plant a known session ID *before* authenticating
Log out / clear cookies. Before logging in, **set a session ID you choose**, e.g. `PHPSESSID=attackerknows123`, using DevTools or Burp. Confirm it's attached to requests.

**You should see** your chosen value going out in the **Cookie** header on the pre-login page.

**Observe:** this simulates the attacker planting an ID (e.g. via a crafted link) that the victim will then authenticate.

### C2. Log in, then compare the ID
Now log in with valid DVWA credentials. In Burp, inspect the login **response** and subsequent requests.

**You should see** one of two outcomes:
- **Reused (vulnerable):** the post-login `PHPSESSID` is still `attackerknows123` — the app authenticated the attacker-known ID.
- **Reissued (fixed):** the login response contains a **`Set-Cookie: PHPSESSID=<new random value>`** and the old ID no longer works.

**Observe:** if the ID is **reused across the login boundary**, the app is vulnerable to **session fixation** — an attacker who knew the pre-login value now holds an authenticated session.

<details><summary>Hint: how to be sure it rotated</summary>Diff the `PHPSESSID` value in the last pre-login request against the first post-login request. Different value + a `Set-Cookie` on the login response = rotation (safe). Same value = fixation (vulnerable). Try replaying `attackerknows123` in Repeater after login to confirm whether it still authenticates.</details>

**Defender/PAM view:** the definitive fix is to **regenerate the session ID on authentication** (and on any privilege change), so a pre-set ID can never survive login. Pair with **step-up re-authentication** for sensitive actions so even a valid session can't perform high-impact operations unchallenged.

---

## What you should conclude
| Step | What it proved | Real-world defense |
|---|---|---|
| A2 captured `PHPSESSID` in cleartext | The token is readable in the path | **TLS everywhere + HSTS**, `Secure` flag |
| A2 cookie lacked HttpOnly | Script could read it (XSS) | **HttpOnly** cookie flag, CSP |
| B1 rode the session from a 2nd browser | Token is an unbound bearer credential | **Bind session** to client/MFA, short idle timeout, alert on new IP/UA |
| C2 ID reused across login | Session fixation | **Regenerate session ID on authentication** |
| Any stolen privileged session | Attacker inherits live access | **PAM brokering/recording (PSM)** + **step-up re-auth** — no token on the endpoint |

## Cleanup
```bash
# Nothing persistent is created. In each browser: clear cookies for localhost:8081
# and log out of DVWA. Reset via DVWA's "Setup / Reset DB" page if desired.
# Close Burp; revert the browser proxy setting to Off.
```

## Record it
Log the captured cookie handling, the ride-the-session result, and the fixation verdict (reused vs. reissued) in the **My lab log** table in [README.md](README.md); note misses in [PROGRESS.md](../../PROGRESS.md).
