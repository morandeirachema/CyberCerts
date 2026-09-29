# Module 15 — SQL Injection · Practice Questions

> **Original, concept-based questions** — not exam dumps. Answers are collapsed: decide first, then expand. Target **≥80%**. Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** What is the **single most effective** defense against SQL injection?

- A. A web application firewall (WAF)
- B. Blocklist filtering of the word "SELECT"
- C. Parameterized queries / prepared statements
- D. Renaming the database tables

<details><summary>Answer</summary>

**C. Parameterized queries / prepared statements.** They separate *code* from *data* so input can never change query structure. A WAF is bypassable (encoding/case), blocklists are trivially evaded, and obscurity does nothing. On the exam, "parameterized/prepared statements" is the canonical best answer.
</details>

---

**Q2.** A `SLEEP(5)` in the response time confirms which SQLi type?

- A. UNION-based
- B. Error-based
- C. Time-based blind
- D. Out-of-band

<details><summary>Answer</summary>

**C. Time-based blind.** When no data or error is reflected, you infer bits by making the DB pause on a true condition. Boolean-based blind uses page *content* changes instead; OOB uses a network callback.
</details>

---

**Q3.** Before a UNION-based injection can return data, the attacker must first determine:

- A. The database administrator's password
- B. The number of columns (and compatible types) in the original query
- C. The web server's OS
- D. The TLS cipher suite

<details><summary>Answer</summary>

**B.** A `UNION SELECT` must match the original query's **column count and types**. Find the count with `ORDER BY n` (increment until it errors) or by adding columns to `UNION SELECT 1,2,3...`.
</details>

---

**Q4.** Which payload is a classic **authentication bypass** test?

- A. `1' OR '1'='1' -- -`
- B. `'; DROP TABLE users; --`
- C. `<script>alert(1)</script>`
- D. `../../etc/passwd`

<details><summary>Answer</summary>

**A. `1' OR '1'='1' -- -`** makes the WHERE clause always true and comments out the rest. B is destructive (and not "bypass"); C is XSS; D is path traversal.
</details>

---

**Q5.** SQLi is which OWASP Top 10 (2021) category?

- A. A01 Broken Access Control
- B. A10 SSRF
- C. A07 Identification & Authentication Failures
- D. A03 Injection

<details><summary>Answer</summary>

**D. A03 Injection** — which also covers command injection and (in 2021) XSS.
</details>

---

**Q6.** On **Microsoft SQL Server**, which feature is abused to run OS commands via SQLi?

- A. `INTO OUTFILE`
- B. `information_schema`
- C. `LOAD_FILE()`
- D. `xp_cmdshell`

<details><summary>Answer</summary>

**D. `xp_cmdshell`** (MSSQL). `INTO OUTFILE`/`LOAD_FILE()` are **MySQL** file write/read primitives; `information_schema` is for schema enumeration, not command execution. Don't mix the MSSQL vs MySQL primitives.
</details>

---

**Q7.** Which system view is commonly queried to enumerate table and column names in MySQL/MSSQL/PostgreSQL?

- A. `information_schema`
- B. `sys.master`
- C. `pg_hba`
- D. `mysql.user` only

<details><summary>Answer</summary>

**A. `information_schema`** (`.tables`, `.columns`). Oracle differs (`all_tables`/`user_tables`). Knowing the schema source per DBMS is a frequent question.
</details>

---

**Q8.** A pentester runs `sqlmap ... --is-dba --current-user`. What are they checking?

- A. Whether the site uses HTTPS
- B. The WAF vendor
- C. The number of columns
- D. The privilege level of the DB account the app uses

<details><summary>Answer</summary>

**D.** These report the current DB user and whether it has DBA rights — i.e., *how much damage* the injection enables. An over-privileged app account (e.g., `sa`) turns SQLi into full DB/host compromise, which is why **least-privilege DB accounts** matter.
</details>

---

**Q9.** "Blind" SQL injection means:

- A. The injection is impossible to exploit
- B. No data or errors are returned directly, so results are inferred
- C. The attacker cannot see the login page
- D. The database is encrypted

<details><summary>Answer</summary>

**B.** Blind = no direct output; you infer data via **boolean** (page changes) or **time** (delays) responses. It's slower but still fully exfiltrates data.
</details>

---

**Q10.** Why are **stored procedures** *not automatically* safe against SQLi?

- A. If they build and execute dynamic SQL from input, they're still injectable
- B. They are always slower
- C. They only work on Oracle
- D. They disable parameterization

<details><summary>Answer</summary>

**A.** A stored procedure that concatenates user input into dynamic SQL (`EXEC(@sql)`) is just as vulnerable. Safety comes from **parameterization**, not from being "in a procedure."
</details>

---

**Q11.** Which is a legitimate reason a **WAF** is only a *partial* SQLi control?

- A. WAFs cannot inspect HTTP
- B. WAFs block all database traffic
- C. Payloads can be obfuscated (encoding, case variation, inline comments) to evade signatures
- D. WAFs replace the need for patching

<details><summary>Answer</summary>

**C.** Signature-based WAFs are bypassable with `/*!50000UNION*/`, URL/hex encoding, mixed case, etc. Use a WAF as *defense-in-depth* behind parameterized queries — never as the primary fix.
</details>

---

**Q12.** In the DVWA lab, you extract credentials with `1' UNION SELECT user, password FROM users -- -`. The passwords come back as MD5 hashes. What's the exam-relevant follow-up weakness?

- A. The app used HTTPS
- B. Passwords stored as fast, unsalted hashes (MD5) are quickly cracked offline
- C. The database is too small
- D. UNION is not real SQLi

<details><summary>Answer</summary>

**B.** Storing passwords as fast hashes like **MD5** (unsalted) means once exfiltrated they crack in seconds. Password storage should use slow, salted KDFs (bcrypt/scrypt/Argon2/PBKDF2) — ties back to Module 20.
</details>

---

### Score yourself
- **11–12:** strong — drill the MySQL-vs-MSSQL primitives in [facts.md](facts.md).
- **8–10:** re-read the SQLi taxonomy and UNION-requirements sections.
- **< 8:** redo the [lab-walkthrough.md](lab-walkthrough.md) against DVWA and re-read [README.md](README.md).
