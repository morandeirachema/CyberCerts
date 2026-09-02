# Glossary

> 🔁 This is the **PAM / identity** glossary. For offensive / ethical-hacking terms, see the
> [CEH glossary](../certs/ceh/reference/glossary.md) — the two are complementary, not duplicated.

An alphabetical glossary of Privileged Access Management (PAM), identity and broader
cybersecurity terms, each defined **in PAM context** for a sysadmin starting a career in
access security. Where a term is treated in depth elsewhere in this repo, the entry
cross-links to the relevant [foundations](../foundations/) page or to the
[PAM playbook](../certs/ceh/defender-pam/pam-playbook.md) /
[PAM architecture](../certs/ceh/defender-pam/pam-architecture.md) pages.

For the expansions of acronyms, see [acronyms.md](acronyms.md). For how these concepts
map to regulations, see [compliance-and-standards.md](compliance-and-standards.md).

> Conventions: PAM data-model objects (Account, Authorization, Target, etc.) are
> capitalised when referring to objects in a PAM platform's configuration; product names
> vary by vendor.

---

## A

**Access Control List (ACL)** — A set of rules stating which subjects may perform which
actions on which objects. Most PAM platforms' rights engines are ACLs binding user
groups to target groups.

**Access certification (recertification)** — A periodic governance review where managers
re-confirm that each person's access is still appropriate; stale rights are revoked. A
core IGA/IAG capability — see
[pam-iam-iga-idaas-epm.md](../foundations/pam-iam-iga-idaas-epm.md).

**Account (target account)** — In a PAM platform, the credential-bearing entity used to
authenticate to a target system (device + service + account); it usually belongs to a
domain. Types include directory/global, local/device and application accounts.

**Agentless** — Requiring no software installed on the target. A proxy-based PAM bastion
is agentless on targets (it proxies the protocol), which is essential in OT where
PLCs/RTUs cannot host agents. Contrast with the agent-based EPM model on endpoints.

**Application-to-Application (A2A)** — Machine-to-machine authentication where one
application retrieves a credential to talk to another, with no human involved; the use
case behind AAPM (removing hard-coded passwords). See
[privileged-accounts-and-credentials.md](../foundations/privileged-accounts-and-credentials.md).

**Attack surface** — The total set of points an attacker could exploit. PAM shrinks it by
removing standing local-admin accounts, vaulting credentials and brokering all privileged
access. See [pam-threat-landscape.md](../foundations/pam-threat-landscape.md).

**Authentication (AuthN)** — Proving *who you are* (password, token, biometric). A PAM
gateway authenticates the human (often with MFA) before any privileged access.

**Authorization (AuthZ)** — Determining *what you may do* once authenticated. In a PAM
platform the **Authorization** (access policy) object binds a user group to a target
group, carrying session and/or secret-retrieval rights.

## B

**Bastion host / jump server** — A hardened intermediary that all privileged connections
pass through, so administrators never connect directly to targets. A PAM session proxy
is a bastion with vaulting and recording added; see
[what-is-pam.md](../foundations/what-is-pam.md) and
[pam-architecture.md](../certs/ceh/defender-pam/pam-architecture.md).

**Blast radius** — How much damage a single compromise can cause. Least privilege and
session isolation keep the blast radius small.

