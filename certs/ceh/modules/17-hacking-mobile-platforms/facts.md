# Module 17 — Hacking Mobile Platforms · Must-Know Facts

> One-page, high-yield recall sheet. If you can reproduce this from memory, you own the module. Pairs with [README.md](README.md) · [practice-questions.md](practice-questions.md) · [flashcards.csv](flashcards.csv) · [lab-walkthrough.md](lab-walkthrough.md).

## The one-line hook
Phones are **unmanaged endpoints holding session tokens and MFA approvals** — treat a phone that reaches admin systems as a **privileged endpoint**. Findings cluster into two buckets: **secrets on the device** and **traffic off the device**.

## Android vs iOS — architecture & security model
| | Android | iOS |
|---|---|---|
| Base | Modified Linux kernel | Darwin (XNU) |
| Runtime | ART (AOT/JIT) | Native (Objective-C / Swift) |
| App package | **APK** (or AAB) | **IPA** |
| Store / install | Open + **sideloading** allowed | Closed, App Store review; sideloading restricted |
| Privilege bypass | **Rooting** | **Jailbreaking** |
| Isolation | App sandbox, **UID per app**, permissions | App sandbox, code signing, Data Protection classes |
| Hardware secret store | **Android Keystore** (TEE/StrongBox) | **Keychain** + Secure Enclave |

Shared model: **app sandbox** isolates apps, **code signing** ensures only trusted code runs, and each app gets a private data directory other apps can't read — until the device is rooted/jailbroken.

## OWASP Mobile Top 10 (2024) — the exam list
| # | Category |
|---|---|
| M1 | Improper Credential Usage |
| M2 | Inadequate Supply Chain Security |
| M3 | Insecure Authentication / Authorization |
| M4 | Insufficient Input/Output Validation |
| M5 | Insecure Communication |
| M6 | Inadequate Privacy Controls |
| M7 | Insufficient Binary Protections |
| M8 | Security Misconfiguration |
| M9 | Insecure Data Storage |
| M10 | Insufficient Cryptography |

> The older **2016** list (M1 Improper Platform Usage, M2 Insecure Data Storage, M3 Insecure Communication, …) still appears in question banks — recognize both, but favor the 2024 categories above.

## Rooting (Android) vs. jailbreaking (iOS)
Both **remove the vendor's privilege restrictions** and break the OS trust model:
- **Break the sandbox / gain root** → any app can read another app's private storage.
- **Disable code-signing / verified boot** → unsigned or tampered apps run.
- **Expose Keystore/Keychain material** to extraction.

That's why **MDM blocks rooted/jailbroken devices** from enrolling or reaching corporate data — attestation (**Play Integrity** on Android, device checks on iOS) is the signal.

## The app-flaw quartet you'll be tested on
| Flaw | What it looks like | OWASP (2024) |
|---|---|---|
| **Insecure storage** | Secrets in SharedPreferences / plist / SQLite / logs in cleartext | M9 |
| **Insecure comms** | No TLS / **no cert pinning** → MITM reads traffic | M5 |
| **Weak auth** | Client-side auth, guessable tokens, no server-side check | M3 |
| **Weak crypto** | Hardcoded keys, ECB mode, MD5, home-rolled ciphers | M10 |

## Where sensitive data hides on the device
| Android | iOS |
|---|---|
| `/data/data/<pkg>/shared_prefs/*.xml` | `Library/Preferences/*.plist` |
| `/data/data/<pkg>/databases/*.sqlite` | app sandbox `Documents/`, SQLite |
| **Logcat** leakage | **Unified logging** leakage |
| **Android Keystore** = correct place | **Keychain** = correct place |

**Rule:** secrets belong in **Keystore / Keychain**, *never* in SharedPreferences / plist / SQLite / logs.

## Mobile malware & supply-chain risk
- **Repackaged / trojanized apps**: attacker decompiles a legit app, injects a payload, re-signs, and distributes via **sideloading** or a fake store.
- **Sideloading** (installing from outside the official store) is the main delivery path for Android malware; iOS restricts it heavily.
- Watch for **over-broad permissions** and unknown install sources (M2 Supply Chain).

## Mobile-relevant identity attacks
- **Smishing** = SMS phishing; **SIM swapping** = port the victim's number to steal SMS OTP; **OTP interception**.
- These are why **SMS-based MFA is weak** — app-based (TOTP/push) is better, **FIDO2 / passkeys (phishing-resistant)** is best.
- **MFA fatigue / push bombing**: spam push prompts until the user taps *Approve*. Countered by **number matching** and rate-limits.

## Device management — MDM vs MAM vs UEM
| Term | Manages | Use it for |
|---|---|---|
| **MDM** | The **whole device** (enroll, policy, remote wipe) | Corporate-owned devices |
| **MAM** | Just the **app / corporate data** (containerization) | **BYOD** — don't wipe the user's personal device |
| **UEM** | Unified endpoint mgmt (phones + laptops + IoT) | Single console across endpoint types |

Core MDM/MAM controls: **block rooted/jailbroken**, require encryption, screen-lock policy, **remote wipe**, containerize corporate data, block sideloading, enforce transport security.

## Tools — static vs dynamic
| Tool | Purpose | Static / Dynamic |
|---|---|---|
| **MobSF** | Automated mobile app analysis + report | Both |
| **adb** | Device shell, pull/install, logcat | Dynamic (device I/O) |
| **apktool** | Decode/rebuild APK resources & smali | Static |
| **jadx** | APK → readable Java | Static |
| **Frida / Objection** | Runtime instrumentation, **SSL-pinning bypass** | Dynamic |
| **Drozer** | Android IPC / attack-surface (exported components) | Dynamic |

**Static** = decompile & inspect (jadx, apktool, MobSF static). **Dynamic** = run & instrument (Frida/Objection, Drozer, MobSF dynamic).

## PAM angle (treat the phone as a privileged endpoint)
- A phone that approves MFA and holds session tokens **is** a privileged endpoint — broker its access.
- **Remote Access with mobile biometric MFA** instead of SMS OTP (VPN-less, phishing-resistant).
- **JIT (just-in-time)** elevation → the device never holds a **durable** privileged secret; a stolen token/SMS is worthless after the window closes.
- Require **MDM enrollment with a rooted/jailbroken block**; containerize corporate data with **MAM**; keep privileged approvals behind a **number-matching / JIT** workflow so a compromised handset can't silently rubber-stamp elevation.

## Top traps
- **Rooting = Android, Jailbreaking = iOS.** Both defeat the sandbox / code-signing trust model.
- **APK = Android, IPA = iOS.** Android allows **sideloading**; iOS is far more locked down.
- **Insecure Data Storage (M9)** is the perennial top mobile flaw — Keystore/Keychain is the *correct* home, not SharedPreferences/plist/logs.
- **Cert pinning** defeats casual MITM; **Frida/Objection** bypass it at runtime — know **both** sides.
- **SMS-based MFA is weak** (SIM swap, OTP intercept) — exam wants **app / hardware / FIDO2** as the stronger answer.
- **MDM** = whole device; **MAM** = just the app/data. Pick **MAM for BYOD** (don't wipe personal devices).
- **Static** (jadx/apktool) ≠ **dynamic** (Frida/Objection) — don't swap the tool to the wrong phase.
- 2024 M1 = **Improper Credential Usage** (2016 M1 was *Improper Platform Usage*) — don't confuse the two lists.
