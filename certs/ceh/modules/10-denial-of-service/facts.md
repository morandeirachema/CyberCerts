# Module 10 — Denial-of-Service · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The one-line definition
DoS attacks deny **availability** — the "A" in the CIA triad — by exhausting one of three resources: **bandwidth**, **connection state**, or **application capacity**. The whole module is really one table (below) plus the named classics.

## DoS vs. DDoS vs. DRDoS
| Term | Sources | Why it matters |
|---|---|---|
| **DoS** | Single source | Can be blocked by one IP/rule |
| **DDoS** | Many sources (botnet) | Distributed → **can't** just block one IP |
| **DRDoS** | Reflectors (spoofed source IP) | True origin hidden behind reflectors |
| **Botnet** | Compromised hosts + **C2** | Bot herder → **handlers** → **agents/zombies** (e.g. Mirai IoT) |
| **PDoS / phlashing** | — | *Permanent* DoS: brick firmware/hardware ("BrickerBot") |

Botnet chain: **bot herder → handlers (C2) → agents (zombies)**. Blocking a single IP fails against DDoS because traffic comes from thousands of hosts.

## The three categories (the core exam table)
| Category | Exhausts | Measured in | Example attacks |
|---|---|---|---|
| **Volumetric** | Link bandwidth | bits/sec (bps) | UDP flood, ICMP flood, **DNS/NTP/memcached/SSDP amplification** |
| **Protocol / state** | Connection tables, OS/gear state | packets/sec (pps) | **SYN flood**, Ping of Death, Teardrop, Smurf, fragmentation |
| **Application-layer (L7)** | CPU/RAM/threads/DB | requests/sec (rps) | **Slowloris**, HTTP GET/POST flood, Slow POST (R-U-Dead-Yet) |

Rule of thumb: **volumetric = fill the pipe**, **protocol = fill the table**, **application = tie up the app**.

## Named classic attacks (know the mechanism)
- **SYN flood** (protocol/L4): send SYNs, never complete the handshake → **half-open** connections pile up and exhaust the backlog. Defeated by **SYN cookies**.
- **UDP flood** (volumetric): blast UDP to random ports; host replies ICMP port-unreachable, both directions burn bandwidth.
- **ICMP flood** (volumetric): ping flood saturating the link.
- **Smurf** (volumetric reflect): spoofed **ICMP** echo to a **broadcast** address → every host replies to the victim. Dead (directed broadcast disabled).
- **Fraggle** (volumetric reflect): Smurf but with **UDP** (echo/chargen) to broadcast. Dead.
- **Ping of Death** (protocol): oversized/fragmented ICMP **> 65,535 bytes** crashes the stack. Patched.
- **Teardrop** (protocol): overlapping IP **fragment offsets** crash reassembly. Patched.
- **Slowloris** (L7): opens many connections, sends **partial HTTP headers slowly**, holds sockets open — wins with **almost no bandwidth**. Beaten by connection/time limits + reverse proxy.
- **HTTP flood** (L7): flood of *valid* GET/POST — hard to tell from real users. WAF, rate limit, CAPTCHA.

## Amplification & reflection (DRDoS)
**Reflection** = spoof the *victim's* IP as source, send small queries to open servers → replies land on the victim. **Amplification** = pick a protocol whose *reply is much larger than the request*. Both **require UDP** (connectionless, no handshake, so the source can be spoofed) and **source-IP spoofing**.

**Amplification factor** = response size ÷ request size. A ~60-byte spoofed query that triggers a multi-kilobyte reply gives one attacker the firepower of a much larger link.

| Protocol | Trigger | Approx factor* |
|---|---|---|
| **memcached** | UDP **:11211** stats/get | ~10,000–51,000× (record-setting) |
| **NTP** | `monlist` command | ~500× |
| **CLDAP** | connectionless LDAP | ~50–70× |
| **DNS** | ANY / large TXT | ~28–54× |
| **SSDP** | UPnP discovery | ~30× |

\*Memorize the **ranking** (memcached ≫ NTP ≫ CLDAP/DNS ≫ SSDP), not exact numbers. NTP's trigger word is **`monlist`**; memcached is UDP **:11211**.

## Tools (recognition)
| Tool | Purpose |
|---|---|
| **hping3** | Crafted TCP/UDP/ICMP packets — SYN floods, custom flags, `--flood`, `--rand-source` (lab testing) |
| **Slowloris** (script) | Low-bandwidth L7 connection-exhaustion PoC |
| **LOIC / HOIC** | *Name-recognition only* — historic volumetric stress cannons (do not deploy) |

## Countermeasures (match to the attack)
- **SYN flood → SYN cookies** (validate the handshake **without enlarging the backlog**), connection rate limiting, upstream filtering.
- **Volumetric flood → upstream scrubbing / CDN / anycast**, ingress ACLs, RTBH/sinkhole — you *cannot* absorb a botnet at the host.
- **Amplification/reflection → BCP38 anti-spoofing (uRPF)** at the edge, close/patch open reflectors, disable NTP `monlist` & memcached UDP, response-rate limiting.
- **Application-layer (Slowloris/HTTP flood) → reverse proxy + connection/time-outs**, WAF, per-IP request limits, CAPTCHA.
- **DDoS volumetric → autoscaling / cloud scrubbing** to add capacity faster than the attacker.

## The PAM angle (why availability is a privileged-access problem)
DoS is an *availability* attack, so the PAM question is: **can you still administer and recover while the service is under fire?**
- **Out-of-band admin plane** — separate management network/VLAN so a saturated data-plane never starves SSH/RDP/console.
- **Harden/protect jump hosts & PAM proxies** — single points that must survive; give them QoS priority and no exposure to the flooded segment.
- **Vault HA / DR** — clustered + disaster-recovery + distributed (satellite) vaults so a DoS on the PAM control plane doesn't lock everyone out.
- **Load-balanced PSM farm** — the session broker must not be a single bottleneck/SPOF.
- **Break-glass access** — documented, sealed, dual-control, monitored emergency path that still works when normal auth infrastructure is degraded; alert on any retrieval.

Mapping lives in [`../../defender-pam/`](../../defender-pam/).

## Top traps
- **Match attack → category** — SYN flood = **protocol/state**; UDP/ICMP/amplification = **volumetric**; Slowloris/HTTP flood = **application-layer**. This mapping is the single most-tested thing.
- **Slowloris is *low-bandwidth*** — "minimal bandwidth" or "incomplete/partial HTTP headers" ⇒ Slowloris, not a flood.
- **Smurf vs. Fraggle:** Smurf = **ICMP** to broadcast; Fraggle = **UDP** (echo/chargen) to broadcast.
- **Ping of Death vs. Teardrop:** PoD = **oversized** ping (>65,535 bytes); Teardrop = **overlapping fragment offsets**. Both legacy/patched.
- **Amplification needs UDP + spoofing** — TCP's handshake defeats source spoofing, so reflection uses connectionless UDP protocols.
- **DDoS can't be stopped by blocking one IP** (many sources); **DRDoS** hides the origin behind reflectors — fix is **BCP38/uRPF**.
- **SYN cookies** defend SYN floods **without enlarging the backlog** — that's the mechanism they want.
- **PDoS/phlashing = permanent** (bricking), not a temporary outage.
