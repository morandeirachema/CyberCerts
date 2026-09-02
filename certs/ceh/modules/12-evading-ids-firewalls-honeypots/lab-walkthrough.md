# Module 12 — Evading IDS, Firewalls & Honeypots · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab against **your own** environment only (the lab in [`../../labs/`](../../labs/README.md) — see [`../../labs/topology.md`](../../labs/topology.md)). Each step gives the command, what you should observe, a hint, and the defender/PAM takeaway. Outputs shown are **representative** — yours will differ.

**Goal:** stand up an IDS, watch a plain scan light it up, then re-run with evasion flags and see **which alerts go quiet and which behavioral tells remain**. Evasion moves the evidence; it rarely erases it.

**Hosts:** Kali `192.168.56.10` (attacker) · Metasploitable2 `192.168.56.20` (target) · **sniffing host** — the IDS sensor on the `192.168.56.0/24` host-only segment. You can run the sensor on a dedicated VM watching the host-only interface, or on the Kali box itself against its lab interface. Substitute your real interface name (`eth0`/`eth1`/`enp0s8`) wherever a command says `<IFACE>`.

**Prereqs:** lab is up (`labs/scripts/setup.sh`), you can ping `192.168.56.20`, and Suricata (or Snort) is installed on the sensor.

> Everything stays inside `192.168.56.0/24`. Never point these scans at anything you do not own.

---

## Part A — Stand up the IDS on the sniffing host

### A1. Start Suricata as an IDS and tail its alerts
```bash
# on the sniffing host
sudo suricata -c /etc/suricata/suricata.yaml -i <IFACE> &
sudo tail -f /var/log/suricata/eve.json | jq 'select(.event_type=="alert")'
```
**You should see** Suricata initialise (rule count loaded) and the `tail` sit idle, waiting for the first alert:
```
<info> - all 5 packet processing threads, 4 management threads initialized, engine started.
```
**Observe:** the sensor is now watching the wire. No alerts yet — nothing malicious has crossed the segment. Keep this `tail` window open; every scan in Part B should surface here.

<details><summary>Hint: prefer Snort, or no eve.json?</summary>To use Snort instead: `sudo snort -A console -q -c /etc/snort/snort.conf -i <IFACE>` and read alerts straight on the console. If `eve.json` never appears, confirm `eve-log` is enabled in `suricata.yaml` and that you passed the correct `-i` interface (`ip -br addr` lists them). Run `sudo suricata-update` once so a rule set is present.</details>

**Defender/PAM view:** this sensor is your out-of-band NIDS — it detects and alerts but does **not** block. On the privileged plane you would pair it with HIDS/EDR on every jump/bastion host and **alert if a sensor stops logging** (blinding a sensor is itself an attack).

### A2. Add a local SYN-scan rule so scans reliably fire
```bash
# append to the sensor's local rules, then reload
echo 'alert tcp any any -> $HOME_NET any (flags:S; msg:"LOCAL Possible SYN scan"; \
  detection_filter:track by_src, count 20, seconds 5; sid:1000012; rev:1;)' \
  | sudo tee -a /etc/suricata/rules/local.rules
sudo suricatasc -c reload-rules      # Snort: restart with the rule in local.rules
```
**You should see** a successful reload:
```
{"message": "done", "return": "OK"}
```
**Observe:** the rule fires when one source sends 20+ SYNs in 5s — exactly what a scan does. This is your **signature** baseline; Part B tests how each evasion flag affects it.

<details><summary>Hint: rule not firing later?</summary>Confirm `$HOME_NET` in `suricata.yaml` includes `192.168.56.0/24`, and that `local.rules` is listed under `rule-files`. A unique high `sid` (1000012) avoids clashing with the shipped rule set.</details>

**Defender/PAM view:** rule anatomy to remember — **header** (`alert tcp any any -> $HOME_NET any`) + **options** (`msg`, `flags`, `detection_filter`, `sid`, `rev`). Rate-based `detection_filter` is what evasion timing (`-T1`) is designed to slip under.

