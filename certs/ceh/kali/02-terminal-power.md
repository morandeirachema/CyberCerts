# 02 — Terminal Power

> **What you'll learn:** how the bash shell really works, how to connect commands with pipes and redirection, search text with `grep` (plus basic regular expressions), slice output with `cut`/`sort`/`uniq`/`wc`, keep long scans alive with **tmux**, and write your first bash script — turning single commands into repeatable workflows.
> **Prerequisites:** [01 — Linux essentials](01-linux-essentials.md). ⬅️ [Course index](README.md)

Chapter 01 taught you to *run* commands one at a time; this chapter teaches you to *combine* them. That is the whole difference between a beginner who types a command, reads the screen, and types the next — and a pro who builds a scan-parse-filter-report pipeline in a single line. We ramp from basics to mastery, so take the sections in order.

---

## The shell — what actually happens when you type

The **shell** is the program that reads what you type, runs it, and shows the result. Kali's default shell is **bash** (short for "Bourne Again SHell"). Almost every command follows the same shape:

```bash
command   options      arguments
nmap      -sV          192.168.56.20
```

- **command** — the tool to run (`nmap`).
- **options** (also called **flags**) — switches that change behaviour, usually starting with `-` or `--` (`-sV` = "detect service versions").
- **arguments** — what the command acts on (here, the target IP).

The **prompt** is the shell telling you it is ready — on Kali it looks like `┌──(kali㉿kali)-[~]` then `└─$`. That trailing `$` means you are a normal user; a `#` means you are **root** — a quick "am I about to run this as admin?" safety check. When you press Enter, bash splits your line into words, expands any special characters (wildcards, variables — both covered below), finds the program, and runs it.

---

## Redirection — deciding where output goes

Every command has three standard "streams":

| Stream | Name | Number | Default destination |
|---|---|---|---|
| Input | **stdin** | `0` | Your keyboard |
| Normal output | **stdout** | `1` | Your screen |
| Error messages | **stderr** | `2` | Your screen |

**Redirection** sends a stream somewhere else — usually a file. This is how you save scan results instead of watching them scroll away.

```bash
nmap 192.168.56.20 > scan.txt        # send stdout to a file (OVERWRITES it)
nmap 192.168.56.30 >> scan.txt       # APPEND to the file instead of overwriting
nmap 192.168.56.20 2> errors.txt     # send only errors (stderr) to a file
nmap 192.168.56.20 &> all.txt        # send BOTH stdout and stderr to one file
nmap 192.168.56.20 2>/dev/null       # throw errors away (/dev/null = the trash can)
```

> `>` clobbers the file — if `scan.txt` already had data, it is gone; use `>>` to keep adding. `/dev/null` is a special "black hole" file; anything sent there disappears, handy for silencing noisy errors. You should see nothing on screen when you redirect stdout to a file — that is correct. Read it back with `cat scan.txt`.

---

## Pipes — connecting commands into a chain

A **pipe**, written `|`, feeds the *output* of one command straight into the *input* of the next, without a temporary file. It is the single most important idea in the terminal.

```bash
nmap 192.168.56.20 | grep open      # nmap's output goes INTO grep, which keeps only "open" lines
cat scan.txt | wc -l                # feed the file into wc to count its lines
```

Read a pipeline left to right as "do this, then hand it to that, then to that": `nmap ... | grep open | cut -d/ -f1 | sort -n` scans, keeps the open lines, extracts the port numbers, and sorts them. Each stage does one small job; the pipe glues them. We build exactly this pipeline for real at the end of the chapter.

---

## Wildcards (globbing) — matching many files at once

Before bash runs a command, it expands **wildcards** (also called **globbing**) into matching filenames. This lets one command act on many files.

| Pattern | Matches |
|---|---|
| `*` | Any number of characters (`*.txt` = every file ending in `.txt`) |
| `?` | Exactly one character (`scan?.txt` = `scan1.txt`, `scanA.txt`) |
| `[abc]` | One character from the set (`host[123].txt`) |
| `[0-9]` | One character in a range (any single digit) |

```bash
ls *.txt                    # list every .txt file in this folder
cat scan-*.txt              # print every file starting "scan-"
rm host[0-9].txt            # delete host0.txt ... host9.txt — check with ls first!
```

