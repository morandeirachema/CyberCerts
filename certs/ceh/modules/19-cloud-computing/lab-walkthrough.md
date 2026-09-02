# Module 19 — Cloud Computing · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab. Outputs shown are **representative** — yours will differ. Each step gives the command, what you should observe, a hint, and the defender/PAM takeaway.
>
> ⚠️ **AUTHORIZATION — read this first.** Run cloud assessment tools **only against a cloud account you own** (a **throwaway / free-tier** account with nothing valuable in it), and know your **provider's testing policy** — even self-service pentesting of *managed* services can require notice. Aggressive tools like **Pacu** modify resources. Container/Kubernetes work stays on **your own workstation** (see [`../../labs/`](../../labs/README.md) · [`../../labs/topology.md`](../../labs/topology.md)).

**Goal:** see how cloud compromise is almost always an **identity or configuration** failure — then watch each PAM/config control turn a win into a loss.

**Prereqs:** a throwaway cloud account + its CLI configured (`aws configure`), plus local `docker`, `trivy`, `kube-bench`, and (optionally) `minikube`/`kind`. Install tools only where you're allowed to.

---

## Part A — Posture audit + IAM enumeration (your own account)

### A1. Read-only posture audit
```bash
scoutsuite aws          # multi-cloud posture audit → HTML report
prowler aws             # CIS + best-practice checks
```
**You should see** a findings report; ScoutSuite writes an HTML dashboard, Prowler prints PASS/FAIL rows:
```
scout_report/index.html  generated
prowler: check11 -> FAIL (Ensure MFA is enabled for the root account)
prowler: s3    -> FAIL (Bucket 'demo-bucket' is publicly readable)
```
**Observe:** these tools are **read-only** — they enumerate misconfigurations, they don't change anything. Note how many findings are **identity/config** issues (public buckets, wildcard policies, no MFA).

<details><summary>Hint if the tools can't authenticate</summary>Confirm your creds first: `aws sts get-caller-identity`. If that fails, re-run `aws configure` (or set `AWS_PROFILE`). Use a profile scoped to the throwaway account so you never point these at production.</details>

### A2. Enumerate IAM for over-permissions
```bash
aws sts get-caller-identity
aws iam list-users
aws iam get-account-authorization-details   # dump policies to spot wildcards / privesc
```
**You should see** the policy dump; scan for danger signs like `"Action": "*"` or `iam:PassRole`:
```json
{ "Effect": "Allow", "Action": ["iam:PassRole","ec2:RunInstances"], "Resource": "*" }
```
**Observe:** `iam:PassRole` + a compute-launch permission is a **privilege-escalation** path — you can launch a resource carrying a more-privileged role and inherit it. `Action: "*"` on `Resource: "*"` is standing over-permission.

**Defender/PAM view:** right-size with **CIEM**, apply **permission boundaries / SCPs**, and grant elevation **JIT** via **Secure Cloud Access** instead of leaving standing wildcards. See [`../../defender-pam/cyberark-attack-mapping.md`](../../defender-pam/cyberark-attack-mapping.md).

---

## Part B — IMDS credential theft: IMDSv1 vs IMDSv2 (an instance you own)

Run these **on a free-tier VM you own** (an SSRF against a real app would reach the same endpoint).

### B1. IMDSv1 — the SSRF-reachable path
```bash
# No token needed on IMDSv1 — a single GET returns credentials:
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>
```
**You should see** the role name, then temporary credentials:
```json
{ "AccessKeyId":"ASIA...","SecretAccessKey":"...","Token":"...","Expiration":"..." }
```
**Observe:** one unauthenticated GET yields **live role credentials**. This is exactly what a server-side request forgery reaches — no shell required.

<details><summary>Hint: nothing returned?</summary>The instance may already enforce IMDSv2, or no role is attached. Attach a test role, or temporarily set the instance metadata option to `optional` (v1+v2) to reproduce the v1 behavior, then re-run.</details>

