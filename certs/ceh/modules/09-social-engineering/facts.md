# Module 09 — Social Engineering · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The core idea
You **attack the human, not the host** — no exploit, no patch. The "vulnerability" is trust. The exam tests the **taxonomy** hard: match the *technique* to the *channel* and to the right *bucket*.

## The three delivery vectors
| Vector | Definition | Techniques |
|---|---|---|
| **Human-based** | Person-to-person deception | Impersonation, pretexting, tailgating, piggybacking, shoulder surfing, dumpster diving, quid pro quo, eavesdropping, reverse SE |
| **Computer-based** | Software/web/email lures | Phishing, spear-phishing, whaling, pharming, pop-ups, scareware, fake sites |
| **Mobile-based** | Apps & phone messaging | Malicious/repackaged apps, **smishing**, fake security apps, SMS/QR lures |

> **Vishing** (voice) is telephony/computer-based but often grouped with mobile; **smishing** (SMS) is **mobile-based**. Match the channel to the term.

## The phishing family — by *target* and *channel*
| Term | Channel | Target / twist |
|---|---|---|
| Phishing | Email/web | Broad, untargeted spray |
| **Spear-phishing** | Email | *Specific* individual/group, personalized |
| **Whaling** | Email | *Executives / high-value* ("big fish") — a **subset of spear-phishing** |
| **Vishing** | Voice call | Verbal pretext ("this is IT support…") |
| **Smishing** | SMS text | Malicious link/number via text |
| **Pharming** | DNS / hosts file | Redirects a *correct* URL to a fake site — **no bad-link click needed** |
| **BEC** | Email | Impersonate an exec/vendor to authorize a **wire transfer / invoice change** |
| Angler | Social media | Fake support account hijacks a complaint |

Mnemonic: **spear** = one target · **whale** = one *big* target · **v**ishing = **v**oice · **sm**ishing = **SM**S · **pharming** = poisoned name resolution.

## Human-based techniques — know the exact distinctions
| Technique | What it is | Exam trap |
|---|---|---|
| **Pretexting** | Inventing a scenario/role to gain trust | The *story*, not the delivery |
| **Baiting** | Dangling malware bait (USB drop, "free" download) | Victim *curiosity/greed* takes the item |
| **Quid pro quo** | Offers a *service in exchange* (fake IT help) | "Something for something" — a *transaction* |
| **Tailgating** | Following an authorized person through a door | **No consent** from the badge-holder |
| **Piggybacking** | Authorized person *knowingly* lets you in | **With consent** ("hold the door") |
| **Impersonation** | Posing as staff/vendor/exec/delivery | Often combined with pretexting |
| **Dumpster diving** | Recovering info from discarded trash | Physical, non-electronic |
| **Shoulder surfing** | Watching someone type/read | Passwords, PINs, screens |
| **Eavesdropping** | Overhearing conversations/comms | Passive |
| **Reverse SE** | Attacker gets the *victim to ask them* for help | Victim initiates contact |

## Insider threats (they bypass the perimeter)
| Type | Motivation | Example |
|---|---|---|
| **Malicious** | Revenge, greed, espionage | Disgruntled admin exfiltrates data |
| **Negligent** | Carelessness, convenience | Reuses passwords, clicks phish |
| **Compromised** | Account taken over via SE | Phished user becomes the tool |
| **Professional / mole** | Planted for espionage | Long-game infiltration |

Answer for insiders = **least privilege, JIT, session monitoring, separation of duties** — *not* a firewall.

## The SE attack lifecycle
**Research → Hook → Play → Exit.** (EC-Council also: **Research target → Select victim → Develop relationship → Exploit**.) Research = OSINT/dumpster/org charts; Hook = pretext & first contact; Play = extract info/access; Exit = cover tracks, clean escape.

## Tool → purpose
| Tool | For |
|---|---|
| **SET** (Social-Engineer Toolkit) | Framework: credential-harvester clone pages, mass mailer, payloads |
| **Gophish** | Self-hosted phishing *campaign* platform (templates, tracking, reporting) |
| **King Phisher** | Phishing campaign toolkit with template server & metrics |
| **theHarvester / Maltego** | OSINT for the Research phase |

## Countermeasures
- **User awareness/training** — the near-universal "best" answer on the exam (you can't patch a human).
- **Phishing-resistant MFA (FIDO2/WebAuthn/passkeys)** — makes a harvested password worthless.
- **Email authentication: SPF + DKIM + DMARC** — kill spoofed sender domains (defeats BEC/whaling spoofing).
- **Strict help-desk identity verification** for privileged resets (callback, ticket, secondary factor, manager approval).
- **Report-phish button**, mail-gateway filtering, clean-desk, shredding, privacy screens, device control (USB).

## PAM angle (your world)
- **Phishing-resistant MFA + number-matching** at the vault/PVWA → stolen password unlocks nothing standing.
- **JIT elevation** → a phished admin holds *no durable* privilege to abuse.
- **Remote Access** (VPN-less, mobile-biometric MFA) → contains vendor/third-party spear-phish.
- **Privileged session recording** → turns a compromised insider into a *detected* one.

## Top traps
- **Tailgating** = *without* consent; **piggybacking** = *with* consent. Favorite question.
- **Whaling ⊂ spear-phishing** (spear-phish aimed at executives).
- **Pharming ≠ phishing** — pharming is **DNS/hosts poisoning**; the victim types the *right* URL and lands on a fake site, no click.
- **Quid pro quo** = offers a *service*; **baiting** = dangles an *item* (USB). Both trade on desire.
- **Reverse SE** — the *victim* initiates contact.
- **Vishing = voice, smishing = SMS.** Don't swap them.
- Best countermeasure ≈ **awareness + MFA**; technology alone never fully solves a human-trust attack.
