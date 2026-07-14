#!/usr/bin/env bash
# =============================================================================
# CEH Practical — local challenge generator
# -----------------------------------------------------------------------------
# Builds the challenge *types* the AD/web lab can't provide — steganography,
# packet-capture forensics, crypto/encoding, hash cracking, password-protected
# archives, and file hunts — so you can drill them under a timer.
#
# Everything is generated LOCALLY, on YOUR machine, for YOUR practice only.
# Nothing here touches the network beyond loopback. Answers are in answers.md
# (keep it closed until you've solved a challenge).
#
# Usage:   ./setup-challenges.sh [output_dir]     (default: ~/ceh-practical-challenges)
#          ./setup-challenges.sh --clean [dir]    (remove generated files)
#
# Re-runnable (idempotent). Skips any challenge whose tool is missing and tells
# you how to install it. Best run on Kali; needs: coreutils, openssl, zip.
# Optional (each enables one more challenge): steghide, imagemagick, exiftool,
# gpg, python3-scapy, apache2-utils (htpasswd), zip.
# =============================================================================
set -u

OUT="${1:-$HOME/ceh-practical-challenges}"
if [ "${1:-}" = "--clean" ]; then OUT="${2:-$HOME/ceh-practical-challenges}"; rm -rf "$OUT"; echo "[+] Removed $OUT"; exit 0; fi

have() { command -v "$1" >/dev/null 2>&1; }
mk()   { for d in "$@"; do mkdir -p "$OUT/$d"; done; }
note() { printf '  [-] %s\n' "$*"; }
ok()   { printf '  [+] %s\n' "$*"; }

echo "[*] Generating CEH Practical challenges in: $OUT"
mkdir -p "$OUT"

# A few plaintexts that live in rockyou (so they're crackable in the drills).
P1="iloveyou"; P2="superman"; P3="trustno1"; ZIPPW="letmein"; STEGPW="hacktheplanet"

# ---------------------------------------------------------------------------
# 1) HASH CRACKING  -> practice hashcat/john + hash identification
# ---------------------------------------------------------------------------
echo "[*] [1] hashes/"
mk hashes
{
  echo "# Crack each hash. Identify the type first (hashid), then use the right -m mode."
  printf 'md5:    %s\n'    "$(printf '%s' "$P1" | md5sum | cut -d' ' -f1)"
  printf 'sha1:   %s\n'    "$(printf '%s' "$P2" | sha1sum | cut -d' ' -f1)"
  printf 'sha256: %s\n'    "$(printf '%s' "$P3" | sha256sum | cut -d' ' -f1)"
} > "$OUT/hashes/hashes.txt"
# sha512crypt (openssl is always on Kali)
if have openssl; then
  printf 'sha512crypt: %s\n' "$(openssl passwd -6 -salt ceh12345 "$P1")" >> "$OUT/hashes/hashes.txt"; fi
# bcrypt (needs htpasswd from apache2-utils) — keep the full $2y$.. so hashcat -m 3200 parses it
if have htpasswd; then
  BC="$(htpasswd -bnBC 10 "" "$P2" 2>/dev/null | cut -d: -f2 | tr -d '\n')"
  printf 'bcrypt: %s\n' "$BC" >> "$OUT/hashes/hashes.txt"
else note "bcrypt skipped — install: sudo apt install apache2-utils"; fi
# NTLM (MD4 of UTF-16LE) — try python3, then openssl legacy provider
NTLM=""
if have python3; then NTLM="$(python3 - "$P3" <<'PY' 2>/dev/null
import sys,hashlib
try: print(hashlib.new('md4', sys.argv[1].encode('utf-16le')).hexdigest())
except Exception: pass
PY
)"; fi
if [ -z "$NTLM" ] && have openssl; then
  NTLM="$(printf '%s' "$P3" | iconv -f ASCII -t UTF-16LE 2>/dev/null | openssl dgst -md4 -provider legacy -provider default 2>/dev/null | awk '{print $NF}')"; fi
if [ -n "$NTLM" ]; then printf 'ntlm: %s\n' "$NTLM" >> "$OUT/hashes/hashes.txt"
else note "NTLM skipped — md4 unavailable (fine; the others still work)"; fi
ok "hashes/hashes.txt  (crack with: hashcat -m <mode> hashes.txt rockyou.txt)"

