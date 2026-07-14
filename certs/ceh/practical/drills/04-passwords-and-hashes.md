# Drill Pack 04 — Passwords & Hashes

> Deep, timed practice for the **"what is the password of user X?" / "crack this hash"** Practical family. **Prereq:** generate the [challenge-lab](../challenge-lab/) (`../challenge-lab/setup-challenges.sh` → `~/ceh-practical-challenges/`) and `gunzip -k /usr/share/wordlists/rockyou.txt.gz`. Recipes: [`../challenge-playbooks.md`](../challenge-playbooks.md); theory: [Module 06 — System Hacking](../../modules/06-system-hacking/). Online/shadow box: Metasploitable2 `192.168.56.20` (`msfadmin`/`msfadmin`). **Crack only hashes from your own lab.**

Set these once, then **the loop never changes: get the hash → name it (`hashid`) → pick the mode → crack.** The mode is everything: the right `-m` cracks in seconds, the wrong one "runs" forever and finds nothing.

```bash
C=~/ceh-practical-challenges          # challenge-lab output      | -m tells:
T=192.168.56.20                       # Metasploitable2           | 0 MD5(32hex) 100 SHA1(40) 1400 SHA256(64)
W=/usr/share/wordlists/rockyou.txt    #                           | 500 md5crypt($1$) 1800 sha512crypt($6$)
R=/usr/share/hashcat/rules/best64.rule#                           | 3200 bcrypt($2) 1000 NTLM 5600 NetNTLMv2 17200 zip
```

Score yourself: **✅ under target / ⚠️ over time / ❌ needed the solution.** Re-drill anything not ✅.

---

### Drill 1 — Identify a mystery hash, then crack it ⏱️ 4 min
**Q:** The first line of `$C/hashes/hashes.txt` is a bare 32-hex string with no prefix. What type is it, and what is the plaintext?

<details><summary>Solution</summary>

```bash
grep md5 $C/hashes/hashes.txt              # -> md5: f25a2fc72690b780b2a14e140ef6a9e0
hashid 'f25a2fc72690b780b2a14e140ef6a9e0'  # candidates: MD5, NTLM, ...
echo 'f25a2fc72690b780b2a14e140ef6a9e0' > md5.txt
hashcat -m 0 -a 0 md5.txt $W
```

**You should see** `hashid` list **MD5** *and* **NTLM** (32 hex is ambiguous) — context decides: web-app hashes, not a Windows SAM, so MD5. Hashcat prints `f25a2fc72690b780b2a14e140ef6a9e0:iloveyou` → answer type **MD5** (`-m 0`), plaintext **`iloveyou`**.

⚡ **faster:** for an obvious 32/40/64-hex hash you can skip `hashid` and go straight to `0`/`100`/`1400`. `hashcat -m 0 md5.txt --show` re-prints any result from the potfile instantly.
</details>

### Drill 2 — Crack the SHA-1 ⏱️ 3 min
**Q:** Crack the `sha1:` line in `$C/hashes/hashes.txt`. What is the plaintext?

<details><summary>Solution</summary>

```bash
grep sha1 $C/hashes/hashes.txt | awk '{print $2}' > sha1.txt   # 40 hex chars
hashid "$(cat sha1.txt)"                                       # -> SHA-1
hashcat -m 100 -a 0 sha1.txt $W
```

**You should see** `18c28604dd31094a8d69dae60f1bcd347f1afc5a:superman` → answer **`superman`** (SHA-1, `-m 100`).

⚡ **faster:** **40 hex = SHA-1**, always `-m 100`. Length tells you the type — no need to identify every time.
</details>

### Drill 3 — Crack the SHA-256 ⏱️ 3 min
**Q:** Crack the `sha256:` line. Note the correct mode — it's **not** `-m 0`.

<details><summary>Solution</summary>

```bash
grep sha256 $C/hashes/hashes.txt | awk '{print $2}' > sha256.txt   # 64 hex chars
hashcat -m 1400 -a 0 sha256.txt $W
```

**You should see** `203b70b5ae883932161bbd0bded9357e763e63afce98b16230be33f0b94c2cc5:trustno1` → answer **`trustno1`** (SHA-256, **`-m 1400`**).

⚡ **faster:** **64 hex = SHA-256 = `-m 1400`.** Classic trap: reaching for MD5 mode on a long hash — check the length first.
</details>

### Drill 4 — Crack the sha512crypt (`$6$`) shadow-style hash ⏱️ 6 min
**Q:** Crack the `sha512crypt:` line. Which mode, and why is this one slower than drills 1–3?

<details><summary>Solution</summary>

```bash
grep sha512crypt $C/hashes/hashes.txt | cut -d' ' -f2 > s512.txt   # starts with $6$
hashid "$(cat s512.txt)"                                            # -> sha512crypt
hashcat -m 1800 -a 0 s512.txt $W
# or let John auto-detect:
john --format=sha512crypt s512.txt --wordlist=$W ; john --show s512.txt
```

