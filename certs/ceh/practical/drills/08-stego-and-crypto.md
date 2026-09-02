# Drill Pack 08 — Steganography & Crypto

> **Prereq:** generate the artifacts first — `../challenge-lab/setup-challenges.sh` drops everything under `~/ceh-practical-challenges/`. Then **set `C=~/ceh-practical-challenges`** and keep [`../challenge-playbooks.md`](../challenge-playbooks.md) open. These are the [challenge-lab](../challenge-lab/README.md) stego/crypto artifacts turned into 10 timed, Practical-style drills — detection → extraction → decode → decrypt, easy to hard. Concepts: [Module 20 — Cryptography](../../modules/20-cryptography/README.md). Timer on; expand the solution only when solved or stuck.

---

### 1. Triage: which of the four `stego/` images hide data — and how? ⏱️ 3 min

Fingerprint `vacation.jpg`, `cat.jpg`, `beach.jpg`, `carrier.jpg` *before* extracting. Name the method used in each.

<details><summary>Solution</summary>

```bash
file      $C/stego/*.jpg                          # oversized/appended?
strings   $C/stego/vacation.jpg | grep -i CEH     # plaintext in the bytes?
exiftool  $C/stego/carrier.jpg   | grep -i comment # metadata fields
binwalk   $C/stego/cat.jpg                         # appended files (scan only)
steghide info $C/stego/beach.jpg                   # "embedded data" prompt?
```

**You should see** each carrier expose its method:

```
vacation.jpg → cleartext flag        (strings)
carrier.jpg  → flag in EXIF Comment   (exiftool)
cat.jpg      → Zip archive after JPEG (binwalk / appended)
beach.jpg    → steghide embedded data (needs a passphrase)
```

**Answer:** strings / EXIF / appended-Zip / steghide — those map to drills 2–5.

**⚡ faster (CyberChef):** chain **Detect File Type** → **Extract strings** / **Extract EXIF** to triage in-browser (no steghide there — that stays CLI).

</details>

### 2. Find the flag hidden in plain sight in `vacation.jpg` ⏱️ 3 min

<details><summary>Solution</summary>

```bash
strings $C/stego/vacation.jpg | grep CEH
```

**You should see:** `CEH{plain_strings_in_the_file}`

**Flag:** `CEH{plain_strings_in_the_file}`

**⚡ faster (CyberChef):** upload the file into **Extract strings** with regex `CEH\{.*\}`.

</details>

### 3. Read the flag hidden in `carrier.jpg`'s metadata ⏱️ 3 min

<details><summary>Solution</summary>

```bash
exiftool $C/stego/carrier.jpg | grep -i comment
# or dump every tag:  exiftool -a -u -g1 $C/stego/carrier.jpg
```

**You should see:**

```
Comment  : CEH{hidden_in_exif_metadata}
```

**Flag:** `CEH{hidden_in_exif_metadata}`

**⚡ faster (CyberChef):** the **Extract EXIF** operation lists every field, Comment included.

</details>

### 4. Carve the file appended to `cat.jpg` ⏱️ 4 min

A valid JPEG with a whole ZIP glued to the end — recover the flag inside.

<details><summary>Solution</summary>

```bash
binwalk $C/stego/cat.jpg      # scan: JPEG image data ... + Zip archive
binwalk -e $C/stego/cat.jpg   # extract embedded files
find _cat.jpg.extracted -type f -name '*.txt' -exec cat {} +
```

**You should see** the appended archive flagged, then the carved flag:

```
0    0x0   JPEG image data, JFIF standard
...  ...   Zip archive data, ... .hidden.txt
CEH{carved_from_the_image}
```

**Flag:** `CEH{carved_from_the_image}` — if binwalk's extractor is blocked, `foremost -i $C/stego/cat.jpg -o out/` or `unzip $C/stego/cat.jpg` (unzip ignores the JPEG prefix) also work.

**⚡ faster (CyberChef):** **Detect File Type** → **Extract Files** (Forensics) carves the embedded ZIP from the upload.

</details>

### 5. Extract the steghide-embedded flag from `beach.jpg` (pw `hacktheplanet`) ⏱️ 4 min

<details><summary>Solution</summary>

```bash
steghide info $C/stego/beach.jpg                                     # confirms embedded data
steghide extract -sf $C/stego/beach.jpg -p hacktheplanet -xf flag.txt
cat flag.txt
```

**You should see:**

```
wrote extracted data to "flag.txt".
CEH{steghide_embedded_flag}
```

