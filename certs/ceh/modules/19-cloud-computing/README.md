# Module 19 — Cloud Computing

> **One-liner:** attacking and defending IaaS/PaaS/SaaS, containers, Kubernetes, and serverless — where the perimeter is gone and **identity is everything**. The signature cloud breaches (public buckets, over-permissive IAM, stolen instance-role creds via SSRF) are all failures of the exact discipline a PAM practitioner owns: least privilege, short-lived credentials, and secrets management.

> **📚 Study companions:** [Facts sheet](facts.md) · [Practice questions](practice-questions.md) · [Flashcards (Anki)](flashcards.csv) · [Lab walkthrough](lab-walkthrough.md)

## Exam focus

- The three **service models** (IaaS / PaaS / SaaS) and what each shifts to the provider.
- The four **deployment models** (public / private / hybrid / community) and NIST's **5 essential characteristics**.
- The **shared responsibility model**: security *of* the cloud vs. security *in* the cloud.
- **Container & Kubernetes** components, attack surface, and hardening (RBAC, PSA, network policy).
- **Serverless (FaaS)** basics and its risks.
- The canonical **cloud attacks**: misconfigured storage buckets, over-permissive IAM & IAM privilege escalation, **instance metadata SSRF (169.254.169.254)**, container escape, exposed secrets.
- **IMDSv1 vs IMDSv2** as the SSRF mitigation.
- Tooling → purpose pairs: ScoutSuite, Prowler, Pacu, kube-hunter, kube-bench, Trivy.

## Key concepts

### Service models & the shared responsibility line

| Layer | On-prem | IaaS | PaaS | SaaS |
|---|:--:|:--:|:--:|:--:|
| **Data** | YOU | YOU | YOU | YOU |
| **Identity** | YOU | YOU | YOU | YOU |
| App | YOU | YOU | YOU | CSP |
| Runtime | YOU | YOU | CSP | CSP |
| OS | YOU | YOU | CSP | CSP |
| Virtualization | YOU | CSP | CSP | CSP |
| Network / HW | YOU | CSP | CSP | CSP |

> You **always** own your **data and identities**, regardless of model. Customer responsibility decreases left → right (On-prem → SaaS).

- Provider secures **"of the cloud"** (hardware, hypervisor, managed-service internals).
- Customer secures **"in the cloud"** (data, identity/IAM, config, OS where applicable).
- **IaaS = customer owns the most**; **SaaS = the least** — but you **always** own your data, identities, and access configuration.

### Deployment models & NIST definition

| Model | Who uses it |
|---|---|
| **Public** | Shared multi-tenant provider (AWS/Azure/GCP) |
| **Private** | Single organization, dedicated |
| **Community** | Shared by orgs with **common concerns** (e.g., a regulatory sector) |
| **Hybrid** | Mix of the above with data/app portability |

**NIST SP 800-145** frames the cloud as **5 essential characteristics** (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) × **3 service models** × **4 deployment models**. Memorize the counts — CEH asks "how many…".

### Containers & Kubernetes

Containers share the **host kernel** (isolation via namespaces + cgroups + capabilities + seccomp/AppArmor) — **weaker isolation than a VM**. Kubernetes orchestrates them.

| K8s component | Role | Exposure risk |
|---|---|---|
| API server | Cluster control plane (**6443**; legacy insecure **8080**) | Anonymous/over-permissive RBAC |
| etcd | Key-value store (secrets!) (**2379**) | Unauthenticated read = full compromise |
| kubelet | Node agent (**10250**) | Exec into pods if exposed |
| Dashboard | Web UI | Public dashboard = takeover |

**Hardening:** RBAC least privilege, **Pod Security Standards**, network policies, no `privileged` pods, drop capabilities, read-only rootfs, don't mount `docker.sock`, scan images.

### Serverless (FaaS)

Functions (Lambda / Cloud Functions / Azure Functions) push even more to the provider, but you still own the **function's IAM role** and **code/dependencies**. Top risks: **over-privileged function roles**, event-data injection, vulnerable dependencies, and **secrets in environment variables**.

### Canonical cloud attacks

| Attack | Mechanism | Why it works |
|---|---|---|
| **Public storage bucket** | S3/Blob/GCS made public or ACL-misconfigured | Default-open or lazy ACLs |
| **Over-permissive IAM / privesc** | Wildcard actions; abuse `iam:PassRole`, `CreatePolicyVersion`, `AttachUserPolicy` | Standing, broad entitlements |
| **IMDS SSRF** | App SSRF → `169.254.169.254` → steal the instance **role credentials** | **IMDSv1** answers any local request |
| **Container escape** | Break out of a `privileged`/misconfigured container to the host | Shared kernel + excess capabilities / mounted socket |
| **Exposed secrets** | Keys in code, git history, env vars, metadata | Long-lived credentials committed/leaked |

