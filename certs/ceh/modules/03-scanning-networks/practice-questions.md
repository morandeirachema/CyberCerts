# Module 03 — Scanning Networks · Practice Questions

> **Original, concept-based questions** — not exam dumps. Answers are collapsed: decide first, then expand. Target **≥80%**. Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** A **SYN (half-open) scan** (`-sS`) is preferred over a full connect scan (`-sT`) mainly because:

- A. It completes the full TCP handshake for reliability
- B. It never sends any packets
- C. It doesn't complete the handshake, so it's faster and historically stealthier
- D. It works without root privileges

<details><summary>Answer</summary>

**C.** `-sS` sends SYN, gets SYN/ACK (open) or RST (closed), then sends RST to tear down — never completing the handshake. That's faster and less likely to be logged by the application. It *requires* root (raw sockets); `-sT` is the one that needs no root.
</details>

---

**Q2.** In a TCP scan, an **open** port responds to a SYN with:

- A. RST
- B. SYN/ACK
- C. FIN
- D. No response

<details><summary>Answer</summary>

**B. SYN/ACK.** Open ports answer a SYN with SYN/ACK; **closed** ports reply with **RST**; **filtered** ports (firewall) typically give **no response**.
</details>

---

**Q3.** On most systems, sending a **FIN, NULL, or XMAS** scan to a **closed** port yields:

- A. SYN/ACK
- B. RST
- C. No response
- D. ICMP echo reply

<details><summary>Answer</summary>

**B. RST.** Per RFC 793, a closed port replies with RST to these flag scans, while an **open** port sends **no response**. (These scans don't work reliably against Windows, which RSTs regardless — a common exam caveat.)
</details>

---

**Q4.** Which port state means a firewall is likely dropping the probes?

- A. Open
- B. Closed
- C. Filtered
- D. Unfiltered

<details><summary>Answer</summary>

**C. Filtered.** Nmap marks a port *filtered* when it gets no response (or an ICMP unreachable), indicating a firewall/filter is blocking the probe rather than the host actively refusing it.
</details>

---

**Q5.** An **ACK scan** (`-sA`) is used primarily to:

- A. Grab service banners
- B. Map firewall rules (stateful vs stateless / filtered vs unfiltered)
- C. Crack passwords
- D. Detect the OS version

<details><summary>Answer</summary>

**B.** `-sA` doesn't determine open/closed — it determines whether a port is **filtered** or **unfiltered**, which helps infer firewall rulesets.
</details>

---

**Q6.** Which scan requires **no root/administrator** privileges?

- A. `-sS` SYN scan
- B. `-sT` TCP connect scan
- C. `-sF` FIN scan
- D. `-sX` XMAS scan

<details><summary>Answer</summary>

**B. `-sT`.** It uses the OS's full `connect()` call, so no raw-socket privilege is needed (but it's slower and more likely logged). The raw-packet scans (`-sS/-sF/-sX/-sN`) need root.
</details>

---

**Q7.** Why is a **UDP scan** (`-sU`) slow and often ambiguous?

- A. UDP always replies with SYN/ACK
- B. Open UDP ports usually don't reply, so "open" and "filtered" are hard to distinguish, and scans are rate-limited by ICMP
- C. UDP doesn't use ports
- D. Nmap can't scan UDP

<details><summary>Answer</summary>

**B.** Open UDP ports frequently send nothing back; a closed port returns ICMP port-unreachable (which is rate-limited). So Nmap often reports `open|filtered`, and scans crawl.
</details>

---

**Q8.** Which nmap option appends random data / decoys to help evade an IDS?

- A. `-sV`
- B. `-O`
- C. `-D RND:5`
- D. `-p-`

<details><summary>Answer</summary>

**C. `-D RND:5`** adds 5 random decoy source addresses so your real IP is hidden among them. `-sV` is version detection, `-O` is OS detection, `-p-` scans all 65535 ports.
</details>

---

**Q9.** `nmap -sV` provides:

- A. The OS family only
- B. Service and version information on open ports
- C. A password list
- D. A list of subdomains

<details><summary>Answer</summary>

**B.** `-sV` probes open ports to identify the **service and its version** (e.g., "OpenSSH 7.2p2"). `-O` is the separate OS-detection flag; `-A` combines version + OS + default scripts + traceroute.
</details>

---

**Q10.** What does `-f` (or `--mtu`) do in an nmap scan?

- A. Speeds up the scan with more threads
- B. Fragments packets to slip past simple packet inspection
- C. Forces a full connect scan
- D. Fingerprints the firewall vendor

<details><summary>Answer</summary>

**B.** `-f` splits probes into tiny IP fragments so a signature engine that doesn't reassemble may miss them. `--mtu` sets a custom (multiple-of-8) fragment size.
</details>

---

**Q11.** The nmap timing template **`-T0`** vs **`-T4`**:

- A. T0 is fastest, T4 is slowest
- B. T0 is very slow/stealthy ("paranoid"), T4 is aggressive/fast
- C. They control the number of ports
- D. They set the output format

<details><summary>Answer</summary>

**B.** Timing runs `-T0` (paranoid, slow to dodge rate-based IDS) through `-T5` (insane, fastest). `-T4` is a common "fast but reasonable" choice on a healthy network.
</details>

---

**Q12.** A **ping sweep** / host discovery scan is invoked with:

- A. `-sn`
- B. `-sS`
- C. `-p-`
- D. `-A`

<details><summary>Answer</summary>

**A. `-sn`** does host discovery *without* a port scan (which hosts are up). On a local LAN, `-PR` (ARP) is the most reliable discovery method.
</details>

---

**Q13.** Spoofing your source port to **53** (`-g 53` / `--source-port 53`) can help because:

- A. Port 53 is always closed
- B. Some firewalls trust DNS-sourced traffic and let it through
- C. It encrypts the scan
- D. It disables logging on the target

<details><summary>Answer</summary>

**B.** Poorly configured firewalls may allow traffic that appears to come from DNS (port 53), so sourcing probes from 53 can bypass such rules.
</details>

---

### Score yourself
- **11–13:** strong — memorize the scan-type↔response table in [facts.md](facts.md).
- **8–10:** re-read port states and the FIN/NULL/XMAS behavior.
- **< 8:** redo the [lab-walkthrough.md](lab-walkthrough.md) with nmap against Metasploitable2.