# ---------------------------------------------------------------------------
# 2) CRYPTO / ENCODING  -> practice decoding + symmetric decrypt
# ---------------------------------------------------------------------------
echo "[*] [2] crypto/"
mk crypto
FLAG2="CEH{layered_encoding_is_not_encryption}"
# nested: base64( rot13( hex( flag ) ) )   -- decode in reverse
HEX="$(printf '%s' "$FLAG2" | xxd -p | tr -d '\n')"
ROT="$(printf '%s' "$HEX" | tr 'A-Za-z' 'N-ZA-Mn-za-m')"
printf '%s' "$ROT" | base64 > "$OUT/crypto/mystery.txt"
echo "Decode mystery.txt back to plaintext. (Three layers. Try CyberChef 'Magic'.)" > "$OUT/crypto/README.txt"
# openssl AES file with the key GIVEN
if have openssl; then
  printf 'CEH{aes_with_a_known_key}' | openssl enc -aes-256-cbc -pbkdf2 -salt -k "s3cr3tkey" -out "$OUT/crypto/secret.aes.enc" 2>/dev/null
  echo "secret.aes.enc: AES-256-CBC, pbkdf2, passphrase = s3cr3tkey" >> "$OUT/crypto/README.txt"
  ok "crypto/secret.aes.enc  (decrypt: openssl enc -d -aes-256-cbc -pbkdf2 -k s3cr3tkey -in secret.aes.enc)"; fi
# gpg symmetric with passphrase GIVEN
if have gpg; then
  printf 'CEH{gpg_symmetric_flag}' | gpg --batch --yes --passphrase "openme" -c -o "$OUT/crypto/message.gpg" 2>/dev/null
  echo "message.gpg: GPG symmetric, passphrase = openme" >> "$OUT/crypto/README.txt"
  ok "crypto/message.gpg  (decrypt: gpg --batch --passphrase openme -d message.gpg)"
else note "gpg challenge skipped — install: sudo apt install gnupg"; fi
ok "crypto/mystery.txt  (nested base64/rot13/hex)"

# ---------------------------------------------------------------------------
# 3) STEGANOGRAPHY  -> practice steghide / strings / exif / binwalk / zsteg
# ---------------------------------------------------------------------------
echo "[*] [3] stego/"
mk stego
# a base carrier image (ImageMagick), else a tiny placeholder
if have convert; then
  convert -size 640x400 xc:skyblue -pointsize 40 -gravity center -annotate 0 "CEH LAB" "$OUT/stego/carrier.jpg" 2>/dev/null
else printf 'JPEGPLACEHOLDER' > "$OUT/stego/carrier.jpg"; note "imagemagick missing — carrier is a placeholder (install: sudo apt install imagemagick)"; fi
# 3a) steghide-embedded flag (passphrase given)
if have steghide && [ -s "$OUT/stego/carrier.jpg" ]; then
  printf 'CEH{steghide_embedded_flag}' > "$OUT/stego/.s.txt"
  cp "$OUT/stego/carrier.jpg" "$OUT/stego/beach.jpg"
  steghide embed -cf "$OUT/stego/beach.jpg" -ef "$OUT/stego/.s.txt" -p "$STEGPW" -q 2>/dev/null && \
    ok "stego/beach.jpg  (steghide, passphrase = $STEGPW)"
  rm -f "$OUT/stego/.s.txt"
else note "steghide challenge skipped — install: sudo apt install steghide"; fi
# 3b) strings-in-image (no tools needed to build)
cp "$OUT/stego/carrier.jpg" "$OUT/stego/vacation.jpg" 2>/dev/null
printf '\nCEH{plain_strings_in_the_file}\n' >> "$OUT/stego/vacation.jpg"
ok "stego/vacation.jpg  (hint: strings)"
# 3c) appended ZIP (binwalk/foremost carve)
printf 'CEH{carved_from_the_image}' > "$OUT/stego/.hidden.txt"
( cd "$OUT/stego" && zip -q hidden.zip .hidden.txt && cat carrier.jpg hidden.zip > cat.jpg && rm -f hidden.zip .hidden.txt )
ok "stego/cat.jpg  (hint: binwalk -e  /  foremost)"
# 3d) EXIF comment
if have exiftool; then
  exiftool -overwrite_original -Comment='CEH{hidden_in_exif_metadata}' "$OUT/stego/carrier.jpg" >/dev/null 2>&1 && \
    ok "stego/carrier.jpg  (hint: exiftool)"
