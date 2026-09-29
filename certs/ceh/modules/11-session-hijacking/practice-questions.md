# Module 11 — Session Hijacking · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** An attacker forces the client's and server's TCP sequence numbers out of alignment so that only the attacker's injected packets are accepted while the real client's are dropped. Which technique is this?

- A. Session desynchronization
- B. Session fixation
- C. UDP hijacking
- D. Cross-site request forgery

<details><summary>Answer</summary>

**A. Session desynchronization.** Knocking the two endpoints' SEQ numbers out of sync (often producing an "ACK storm") lets the attacker inject accepted packets while the legitimate client is effectively cut out. This is a **network-level**, active hijack. Fixation and CSRF are application-level; UDP hijacking involves no sequence numbers at all.
</details>

---

**Q2.** Which pairing correctly maps the two CEH hijacking levels to their target?

- A. Network-level → session cookies; application-level → TCP sequence numbers
- B. Both levels target the TLS handshake
- C. Network-level → TCP/IP session; application-level → session token/cookie
- D. Network-level → CSRF; application-level → ARP spoofing

<details><summary>Answer</summary>

**C.** **Network-level** hijacking attacks the **TCP/IP session** itself (SEQ/ACK prediction, desync, RST). **Application-level** hijacking attacks the **session token/cookie** (theft, fixation, predictable IDs, CSRF riding). This split is the first thing CEH tests here.
</details>

---

**Q3.** An attacker emails a victim a link containing a session identifier the attacker already knows. The victim clicks it and logs in; the app keeps that same ID, and the attacker now reuses it. Which attack is this?

- A. Session theft via sniffing
- B. Blind hijacking
- C. Pass-the-Ticket
- D. Session fixation

<details><summary>Answer</summary>

**D. Session fixation.** The distinguisher is that the attacker **supplies the session ID before authentication** and waits for the victim to authenticate it. In *theft*, the attacker instead **captures an ID the victim already holds**. The fix for fixation is to **regenerate the session ID at login**.
</details>

---

**Q4.** Which cookie attribute most directly prevents a cross-site request forgery from silently riding a user's session?

- A. HttpOnly
- B. Secure
- C. SameSite
- D. Domain

<details><summary>Answer</summary>

**C. SameSite.** It restricts whether the cookie is attached to cross-site requests, which is exactly the vector CSRF relies on. **HttpOnly** blocks *script* from reading the cookie (XSS), **Secure** keeps it off non-TLS links, and `Domain` just scopes the cookie. Pair SameSite with anti-CSRF tokens.
</details>

---

**Q5.** An off-path attacker cannot see the responses in the TCP conversation and must guess the next sequence numbers to inject data. This describes:

- A. Non-blind hijacking
- B. Blind hijacking
- C. Sidejacking
- D. Session fixation

<details><summary>Answer</summary>

**B. Blind hijacking.** "Off-path, can't see responses, must predict SEQ" is the definition of **blind** hijacking — made much harder by modern ISN randomization. **Non-blind** hijacking is the MITM case where the attacker *can* see the traffic and simply reads the sequence numbers.
</details>

---

**Q6.** How does CSRF differ from classic session hijacking?

- A. CSRF steals the session token and replays it from the attacker's machine
- B. CSRF requires cracking the user's password first
- C. CSRF only works over UDP
- D. CSRF forces the victim's browser to send an authenticated request without the attacker ever seeing the token

<details><summary>Answer</summary>

**D.** CSRF **rides** the victim's existing session: it makes the victim's own browser send a state-changing authenticated request, and the attacker **never obtains the token**. Classic hijacking, by contrast, involves the attacker *possessing* the session (stolen or predicted). That is why CSRF is *related to* but distinct from hijacking — and why SameSite + anti-CSRF tokens are its fix.
</details>

---

**Q7.** On a coffee-shop network an attacker captures a victim's session cookie because the site sent it over plain HTTP after an HTTPS login. What is this called, and what single control defeats it?

- A. Fixation; account lockout
- B. Sidejacking; TLS everywhere (HSTS + Secure flag)
- C. Kerberoasting; gMSA
- D. Blind hijacking; ISN randomization

<details><summary>Answer</summary>

**B. Sidejacking; TLS everywhere.** Capturing the cookie off an unencrypted/downgraded link is **sidejacking** (the "Firesheep" scenario). Enforcing **TLS on every request** (with **HSTS** to prevent downgrade and the **Secure** flag so the cookie never traverses HTTP) removes the cleartext window entirely.
</details>

---

**Q8.** An attacker sends a forged TCP segment with the correct sequence number and the RST flag set, abruptly tearing down a target's established connection. Besides hijacking prep, what else is this a building block for?

- A. Privilege escalation
- B. Password cracking
- C. Denial of service
- D. DNS cache poisoning

