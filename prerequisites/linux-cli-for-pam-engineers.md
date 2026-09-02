# Linux CLI Deep Dive for PAM Engineers

Expert-level PAM (Privileged Access Management) administration explicitly requires
**GNU/Linux command-line** skills, because the expert tasks — troubleshooting, the REST
Application Programming Interface (API), proxy tuning, and high availability — happen at
the shell of the PAM appliance, not just in the web GUI. Whatever the vendor, the bastion
/ session proxy is a hardened Linux system, and the commands below are what you reach for
when the GUI cannot tell you *why* a session failed, a rotation stalled, or a node stopped
replicating. This page is a focused, transferable Linux-CLI study guide for that level.

> This page teaches the **portable Linux skills** you need. The **vendor-specific**
> commands, exact log paths, service names and CLI tools live in each product's
> administration guide — each section says what to look up there. New to Linux? Start
> with [Linux essentials for PAM](linux-essentials-for-pam.md).

## Learning objectives

- Get a shell on a Linux host/appliance and move around safely.
- Read and search logs, inspect services/processes/ports, and edit config files.
- Call a REST API and parse JavaScript Object Notation (JSON) from the shell.
- Recognise the operational commands behind expert-level PAM troubleshooting, REST API
  automation, and high-availability (HA) operations.

## How CLI skills map to PAM operational tasks

| CLI skill group | PAM operational task it unlocks |
|-----------------|---------------------------------|
| Navigate & read files | Finding config, certificates, and recordings on the appliance |
| Logs & text | Troubleshooting failed sessions, auth errors, proxy crashes |
| Services & ports | Checking proxy engines, database, API health; verifying listeners |
| Network & crypto | Diagnosing X.509 / Kerberos / LDAP / RADIUS integrations |
| REST from shell | Automating account, target and authorization management |
| Scripting & cron | Password-rotation schedules, batch onboarding, health checks |
| Services + logs | HA replication and disaster-recovery (DR) operations |

```mermaid
flowchart LR
    subgraph CLI["Linux CLI skill groups"]
        Nav["Navigate & read files<br/>ls · cd · less · find"]
        Logs["Logs & text<br/>tail · grep · awk · journalctl"]
        Svc["Services & ports<br/>systemctl · ps · ss"]
        Net["Network & crypto<br/>dig · ping · openssl · ssh-keygen"]
        Api["REST from shell<br/>curl · jq"]
        Auto["Scripting & cron<br/>bash · variables · schedules"]
    end
    Logs --> T1["Troubleshoot sessions<br/>& authentication"]
    Svc --> T1
    Net --> T2["Diagnose auth integrations<br/>(X.509 / Kerberos / LDAP)"]
    Api --> T3["Automate via REST API"]
    Auto --> T4["Password rotation<br/>& scheduled jobs"]
    Svc --> T5["HA & DR<br/>replication"]
```

## 1. Getting a shell

A PAM bastion is a hardened **Linux appliance** (usually Debian- or RHEL-based).
Expert-level work means connecting to it over **Secure Shell (SSH)** with the
administrative account you've been given, then working at the prompt.

```bash
ssh admin@bastion.example.com        # connect (use the account/port you were provided)
whoami                               # which user am I?
id                                   # my user id and groups
pwd                                  # where am I in the filesystem?
exit                                 # leave the session
```

> The exact administrative account, console behaviour, and management ports are
> appliance-specific — check the vendor's deployment guide, and see
> [PAM reference architecture](../certs/ceh/defender-pam/pam-architecture.md) for the
> generic component layout. Always prefer **read-only** inspection first, and take a
> snapshot before changes.

## 2. Navigate & read files

```bash
ls -lah /var/log            # list, long + human sizes + hidden
cd /var/log                 # change directory
less bigfile.log            # page through (q to quit, / to search, G end, g top)
cat file                    # dump small file
find / -name "*.conf" 2>/dev/null   # locate files by name (errors hidden)
stat file                   # size, owner, timestamps
```

File permissions matter for config and key files (covered in
[Linux essentials → permissions](linux-essentials-for-pam.md)): `chmod`, `chown`, and the
`rwx` triplets.

## 3. Logs & text processing — the heart of troubleshooting

Most troubleshooting is *reading logs fast*:

```bash
tail -f /var/log/app.log              # follow a log live (Ctrl-C to stop)
tail -n 200 app.log                   # last 200 lines
grep -i "error" app.log               # case-insensitive search
grep -ri "kerberos" /var/log/         # recursive search in a tree
zgrep "fail" app.log.1.gz             # search inside rotated/compressed logs
awk '{print $1, $9}' access.log       # pick columns
cut -d: -f1 /etc/passwd                # split on a delimiter
sort | uniq -c | sort -rn              # count & rank (e.g. top error lines)
journalctl -u <service> --since today # systemd journal for one unit
```

> **Which** logs and databases to read on a given appliance — exact paths and what each
> contains — are vendor-specific; find them in the product's administration guide. What
> to *look for* (failed sessions, authentication errors, anomalous privileged activity)
> is covered in
> [detection engineering](../certs/ceh/defender-pam/detection-engineering.md).

