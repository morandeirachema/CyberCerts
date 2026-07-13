# Module 20 — Cryptography · Guided Lab Walkthrough

> Hands-on with **your own** keys, files, and lab hosts only. Cryptography is best learned by *doing the operations*: encrypt, hash, sign, verify, and inspect a real TLS handshake. Each step: command, what you should see, a hint, and the defender/PAM takeaway. Outputs are **representative**.

**Goal:** feel the difference between symmetric/asymmetric, see why fast hashes are wrong for passwords, and read a live TLS handshake.

**Tools:** `openssl`, `gpg`, `hashcat` (all in Kali). Nothing here touches a system you don't own.

---

## Part A — Symmetric encryption (AES-GCM) and the ECB lesson

### A1. Encrypt/decrypt a file with AES-256-GCM
```bash
echo "the vault server key must never sit in cleartext" > secret.txt
openssl enc -aes-256-gcm -pbkdf2 -salt -in secret.txt -out secret.enc
openssl enc -d -aes-256-gcm -pbkdf2 -in secret.enc -out secret.dec
diff secret.txt secret.dec && echo "round-trip OK"
```
**You should see** `round-trip OK`. **Observe:** one shared passphrase both encrypts and decrypts — that's **symmetric**, and it's fast. `-pbkdf2 -salt` derives the key properly (don't use raw `-k`).

### A2. Why ECB is the "penguin" mode (concept check)
ECB encrypts identical plaintext blocks to identical ciphertext blocks, so structure leaks. You don't need an image to prove it — reason it out: with a 16-byte block, `openssl enc -aes-128-ecb` on `AAAAAAAAAAAAAAAA` repeated yields repeating ciphertext blocks; **GCM/CBC with an IV do not.**

**Defender/PAM view:** at rest, secrets belong in an encrypted, tamper-evident store, not a file — that's exactly what the [CyberArk Vault](../../defender-pam/pam-architecture.md) provides, with the master **Server Key** HSM-backed.

---

## Part B — Hashing, and why "fast" is wrong for passwords

### B1. Generate and identify hashes
```bash
echo -n 'password' | md5sum        # 5f4dcc3b5aa765d61d8327deb882cf99
echo -n 'password' | sha256sum
```
**Observe:** deterministic, one-way, fixed length. MD5 is 128-bit → weak to collisions and fast cracking.

### B2. Crack a fast hash vs. a slow KDF (the timing lesson)
```bash
# fast, unsalted MD5 — falls instantly
echo '5f4dcc3b5aa765d61d8327deb882cf99' > md5.txt
hashcat -m 0 md5.txt /usr/share/wordlists/rockyou.txt --quiet

# a bcrypt hash of the same word — orders of magnitude slower per guess
htpasswd -bnBC 10 "" password | tr -d ':\n' | sed 's/^..//' > bcrypt.txt
hashcat -m 3200 bcrypt.txt /usr/share/wordlists/rockyou.txt --quiet
```
**You should see** the MD5 crack in a heartbeat and the bcrypt crack proceed **far slower** (watch the H/s rate — millions/billions for MD5 vs. thousands for bcrypt).

<details><summary>Hint</summary>Hashcat mode `-m 0` = MD5, `-m 3200` = bcrypt. If `htpasswd` is missing: `sudo apt install apache2-utils`. The point is the **rate difference**, not fully cracking bcrypt — Ctrl-C after you see the H/s.</details>

**Observe:** the *only* thing that changed is the algorithm's speed — that's why passwords need **slow, salted KDFs** (bcrypt/scrypt/Argon2/PBKDF2). This is the concrete reason behind the Module 06/15 "MD5 hashes crack instantly" findings.

---

## Part C — Asymmetric: keys, encryption, signatures (GPG)

### C1. Generate a keypair and encrypt to a public key
```bash
gpg --batch --quick-generate-key "Lab User <lab@ceh.lab>" default default 0
gpg --armor --export "lab@ceh.lab" > lab_pub.asc          # share THIS (public)
echo "for your eyes only" > msg.txt
gpg --encrypt --recipient "lab@ceh.lab" msg.txt            # -> msg.txt.gpg
gpg --decrypt msg.txt.gpg
```
**You should see** the decrypted message. **Observe:** you encrypted with the **public** key; only the matching **private** key decrypts — the core asymmetric property.

### C2. Sign and verify
```bash
gpg --clearsign msg.txt          # signs with your PRIVATE key -> msg.txt.asc
gpg --verify msg.txt.asc         # anyone verifies with your PUBLIC key
```
**You should see** `Good signature from "Lab User <lab@ceh.lab>"`. **Observe:** signing proves **integrity + authenticity + non-repudiation** — it does **not** hide the message (it's clear-signed). Encrypt (recipient's public) and sign (your private) are *opposite* key directions — the #1 exam trap.

---

## Part D — Read a real TLS handshake
Point at a host **you own / are authorized to test** (or a lab web target):
```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null \
  | openssl x509 -noout -issuer -subject -dates
openssl s_client -connect example.com:443 -tls1_3 </dev/null 2>/dev/null | grep -E 'Protocol|Cipher'
```
**You should see** the cert issuer/subject/validity and a line like:
```
Protocol  : TLSv1.3
Cipher    : TLS_AES_256_GCM_SHA384
```
**Observe:** the negotiated suite shows the **hybrid** model — an (EC)DHE key exchange (asymmetric, forward secrecy) plus **AES-GCM** (symmetric, authenticated) for bulk data. That's the whole handshake in one line.

<details><summary>Hint</summary>If TLS 1.3 fails, the server may cap at 1.2 — drop `-tls1_3`. `-servername` sets SNI so you get the right cert on shared hosts.</details>

---

## What you should conclude
| You did | The exam-critical idea |
|---|---|
| AES round-trip | Symmetric = one key, fast, bulk data |
| MD5 vs bcrypt timing | Passwords need slow, salted KDFs |
| GPG encrypt/decrypt | Encrypt with **recipient's public** key |
| GPG sign/verify | Sign with **your private** key; signatures ≠ confidentiality |
| `s_client` cipher | TLS is hybrid: asymmetric key exchange + symmetric AES-GCM |

## Cleanup
```bash
rm -f secret.* msg.txt* md5.txt bcrypt.txt lab_pub.asc
gpg --batch --yes --delete-secret-and-public-key "lab@ceh.lab"   # remove the throwaway key
```

## Record it
Log commands, the H/s rates you saw, and the negotiated TLS suite in the **My lab log** table in [README.md](README.md); note misses in [PROGRESS.md](../../PROGRESS.md).
