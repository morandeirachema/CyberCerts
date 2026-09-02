# Module 08 — Sniffing · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** You plug a laptop into a modern **switched** network and start Wireshark, but you only see broadcasts and your own traffic — not other hosts' unicast. Why?

- A. Wireshark is not in promiscuous mode
- B. The switch forwards each unicast frame only to the destination port, using its CAM table
- C. The traffic is encrypted
- D. The NIC does not support monitor mode

<details><summary>Answer</summary>

**B.** A switch learns MAC→port mappings in its **CAM table** and delivers unicast frames only to the owning port, so passive sniffing sees little on a switch. That is exactly why attackers must switch to **active** techniques (MAC flooding, ARP poisoning) to redirect traffic. Promiscuous mode (A) is necessary but not sufficient on a switch; encryption (C) would still let you see the packets, just not the payload.
</details>

---

**Q2.** On which environment does **passive** sniffing work without any active attack?

- A. A switch with port security enabled
- B. A hub, or a SPAN/mirror port or network TAP
- C. Any 802.1X-authenticated LAN
- D. A network using DHCP snooping

<details><summary>Answer</summary>

**B.** A **hub** copies every frame to every port, and a **SPAN port / TAP** deliberately feeds you a copy — both let you listen passively. On a switch you'd need an active attack. Note that SPAN/TAP are the *legitimate* sniffing methods (they feed IDS/analyzers), not attacks.
</details>

---

**Q3.** An attacker runs `macof` against a switch. What is the intended outcome?

- A. The switch reboots
- B. The CAM table overflows and the switch fails **open**, flooding frames out all ports like a hub
- C. The attacker's MAC is whitelisted
- D. The switch fails **closed** and blocks the attacker

<details><summary>Answer</summary>

**B.** **MAC flooding** overwhelms the CAM/MAC table with bogus source MACs. Once full, the switch can no longer store legitimate mappings and **fails open** — it floods unicast out every port, behaving like a hub, so the attacker can sniff. "Fail-open = acts like a hub" is the memory hook. It fails *open*, not closed (D). Counter: **port security**.
</details>

---

**Q4.** ARP poisoning succeeds primarily because:

- A. ARP requests are encrypted and can be forged
- B. ARP has no authentication, so hosts accept unsolicited/gratuitous ARP replies
- C. Switches disable ARP by default
- D. IPv6 replaced ARP

<details><summary>Answer</summary>

**B.** **ARP has no authentication.** A host will cache an unsolicited ("gratuitous") ARP reply with no proof, so a forged "gateway IP = attacker MAC" reply silently reroutes the victim's traffic. This one-line reason is the most-tested "why" in the module. Control: **Dynamic ARP Inspection (DAI)** and static ARP for gateways.
</details>

---

**Q5.** During an ARP MITM, the attacker enables `net.ipv4.ip_forward=1`. What does this accomplish?

- A. It encrypts the intercepted traffic
- B. It relays the victim's packets on to the real destination so the victim stays online (transparent MITM)
- C. It disables the victim's ARP cache
- D. It spoofs the DNS responses

<details><summary>Answer</summary>

**B.** With IP forwarding on, the attacker **relays** each intercepted packet to its true destination, so the victim keeps working normally and never notices the interception — a *transparent* man-in-the-middle. Without forwarding, poisoning becomes a denial of service instead of a stealthy MITM.
</details>

---

**Q6.** Match the defense to the attack it most directly counters: **(1) Port security, (2) DHCP snooping, (3) Dynamic ARP Inspection.**

- A. 1→ARP poisoning, 2→MAC flooding, 3→rogue DHCP
- B. 1→MAC flooding, 2→rogue DHCP, 3→ARP poisoning
- C. 1→rogue DHCP, 2→ARP poisoning, 3→MAC flooding
- D. All three counter ARP poisoning equally

<details><summary>Answer</summary>

**B.** **Port security** limits MACs per port → stops **MAC flooding**. **DHCP snooping** allows offers only from trusted ports → stops **rogue DHCP / starvation**. **Dynamic ARP Inspection** validates ARP against the DHCP snooping binding table → stops **ARP poisoning**. Swapping these mappings is the classic exam distractor.
</details>

---

**Q7.** An attacker sets up a DHCP server that answers client requests faster than the real one, handing out its own IP as the default gateway and DNS. This is:

- A. DHCP starvation
- B. A rogue DHCP server
- C. DNS cache poisoning
- D. MAC spoofing

<details><summary>Answer</summary>

**B.** A **rogue DHCP** server wins the race to answer and dictates the victim's **gateway and DNS**, funneling traffic through the attacker (MITM). **DHCP starvation** (A) is the *preceding* move — exhausting the real pool so clients must take the rogue lease. Counter: **DHCP snooping**.
</details>

---

**Q8.** Which set of protocols transmits credentials in **cleartext** by default?

- A. SSH, HTTPS, SFTP
- B. Telnet, FTP, HTTP, SNMPv1/2c, LDAP
- C. LDAPS, FTPS, SNMPv3
- D. IMAPS, POP3S, SMTPS

<details><summary>Answer</summary>

