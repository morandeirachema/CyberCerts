# Module 16 — Hacking Wireless Networks · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## 802.11 basics
- **802.11** is the Wi-Fi family. Know band + generation name:
  - **a** (5 GHz, 54 Mbps) · **b** (2.4 GHz, 11 Mbps) · **g** (2.4 GHz, 54 Mbps).
  - **n = Wi-Fi 4** (2.4/5 GHz, MIMO) · **ac = Wi-Fi 5** (5 GHz, MU-MIMO) · **ax = Wi-Fi 6/6E** (adds 6 GHz).
- **SSID** = network name; **BSSID** = the AP's MAC. An AP beacons its SSID/channel.
- Management/control/data are the three frame types. **Deauth and beacons are management frames** — historically *unauthenticated*, which is why they can be spoofed.

## Encryption / auth evolution (the core exam table)
| Protocol | Cipher | Key mgmt | Fatal / notable weakness |
|---|---|---|---|
| **WEP** | RC4 + 24-bit IV | Static shared key | **Broken by design** — tiny IV space reuses → keystream leaks → crack in minutes |
| **WPA** | **TKIP** (RC4) | PSK or 802.1X | Stopgap; MIC/replay weaknesses, still RC4 |
| **WPA2** | **CCMP/AES** | PSK or 802.1X | Capture 4-way handshake → **offline** PSK crack; KRACK (nonce reuse) |
| **WPA3** | GCMP/AES, **SAE** (Dragonfly) | SAE (PSK) or 802.1X | Forward secrecy, resists offline dictionary; Dragonblood side-channels (concept) |

- **WEP is broken** — the flaw is the **24-bit IV** (too small → IVs repeat), *not* "RC4 is bad on its own." That IV size is the exam answer.
- **WPA2-PSK is not cracked on the wire** — you capture the **4-way handshake** (or a **PMKID**) and attack the passphrase **offline**. Strength = passphrase entropy.
- **WPA3-SAE** replaces the PSK exchange with **Simultaneous Authentication of Equals** (a PAKE): captured traffic no longer yields an offline-crackable blob, and it adds **forward secrecy**.

## The WPA2 4-way handshake (what you actually capture)
- Both sides already share the **PMK** (Pairwise Master Key), derived from **PSK + SSID** (PBKDF2).
- The handshake derives the **PTK** (Pairwise Transient Key) using PMK + ANonce + SNonce + both MACs.
  1. AP → Client: **ANonce**
  2. Client → AP: **SNonce + MIC**
  3. AP → Client: **GTK + MIC**
  4. Client → AP: **ACK**
- **Capturing messages 2 and 3 (the MICs)** is what lets you brute-force offline: guess passphrase → derive PMK/PTK → recompute MIC → compare. Match = correct passphrase.

## Capture → offline crack workflow
- Force a handshake by **deauthing your own client** so it reconnects, then capture with airodump-ng.
- Or grab a **PMKID** (clientless — no deauth needed) from the AP's first EAPOL frame.
- Convert the capture and crack on GPU: **`hashcat -m 22000`** (the modern combined WPA/WPA2/PMKID mode that replaced the older `2500` handshake and `16800` PMKID modes). **Memorize 22000.**

## Attacks to name on sight
| Attack | What it does | Needs a client? | Tool |
|---|---|---|---|
| **Deauth** | Spoofed deauth frames force reconnect (capture handshake or DoS) | Yes (to reconnect) | aireplay-ng |
| **PMKID** | Grabs RSN PMKID from first EAPOL frame — **no client/handshake** | No | hcxdumptool |
| **Evil twin** | Clone a *legit* SSID to lure clients, then MITM / capture creds | Yes (victim) | bettercap, hostapd |
| **Rogue AP** | *Unauthorized* AP plugged into the network (backdoor into the LAN) | No | any AP |
| **WPS PIN brute** | Brute the 8-digit WPS PIN (effectively ~11k tries) | No | reaver / bully |
| **WPS Pixie-Dust** | Offline attack on weak WPS nonce RNG | No | reaver `-K` / bully `-d` |

