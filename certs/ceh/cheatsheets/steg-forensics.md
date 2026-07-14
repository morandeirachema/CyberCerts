# Steganography & File Forensics

Extract hidden data from images/files, crack archives, decode/decrypt. Pairs with the [challenge lab](../practical/challenge-lab/) and the [stego/crypto drills](../practical/drills/08-stego-and-crypto.md). **Practice on your own files only.**

## Triage any suspicious file (do these first, in order)
```bash
file secret.jpg                     # what is it really?
exiftool secret.jpg                 # metadata / Comment field (flags hide here)
strings -n 6 secret.jpg | less      # plain hidden text / URLs
binwalk secret.jpg                  # embedded/appended files?
xxd secret.jpg | head               # magic bytes / manual inspection
```

## Extract hidden data
```bash
# steghide (JPEG/BMP/WAV/AU) — asks a passphrase (try blank, then known/guessed)
steghide info secret.jpg
steghide extract -sf secret.jpg -p '<passphrase>'
# appended / embedded files -> carve them out
binwalk -e secret.jpg               # auto-extract -> _secret.jpg.extracted/
foremost -i disk.img -o out/        # recover files by signature
# PNG LSB stego
zsteg secret.png                    # (gem install zsteg)
# whitespace stego
stegsnow -C hidden.txt
# audio: open in Audacity -> Spectrogram view (flags drawn in the spectrum)
```

## Crack a steghide passphrase
```bash
stegseek secret.jpg /usr/share/wordlists/rockyou.txt     # very fast steghide bruteforce
# or: stegcracker secret.jpg /usr/share/wordlists/rockyou.txt
```

## Password-protected archives
```bash
zip2john secret.zip > zip.hash ; john zip.hash --wordlist=/usr/share/wordlists/rockyou.txt ; john --show zip.hash
hashcat -m 17200 zip.hash /usr/share/wordlists/rockyou.txt   # PKZIP
rar2john secret.rar > rar.hash ; john rar.hash               # RAR
office2john doc.docx > off.hash                              # Office docs
pdf2john file.pdf > pdf.hash                                 # PDF
```

## Decode / decrypt
```bash
echo 'aGVsbG8=' | base64 -d                 # base64
echo '68656c6c6f' | xxd -r -p                # hex
echo 'uryyb' | tr 'A-Za-z' 'N-ZA-Mn-za-m'    # ROT13
hashid '<string>'                            # is it a hash? which type?
openssl enc -d -aes-256-cbc -pbkdf2 -k <key> -in f.enc   # AES decrypt (given key)
gpg --decrypt msg.gpg                        # if you hold the private key / passphrase
```
For layered/unknown encodings, use **CyberChef** "Magic" (auto-detects): https://gchq.github.io/CyberChef/

## Quick "what tool?" map
| Clue | Tool |
|---|---|
| Image with a hidden message | strings → exiftool → steghide → zsteg |
| File looks bigger than it should | binwalk -e / foremost |
| `.zip/.rar/.pdf/.docx` needs a password | *2john → john/hashcat |
| Weird string (`==`, hex, ROT) | base64/xxd/tr, or CyberChef |
| Audio file | Audacity spectrogram / `steghide` (WAV) |

> Refs: steghide — http://steghide.sourceforge.net/ · stegseek — https://github.com/RickdeJager/stegseek · binwalk — https://github.com/ReFirmLabs/binwalk · CyberChef — https://gchq.github.io/CyberChef/