<details><summary>Answer</summary>

**C. Denial of service.** **RST hijacking** forcibly closes a peer's connection; because it kills a live session, it doubles as a **DoS** primitive. It is a network-level technique that depends on getting the SEQ number right.
</details>

---

**Q9.** Why is UDP-based session hijacking generally easier than TCP-based hijacking?

- A. UDP encrypts everything, so tokens are exposed
- B. UDP has no handshake or sequence numbers, so the attacker just races a spoofed reply
- C. UDP requires a MITM position that TCP does not
- D. UDP always uses predictable session cookies

<details><summary>Answer</summary>

**B.** UDP is **connectionless** — there is no three-way handshake and no sequence numbers to synchronize or predict. The attacker simply needs to **inject a spoofed response before the legitimate server's**, which is far less work than defeating TCP's SEQ/ACK machinery.
</details>

---

**Q10.** A hardened web app is tested for session fixation. After the user authenticates, what behavior indicates the app is **not** vulnerable?

- A. The pre-login session ID is reused after authentication
- B. The session ID appears in the URL
- C. The session cookie lacks the HttpOnly flag
- D. The app issues a brand-new session ID at login, invalidating the old one

<details><summary>Answer</summary>

**D.** A non-vulnerable app **regenerates the session ID on authentication**, so any ID an attacker planted beforehand becomes worthless. Reusing the pre-login ID (A) is the fixation flaw itself; missing HttpOnly (C) and IDs in the URL (B) are separate weaknesses.
</details>

---

**Q11.** Which set of controls most directly reduces the blast radius of a **stolen privileged session token** in a PAM-managed environment?

- A. Longer user passwords and disabling IPv6
- B. Enabling LLMNR and NetBIOS
- C. Session brokering/recording, step-up re-auth for sensitive actions, short idle timeouts, and token rotation on privilege change
- D. Allowing session IDs in query strings for easier logging

<details><summary>Answer</summary>

**C.** A privileged **broker (PSM)** runs the session so no reusable token sits on the endpoint; **step-up re-authentication** blocks high-impact actions on a lifted session; **short idle timeouts** and **rotation on privilege change** shrink the reuse window. The other options either don't address token theft or actively increase exposure.
</details>

---

**Q12.** A developer disagrees that HttpOnly is enough to stop all session theft. Which statement is correct?

- A. HttpOnly stops script from reading the cookie but does nothing against on-the-wire sniffing
- B. HttpOnly encrypts the cookie in transit
- C. HttpOnly prevents CSRF entirely
- D. HttpOnly makes the session ID unpredictable

<details><summary>Answer</summary>

**A.** **HttpOnly** only prevents JavaScript (e.g. XSS) from reading `document.cookie`. It provides **no protection against network sniffing/sidejacking** — that requires **Secure + TLS**. It also does not stop CSRF (**SameSite** does) or add entropy to the ID. Each flag defeats a different attack; know the mapping.
</details>

---

**Q13.** Which technique gives an attacker the MITM position most network-level hijacks and sidejacking depend on within a LAN?

- A. ARP spoofing / poisoning
- B. Kerberoasting
- C. SQL injection
- D. Golden ticket forgery

<details><summary>Answer</summary>

**A. ARP spoofing / poisoning.** Poisoning the ARP cache (or DNS spoofing / a rogue AP) puts the attacker **in the path** so they can sniff tokens, inject packets, or strip TLS. Defenses: **Dynamic ARP Inspection**, DHCP snooping, switch port security, and HSTS against downgrade.
</details>

---

**Q14.** How does session **hijacking** differ from IP/identity **spoofing**?

- A. Hijacking forges a source address to start a new connection; spoofing takes over a live one
- B. Hijacking takes over an already-authenticated live session; spoofing forges an identity to initiate access
- C. They are identical terms
- D. Hijacking always requires the victim's password

<details><summary>Answer</summary>

**B.** **Hijacking** rides or seizes an **existing, authenticated** session — no password needed. **Spoofing** forges an identity (e.g. a source IP) to *initiate* a connection where no established session yet exists. Don't conflate them with **replay** either, which resends previously captured data.
</details>

---

**Q15.** A session ID generator produces values like `1001`, `1002`, `1003` for successive users. What is the weakness and the fix?

- A. Predictable session IDs; use long, high-entropy random tokens in a server-side store
- B. Session fixation; enable HttpOnly
- C. Sidejacking; enable SameSite
- D. RST hijacking; randomize the ISN

<details><summary>Answer</summary>

**A. Predictable session IDs.** Sequential, low-entropy IDs let an attacker simply **guess** a valid neighbor's session. The fix is **long, cryptographically random, high-entropy tokens** backed by a server-side session store — entropy and unpredictability are the point.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the network-vs-application and fixation-vs-theft sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