- **Evil twin vs. rogue AP:** an **evil twin** *impersonates a known SSID* to fool clients; a **rogue AP** is any *unauthorized* AP attached to your network. Overlapping but not identical — the evil twin is a social/MITM lure, the rogue AP is an unsanctioned entry point.
- **WPS weakness:** the PIN is validated in **two halves**, collapsing the search space to ~11,000 tries; **Pixie-Dust** exploits weak nonce generation to recover the PIN *offline*. Fix: **disable WPS**.

## aircrack-ng suite (tool → role)
| Tool | Role |
|---|---|
| **airmon-ng** | Put the adapter into (and out of) **monitor mode** (`start`/`stop`) |
| **airodump-ng** | **Scan/capture** — survey APs, lock a channel, write the `.cap` |
| **aireplay-ng** | **Inject** frames — deauth, ARP replay (WEP), fake auth |
| **aircrack-ng** | **Crack** the captured WEP IVs or WPA/WPA2 handshake against a wordlist |

## Enterprise: 802.1X / EAP-TLS
- **WPA2/WPA3-Enterprise** uses **802.1X** with a **RADIUS** server — per-user/per-device auth instead of one shared PSK.
- **EAP-TLS** is the strong method: **mutual certificate** auth (client *and* server certs). No shared passphrase to capture-and-crack.
- The client validating the **RADIUS server certificate** is what defeats an **evil twin** — it won't trust the clone's cert.
- Avoid weak enterprise EAP (**PEAP/MSCHAPv2**) for privileged SSIDs — the challenge-response is crackable offline.

## 802.11w — Protected Management Frames (PMF)
- **802.11w/PMF** cryptographically protects management frames, so **spoofed deauth/disassoc frames are rejected**. It is the direct answer to "how do I stop deauth?"
- **Mandatory in WPA3**, optional in WPA2. It blocks the deauth that feeds handshake capture and deauth-DoS.
- **KRACK ≠ passphrase attack** — it's a **key-reinstallation** flaw in the 4-way handshake (forces nonce reuse), fixed by **patching clients**, not by changing the PSK.

## PAM / privileged-access angle
- A **PSK is a shared credential** — it can't be attributed to a person, rotated per-user, or revoked without changing it for everyone. Privileged networks belong on **802.1X/EAP-TLS**, never a passphrase.
- Cracking a handshake is only step one — the attacker really wants the **network-device admin credentials** (AP / WLC / switch) behind the SSID. **Vault and rotate those** so a cracked handshake still surrenders no standing infrastructure creds.
- **Vault the RADIUS account and its shared secret**; broker device administration (PSM) instead of direct admin to APs/controllers.
- Put admin access on a **segmented SSID/VLAN behind NAC**; enforce **PMF (802.11w)**; never allow privileged/jump access over a PSK network.

## Top traps
- **WEP flaw = the 24-bit IV**, not "RC4 is inherently broken." IV reuse leaks keystream.
- **WPA2-PSK is cracked *offline*** — "capture then dictionary attack" always means offline; nothing is broken on the wire.
- **TKIP vs. CCMP:** WPA → **TKIP** (RC4-based); WPA2 → **CCMP/AES**; WPA3 → **SAE** (Dragonfly) with GCMP. Don't swap them.
- **Hashcat WPA = `-m 22000`** (superset of the old `2500` and `16800`).
- **PMKID needs no client and no deauth** — that's its whole selling point over the handshake attack.
- **802.11w/PMF** stops deauth; **EAP-TLS server-cert validation** stops the evil twin.
- **KRACK** targets the *handshake protocol* (nonce reinstallation), not the passphrase — fixed by patching.
- **Evil twin = impersonate a known SSID**; **rogue AP = unauthorized AP on the network.** Don't conflate them.
