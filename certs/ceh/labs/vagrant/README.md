# Vagrant network range

Brings up the **Kali attacker** and a **Linux target** on the host-only network `192.168.56.0/24`.

## Kali attacker

- Box: `kalilinux/rolling` — official, published on HashiCorp Vagrant registry: https://portal.cloud.hashicorp.com/vagrant/discover/kalilinux/rolling
- IP: `192.168.56.10`
- Provisioner installs the core toolset (nmap, metasploit, hydra, john, sqlmap, responder, etc.).

## Metasploitable target — choose one

Metasploitable2 is **not** shipped as an official Vagrant box; it's a VMDK/OVA. Options:

| Option | How | Pros / cons |
|---|---|---|
| **A. metasploitable3 via Vagrant** | The Vagrantfile references `rapid7/metasploitable3-ub1404`. Confirm the box exists first: `vagrant box add rapid7/metasploitable3-ub1404`. | Automated; but metasploitable3 usually expects a local build. Verify availability. |
| **B. Import Metasploitable2 OVA/VMDK manually** | Download from Rapid7/SourceForge, import into VirtualBox, add a host-only adapter, set IP `192.168.56.20`. Comment out the `metasploitable` stanza in the Vagrantfile. | Fully offline, canonical target. Manual. |
| **C. Docker** | `docker run --rm -it tleemcjr/metasploitable2` (limited services). | Quick, but not a full VM. |

Official Metasploitable references:
- Rapid7 Metasploitable 2 docs — https://docs.rapid7.com/metasploit/metasploitable-2/
- Metasploitable download (SourceForge) — https://sourceforge.net/projects/metasploitable/
- Metasploitable3 project — https://github.com/rapid7/metasploitable3

Default Metasploitable2 credentials: `msfadmin` / `msfadmin`.

## Verify connectivity from Kali

```bash
vagrant ssh kali
ping -c1 192.168.56.20          # target reachable
nmap -sn 192.168.56.0/24        # who's on the segment
```

## Common commands

```bash
vagrant up kali                 # start just Kali
vagrant status                  # what's running
vagrant reload --provision      # re-run provisioners
vagrant halt                    # stop all
vagrant destroy -f              # remove all
```