else note "exif challenge skipped — install: sudo apt install libimage-exiftool-perl"; fi

# ---------------------------------------------------------------------------
# 4) PASSWORD-PROTECTED ARCHIVE  -> practice zip2john + hashcat
# ---------------------------------------------------------------------------
echo "[*] [4] archives/"
mk archives
if have zip; then
  printf 'CEH{cracked_the_zip_password}' > "$OUT/archives/.flag.txt"
  ( cd "$OUT/archives" && zip -q -P "$ZIPPW" secret.zip .flag.txt && rm -f .flag.txt )
  ok "archives/secret.zip  (crack: zip2john secret.zip > z.hash ; john z.hash)"
else note "zip challenge skipped — install: sudo apt install zip"; fi

# ---------------------------------------------------------------------------
# 5) PCAP FORENSICS  -> practice Wireshark 'Follow TCP Stream'
# ---------------------------------------------------------------------------
echo "[*] [5] pcap/"
mk pcap
BUILT=""
if have python3 && python3 -c "import scapy.all" 2>/dev/null; then
  python3 - "$OUT/pcap/traffic.pcap" <<'PY' 2>/dev/null && BUILT=1
import sys
from scapy.all import Ether, IP, TCP, Raw, wrpcap
body = "username=admin&password=Summer2025!&submit=Login"
req  = ("POST /login HTTP/1.1\r\nHost: portal.ceh.lab\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(body)}\r\n\r\n{body}")
c2s = Ether()/IP(src="192.168.56.101",dst="192.168.56.50")/TCP(sport=51000,dport=80,flags="PA",seq=1)/Raw(load=req)
s2c = Ether()/IP(src="192.168.56.50",dst="192.168.56.101")/TCP(sport=80,dport=51000,flags="PA",seq=1)/Raw(load="HTTP/1.1 302 Found\r\nLocation: /dashboard\r\n\r\n")
wrpcap(sys.argv[1], [c2s, s2c])
PY
fi
if [ -n "$BUILT" ]; then
  ok "pcap/traffic.pcap  (Wireshark -> Follow TCP Stream, or: tshark -r traffic.pcap -Y http.request.method==POST)"
else
  cat > "$OUT/pcap/README.txt" <<'EOF'
scapy not available, so no synthetic pcap was built. Make your own instead:
  1) sudo tcpdump -i <lab-iface> -w mine.pcap
  2) log into the lab FTP:  ftp 192.168.56.20   (msfadmin / msfadmin)
  3) stop tcpdump, then in Wireshark: Follow TCP Stream, or
     tshark -r mine.pcap -Y 'ftp.request.command=="PASS"' -T fields -e ftp.request.arg
Install scapy to auto-generate this challenge:  sudo apt install python3-scapy
EOF
  note "pcap auto-gen skipped — see pcap/README.txt (install python3-scapy)"
fi

# ---------------------------------------------------------------------------
# 6) FILE HUNT  -> practice find / grep / decoding on a filesystem
# ---------------------------------------------------------------------------
echo "[*] [6] filehunt/"
mk filehunt/documents filehunt/.config filehunt/backup
echo "Nothing to see here." > "$OUT/filehunt/documents/readme.txt"
printf 'CEH{hidden_dotfile}' > "$OUT/filehunt/.config/.flag"
printf '%s' "CEH{base64_in_a_file}" | base64 > "$OUT/filehunt/backup/notes.b64"
printf 'CEH{reverse_me}' | rev > "$OUT/filehunt/backup/reversed.txt"
ok "filehunt/  (hint: find . -name '.*' ; grep -r CEH ; base64 -d ; rev)"

# ---------------------------------------------------------------------------
echo
echo "[*] Done. $(find "$OUT" -type f | wc -l) files created."
echo "    Challenges & questions:  practical/challenge-lab/README.md"
echo "    Solutions (spoilers):    practical/challenge-lab/answers.md"
echo "    Wordlist:  gunzip -k /usr/share/wordlists/rockyou.txt.gz"
echo "    Clean up:  $0 --clean $OUT"
