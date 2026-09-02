# Challenge Lab — Answer Key (spoilers!)

> **Don't read this until you've solved the challenge** (or you're genuinely stuck). Under the Practical's clock, reading answers builds nothing. Each solution shows the command and the result. Set `C=~/ceh-practical-challenges` first.

## 1. Hashes (`$C/hashes/hashes.txt`)
```bash
hashid '<hash>'                         # identify each
hashcat -m 0     md5.txt    rockyou.txt   # md5
hashcat -m 100   sha1.txt   rockyou.txt   # sha1
hashcat -m 1400  sha256.txt rockyou.txt   # sha256
hashcat -m 1800  s512.txt   rockyou.txt   # sha512crypt ($6$)
hashcat -m 3200  bcrypt.txt rockyou.txt   # bcrypt ($2b$)
hashcat -m 1000  ntlm.txt   rockyou.txt   # ntlm
```
| Type | Plaintext |
|---|---|
| md5 | `iloveyou` |
| sha1 | `superman` |
| sha256 | `trustno1` |
| sha512crypt | `iloveyou` |
| bcrypt | `superman` |
| ntlm | `trustno1` |

## 2. `crypto/mystery.txt`
Layers, decoded in reverse (base64 → rot13 → hex):
```bash
cat $C/crypto/mystery.txt | base64 -d | tr 'A-Za-z' 'N-ZA-Mn-za-m' | xxd -r -p
```
→ `CEH{layered_encoding_is_not_encryption}`  *(CyberChef "Magic" finds this too)*

## 3. `crypto/secret.aes.enc`
```bash
openssl enc -d -aes-256-cbc -pbkdf2 -k s3cr3tkey -in $C/crypto/secret.aes.enc
```
→ `CEH{aes_with_a_known_key}`

## 4. `crypto/message.gpg`
```bash
gpg --batch --passphrase openme -d $C/crypto/message.gpg
```
→ `CEH{gpg_symmetric_flag}`

## 5. `stego/vacation.jpg`
```bash
strings $C/stego/vacation.jpg | grep CEH
```
→ `CEH{plain_strings_in_the_file}`

## 6. `stego/cat.jpg` (appended zip)
```bash
binwalk -e $C/stego/cat.jpg        # or: foremost -i cat.jpg
cat _cat.jpg.extracted/*.txt        # find the carved .hidden.txt
```
→ `CEH{carved_from_the_image}`

## 7. `stego/beach.jpg` (steghide)
```bash
steghide extract -sf $C/stego/beach.jpg -p hacktheplanet
cat *.txt
```
→ `CEH{steghide_embedded_flag}`

## 8. `stego/carrier.jpg` (EXIF)
```bash
exiftool $C/stego/carrier.jpg | grep -i comment
```
→ `CEH{hidden_in_exif_metadata}`

## 9. `archives/secret.zip`
```bash
zip2john $C/archives/secret.zip > z.hash
john z.hash --wordlist=/usr/share/wordlists/rockyou.txt ; john --show z.hash
# password = letmein  ; then:
unzip -P letmein $C/archives/secret.zip && cat .flag.txt
```
→ password `letmein`, flag `CEH{cracked_the_zip_password}`

## 10. `pcap/traffic.pcap`
```bash
tshark -r $C/pcap/traffic.pcap -Y 'http.request.method=="POST"' -T fields -e http.file_data
# or Wireshark: right-click the POST -> Follow -> TCP Stream
```
→ username `admin`, password `Summer2025!`

## 11. `filehunt/`
```bash
grep -rIna CEH $C/filehunt/                          # finds the dotfile flag
cat $C/filehunt/.config/.flag                         # CEH{hidden_dotfile}
base64 -d $C/filehunt/backup/notes.b64                # CEH{base64_in_a_file}
rev $C/filehunt/backup/reversed.txt                   # CEH{reverse_me}
```

---

> Re-run `./setup-challenges.sh` for a fresh copy any time. The plaintexts/flags are fixed here, but the *skill* — identify → pick the right tool → produce the answer fast — is the point.
