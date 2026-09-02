# Module 10 — Denial-of-Service · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab against **your own** disposable lab only (the isolated VirtualBox/Docker lab in [`../../labs/`](../../labs/README.md) — see [`../../labs/topology.md`](../../labs/topology.md)). Each step gives the command, what you should see, what to observe, a hint, and the defender/PAM takeaway. Outputs shown are **representative** — yours will differ.

> ⚠️ **STOP — READ THIS.** DoS/DDoS against any system you do not own is a **crime** (CFAA / Computer Misuse Act equivalents) — no exceptions, no "just testing." These techniques also disrupt **shared** infrastructure. Run everything **only** against a **dedicated, disposable target on the isolated `192.168.56.0/24` segment or a localhost container you can afford to crash** (Kali `192.168.56.10`, Metasploitable2 `192.168.56.20`). **Never** point any of this at the internet, a cloud VM, a home router, a shared link, or a third party. LOIC/HOIC are named for **recognition only** — do not fire them at anything.

**Goal:** feel each of the three DoS categories map to a specific resource — the **table** (SYN flood), the **app** (Slowloris-style), and the **pipe** (amplification math) — and watch a matching control turn the outage back into uptime.

**Targets:** Kali attacker `192.168.56.10` · Metasploitable2 disposable target `192.168.56.20`.

**Prereqs:** lab is up, you can `ping 192.168.56.20` from Kali, and `hping3` is installed (`sudo apt install hping3`). Keep a **second terminal on the target** to watch sockets. Snapshot the target VM first so you can roll back.

---

## Part A — SYN flood: fill the connection table, then defend it

### A1. Baseline the target's sockets
Run this **on the target** (`192.168.56.20`) in a second terminal and leave it running:
```bash
watch -n1 'ss -ant state syn-recv | wc -l'
```
**You should see** a steady low number (near **0**) — no half-open connections under normal load.

**Observe:** this is your normal baseline for the TCP backlog. Everything in Part A is about watching this number climb.

<details><summary>Hint if <code>ss</code> shows nothing</summary>On older targets use <code>netstat -ant | grep SYN_RECV | wc -l</code>. The state name is <code>SYN-RECV</code> (dash) for <code>ss</code> and <code>SYN_RECV</code> (underscore) for <code>netstat</code>.</details>

### A2. Launch the SYN flood from Kali
From **Kali** (`192.168.56.10`), against the **disposable** target only:
```bash
# -S SYN flag, -p 80 target port, --flood = as fast as possible, --rand-source spoofs source IPs
sudo hping3 -S -p 80 --flood --rand-source 192.168.56.20
```
**You should see** hping3 print `HPING 192.168.56.20 ... --flood mode, no replies will be shown` and then appear to hang — that is the flood running.

**Observe:** flip to the target's `watch` window — the SYN-RECV count **shoots up** and stays high as half-open connections pile up. Try loading the target's web service; it becomes **slow or unresponsive**. You have exhausted the **connection table** (protocol/state category), not the bandwidth.

<details><summary>Hint: count not climbing?</summary>Make sure a service is actually listening on the port you chose (<code>-p 80</code>). On Metasploitable, port 80 (Apache) and 21/22/23 are open. Confirm with <code>nc -nv 192.168.56.20 80</code> from Kali before flooding.</details>

**Defender/PAM view:** the detection signal is a spike in **SYN-RECV / half-open connections** with the backlog dropping new clients — see the mapping in [`../../defender-pam/`](../../defender-pam/README.md). At scale the durable fix is **upstream filtering + connection rate limiting**, not host tuning.

### A3. Apply the control — SYN cookies
Stop the flood (Ctrl-C on Kali). On the **target**, enable SYN cookies, then re-run A2:
```bash
# on the target
sudo sysctl -w net.ipv4.tcp_syncookies=1
```
**You should see** `net.ipv4.tcp_syncookies = 1`. Re-launch the A2 flood from Kali and watch the target's `watch` window.

**Observe:** the SYN-RECV count **no longer runs away** and the service keeps answering — the kernel encodes handshake state into the SYN-ACK and allocates a backlog slot only when a valid ACK returns. **You just demonstrated SYN cookies: the defense works without enlarging the backlog.**

<details><summary>Hint: make it persistent</summary>The <code>sysctl -w</code> change is runtime-only. To keep it, add <code>net.ipv4.tcp_syncookies=1</code> to <code>/etc/sysctl.conf</code> and run <code>sudo sysctl -p</code>.</details>

**Defender/PAM view:** SYN cookies are the textbook answer for "defend a SYN flood **without** growing the backlog." Rate-limiting new connections per source (`iptables ... connlimit`) complements it. PAM angle: keep this box reachable via an **out-of-band** path so you can toggle the control even while the data-plane is saturated — [`../../defender-pam/pam-architecture.md`](../../defender-pam/pam-architecture.md).

---

## Part B — Slowloris-style slow request: exhaust the app's workers

### B1. Baseline a lab web server
Pick a **disposable lab web server** — a localhost DVWA container (`127.0.0.1:8081`) or the target's Apache. Load it in a browser and confirm it responds **instantly**. On the web host, watch worker/connection count:
```bash
# on the web host — count established connections to the web port
watch -n1 'ss -ant "( dport = :8081 or sport = :8081 )" | grep ESTAB | wc -l'
```
**You should see** a low, stable count.

