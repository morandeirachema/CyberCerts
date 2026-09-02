# Module 06 — System Hacking · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The methodology (in order)
**Gaining Access → Privilege Escalation → Maintaining Access → Clearing Logs.** Cracking/guessing is *gaining access*; log clearing is *anti-forensics*, the last phase — not privesc.

## Password attack taxonomy
| Category | What | Tool |
|---|---|---|
| Passive online | Sniff on the wire | Wireshark, Responder |
| Active online | Guess a live service | Hydra, Medusa, NetExec |
| Offline | Crack captured hashes | Hashcat, John |
| Non-electronic | Shoulder-surf, dumpster, social | — |

Strategies: **dictionary · brute force · hybrid · rule-based · rainbow table.**

## Windows credential stores
| Store | Holds | Attack |
|---|---|---|
| SAM | Local NT hashes | Dump with SYSTEM |
| LSASS (memory) | Logged-on creds, tickets | Mimikatz `sekurlsa` |
| NTDS.dit (DC) | All domain hashes | DCSync, VSS |
| LSA secrets | Service-acct passwords | `secretsdump` |

## Hash & ticket attacks — does it need cracking?
| Attack | Abuses | Crack? |
|---|---|---|
| **Pass-the-Hash** | NT hash used directly | **No** |
| **Pass-the-Ticket** | Reuse TGT/TGS | **No** |
| **Kerberoasting** | TGS for an SPN, crack the **service-account** password offline | **Yes** |
| **AS-REP roasting** | Accounts with preauth disabled | **Yes** |
| **Golden ticket** | Forged TGT signed with **krbtgt** hash | No (post-compromise) |
| **Silver ticket** | Forged TGS signed with the **service** account key | No |

## Numbers to memorize
- **Hashcat modes:** `0` MD5 · `100` SHA1 · `1000` NTLM · `1800` sha512crypt · `5600` NetNTLMv2 · `13100` Kerberos TGS-REP · `22000` WPA.
- **Kerberos encryption type on the wire:** RC4 = `0x17` (the Kerberoasting tell).
- **Key event IDs:** `4624` logon · `4625` failed logon · `4768` TGT · `4769` TGS · `4662` replication (DCSync) · `4672` special privileges · `1102` log cleared.

## Rainbow tables vs. salt
Rainbow table = precomputed hash→plaintext lookup. **Salt defeats it** (per-hash randomness kills precomputation). **NTLM is unsalted** → still crackable → why Kerberoasting works.

## Privilege escalation quick hits
- **Windows:** unquoted service paths, weak service perms, `AlwaysInstallElevated`, DLL hijacking, token impersonation, kernel exploits.
- **Linux:** `sudo -l`, SUID binaries (`find / -perm -4000`), writable cron, PATH abuse, kernel exploits.
- **Vertical** = gain higher privilege; **horizontal** = same level, different user.

## Anti-forensics (Maintaining/Clearing phase)
- Windows log clear: `wevtutil cl <log>` / `Clear-EventLog` (→ event `1102`).
- **NTFS Alternate Data Streams** hide data: `file.txt:hidden.exe`.
- **Steganography** hides data in media; **rootkits** hide presence (user/kernel/boot/firmware).

## The one-line PAM answer key
- Kerberoasting → **gMSA / CPM-rotated** long random service password (AES-only).
- PtH/PtT → **tiering + Protected Users + Credential Guard + LAPS**, sessions brokered so creds never hit the endpoint.
- LSASS dumping → **Credential Guard + EPM credential-theft protection**.
- DCSync → restrict replication rights to DCs, **Tier 0 isolation**, rotate **krbtgt twice** after compromise.
- Local-admin reuse → **LAPS** (unique per host).

## Top traps
- "Crack" in the question ⇒ **not** PtH (PtH needs no cracking).
- Kerberoasting cracks the **service account** password, not the user's.
- Golden = **krbtgt**; Silver = **service** key. Don't swap them.
- Salting stops **rainbow tables**, not brute force.
