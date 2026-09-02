# Drill Pack 06 — PCAP Forensics

> Pull secrets out of packet captures the way the Practical asks: *"what are the username and password in this pcap?"*, *"export the transferred file"*, *"crack this hash from the capture."* Every challenge has a **full solution** — the Wireshark GUI steps **and** the `tshark`/`tcpdump` command, what you should see, the exact answer, and a ⚡ faster note. Solve under the timer; expand the solution only when done or stuck.
>
> **Prereq:** generate the [challenge-lab](../challenge-lab/README.md) (`../challenge-lab/setup-challenges.sh`) so `~/ceh-practical-challenges/pcap/traffic.pcap` exists, and have the [lab](../../labs/README.md) Metasploitable2 (`192.168.56.20`, cleartext FTP) reachable. Recipes: [`../challenge-playbooks.md`](../challenge-playbooks.md) · concepts: [Module 08 — Sniffing](../../modules/08-sniffing/README.md) · tool drills: [`../../kali/12-sniffing-mitm.md`](../../kali/12-sniffing-mitm.md).
>
> Set these first so the commands paste clean (lab-only — every capture is your own traffic on `192.168.56.0/24`):
> ```bash
> C=~/ceh-practical-challenges   # challenge-lab artifacts
> IFACE=eth1                     # your lab (host-only) interface — confirm with: ip a
> T=192.168.56.20                # Metasploitable2
> ```

---

### 1. What are the username and password in `traffic.pcap`? ⏱️ 2 min · easy

<details><summary>Solution</summary>

An HTTP form login is cleartext — the credentials sit in the POST body.

**Wireshark:** open the file, right-click the `POST` packet → **Follow → HTTP Stream** (or **TCP Stream**). The request body appears in one readable window.
```bash
wireshark $C/pcap/traffic.pcap &
```
**tshark:** print the POST body directly, no GUI:
```bash
tshark -r $C/pcap/traffic.pcap -Y 'http.request.method=="POST"' -T fields -e http.file_data
```
**You should see:**
```
username=admin&password=Summer2025!&submit=Login
```
**Answer:** username `admin`, password `Summer2025!`

⚡ **faster:** the `tshark` one-liner reads the answer off in one shot — skip opening the GUI at all.
</details>

### 2. Which HTTP method and Host did the client use? ⏱️ 1 min · easy

<details><summary>Solution</summary>

**Wireshark:** click the request packet, expand **Hypertext Transfer Protocol** in the middle pane — the request line and headers are spelled out.

**tshark:** pull the method, host, and URI as fields:
```bash
tshark -r $C/pcap/traffic.pcap -Y http.request \
  -T fields -e http.request.method -e http.host -e http.request.uri
```
**You should see:**
```
POST	portal.ceh.lab	/login
```
**Answer:** method `POST`, Host `portal.ceh.lab`, path `/login`.

⚡ **faster:** field extraction (`-T fields -e …`) beats scrolling the packet-details tree when the question names the exact value it wants.
</details>

### 3. What is the server's response code — and where did it redirect the client? ⏱️ 1 min · easy

<details><summary>Solution</summary>

**Wireshark:** click the server's reply packet (source `192.168.56.50`), expand **Hypertext Transfer Protocol** → **Status Code**, or **Follow → HTTP Stream** to see both sides.

**tshark:** the response code, phrase, and `Location` header:
```bash
tshark -r $C/pcap/traffic.pcap -Y http.response \
  -T fields -e http.response.code -e http.response.phrase -e http.location
```
**You should see:**
```
302	Found	/dashboard
```
**Answer:** `302 Found`, redirecting to `/dashboard` (a `3xx` redirect after a login = success → the app hands the browser to the dashboard).

⚡ **faster:** filter `http.response` alone jumps straight to the reply; `http.response.code` is the whole answer.
</details>

### 4. Identify the plaintext protocol in a capture. ⏱️ 2 min · easy

<details><summary>Solution</summary>

Don't guess from ports — let Wireshark enumerate what's actually dissected. Cleartext protocols (HTTP, FTP, Telnet, SMTP, POP3, IMAP, SNMPv1/2c) carry readable payloads; TLS/SSH show only encrypted blobs.

