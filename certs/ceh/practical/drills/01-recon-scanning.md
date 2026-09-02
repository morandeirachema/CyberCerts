# Drill Pack 01 — Recon & Scanning

> **What this drills:** the *first move* of every Practical challenge — turn IPs into a map of hosts, open ports, service versions, OS, and the odd non-standard port where the interesting stuff hides. Every question below mimics the phrasing the CEH Practical uses ("*What is the exact version…*", "*How many open TCP ports…*", "*Which port runs…*", "*Is anonymous FTP allowed…*") and carries a **time target** — set a timer and treat it like the real clock.
>
> **Prereq:** your [lab](../../labs/README.md) is running — Kali `192.168.56.10`, Metasploitable2 `192.168.56.20`, DC/ADCS `192.168.56.30` (`ceh.lab`). Recipes live in [`../challenge-playbooks.md`](../challenge-playbooks.md); the theory behind every flag is [Module 03 — Scanning Networks](../../modules/03-scanning-networks/README.md) and [`kali/05-nmap-scanning.md`](../../kali/05-nmap-scanning.md).
>
> Answer from the tool output; open the **Solution** only to check yourself or when truly stuck. Ports/versions below match a stock Metasploitable2 and a Windows Server 2019 DC — a dynamic RPC port may shift a number by one or two.

Score each: **✅ under target time / ⚠️ over time / ❌ needed the solution**. Re-drill anything not ✅.

---

### Challenge 1 — Who's alive on the segment? ⏱️ 3 min
**Q:** How many hosts are up on `192.168.56.0/24`, and what are their IPs?

<details><summary>Solution</summary>

**Step — ARP ping-sweep the subnet** (link-layer discovery is the most reliable on a host-only LAN; even firewalled hosts must answer ARP):
```bash
sudo nmap -sn -PR 192.168.56.0/24
```
**You should see:**
```
Nmap scan report for 192.168.56.10   # Kali (you)
Nmap scan report for 192.168.56.20   # Metasploitable2
Nmap scan report for 192.168.56.30   # DC / ADCS (ceh.lab)
Nmap done: 256 IP addresses (3 hosts up) scanned in 2.09s
```
**Answer:** **3 hosts** — `192.168.56.10`, `.20`, `.30`.

⚡ **Faster / alternative:** `sudo netdiscover -r 192.168.56.0/24` gives the same list with MAC/vendor. Do **not** use `-Pn` here — that skips discovery entirely and is the wrong tool for a "who's up" question.
</details>

---

### Challenge 2 — Count the attack surface ⏱️ 5 min
**Q:** How many **open TCP ports** does Metasploitable2 (`192.168.56.20`) expose on the default (top-1000) scan?

<details><summary>Solution</summary>

**Step — fast SYN scan, default port set:**
```bash
sudo nmap -sS -T4 192.168.56.20
```
**You should see** (tail of the output):
```
Not shown: 977 closed tcp ports (reset)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
...
8180/tcp open  unknown
Nmap done: 1 IP address (1 host up) scanned in 1.6s
```
**Answer:** **23 open TCP ports** (1000 − 977 shown closed). The classic list: 21, 22, 23, 25, 53, 80, 111, 139, 445, 512, 513, 514, 1099, 1524, 2049, 2121, 3306, 5432, 5900, 6000, 6667, 8009, 8180.

⚡ **Faster / alternative:** count them programmatically — `sudo nmap -sS -T4 192.168.56.20 -oG - | grep -oc 'open'`, or scan **all** ports (`-p- --min-rate 2000`) to catch the extras top-1000 misses (e.g. 3632 distccd, 6697, 8787), which pushes the total to ~30.
</details>

---

### Challenge 3 — Exact service version ⏱️ 4 min
**Q:** What is the **exact version** of the FTP service on `192.168.56.20`?

<details><summary>Solution</summary>

**Step — version-probe just port 21** (targeting one port keeps it near-instant):
```bash
sudo nmap -sV -p21 192.168.56.20
```
**You should see:**
```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 2.3.4
```
**Answer:** **`vsftpd 2.3.4`** — the exact string in the `VERSION` column (that specific build ships the famous smiley-face backdoor; feeds straight into vuln analysis).

⚡ **Faster / alternative:** grab the banner by hand — `nc -nv 192.168.56.20 21` prints `220 (vsFTPd 2.3.4)` on connect, no scan needed.
</details>

---

