# 15 — Notes & Reporting

> **What you'll learn:** why note-taking is the skill that separates hobbyists from professionals, how to lay out a clean engagement folder, how to log everything you type, and how to turn raw scan output into a professional **finding** and a full **pentest report**.
> **Prerequisites:** [14 — Post-exploitation & pivoting](14-post-exploitation-pivoting.md). ⬅️ [Course index](README.md)

Beginners skip this chapter. Professionals obsess over it. A pentest isn't judged by how many machines you popped — it's judged by the **report** you hand over. The client never watches you work; they only read what you wrote. This chapter is the bridge from "I hacked something" to "I can prove it, explain it, and tell you how to fix it."

---

## Why notes matter

**You cannot report what you didn't record.** Three days into an engagement, you *will not* remember which command dumped that password, what the exact URL was, or which host had port 8080 open. If it isn't written down, it didn't happen — and an unproven finding is worthless.

Good notes also protect *you*. If a client says "your test crashed our database," your timestamped log showing exactly what you ran (and when) is your defence. Notes are evidence, memory, and legal cover all at once.

The rule: **write it down as you go, not at the end.** Reconstructing a day of work from memory is where findings get lost.

## A clean engagement folder

Start every engagement with the same folder skeleton so you never wonder "where did I put that?" Create it before you run a single tool:

```bash
mkdir -p ~/engagements/acme-2026/{scans,loot,notes,screenshots,exploits,report}
cd ~/engagements/acme-2026
```

| Folder | What goes in it |
|---|---|
| `scans/` | Raw tool output — nmap, nikto, gobuster, everything (never edit these) |
| `loot/` | Stuff you pulled off targets: password hashes, config files, dumped databases |
| `notes/` | Your running Markdown log — the story of the engagement |
| `screenshots/` | Proof images (a shell prompt, an admin panel, a decrypted secret) |
| `exploits/` | Scripts and payloads you wrote or downloaded for this job |
| `report/` | The deliverable(s) you'll actually send |

**Keep `loot/` out of git.** Password hashes and captured traffic must never land in a public (or even private) repo by accident. This course's [`.gitignore`](../../../.gitignore) already ignores the dangerous folders — mirror that habit in your own engagement repos:

```gitignore
# never commit stolen data or secrets
loot/
captures/
*.pcap
*.pcapng
hashes.txt
cracked.txt
*.key
*.pem
```

> If it contains a target's data or a credential, it is **loot** and it stays git-ignored. When in doubt, ignore it.

## tmux as a workflow, not just a terminal

**tmux** ("terminal multiplexer", introduced in [02 — Terminal power](02-terminal-power.md)) lets one terminal window hold many sessions that keep running even if you disconnect. For reporting, its killer feature is **structure**: give each phase of the engagement its own window.

```bash
tmux new -s acme          # start a named session for this engagement
# Ctrl+b c   -> create a new window
# Ctrl+b ,   -> rename the current window (recon / scan / exploit / loot)
# Ctrl+b n   -> next window,  Ctrl+b p -> previous
# Ctrl+b d   -> detach (leave everything running); reattach later:
tmux attach -t acme
```

A tidy layout: window 0 = **recon**, 1 = **scanning**, 2 = **exploitation**, 3 = **notes** (an open editor). You can glance back at any phase instead of scrolling one giant history.

### Log every keystroke

Two ways to capture a full transcript of a pane so you never lose output:

```bash
# Option A — tmux's built-in pipe (saves the current pane live):
# Ctrl+b :  then type:  pipe-pane -o "cat >> ~/engagements/acme-2026/notes/tmux-$(date +%F).log"

# Option B — script(1): records EVERYTHING in the shell to a file (works anywhere):
script -a ~/engagements/acme-2026/notes/session-$(date +%F).log
# ...do your work...
exit                       # stops recording
```

`script` writes both what you typed and what the tools printed. Start it at the beginning of a work session and you have a complete, timestamped record for free.

## Always `nmap -oA`

Your scans are the backbone of the report, so save them in a format you can re-read later. Nmap's `-oA` ("output all") writes **three files at once** from a single scan — no re-scanning, no lost data:

```bash
nmap -sV -sC -oA scans/tcp-192.168.56.20 192.168.56.20
#            ^^^ base name; produces:
#   scans/tcp-192.168.56.20.nmap  -> human-readable (paste into notes)
#   scans/tcp-192.168.56.20.gnmap -> "grepable" (grep for open ports fast)
#   scans/tcp-192.168.56.20.xml   -> machine-readable (imports into Faraday/Dradis/Metasploit)
```

