# Module 10 — Denial-of-Service · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — **not exam dumps** (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** What is the defining difference between a **DoS** and a **DDoS** attack?

- A. DDoS targets Layer 7 while DoS targets Layer 4
- B. DoS uses UDP and DDoS uses TCP
- C. DoS is illegal but DDoS is a legitimate stress test
- D. DDoS comes from many distributed sources (a botnet); DoS from a single source

<details><summary>Answer</summary>

**D. DDoS comes from many distributed sources.** The distributed nature is the whole point: you cannot just block one offending IP because traffic arrives from thousands of compromised hosts. Layer and protocol (A, B) vary independently of source count, and both DoS and DDoS against systems you don't own are crimes (C).
</details>

---

**Q2.** A server's TCP backlog fills with connections stuck in the **SYN-RECV** state and it stops accepting new clients. Which attack is this?

- A. UDP flood
- B. Slowloris
- C. SYN flood
- D. Smurf

<details><summary>Answer</summary>

**C. SYN flood.** The attacker sends SYNs but never completes the three-way handshake, leaving **half-open** connections that exhaust the backlog table. This is a **protocol/state** attack, not volumetric. Slowloris also holds connections open but does so with *partial HTTP headers* at Layer 7, not half-open TCP.
</details>

---

**Q3.** Which countermeasure defeats a SYN flood **without enlarging the connection backlog**?

- A. SYN cookies
- B. Increasing the `net.core.somaxconn` backlog size
- C. Blocking all ICMP
- D. Enabling a CAPTCHA

<details><summary>Answer</summary>

**A. SYN cookies.** The server encodes handshake state into the sequence number it returns and allocates no backlog slot until a valid ACK comes back — so a flood of bare SYNs consumes no table space. Merely growing the backlog (B) just delays exhaustion. ICMP blocking (C) and CAPTCHA (D) address different attack classes.
</details>

---

**Q4.** Match the attack to its category. **Slowloris** belongs to which DoS category?

- A. Volumetric
- B. Protocol / state
- C. Application-layer (L7)
- D. Reflection / amplification

<details><summary>Answer</summary>

**C. Application-layer (L7).** Slowloris ties up a web server's worker threads/sockets by holding many connections open with slow, partial HTTP requests — it exhausts the *application*, not bandwidth or the TCP table. It is the classic L7 example precisely because it uses almost **no** bandwidth.
</details>

---

**Q5.** Why do amplification/reflection attacks rely on **UDP-based** protocols such as DNS, NTP, and memcached?

- A. UDP packets are always larger than TCP packets
- B. UDP is connectionless, so the source IP can be spoofed without completing a handshake
- C. TCP does not support broadcast addresses
- D. UDP encrypts the payload, hiding the attacker

<details><summary>Answer</summary>

**B. UDP is connectionless.** With no handshake to complete, the attacker can forge (spoof) the *victim's* IP as the source, so every reflector's reply is sent to the victim. TCP's three-way handshake would fail against a spoofed source, defeating reflection. Amplification then adds the multiplier by choosing protocols whose replies dwarf the request.
</details>

---

**Q6.** The **amplification factor** of a reflection attack is best described as:

- A. The number of bots in the botnet
- B. The percentage of packets that reach the target
- C. The number of hops between attacker and victim
- D. The ratio of the reflected response size to the request size

<details><summary>Answer</summary>

**D. Response size ÷ request size.** A tiny spoofed query that triggers a huge reply lets one attacker generate traffic far exceeding their own uplink. This is why the **ranking** matters: **memcached (~10,000–51,000×) ≫ NTP (~500×) ≫ DNS (~28–54×) ≫ SSDP (~30×)**.
</details>

---

**Q7.** An NTP-based reflection attack is triggered by which command, and memcached reflection abuses which UDP port?

- A. `monlist` / UDP 11211
- B. `version` / UDP 123
- C. `ANY` / UDP 53
- D. `stats` / UDP 1900

<details><summary>Answer</summary>

**A. `monlist` / UDP 11211.** NTP's legacy `monlist` returns a large list of recent clients, giving a ~500× amplifier; memcached exposed on UDP **11211** is the record-setting amplifier. (DNS uses `ANY`/large TXT on 53, and SSDP uses UPnP discovery on 1900 — good distractors.)
</details>

---

**Q8.** What distinguishes a **Smurf** attack from a **Fraggle** attack?

- A. Smurf uses UDP echo/chargen; Fraggle uses ICMP
- B. Smurf uses ICMP to a broadcast address; Fraggle uses UDP to a broadcast address
- C. Smurf is application-layer; Fraggle is volumetric
- D. Smurf forges TCP SYNs; Fraggle forges ACKs

<details><summary>Answer</summary>

**B.** Both are reflection attacks that spoof the victim's IP and aim traffic at a **directed broadcast** so every host on the segment replies to the victim. The difference is the protocol: **Smurf = ICMP**, **Fraggle = UDP** (echo/chargen). Both are effectively dead because directed broadcast is disabled by default.
</details>

