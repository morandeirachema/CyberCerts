# Module 09 — Social Engineering · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab against **your own** environment only (the AD + mail lab in [`../../labs/`](../../labs/README.md) — see [`../../labs/topology.md`](../../labs/topology.md)). Each step gives the action, what you should observe, a hint, and the defender/PAM takeaway. Outputs shown are **representative** — yours will differ.

> ⚠️ **AUTHORIZED SIMULATION ONLY.** Every step below targets **lab accounts you created** (`alice@ceh.lab`, `bob@ceh.lab`) on **your own** mail/AD lab, or **your own** test inbox. Sending a phish, cloning a login page, spoofing a header, or pretexting a **real** person or third-party org — even "to prove a point" — is fraud/unauthorized access and is illegal and unethical **without written authorization, defined scope, and consenting recipients**. If a recipient did not consent and isn't yours, **do not send it.** Full stop.

**Goal:** run a phishing simulation end-to-end, harvest a lab credential, dissect a spoofed email — then *watch PAM controls turn each win into a loss.*

**Targets:** Kali `192.168.56.10` · Windows DC `192.168.56.30` (`ceh.lab`) · lab SMTP + your two test users `alice@ceh.lab`, `bob@ceh.lab`.

**Prereqs:** lab is up (`labs/scripts/setup.sh`); a lab-only SMTP server; you created `alice`/`bob` as **disposable** users; you are on the isolated lab segment with **no route to the internet or home LAN**.

---

## Part A — Gophish phishing simulation (your own test inbox)

### A1. Stand up the Gophish campaign server
```bash
# on Kali, in the lab segment only
./gophish
```
**You should see** the admin UI and phish server bind locally:
```
Starting admin server at https://127.0.0.1:3333
Starting phishing server at http://0.0.0.0:80
```
**Observe:** everything is self-hosted — the admin console, the landing page, and the sending profile all live in *your* lab. Log in at `https://127.0.0.1:3333` with the printed initial credentials.

<details><summary>Hint if the UI won't load</summary>Gophish prints a one-time admin password to stdout on first run — scroll up. Accept the self-signed cert warning; it's your own lab cert. Confirm nothing else holds port 80 (`sudo ss -ltnp | grep :80`).</details>

**Defender/PAM view:** a phishing-simulation platform is exactly what a blue team uses for *authorized* awareness campaigns and click-rate metrics. Mapping lives in [`../../defender-pam/`](../../defender-pam/README.md).

### A2. Build the campaign — recipients are lab users ONLY
In the UI, create in order: **Sending Profile** (your lab SMTP) → **Email Template** ("IT password expiry") → **Landing Page** (a cloned login) → **Users & Groups** containing **only** `alice@ceh.lab` and `bob@ceh.lab` → **Campaign**, then launch.

**You should see** the campaign timeline begin recording events:
```
Email Sent      alice@ceh.lab
Email Opened    alice@ceh.lab
Clicked Link    alice@ceh.lab
```
**Observe:** the recipient list is your gate. If any address you don't own appears here, **stop** — the simulation is no longer authorized.

<details><summary>Hint: no "Email Sent"?</summary>Test the Sending Profile with the UI's "Send Test Email" button. If SMTP auth fails, re-check the lab mail server creds; if mail queues but never delivers, confirm `alice`/`bob` mailboxes exist on the lab server.</details>

**Defender/PAM view:** open/click telemetry is the same signal a mail gateway and a report-phish button surface in production — see the phishing row in [`../../defender-pam/`](../../defender-pam/README.md).

### A3. Capture the submitted credential, then apply the control
Log in as `alice` (your test user), click the link, and submit a **fake** password on the landing page. Watch Gophish record it:
```
Submitted Data  alice@ceh.lab   (username + password captured)
```
Now enable **FIDO2/WebAuthn** (or a TOTP step) on the test accounts and re-run the click.

**You should see** the harvest still succeed at the page, but the credential no longer grants access — the second factor blocks the login.

**Observe:** **the credential harvest always succeeds** (humans click). The attack only becomes a *loss* when the stolen secret is worthless.

<details><summary>Hint</summary>If you don't have WebAuthn wired to the lab app, simulate the control conceptually: the harvested password is *valid* but authentication now requires a hardware-bound factor the fake page can't relay.</details>

**Defender/PAM view:** [phishing-resistant MFA](../../defender-pam/README.md) makes A3's harvested password unusable; detection = impossible-travel logon right after credential entry. See [`../../defender-pam/detection-engineering.md`](../../defender-pam/detection-engineering.md).

---

## Part B — SET credential harvester (clone a page you own)