Make `-oA` a reflex on **every** nmap run. The `.xml` especially is what team tools ingest to build the report for you. The same idea applies to other tools — always redirect output into `scans/` (`nikto -h http://target | tee scans/nikto-target.txt`); `tee` prints to screen *and* saves to a file.

## Note-taking tools

There's no single right tool — the right one is the one you'll actually use. Pick from:

| Tool | What it is | Best for |
|---|---|---|
| **Plain Markdown** | `.md` text files (like this course) in your `notes/` folder | Simplicity, git-friendly, works everywhere — start here |
| **Obsidian** | Markdown editor with backlinks and a graph view | Linking hosts ↔ creds ↔ findings across a big engagement |
| **CherryTree** | Hierarchical notebook (a tree of rich-text nodes), pre-installed on Kali | Per-host node trees, embedding screenshots inline |

Plain Markdown is the honest recommendation for a beginner: it's future-proof, diffs cleanly in git, and forces you to write structured text. A minimal `notes/log.md` might just be a running table (mirror the **lab-log tables** at the bottom of every course [module](../modules/) — that habit scales straight into real engagements):

```markdown
| Time  | Host           | Command                        | Result                          |
|-------|----------------|--------------------------------|---------------------------------|
| 10:14 | 192.168.56.20  | nmap -sV -oA scans/msf2 ...    | 21/ftp vsftpd 2.3.4, 445/smb    |
| 10:31 | 192.168.56.20  | searchsploit vsftpd 2.3.4      | CVE-2011-2523 backdoor -> shell |
```

### Screenshots — Flameshot

A screenshot of a root shell or an admin panel is your strongest evidence. **Flameshot** is the go-to on Kali because it lets you annotate (arrows, boxes, blur) before saving:

```bash
sudo apt install flameshot     # if not already present
flameshot gui                  # select a region, annotate, save to screenshots/
```

Name shots so they explain themselves: `screenshots/56.20-root-shell.png`, not `Screenshot_2026-07-13.png`. **Blur any real secret** you don't need to show. Capture proof the moment you get it — that shell may not survive a reboot.

## How to write a finding

A **finding** is one vulnerability, written up so anyone — a sysadmin *or* a CFO — can understand what's wrong and what to do. Every good finding answers six things in the same order:

| Section | Answers | Example |
|---|---|---|
| **Title** | What is it, in one line? | "Anonymous FTP with backdoor command execution (vsftpd 2.3.4)" |
| **Severity (CVSS)** | How bad, on a standard scale? | Critical — CVSS 9.8 (see [Module 05](../modules/05-vulnerability-analysis/)) |
| **Affected asset** | Where exactly? | `192.168.56.20:21` (Metasploitable2) |
| **Evidence** | Prove it: command + output | The exact command you ran and what came back |
| **Impact** | So what? Why should they care? | Full remote root shell → total system compromise |
| **Remediation** | How do they fix it? | Upgrade vsftpd; block FTP at the perimeter |

**Severity** uses **CVSS** (Common Vulnerability Scoring System, a 0.0–10.0 score maintained by FIRST — the full metric groups and severity bands are covered in [Module 05](../modules/05-vulnerability-analysis/)). Don't invent numbers: look the CVE up on the [NVD](https://nvd.nist.gov/) and cite its score and vector.

A copy-paste template for `notes/findings.md`:

```markdown
### Finding: Anonymous FTP backdoor command execution (vsftpd 2.3.4)

- **Severity:** Critical — CVSS 9.8 (CVE-2011-2523)
- **Affected asset:** 192.168.56.20, TCP/21 (vsftpd 2.3.4)
- **Evidence:**
    $ nmap -p21 -sV 192.168.56.20
    21/tcp open  ftp  vsftpd 2.3.4
    $ use exploit/unix/ftp/vsftpd_234_backdoor   # metasploit -> root shell
    uid=0(root) gid=0(root)
  (see screenshots/56.20-root-shell.png)
- **Impact:** Any remote attacker gains an unauthenticated ROOT shell, giving
  full control of the host and any data or credentials it holds.
- **Remediation:** Remove/upgrade the backdoored vsftpd build to a current
  patched version; restrict FTP exposure; monitor for the `:)` trigger.
```

