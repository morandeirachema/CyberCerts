# Module 12 — Evading IDS, Firewalls & Honeypots · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** A sensor sits on a SPAN port, watches a copy of segment traffic, and raises alerts but never drops a packet. What is it?

- A. An inline IPS
- B. A NIDS
- C. A stateful firewall
- D. A proxy gateway

<details><summary>Answer</summary>

**B. A NIDS.** Watching a *copy* of the traffic (tap/SPAN) and only alerting is the defining trait of a network IDS. An IPS sits **inline** and can drop or reset; a firewall makes allow/deny decisions rather than pattern-matching for attacks. **Tell:** "copy of traffic" + "alert only" = IDS, not IPS.
</details>

---

**Q2.** Which statement correctly separates an **IDS** from an **IPS**?

- A. IDS blocks traffic inline; IPS only logs
- B. IDS detects and alerts out of band; IPS detects and blocks inline
- C. IDS works at Layer 7 only; IPS works at Layer 3 only
- D. They are identical; the names are interchangeable

<details><summary>Answer</summary>

**B.** Same detection engine, different placement and authority: the **IDS** watches out-of-band and can only **alert**; the **IPS** sits **inline** and can **drop/reset/rewrite**. Placement (out-of-band vs in-path), not OSI layer, is the distinction.
</details>

---

**Q3.** An attacker crafts packets that the **IDS accepts and reassembles but the target host silently discards**, so the reassembled IDS view never matches the real payload. Which Ptacek & Newsham category is this?

- A. Evasion
- B. Denial of service
- C. Insertion
- D. Fragmentation overlap only

<details><summary>Answer</summary>

**C. Insertion.** The **IDS accepts** a packet the **end host rejects**, padding the IDS's reconstruction so the signature never fires. Evasion is the mirror image (host accepts what the IDS misses). Anchor on **who accepted the packet**.
</details>

---

**Q4.** From Kali you run `nmap --badsum 192.168.56.20`. The target reports no open ports, yet your Suricata still logs the probes. Which concept does this gap illustrate?

- A. Evasion
- B. Insertion
- C. A false negative on the host
- D. Anomaly detection

<details><summary>Answer</summary>

**B. Insertion.** A bad TCP checksum makes the **end host drop** the packet while a sensor that ignores checksums may still process it — the IDS "sees" traffic the target never accepted. That divergence between IDS view and host view is the textbook insertion scenario, and `--badsum` is also used to fingerprint filtering devices.
</details>

---

**Q5.** Which detection method compares live traffic against a **learned baseline of normal behavior** and can therefore flag novel, never-before-seen attacks?

- A. Signature / misuse detection
- B. Anomaly / behavior detection
- C. Stateless packet filtering
- D. Rainbow-table matching

<details><summary>Answer</summary>

**B. Anomaly / behavior detection.** It measures deviation from a baseline, so it can catch **unknown/0-day** activity — at the cost of more **false positives** and a training period. Signature detection matches known-bad patterns and is blind to novel attacks.
</details>

---

**Q6.** Encrypted tunneling (e.g. HTTPS or DNS-over-TXT C2) most directly defeats which detection approach, while still leaving a tell for another?

- A. Defeats anomaly detection; leaves nothing for signatures
- B. Defeats signature detection; still leaves a behavioral/flow tell
- C. Defeats both equally
- D. Defeats stateful firewalls only

<details><summary>Answer</summary>

**B.** Signature IDS **can't read the encrypted payload**, so content rules go blind. But tunneling still produces a **behavioral shape** — high-entropy query volume, beaconing intervals, odd data lengths — that anomaly/flow analysis and egress monitoring can catch. Evasion moves the evidence; it rarely erases it.
</details>

---

**Q7.** In an nmap command, what does the `-D` flag do?

- A. Sets a decoy list of spoofed source IPs to hide the real scanner
- B. Fragments packets into 8-byte pieces
- C. Spoofs the source port
- D. Appends random bytes to each packet

<details><summary>Answer</summary>

**A. Decoys.** `-D ip1,ME,ip2` (or `-D RND:5`) sprays the target's logs with many apparent sources so the analyst can't tell which is real. Don't confuse it with `-S` (spoof **source IP**), `-g` (spoof **source port**), or `-f` (**fragment**). CEH loves this flag→purpose match.
</details>

---

**Q8.** You want nmap to send probes **from source port 53** to slip past an ACL that trusts DNS traffic. Which flag?

- A. `--data-length 53`
- B. `-f`
- C. `-g 53`
- D. `--spoof-mac 53`

