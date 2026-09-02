# Lab Network Topology

Everything lives on an isolated host-only / internal network. The Docker web targets are reachable only via `localhost` published ports on your workstation; the VMs share a private VirtualBox host-only network.

```mermaid
flowchart TB
    subgraph WS["YOUR WORKSTATION - host"]
        subgraph DOCKER["Docker bridge - published<br/>to localhost only"]
            DVWA["DVWA :8081"]
            JUICE["Juice Shop :8082"]
            WEBGOAT["WebGoat :8083"]
            BWAPP["bWAPP :8084"]
        end
        subgraph VBOX["VirtualBox host-only<br/>network 192.168.56.0/24"]
            KALI["Kali attacker<br/>192.168.56.10"]
            META["Metasploitable2 target<br/>192.168.56.20"]
            DC["Windows DC - AD/PAM lab<br/>192.168.56.30 dc01"]
            WS01["Windows member ws01<br/>192.168.56.31"]
            KALI --> META
            KALI --> DC
        end
        NOTE["✗ NO route to internet /<br/>home LAN from lab segment"]
    end
```

## IP / port plan

| Host | Address | Role | Access |
|---|---|---|---|
| Workstation | host-only gateway (typically 192.168.56.1) | Runs Docker + hypervisor | — |
| DVWA | localhost:8081 | Web target | Browser |
| Juice Shop | localhost:8082 | Web target | Browser |
| WebGoat | localhost:8083 (+ WebWolf :9090) | Web target | Browser |
| bWAPP | localhost:8084 | Web target | Browser |
| Kali | 192.168.56.10 | Attacker | `vagrant ssh kali` |
| Metasploitable2 | 192.168.56.20 | Linux target | From Kali |
| dc01 | 192.168.56.30 | Windows Domain Controller | From Kali |
| ws01 | 192.168.56.31 | Windows domain member | From Kali |

## AD domain design (PAM-flavored)

```mermaid
flowchart TD
    D["Domain ceh.lab — NetBIOS CEH"]
    T0["OU=Tier0 — Domain Admins, DC<br/>admins, PKI, PAM vault admins<br/>— never log on to lower tiers"]
    T1["OU=Tier1 — server admins<br/>— member servers, DBs"]
    T2["OU=Tier2 — workstation<br/>admins / helpdesk"]
    U["OU=Users — standard users"]
    PU["Group Protected Users —<br/>high-value accounts — blocks<br/>NTLM/delegation cred caching"]
    ACC["Accounts — jump/PAM break-glass<br/>accounts, LAPS-managed local admin"]
    D --> T0
    D --> T1
    D --> T2
    D --> U
    D --> PU
    D --> ACC
```

The AD lab intentionally models the controls a PAM/sysadmin runs so you can both **attack** it (enumeration, Kerberoasting, credential access) and **see the control working** (tiering blocks lateral movement, Protected Users limits cred theft). Attack↔control mapping lives in [`../defender-pam/`](../defender-pam/README.md).