**Wireshark:** **Statistics → Protocol Hierarchy** lists every protocol with byte/packet counts. **tshark:** the same from the CLI:
```bash
tshark -r $C/pcap/traffic.pcap -q -z io,phs        # protocol hierarchy statistics
```
**You should see** (for `traffic.pcap`) an `http` node under `tcp`; on the FTP capture from challenge 5 you'd see an `ftp` node instead.

**Answer:** name the cleartext protocol present — **HTTP** for `traffic.pcap` (**FTP** for your challenge-5 capture). If you only see `tls`/`ssh`, it's encrypted — nothing to read.

⚡ **faster:** `tshark -r cap -T fields -e frame.protocols | sort -u` dumps the protocol stack of every packet in one line.
</details>

### 5. Capture your OWN FTP login to `192.168.56.20` and recover the credentials. ⏱️ 4 min · medium

<details><summary>Solution</summary>

FTP (port 21) sends `USER`/`PASS` in the clear. Capture the session, then read it back.
```bash
sudo tcpdump -i $IFACE -w ~/lab/captures/ftp.pcap port 21   # Terminal 1 — start BEFORE you log in
ftp $T          # Terminal 2 — msfadmin / msfadmin, then: bye  (then Ctrl+C Terminal 1)
```
**Wireshark:** open the file, filter `ftp`, right-click → **Follow → TCP Stream** — the whole login is plain text. **tshark:** dump the control channel with `tshark -r ~/lab/captures/ftp.pcap -Y ftp`.

**You should see:**
```
Request: USER msfadmin
Response: 331 Please specify the password.
Request: PASS msfadmin
Response: 230 Login successful.
```
**Answer:** username `msfadmin`, password `msfadmin`.

⚡ **faster:** skip Wireshark entirely — `tcpdump -r ~/lab/captures/ftp.pcap -A | grep -Ei 'USER|PASS'` prints the creds from the raw file.
</details>

### 6. Recover just the FTP password with a one-line filter (no GUI). ⏱️ 1 min · medium

<details><summary>Solution</summary>

When the question wants *only* the password, target the exact packet that carries it — `ftp.request.command=="PASS"` — and print its argument.

**tshark:**
```bash
tshark -r ~/lab/captures/ftp.pcap -Y 'ftp.request.command=="PASS"' -T fields -e ftp.request.arg
tshark -r ~/lab/captures/ftp.pcap -Y 'ftp.request.command=="USER"' -T fields -e ftp.request.arg   # username too
```
**You should see:**
```
msfadmin
```
**Answer:** password `msfadmin` (username `msfadmin`).

⚡ **faster:** this *is* the fast path — one command, one field, no stream to eyeball. Memorize `ftp.request.command=="PASS"` for the exam.
</details>

### 7. Export a transferred file from a capture (File → Export Objects). ⏱️ 4 min · medium

<details><summary>Solution</summary>

Wireshark reassembles files that crossed the wire and lets you save them. **Capture a download** from the lab web server:
```bash
sudo tcpdump -i $IFACE -w ~/lab/captures/http-dl.pcap "tcp port 80 and host $T"   # Terminal 1
wget http://$T/index.php -O /dev/null            # Terminal 2 — pull any file, then Ctrl+C Terminal 1
```
**Wireshark:** **File → Export Objects → HTTP** — a list of every reassembled object; select one → **Save**. (Same menu offers **SMB**, **TFTP**, **FTP-DATA**.) **tshark:** carve them all in one command:
```bash
mkdir -p /tmp/objects
tshark -r ~/lab/captures/http-dl.pcap --export-objects http,/tmp/objects
ls /tmp/objects        # then open/cat the file you want
```
**You should see** the transferred file(s) written out; read the contents to get the answer.

**Answer:** the recovered file's contents / filename (whatever the question asks for).

⚡ **faster:** `tshark --export-objects http,<dir>` dumps every object without a single click — or drop the pcap into **NetworkMiner**, whose **Files** tab auto-carves everything it saw.
</details>

