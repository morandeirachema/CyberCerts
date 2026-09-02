# Module 11 — Session Hijacking · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The core definition
Hijacking = **stealing or riding an already-authenticated session** so you skip the login entirely. No password needed — you inherit a *live* session. CEH's first dividing line is **network-level** (TCP/packet layer) vs. **application-level** (session tokens/cookies).

## Network-level vs. application-level
| Level | You attack | Techniques |
|---|---|---|
| **Network-level** | The **TCP/IP session** itself | Seq-number prediction, session desync, RST/FIN hijack, blind/UDP hijack, IP spoofing |
| **Application-level** | The **session token/cookie** | Token theft (XSS, sniffing/sidejacking), session fixation, predictable session IDs, CSRF riding |

## Network-level techniques
| Technique | Mechanism | Key point |
|---|---|---|
| **TCP sequence prediction** | Guess/observe next SEQ/ACK to inject packets as the client | Modern OSes randomize ISN → hard when blind |
| **Session desynchronization** | Force client & server SEQ out of sync, then inject | Attacker's packets accepted, real client's dropped (ACK storm) |
| **RST / FIN hijacking** | Forge an **RST**/FIN with the right SEQ to tear down a peer | Also a **DoS** primitive |
| **Blind hijacking** | Attacker is **off-path**, can't see responses → must *predict* SEQ | Contrast **non-blind** = MITM *sees* traffic |
| **UDP hijacking** | No handshake/SEQ — just race a spoofed reply before the server | **Easier** than TCP; connectionless |
| **IP spoofing** | Forge source IP to impersonate the client | Prerequisite for many of the above |

TCP handshake being abused: `SYN → SYN/ACK → ACK`. Hijacking injects into an **established** session by getting the **SEQ/ACK numbers right**.

## Application-level techniques
| Technique | Mechanism | Distinguisher |
|---|---|---|
| **Token theft (sniffing / sidejacking)** | Capture the cookie off an unencrypted/downgraded link | Classic "Firesheep"; **TLS everywhere** kills it |
| **XSS cookie theft** | Script reads `document.cookie` and exfiltrates it | **HttpOnly** blocks script access |
| **Session fixation** | Attacker *sets/knows* the ID **before** login; victim authenticates it; attacker reuses | Fix: **regenerate session ID on login** |
| **Predictable session IDs** | Sequential/low-entropy IDs → guess a valid one | Fix: long, random, high-entropy tokens |
| **CSRF (related)** | Forces the victim's browser to send an authenticated request; attacker **never sees** the token | Rides the session; fix = anti-CSRF token + **SameSite** |

## Fixation vs. theft (the classic trap)
- **Fixation** = attacker supplies the session ID *up front* and waits for the victim to authenticate it.
- **Theft** = attacker *captures* an ID the victim already has.
- Fixation is defeated by **rotating the session ID at authentication**.

## Hijacking vs. spoofing vs. replay
- **Hijacking** takes over an **active, authenticated** session (no password).
- **Spoofing** forges an identity to *initiate* a connection (you're not in an existing session).
- **Replay** resends captured data/credentials to re-establish access.

## Active vs. passive
- **Passive** = watch/record the session, steal the token, replay later.
- **Active** = take over the live session and push the legitimate user out (desync/RST).

## MITM: the enabling position
Most network-level and sidejacking attacks need the attacker **in the path**. Get there on a LAN via **ARP spoofing/poisoning**, **DNS spoofing**, or a rogue AP. Once MITM: sniff tokens, inject packets, or strip TLS (**SSL stripping**, defeated by **HSTS**).

## Cookie flags — know which defeats which
| Flag | Stops | Attack it blocks |
|---|---|---|
| **HttpOnly** | JavaScript reading the cookie | XSS `document.cookie` theft |
| **Secure** | Cookie traversing non-TLS | Sidejacking / cleartext sniffing |
| **SameSite** | Cookie sent on cross-site requests | CSRF riding the session |

## Tools → purpose
| Tool | Purpose |
|---|---|
| **Burp Suite** | Intercept/modify HTTP, inspect & replay tokens, test fixation |
| **Wireshark** | Sniff, Follow TCP Stream, observe cookies/SEQ numbers |
| **ettercap** | ARP poisoning / MITM framework (LAN) |
| **bettercap** | Modern MITM: ARP/DNS spoof, sniff, HTTP(S) proxy |

## Defenses (map the fix to the flaw)
- **TLS everywhere + HSTS** → kills sniffing/sidejacking and SSL stripping.
- **HttpOnly / Secure / SameSite** cookie flags → XSS theft / cleartext / CSRF respectively.
- **Rotate the session ID on authentication and privilege change** → defeats fixation.
- **Long, high-entropy random tokens** (server-side store) → defeats guessing.
- **Short idle timeouts / short TTL** → shrink the reuse window.
- Network hijack: **encrypted transport** (TLS/SSH/IPsec), **dynamic ARP inspection**, DHCP snooping, switch port security, IDS.

## The PAM angle (why the broker wins)
A hijack needs a token to steal. **PSM runs the privileged session on the broker, not on the admin's endpoint** — so there is **no local token/cookie to lift**, and a suspicious session can be killed live. Pair with:
- **Session brokering + recording** → no raw reusable token; every action attributable and replayable.
- **Step-up re-authentication (MFA)** for sensitive actions → a stolen session alone can't approve/delete/escalate.
- **Short idle timeouts + token rotation on privilege change** → captured session expires fast.
- **Bind sessions** to client attributes/MFA → a lifted cookie fails from a new context.

## Top traps
- **Network vs. application** is tested first: TCP/SEQ/RST/desync = **network**; cookies/tokens/XSS/fixation = **application**.
- **Fixation ≠ theft:** fixation *sets* the ID before login; theft *captures* an existing ID. Fix for fixation = **rotate the ID at login**.
- **Hijacking ≠ spoofing ≠ replay** — hijacking rides a live authenticated session, no password.
- **HttpOnly** stops script reading the cookie; **Secure** stops non-TLS transit; **SameSite** curbs CSRF. Don't swap them.
- **Blind = off-path, must predict SEQ** (harder); **non-blind = MITM sees traffic**.
- **UDP hijacking is easier** than TCP (no handshake/SEQ to defeat).
- **CSRF doesn't steal the token** — it makes the browser send an authenticated request.
- **RST hijacking doubles as a DoS** primitive.
