# Module 20 — Cryptography · Practice Questions

> **Original, concept-based questions** — not exam dumps. Answers collapsed: decide first, then expand. Target **≥80%**. Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** To send a message that **only the recipient** can read, you encrypt it with:

- A. Your private key
- B. Your public key
- C. The recipient's public key
- D. The recipient's private key

<details><summary>Answer</summary>

**C. The recipient's public key.** Only their matching *private* key can decrypt it. (Signing, by contrast, uses **your private** key. Swapping these two is the most common crypto trap.)
</details>

---

**Q2.** A digital signature provides all of the following **except**:

- A. Integrity
- B. Authenticity
- C. Non-repudiation
- D. Confidentiality

<details><summary>Answer</summary>

**D. Confidentiality.** A signature (hash encrypted with the signer's private key) proves who sent it and that it's unaltered, and prevents denial — but it does **not** hide the message. Encryption provides confidentiality.
</details>

---

**Q3.** Which algorithm performs **key exchange only** (no encryption or signing)?

- A. RSA
- B. Diffie-Hellman
- C. AES
- D. ECC

<details><summary>Answer</summary>

**B. Diffie-Hellman.** DH securely agrees a shared secret over an untrusted channel but can't encrypt or sign. RSA does both; **DSA** signs only; AES is symmetric. Memorize the capability of each.
</details>

---

**Q4.** Which block-cipher mode should you **never** use because identical plaintext blocks produce identical ciphertext (the "penguin")?

- A. GCM
- B. CBC
- C. CTR
- D. ECB

<details><summary>Answer</summary>

**D. ECB.** It leaks structure. Prefer **GCM** (authenticated: confidentiality + integrity). CBC is acceptable but is the padding-oracle target; CTR turns a block cipher into a stream.
</details>

---

**Q5.** What does adding a **salt** to a password hash defeat?

- A. Brute-force attacks
- B. Rainbow-table (precomputation) attacks
- C. Side-channel attacks
- D. Phishing

<details><summary>Answer</summary>

**B. Rainbow-table attacks.** A unique per-password salt makes precomputed tables useless. Slowing brute force is the job of a **work factor** (bcrypt/scrypt/Argon2/PBKDF2), a separate property.
</details>

---

**Q6.** Which is the correct choice for **storing user passwords**?

- A. MD5
- B. SHA-256
- C. Argon2 (or bcrypt/scrypt/PBKDF2)
- D. Base64 encoding

<details><summary>Answer</summary>

**C. Argon2 / bcrypt / scrypt / PBKDF2.** These are *slow, salted, tunable* KDFs. MD5 and SHA-256 are built to be **fast** — exactly wrong for passwords. Base64 is encoding, not hashing at all.
</details>

---

**Q7.** In the TLS handshake, asymmetric cryptography is used to ___ and symmetric to ___.

- A. encrypt bulk data; exchange keys
- B. exchange/agree a session key; encrypt bulk data
- C. hash the message; sign the message
- D. compress data; pad data

<details><summary>Answer</summary>

**B.** TLS is **hybrid**: asymmetric (RSA/ECDHE) agrees the session key, then fast symmetric (AES-GCM) encrypts the bulk data. TLS 1.3 mandates ephemeral DH for **forward secrecy**.
</details>

---

**Q8.** The **birthday attack** is relevant to which primitive, and roughly what work does it require for an n-bit output?

- A. Symmetric ciphers; 2^n
- B. Hash functions; ~2^(n/2)
- C. Asymmetric keys; 2^n
- D. Passwords; n²

<details><summary>Answer</summary>

**B. Hash functions; ~2^(n/2).** The birthday paradox means a collision is found in about the square root of the output space — why 128-bit hashes (MD5) are weak and 256-bit is preferred.
</details>

---

**Q9.** Which pair correctly matches the email-security technology to its **trust model**?

- A. PGP → X.509 CA hierarchy; S/MIME → web of trust
- B. PGP → web of trust; S/MIME → X.509 CA hierarchy
- C. Both use a CA hierarchy
- D. Both use a web of trust

<details><summary>Answer</summary>

**B. PGP/GPG = web of trust; S/MIME = X.509 / CA (PKI).** A frequent matching question.
</details>

---

**Q10.** A **padding-oracle** attack specifically targets:

- A. ECB mode
- B. CBC mode
- C. Hash functions
- D. RSA key generation

<details><summary>Answer</summary>

**B. CBC mode.** When a server reveals whether padding is valid, an attacker can decrypt ciphertext byte-by-byte. Authenticated modes (GCM) or encrypt-then-MAC prevent it.
</details>

---

**Q11.** DES is considered broken primarily because:

- A. It uses a 56-bit key (too short for modern brute force)
- B. It has no S-boxes
- C. It is an asymmetric cipher
- D. It cannot be implemented in hardware

<details><summary>Answer</summary>

**A. 56-bit key.** DES's key space is exhaustible by modern hardware. 3DES extended it (legacy); **AES** (128/192/256-bit) is the standard replacement.
</details>

---

**Q12.** What is the difference between **cryptography** and **steganography**?

- A. They are the same thing
- B. Cryptography scrambles content; steganography hides the message's very existence
- C. Steganography is always stronger
- D. Cryptography only works on images

<details><summary>Answer</summary>

**B.** Cryptography makes content unreadable (but visibly encrypted); steganography *conceals that a message exists* (e.g., LSB embedding in an image). Detecting hidden data is **steganalysis**; combine both for defense-in-depth.
</details>

---

**Q13.** Which algorithm is preferred for constrained devices (mobile/IoT) because it offers equivalent strength with **smaller keys**?

- A. RSA
- B. 3DES
- C. ECC
- D. DSA

<details><summary>Answer</summary>

**C. ECC.** Elliptic-curve crypto achieves RSA-equivalent security with much smaller keys, reducing compute/power — ideal for mobile and IoT (ties to Modules 17 and 18).
</details>

---

### Score yourself
- **12–13:** excellent — you have the pairings cold.
- **9–11:** re-drill the asymmetric-capability and public/private-key-direction facts.
- **< 9:** re-read [README.md](README.md) and the [facts.md](facts.md) master tables, then redo the [lab-walkthrough.md](lab-walkthrough.md).