> The **shell**, not the command, expands `*` — so `ls *.txt` never sees the `*`, only the real filenames. If nothing matches, bash passes the literal `*.txt` through, which can surprise you, so always test a risky pattern with `ls` before `rm`.

---

## `grep` — finding text (your everyday power tool)

**`grep`** searches text for lines that match a pattern and prints them. You will use it constantly to pull the interesting lines out of huge tool output.

```bash
grep open scan.txt          # lines containing "open"
grep -i error log.txt       # -i = case-insensitive (matches Error, ERROR, error)
grep -v closed scan.txt     # -v = invert: lines WITHOUT "closed"
grep -n root /etc/passwd    # -n = show line numbers
grep -c open scan.txt       # -c = just count matching lines
grep -r "password" .        # -r = search every file under this folder (recursive)
grep -oE '[0-9]+/(tcp|udp)' scan.txt   # -o = print only the match (e.g. 22/tcp), not the whole line
```

### Regular expressions — patterns, not just words

A **regular expression** (**regex**) is a mini-language for describing text patterns. `grep -E` turns on "extended" regex; `grep -P` turns on richer "Perl" regex (needed for `\d`).

| Symbol | Means |
|---|---|
| `.` | Any single character |
| `*` | Zero or more of the thing before it |
| `+` | One or more (needs `-E`) |
| `^` | Start of the line |
| `$` | End of the line |
| `[0-9]` | Any one digit |
| `\d` | A digit (needs `-P`) |
| `a|b` | `a` **or** `b` (needs `-E`) |

```bash
grep -E '^22/tcp' scan.txt                       # lines that START with 22/tcp
grep -E 'open|filtered' scan.txt                 # lines with "open" OR "filtered"
grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' scan.txt  # pull out every IPv4 address
```

That last one reads: "one-to-three digits then a dot, three times, then one-to-three digits." Extracting IPs from messy output is a task you will repeat forever — this is the pattern to remember.

---

## `find` — locating files across the system

Where `grep` searches *inside* files, **`find`** searches *for* files by name, type, size, or age.

```bash
find /usr/share/wordlists -name "*.txt"    # every .txt under the wordlists folder
find . -type f -name "scan*"               # files (not folders) starting "scan"
find / -perm -4000 -type f 2>/dev/null     # SUID binaries — a classic privesc hunt
find ~ -mmin -10                           # files in your home changed in the last 10 minutes
```

> `-type f` = files, `-type d` = directories. That `2>/dev/null` silences the "Permission denied" noise you get when searching the whole system as a normal user.

---

## Slicing output — `cut`, `sort`, `uniq`, `wc`

These four small tools reshape text. Combined with pipes, they turn raw output into clean data.

```bash
cut -d/ -f1 ports.txt       # cut each line on "/" (-d = delimiter), keep field 1 (-f1)
sort scan.txt               # sort lines alphabetically
sort -n ports.txt           # -n = numeric sort (so 9 comes before 80, not after)
sort -u hosts.txt           # sort AND drop duplicates
uniq -c sorted.txt          # collapse repeats, -c prefixes each with its count
wc -l scan.txt              # -l = count lines (also -w words, -c bytes)
```

A classic combo — "count how many times each value appears, most common first":

```bash
sort ips.txt | uniq -c | sort -rn        # -r = reverse (biggest first), -n = numeric
```

> `uniq` only removes **adjacent** duplicates, so you almost always `sort` first. That `sort | uniq -c | sort -rn` idiom is worth memorising — it answers "what shows up most?" for logs, IPs, ports, anything.

---

## A gentle look at `awk` and `sed`

**`awk`** and **`sed`** are whole languages, but you only need a little to be dangerous.

**`awk`** splits each line into fields (columns) and prints the ones you want. `$1` is the first column, `$2` the second, and so on:

```bash
awk '{print $1, $3}' scan.txt          # print the first and third columns of every line
awk '/open/ {print $1}' scan.txt       # only lines matching "open", print column 1
awk -F: '{print $1}' /etc/passwd       # -F: sets ":" as the field separator -> usernames
```

**`sed`** edits a stream of text — most commonly find-and-replace with `s/old/new/`:

```bash
sed 's/open/OPEN/' scan.txt            # replace first "open" per line with "OPEN"
sed 's/open/OPEN/g' scan.txt           # g = global: every match on the line
sed -n '1,5p' scan.txt                 # print only lines 1 to 5
```