### Challenge 4 — Fingerprint the OS ⏱️ 5 min
**Q:** What operating system / kernel family does `192.168.56.20` report?

<details><summary>Solution</summary>

**Step — OS detection** (`-O` crafts raw probes, so it needs root):
```bash
sudo nmap -O -p22,80,445 192.168.56.20
```
**You should see:**
```
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6
OS details: Linux 2.6.9 - 2.6.33
```
**Answer:** **Linux, kernel 2.6.x** (the Ubuntu 8.04 "Hardy" base of Metasploitable2). Read it off the `OS details` line.

⚡ **Faster / alternative:** `sudo nmap -A 192.168.56.20` bundles `-sV -O -sC` in one pass — thorough but loud; never the answer to a *stealth* question. Cross-check the guess against a version banner like `OpenSSH 4.7p1 Debian 8ubuntu1`, which pins the same era.
</details>

---

### Challenge 5 — Find the service on a non-standard port ⏱️ 6 min
**Q:** **Which port** runs Apache Tomcat on `192.168.56.20`, and what does its version string read?

<details><summary>Solution</summary>

**Step — version-scan the full range** so nothing hides high (Tomcat is not on 8080 here):
```bash
sudo nmap -sV -p- --min-rate 2000 192.168.56.20
```
**You should see:**
```
PORT     STATE SERVICE VERSION
8180/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
```
**Answer:** **Port `8180/tcp`** — `Apache Tomcat/Coyote JSP engine 1.1`.

⚡ **Faster / alternative:** if you already know Metasploitable's high ports, jump straight there — `nmap --script http-title -p8180 192.168.56.20` returns `Apache Tomcat/5.5`, confirming both the port and that the manager app (`/manager/html`, creds `tomcat:tomcat`) is your next stop.
</details>

---

### Challenge 6 — Anonymous access check ⏱️ 5 min
**Q:** **Is anonymous FTP allowed** on `192.168.56.20`?

<details><summary>Solution</summary>

**Step — run the FTP anonymous-login NSE script against port 21:**
```bash
nmap --script ftp-anon -p21 192.168.56.20
```
**You should see:**
```
PORT   STATE SERVICE
21/tcp open  ftp
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--   1 0   0   0 ... (directory listing)
```
**Answer:** **Yes — anonymous FTP login is allowed** (`FTP code 230`).

⚡ **Faster / alternative:** prove it interactively — `ftp 192.168.56.20`, log in as user `anonymous` with any/blank password; a `230 Login successful` confirms it. (`230` = login accepted; `530` would mean denied.)
</details>

---

### Challenge 7 — A UDP service ⏱️ 8 min
**Q:** Name one **open UDP** service (port + service) on `192.168.56.20`.

<details><summary>Solution</summary>

**Step — bounded UDP scan** (UDP is connectionless and slow — always cap it with `--top-ports`; `-sU` needs root):
```bash
sudo nmap -sU --top-ports 20 192.168.56.20
```
**You should see** (this takes far longer than a TCP scan):
```
PORT    STATE         SERVICE
53/udp  open          domain
69/udp  open|filtered tftp
111/udp open          rpcbind
137/udp open          netbios-ns
2049/udp open         nfs
```
**Answer:** **`53/udp domain`** (DNS) is cleanly open — `137/udp netbios-ns`, `111/udp rpcbind`, and `2049/udp nfs` are also open.

⚡ **Faster / alternative:** add `-sV` to resolve any `open|filtered` verdicts — a version reply proves *open*, silence leaves it ambiguous. Remember the UDP rule: **no response = `open|filtered`**, a closed UDP port returns an ICMP port-unreachable.
</details>

---

### Challenge 8 — Fully-qualified domain name of the DC ⏱️ 6 min
**Q:** What is the **FQDN** of the domain controller at `192.168.56.30`?

<details><summary>Solution</summary>

**Step — pull identity from the RDP NTLM handshake** (reliable on modern Windows where SMBv1/`smb-os-discovery` is often disabled):
```bash
nmap --script rdp-ntlm-info -p3389 192.168.56.30
```
**You should see:**
```
| rdp-ntlm-info:
|   NetBIOS_Domain_Name: CEH
|   NetBIOS_Computer_Name: DC01
|   DNS_Domain_Name: ceh.lab
|   DNS_Computer_Name: dc01.ceh.lab
|   DNS_Tree_Name: ceh.lab
|_  Product_Version: 10.0.17763
```
**Answer:** **`dc01.ceh.lab`** (domain `ceh.lab`, NetBIOS `CEH`).

