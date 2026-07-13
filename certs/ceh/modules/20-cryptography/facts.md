# Module 20 — Cryptography · Must-Know Facts

> One-page, high-yield recall sheet. Cryptography is *definition-precise* — the exam rewards exact pairings. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## Symmetric vs. asymmetric (the master table)
| Property | Symmetric | Asymmetric |
|---|---|---|
| Keys | **one shared secret** | **public/private pair** |
| Speed | fast | slow (~orders of magnitude) |
| Best for | **bulk data encryption** | **key exchange + digital signatures** |
| Key distribution | hard | easy (publish public key) |
| Examples | AES, DES, 3DES, RC4, Blowfish, Twofish | RSA, ECC, Diffie-Hellman, ElGamal, DSA |

**TLS = both:** asymmetric to agree a session key, then symmetric (AES-GCM) for bulk data.

## Symmetric ciphers
| Cipher | Type | Key | Note |
|---|---|---|---|
| DES | block 64-bit | **56-bit** | broken (key too short) |
| 3DES | block 64-bit | 112/168 | legacy/deprecated |
| **AES** (Rijndael) | block 128-bit | 128/192/256 | **the standard**, FIPS 197 |
| RC4 | **stream** | variable | broken (old WEP/TLS) |
| Blowfish / Twofish | block | up to 448 / 256 | Schneier; Twofish = AES finalist |

**Modes:** **ECB** leaks patterns (never use) · **CBC** chains with IV (padding-oracle target) · **CTR** = block-as-stream · **GCM** = authenticated (integrity + confidentiality → prefer).

## Asymmetric algorithms — what each can do
| Algo | Hard problem | Capability |
|---|---|---|
| **RSA** | integer factorization | encryption **and** signatures |
| **Diffie-Hellman** | discrete log | **key exchange only** |
| **ECC** | elliptic-curve discrete log | like RSA, **smaller keys** (mobile/IoT) |
| **ElGamal** | discrete log | encryption + signatures |
| **DSA** | discrete log | **signatures only** |

## Hashing (integrity, one-way)
| Hash | Output | Status |
|---|---|---|
| MD5 | 128-bit | broken (collisions) |
| SHA-1 | 160-bit | broken (SHAttered) |
| SHA-2 (256/384/512) | 256+ | secure |
| SHA-3 (Keccak) | variable | secure (sponge) |
| RIPEMD-160 | 160-bit | ok; Bitcoin |

Resists **preimage · second-preimage · collision**. Hashing ≠ encryption (no confidentiality, not reversible).

## Password hashing (KDFs) — NOT fast hashes
Use **bcrypt · scrypt (memory-hard) · Argon2 (PHC winner) · PBKDF2**. **Salt** defeats rainbow tables; **work factor** slows brute force. Using MD5/SHA-256 for passwords is *wrong* (too fast).

## PKI & signatures
- Components: **CA** (issues/signs), **RA** (verifies identity), **X.509** cert (binds identity↔public key), **CRL/OCSP** (revocation), **root→intermediate→leaf** chain of trust.
- **Digital signature:** hash the message, encrypt the hash with **your private** key; verify with **your public** key → **integrity + authenticity + non-repudiation** (NOT confidentiality).
- **Confidential to a recipient:** encrypt with the **recipient's public** key. **Prove it's from you:** sign with **your private** key. *(Swapping these is the #1 trap.)*

## TLS handshake (hybrid)
ClientHello → ServerHello + cert → verify chain → key exchange (ECDHE/RSA, asymmetric) → derive session key → bulk data via AES-GCM (symmetric). **TLS 1.3:** 1-RTT, mandatory **forward secrecy** (ephemeral DH), dropped RSA key transport & RC4.

## Disk/email encryption
| Tool | Scope | Trust model |
|---|---|---|
| BitLocker | full disk (Win) | AES, TPM-sealed |
| PGP/GPG | files/email | **web of trust** |
| S/MIME | email | **X.509 / CA (PKI)** |

## Crypto attacks
Brute force · **Birthday** (collision in ~2^(n/2)) · Collision · Known/Chosen-plaintext (KPA/CPA) · Chosen-ciphertext (CCA) · **Side-channel** (timing/power) · **Padding oracle** (CBC) · **MITM on unauthenticated DH** · Rainbow table (unsalted).

## Stego vs. crypto
**Crypto scrambles** content (visibly encrypted); **stego hides existence** (LSB in an image). Detecting hidden data = **steganalysis**.

## PAM angle
Keys are secrets: **vault + rotate + audit** them. HSM-back the vault master/Server Key; use Conjur for app keys. See [pam-architecture.md](../../defender-pam/pam-architecture.md).

## Top traps
- **Encrypt with recipient's public key**; **sign with your private key.**
- **DH = key exchange only**; **DSA = signatures only**; **RSA = both.**
- **ECB is the bad mode** (penguin); **GCM** is authenticated.
- Password storage = **slow salted KDF**, never plain MD5/SHA.
- Digital signatures give **non-repudiation**, not confidentiality.