> Neither command changes the original file unless you tell it to (`sed -i` edits in place). They print to the screen, so you can safely experiment.

---

## Command history and shortcuts — stop retyping

Bash remembers everything you type. This saves enormous time.

```bash
history                     # numbered list of past commands
history | grep nmap         # find that nmap command you ran earlier
!!                          # re-run the PREVIOUS command
sudo !!                     # re-run the previous command WITH sudo (huge when you forgot it)
!143                        # re-run command number 143 from history
!nmap                       # re-run the last command that started with "nmap"
```

Live editing shortcuts on the prompt:

| Keys | Action |
|---|---|
| **↑ / ↓** | Step back/forward through history |
| **Ctrl-R** | Reverse-search history — type a few letters, Enter to run |
| **Ctrl-A / Ctrl-E** | Jump to start / end of the line |
| **Ctrl-C** | Cancel the current line (or stop a running command) |
| **Ctrl-L** | Clear the screen (same as `clear`) |

> `sudo !!` is the one everyone falls in love with: a command fails with "Permission denied," you type `sudo !!`, done — no retyping.

---

## Aliases and `~/.bashrc` — make the shell yours

An **alias** is a short nickname for a longer command. `~/.bashrc` is a script bash runs every time it opens a new shell — the place to keep your aliases and settings permanently.

```bash
alias ll='ls -lah'          # define an alias for THIS session only
alias ports="grep open"     # now: cat scan.txt | ports
```

To make aliases stick, add them to `~/.bashrc`:

```bash
echo "alias ll='ls -lah'" >> ~/.bashrc   # append the alias to your config
source ~/.bashrc                          # reload it into the current shell (or open a new terminal)
```

> `source` (or its shorthand `.`) re-runs the file *in your current shell* so changes apply immediately, without opening a new terminal. Keep your engagement aliases here and every new terminal is ready to go.

---

## tmux — never lose a long scan again

**tmux** ("terminal multiplexer") lets one terminal hold many **sessions**, each with multiple **windows** (like browser tabs) and **panes** (splits within a window). The killer feature: you can **detach** from a session, close the terminal or drop your SSH connection, and everything *keeps running*. Reattach later and it is exactly as you left it — vital when a scan takes an hour.

- **Session** = a whole workspace (e.g. one per target or engagement).
- **Window** = a tab inside a session.
- **Pane** = a split within a window (run a scan on the left, take notes on the right).

Every tmux shortcut starts with the **prefix**, `Ctrl-b`: press and release `Ctrl-b`, *then* the next key.

```bash
tmux                        # start tmux
tmux new -s recon           # start a NAMED session called "recon"
```

| Keys | Action |
|---|---|
| `Ctrl-b` then `c` | Create a new window |
| `Ctrl-b` then `n` / `p` | Next / previous window |
| `Ctrl-b` then `"` | Split into two panes, stacked (one above the other) |
| `Ctrl-b` then `%` | Split into two panes, side by side |
| `Ctrl-b` then arrow key | Move between panes |
| `Ctrl-b` then `d` | **Detach** — leave the session running in the background |

```bash
tmux ls                     # list running sessions
tmux a                      # attach to the last session
tmux a -t recon             # attach to the session named "recon"
```

You should see, after `tmux ls`, a line like `recon: 1 windows (created ...)`. Kick off a long scan, press `Ctrl-b d`, close the window, come back tomorrow, `tmux a` — the scan is either finished or still running. Chapter [15 — Notes & reporting](15-notes-and-reporting.md) builds a full engagement layout on this.

---

## Your first bash script

A **script** is a file of commands bash runs top to bottom. Three ingredients:

1. A **shebang** — the first line `#!/bin/bash` tells the system which interpreter to use.
2. **Variables** — store a value once, reuse it: set with `name=value` (no spaces), read with `$name`.
3. A **loop** — repeat an action over a list.

Create `sweep.sh` (with `nano sweep.sh`):

```bash
#!/bin/bash
# sweep.sh — ping-sweep the lab and report which hosts are alive
network="192.168.56"                     # a variable holding the network prefix

for host in 10 20 30 31; do              # loop over the last octet of each lab host
    ip="$network.$host"                  # build the full IP, e.g. 192.168.56.20
    if ping -c1 -W1 "$ip" &>/dev/null; then   # -c1 = one packet, -W1 = 1s timeout, hide output
        echo "[+] $ip is UP"
    fi
done
```