⚡ **Faster / alternative:** query LDAP's rootDSE — `nmap --script ldap-rootdse -p389 192.168.56.30` returns `defaultNamingContext: DC=ceh,DC=lab` and the server DNS name. `nxc smb 192.168.56.30` prints the same hostname/domain in its banner line.
</details>

---

### Challenge 9 — Windows version + role of the DC ⏱️ 7 min
**Q:** What **Windows Server version** runs on `192.168.56.30`, and **which port** answers Kerberos?

<details><summary>Solution</summary>

**Step — service + script scan the DC's core ports** (`-Pn` because a hardened DC may drop ICMP):
```bash
sudo nmap -Pn -sV -sC -p88,135,389,445,464,636,3268,3389,5985 192.168.56.30
```
**You should see:**
```
PORT     STATE SERVICE       VERSION
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: ...)
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: ceh.lab)
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server Microsoft Terminal Services
```
The `Product_Version: 10.0.17763` from Challenge 8 (or `-O`) maps the build to a release.
**Answer:** **Windows Server 2019** (build 10.0.17763); **Kerberos runs on `88/tcp`** (`kerberos-sec`). The 88/389/445/636/3268 cluster confirms it's a **domain controller**.

⚡ **Faster / alternative:** confirm the **ADCS** role — `nmap --script http-title -p443 192.168.56.30` returns `Microsoft Active Directory Certificate Services` when the web-enrollment (`/certsrv`) endpoint is present, the toehold for ESC1-style attacks.
</details>

---

### Challenge 10 — Open vs. filtered vs. a lying scan ⏱️ 8 min
**Q:** An Xmas scan of `192.168.56.30` reports **every port `closed`**. Is port 445 really closed on the DC? Decide and prove it.

<details><summary>Solution</summary>

**Step 1 — reproduce the misleading result:**
```bash
sudo nmap -sX -p445 192.168.56.30
```
**You should see:**
```
PORT    STATE  SERVICE
445/tcp closed microsoft-ds
```
**Step 2 — verify with a reliable scan** and ask *why* Nmap decided each state:
```bash
sudo nmap -sS -p445 --reason 192.168.56.30
```
**You should see:**
```
PORT    STATE SERVICE      REASON
445/tcp open  microsoft-ds syn-ack ttl 128
```
**Answer:** **445 is genuinely OPEN.** The Xmas "closed" is a **false read**: Xmas/FIN/NULL rely on RFC 793 behavior (open = silence → `open|filtered`, closed = RST), but **Windows replies RST to *every* probe**, so those scans report everything `closed` on a Windows host — a classic exam trap. Trust the SYN scan's `syn-ack` reason. (Run the *same* Xmas scan against Linux `192.168.56.20` and open ports correctly show `open|filtered` — that's the intended behavior.)

⚡ **Faster / alternative:** to tell a *real* firewall drop from a closed port, use an **ACK scan** — `sudo nmap -sA -p445 192.168.56.30`: a returned RST = `unfiltered` (packet got through), silence = `filtered`. `-sA` maps firewall rules, not open ports.
</details>

---

## Score yourself
Log each challenge as you finish:

| Result | Meaning | Action |
|---|---|---|
| ✅ | Correct answer **under** the time target, no Solution peeked | Move on |
| ⚠️ | Correct but **over** time | Re-drill until you're under target |
| ❌ | Needed the Solution to get the answer | Re-run it cold tomorrow |

When Challenges 1–10 are all ✅ cold, recon/scanning won't cost you exam clock — you'll have the *map* in the first few minutes and can spend your 6 hours on the exploiting. Record ✅/⚠️/❌ in [`../../PROGRESS.md`](../../PROGRESS.md).

## Sources
- Nmap Reference Guide (the whole book) — https://nmap.org/book/
- Nmap port-scanning techniques — https://nmap.org/book/man-port-scanning-techniques.html
- Nmap Scripting Engine (NSE), incl. `ftp-anon`, `rdp-ntlm-info`, `smb-os-discovery` — https://nmap.org/book/nse.html
- Nmap host discovery — https://nmap.org/book/man-host-discovery.html
- CEH companion — [Module 03 — Scanning Networks](../../modules/03-scanning-networks/README.md) · [`kali/05-nmap-scanning.md`](../../kali/05-nmap-scanning.md)