### B2. IMDSv2 — the mitigation
```bash
# Must PUT for a session token first, then send it as a header:
TOKEN=$(curl -sX PUT "http://169.254.169.254/latest/api/token" \
        -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
     http://169.254.169.254/latest/meta-data/iam/security-credentials/
```
Now **enforce IMDSv2 (require token, hop limit 1)** and retry the naïve B1 `curl`:
```bash
aws ec2 modify-instance-metadata-options --instance-id <id> \
    --http-tokens required --http-put-response-hop-limit 1
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/   # naïve GET
```
**You should see** the token flow succeed, but the naïve B1 GET now **fail**:
```
401 - Unauthorized (IMDSv1 request rejected)
```
**Observe:** an SSRF typically can only coerce a simple GET — it can't issue the `PUT` or set the token header, and the **hop limit** stops proxied hops. **You just neutralized the #1 SSRF-to-cloud path.**

**Defender/PAM view:** enforce IMDSv2 fleet-wide, fix the SSRF, and keep secrets **off the instance** with **Conjur**-delivered runtime secrets so a metadata theft yields nothing durable. Detection: role creds used from an off-instance IP; requests to `169.254.169.254` — see [`../../defender-pam/detection-engineering.md`](../../defender-pam/detection-engineering.md).

---

## Part C — Local Kubernetes & container hardening (your workstation only)

### C1. CIS benchmark + image/filesystem scans
```bash
kube-bench                              # CIS Benchmark audit of your node/cluster
trivy image bkimminich/juice-shop:latest   # scan a lab image for CVEs
trivy fs .                              # scan IaC + secrets in a repo you own
```
**You should see** failed CIS controls and CVE/secret counts:
```
[FAIL] 1.2.16 Ensure that the --anonymous-auth argument is set to false
juice-shop:latest  Total: 143 (HIGH: 51, CRITICAL: 12)
```
**Observe:** **kube-bench = defensive CIS audit**; **Trivy = vuln/IaC/secret scanning**. (The offensive counterpart, **kube-hunter --pod**, pentests only your own cluster.)

<details><summary>Hint: kube-bench finds no cluster?</summary>Start one first: `minikube start` or `kind create cluster`, then re-run. Trivy needs no cluster for `image`/`fs` scans — run those anywhere on your workstation.</details>

### C2. Container-escape indicators on a foothold container
```bash
docker run --rm -it alpine sh
# inside the container:
cat /proc/1/cgroup            # am I inside a container?
ls -la /var/run/docker.sock   # mounted docker socket = escape path
capsh --print                 # excess Linux capabilities?
```
**You should see** the container ID in cgroup, and (on a *safe* default run) **no** docker.sock and a **reduced** capability set:
```
/proc/1/cgroup: .../docker/3f9a...          <- you are in a container
ls: /var/run/docker.sock: No such file      <- good: no socket mounted
Current: cap_net_bind_service,... (dropped many)
```
Now re-run **insecurely** to see the risk (`docker run --rm -it -v /var/run/docker.sock:/var/run/docker.sock --privileged alpine sh`) and repeat the checks — the socket now appears and `capsh` shows a full capability set.
**Observe:** a mounted **`docker.sock`** or **`--privileged`** turns a container foothold into host takeover — the classic escape enablers.

**Defender/PAM view:** enforce **Pod Security Standards**, **no privileged pods**, **drop capabilities**, **read-only rootfs**, and **never mount `docker.sock`**. Detect host processes spawned from containers (Falco/EDR). See [`../../defender-pam/identity-attack-paths.md`](../../defender-pam/identity-attack-paths.md).

---

## What you should conclude
Every "win" above has a specific control that turns it into a logged, contained "loss":

| You did | The control that stops it |
|---|---|
| Found public bucket / wildcard IAM | Block Public Access + CIEM right-sizing + SCPs + JIT |
| Enumerated `iam:PassRole` privesc | Permission boundaries, least privilege, JIT elevation |
| Stole role creds via IMDSv1 | Enforce IMDSv2 (token + hop limit); keep secrets off the instance |
| Escaped via `docker.sock` / privileged | Pod Security Standards, drop caps, no socket, read-only rootfs |

Cloud compromise is almost always an **identity or configuration** failure. **IMDSv2 + private buckets + least-privilege IAM + no long-lived keys** removes the top attack paths — and every one is a PAM/CIEM control.

## Cleanup
```bash
# --- Local ---
docker rm -f $(docker ps -aq) 2>/dev/null     # remove lab containers
minikube delete 2>/dev/null; kind delete cluster 2>/dev/null
rm -rf scout_report/ *.html                    # scan artifacts

# --- Your cloud account ---
# Delete any test role, over-broad policy, and public bucket you created.
# Re-run 'prowler aws' to confirm the findings you created have cleared.
```

## Record it
Log commands, outputs, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