### B1. Clone your own lab login page
```bash
sudo setoolkit
#   1) Social-Engineering Attacks
#     2) Website Attack Vectors
#       3) Credential Harvester Attack Method
#         2) Site Cloner
#   -> clone the LAB login page you host (e.g. http://ceh.lab/login), post back to Kali
```
**You should see** SET stand up the harvester and clone the page:
```
[*] Cloning the website: http://ceh.lab/login
[*] The Social-Engineer Toolkit Credential Harvester Attack
[*] Credential Harvester is running on port 80
```
**Observe:** the clone is pixel-identical but the form posts to **your** Kali box. Only *you*, hitting it from a lab browser as the test user, will submit anything.

<details><summary>Hint: clone looks broken?</summary>Some pages pull assets from paths SET can't rewrite — that's fine for the concept. Confirm the harvester is listening (`sudo ss -ltnp | grep :80`) and browse to `http://192.168.56.10` from a lab host.</details>

**Defender/PAM view:** a cloned login is what phishing-resistant MFA neutralizes — origin-bound WebAuthn won't authenticate against the attacker's host even with the right password. See [`../../defender-pam/`](../../defender-pam/README.md).

### B2. Submit a lab credential and read the capture
From a lab browser, as your test user, submit a **fake** credential on the clone.

**You should see** SET print the captured POST:
```
PARAM: username=alice
POSSIBLE PASSWORD FIELD FOUND: password=NotMyRealPass!
[*] WHEN YOU'RE FINISHED, HIT CONTROL-C
```
**Observe:** a static password is captured in plaintext the instant it's typed — this is *why* the secret must not be the only thing standing between an attacker and the account.

**Defender/PAM view:** with **JIT** the harvested account holds no durable privilege; with **least privilege** a phished `alice` reaches almost nothing. See [`../../defender-pam/identity-attack-paths.md`](../../defender-pam/identity-attack-paths.md).

---

## Part C — Spoofed email & header analysis

### C1. Inspect the headers of a spoofed lab message
Take a message you sent *within the lab* with a forged `From:` (or the Gophish send), and read its full headers.
```bash
# view the raw headers of a saved lab message
cat ~/lab-mail/phish.eml | grep -Ei 'From:|Return-Path:|Received:|Authentication-Results|spf=|dkim=|dmarc='
```
**You should see** the sender fields disagree and authentication fail:
```
From: "IT Support" <it-support@ceh.lab>
Return-Path: <bounce@attacker.lab>
Authentication-Results: mx.ceh.lab; spf=fail dkim=fail dmarc=fail
```
**Observe:** the friendly `From:` lies, but `Return-Path`, the `Received:` chain, and **spf/dkim/dmarc=fail** expose the spoof. This is exactly the tell a mail gateway acts on.

<details><summary>Hint: all results say "none"?</summary>`none` (not `pass`/`fail`) means the *sending* domain published no SPF/DKIM/DMARC records. Publish records for `ceh.lab` in the lab DNS, then re-send to see `fail` on a spoof and `pass` on a legitimate message.</details>

**Defender/PAM view:** **SPF + DKIM + DMARC** with a reject policy is the direct control against exact-domain spoofing used in **BEC/whaling** — see the phishing/BEC mapping in [`../../defender-pam/`](../../defender-pam/README.md).

### C2. Help-desk vishing drill (privileged reset refusal)
Script a **vishing** call against **your own** lab help-desk runbook: as `alice`, phone the "help desk" and pressure them to reset a **privileged** account password — no ticket, urgent tone.

**You should see** the runbook **refuse** without out-of-band proof:
```
> Reset requires: verified callback to number on file + secondary factor + manager approval.
> Request DENIED — no ticket, identity not proven.
```
**Observe:** the pretext (urgency + authority) is powerful, but a **proof bar it can't satisfy** stops it cold. The help desk is a top target precisely because it can hand over Tier 0.

**Defender/PAM view:** treat **privileged resets** as high-assurance events — callback, secondary factor, approval, PAM-brokered break-glass with logging. See [`../../defender-pam/cyberark-attack-mapping.md`](../../defender-pam/cyberark-attack-mapping.md).

---

## What you should conclude
The human "win" is nearly guaranteed — people click, submit, and trust. Each win only becomes a *loss* when a specific control removes the payoff:

| You did | The control that turns it into a loss |
|---|---|
| Gophish harvest of `alice`'s password | **Phishing-resistant MFA** — stolen password is worthless |
| SET clone captures a lab credential | **Origin-bound WebAuthn + JIT + least privilege** — nothing standing to abuse |
| Spoofed `From:` slips into the inbox | **SPF + DKIM + DMARC (reject)** — spoof fails auth and is dropped |
| Vishing for a privileged reset | **Out-of-band identity verification + approval** — pretext can't meet the proof bar |

## Cleanup
```bash
# stop the harvesters/servers
# (Ctrl-C the SET harvester and the Gophish process)
rm -f ~/lab-mail/phish.eml
# delete the Gophish campaign, sending profile, and the disposable alice/bob test users
# revert any MFA/DNS test records you added if you want to repeat from the weak state
```

## Record it
Log actions, outputs, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