Make it executable and run it (see chapter 01 on `chmod`):

```bash
chmod +x sweep.sh           # add execute permission
./sweep.sh                  # run it (the ./ means "in this folder")
```

You should see a line like `[+] 192.168.56.20 is UP` for each host that replies. You just automated something that would be tedious by hand — the essence of terminal power.

You can loop over **ports** the same way, using `nc` (netcat) to test each one:

```bash
for port in 21 22 80 445 3389; do        # loop over a list of ports
    nc -z -w1 192.168.56.20 "$port" 2>/dev/null && echo "port $port open"
done
```

> `-z` just checks the port (sends no data), `-w1` waits at most 1 second, and `&&` runs the `echo` **only if** the check succeeded. Fine for learning — but for real port scanning use `nmap` (chapter 05), which is far faster and smarter.

---

## Putting it together — parsing a real nmap scan

Here is a complete beginner-to-pro workflow: scan a target, save it, then use everything above to pull out exactly what you need.

```bash
# 1. Scan Metasploitable2 and save the human-readable output to a file
nmap -sV 192.168.56.20 -oN scan.txt      # -oN = "normal" output to scan.txt

# 2. See just the open ports
grep open scan.txt
```

You should see lines like:

```
22/tcp   open  ssh     OpenSSH 4.7p1 Debian 8ubuntu1
80/tcp   open  http    Apache httpd 2.2.8 ((Ubuntu) DAV/2)
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X
```

Now refine with pipes:

```bash
grep open scan.txt | wc -l                    # HOW MANY open ports?
grep open scan.txt | cut -d/ -f1              # just the port NUMBERS (cut on "/")
grep open scan.txt | awk '{print $1, $3}'     # port and service name, side by side
grep open scan.txt | cut -d/ -f1 | sort -n | paste -sd,   # a comma-list: 22,80,445
```

That last line is a genuine pro move: `paste -sd,` joins the sorted ports into `22,80,445`, which you can hand straight to the next tool. Build the pipeline one stage at a time — add a `|`, check the output, add the next — and you can shape any tool's output into whatever the next tool needs.

---

## Common beginner mistakes
- **`>` overwrites without warning.** It silently wipes the file. Use `>>` to append when you mean to add.
- **Forgetting `sort` before `uniq`.** `uniq` only removes *adjacent* duplicates, so `sort | uniq` (or `sort -u`) is almost always what you want.
- **Spaces around `=` in a variable.** `name = value` fails; it must be `name=value`. And read it back as `$name`.
- **Mixing up `grep` and `find`.** `grep` searches *inside* files for text; `find` searches *for* files by name/type. Reach for the right one.
- **Quoting.** Wrap variables in double quotes (`"$ip"`) so paths or values with spaces don't break the command.
- **Losing a long scan** because you closed the terminal — run it inside **tmux** and detach instead.

## ✅ Practice task
1. Scan Metasploitable2 and save it: `nmap -sV 192.168.56.20 -oN ~/lab/scans/meta.txt`.
2. From that file, print **only the open ports' numbers**, sorted numerically (hint: `grep`, `cut -d/ -f1`, `sort -n`).
3. Count how many services are open with a single pipeline ending in `wc -l`.
4. Add `alias openports='grep open'` to `~/.bashrc`, `source` it, then run `cat ~/lab/scans/meta.txt | openports`.
5. Start `tmux new -s practice`, run a long scan (`nmap -p- 192.168.56.20`), detach with `Ctrl-b d`, list sessions with `tmux ls`, and reattach with `tmux a`.
6. Write and run a `sweep.sh` that ping-sweeps `192.168.56.10`, `.20`, `.30`, and `.31` and prints which are UP.

## Next
➡️ [03 — Networking basics](03-networking-basics.md): IP addresses, ports, protocols, and DNS — the language every tool in this course speaks.

## Sources
- GNU Bash Reference Manual: https://www.gnu.org/software/bash/manual/
- GNU Grep Manual: https://www.gnu.org/software/grep/manual/
- tmux — official wiki & manual: https://github.com/tmux/tmux/wiki
- The Linux Command Line (free book, W. Shotts): https://linuxcommand.org/tlcl.php
- Kali Docs: https://www.kali.org/docs/