**Break-glass** — A pre-arranged, heavily-audited emergency override that grants
exceptional privileged access when normal channels fail. Must be rare, alarmed and
time-limited. See [core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

**Broker (proxy)** — The PAM gateway sits *between* user and target, terminating the user
side and opening a separate, credential-injected connection to the target. This brokering
gives isolation, recording and credential hiding. See
[what-is-pam.md](../foundations/what-is-pam.md).

## C

**Check-out / check-in** — The borrow-and-return model for vaulted secrets: a user checks
out a credential (optionally locking it for exclusive use), uses it, then checks it in — at
which point it can be automatically rotated. See
[privileged-accounts-and-credentials.md](../foundations/privileged-accounts-and-credentials.md).

**Credential** — A secret used to authenticate (password, SSH key, certificate, API key).
PAM's job is to vault, rotate and hide credentials from the human user.

**Credential injection** — The gateway supplies the target credential to the session
*directly* so the user never sees or types it; defeats credential theft from the
workstation. See [what-is-pam.md](../foundations/what-is-pam.md).

**Credential vault (secrets vault)** — An encrypted central store for passwords, SSH keys
and certificates, replacing secrets scattered on endpoints, scripts and spreadsheets. The
password-manager component of a PAM platform is the vault.

## D

**Defense in depth** — Layering multiple independent controls so no single failure is
catastrophic; PAM is one layer alongside EPM, MFA, segmentation and monitoring.

**Disaster Recovery (DR)** — Restoring service after a major outage. For what a PAM
platform must replicate (vault, policy, recordings) see
[pam-architecture.md](../certs/ceh/defender-pam/pam-architecture.md).

**Dual control (four-eyes)** — A real-time form of SoD requiring two people for a sensitive
action: one performs it, one approves/watches. In PAM: approval workflows and
**4-eyes** (watch) / **4-hands** (take control) live monitoring. See
[core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

## E

**Elevation (privilege elevation)** — Temporarily raising a process or user to higher
rights. PEDM/EPM elevate the *specific action* rather than the whole user; see
[pam-iam-iga-idaas-epm.md](../foundations/pam-iam-iga-idaas-epm.md).

**Encryption at rest** — Protecting stored data with encryption. A PAM appliance
typically uses full-disk encryption (e.g. **LUKS**/dm-crypt) and encrypts session
recordings so only the originating platform can replay them.

**Endpoint Privilege Management (EPM)** — Removing local-admin rights from
workstations/servers and granting per-application elevation (privilege attached to
applications, not users).

**Entitlement** — A specific right or permission granted to an identity. Governance (IGA)
maps entitlements; CIEM right-sizes them in the cloud.

## F

**Federation** — Trusting another system's authentication so a user can SSO across domains,
via SAML/OIDC. IDaaS platforms and PAM web portals use federation for SSO/MFA. See
[pam-iam-iga-idaas-epm.md](../foundations/pam-iam-iga-idaas-epm.md).

**Four-eyes principle** — See **Dual control**.

## G

**Gateway** — See **Broker (proxy)** and **Bastion host**. Many PAM products add a web
gateway/reverse proxy in front of one or more session proxies for HTML5 access.

**Governance** — The discipline of deciding and proving *who should have access*; delivered
by IGA/IAG (access reviews, SoD, compliance reporting), distinct from the IAM plumbing that
*operates* access.

## H

**Hardening** — Reducing a system's attack surface by removing unneeded services,
tightening configuration and applying secure defaults; expected of a bastion appliance.

**High Availability (HA)** — Configuration that avoids single points of failure. For PAM
this usually means clustered/replicated vault databases plus multiple session proxies;
check what is *not* replicated (often audit and recording data). See
[pam-architecture.md](../certs/ceh/defender-pam/pam-architecture.md).

## I

**Identity** — The digital representation of a person, service or machine. IAM manages
identities; PAM controls the *privileged* subset of what they can do.

**Identity & Access Governance (IAG/IGA)** — The governance overlay (access reviews, SoD,
remediation, compliance). See
[pam-iam-iga-idaas-epm.md](../foundations/pam-iam-iga-idaas-epm.md).

**Identity-as-a-Service (IDaaS)** — Cloud-delivered IAM (SSO/MFA/federation), e.g. Okta
or Microsoft Entra ID.

**Just-in-Time, see JIT (filed under J).**

## J

**Joiner-Mover-Leaver (JML)** — The identity lifecycle: onboarding, role change,
offboarding. Governance recertifies access at each transition (especially "mover") to
prevent privilege accumulation.

**Jump server (jump host)** — See **Bastion host**.

**Just-In-Time (JIT) access** — Granting privileged access only at the moment it is needed,
for a specific task and limited time, then auto-revoking it. PoLP applied to *time*. See
[core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

## L

**Lateral movement** — An attacker's technique of hopping from one compromised host to
others, typically by reusing harvested credentials. Session isolation, credential hiding
and least privilege break the chain. See
[pam-threat-landscape.md](../foundations/pam-threat-landscape.md).

**Least privilege (PoLP)** — Granting the minimum rights needed, for no longer than
necessary (NIST SP 800-53 AC-6); the foundational rule of access security. See
[core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

## M

**Multi-Factor Authentication (MFA)** — Requiring two or more independent factors (know /
have / are). A PAM gateway typically requires MFA before privileged access. See
[pam-iam-iga-idaas-epm.md](../foundations/pam-iam-iga-idaas-epm.md).

## N

**Non-human identity (machine identity)** — A service account, application or bot that
authenticates without a person. These vastly outnumber humans and are managed via vaulting,
rotation and AAPM. See
[privileged-accounts-and-credentials.md](../foundations/privileged-accounts-and-credentials.md).

**Non-repudiation** — The property that a user cannot credibly deny what they did, because
tamper-resistant, individually-attributed evidence (session recording) exists. Requires
named accounts, not shared ones.

## O

**Orphan account** — An account whose owner has left or is unknown, left active by mistake;
a prime attacker foothold. Governance (IAG) discovers and remediates orphan/over-entitled
accounts.

**Over-privileged (over-entitled)** — Holding more rights than the role needs; the gap
least privilege and access reviews aim to close.

## P

**Pass-the-Hash (PtH)** — An attack that authenticates using a stolen password *hash*
without cracking it, enabling lateral movement on Windows. PAM mitigates it by hiding
credentials, rotating secrets and not exposing hashes to the workstation. See
[pam-threat-landscape.md](../foundations/pam-threat-landscape.md).

**Pass-the-Ticket (PtT)** — Similar to Pass-the-Hash but reusing a stolen Kerberos ticket.

**Privilege Elevation & Delegation Management (PEDM)** — Elevating a specific
command/application rather than the whole user; least privilege at the action level.

**Privileged access** — Access that can change, control or destroy systems and data
(admin/root, network gear, databases, hypervisors). The "dangerous" subset PAM exists to
control. See [what-is-pam.md](../foundations/what-is-pam.md).

**Privileged Access Management (PAM)** — The discipline of controlling, vaulting,
brokering, recording and auditing privileged access. See
[what-is-pam.md](../foundations/what-is-pam.md).

**Privileged account** — An account with elevated rights (e.g. `root`, `Administrator`,
`sa`, network-device enable, service accounts). Catalogued by risk in
[privileged-accounts-and-credentials.md](../foundations/privileged-accounts-and-credentials.md).

**Privileged Access Governance (PAG)** — IGA governance applied specifically to privileged
accounts (pairing an IGA tool with the PAM platform).

**Proxy** — See **Broker**.

**Purdue Model** — A reference model layering industrial networks (Levels 0–5). A PAM
jump/bastion host typically sits in the **Industrial DMZ (Level 3.5)** between OT and IT.
See [acronyms.md](acronyms.md) and
[05-pam-for-ot.md](../certs/ceh/ot-security/05-pam-for-ot.md).

## R

**Reconciliation account** — A privileged "administrator" account the PAM tool uses to
reset/fix a target credential when its vaulted value has drifted out of sync with the
target. See
[privileged-accounts-and-credentials.md](../foundations/privileged-accounts-and-credentials.md).

**Reverse proxy** — A server that fronts internal services and forwards requests to them;
PAM web portals are typically HTML5 reverse proxies in front of the session proxy.

**Role-Based Access Control (RBAC)** — Granting access by assigning users to roles that
bundle permissions, simplifying administration and reviews.

**Rotation (credential rotation)** — Automatically changing secrets on a schedule or after
each use, so a leaked secret quickly becomes worthless. See
[privileged-accounts-and-credentials.md](../foundations/privileged-accounts-and-credentials.md).

## S

**Secret** — Any sensitive authentication material: password, SSH key, certificate, API
token. Stored in the vault, never on endpoints. See
[privileged-accounts-and-credentials.md](../foundations/privileged-accounts-and-credentials.md).

**Segregation/Separation of Duties (SoD)** — Splitting a sensitive process so no single
person controls all of it (e.g. requester ≠ approver). Governance detects "toxic
combinations". See
[core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

**Session isolation** — The user's workstation never connects directly to the target; the
PAM gateway proxies in between, isolating the two ends so malware can't ride the connection
and the credential never reaches the workstation.

**Session recording** — Capturing a privileged session (video, keystrokes, commands,
metadata) for forensics, dispute resolution and compliance; the basis of non-repudiation.
Recordings should be encrypted and integrity-protected. See
[what-is-pam.md](../foundations/what-is-pam.md).

**Service account** — A non-human account used by an application/service to run or
authenticate; often over-privileged and rarely rotated, hence a prime PAM target.

**Single Sign-On (SSO)** — Authenticate once and reach many trusting apps via federation
(SAML/OIDC). A usability *and* security win (fewer passwords to phish).

**Standing privilege** — Privileged rights held continuously "at rest", available to be
stolen between tasks. JIT/ZSP aim to eliminate standing privilege.

**Sub-protocol** — A granular, authorization-gated capability within a proxied protocol
(e.g. SSH: shell, SCP, SFTP, X11; RDP: clipboard, drive, printer) that a PAM proxy can
allow or block per policy.

## T

**Target** — In a PAM platform, a device + service + target account — i.e. *what* a user
is authorized to reach. The unit authorizations are granted against.

**Target group** — A collection of similar Targets that share authorizations.

**Toxic combination** — A pairing of entitlements that together enable fraud or abuse,
violating SoD (e.g. create a vendor *and* approve its payment); flagged by governance.

## U

**User mapping (account mapping)** — A PAM connection mode where the user reaches the
target with *their own* directory credentials, injected automatically. Contrast with a
vault-stored shared/specific account or a manual interactive login.

## V

**Vaulting** — Storing secrets in an encrypted central vault rather than on endpoints,
scripts or notes. See **Credential vault** and the
[PAM playbook](../certs/ceh/defender-pam/pam-playbook.md).

## Z

**Zero Standing Privileges (ZSP)** — The end-state where no account holds privileged rights
at rest; every privilege is acquired Just-In-Time and disappears afterward. See
[core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

**Zero Trust** — The security model that assumes no implicit trust based on network
location: *"never trust, always verify."* Every access request is authenticated,
authorized and continuously evaluated. A PAM gateway is a practical Zero-Trust enforcement
point for privileged access. See
[core-concepts](../foundations/core-concepts-least-privilege-jit-zero-trust.md).

**Zero Trust Network Access (ZTNA)** — Applying Zero Trust to connectivity: granting
per-session access to *specific* resources after verification, rather than dropping a user
onto the network as a VPN does.

---

## See also

- [Acronyms](acronyms.md) — expansions of every abbreviation used above.
- [Compliance & standards](compliance-and-standards.md) — how PAM maps to regulations.
- [What is PAM?](../foundations/what-is-pam.md)
- [Core concepts: least privilege, JIT, Zero Trust](../foundations/core-concepts-least-privilege-jit-zero-trust.md)
- [Privileged accounts & credentials](../foundations/privileged-accounts-and-credentials.md)
- [PAM threat landscape](../foundations/pam-threat-landscape.md)
- [PAM playbook](../certs/ceh/defender-pam/pam-playbook.md)
- [PAM architecture](../certs/ceh/defender-pam/pam-architecture.md)

---

## Sources

- NIST SP 800-53 Rev. 5 (AC-6 least privilege; AC-5 separation of duties): https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-207 Zero Trust Architecture: https://csrc.nist.gov/pubs/sp/800/207/final
- Gartner — PAM glossary (privileged access, JIT): https://www.gartner.com/en/information-technology/glossary/privileged-access-management-pam
- MITRE ATT&CK — Pass-the-Hash (T1550.002) / Pass-the-Ticket (T1550.003): https://attack.mitre.org/techniques/T1550/
