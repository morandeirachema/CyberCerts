# Module 19 — Cloud Computing · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## Service models — what shifts to the provider
| Model | Provider runs | You still own |
|---|---|---|
| **IaaS** | Hardware, hypervisor, network | OS, runtime, app, **data + identity** (most customer responsibility) |
| **PaaS** | + OS + runtime | App/config, **data + identity** |
| **SaaS** | + the application | **Data + identity + access config** (least customer responsibility) |

You **always** own your **data and identities**, in every model. Customer responsibility decreases On-prem → IaaS → PaaS → SaaS.

## Deployment models
| Model | Who uses it |
|---|---|
| **Public** | Shared multi-tenant provider (AWS/Azure/GCP) |
| **Private** | Single organization, dedicated |
| **Community** | Orgs with a **common concern** (e.g., a regulatory sector) |
| **Hybrid** | Mix of the above with data/app portability |

## NIST SP 800-145 — the counts to memorize
- **5** essential characteristics: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service.
- **3** service models (IaaS/PaaS/SaaS).
- **4** deployment models (public/private/community/hybrid).

CEH asks "how many…": answer **5 / 3 / 4**.

## Shared responsibility — "of" vs "in"
- Provider secures **"of the cloud"** — hardware, hypervisor, managed-service internals.
- Customer secures **"in the cloud"** — data, identity/IAM, configuration, guest OS where applicable.

## Containers & Kubernetes
Containers share the **host kernel** (isolation = namespaces + cgroups + capabilities + seccomp/AppArmor) — **weaker isolation than a VM**, so escape is realistic. Kubernetes orchestrates them.

| K8s component | Role | Port | Exposure risk |
|---|---|---|---|
| API server | Control plane | **6443** (legacy insecure **8080**) | Anonymous / over-permissive RBAC |
| etcd | Key-value store (holds secrets) | **2379** | Unauthenticated read = full compromise |
| kubelet | Node agent | **10250** | Exec into pods if exposed |
| Dashboard | Web UI | — | Public dashboard = cluster takeover |

**Hardening:** RBAC least privilege, **Pod Security Standards/Admission**, **network policies**, no `privileged` pods, drop capabilities, read-only rootfs, **never mount `docker.sock`**, scan images.

## Serverless (FaaS)
Functions (Lambda / Cloud Functions / Azure Functions) push more to the provider, but you still own the **function's IAM role** and **code/dependencies**. Top risks: **over-privileged function role**, event-data injection, vulnerable dependencies, **secrets in environment variables**.

## Canonical cloud attacks
| Attack | Mechanism | Why it works |
|---|---|---|
| **Public storage bucket** | S3/Blob/GCS public or ACL-misconfigured | Default-open or lazy ACLs |
| **Over-permissive IAM / privesc** | Wildcard actions; abuse **`iam:PassRole`**, `CreatePolicyVersion`, `AttachUserPolicy` | Standing, broad entitlements |
| **IMDS SSRF** | App SSRF → **169.254.169.254** → steal instance **role credentials** | **IMDSv1** answers any local request |
| **Container escape** | Break out of a `privileged`/misconfigured container to the host | Shared kernel + excess capabilities / mounted socket |
| **Exposed secrets** | Keys in code, git history, env vars, metadata | Long-lived credentials committed/leaked |

## IMDS — 169.254.169.254 (link-local)
Serves instance data **including temporary role credentials**.
- **IMDSv1** = request/response — **SSRF-reachable** (a single GET returns creds).
- **IMDSv2** = session-oriented: requires a **`PUT` token first**, then that token on every request, and honors a **hop limit** (default 1). This blocks the classic SSRF path because an SSRF typically can't issue the PUT and can't set the header.

## Tools → purpose
| Tool | Purpose |
|---|---|
| **ScoutSuite** | Multi-cloud posture audit (read-only) |
| **Prowler** | AWS/Azure/GCP CIS & best-practice checks |
| **Pacu** | AWS **exploitation** framework (enum + privesc) |
| **kube-hunter** | Kubernetes **pentest** (offensive) |
| **kube-bench** | Kubernetes **CIS Benchmark** audit (defensive) |
| **Trivy** | Image / IaC / secret vulnerability scanner |

## PAM angle (identity is the perimeter)
- **Secure Cloud Access / CIEM** → **JIT** elevation to consoles and roles; continuously **right-size** entitlements to kill standing privilege.
- **Conjur / CCP** → deliver secrets at **runtime**; keep them off the instance so an IMDS-SSRF theft yields nothing durable.
- **No long-lived keys** → federate via STS/short-lived credentials; rotate; never put secrets in env vars or code.
- **Break-glass** root/owner accounts sealed behind hardware MFA with alerting on every use.
- Detection (privileged lens): requests to `169.254.169.254`, new admin-role assignments, unused-then-used permissions.

## Top traps
- **kube-bench = CIS audit (defensive); kube-hunter = pentest (offensive).** Don't swap them. **Trivy = vuln/IaC/secret scanning.**
- **IaaS = MOST customer responsibility, SaaS = LEAST** — but you **always** own data + identities.
- **IMDSv2** (token + hop limit) mitigates the SSRF path; **IMDSv1** does not. The address is **169.254.169.254**.
- **Community cloud** = shared **common concern**; don't confuse it with **public**.
- **Container ≠ VM:** shared **host kernel**; `privileged` + mounted **`docker.sock`** are the classic escape enablers.
- **NIST counts: 5 / 3 / 4** (characteristics / service / deployment).
- Provider = security **of** the cloud; customer = security **in** the cloud.
- **Serverless** still carries the **over-privileged function role** risk — least privilege applies to functions too.
- IAM privesc keyword to spot: **`iam:PassRole`** (hand a role to a service you control).
