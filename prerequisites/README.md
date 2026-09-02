# Prerequisites — the sysadmin → cyber skill bridge

PAM sits on top of the infrastructure you already know. These pages refresh the systems,
networking, and cryptography fundamentals that any PAM platform brokers and integrates with —
each tied explicitly to *how a PAM platform uses it*.

| Page | Covers | Where PAM uses it |
|------|--------|-------------------|
| [Linux essentials for PAM](linux-essentials-for-pam.md) | SSH, sudo/su, users/permissions, systemd, logs — and the Linux "PAM" name clash | Linux-based appliances, the SSH proxy, target-side hardening |
| [Linux CLI deep dive for PAM engineers](linux-cli-for-pam-engineers.md) | Logs, services & ports, REST API via curl/jq, network/crypto helpers, cron & scripting | Troubleshooting, automation, and high availability at the shell |
| [Windows & Active Directory](windows-and-active-directory.md) | AD objects, GPO, RDP, NTLM vs Kerberos, privileged groups, LAPS, tiered admin | AD/LDAP integration, the RDP proxy, Kerberos auth, tier models |
| [Networking & protocols](networking-and-protocols.md) | SSH/RDP/VNC/LDAP/RADIUS/Kerberos/SAML/OIDC/SCIM/Syslog with ports & flows | Every protocol a PAM platform proxies or authenticates with |
| [Cryptography & PKI](cryptography-and-pki.md) | Symmetric/asymmetric, hashing, TLS, PKI/X.509, SSH keys, TOTP/FIDO2 | Vault encryption at rest, certificate auth, key rotation, MFA |

➡️ Next: the [protocols](../protocols/README.md) for the full mechanisms, then the
**[CEH hub](../certs/ceh/README.md)** — the first certification on the
[roadmap](../learning/roadmap.md).

> 🔌 **Want the full mechanism?** See **[protocols/](../protocols/README.md)** for
> step-by-step, RFC-grounded explanations of **Kerberos, RADIUS, Active Directory, LDAP,
> TLS, SSH, SAML and OIDC** — message flows, what's encrypted and how, with Mermaid sequence diagrams.

> 🔁 **Same fundamentals, offensive angle:** the [CEH hub](../certs/ceh/README.md) covers this
> ground from an attacker's perspective — e.g. [cryptography](../certs/ceh/domains/20-cryptography.md),
> [scanning & networking](../certs/ceh/domains/03-scanning-networks.md),
> [Windows/AD attacks](../certs/ceh/domains/06-system-hacking.md) — and its
> [Kali course](../certs/ceh/kali/README.md) teaches the tooling from zero. They're complementary, not duplicated.
