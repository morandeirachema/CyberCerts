# Module 19 — Cloud Computing · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** Under the shared responsibility model for an **IaaS** deployment, which of the following is the **customer's** responsibility?

- A. Patching the hypervisor
- B. Physical security of the data center
- C. Patching the guest operating system
- D. Securing the managed-service backplane

<details><summary>Answer</summary>

**C. Patching the guest OS.** In IaaS the provider secures "of the cloud" (hardware, hypervisor, facility); the customer secures "in the cloud", which in IaaS includes the **guest OS, runtime, app, data, and identity**. IaaS = the **most** customer responsibility. A, B, and D are provider duties.
</details>

---

**Q2.** Which statement is true across **all** cloud service models (IaaS, PaaS, and SaaS)?

- A. The customer always patches the operating system
- B. The customer always owns their data and identities
- C. The provider always manages the application code
- D. The provider always owns the customer's IAM configuration

<details><summary>Answer</summary>

**B.** Regardless of model, **data and identities are always the customer's responsibility**. A is false (in PaaS/SaaS the provider handles the OS); C is false (only in SaaS); D is false — the customer always owns their access configuration.
</details>

---

**Q3.** A web app is vulnerable to SSRF. On an EC2 instance using **IMDSv1**, what is the most valuable target an attacker reaches via `http://169.254.169.254/`?

- A. The instance's temporary IAM **role credentials**
- B. The AWS root account password
- C. The hypervisor management console
- D. Other tenants' metadata

<details><summary>Answer</summary>

**A. The instance's temporary IAM role credentials** at `/latest/meta-data/iam/security-credentials/`. With IMDSv1 a single SSRF-driven GET returns them, and the attacker then uses them from anywhere. It cannot reach the root password (B), the hypervisor (C), or other tenants (D) — metadata is per-instance.
</details>

---

**Q4.** Why does **IMDSv2** defeat the classic SSRF-to-metadata attack that works against **IMDSv1**?

- A. It moves metadata to a public IP
- B. It disables the metadata service entirely
- C. It encrypts the role credentials at rest
- D. It requires a session token obtained via a `PUT`, plus a hop limit

<details><summary>Answer</summary>

**D.** IMDSv2 is session-oriented: you must first `PUT` to `/latest/api/token`, then send that token as a header on every request, and the service enforces a **hop limit** (default 1). A typical SSRF can only coerce a simple GET and cannot set custom headers or issue the PUT, so the credential path breaks. The address is still **169.254.169.254**.
</details>

---

**Q5.** In a Kubernetes cluster, which component holds **secrets** and, if reachable **unauthenticated on port 2379**, means full cluster compromise?

- A. kubelet
- B. API server
- C. etcd
- D. kube-proxy

<details><summary>Answer</summary>

**C. etcd** (port **2379**) is the key-value store backing the cluster, including Secrets (often base64, not encrypted by default). Unauthenticated read access exposes everything. The API server is **6443** (legacy **8080**); the **kubelet** is **10250**.
</details>

---

**Q6.** An exposed Kubernetes **kubelet** API is dangerous primarily because an attacker can:

- A. Read the cloud provider's billing data
- B. Delete the etcd database directly
- C. Rotate the cluster's TLS certificates
- D. Execute commands inside pods on that node

<details><summary>Answer</summary>

**D.** The kubelet (**10250**) is the node agent; an exposed/anonymous kubelet API lets an attacker run commands (`exec`) in the pods on that node and read their secrets. It is a node-level foothold, not a billing (A), PKI (C), or direct etcd (B) interface.
</details>

---

**Q7.** During enumeration of your own AWS account you find a policy granting `iam:PassRole` plus permission to launch EC2/Lambda. Why is this a **privilege-escalation** path?

- A. `PassRole` lets you read other users' passwords
- B. You can hand a **more-privileged role** to a service you control and inherit its permissions
- C. It disables CloudTrail logging
- D. It grants root automatically

<details><summary>Answer</summary>

**B.** `iam:PassRole` lets a principal **assign an existing role to a service** (e.g., launch an EC2 instance or Lambda with an admin role attached), then operate as that role — classic privesc. `CreatePolicyVersion` and `AttachUserPolicy` are other keywords to spot. It does not read passwords, disable logging, or grant root by itself.
</details>

---

**Q8.** Which tool pairing is **correct** for Kubernetes?

