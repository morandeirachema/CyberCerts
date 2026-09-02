# Module 18 — IoT and OT Hacking · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab against **your own** environment only. Each step gives the command, what you should observe, a hint, and the defender/PAM takeaway. Outputs shown are **representative** — yours will differ. See [`../../labs/`](../../labs/) and [`../../labs/topology.md`](../../labs/topology.md).

> ⛔ **OT SAFETY — read this first.** Never scan, connect to, or write to **any real ICS/OT device, PLC, or IoT product you do not own** on an isolated bench. A stray Modbus write or an aggressive scan can trip a safety system, damage equipment, or hurt people. Everything below targets **your own loopback simulators, your own firmware images, and Shodan's *index* — which you query, never connect to.** If you see a Shodan/Censys result, you look at the *count and metadata only*; you do **not** open a session to it.

**Goal:** feel *why* IoT/OT protocols are insecure by design — pub/sub with no auth, register read/write with no identity — then map each finding to the PAM control that contains it.

**Targets:** your own workstation only — `127.0.0.1` (loopback). No external host is contacted except Shodan's search API in Part A.

**Prereqs:** `mosquitto` + `mosquitto-clients` installed, Python with `pip install pymodbus`, `binwalk` installed, and (optional) a Shodan account/API key (`shodan init <KEY>`). A firmware image **you legally own** (e.g. from your own router vendor's download page) saved as `firmware.bin`.

> 💡 **Prefer one command?** Parts B and C are containerised in [`../../labs/ot/`](../../labs/ot/) — `docker compose -f labs/ot/docker-compose.yml up -d --build` gives you the MQTT broker and Modbus simulator with the clients already inside the images (no host install). Come back here for Part A (Shodan) and the firmware carving in C3.

---

## Part A — Passive exposure recon (query the INDEX, never connect)

### A1. Count internet-exposed Modbus and MQTT — from the index only
```bash
shodan count 'port:502 product:Modbus'      # how many exposed Modbus endpoints
shodan count 'port:1883'                      # how many exposed MQTT brokers
```
**You should see** a single integer per query — a population count, no connection made:
```
17432
289104
```
**Observe:** you learned the *scale of exposure* for protocols with no built-in auth **without sending a single packet to any device**. `shodan count` returns only the index tally; `shodan search` would add metadata — still index data, still no connection.

<details><summary>Hint if `shodan` isn't set up</summary>Run `shodan init <YOUR_API_KEY>` once. No key? Do the identical search in the web UI at https://www.shodan.io/ or https://censys.com/ and read the "Total results" number. Either way you are reading an **index**, never touching a device.</details>

**Defender/PAM view:** these are devices that should never be internet-reachable. The control is **segmentation + IEC 62443 zones/conduits** — Modbus/MQTT belong deep in OT, reachable only through a brokered jump host in the IDMZ, never NATed to the edge.

---

## Part B — Local MQTT lab: pub/sub with no identity

### B1. Start your own broker
```bash
mosquitto -v          # verbose broker on 127.0.0.1:1883 (leave running in terminal 1)
```
**You should see** the broker bind and log connections:
```
mosquitto version 2.x starting
Opening ipv4 listen socket on port 1883.
```
**Observe:** a default broker with no config accepts **anonymous** clients — no username, no password, no TLS.

### B2. Subscribe to every topic with the wildcard
```bash
# terminal 2
mosquitto_sub -h 127.0.0.1 -t '#' -v
```
**You should see** the client connect and wait, then (after B3) print every message on every topic:
```
lab/sensor/temp 21.4
lab/sensor/temp spoofed
```
**Observe:** `#` is the **multi-level wildcard** — one unauthenticated subscribe reads **all traffic** on the broker. This is passive interception with zero credentials.

### B3. Publish a spoofed reading (missing-auth pub/sub abuse)
```bash
# terminal 3 — first a legit-looking value, then the forgery
mosquitto_pub -h 127.0.0.1 -t 'lab/sensor/temp' -m '21.4'
mosquitto_pub -h 127.0.0.1 -t 'lab/sensor/temp' -m 'spoofed'
```
**You should see** both messages appear in the terminal-2 subscriber immediately.
**Observe:** any anonymous client can **inject** on any topic. A downstream controller subscribed to `lab/sensor/temp` would accept `spoofed` as truth — this is OWASP "insecure network services" in miniature: no auth means anyone can both **read and write** the entire message bus.

<details><summary>Hint if the subscriber sees nothing</summary>Confirm the broker is still running in terminal 1 and that all three commands use `-h 127.0.0.1`. If your distro ships a hardened `mosquitto.conf` with `allow_anonymous false`, that's the *fixed* state — temporarily test with a config that sets `allow_anonymous true` **on loopback only** to observe the insecure behavior, then revert.</details>

**Defender/PAM view:** require broker authentication + TLS (**8883**), and architecturally put the broker inside an OT zone reachable only via a brokered path. Detection: anonymous subscribes to `#`, or publishes from an unexpected client ID. PAM lever: **vault the broker/service credential** and rotate it (CyberArk CPM); no shared anonymous access.

---

## Part C — Local Modbus lab + firmware secrets

### C1. Start a Modbus simulator on loopback
```bash
# terminal 1 — CLI varies by pymodbus version
python -m pymodbus.server --host 127.0.0.1 --port 5020
```
**You should see** the simulator bind to loopback and wait for a client:
```
Server(TCP) listening.
```
**Observe:** the simulator speaks Modbus with **no login prompt** — exactly like the real protocol.

### C2. Read holding registers (FC3), then write one (FC6 — simulator only)
```bash
# terminal 2
python - <<'PY'
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient('127.0.0.1', port=5020); c.connect()
print("FC3 read :", c.read_holding_registers(0, 10))   # function code 3 — read
c.write_register(1, 42)                                  # function code 6 — write (SIM ONLY)
print("FC3 after:", c.read_holding_registers(0, 10))    # confirm the change
c.close()
PY
```
**You should see** ten register values, then the same set with index 1 changed to 42:
```
FC3 read : ReadHoldingRegistersResponse (10 registers)
FC3 after: [0, 42, 0, 0, 0, 0, 0, 0, 0, 0]
```
**Observe:** there was **no authentication, no authorization, and no encryption** — a plain `write_register` (FC6) altered process state. On a real PLC this same call could open a valve or stop a motor, which is why **you only ever do this against a simulator**.

<details><summary>Hint if the connection is refused</summary>Confirm the server terminal shows "listening" and that client and server use the same port (`5020` here). If `python -m pymodbus.server` isn't available in your version, use the packaged `pymodbus.simulator` or a `StartTcpServer(...)` script — the FC3/FC6 client calls are unchanged.</details>

### C3. Carve a firmware image you own for hardcoded secrets
```bash
binwalk firmware.bin                # identify embedded filesystems/signatures
binwalk -e firmware.bin             # extract the rootfs
grep -rniE 'password|api[_-]?key|BEGIN .*PRIVATE' _firmware.bin.extracted/
```
**You should see** binwalk list signatures (e.g. `Squashfs filesystem`, `gzip`), extract a rootfs, and grep surface any embedded secrets:
```
DECIMAL   HEXADECIMAL  DESCRIPTION
0x...     ...          Squashfs filesystem, little endian
_firmware.bin.extracted/squashfs-root/etc/shadow:root:$1$...
```
**Observe:** IoT firmware routinely ships with **hardcoded credentials/keys** — the same OWASP #1 (default/weak/hardcoded passwords) that Mirai weaponized, but baked into the image.

<details><summary>Hint if extraction is empty</summary>You need a firmware image you legally own (download from your own device vendor). Some images are encrypted/packed — `binwalk` will show entropy near 1.0 and no filesystem; that's a finding in itself (the vendor obfuscated it), not a failure.</details>

**Defender/PAM view:** Modbus/firmware findings share one root cause — **implicit trust**. Controls: keep OT protocols on isolated, monitored segments (protocol-aware firewall denies write function codes from IT); require **signed firmware + secure boot**; and **vault/rotate device credentials** so a hardcoded secret in an image isn't a live key. Detection: unexpected FC5/6/15/16 writes, firmware hash/signature mismatch.

---

## What you should conclude
Every "win" above exists because the protocol assumes a **trusted, isolated network** — so the entire defense is *the network and the broker*, not the protocol.

| You did | Why it worked | The control that stops it |
|---|---|---|
| Counted exposed Modbus/MQTT via Shodan index | Devices NATed to the internet | Segmentation + IEC 62443 zones/conduits; never edge-reachable |
| Subscribed to `#` and injected on MQTT | Broker allows anonymous read/write | Broker auth + TLS (8883); brokered access; vault the credential |
| FC3 read + FC6 write on Modbus | No auth/authorization/crypto in the protocol | IT/OT segmentation; deny writes from IT; PSM/PSMP jump host into OT |
| Grepped firmware for hardcoded creds | Secrets baked into the image | Signed firmware + secure boot; vault/rotate device creds |

**PAM through-line:** treat OT as **crown-jewel Tier 0**. No human or vendor touches L0/L1 directly — every path goes through a **jump host in the IDMZ** with JIT, MFA, approval, and full session recording. Map these to [`../../defender-pam/`](../../defender-pam/).

## Cleanup
```bash
# stop the broker (terminal 1) and Modbus server (terminal 1/C1) with Ctrl-C
rm -rf _firmware.bin.extracted/          # remove extracted firmware rootfs
# if you set allow_anonymous true to observe B, revert mosquitto.conf now
```

## Record it
Log commands, outputs, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
