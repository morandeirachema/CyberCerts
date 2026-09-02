# Challenge Lab — practice the types the main lab can't provide

The AD/web [lab](../../labs/README.md) is great for scanning, enumeration, web, SQLi, and AD. But the Practical also throws **steganography, packet-capture forensics, crypto/encoding, hash cracking, and password-protected archives** — which need artifacts, not a live host. [`setup-challenges.sh`](setup-challenges.sh) generates all of those **locally** so you can drill them under a timer.

> Everything is generated on your own machine for your own practice. Nothing here touches the network beyond loopback.

## Run it
```bash
cd practical/challenge-lab
./setup-challenges.sh                 # -> ~/ceh-practical-challenges/
gunzip -k /usr/share/wordlists/rockyou.txt.gz   # if you haven't already
```
It's **re-runnable** and skips any challenge whose tool is missing (telling you what to install). Clean up with `./setup-challenges.sh --clean`.

**For the full set, install the optional tools (all on Kali or one `apt` away):**
```bash
sudo apt install -y steghide imagemagick libimage-exiftool-perl gnupg zip \
                    apache2-utils python3-scapy binwalk foremost
# PNG LSB stego (optional): sudo gem install zsteg
```

## The challenges (answer each, then check `answers.md`)

⏱️ Give yourself the target time — the Practical is a race.

### hashes/ — cracking ⏱️ 3 min each
1. Crack every hash in `hashes/hashes.txt`. **What is each plaintext?** (Identify with `hashid` first, then `hashcat -m <mode>`.)

### crypto/ — encoding & decryption ⏱️ 5 min each
2. Decode `crypto/mystery.txt` to plaintext. **What is the flag?** (It's layered — three transforms.)
3. Decrypt `crypto/secret.aes.enc` (AES-256-CBC, pbkdf2, passphrase in `crypto/README.txt`). **Flag?**
4. Decrypt `crypto/message.gpg` (GPG symmetric, passphrase in `crypto/README.txt`). **Flag?**

### stego/ — steganography ⏱️ 4 min each
5. `stego/vacation.jpg` hides a flag in plain sight. **Find it.** (`strings`)
6. `stego/cat.jpg` has a file appended to it. **Recover the flag.** (`binwalk -e` / `foremost`)
7. `stego/beach.jpg` was made with steghide (passphrase = `hacktheplanet`). **Extract the flag.** *(needs steghide+imagemagick)*
8. `stego/carrier.jpg` hides a flag in its metadata. **Read it.** (`exiftool`) *(needs exiftool)*

### archives/ — password-protected ⏱️ 6 min
9. `archives/secret.zip` is password-protected. **Crack the password and read the flag.** (`zip2john` → `john`/`hashcat -m 17200`)

### pcap/ — packet forensics ⏱️ 6 min
10. `pcap/traffic.pcap` contains a login. **What are the username and password?** (Wireshark → Follow TCP Stream) *(needs python3-scapy to auto-generate; else see `pcap/README.txt`)*

### filehunt/ — find the flags ⏱️ 8 min for all
11. Three flags are hidden in `filehunt/` (a dotfile, a base64-encoded file, and a reversed file). **Recover all three.** (Tip: `grep -r CEH` finds the plaintext one instantly; the others need decoding.)

---

## How to drill this
- Run the generator, then **time-box each challenge** and solve it from the recipes in [`../challenge-playbooks.md`](../challenge-playbooks.md).
- Only open [`answers.md`](answers.md) after you've solved it (or truly stuck) — reading the answer teaches you nothing under exam pressure.
- Re-run `setup-challenges.sh` any time for a fresh set; combine with the lab [drills](../drills.md) and [drills/](../drills/README.md) for full coverage.

## Sources
- steghide: http://steghide.sourceforge.net/ · binwalk: https://github.com/ReFirmLabs/binwalk
- CyberChef (encoding/crypto): https://gchq.github.io/CyberChef/
- john the ripper (zip2john): https://www.openwall.com/john/