- A. kube-bench = pentest; kube-hunter = CIS audit
- B. Both are image scanners
- C. Both are exploitation frameworks
- D. kube-bench = CIS Benchmark audit; kube-hunter = penetration testing

<details><summary>Answer</summary>

**D.** **kube-bench** runs the **CIS Benchmark** (defensive audit of your node/cluster config); **kube-hunter** actively **pentests** (offensive) the cluster. Don't swap them. Image/IaC/secret scanning is **Trivy's** job.
</details>

---

**Q9.** You need a **read-only, multi-cloud posture audit** that flags misconfigurations without changing anything. Which tool fits best?

- A. ScoutSuite
- B. Pacu
- C. Mimikatz
- D. Responder

<details><summary>Answer</summary>

**A. ScoutSuite** performs a read-only multi-cloud posture audit and produces an HTML report. **Pacu** is the AWS **exploitation** framework (it modifies resources — use only on a throwaway account). Mimikatz and Responder are unrelated (Windows credential / LLMNR tooling).
</details>

---

**Q10.** On a foothold container, which single indicator most directly suggests a viable **container-escape** path to the host?

- A. `/proc/1/cgroup` mentions a container ID
- B. A mounted `/var/run/docker.sock`
- C. The container has an IPv6 address
- D. `hostname` returns a random string

<details><summary>Answer</summary>

**B. A mounted `docker.sock`.** Access to the Docker daemon socket lets you start a new privileged container that mounts the host filesystem — a direct escape. `/proc/1/cgroup` (A) only tells you that you *are* in a container; C and D are normal container traits, not escape paths. Other enablers: `privileged` mode and excess capabilities (check `capsh --print`).
</details>

---

**Q11.** According to **NIST SP 800-145**, how many essential characteristics, service models, and deployment models define cloud computing?

- A. 3, 4, 5
- B. 5, 3, 4
- C. 4, 3, 5
- D. 5, 4, 3

<details><summary>Answer</summary>

**B. 5 / 3 / 4.** **5** essential characteristics (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service), **3** service models (IaaS/PaaS/SaaS), **4** deployment models (public/private/community/hybrid).
</details>

---

**Q12.** A cloud model shared by several organizations that have a **common concern** (e.g., the same regulatory regime) is which deployment model?

- A. Public
- B. Private
- C. Community
- D. Hybrid

<details><summary>Answer</summary>

**C. Community.** Shared infrastructure among organizations with a **common concern** (compliance, mission, security policy). Don't confuse it with **public** (open multi-tenant) — that swap is a classic trap.
</details>

---

**Q13.** Which is the **most durable** control against the "SSRF → steal instance role credentials" attack path?

- A. Enforce IMDSv2 (token + hop limit) and keep secrets off the instance
- B. A longer instance password
- C. Disable IPv6 on the VPC
- D. Rotate the AWS root password weekly

<details><summary>Answer</summary>

**A.** **Enforce IMDSv2** (require token, hop limit 1) so SSRF can't pull creds, and deliver secrets at runtime (e.g., Conjur) so the instance holds nothing long-lived. Fixing the SSRF itself and preferring short-lived roles over keys complete the fix. B, C, and D don't address the metadata path.
</details>

---

**Q14.** For **serverless (FaaS)**, which risk remains squarely the customer's responsibility?

- A. Patching the underlying container runtime
- B. Physical host security
- C. An **over-privileged function IAM role**
- D. Hypervisor isolation between tenants

<details><summary>Answer</summary>

**C.** Even though the provider runs the platform, the customer owns the **function's IAM role** and its **code/dependencies**. An over-privileged role is the top serverless risk (plus event-data injection, vulnerable dependencies, and secrets in environment variables). A, B, D are provider duties.
</details>

---

**Q15.** A CSPM tool alerts that an S3 bucket is world-readable. Which control **most directly** remediates it and prevents recurrence?

- A. Enable "Block Public Access" and enforce it via IaC guardrails
- B. Rotate the bucket's encryption key
- C. Add the bucket to a private subnet
- D. Enable MFA on the root account

<details><summary>Answer</summary>

**A.** "Block Public Access" plus least-privilege bucket policy, applied and enforced through **IaC guardrails/CSPM**, closes the exposure and stops it drifting back open. Key rotation (B) doesn't affect access; buckets aren't in subnets (C); root MFA (D) is good hygiene but unrelated to this misconfiguration.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the Containers & Kubernetes and IMDS sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
