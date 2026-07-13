# Hashcat & John Cheatsheet

Offline cracking. Hashcat: https://hashcat.net/hashcat/ · John the Ripper: https://www.openwall.com/john/

> Crack only hashes from your own lab. `rockyou.txt` ships in Kali at `/usr/share/wordlists/rockyou.txt` (gunzip first if needed).

## Hashcat modes to memorize (`-m`)

| Mode | Hash |
|---|---|
| 0 | MD5 |
| 100 | SHA1 |
| 1400 | SHA-256 |
| 1000 | NTLM |
| 3000 | LM |
| 5600 | NetNTLMv2 (Responder captures) |
| 1800 | sha512crypt ($6$ — Linux /etc/shadow) |
| 500 | md5crypt ($1$) |
| 13100 | Kerberos 5 TGS-REP (Kerberoasting) |
| 18200 | Kerberos 5 AS-REP (AS-REP roasting) |
| 22000 | WPA-PBKDF2-PMKID+EAPOL (Wi-Fi) |
| 1600 | Apache apr1 ($apr1$) |

## Attack modes (`-a`)

| Mode | Attack |
|---|---|
| 0 | Straight (wordlist) |
| 1 | Combination |
| 3 | Brute force / mask |
| 6 | Wordlist + mask (hybrid) |
| 7 | Mask + wordlist (hybrid) |

## Hashcat examples

```bash
# Wordlist attack on NTLM
hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# Wordlist + rules (best bang for buck)
hashcat -m 1000 -a 0 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Mask brute force: 8 chars, upper+lower+digit
hashcat -m 1000 -a 3 hashes.txt ?a?a?a?a?a?a?a?a

# Kerberoast crack
hashcat -m 13100 -a 0 kerberoast.txt rockyou.txt

# Show cracked results / status
hashcat -m 1000 hashes.txt --show
```

Mask charsets: `?l` a-z · `?u` A-Z · `?d` 0-9 · `?s` symbols · `?a` all.

## John the Ripper examples

```bash
# Auto-detect + wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt
# Force a format
john --format=nt hashes.txt --wordlist=rockyou.txt
john --format=sha512crypt shadow.txt --wordlist=rockyou.txt
# Combine passwd + shadow first
unshadow /etc/passwd /etc/shadow > crackme.txt
john crackme.txt
# Show cracked
john --show hashes.txt
# List formats
john --list=formats
```

Identify an unknown hash first: `hashid '<hash>'` or `hash-identifier`.

## Recall

- **NTLM = 1000**, **Kerberoast (TGS) = 13100**, **WPA = 22000**. These three show up constantly.
- Rainbow tables are defeated by **salting**; that's why NTLM (unsalted) stays crackable.
- Prefer **wordlist + rules** over pure brute force for realistic speed.
