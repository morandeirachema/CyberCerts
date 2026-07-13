# Module 16 — Hacking Wireless Networks · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** WEP is considered broken. What is the *root* weakness an examiner expects you to name?

- A. RC4 is a fundamentally insecure cipher
- B. The 24-bit initialization vector (IV) is too small, so IVs repeat and leak keystream
- C. The pre-shared key is limited to 8 characters
- D. It uses a 4-way handshake that can be captured

<details><summary>Answer</summary>

**B. The 24-bit IV is too small.** WEP's IV space is tiny, so IVs collide quickly; passive collection plus a statistical attack recovers the key in minutes. Blaming "RC4" alone is the trap — RC4 is used correctly elsewhere; here it's the **IV reuse** that kills it. WEP has no 4-way handshake (that's WPA/WPA2).
</details>

---

**Q2.** Which pairing of protocol and cipher is correct?

- A. WPA2 → TKIP
- B. WPA → CCMP/AES
- C. WPA2 → CCMP/AES
- D. WEP → SAE

<details><summary>Answer</summary>

**C. WPA2 → CCMP/AES.** Memorize the ladder: **WEP** = RC4 + weak IV, **WPA** = **TKIP** (still RC4-based), **WPA2** = **CCMP/AES**, **WPA3** = **SAE**/GCMP. Options A and B swap WPA and WPA2's ciphers; SAE belongs to WPA3, not WEP.
</details>

---

**Q3.** In a WPA2-PSK attack, what specifically must you capture to enable an offline crack?

- A. The plaintext passphrase as it is typed
- B. The 4-way handshake (the EAPOL frames carrying the MIC)
- C. The AES session key from the AP's memory
- D. The DHCP lease of the client

<details><summary>Answer</summary>

**B. The 4-way handshake.** The EAPOL messages (especially 2 and 3) carry a **MIC** derived from the PMK (which comes from PSK + SSID). Offline you guess a passphrase → derive PMK/PTK → recompute the MIC → compare. The passphrase never travels in plaintext, and the session keys stay on the endpoints — you recompute them from a guess.
</details>

---

**Q4.** Why is WPA2-PSK cracking called an *offline* attack?

- A. The attacker must be disconnected from the internet
- B. Once the handshake is captured, guessing happens locally with no further AP interaction
- C. The AP goes offline during the attack
- D. It only works on powered-off access points

<details><summary>Answer</summary>

**B. Guessing happens locally after capture.** After you have the handshake (or a PMKID), every passphrase guess is computed on your own machine — no packets to the AP, no logs, no lockout. That is why it beats online guessing and why passphrase entropy is the only thing protecting you.
</details>

---

**Q5.** What is the defining advantage of the **PMKID** attack over the classic handshake capture?

- A. It cracks the passphrase without any wordlist
- B. It requires no connected client and no deauth — it's clientless
- C. It works against WPA3-SAE
- D. It recovers the passphrase instantly

<details><summary>Answer</summary>

**B. It is clientless — no client, no deauth needed.** The PMKID can be pulled from the AP's first EAPOL frame during association, so you don't have to wait for or deauth a victim. You *still* crack the passphrase offline with a wordlist (so A and D are wrong), and SAE is specifically designed to resist this class of attack (C is wrong).
</details>

---

**Q6.** What is the primary purpose of a **deauthentication** attack in a handshake-capture workflow?

- A. To permanently disable the access point
- B. To force a client to disconnect and reconnect, producing a fresh 4-way handshake to capture
- C. To brute-force the WPS PIN
- D. To decrypt AES traffic in real time

<details><summary>Answer</summary>

**B. Force a reconnect to capture the handshake.** Spoofed deauth frames knock the client off; when it re-associates it performs the 4-way handshake, which you sniff. (Deauth can also be used as a pure DoS.) It doesn't disable the AP permanently, has nothing to do with WPS, and does not decrypt traffic.
</details>

---

**Q7.** Which control most directly stops a spoofed-deauth attack?

- A. A longer WPA2 passphrase
- B. Disabling the SSID broadcast
- C. 802.11w Protected Management Frames (PMF)
- D. MAC address filtering

<details><summary>Answer</summary>

**C. 802.11w / PMF.** Deauth works because management frames were historically unauthenticated. PMF cryptographically protects them, so spoofed deauth/disassoc frames are rejected. It is **mandatory in WPA3**. A longer passphrase helps the *crack* resistance, not the deauth; hiding the SSID and MAC filtering are trivially bypassed.
</details>

---

**Q8.** What distinguishes an **evil twin** from a **rogue AP**?

- A. An evil twin impersonates a legitimate SSID to lure clients; a rogue AP is any unauthorized AP attached to the network
- B. An evil twin is always wired; a rogue AP is always wireless
- C. They are two names for the same attack
- D. An evil twin only targets WEP networks

<details><summary>Answer</summary>

**A.** An **evil twin** clones a trusted SSID (a social/MITM lure to fool clients into associating), while a **rogue AP** is an *unsanctioned* access point plugged into your environment — a backdoor into the LAN. They overlap but are not identical, and neither is tied to a specific encryption era.
</details>

---

**Q9.** The best defense against an **evil twin** on an enterprise WLAN is:

- A. A hidden SSID
- B. Clients that validate the RADIUS server certificate (EAP-TLS mutual auth)
- C. A stronger PSK
- D. Turning off 5 GHz

<details><summary>Answer</summary>

**B. Server-certificate validation (EAP-TLS).** A client configured to validate the RADIUS server's certificate will refuse to join the clone because the evil twin can't present a trusted cert. A PSK network has no server identity to validate (so C doesn't help), and hiding the SSID or dropping a band does nothing against a clone.
</details>

---

**Q10.** Why is the **WPS PIN** so weak against brute force?

- A. The PIN is only 4 digits
- B. The 8-digit PIN is validated in two halves (and the last digit is a checksum), collapsing the search to about 11,000 attempts
- C. WPS transmits the PIN in plaintext beacons
- D. The PIN equals the last 4 bytes of the BSSID

<details><summary>Answer</summary>

**B. It is checked in two halves.** The registrar validates the first and second halves separately and the eighth digit is a checksum, so the effective keyspace drops from 10^8 to roughly **11,000** tries — feasible to brute force (reaver/bully). **Pixie-Dust** goes further, recovering the PIN offline from weak nonce RNG. The fix is to **disable WPS**.
</details>

---

**Q11.** In the aircrack-ng suite, which tool places the wireless adapter into **monitor mode**?

- A. airodump-ng
- B. aireplay-ng
- C. airmon-ng
- D. aircrack-ng

<details><summary>Answer</summary>

**C. airmon-ng.** `airmon-ng start wlan0` creates the monitor interface (e.g. `wlan0mon`). Then **airodump-ng** scans/captures, **aireplay-ng** injects (deauth/ARP replay), and **aircrack-ng** cracks the captured WEP IVs or WPA handshake. Know each tool's one-word role.
</details>

---

**Q12.** Which aircrack-ng tool is used to **inject** deauthentication frames?

- A. airmon-ng
- B. aireplay-ng
- C. airodump-ng
- D. aircrack-ng

<details><summary>Answer</summary>

**B. aireplay-ng.** It performs frame injection — deauth, fake authentication, and ARP replay (to generate WEP IV traffic). airmon-ng only toggles monitor mode, airodump-ng captures, and aircrack-ng does the cracking.
</details>

---

**Q13.** Which hashcat mode cracks a captured WPA/WPA2 handshake or PMKID?

- A. `-m 0`
- B. `-m 1000`
- C. `-m 13100`
- D. `-m 22000`

<details><summary>Answer</summary>

**D. `-m 22000`.** This is the modern combined WPA/WPA2/PMKID mode that replaced the older `2500` (handshake) and `16800` (PMKID-only) modes. `0` = MD5, `1000` = NTLM, `13100` = Kerberos TGS-REP — all from other modules. Memorize **22000** for wireless.
</details>

---

**Q14.** How does **WPA3-SAE** defeat the offline dictionary attack that works against WPA2-PSK?

- A. It uses a longer pre-shared key by default
- B. It replaces the PSK exchange with a password-authenticated key exchange (Dragonfly), so captured traffic yields no crackable blob, and it adds forward secrecy
- C. It encrypts the SSID
- D. It disables the 4-way handshake entirely and uses no keys

<details><summary>Answer</summary>

**B. SAE is a PAKE (Dragonfly).** **Simultaneous Authentication of Equals** never exposes a value you can brute-force offline from a passive capture, and it provides **forward secrecy** (a later key compromise doesn't decrypt past sessions). It doesn't merely lengthen the PSK (A), encrypt the SSID (C), or drop keys altogether (D).
</details>

---

**Q15.** A captured 4-way handshake fails to crack even after exhausting a large wordlist. What does this most directly demonstrate?

- A. The AP is running WEP
- B. WPA2-PSK strength depends entirely on passphrase entropy — a long, non-dictionary passphrase resists the offline attack
- C. The handshake was captured incorrectly, so the attack is impossible in principle
- D. Monitor mode was never enabled

<details><summary>Answer</summary>

**B. Passphrase entropy is the whole game.** A valid handshake plus an exhausted wordlist means the passphrase simply wasn't in the list — a long random passphrase (or better, moving off PSK to 802.1X/EAP-TLS) is what defeats the crack. It says nothing about WEP, and a genuinely malformed capture would be flagged as invalid rather than "exhausted."
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the encryption-evolution table and the 4-way-handshake section.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