The evidence is what makes it a *finding* and not an opinion — the command and its output let the client reproduce it. This is exactly the standardisation flow ([CVE → CVSS → CWE → CPE](../modules/05-vulnerability-analysis/)) that Module 05 drills.

## The structure of a pentest report

Individual findings are the ingredients; the **report** is the meal. A standard professional report has five parts:

| Section | Audience | Contents |
|---|---|---|
| **Executive summary** | Managers, non-technical | Plain-English risk picture, a few sentences, a severity count — no jargon |
| **Scope** | Everyone (legal record) | What you were allowed to test (IPs, URLs, dates, rules of engagement) |
| **Methodology** | Technical reviewers | How you tested — the phases (recon → scan → exploit) and standards followed |
| **Findings** | Sysadmins, engineers | Every finding in the six-part format above, ordered by severity |
| **Appendix** | Technical / auditors | Full tool output, raw scan files, extra evidence, references |

The **executive summary** is written *last* but read *first* — and it's the only page many decision-makers open. Lead with risk and business impact, not tools. The **scope** section is your contract: testing anything outside it is illegal, so it's stated in writing. Order findings **highest severity first** — nobody reads to the bottom.

## Team tools

On a real team, several testers hit the same target and their findings must merge into one report. Two open tools handle this:

| Tool | What it does |
|---|---|
| **Faraday** | Multi-user collaboration platform; imports nmap/nikto/etc. output (that `.xml`!) and de-duplicates findings across a team |
| **Dradis** | Collaboration + reporting framework; templated findings and one-click export to a formatted report |

Both ingest the machine-readable output you already saved (this is why `-oA` matters). You stay in the tool for a solo lab, but knowing they exist — and feeding them clean, structured output — is what makes you employable on a team.

## Common beginner mistakes

- **Taking notes "later."** Later never comes; you forget the command. Log as you go with `script` or `tee`.
- **No proof.** A finding without command output or a screenshot is just a claim — and claims don't make it into reports.
- **Committing loot to git.** Hashes, pcaps, and dumped data must live in git-ignored folders. One careless `git add .` can leak a client's data.
- **Only saving the pretty nmap output.** Use `-oA` so you also keep the `.xml` that tools import — re-scanning later wastes time and changes results.
- **Writing the report like a hacker, not for the reader.** The exec summary is for managers; drop the jargon and lead with business risk.
- **Inventing severity.** Cite the real CVSS from the NVD; don't guess a number.

## ✅ Practice task

1. Create an engagement folder: `mkdir -p ~/engagements/lab-2026/{scans,loot,notes,screenshots,report}`.
2. Start a `tmux` session named `lab`, and inside it start `script ~/engagements/lab-2026/notes/session.log`.
3. Run `nmap -sV -sC -oA ~/engagements/lab-2026/scans/msf2 192.168.56.20` and confirm all **three** output files exist (`ls scans/`).
4. Take a screenshot of the nmap results with `flameshot gui`, annotate one open port, and save it to `screenshots/`.
5. In `notes/findings.md`, write up **one** vulnerability using the six-part template (Title → Severity → Asset → Evidence → Impact → Remediation). Look up its real CVSS on the [NVD](https://nvd.nist.gov/).
6. Fill in a lab-log row like the tables at the bottom of every [module](../modules/) — make it a habit that carries into real work.

## Next

➡️ [Appendix — Troubleshooting](appendix-troubleshooting.md): the common beginner errors across every chapter and how to fix them fast.

## Sources
- tmux — GitHub wiki & manual: https://github.com/tmux/tmux/wiki
- `script(1)` manual (session logging): https://man7.org/linux/man-pages/man1/script.1.html
- Nmap — Output formats (`-oA`): https://nmap.org/book/output.html
- Obsidian: https://obsidian.md/ · CherryTree: https://www.giuspen.net/cherrytree/ · Flameshot: https://flameshot.org/
- Faraday: https://faradaysec.com/ · Dradis: https://dradisframework.com/
- FIRST — CVSS specification: https://www.first.org/cvss/
- NIST — National Vulnerability Database (NVD): https://nvd.nist.gov/
- PTES — Penetration Testing Execution Standard (reporting): http://www.pentest-standard.org/
- Related: [Module 05 — Vulnerability Analysis](../modules/05-vulnerability-analysis/)