### 8. Extract and crack a NetNTLMv2 hash from a capture. ⏱️ 6 min · hard

<details><summary>Solution</summary>

A Windows host authenticating over SMB/HTTP leaks a **NetNTLMv2** challenge/response — crackable offline into the user's password (hashcat mode **5600**).

**Capture the auth** (LLMNR/NBT-NS poisoning — see [`../../kali/12-sniffing-mitm.md`](../../kali/12-sniffing-mitm.md)):
```bash
sudo responder -I $IFACE -wv        # answers the broadcast and records the NetNTLMv2
# trigger from a Windows lab host: browse a bad path  \\fileserv01\share
# Responder prints the hash and saves it under /usr/share/responder/logs/
```
**From a raw pcap instead:** filter `ntlmssp` — the **NTLMSSP_AUTH** message holds the username/domain + NTLMv2 response, the preceding **NTLMSSP_CHALLENGE** holds the server challenge. Reassembling those into hashcat's `user::DOMAIN:challenge:proof:blob` by hand is fiddly, so let a tool do it: **NetworkMiner**'s **Credentials** tab lists NTLM challenge/responses ready to crack. Then crack:
```bash
hashcat -m 5600 netntlmv2.txt /usr/share/wordlists/rockyou.txt --show   # add --show to print the result
```
**You should see** hashcat print the username and the recovered plaintext once it's in the wordlist.

**Answer:** the cracked plaintext password of the captured account.

⚡ **faster:** Responder writes a hashcat-ready `user::DOMAIN:…` line — feed the log file straight to `hashcat -m 5600`; no manual reassembly.
</details>

### 9. Pull every cleartext credential from a capture at once. ⏱️ 3 min · hard

<details><summary>Solution</summary>

Instead of hunting protocol by protocol, ask the tooling to surface all detected credentials.

**tshark** has a built-in credentials tap (FTP, HTTP basic, IMAP, POP, SMTP):
```bash
tshark -q -z credentials -r ~/lab/captures/ftp.pcap
```
**You should see** a table of packet number, protocol, and the username/password it flagged:
```
Packet   Protocol   Username   Info
5        FTP        msfadmin   Username in packet: 5
7        FTP        msfadmin   Password in packet: 7
```
**Wireshark:** the same is under **Statistics → Follow** per-stream, and older builds expose **Tools → Credentials**.

**Answer:** every credential the capture leaked (e.g. FTP `msfadmin`/`msfadmin`, plus any HTTP basic auth).

⚡ **faster:** drop the pcap into **NetworkMiner** — its **Credentials** tab auto-lists FTP/HTTP/SMB creds and its **Files** tab carves transferred files, all with zero commands. One GUI, whole-capture triage.
</details>

---

## Score yourself

| Result | Meaning |
|---|---|
| ✅ | Solved cold, under the time target, GUI **and** CLI path known |
| ⚠️ | Solved but slow, or needed a peek at the solution |
| ❌ | Couldn't produce the answer |

Re-drill anything not ✅. Exam-critical muscle memory: **Follow TCP/HTTP Stream**, `http.request.method=="POST"` + `http.file_data`, `ftp.request.command=="PASS"`, **File → Export Objects** / `--export-objects`, and `hashcat -m 5600` for a captured NetNTLMv2. All nine ✅ under time → move to the next pack in [`../drills/`](../drills/README.md) or a [simulated exam](../exams/README.md).

## Sources
- Wireshark — User Guide (Follow Stream, Export Objects, Statistics): https://www.wireshark.org/docs/wsug_html_chunked/
- Wireshark — Display filter reference: https://www.wireshark.org/docs/dfref/
- Wireshark — `tshark` manual: https://www.wireshark.org/docs/man-pages/tshark.html
- tcpdump — manual: https://www.tcpdump.org/manpages/tcpdump.1.html
- NetworkMiner (GUI pcap credential/file extractor): https://www.netresec.com/?page=NetworkMiner
- hashcat — example hashes (mode 5600, NetNTLMv2): https://hashcat.net/wiki/doku.php?id=example_hashes
