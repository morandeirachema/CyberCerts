# 12 — Sniffing & MITM

> **What you'll learn:** what a packet is and how to capture one, why a switch makes sniffing hard, and how to become a **man-in-the-middle** to read a victim's traffic — using tcpdump and Wireshark to grab cleartext passwords, bettercap to ARP-poison the lab, and Responder to steal and crack Windows hashes.
> **Prerequisites:** [11 — Active Directory](11-active-directory.md). ⬅️ [Course index](README.md)

Sniffing is eavesdropping on a network. It sounds passive and harmless, but on a modern network *reading* someone else's traffic usually means first *redirecting* it — and that redirection can knock real networks offline. This chapter builds the idea from the ground up, then weaponizes it, then shows why encryption defeats it. Everything here is **lab-only**.

---

## What "sniffing" actually means

A **packet** is a small chunk of data. Anything your computer sends over a network — a web page, a login, a ping — is chopped into packets, each stamped with a source address, a destination address, and a payload (the actual contents). **Sniffing** is capturing those packets off the wire and reading them.

An **interface** (or NIC, network interface card) is the connection your machine uses to reach a network — `eth0`, `eth1`, `wlan0`. In our lab the host-only network `192.168.56.0/24` is on **`eth1`** (confirm with `ip a`; see [03 — Networking basics](03-networking-basics.md)). Every capture command needs to know which interface to listen on.

Normally a network card ignores any packet not addressed to it. **Promiscuous mode** tells the card, "accept and hand me *every* packet you see, not just my own." Capture tools switch this on automatically — which is why they need `sudo`.

## Why a switch means you must become the "man in the middle"

Old networks used a **hub**, which copied every frame to every port. On a hub, one machine could passively sniff the whole network. Easy — and extinct.

Modern networks use a **switch**. A switch learns which MAC address lives on which physical port (it stores this in a **CAM table**, also called the MAC table) and forwards each frame **only** to the port that owns the destination MAC. The upshot: plug Kali into a switch and passively sniff, and you see your own traffic plus broadcasts — almost nothing juicy.

To read *someone else's* traffic on a switch, you have to make it flow through you. That is a **man-in-the-middle (MITM)** attack, and the classic way to set one up is **ARP poisoning**.

**ARP** (Address Resolution Protocol) is how a machine finds the MAC address behind an IP on the local network. It shouts, "Who has `192.168.56.1`? Tell `192.168.56.31`," and the owner replies with its MAC. The fatal flaw: **ARP has no authentication.** Any machine can send a reply, and the most recent answer wins. So the attacker lies — telling the victim "the gateway's IP is at *my* MAC" and telling the gateway "the victim's IP is at *my* MAC." Now both send their traffic to Kali, Kali quietly forwards it on, and you sit in the middle reading everything.

| Term | Plain-English meaning |
|---|---|
| Packet / frame | A chunk of network data with to/from addresses and a payload |
| Interface | The card/connection you capture on (`eth1` in the lab) |
| Promiscuous mode | "Give me every packet you see," not just my own |
| CAM / MAC table | The switch's map of which MAC is on which port |
| ARP poisoning | Forging ARP replies to redirect a victim's traffic to you |
| MITM | Sitting between two hosts so their traffic passes through you |

The full attack taxonomy (MAC flooding, DHCP starvation, DNS poisoning, and the defenses) lives in [Module 08 — Sniffing](../modules/08-sniffing/).

## ⚠️ Safety first — read before you poison anything

**ARP poisoning and Responder are disruptive, active attacks.** They send forged traffic to other machines. On a real corporate or home network they cause outages, trip security alarms, and are illegal without written authorization.

- Run every command in this chapter **only** on your isolated lab segment `192.168.56.0/24`.
- Never point an attack at the gateway or a host you don't own.
- The lab is **host-only** — nothing leaks to the internet. Keep it that way; do not "bridge" the VM to make something work (see [03](03-networking-basics.md)).

If you are unsure whether a target is in-scope, it isn't.

## tcpdump — capturing from the command line

**tcpdump** is the no-frills packet capturer that is on almost every Linux box. Start by watching live traffic, then save a capture to a file for later analysis.

```bash
# List interfaces tcpdump can see
sudo tcpdump -D

# Watch live traffic on the lab interface (Ctrl+C to stop)
sudo tcpdump -i eth1 -n              # -n = don't resolve names/ports (faster, clearer)
```
You should see a scrolling line per packet: a timestamp, source `IP.port > `, destination `IP.port`, and flags. It goes by fast — that's why we filter and save.

A **capture filter** (BPF syntax) narrows what tcpdump records. Combine them with `and`/`or`:

```bash
sudo tcpdump -i eth1 host 192.168.56.20            # only traffic to/from Metasploitable2
sudo tcpdump -i eth1 port 21                        # only FTP
sudo tcpdump -i eth1 'tcp port 80 or tcp port 443'  # HTTP or HTTPS
```

Now **save a capture to a file** — a `.pcap` — so you can open it in Wireshark:

```bash
mkdir -p ~/lab/captures
sudo tcpdump -i eth1 -w ~/lab/captures/ftp.pcap port 21   # write raw packets to a file
# ...reproduce the traffic you want, then Ctrl+C...
tcpdump -r ~/lab/captures/ftp.pcap -A                      # read it back; -A = show ASCII payload
```
You should see the file fill while the FTP session happens, and on read-back the cleartext of the conversation appears in the `-A` output. `-w` writes, `-r` reads — no `sudo` needed just to read your own file.

> The scriptable cousin `tshark` reads the same files and takes Wireshark **display** filters: `tshark -r ~/lab/captures/ftp.pcap -Y 'ftp'`. Handy for grepping captures without a GUI.

## Wireshark — reading a capture like a book

**Wireshark** is the graphical analyzer. It captures live too, but the beginner-friendly workflow is: capture with tcpdump, then open the `.pcap` in Wireshark to explore it.

```bash
wireshark ~/lab/captures/ftp.pcap &    # open a saved capture (& = run in background)
```

The window has **three panes**, top to bottom:

| Pane | What it shows |
|---|---|
| **Packet list** (top) | One row per packet: number, time, source, destination, protocol, summary |
| **Packet details** (middle) | The selected packet broken into layers (Ethernet → IP → TCP → HTTP), expandable |
| **Packet bytes** (bottom) | The raw hex and ASCII of that packet — where cleartext passwords show up |

The real power is the **display filter** bar at the top. Unlike tcpdump's capture filters, display filters hide/show packets *already captured* and use their own syntax. Type one and press Enter:

| Display filter | Shows |
|---|---|
| `http.request` | Every outgoing HTTP request (page loads, form posts) |
| `ftp` | All FTP control traffic (logins live here) |
| `tcp.port==445` | SMB traffic (Windows file sharing / auth) |
| `http.request.method == "POST"` | Form submissions — where web logins are sent |
| `ftp.request.command == "PASS"` | The exact packet carrying an FTP password |

**Follow TCP Stream** is the killer feature: right-click any packet → **Follow → TCP Stream**. Wireshark stitches every packet of that one conversation back together and shows it as plain text — the whole FTP or HTTP exchange in one readable window, client text in one color and server text in another.

> Wireshark **display filters** (`http.request`) are a different language from tcpdump **capture filters** (`tcp port 80`). Mixing them up is the #1 beginner error — see [Module 08](../modules/08-sniffing/).

## Proving it: capturing cleartext credentials

Old protocols send passwords in the clear. Let's capture one against Metasploitable2 (`192.168.56.20`), which runs a cleartext FTP server.

```bash
# Terminal 1 — start capturing FTP before you log in
sudo tcpdump -i eth1 -w ~/lab/captures/ftp-login.pcap port 21

# Terminal 2 — log in to the target's FTP (any account; msfadmin/msfadmin works on Metasploitable2)
ftp 192.168.56.20
# enter a username and password at the prompts, then type: bye
```
Back in Terminal 1, press `Ctrl+C`, then open the file:

```bash
wireshark ~/lab/captures/ftp-login.pcap &
# In the display filter bar, type:  ftp
# Right-click a packet -> Follow -> TCP Stream
```
You should see the whole login in plain text, including `USER msfadmin` and `PASS msfadmin`. That is a real password, read straight off the wire — no cracking required. HTTP form logins (for example the DVWA login over `http://`) leak the same way: filter `http.request.method == "POST"` and read the `username=`/`password=` fields in the packet bytes.

**Now confirm encryption defeats this.** Repeat against an HTTPS site or an SSH/SFTP login and filter for `tls` or `tcp.port==22`:

```bash
sudo tcpdump -i eth1 -w ~/lab/captures/https.pcap 'tcp port 443'
# browse an https:// page or run an ssh session, then Ctrl+C and open it
```
You should see only **TLS Application Data** — encrypted gibberish. You can tell *that* two machines talked and *how much*, but not *what they said*. This is the whole lesson: MITM lets you see traffic, but **encryption removes the payoff.**

## ARP poisoning MITM with bettercap

To capture *another* machine's traffic on the switch, you must become the man-in-the-middle. **bettercap** automates the ARP poisoning. We'll put Kali (`192.168.56.10`) between the Windows member `ws01` (`192.168.56.31`) and the gateway (`192.168.56.1`).

First, **enable IP forwarding** so packets you intercept still reach their destination — otherwise you cut the victim's internet and the attack is obvious:

```bash
sudo sysctl -w net.ipv4.ip_forward=1     # let Kali forward packets it isn't the final destination for
```
You should see `net.ipv4.ip_forward = 1` printed back.

Now launch bettercap and drive it from its interactive prompt:

```bash
sudo bettercap -iface eth1
```
At the `»` prompt:

```bash
net.probe on                              # discover live hosts on the subnet
set arp.spoof.targets 192.168.56.31       # the victim we want to intercept (ws01)
set arp.spoof.fullduplex true             # poison BOTH victim and gateway (full MITM)
arp.spoof on                              # start sending forged ARP replies
net.sniff on                              # capture and print the intercepted traffic
```
You should see bettercap announce it is poisoning `192.168.56.31`, then a live feed of that host's connections — DNS lookups, HTTP requests, and any cleartext credentials it flags. To stop cleanly and un-poison the victim (restoring the real ARP entries), run `arp.spoof off` before quitting with `q`. **Always turn it off** — leaving a host poisoned breaks its networking.