<details><summary>Answer</summary>

**C. `-g 53`** (equivalently `--source-port 53`) sets the source port. Poorly written stateless rules that "allow anything from port 53/80/443" can be bypassed this way — which is exactly why a **stateful, default-deny** firewall should never trust the source port. `--data-length` pads packets; `-f` fragments.
</details>

---

**Q9.** A colleague runs `nmap --mtu 15 target` and it errors out. Why?

- A. MTU cannot exceed 8
- B. `--mtu` must be a multiple of 8
- C. `--mtu` requires root even in a lab
- D. MTU cannot be combined with `-sS`

<details><summary>Answer</summary>

**B. `--mtu` must be a multiple of 8** (8, 16, 24, …). Fragmentation offsets are counted in 8-byte units, so nmap rejects 15. Recall the shortcut aliases: `-f` ≈ MTU 8, `-ff` ≈ MTU 16.
</details>

---

**Q10.** Which firewall type inspects the **full application-layer payload**, terminates the connection, and re-originates it on behalf of the client?

- A. Stateless packet filter (Layer 3–4)
- B. Stateful inspection firewall
- C. Circuit-level gateway (Layer 5)
- D. Application / proxy firewall (Layer 7)

<details><summary>Answer</summary>

**D. Application / proxy firewall.** It operates at **Layer 7**, reads the whole payload per-protocol, and terminates then re-originates the session — deep but slower. A packet filter (3–4) only checks headers; a circuit-level gateway (5) validates the session, not the payload.
</details>

---

**Q11.** What is the defining difference between a **low-interaction** and a **high-interaction** honeypot?

- A. Low-interaction runs real OS/services; high-interaction only emulates
- B. Low-interaction emulates services; high-interaction exposes real systems
- C. Low-interaction is always research; high-interaction is always production
- D. Low-interaction can block traffic; high-interaction cannot

<details><summary>Answer</summary>

**B.** **Low-interaction = emulated** services (honeyd, Dionaea) — safer and cheaper but yields limited data. **High-interaction = real** operating systems and services (honeynets) — far richer attacker data, but greater risk since a real system can be abused as a pivot.
</details>

---

**Q12.** A security team deploys a honeypot **inside the corporate network purely as an early-warning tripwire** — any connection to it is suspicious. Which honeypot *purpose* is this?

- A. Research honeypot
- B. Production honeypot
- C. Tarpit
- D. Pure honeypot

<details><summary>Answer</summary>

**B. Production honeypot.** Its job is **early warning / detection** inside your own environment, so it can stay simple. A **research** honeypot exists to study attacker TTPs in depth. A **tarpit** (LaBrea) deliberately slows scanners; a **pure** honeypot is a full real system.
</details>

---

**Q13.** During a scan you notice services with canned, unrealistically consistent banners, abnormal latency, and no genuine user activity. What have you most likely found?

- A. A next-generation firewall
- B. A honeypot
- C. An IPS in fail-open mode
- D. A DMZ bastion host

<details><summary>Answer</summary>

**B. A honeypot.** Canned banners, too-consistent open services, odd latency/tarpit stalling, VM/sandbox artifacts, and the absence of real user activity are exactly the **fingerprinting tells** an attacker uses to spot deception before engaging.
</details>

---

**Q14.** Which technique splits an HTTP attack across many tiny TCP segments so **no single packet matches a signature**, relying on the target to reassemble the full request?

- A. Source routing
- B. Session splicing / fragmentation
- C. MAC spoofing
- D. Circuit-level gateway bypass

<details><summary>Answer</summary>

**B. Session splicing / fragmentation.** The payload is carved across small packets (whisker-style for HTTP) so signature engines that inspect single packets never see the whole pattern; the target reassembles it. Defense: force **full IDS/IPS reassembly** and NGFW normalization, and drop overlapping fragments.
</details>

---

**Q15.** Which control most directly neutralizes **source-port spoofing** (`-g 53/80/443`) against a network perimeter?

- A. Enabling LLMNR
- B. A stateful, default-deny firewall that does not trust the source port
- C. Longer administrator passwords
- D. Disabling the IDS to reduce false positives

<details><summary>Answer</summary>

**B.** Source-port spoofing only works against **stateless ACLs that trust a "safe" source port**. A **stateful, default-deny** firewall tracks real connection state and evaluates the *destination* service and flow direction, so a packet claiming to be "from port 53" gets no free pass. The other options are irrelevant or actively harmful.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the Insertion-vs-Evasion and nmap evasion-flag sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