**You should see** `$6$ceh12345$BPtWux2wJiEi…SswBdZp5MyNL09CXC1:iloveyou` → answer **`iloveyou`** (sha512crypt, **`-m 1800`**).

⚡ **faster:** `$6$` is **salted, thousands of rounds** — deliberately slow versus a raw MD5, but trivial for a top-20 rockyou word. This is the format of a modern Linux `/etc/shadow`.
</details>

### Drill 5 — Crack the bcrypt (`$2`) hash ⏱️ 8 min
**Q:** Crack the `bcrypt:` line. What is the plaintext, and what's the mode?

<details><summary>Solution</summary>

```bash
grep bcrypt $C/hashes/hashes.txt | cut -d' ' -f2 > bcrypt.txt
cat bcrypt.txt        # must start with $2a$ / $2b$ / $2y$
hashcat -m 3200 -a 0 bcrypt.txt $W
```

**You should see** (salt is random each generation, so your hash differs) something like `$2y$10$Q9f…<random>…:superman` and `Status....: Cracked` → answer **`superman`** (bcrypt, **`-m 3200`**).

⚡ **faster / gotcha:** bcrypt is **intentionally slow** (cost 10) and CPU-bound — expect minutes, not milliseconds; that's the whole point of bcrypt. **If your line reads `bcrypt: y$10$…` (missing the leading `$2`), prepend it** so hashcat parses it: `sed -i 's/^y\$/\$2y\$/' bcrypt.txt`.
</details>

### Drill 6 — Crack the NTLM ⏱️ 3 min
**Q:** Crack the `ntlm:` line — another bare 32-hex string. Why is the mode different from drill 1's MD5?

<details><summary>Solution</summary>

```bash
grep ntlm $C/hashes/hashes.txt | awk '{print $2}' > ntlm.txt
hashid "$(cat ntlm.txt)"                    # MD5 / NTLM — same 32 hex ambiguity as drill 1
hashcat -m 1000 -a 0 ntlm.txt $W
# John equivalent: john --format=nt ntlm.txt --wordlist=$W
```

**You should see** `f773c5db7ddebefa4b0dae7ee8c50aea:trustno1` → answer **`trustno1`** (NTLM, **`-m 1000`**).

⚡ **faster:** MD5 and NTLM are visually identical (32 hex) — **context decides the mode**: a Windows SAM / `secretsdump` dump → NTLM (`1000`); a web-app DB → MD5 (`0`). NTLM is **unsalted**, so it cracks blazingly fast.
</details>

### Drill 7 — Crack `/etc/shadow` with unshadow + John ⏱️ 8 min
**Q:** What is `msfadmin`'s login password, cracked from `192.168.56.20`'s `/etc/shadow`?

<details><summary>Solution</summary>

```bash
# On the box (msfadmin can sudo), grab both files and copy back to Kali:
sudo grep msfadmin /etc/passwd > passwd.txt
sudo grep msfadmin /etc/shadow > shadow.txt
hashid "$(cut -d: -f2 shadow.txt)"          # $1$ -> md5crypt
unshadow passwd.txt shadow.txt > crackme.txt   # merge so John has the username
john --wordlist=$W crackme.txt
john --show crackme.txt
```

**You should see** `john --show` print `msfadmin:msfadmin:...` → answer **`msfadmin`**. Metasploitable2 uses **md5crypt `$1$` → `-m 500`** (hashcat route: `hashcat -m 500 shadow.txt $W`).

⚡ **faster:** **`unshadow` is the step people skip** — feeding raw `/etc/shadow` to John loses usernames. John auto-detects `$1$`, so you don't even need `--format`. `john --show` is your answer, not the scroll-by output.
</details>

### Drill 8 — Crack the password-protected `secret.zip` ⏱️ 6 min
**Q:** `$C/archives/secret.zip` is encrypted. Recover the **archive password** and read the **flag** inside.

<details><summary>Solution</summary>

```bash
zip2john $C/archives/secret.zip > z.hash      # extract the crackable hash
cat z.hash                                     # note the $pkzip2$... / $zip2$ format
john z.hash --wordlist=$W ; john --show z.hash
# hashcat route — PKZIP is mode 17200:
hashcat -m 17200 -a 0 z.hash $W
# then open it with the recovered password:
unzip -P letmein $C/archives/secret.zip -d /tmp/zc && cat /tmp/zc/.flag.txt
```

**You should see** John print `letmein (secret.zip)`, then the unzip reveal the flag → password **`letmein`**, flag **`CEH{cracked_the_zip_password}`** (PKZIP, **`-m 17200`**).

⚡ **faster:** John **auto-detects** the zip2john format — no `--format` needed, so the John route is the quickest one-liner here. Use `-m 17200` only if you want the GPU.
</details>