**B.** **Telnet (23), FTP (21), HTTP (80), SNMPv1/2c (161), and LDAP (389)** carry credentials in the clear. Their encrypted swaps: SSH, SFTP/FTPS, HTTPS, SNMPv3, and LDAPS (636). A/C/D are all already-encrypted options.
</details>

---

**Q9.** You capture SNMP traffic and read the community string "public" straight from the packet. Which version was in use, and what is the fix?

- A. SNMPv3; upgrade to v2c
- B. SNMPv1/2c (cleartext community strings); move to SNMPv3 (auth + privacy)
- C. SNMPv3; enable community strings
- D. It cannot be SNMP; SNMP is always encrypted

<details><summary>Answer</summary>

**B.** **SNMPv1 and v2c** send community strings ("public"/"private") in **cleartext**. **SNMPv3** adds authentication and privacy (encryption), so the string no longer appears on the wire. This is a favorite "know the secure swap" item.
</details>

---

**Q10.** In Wireshark, `ftp.request.command == "PASS"` and `tcp port 21` are, respectively:

- A. Both capture filters
- B. Both display filters
- C. A **display filter** and a **capture filter (BPF)** — different syntaxes
- D. A capture filter and a display filter

<details><summary>Answer</summary>

**C.** `ftp.request.command == "PASS"` is a **display filter** (Wireshark's expression language, applied *after* capture). `tcp port 21` is a **capture filter** written in **BPF/libpcap** syntax (applied *before* capture, limiting what's saved). The two grammars are not interchangeable — a top exam trap.
</details>

---

**Q11.** Responder answers **LLMNR/NBT-NS** broadcasts and captures authentication material. What does it capture, and how is it cracked?

- A. Cleartext passwords; no cracking needed
- B. NTLM hashes; `hashcat -m 1000`
- C. NetNTLMv2 challenge/response; `hashcat -m 5600`
- D. Kerberos TGS tickets; `hashcat -m 13100`

<details><summary>Answer</summary>

**C.** When a Windows host fails DNS and broadcasts an LLMNR/NBT-NS query, Responder replies "that's me," and the victim authenticates — yielding a **NetNTLMv2** challenge/response, cracked offline with **`hashcat -m 5600`**. Don't confuse it with raw NTLM (`-m 1000`) or Kerberos TGS-REP (`-m 13100`). Fix: disable LLMNR/NBT-NS + SMB signing.
</details>

---

**Q12.** A pentester is on a switched LAN and needs to read another host's HTTP session. Which is the correct *active* step to get on-path?

- A. Enable promiscuous mode and wait
- B. ARP-poison the victim ↔ gateway to become MITM
- C. Change the Wireshark display filter to `http`
- D. Plug into a SPAN port

<details><summary>Answer</summary>

**B.** On a switch, listening passively (A) yields nothing for other hosts' unicast. You must **actively** redirect traffic — **ARP poisoning** the victim and gateway puts you on-path. A display filter (C) only changes what you *see* in an existing capture. A SPAN port (D) is a legitimate admin method, not something an attacker typically has.
</details>

---

**Q13.** You ARP-poison a victim and it browses an **HTTPS** site. What do you see?

- A. The plaintext credentials, because you are MITM
- B. Only encrypted (TLS) traffic — you're on-path but can't read the payload; the victim may see a cert warning if you try to intercept TLS
- C. Nothing at all — HTTPS blocks ARP poisoning
- D. The site's private key

<details><summary>Answer</summary>

**B.** Being MITM at **L2** lets you *see and relay* the packets, but **TLS encrypts the payload**, so you get ciphertext. Actively terminating/re-signing the TLS session would throw a **certificate warning** on the victim. This is the module's core lesson: **encryption neutralizes the payoff** even when the technique succeeds.
</details>

---

**Q14.** From a PAM/defender standpoint, what best ensures a privileged credential is **never on the wire** in a form a sniffer can capture?

- A. A longer admin password
- B. Broker the session through a PAM proxy (PSM) that injects the target credential **server-side** over a TLS-tunneled, recorded session
- C. Enable Telnet with a banner warning
- D. Put the admin workstation on a different VLAN

<details><summary>Answer</summary>

**B.** A **PAM session broker (PSM/PSMP)** injects the target password **server-side** and tunnels/records the session over TLS, so the credential never traverses the admin's endpoint or the LAN in readable form — a sniffer or ARP MITM captures only ciphertext. Password length (A) doesn't matter if it's sent in cleartext; VLAN segmentation (D) helps but doesn't keep the credential off the wire within the segment.
</details>

---

**Q15.** Which of the following is a **legitimate** (sanctioned) way to feed traffic to an IDS, *not* an attack?

- A. MAC flooding
- B. ARP poisoning
- C. SPAN port / port mirroring or a network TAP
- D. Rogue DHCP

<details><summary>Answer</summary>

**C.** A **SPAN/mirror port** or a **network TAP** copies traffic to a monitoring device on purpose — the sanctioned way to sniff for an IDS/analyzer. The others (A, B, D) are active attacks. Know these terms as *legitimate monitoring*.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the active-sniffing attacks table and the defense↔attack matching in [facts.md](facts.md).
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