---

## Part B — Scan from Kali and read the alerts

Run each command from **Kali** and watch the sensor's `tail`/console after each one.

### B1. Baseline — a plain SYN scan (no evasion)
```bash
nmap -sS 192.168.56.20
```
**You should see** the local rule fire, plus likely ET SCAN signatures:
```
{"event_type":"alert","src_ip":"192.168.56.10","dest_ip":"192.168.56.20",
 "alert":{"signature":"LOCAL Possible SYN scan","signature_id":1000012}}
{"event_type":"alert","src_ip":"192.168.56.10","dest_ip":"192.168.56.20",
 "alert":{"signature":"ET SCAN Potential SYN Scan","category":"Attempted Recon"}}
```
**Observe:** the true source `192.168.56.10` is named cleanly, and the SYN burst trips the rate rule. This is the **loud, fully-detected** case — your yardstick for everything below.

<details><summary>Hint</summary>If nothing fires, generate more traffic with `-p 1-1000` so the SYN count clears the `count 20` threshold, and confirm the scan actually reached the target (`nmap` should report open ports like 21/22/80).</details>

**Defender/PAM view:** clean attribution to one source IP is the analyst's happy path. The evasions in B2–B6 each attack a *different* piece of this: the payload signature, the source attribution, or the rate.

### B2. Fragmentation (`-f`)
```bash
nmap -f -sS 192.168.56.20
```
**You should see** the rate/SYN rule still fire, but **payload/content signatures may fall silent**; some sensors emit a reassembly note instead:
```
{"event_type":"alert","alert":{"signature":"LOCAL Possible SYN scan","signature_id":1000012}}
{"event_type":"anomaly","anomaly":{"type":"stream","event":"stream.reassembly_overlap"}}
```
**Observe:** splitting packets into 8-byte fragments defeats signatures that inspect a **single packet**, but a sensor doing **full reassembly** still reconstructs the scan — and the fragmentation itself becomes a behavioral tell.

<details><summary>Hint</summary>Try `-ff` (16-byte) or `--mtu 16` (must be a multiple of 8) to vary fragment size. If Suricata swallows it silently, that is the point — check whether stream reassembly is enabled in `suricata.yaml`.</details>

**Defender/PAM view:** the control is **forcing IDS/IPS full reassembly** and NGFW normalization, and dropping overlapping fragments. Detection shifted from *content* to *behavior*.

### B3. Decoys (`-D`)
```bash
nmap -D RND:5 -sS 192.168.56.20
```
**You should see** the scan alert(s) fire, but now attributed to **several source IPs at once**:
```
{"event_type":"alert","src_ip":"10.0.0.7","alert":{"signature":"LOCAL Possible SYN scan"}}
{"event_type":"alert","src_ip":"172.16.4.9","alert":{"signature":"LOCAL Possible SYN scan"}}
{"event_type":"alert","src_ip":"192.168.56.10","alert":{"signature":"LOCAL Possible SYN scan"}}
```
**Observe:** detection did **not** drop — the scan is still flagged. What changed is **attribution**: five decoys plus your real IP pollute the source field, so the analyst can't tell which host is real from the alert alone.

<details><summary>Hint</summary>Use explicit decoys to see your own IP hidden in the list: `nmap -D 192.168.56.31,ME,192.168.56.50 -sS 192.168.56.20`. `ME` marks your true position.</details>

**Defender/PAM view:** correlate on the host that actually **completed** connections (only the real source gets return traffic); NetFlow/session baselining strips the decoys. Decoys defeat *attribution*, not *detection*.

### B4. Source-port spoofing (`-g 53`)
```bash
nmap -g 53 -sS 192.168.56.20
```
**You should see** the scan still detected, now sourced from **port 53**:
```
{"event_type":"alert","src_ip":"192.168.56.10","src_port":53,"dest_ip":"192.168.56.20",
 "alert":{"signature":"LOCAL Possible SYN scan","signature_id":1000012}}
```
**Observe:** the IDS still fires, but this flag targets a **firewall**, not the sensor: a stateless ACL that "allows anything from port 53" would wave these packets through. Against a stateful, default-deny firewall it buys nothing.

