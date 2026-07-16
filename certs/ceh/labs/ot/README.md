# OT / ICS target range (Docker)

A turnkey, loopback-only range for **Module 18 (IoT and OT Hacking)** — two
industrial protocols that ship with **no authentication by design**:

| Service | Port (host) | Real-world port | What it demonstrates |
|---|---|---|---|
| **MQTT** (eclipse-mosquitto) | `127.0.0.1:1883` | 1883 (TLS 8883) | Anonymous pub/sub — read and inject on every topic |
| **Modbus/TCP** (pymodbus sim) | `127.0.0.1:5020` | 502 | Unauthenticated register read (FC3) and **write** (FC6) |

This is the same lesson as [`../../modules/18-iot-and-ot-hacking/lab-walkthrough.md`](../../modules/18-iot-and-ot-hacking/lab-walkthrough.md),
but containerised so it comes up in one command instead of hand-installing
`mosquitto` and `pymodbus`. Both clients ship **inside the images**, so you need
nothing on the host but Docker.

> ⛔ **OT SAFETY.** Never point these tools at a real PLC/ICS/IoT device you do
> not own on an isolated bench. A stray Modbus write or aggressive scan can trip
> a safety system, damage equipment, or hurt people. Everything below targets
> **your own loopback containers only.**

---

## Bring it up

```bash
docker compose -f labs/ot/docker-compose.yml up -d --build
docker compose -f labs/ot/docker-compose.yml ps
```

## 1. MQTT — pub/sub with no identity

Subscribe to **every** topic with the multi-level wildcard `#`, then inject a
spoofed reading from a second client. Both run inside the broker image:

```bash
# terminal 1 — read everything on the bus (no credentials)
docker exec -it ceh-mqtt mosquitto_sub -t '#' -v

# terminal 2 — publish a legit value, then a forgery
docker exec ceh-mqtt mosquitto_pub -t 'plant/sensor/temp' -m '21.4'
docker exec ceh-mqtt mosquitto_pub -t 'plant/sensor/temp' -m 'spoofed'
```

**You should see** both messages appear in terminal 1 immediately:

```
plant/sensor/temp 21.4
plant/sensor/temp spoofed
```

**Observe:** one anonymous subscribe to `#` reads all traffic; any anonymous
publish injects on any topic. No username, no password, no TLS.

**Defender / PAM view:** require broker auth + TLS (**8883**) and put the broker
in an OT zone reachable only through a brokered jump host (IEC 62443
zones/conduits). Vault + rotate the broker credential (CyberArk CPM); no shared
anonymous access. Flip `mosquitto.conf` to its commented "FIXED state" to watch
the control work.

## 2. Modbus — read then WRITE with no auth

Read holding registers (FC3), write one (FC6), and confirm the change — all
unauthenticated. The client runs inside the simulator image (`pymodbus` is
already installed):

```bash
docker exec ceh-modbus python - <<'PY'
from pymodbus.client import ModbusTcpClient
c = ModbusTcpClient("127.0.0.1", port=5020); c.connect()
print("FC3 read :", c.read_holding_registers(0, 10).registers)
c.write_register(1, 42)                                 # FC6 write — no login
print("FC3 after:", c.read_holding_registers(0, 10).registers)
c.close()
PY
```

**You should see** register 1 change to 42 with no authentication step:

```
FC3 read : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FC3 after: [0, 42, 0, 0, 0, 0, 0, 0, 0, 0]
```

**Observe:** a plain `write_register` (FC6) altered process state. On a real PLC
that same call could open a valve or stop a motor — which is why you only ever
do this against a simulator.

**Scan it like the exam expects** (loopback only):

```bash
nmap -sV -p 5020 --script modbus-discover 127.0.0.1     # real PLCs: -p 502
nmap -p 1883,8883 -sV 127.0.0.1                          # MQTT fingerprint
```

**Defender / PAM view:** keep Modbus on an isolated, monitored segment; a
protocol-aware firewall denies **write** function codes (FC5/6/15/16) from IT.
Every engineer/vendor path into L0/L1 goes through a **PSM/PSMP jump host in the
IDMZ** — JIT, MFA, approval, full session recording — never a flat, standing
route to the plant floor.

## What ties it together

Both "wins" exist because the protocol assumes a **trusted, isolated network**,
so the defense is *the network and the broker*, not the protocol. Map each
finding to the control in [`../../defender-pam/`](../../defender-pam/) and place
each component on the Purdue model (treat OT as crown-jewel **Tier 0**).

## Tear down

```bash
docker compose -f labs/ot/docker-compose.yml down -v
```