> **Note on ettercap.** The older **ettercap** does the same job. Command-line: `sudo ettercap -T -i eth1 -M arp:remote /192.168.56.31// /192.168.56.1//` (text UI, ARP MITM between victim and gateway), or launch the GUI with `sudo ettercap -G`. bettercap is the modern default, but you'll see ettercap in older guides and the exam.

## Responder — stealing Windows hashes

When a Windows machine can't resolve a name through DNS, it falls back to broadcasting on **LLMNR** and **NBT-NS** — "does anyone know who `fileserv01` is?" **Responder** answers *every* such broadcast with "yes, that's me," the victim tries to authenticate, and Responder captures the resulting **NetNTLMv2** hash — a challenge/response you can crack offline into the user's password. No ARP poisoning needed; you just answer faster than nobody.

```bash
sudo responder -I eth1 -wv        # -I interface, -w rogue WPAD proxy, -v verbose
```
You should see Responder start its poisoners and listeners, then wait. Trigger it from the lab: on `ws01` (`192.168.56.31`), open Explorer and type a bad path like `\\fileserv01\share`, or run `ping doesnotexist` — the failed lookup makes Windows broadcast. Responder prints the captured hash and saves it under `/usr/share/responder/logs/`.

Crack the captured NetNTLMv2 hash with hashcat's mode **5600** (see [10 — Password attacks](10-password-attacks.md)):

```bash
# The saved log line IS the hash; point hashcat at it
hashcat -m 5600 ~/lab/captures/netntlmv2.txt /usr/share/wordlists/rockyou.txt
hashcat -m 5600 ~/lab/captures/netntlmv2.txt /usr/share/wordlists/rockyou.txt --show   # print result
```
You should see the username and cracked password once hashcat finds it in the wordlist. That credential is your foothold back into the domain from [11 — Active Directory](11-active-directory.md). The defense — **disabling LLMNR/NBT-NS** and enforcing SMB signing — is why this attack is graded so heavily on the exam.

## Common beginner mistakes

- **Sniffing the wrong interface.** If your capture is empty, you're probably on `eth0` (NAT) not `eth1` (the lab). Run `ip a` first and match the `192.168.56.x` address.
- **Forgetting `sudo`.** Capturing packets and putting the card in promiscuous mode need root. "You don't have permission to capture" means add `sudo`.
- **Forgetting IP forwarding before an ARP attack.** Without `net.ipv4.ip_forward=1`, you drop the victim's traffic instead of relaying it — an instant, obvious DoS.
- **Leaving a victim poisoned.** Always `arp.spoof off` and quit cleanly, or `ws01` loses its network until its ARP cache expires.
- **Confusing capture filters with display filters.** `tcp port 80` is tcpdump/BPF; `http.request` is Wireshark. They are not interchangeable.
- **Expecting to read HTTPS/SSH.** MITM shows you encrypted blobs, not passwords. Cleartext protocols (FTP, HTTP, Telnet) are the ones that leak.
- **Doing any of this off the lab.** ARP poisoning disrupts and is illegal on networks you don't own. `192.168.56.0/24` only.

## ✅ Practice task

1. Confirm your capture interface with `ip a` (should be `eth1` with `192.168.56.10`).
2. Capture FTP to a file with tcpdump while logging in to `192.168.56.20`; open it in Wireshark, filter `ftp`, and **Follow TCP Stream** to read the `USER`/`PASS` in cleartext.
3. Capture an HTTPS session and confirm you see only **TLS Application Data** — write down why encryption beat you.
4. Enable IP forwarding, then use bettercap to ARP-poison `192.168.56.31` ↔ `192.168.56.1`; watch `net.sniff` show the victim's traffic. Turn it off cleanly with `arp.spoof off`.
5. Run Responder on `eth1`, trigger a bad name lookup from a Windows host, capture the NetNTLMv2 hash, and crack it with `hashcat -m 5600`.
6. In your notes, match each attack to its defense (encryption, DAI, disabling LLMNR) using [Module 08](../modules/08-sniffing/).

## Next

➡️ [13 — Wireless](13-wireless.md): the same sniffing ideas over the air — monitor mode, capturing handshakes, and cracking Wi-Fi with the aircrack-ng suite.

## Sources

- Wireshark — User Guide & display filter reference: https://www.wireshark.org/docs/
- tcpdump — manual & examples: https://www.tcpdump.org/manpages/tcpdump.1.html
- bettercap — documentation: https://www.bettercap.org/
- Ettercap project: https://www.ettercap-project.org/
- Responder: https://github.com/lgandx/Responder
- hashcat — example hashes (mode 5600, NetNTLMv2): https://hashcat.net/wiki/doku.php?id=example_hashes
- MITRE ATT&CK — Adversary-in-the-Middle (T1557): https://attack.mitre.org/techniques/T1557/