**Flag:** `CEH{steghide_embedded_flag}` — `-xf` forces the output name (else steghide writes the embedded file's original dot-name). Unknown passphrase? Brute-force with `stegseek beach.jpg rockyou.txt`.

**⚡ faster (CyberChef):** none — steghide's DCT embedding has no CyberChef op; CLI-only.

</details>

### 6. Decode these three strings ⏱️ 3 min

`aGVsbG8=`, `68656c6c6f`, `uryyb` — what does each decode to, and which transform is it?

<details><summary>Solution</summary>

Recognize the shape, then reverse it:

```bash
echo 'aGVsbG8=' | base64 -d                     # ends in '=', A–Za–z0–9  -> Base64
echo '68656c6c6f' | xxd -r -p                   # only 0–9a–f, even len  -> hex
echo 'uryyb' | tr 'A-Za-z' 'N-ZA-Mn-za-m'       # shifted text           -> ROT13
```

**You should see** all three resolve to `hello`.

**Answer:** `hello` — Base64, hex, ROT13 respectively. (`hashid '<str>'` tells you if a mystery string is instead a **hash**.)

**⚡ faster (CyberChef):** paste any into **Magic** — it auto-detects Base64/hex/ROTn.

</details>

### 7. Decode `crypto/mystery.txt` to the flag ⏱️ 5 min

Not encryption — encoding, stacked three deep. Peel it in reverse.

<details><summary>Solution</summary>

The stack is `base64( rot13( hex(flag) ) )`, so undo it outside-in: Base64 → ROT13 → hex.

```bash
cat $C/crypto/mystery.txt | base64 -d | tr 'A-Za-z' 'N-ZA-Mn-za-m' | xxd -r -p
```

**You should see:** `CEH{layered_encoding_is_not_encryption}`

**Flag:** `CEH{layered_encoding_is_not_encryption}`

**⚡ faster (CyberChef):** paste the contents into **Magic** (tick *Intensive mode*) — it unravels all three layers automatically.

</details>

### 8. Decrypt `crypto/secret.aes.enc` (key `s3cr3tkey`) ⏱️ 4 min

Real symmetric crypto: AES-256-CBC, key-derived with PBKDF2 (see `crypto/README.txt`).

<details><summary>Solution</summary>

```bash
openssl enc -d -aes-256-cbc -pbkdf2 -k s3cr3tkey -in $C/crypto/secret.aes.enc
```

**You should see:** `CEH{aes_with_a_known_key}`

**Flag:** `CEH{aes_with_a_known_key}` — must match how it was made: `-aes-256-cbc` **and** `-pbkdf2`. Drop `-pbkdf2` and OpenSSL uses the legacy KDF → "bad decrypt".

**⚡ faster (CyberChef):** **AES Decrypt** works but needs **Derive PBKDF2 key** first to handle the OpenSSL `Salted__` header — the one-line `openssl` is quicker here.

</details>

### 9. Decrypt `crypto/message.gpg` (pw `openme`) ⏱️ 4 min

GPG **symmetric** (password-based, not a keypair).

<details><summary>Solution</summary>

```bash
gpg --batch --passphrase openme -d $C/crypto/message.gpg
```

**You should see** (flag on stdout, cipher info on stderr):

```
gpg: AES256.CFB encrypted data
CEH{gpg_symmetric_flag}
```

**Flag:** `CEH{gpg_symmetric_flag}` — a `.gpg` encrypted *to a public key* instead needs the matching **private key** imported (`gpg --import priv.asc`), not a passphrase.

**⚡ faster (CyberChef):** none for symmetric GPG — its **PGP Decrypt** wants a private key + password, not a passphrase-only message. Use the `gpg` CLI.

</details>

### 10. Identify these hashes and name their hashcat modes ⏱️ 3 min

Identify `5f4dcc3b5aa765d61d8327deb882cf99`, a `$6$...` string, and a `$2b$...` string.

<details><summary>Solution</summary>

`hashid` recognizes the format; `-m` adds the hashcat mode:

```bash
hashid -m '5f4dcc3b5aa765d61d8327deb882cf99'   # 32 hex   -> MD5           (-m 0)
hashid '$6$ceh12345$...'                        # $6$      -> sha512crypt   (-m 1800)
hashid '$2b$10$...'                             # $2b$     -> bcrypt        (-m 3200)
```

**You should see** the type inferred from prefix/length:

```
[+] MD5
[+] SHA-512 Crypt   (Hashcat Mode: 1800)
[+] bcrypt          (Hashcat Mode: 3200)
```

**Answer:** MD5 (`-m 0`), sha512crypt `$6$` (`-m 1800`), bcrypt `$2b$` (`-m 3200`). Prefixes to know: `$1$` md5crypt, `$5$` sha256crypt, `$6$` sha512crypt, `$2a/$2b/$2y$` bcrypt. Cracking the plaintexts is [Pack 04](04-passwords-and-hashes.md).

**⚡ faster (CyberChef):** the **Analyse hashes** op reports likely types from length/charset.

</details>

---

## Score yourself

Mark each: ✅ solved cold under time · ⚠️ slow or needed a peek · ❌ stuck.

| # | Drill | Tool / skill | Flag / answer | Score |
|---|---|---|---|---|
| 1 | Triage the four images | file · strings · exiftool · binwalk | strings/EXIF/zip/steghide |  |
| 2 | vacation.jpg | strings | `CEH{plain_strings_in_the_file}` |  |
| 3 | carrier.jpg | exiftool | `CEH{hidden_in_exif_metadata}` |  |
| 4 | cat.jpg | binwalk -e / foremost | `CEH{carved_from_the_image}` |  |
| 5 | beach.jpg | steghide (`hacktheplanet`) | `CEH{steghide_embedded_flag}` |  |
| 6 | Single-layer decode | base64 / xxd / tr | `hello` ×3 |  |
| 7 | mystery.txt | base64 → rot13 → hex | `CEH{layered_encoding_is_not_encryption}` |  |
| 8 | secret.aes.enc | openssl (`s3cr3tkey`) | `CEH{aes_with_a_known_key}` |  |
| 9 | message.gpg | gpg (`openme`) | `CEH{gpg_symmetric_flag}` |  |
| 10 | Identify hashes | hashid | MD5 / sha512crypt / bcrypt |  |

Any ⚠️/❌ → re-run `setup-challenges.sh` for a fresh copy and drill it again under the timer. When all ✅, move to [Pack 09](09-exploitation-privesc.md).

## Sources
- CyberChef (stacked encoding/crypto, Magic, Extract EXIF/Files) — https://gchq.github.io/CyberChef/
- steghide — http://steghide.sourceforge.net/ · stegseek (cracker) — https://github.com/RickdeJager/stegseek
- binwalk (file carving) — https://github.com/ReFirmLabs/binwalk · foremost — https://foremost.sourceforge.net/
- exiftool — https://exiftool.org/ · OpenSSL — https://www.openssl.org/ · GnuPG — https://gnupg.org/ · hashID — https://github.com/psypanda/hashID
