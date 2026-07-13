# Appendix — Troubleshooting Common Beginner Problems

> **What you'll learn:** how to read an error message calmly and fix the dozen problems that trip up almost every beginner — permission errors, missing commands, unreachable lab hosts, broken wordlists, proxy and certificate headaches, clock skew, and hanging scans.
> **Prerequisites:** any chapter — keep this open in a tab while you work. ⬅️ [Course index](README.md)

This is the "why isn't it working?" page. Nothing here is your fault — every one of these has happened to everyone. The trick is always the same: **read the actual error**, match it to a row below, apply the fix. No shame, just steps.

---

## Permissions — "Permission denied" / "you must be root"

Many scans and system tools need root because they touch raw network sockets or protected files. Borrow root with `sudo` — but not everything needs it (a plain `nmap -sT` runs as the normal `kali` user).

| Symptom | Likely cause | Fix |
|---|---|---|
| `Permission denied` running a tool | Tool needs root | Put `sudo` in front |
| nmap: `You requested a scan type which requires root privileges` | `-sS` (SYN) and `-O` (OS detect) need raw sockets | Run `sudo nmap ...` |
| `bash: ./script.sh: Permission denied` | Script isn't executable | `chmod +x script.sh` then `./script.sh` |
| Can't write to `/usr/share/...` | Owned by root | `sudo` the command, or work in `~` |

```bash
sudo nmap -sS -O 192.168.56.20      # SYN scan + OS detection need root
chmod +x loot.sh && ./loot.sh       # make your own script runnable
```

## "command not found"

The tool either isn't installed, or your package list is stale. **Update first**, then install.

| Symptom | Likely cause | Fix |
|---|---|---|
| `command: not found` for a Kali tool | Not installed (Kali ships lean now) | `sudo apt install <pkg>` |
| Python tool missing (`impacket`, `certipy`) | Installed via pipx, not apt | `pipx install <tool>` |
| Tool only exists on GitHub | Niche/newer tool | `git clone <url>` then read its README |
| `apt install` says *Unable to locate package* | Package list is stale | `sudo apt update` first, then retry |

```bash
sudo apt update                     # ALWAYS refresh the list first
sudo apt install seclists nikto     # install from Kali's repo
pipx install impacket               # Python security tools
apt search <partial-name>           # can't find it? check the spelling
```

## Can't reach a lab host — `No route to host`, ping fails

This is the single most common lab problem, and it's almost always the **VirtualBox network setting**, not the tool.

| Symptom | Likely cause | Fix |
|---|---|---|
| `No route to host` / `Destination unreachable` | VM's network is NAT/Bridged, not host-only | Set the adapter to **Host-only** (`vboxnet0`) on **both** VMs |
| `ping 192.168.56.20` times out | Target VM is powered off | Start Metasploitable2 / the DC in VirtualBox |
| Kali has no `192.168.56.x` address | Host-only adapter missing or down | Check `ip a`; add the adapter in VM settings |
| Reachable, but a port is refused | Host firewall (common on the Windows DC) | Expected — try another service/port |

```bash
ip a          # do you have an inet 192.168.56.10 on the host-only NIC?
ip r          # is there a route for 192.168.56.0/24?
ping 192.168.56.20   # Ctrl+C to stop
```

If `ip a` shows no `192.168.56.x` address on Kali, the fix is in **VirtualBox → VM Settings → Network**: set Adapter to *Host-only Adapter*, name `vboxnet0`. See [03 — Networking basics](03-networking-basics.md) and [`../labs/topology.md`](../labs/topology.md).

## Wordlists — rockyou is missing

Kali ships `rockyou.txt` **compressed** to save space. You unzip it once.

| Symptom | Likely cause | Fix |
|---|---|---|
| `rockyou.txt: No such file or directory` | It's still gzipped as `.gz` | `sudo gunzip /usr/share/wordlists/rockyou.txt.gz` |
| Want more lists (users, subdomains) | SecLists not installed | `sudo apt install seclists` |

```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz     # one-time, unzips in place
sudo apt install seclists                           # more lists in /usr/share/seclists
```

