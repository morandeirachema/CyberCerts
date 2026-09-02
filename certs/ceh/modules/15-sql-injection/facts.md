# Module 15 — SQL Injection · Must-Know Facts

> One-page, high-yield recall sheet. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## Root cause & the one real fix
**Cause:** untrusted input concatenated into a SQL query, so data becomes *code*.
**Primary fix:** **parameterized queries / prepared statements** (bind variables). Input validation, WAF, and least-privilege DB accounts are *defense-in-depth*, **not** the primary fix. (SQLi = OWASP **A03: Injection**.)

## SQLi taxonomy
| Class | Type | How you read the result |
|---|---|---|
| **In-band** | Error-based | DB error messages leak data |
| **In-band** | UNION-based | Append `UNION SELECT` to return extra rows |
| **Inferential (blind)** | Boolean-based | Page changes True vs False |
| **Inferential (blind)** | Time-based | `SLEEP()` delay = condition true |
| **Out-of-band (OOB)** | DNS/HTTP | DB makes a network callback carrying data |

## UNION requirements (asked often)
1. **Same number of columns** — find with `ORDER BY n` (increment until error) or `UNION SELECT 1,2,3...`.
2. **Compatible data types** in the injected columns.
3. Find which columns are **displayed** (use markers like `1,2,3`).

## Detection payloads
- `'` or `"` → error/broken page = candidate.
- `1' OR '1'='1' -- -` → always-true (auth bypass / boolean).
- `1' ORDER BY 5 -- -` → column counting.

## Comment / syntax notes
- `-- ` (dash-dash-**space**) and `#` (MySQL) and `/* */` are comment terminators.
- Fingerprint: MySQL `version()`,`database()`,`@@version`; MSSQL `@@version`; schema via `information_schema.tables/columns` (Oracle uses `all_tables`/`user_tables`).

## SQLi → beyond data theft
- **MSSQL:** `xp_cmdshell` → OS command execution (if enabled + privileged).
- **MySQL:** `INTO OUTFILE` (write a web shell), `LOAD_FILE()` (read files).
- Reading files / writing web shells turns SQLi into **RCE**.

## sqlmap essentials
| Flag | Purpose |
|---|---|
| `--dbs` | list databases |
| `-D db --tables` | list tables |
| `-D db -T users --dump` | dump a table |
| `--current-user --is-dba` | check DB privilege |
| `--batch` | non-interactive defaults |
| `--level / --risk` | test depth / risky payloads |
| `--technique` | restrict to B/E/U/T/S |
| `--os-shell` | attempt an OS shell |

## Defenses (rank them)
1. **Parameterized queries / prepared statements** (the answer).
2. Stored procedures (only if they don't build dynamic SQL).
3. Allow-list input validation.
4. **Least-privilege DB account** (no `sa`/DBA; disable `xp_cmdshell`).
5. WAF (buys time; bypassable via encoding/case/inline comments).
6. Escaping (weakest; error-prone).

## PAM angle
Vault + **CPM-rotate** the DB service account; deliver the connection string via **CCP/Conjur** at runtime so a dumped `web.config` or an exfiltrated string is short-lived and low-privilege. See [cyberark-attack-mapping.md](../../defender-pam/cyberark-attack-mapping.md).

## Top traps
- **Parameterized queries** is the *best* fix — not "input validation" or "WAF."
- **Blind ≠ no data** — boolean/time-based still exfiltrate, just slowly.
- UNION needs **matching column count and types**.
- `xp_cmdshell` is **MSSQL**; `INTO OUTFILE` is **MySQL**. Don't swap.
- Stored procedures are **not** automatically safe if they concatenate input.