**Instance Metadata Service (IMDS):** the link-local address **169.254.169.254** serves instance data **including temporary role credentials**. **IMDSv1** is request/response (SSRF-reachable). **IMDSv2** requires a session token (a `PUT` first) and honors a **hop limit**, which blocks the classic SSRF path.

## Key tools

| Tool | Purpose | Reference |
|---|---|---|
| ScoutSuite | Multi-cloud security posture audit (read-only) | https://github.com/nccgroup/ScoutSuite |
| Prowler | AWS/Azure/GCP CIS & best-practice checks | https://github.com/prowler-cloud/prowler |
| Pacu | AWS **exploitation** framework (privesc, enum) | https://github.com/RhinoSecurityLabs/pacu |
| kube-hunter | Kubernetes penetration testing | https://github.com/aquasecurity/kube-hunter |
| kube-bench | Kubernetes **CIS Benchmark** audit | https://github.com/aquasecurity/kube-bench |
| Trivy | Image / IaC / secret vulnerability scanner | https://github.com/aquasecurity/trivy |

## Commands & techniques (lab-ready)

> ⚠️ **AUTHORIZATION — read this first.** Run cloud assessment tools **only against a cloud account you own**, and know your provider's testing policy — even self-service pentesting of *managed* services can require notice. Aggressive tools like **Pacu** modify resources; use a **throwaway/free-tier account** with nothing valuable in it. Local container/Kubernetes work stays on **your own workstation** (the Docker range in [`../../labs/`](../../labs/README.md) / [`../../labs/topology.md`](../../labs/topology.md)).

```bash
# --- Posture audit of YOUR OWN account (read-only) ---
scoutsuite aws                                   # HTML posture report
prowler aws                                       # CIS + best-practice checks

# --- IAM enumeration with your own creds (hunt over-permissions) ---
aws sts get-caller-identity
aws iam list-users
aws iam get-account-authorization-details          # dump policies to spot wildcards/privesc

# --- IMDS credential theft demo, from an instance YOU own ---
# IMDSv1 (no token) — this is what an SSRF reaches via 169.254.169.254:
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
# IMDSv2 (mitigation) requires a session token first:
TOKEN=$(curl -sX PUT "http://169.254.169.254/latest/api/token" \
        -H "X-aws-ec2-metadata-token-ttl-seconds: 60")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/

# --- Pacu: AWS exploitation FRAMEWORK, only against your own account ---
pacu
#  > import_keys --all
#  > run iam__enum_permissions
#  > run iam__privesc_scan            # reports privilege-escalation paths in your account

# --- Local Kubernetes / containers (your workstation only) ---
kube-bench                                        # CIS benchmark of your node/cluster
kube-hunter --pod                                 # test ONLY your own cluster
trivy image bkimminich/juice-shop:latest          # scan a lab image for CVEs
trivy fs .                                         # scan IaC + secrets in a repo you own

# --- Container-escape indicators to check on a foothold container ---
cat /proc/1/cgroup                                # am I inside a container?
ls -la /var/run/docker.sock                       # mounted docker socket = escape path
capsh --print                                     # excess Linux capabilities?
```

## Lab exercise

1. **Scan locally, free:** `docker compose up -d` the web range, then `trivy image` each image and note the CVE counts. If you have `minikube`/`kind`, run `kube-bench` and read the failed CIS controls.
2. **Own-account posture (free tier):** in a **throwaway** cloud account, run **ScoutSuite** and **Prowler** read-only. Create an intentionally **public bucket**, confirm the tool flags it, then enable "block public access" and re-scan — watch the finding clear.
3. **IMDS before/after:** on your own free-tier VM, `curl` IMDSv1 to pull the role credentials, then **enforce IMDSv2** (require token, hop limit 1) and repeat — the naïve `curl` now fails. You just neutralized the #1 SSRF-to-cloud path.
4. **Least privilege proof:** attach an over-broad policy to a test user, run Pacu's `iam__privesc_scan`, watch it find a path; tighten to least privilege and re-run — the path disappears.

**What you should observe:** cloud compromise is almost always an **identity or configuration** failure. **IMDSv2 + private buckets + least-privilege IAM + no long-lived keys** removes the top attack paths — and every one of those is a PAM/CIEM control.

## Defender & PAM mapping

