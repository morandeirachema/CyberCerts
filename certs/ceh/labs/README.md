# CEH Lab Environment (self-hosted)

A runnable practice range you fully control. Three layers:

| Layer | Tooling | What it gives you | Modules it serves |
|---|---|---|---|
| **Web targets** | Docker Compose ([`docker-compose.yml`](docker-compose.yml)) | DVWA, OWASP Juice Shop, WebGoat, bWAPP | 13, 14, 15 (web + SQLi) |
| **Network targets** | Vagrant ([`vagrant/`](vagrant/)) | Kali attacker + Metasploitable2 | 02–08, 10–12 |
| **AD / PAM lab** | Ansible ([`ansible/`](ansible/)) | Windows DC + ADCS with a tiered-admin (PAM) model and planted attack paths | 04, 06, 08, defender mappings |
| **Capstone chain** | [`capstone.md`](capstone.md) | Full recon→Kerberoast→delegation→ADCS→DCSync→cover-tracks engagement | all AD modules |
| **Blue-team lab** | [`blue-team-lab.md`](blue-team-lab.md) | Run the capstone attacks, then **detect** each in Sysmon/logs with Sigma | defender-pam, detection |

> 🔒 **This lab is isolated on purpose.** These images are *deliberately vulnerable*. Keep them on a host-only / internal network, never bridge them to the internet or your production LAN, and never expose the published ports beyond localhost. See [`topology.md`](topology.md).

---

## Prerequisites

- A machine with virtualization enabled (8 GB RAM minimum, 16 GB comfortable; ~60 GB disk).
- **Docker + Docker Compose v2** — https://docs.docker.com/engine/install/
- **VirtualBox** — https://www.virtualbox.org/wiki/Downloads (or libvirt/VMware if you adapt the Vagrantfile)
- **Vagrant** — https://developer.hashicorp.com/vagrant/downloads
- **Ansible** (for the AD lab, run from Kali or your host) — https://docs.ansible.com/ansible/latest/installation_guide/

Check versions:

```bash
docker --version && docker compose version
vagrant --version && vboxmanage --version
ansible --version
```

---

## 1. Web targets (Docker) — fastest to start

```bash
cd labs
cp .env.example .env          # optional: change ports/passwords
docker compose up -d
docker compose ps             # confirm all healthy
```

| Target | URL | Default creds | Notes |
|---|---|---|---|
| DVWA | http://localhost:8081 | admin / password | Set DVWA Security to "low" first, then climb |
| Juice Shop | http://localhost:8082 | self-register | Modern SPA; find the score board |
| WebGoat | http://localhost:8083/WebGoat | self-register | Lessons + WebWolf on :9090 |
| bWAPP | http://localhost:8084 | bee / bug | Install page first: `/install.php` |

Tear down (keeps images): `docker compose down`
Tear down + wipe data: `docker compose down -v`

## 2. Network targets (Vagrant)

```bash
cd labs/vagrant
vagrant up                    # brings up kali + metasploitable2
vagrant ssh kali              # drop into the attacker box
```

- Kali attacker: **192.168.56.10**
- Metasploitable2: **192.168.56.20** (creds: `msfadmin` / `msfadmin`)

See [`vagrant/README.md`](vagrant/README.md) for the Metasploitable image source and alternatives.

## 3. AD / PAM lab (Ansible)

A Windows Server Domain Controller configured with a **tiered administration model** (Tier 0/1/2), Protected Users, dedicated PAM/jump accounts, **and ADCS** — the exact structure you defend, used here as a realistic target. It plants **deliberate attack paths** so you can practice what the docs teach and then apply the fix:

| Planted weakness | Practice | The fix (also in the lab) |
|---|---|---|
| `svc-sql` with a weak SPN password | Kerberoasting | `gmsa-web` gMSA (roast-proof) |
| `ws01` trusted for unconstrained delegation | TGT capture | remove flag + Protected Users |
| `jdoe` has `GenericWrite` on `ws01` | RBCD delegation abuse | least-privilege on computer writes |
| Vulnerable **ESC1** certificate template | ADCS → domain admin | template/CA hardening (Certipy audit) |
| — | Pass-the-Hash lateral movement | **Windows LAPS** (unique local admin) |

See [`ansible/README.md`](ansible/README.md) — it requires Windows evaluation VMs you provide, then:

```bash
cd labs/ansible
ansible-galaxy collection install microsoft.ad ansible.windows community.windows
ansible-playbook -i inventory.ini ad-lab.yml
```

## 4. Capstone — chain it all together

Once the AD lab is up, run the **[capstone.md](capstone.md)** engagement: a single attack chain (recon → enumeration → Kerberoast → RBCD delegation → ADCS ESC1 → DCSync → covering tracks), each stage paired with the PAM control that stops it. Run it once to win, once with the fixes applied to get stopped — that contrast is the learning.

---

## Reset / rebuild

```bash
labs/scripts/reset.sh         # stops docker, wipes volumes, halts vagrant
```

## Safety checklist before every session

- [ ] Lab is on host-only / internal network (no bridge to home/work LAN)
- [ ] No published port is reachable from outside localhost
- [ ] You are only attacking the lab targets above
- [ ] Loot/captures go to git-ignored folders (see repo `.gitignore`)