## Burp Suite — browser won't load HTTPS / certificate errors

When Burp sits between your browser and a site, the browser sees Burp's certificate and (rightly) complains — until you tell it to trust Burp's CA.

| Symptom | Likely cause | Fix |
|---|---|---|
| Browser: *Your connection is not private* on every HTTPS site | Burp's CA cert not installed in the browser | Install Burp's CA (steps below) |
| Nothing appears in Burp's Proxy tab | Browser isn't pointed at Burp | Set proxy to `127.0.0.1:8080` |
| Pages hang forever | Proxy on but Burp not running / Intercept is ON | Start Burp; toggle **Intercept off** |

```text
1. Set the browser proxy to 127.0.0.1 : 8080 (use FoxyProxy in Firefox).
2. With the proxy on, visit http://burp and download "CA Certificate" (cacert.der).
3. Firefox: Settings → Privacy & Security → Certificates → View Certificates →
   Authorities → Import → tick "Trust to identify websites". Full steps in [08 — Web hacking](08-web-hacking.md).
```

## proxychains — traffic isn't being tunneled

`proxychains` only tunnels if the config points at a proxy that's actually listening on the right port.

| Symptom | Likely cause | Fix |
|---|---|---|
| Tool connects directly, ignores the proxy | Wrong SOCKS port in the config | Edit `/etc/proxychains4.conf` to match your listener |
| `Connection refused` for every hop | No proxy/pivot listening yet | Start the SSH `-D` / chisel / Meterpreter SOCKS proxy first |
| Some UDP/ICMP tools "don't work" | SOCKS can't carry them | Use TCP-based tools (e.g. `nmap -sT -Pn`) |

```bash
tail /etc/proxychains4.conf     # last line: socks5 127.0.0.1 1080 (must match your proxy)
proxychains nmap -sT -Pn 10.10.10.5      # force a TCP scan through the tunnel
```

## Kerberos / Active Directory — `KRB_AP_ERR_SKEW` (clock skew)

Kerberos refuses tickets if your clock differs from the Domain Controller by more than ~5 minutes. AD is also picky about **DNS** — names must resolve via the DC.

| Symptom | Likely cause | Fix |
|---|---|---|
| `KRB_AP_ERR_SKEW`, *clock skew too great* | Kali's time drifted from the DC | Sync Kali's clock to the DC |
| *KDC_ERR_C_PRINCIPAL_UNKNOWN* / can't find realm | Kali is using the wrong DNS | Point DNS at the DC's IP |

```bash
sudo ntpdate 192.168.56.30       # sync Kali's clock to the DC (or: sudo rdate -n 192.168.56.30)
echo "nameserver 192.168.56.30" | sudo tee /etc/resolv.conf   # DNS must point at the DC
```

## WinRM / Ansible to the Windows DC fails

Talking to Windows over WinRM (port `5985`) needs the service enabled, correct credentials, and — for Ansible — the right transport settings.

| Symptom | Likely cause | Fix |
|---|---|---|
| `Connection refused` on 5985 | WinRM not enabled on the DC | On the DC (PowerShell, admin): `Enable-PSRemoting -Force` |
| `evil-winrm` / Ansible: authentication failed | Wrong user/password or domain format | Try `DOMAIN\\user` or `user@domain`, verify the password |
| Ansible: certificate/SSL validation error | HTTPS/cert checks on 5986 | Use `ansible_winrm_server_cert_validation=ignore` for the lab |

```bash
nmap -p 5985,5986 192.168.56.30                      # is WinRM even listening?
evil-winrm -i 192.168.56.30 -u Administrator -p 'Password123!'
```

## Metasploit — `db_status` says disconnected

The Metasploit database (Postgres) stores hosts, services, and loot. If it's disconnected, (re)initialize it.

| Symptom | Likely cause | Fix |
|---|---|---|
| `[*] postgresql selected, no connection` | Database not initialized/started | `sudo msfdb init` |
| Was working, now broken after an update | Stale DB state | `sudo msfdb reinit` |

```bash
sudo msfdb init          # first-time setup
sudo msfdb reinit        # nuke & recreate if it's corrupted
msfconsole -q -x "db_status; exit"   # verify — should say "connected"
```