### Drill 9 — Online SSH brute force with Hydra ⏱️ 6 min
**Q:** What is the SSH password of `msfadmin` on `192.168.56.20` — cracked *online* against the live service?

<details><summary>Solution</summary>

```bash
hydra -l msfadmin -P $W ssh://$T -t 4 -f
```

**You should see** `[22][ssh] host: 192.168.56.20   login: msfadmin   password: msfadmin` → answer **`msfadmin`**.

⚡ **faster:** `-f` stops at the first hit; `-t 4` keeps it gentle (high `-t` locks real accounts and floods logs). Online is **slow and loud** — tens/sec vs. the GPU's millions/sec. If you suspect the password, test it directly: `nxc ssh $T -u msfadmin -p msfadmin`. Prefer offline the instant you have the hash.
</details>

### Drill 10 — Crack a NetNTLMv2 capture ⏱️ 6 min
**Q:** You captured a NetNTLMv2 authentication (e.g. from Responder). Save this hash to `net.txt` and crack it. What mode, and what is the plaintext?

```
admin::N46iSNekpT:08ca45b7d7ea58ee:88dcbe4446168966a153a0064958dac6:5c7830315c7830310000000000000b45c67103d07d7b95acd12ffa11230e0000000052920b85f78d013c31cdb3b92f5d765c783030
```

<details><summary>Solution</summary>

```bash
# (the hash above is the official hashcat example for mode 5600)
hashcat -m 5600 -a 0 net.txt $W
```

**You should see** the line ending `…:hashcat` and `Status....: Cracked` → answer **`hashcat`** (NetNTLMv2, **`-m 5600`**).

⚡ **faster:** in a real challenge you get this hash straight out of **Responder** (`Responder -I eth0`) when a host authenticates to you — the `user::DOMAIN:…` shape is the tell. Add `-r $R` to catch mangled passwords in one pass.
</details>

### Drill 11 — Rules: crack a mangled password with best64 ⏱️ 7 min
**Q:** An admin "hardened" their password by reversing a common word. Generate `md5(namrepus)`, then crack it — plain rockyou **fails**, but a rule set succeeds. Which rule mattered?

<details><summary>Solution</summary>

```bash
printf 'namrepus' | md5sum | cut -d' ' -f1 > mangled.txt   # -> cc3dac1c2d5bda29540637b5ffd6428f
hashcat -m 0 -a 0 mangled.txt $W                # plain rockyou: Exhausted, 0 cracked
hashcat -m 0 -a 0 mangled.txt $W -r $R          # + best64: cracked
```

**You should see** the first run end `Status....: Exhausted`, the second print `cc3dac1c2d5bda29540637b5ffd6428f:namrepus` — best64's **reverse rule (`r`)** turned rockyou's `superman` into `namrepus`. Answer **`namrepus`** (via **`-r best64.rule`**; the set also does capitalise, append-digit, and leet swaps `a→@`, `s→$`).

⚡ **faster:** **wordlist + `best64.rule` is the best bang-for-buck** — always your second attempt after a plain rockyou miss, before you reach for heavier sets (`dive.rule`) or masks. John's equivalent is `--rules`: `john --rules --wordlist=$W mangled.txt`.
</details>

---

## Score yourself

| # | Drill | Mode | Answer | ✅/⚠️/❌ |
|---|---|---|---|---|
| 1 | Identify + crack MD5 | `0` | `iloveyou` | |
| 2 | SHA-1 | `100` | `superman` | |
| 3 | SHA-256 | `1400` | `trustno1` | |
| 4 | sha512crypt `$6$` | `1800` | `iloveyou` | |
| 5 | bcrypt `$2` | `3200` | `superman` | |
| 6 | NTLM | `1000` | `trustno1` | |
| 7 | `/etc/shadow` (unshadow+John) | `500` | `msfadmin` | |
| 8 | `secret.zip` | `17200` | `letmein` → `CEH{cracked_the_zip_password}` | |
| 9 | Hydra SSH (online) | — | `msfadmin` | |
| 10 | NetNTLMv2 | `5600` | `hashcat` | |
| 11 | best64 rule (mangled) | `0 -r` | `namrepus` | |

When every row is ✅ cold, you own the whole **identify → mode → crack** loop the Practical drills relentlessly. Re-run `../challenge-lab/setup-challenges.sh` for fresh hashes. Log results in [`../../PROGRESS.md`](../../PROGRESS.md).

## Sources
- Hashcat — example hashes (one sample of every mode): https://hashcat.net/wiki/doku.php?id=example_hashes
- Hashcat wiki: https://hashcat.net/wiki/ · John the Ripper (Openwall): https://www.openwall.com/john/
- THC-Hydra: https://github.com/vanhauser-thc/thc-hydra · NetExec: https://www.netexec.wiki/
- Cheatsheet: [`../../cheatsheets/hashcat-john.md`](../../cheatsheets/hashcat-john.md) · Tool course: [Module 06 — System Hacking](../../modules/06-system-hacking/)