---

**Q9.** A web server is failing under a load that uses **very little bandwidth**, with many connections sending **incomplete HTTP headers** very slowly. Which attack and which fix fit best?

- A. UDP flood → rate-limit UDP
- B. SYN flood → SYN cookies
- C. Slowloris → reverse proxy with connection/time-out limits
- D. DNS amplification → BCP38 anti-spoofing

<details><summary>Answer</summary>

**C. Slowloris → reverse proxy + connection/time-outs.** "Minimal bandwidth" plus "partial/incomplete headers held open" is the signature of Slowloris, an L7 connection-exhaustion attack. A reverse proxy that enforces header-completion timeouts and per-IP connection caps sheds it. The other fixes target volumetric or protocol attacks.
</details>

---

**Q10.** Which countermeasure most directly disrupts **reflection/amplification** attacks at the network edge?

- A. SYN cookies
- B. Autoscaling the web tier
- C. BCP38 / uRPF ingress anti-spoofing filtering
- D. A CAPTCHA challenge

<details><summary>Answer</summary>

**C. BCP38 / uRPF.** Reflection depends on **source-IP spoofing**; ingress filtering (RFC BCP38, enforced with uRPF) drops packets whose source address couldn't legitimately arrive on that interface, so spoofed queries never leave the attacker's network. SYN cookies (A) address SYN floods; autoscaling (B) and CAPTCHA (D) address volumetric/L7 loads.
</details>

---

**Q11.** In a botnet-driven DDoS, what is the role of the **handlers** (command-and-control)?

- A. They are the victim servers being flooded
- B. They relay the bot herder's commands to the agents/zombies
- C. They amplify traffic via `monlist`
- D. They sign firmware to prevent phlashing

<details><summary>Answer</summary>

**B. Handlers relay commands.** The chain is **bot herder → handlers (C2) → agents/zombies**. Handlers let one operator coordinate thousands of compromised hosts while staying insulated from them. Amplification (C) is a separate reflection technique, and firmware signing (D) is a PDoS defense.
</details>

---

**Q12.** Why can a **volumetric** DDoS generally **not** be absorbed at the target host itself?

- A. The host's CPU is too slow to run iptables
- B. Volumetric attacks only target Layer 7
- C. Hosts cannot run SYN cookies
- D. The attack saturates the upstream link before packets ever reach the host's defenses

<details><summary>Answer</summary>

**D. The upstream pipe fills first.** Once inbound bandwidth exceeds the link capacity, dropping packets *at the host* is too late — the congestion is already upstream. That is why volumetric mitigation must be pushed to a **CDN / anycast / cloud scrubbing** provider with far more capacity, or handled with autoscaling.
</details>

---

**Q13.** What is **PDoS (permanent DoS / "phlashing")**?

- A. An attack that corrupts firmware/hardware, bricking the device permanently
- B. A DoS that lasts exactly as long as the attacker keeps flooding
- C. A reflection attack using memcached
- D. A Layer-7 HTTP GET flood

<details><summary>Answer</summary>

**A. It bricks the device.** PDoS corrupts firmware or hardware (e.g. "BrickerBot") so the device is *permanently* out of service and must be replaced or re-flashed — not merely unavailable while an attack runs. Defenses are signed firmware, management-network isolation, and least-privilege device admin.
</details>

---

**Q14.** From a **PAM/availability** standpoint, what is the primary reason to keep the admin plane **out-of-band** on a separate management network?

- A. It makes SSH faster
- B. So a saturated data-plane during a flood doesn't starve admin access needed to recover
- C. To enable memcached amplification
- D. Because BCP38 requires it

<details><summary>Answer</summary>

**B. So you can still administer/recover under attack.** DoS is an availability attack; if SSH/RDP/console share the flooded segment, you lose the very access you need to respond. An out-of-band management VLAN (plus hardened jump hosts with QoS priority and break-glass access) keeps the control plane alive when the data-plane is drowning.
</details>

---

**Q15.** Which pairing correctly maps a PAM control to the DoS risk it addresses?

- A. Vault HA/DR clustering → prevents a DoS on the PAM control plane from locking admins out
- B. SYN cookies → rotate the krbtgt password
- C. Load-balanced PSM farm → encrypts firmware
- D. Break-glass account → amplifies NTP responses

<details><summary>Answer</summary>

**A. Vault HA/DR clustering.** If the PAM control plane itself is DoS'd, admins can't retrieve credentials mid-incident — so the vault is designed with **high availability + disaster recovery + distributed (satellite) nodes**, the session broker (PSM) is load-balanced to avoid a single bottleneck, and a monitored **break-glass** path exists for when normal auth is degraded. The other options are nonsense pairings.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the three-categories table and the amplification/reflection section.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