## apt errors — "Could not get lock" / broken packages

| Symptom | Likely cause | Fix |
|---|---|---|
| `Could not get lock /var/lib/dpkg/lock` | Another apt / auto-update is running | Wait a minute; or close the other package manager |
| *Unable to locate package* | Package list is stale | `sudo apt update` first |
| Install stops mid-way, packages "broken" | Interrupted install | `sudo apt --fix-broken install` |

```bash
sudo apt update                     # fixes most "not found" errors
sudo apt --fix-broken install       # repair a half-finished install
sudo dpkg --configure -a            # finish configuring interrupted packages
```

Don't force-delete the lock file while apt is genuinely running — just wait for it to finish.

## Wireless — monitor mode won't enable

Monitor mode needs an adapter that supports it, and no other process fighting for the interface. In a VM the adapter must be a **USB Wi-Fi dongle passed through** — the VM's built-in NIC can't do monitor mode.

| Symptom | Likely cause | Fix |
|---|---|---|
| `airmon-ng` starts but capture is empty | NetworkManager grabbed the interface | `sudo airmon-ng check kill` first |
| No `wlan0` inside the VM | USB adapter not passed through | VirtualBox → USB → add the dongle; install its driver |
| Monitor mode simply refuses | Chipset doesn't support it | Use a known-good adapter (Atheros/Ralink) |

```bash
sudo airmon-ng check kill           # stop NetworkManager/wpa_supplicant
sudo airmon-ng start wlan0          # creates wlan0mon
iw dev                              # confirm the monitor interface exists
```

## nmap is slow or seems to hang

| Symptom | Likely cause | Fix |
|---|---|---|
| Scan takes forever | Filtered ports make nmap wait on timeouts | Add `--min-rate 1000` or `-T4` |
| UDP scan never finishes | UDP is slow by nature; `-p-` makes it worse | Scan a few ports: `-sU -p 53,161,137` |
| "It froze" | It's still working, just quiet | Press **Enter** for a progress line, or add `--stats-every 10s` |

```bash
sudo nmap -sS -T4 --min-rate 1000 192.168.56.20      # faster TCP scan
sudo nmap -sU -p 53,69,161 192.168.56.20             # targeted UDP, not -p-
```

## Tool runs fine but returns "no results"

Nine times out of ten you scanned the **wrong host or interface** — a typo'd IP, a target that's off, or you're on the NAT NIC instead of host-only.

| Symptom | Likely cause | Fix |
|---|---|---|
| Empty output, no errors | Wrong target IP | Re-check the address; confirm the VM is up with `ping` |
| Nothing found on the lab subnet | You're bound to the wrong interface | `ip a` — confirm you have `192.168.56.10` |
| Web tool finds nothing | Wrong port | Docker apps are `localhost:8081–8084`, not 80 |

```bash
ip a                        # which interfaces/IPs do I actually have?
ping -c1 192.168.56.20      # is the target alive before I scan it?
```

## Golden rules

When something breaks, walk this list in order — it resolves the vast majority of problems:

1. **Update first.** Half of "this tool is broken" is a stale install: `sudo apt update`.
2. **Read the actual error.** The fix is usually in the words on screen — match them to a table above.
3. **Check your target and interface.** `ip a` and a quick `ping` catch wrong-IP / wrong-network mistakes instantly.
4. **Use `sudo` when the tool asks for it** — and only then. Not everything needs root.
5. **Snapshot before anything risky.** A broken Kali should be a 10-second rollback, not a reinstall.

## Next
➡️ Back to the [Course index](README.md) to continue, or jump to the chapter for the tool that's misbehaving.

## Sources
- Kali Docs — General Use & FAQ: https://www.kali.org/docs/general-use/
- Kali Docs — Troubleshooting: https://www.kali.org/docs/troubleshooting/
- Nmap Reference Guide (timing & performance): https://nmap.org/book/man-performance.html
- PortSwigger — Installing Burp's CA certificate: https://portswigger.net/burp/documentation/desktop/external-browser-config/certificate
