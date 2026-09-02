# 01 — Linux Essentials

> **What you'll learn:** how to move around Linux, read and change permissions, manage users and processes, and install tools — the survival skills every later chapter assumes.
> **Prerequisites:** [00 — Getting started](00-getting-started.md). ⬅️ [Course index](README.md)

Most beginner frustration in hacking isn't the tools — it's missing Linux basics. Spend real time here; it pays off everywhere.

---

## The filesystem — one big tree
Linux has no "C: drive." Everything hangs off a single root, written `/`. Key places:

| Path | What it holds |
|---|---|
| `/` | The root of everything |
| `/home/kali` | Your home folder (your files); shortcut: `~` |
| `/etc` | System configuration files |
| `/usr/share` | Shared data — **wordlists** live in `/usr/share/wordlists` |
| `/tmp` | Temporary files (wiped on reboot) |
| `/root` | The root user's home |

## Moving around
```bash
pwd                 # "print working directory" — where am I?
ls                  # list files here
ls -la              # long list, including hidden files (start with .) and permissions
cd /usr/share       # change directory
cd ~                # go home
cd ..               # go up one level
```
**Tab completion** is your best friend: type the first letters of a name and press **Tab** — Kali finishes it. Press it twice to see options.

## Reading, creating, moving files
```bash
cat file.txt              # print a file
less file.txt             # scroll a file (q to quit)
head -n 20 file.txt       # first 20 lines
mkdir loot                # make a folder
touch notes.txt           # create an empty file
cp a.txt b.txt            # copy
mv a.txt archive/         # move (or rename)
rm file.txt               # delete (no recycle bin — be careful!)
nano notes.txt            # a simple text editor (Ctrl+O save, Ctrl+X exit)
```

## Getting help
```bash
man nmap            # the manual for a command (q to quit)
nmap --help         # quick options
which nmap          # where is this tool installed?
```
When a tool confuses you, `man <tool>` or `<tool> --help` is the first move — not a web search.

## Permissions — the thing beginners trip on
Every file has an **owner**, a **group**, and permission bits for **read (r), write (w), execute (x)**. `ls -la` shows them:
```
-rwxr-xr--  1 kali kali  1234 Jul 13 10:00 script.sh
```
- First block `rwx` = the **owner** can read/write/execute.
- Next `r-x` = the **group** can read/execute.
- Next `r--` = **everyone else** can only read.

**Make a script runnable** (you'll do this constantly):
```bash
chmod +x script.sh        # add "execute" permission
./script.sh               # run a script in the current folder
```
`sudo` runs a command as root when normal permissions aren't enough.

## Users & sudo
```bash
whoami                    # who am I?
sudo whoami               # -> root (borrow admin powers)
id                        # your user + groups
```
You'll see `sudo` before scans that need raw network access (nmap `-sS`, tcpdump). If a tool says "Permission denied" or "you must be root," add `sudo`.

## Processes — what's running
```bash
ps aux                    # every running process
top                       # live process viewer (q to quit); htop is nicer: sudo apt install htop
jobs                      # background jobs in this shell
kill <PID>                # stop a process by its ID
Ctrl+C                    # stop the command running in front of you
Ctrl+Z then bg            # pause it and send it to the background
```

## Installing tools — `apt`
Kali uses **apt** to install software from its repositories:
```bash
sudo apt update                 # refresh the list of available software
sudo apt install seclists       # install a package (here: extra wordlists)
apt search bloodhound           # find a package by name
```
Some tools come from **Python** (`pipx install <tool>`) or **GitHub** (`git clone <url>`) — later chapters show which.

## Networking peek (full detail in chapter 03)
```bash
ip a                      # your IP addresses and interfaces
ping 192.168.56.20        # is a host reachable? (Ctrl+C to stop)
```

## Redirecting output — save your work
```bash
nmap 192.168.56.20 > scan.txt        # save output to a file (overwrite)
nmap 192.168.56.20 >> scan.txt       # append to a file
nmap 192.168.56.20 | grep open       # send output INTO another command (a "pipe")
```
Pipes (`|`) are the heart of Linux power — chapter 02 goes deep.

## Common beginner mistakes
- **`rm` has no undo.** Double-check before deleting; never `rm -rf` a path you're unsure of.
- **Forgetting `./`** to run a local script — Linux won't search the current folder by default.
- **Fighting permissions instead of using `sudo`** (or vice-versa — not everything needs root).
- **Not using Tab completion** — it prevents typos and is much faster.

## ✅ Practice task
1. Make a folder `~/lab/scans`, `cd` into it.
2. Run `ip a` and save your Kali IP to a file: `ip a > myip.txt`, then `cat myip.txt`.
3. Create `hello.sh` containing `echo "hello from kali"`, make it executable, and run it.
4. Use `man ls`, find what `-t` does, then run `ls -lat`.

## Next
➡️ [02 — Terminal power](02-terminal-power.md): pipes, grep/find, tmux, and tiny scripts that turn commands into workflows.

## Sources
- The Linux Command Line (free): https://linuxcommand.org/tlcl.php
- Kali Docs: https://www.kali.org/docs/
- `man` pages — built into Kali: run `man man`