## 4. Services, processes & ports

```bash
systemctl status <service>            # is it running? recent log lines
systemctl restart <service>           # restart a unit (with care)
ps aux | grep <name>                  # find a running process
top    # or: htop                     # live CPU/memory view
ss -tlnp                              # listening TCP ports + owning process
ss -tn state established              # current connections
```

A PAM appliance's internal services (database, the RDP and SSH proxy engines, REST API,
schedulers, etc.) and their roles are documented per product; the generic component
layout is in [PAM reference architecture](../certs/ceh/defender-pam/pam-architecture.md).

## 5. Text editing config files

You'll need at least one terminal editor. **`vi`/`vim`** is everywhere:

```text
vi file.conf      open
  i               insert mode (type)
  Esc             back to command mode
  :w              save        :q  quit        :wq save+quit       :q!  quit no-save
  /text           search
```

`nano` is simpler if available (`Ctrl-O` save, `Ctrl-X` exit). **Back up before editing**:
`cp file.conf file.conf.bak`.

## 6. The REST API from the shell

PAM REST API automation is practiced with **`curl`** (make requests) and **`jq`** (read
JSON):

```bash
# generic shape — authenticate, then GET a resource, pretty-print the JSON
curl -s -k -H "X-Auth-Key: <api-key>" \
     https://bastion.example.com/api/<resource> | jq .

# common flags:  -s silent  -k skip TLS check (lab only)  -X method  -H header  -d body  -i show headers
```

> Each product's actual authentication headers, resources, methods and response codes
> are in its API reference — use those exact values, not the placeholder above.

## 7. Network & crypto helpers — advanced authentication

Diagnosing X.509, Kerberos, RADIUS and SAML problems is much easier from the shell:

```bash
ping host                     # reachability
dig host  # or: nslookup host # DNS resolution (matters for Kerberos!)
ss -tn                        # who am I connected to?
openssl s_client -connect host:443        # inspect a TLS service + its cert chain
openssl x509 -in cert.pem -noout -text     # decode a certificate (issuer, dates, SAN)
ssh-keygen -lf key.pub                      # fingerprint an SSH key
date                          # clock skew breaks Kerberos — check the time
```

Background on these protocols: [networking & protocols](networking-and-protocols.md) and
[cryptography & PKI](cryptography-and-pki.md); the wire-level mechanics are in
[../protocols/kerberos.md](../protocols/kerberos.md),
[../protocols/ldap.md](../protocols/ldap.md), [../protocols/radius.md](../protocols/radius.md)
and [../protocols/saml.md](../protocols/saml.md).

## 8. Scheduling & light scripting

```bash
# cron timing: minute hour day-of-month month day-of-week  (used for password-rotation schedules)
# example - run a job at 02:30 every day:
# 30 2 * * *  /path/to/job

# minimal bash:
for h in web db app; do echo "checking $h"; ssh "$h" uptime; done
command && echo OK || echo FAILED      # exit-code branching ($? holds the last code)
```

Password-rotation scheduling uses cron-style timing — see the vaulting and rotation
controls in [PAM playbook](../certs/ceh/defender-pam/pam-playbook.md). Application-launch
scripting on Windows targets (AutoIt-style automation) is not bash, but the same
automation mindset applies.

## 9. High availability / operations

HA replication (database replication between nodes, often over an SSH tunnel) and the
vendor's replication control tool are operated from the shell. Don't memorise invented
flags — the exact commands, modes and "what is/isn't replicated" are in the product's HA
guide; the design goals are in
[PAM reference architecture](../certs/ceh/defender-pam/pam-architecture.md). At the CLI
you'll mostly use `systemctl`, `ss`, log-reading, and the documented replication command.

## Quick-reference

| Task | Commands |
|------|----------|
| Move around | `ls -lah` · `cd` · `pwd` · `less` · `find` |
| Read logs | `tail -f` · `grep -ri` · `zgrep` · `journalctl -u` |
| Services/ports | `systemctl status` · `ps aux` · `ss -tlnp` |
| Edit config | `vi` / `nano` · back up with `cp` first |
| REST API | `curl -H` … `| jq .` |
| Network/crypto | `dig` · `openssl s_client` · `openssl x509` · `date` |
| Automate | `cron` timing · `for` loops · `&&` / `||` / `$?` |

## Safety first

You're often on a **production security appliance**. Inspect read-only before you change
anything, snapshot/back up first, avoid destructive commands (`rm -rf`, redirection over
files) unless you're certain, and only act within your **authorised** scope.

## Sources

- Linux command behaviour: standard GNU coreutils / `man` pages and
  [Linux essentials for PAM](linux-essentials-for-pam.md).
- PAM reference architecture and control set: this repo's
  [pam-architecture.md](../certs/ceh/defender-pam/pam-architecture.md) and
  [pam-playbook.md](../certs/ceh/defender-pam/pam-playbook.md).
- OpenSSL `s_client` / `x509` manual pages: https://docs.openssl.org/master/man1/openssl-s_client/
- `curl` manual: https://curl.se/docs/manpage.html · `jq` manual: https://jqlang.github.io/jq/manual/