**Observe:** this is your normal worker occupancy. Slowloris wins by pinning these slots open, not by flooding.

### B2. Open many slow, partial connections
Use the reference Slowloris script (holds connections open with **partial** HTTP headers) against your **own lab** web server only:
```bash
# lab-only, low connection count is enough to show the effect
slowloris 127.0.0.1 -p 8081 -s 200
```
**You should see** the script report it is keeping ~200 sockets alive, sending a header fragment on each every few seconds.

**Observe:** the ESTAB count climbs and **stays** high while using almost **no bandwidth**; new browser requests to the server start to **hang or time out** because every worker/thread is tied up waiting for headers that never complete. This is the **application-layer** category — resource exhaustion, not a pipe or a table.

<details><summary>Hint: server shrugs it off?</summary>Some servers (nginx, or Apache with the right MPM/mod_reqtimeout) resist this by design — that is the point of B3. If nothing happens, you may already be behind a protective proxy; test the raw origin server to see the effect first.</details>

**Defender/PAM view:** detection is **many slow/half-open HTTP connections and high rps from few IPs at low bandwidth**. The fix is a **reverse proxy with connection/header timeouts**, per-IP connection caps, and a WAF — see [`../../defender-pam/`](../../defender-pam/README.md).

### B3. Apply the control — timeouts / reverse proxy
Put a connection/header timeout in front (e.g. Apache `mod_reqtimeout`, or an nginx reverse proxy), then repeat B2.
```bash
# example: Apache mod_reqtimeout drops connections that dribble headers
# RequestReadTimeout header=20-40,MinRate=500  (in the vhost config), then reload
sudo a2enmod reqtimeout && sudo systemctl reload apache2
```
**You should see** the slow connections get **cut off** once they miss the minimum header-completion rate; the ESTAB count stops climbing and the site stays responsive.

**Observe:** the attack still *runs*, but the payoff is gone — the server reclaims workers faster than Slowloris can pin them. **You just demonstrated L7 connection-timeout mitigation.**

**Defender/PAM view:** front the origin with a hardened reverse proxy / WAF and enforce per-IP limits — [`../../defender-pam/pam-architecture.md`](../../defender-pam/pam-architecture.md). PAM angle: the proxy is now a resource that **must survive**, so give it QoS priority and keep it off the flooded segment.

---

## Part C — Amplification math: why spoofing turns a trickle into a flood

You will **not** run a reflection attack (that would abuse third parties). Instead, work the arithmetic that makes it dangerous.

### C1. Compute an amplification factor
```
amplification factor = response size ÷ request size
```
Worked examples (representative figures — memorize the *ranking*, not the exact numbers):

| Protocol | Request | Typical response | Factor |
|---|---|---|---|
| DNS (ANY/large TXT) | ~60 bytes | ~3,000 bytes | ~50× |
| NTP (`monlist`) | ~8 bytes | ~4,000+ bytes | ~500× |
| memcached (UDP :11211) | ~15 bytes | ~750 KB+ | ~10,000–51,000× |

**You should see** that a single attacker with a **1 Mbps** uplink, using memcached reflectors at ~10,000×, could in principle direct on the order of **~10 Gbps** at a victim — the multiplier, not the attacker's own link, is the threat.

**Observe:** the ranking to keep is **memcached ≫ NTP ≫ CLDAP/DNS ≫ SSDP.**

### C2. Why spoofing is the enabler
Reflection only works because the attacker forges the **victim's IP** as the source of each query, so every reflector's large reply is delivered to the victim. This requires **UDP**: it is connectionless, so there is **no handshake to complete** and the source address is never verified. TCP's three-way handshake would fail against a spoofed source, which is exactly why reflection uses UDP protocols.

**You should conclude:** the network-edge fix is **BCP38 / uRPF ingress filtering** — drop packets whose source address could not legitimately arrive on that interface, so spoofed queries never leave the origin network. Additionally, **close/patch open reflectors** (disable NTP `monlist`, don't expose memcached UDP 11211).

**Defender/PAM view:** volumetric reflection **cannot** be absorbed at the host — the upstream pipe fills first — so mitigation is pushed **upstream** to **CDN / anycast / cloud scrubbing**, with **autoscaling** to add capacity. Mapping in [`../../defender-pam/`](../../defender-pam/README.md).

---

## What you should conclude
Each attack maps to a specific resource, and each has a matching control that turns the outage back into uptime:

| You did / computed | Resource exhausted | The control that stops it |
|---|---|---|
| SYN flood (Part A) | Connection table (protocol/state) | SYN cookies + connection rate limiting |
| Slowloris-style slow request (Part B) | App workers/threads (L7) | Reverse proxy + connection/header timeouts, WAF |
| Amplification math (Part C) | Link bandwidth (volumetric) | BCP38/uRPF anti-spoofing, close reflectors, upstream CDN/anycast/scrubbing |
| Any of the above vs. the admin plane | Availability of management access | Out-of-band mgmt network, hardened jump hosts, break-glass, Vault HA/DR |

## Cleanup
```bash
# stop any running attack tools (Ctrl-C the hping3 / slowloris terminals)
# on the target, restore SYN cookies to its default if you changed it for testing
sudo sysctl -w net.ipv4.tcp_syncookies=1   # (leave enabled — this is the safe default)
# roll the disposable target VM back to your pre-lab snapshot if it became unstable
```

## Record it
Log commands, outputs, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