| Attack | Detection signal | Control / PAM lever |
|---|---|---|
| Public storage bucket | CSPM alert, CloudTrail `PutBucketAcl`, spike in anon reads | **Block public access**, least-priv bucket policy, IaC guardrails, CSPM |
| Over-permissive IAM / privesc | CloudTrail `AttachUserPolicy`/`CreatePolicyVersion`/`PassRole`, Access Analyzer | **IAM least privilege**, **CIEM** right-sizing, permission boundaries, SCPs, **JIT** access |
| IMDS SSRF credential theft | Role creds used from an off-instance IP; GuardDuty exfil finding | **Enforce IMDSv2**, hop limit 1, fix SSRF, prefer short-lived roles over keys |
| Long-lived access keys | Old keys in the access-key-age report; keys in code | **No long-lived keys** — federate/STS, secrets manager, rotation, JIT |
| Exposed secrets in code | Secret-scanner hits, git history matches | **Vault/KMS**, pre-commit secret scanning, immediate rotation + revoke |
| Container escape | Falco/Sysmon privileged syscalls, host process from a container | No `privileged` pods, drop caps, Pod Security Standards, don't mount `docker.sock`, read-only rootfs |
| K8s API/dashboard exposure | Anonymous API calls, dashboard hits, kubelet access | **RBAC least privilege**, network policy, private API endpoint, disable anonymous auth |
| Console/root access without MFA | Sign-in events lacking MFA, root usage | Enforce MFA/SSO via IdP, **sealed & monitored break-glass** root/owner accounts |

> **PAM playbook for cloud:** identity **is** the perimeter. Kill **standing privilege** with **JIT** elevation, use **CIEM** to continuously right-size entitlements, replace **long-lived keys** with short-lived federated credentials, store secrets in **Vault / cloud KMS** (never env vars or code), and keep **break-glass** root/owner accounts sealed behind hardware MFA with alerting on every use. See [`../../defender-pam/`](../../defender-pam/README.md).

### 🔐 PAM engineering deep-dive (CyberArk)

Cloud breaches chase **standing entitlements** and **long-lived keys**. The cloud-native PAM answer is JIT access to consoles and runtime secrets instead of stored keys.

| This module's attack | CyberArk control | Component |
|---|---|---|
| Over-privileged cloud IAM roles | JIT access + right-size entitlements | Secure Cloud Access (CIEM) |
| Long-lived access keys | Eliminate; deliver secrets at runtime | Conjur / CCP |
| SSRF → instance metadata theft | Keep secrets off the instance; IMDSv2 | Conjur + IMDSv2 |
| Standing console admin | JIT to consoles + session recording | Secure Cloud Access + Secure Web Sessions |

**Detection (privileged lens):** requests to `169.254.169.254`, new admin-role assignments, unused-then-used permissions — see [`../../defender-pam/detection-engineering.md`](../../defender-pam/detection-engineering.md).

**Engineering note:** replace long-lived keys with **Conjur-delivered** secrets and stand up **JIT console access** via Secure Cloud Access — remove the standing entitlements and durable keys these attacks depend on.

> Go deeper: [CyberArk mapping](../../defender-pam/cyberark-attack-mapping.md) · [identity attack paths — Entra](../../defender-pam/identity-attack-paths.md)

## Exam tips & gotchas

- **Shared responsibility:** provider = security **of** the cloud; customer = security **in** the cloud. **IaaS = most customer responsibility, SaaS = least** — but the customer **always** owns data + identities.
- **NIST SP 800-145 counts:** **5** essential characteristics, **3** service models, **4** deployment models.
- **169.254.169.254** = instance metadata (link-local). **IMDSv2** (token + hop limit) mitigates the SSRF path; **IMDSv1** does not.
- **Community cloud** = shared by orgs with a **common concern** (don't confuse with public).
- **Container ≠ VM:** containers share the **host kernel**, so escape is a realistic risk; `privileged` + mounted `docker.sock` are the classic enablers.
- **kube-bench = CIS audit (defensive); kube-hunter = pentest (offensive).** Don't swap them. **Trivy = vuln/IaC/secret scanning.**
- **Serverless** still carries an **over-privileged function role** risk — least privilege applies to functions too.

## Sources

- NIST SP 800-145 (The NIST Definition of Cloud Computing) — https://csrc.nist.gov/pubs/sp/800/145/final
- AWS Shared Responsibility Model — https://aws.amazon.com/compliance/shared-responsibility-model/
- AWS — Configure the Instance Metadata Service (IMDSv2) — https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html
- Kubernetes — Security concepts — https://kubernetes.io/docs/concepts/security/
- OWASP Kubernetes Top Ten — https://owasp.org/www-project-kubernetes-top-ten/
- CIS Benchmarks — https://www.cisecurity.org/cis-benchmarks
- MITRE ATT&CK — Cloud matrix — https://attack.mitre.org/matrices/enterprise/cloud/
- ScoutSuite — https://github.com/nccgroup/ScoutSuite · Prowler — https://github.com/prowler-cloud/prowler · Pacu — https://github.com/RhinoSecurityLabs/pacu
- kube-hunter — https://github.com/aquasecurity/kube-hunter · kube-bench — https://github.com/aquasecurity/kube-bench · Trivy — https://github.com/aquasecurity/trivy

---
### 📝 My lab log (fill in)
| Date | Target | Command | Result / notes |
|---|---|---|---|
|  |  |  |  |