<details><summary>Hint</summary>Try `-g 80` and `-g 443` too. If you have a packet filter in the lab, add a naive `allow src-port 53` rule and watch the spoofed scan pass, then switch to stateful and watch it blocked.</details>

**Defender/PAM view:** **never trust the source port.** Default-deny egress + stateful rules evaluate the *destination service* and flow direction, so a packet claiming to be "from DNS" gets no free pass.

### B5. Payload padding (`--data-length`)
```bash
nmap --data-length 25 -sS 192.168.56.20
```
**You should see** the SYN/rate rule still fire; any **length-based content signature** may go quiet:
```
{"event_type":"alert","alert":{"signature":"LOCAL Possible SYN scan","signature_id":1000012}}
```
**Observe:** appending 25 random bytes changes packet size and can break signatures keyed on an exact length or payload, without affecting the flags-based rule.

<details><summary>Hint</summary>Vary the length (e.g. `--data-length 100`) and combine with `-f` to stack fragmentation and padding. A flags-only rule like ours is immune to length changes by design — good to confirm.</details>

**Defender/PAM view:** don't rely on brittle length/exact-content signatures alone; behavioral and flow rules are far harder to pad around.

### B6. Slow timing (`-T1`)
```bash
nmap -T1 -sS 192.168.56.20
```
**You should see** the **rate-based rule stop firing**, even though the scan completes:
```
# (tail stays quiet — no "LOCAL Possible SYN scan" within the 5s window)
```
**Observe:** `-T1` ("sneaky") spaces probes far enough apart that the `count 20, seconds 5` threshold is never met. The scan still happens — you just slid **under** the rate rule. This is the clearest "went dark" case in the lab.

<details><summary>Hint</summary>Compare against `-T4`/`-T5` (fast) to see the rule fire hard again, and try `--scan-delay 2s` for the same slow effect. To catch slow scans, widen the window (e.g. `count 20, seconds 600`) — at the cost of memory and latency.</details>

**Defender/PAM view:** rate-based detection is a trade-off — tight windows miss slow scans, wide windows cost state. This is why **anomaly/flow baselining** and long-horizon correlation matter for low-and-slow recon around privileged assets.

---

## Part C — Which evasions changed detection?

| nmap flag | What it attacks | Did the scan alert still fire? | What changed |
|---|---|---|---|
| *(baseline `-sS`)* | — | **Yes** (loud) | Clean attribution to one source |
| `-f` fragment | Payload signatures | **Yes**, if reassembly on | Content sig may go quiet; frag becomes the tell |
| `-D` decoys | Source **attribution** | **Yes** | Real IP buried among spoofed decoys |
| `-g 53` source port | **Firewall** ACLs | **Yes** | Bypasses stateless "trust port 53" rules only |
| `--data-length` padding | Length/content signatures | **Yes** (flags rule) | Length-based sigs may miss |
| `-T1` slow timing | **Rate** thresholds | **No** (went quiet) | Slid under `count/seconds`; scan still ran |

**What you should conclude:** most evasions did **not** make the scan invisible — they moved the evidence off a **payload signature** and onto a **behavioral** signal (fragmentation storms, decoy spray, odd source port, timing). Only rate evasion (`-T1`) actually silenced our rule, and even that leaves a long-horizon flow pattern. Layer signature **and** anomaly detection, and force full reassembly, so evasion has nowhere clean to hide.

## Cleanup
```bash
# on the sensor: stop Suricata/Snort and remove the local rule
sudo pkill -f suricata          # or Ctrl-C the Snort console
sudo sed -i '/sid:1000012/d' /etc/suricata/rules/local.rules
# on Kali: nothing persists from the scans
```

## Record it
Log the commands, which alerts fired or went quiet, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
