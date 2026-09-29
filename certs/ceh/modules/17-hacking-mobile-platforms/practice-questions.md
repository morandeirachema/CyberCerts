# Module 17 — Hacking Mobile Platforms · Practice Questions

> **Original, concept-based questions** written to *teach* the testable ideas — not exam dumps (those violate the [EC-Council Candidate Agreement](https://www.eccouncil.org/) and get certs revoked). Answers are collapsed: think first, then expand. Aim for **≥80%** before moving on. Log misses in [PROGRESS.md](../../PROGRESS.md).

Pairs with [facts.md](facts.md) · [flashcards.csv](flashcards.csv) · [README.md](README.md).

---

**Q1.** A user removes the vendor's privilege restrictions on an **iPhone** so unsigned apps can run and the sandbox is broken. What is this called, and what is the equivalent on Android?

- A. Jailbreaking on iOS; rooting on Android
- B. Rooting on iOS; jailbreaking on Android
- C. Sideloading on both
- D. Flashing on iOS; unlocking on Android

<details><summary>Answer</summary>

**A. Jailbreaking (iOS); rooting (Android).** Both defeat the same trust model — they break the app sandbox, disable code-signing/verified boot, and expose Keychain/Keystore material. **Exam tell:** *Jailbreak = iOS, Root = Android.* Because the whole OS trust model is gone, **MDM blocks compromised devices** from corporate data.
</details>

---

**Q2.** Which file format is an **Android** application package, and which is **iOS**?

- A. Android = IPA, iOS = APK
- B. Android = AAB, iOS = APK
- C. Both use APK
- D. Android = APK, iOS = IPA

<details><summary>Answer</summary>

**D. Android = APK (or AAB), iOS = IPA.** Android additionally permits **sideloading** (installing packages from outside the official store), which is the main malware-delivery path; iOS heavily restricts sideloading and requires App Store review. Don't swap the extensions.
</details>

---

**Q3.** During static review you find an auth token written to `/data/data/com.app/shared_prefs/session.xml` in cleartext. Which OWASP Mobile Top 10 (2024) category is this, and where *should* the secret live?

- A. M5 Insecure Communication; in the app's SQLite DB
- B. M7 Insufficient Binary Protections; in the APK resources
- C. M3 Insecure Authentication; in SharedPreferences with a flag
- D. M9 Insecure Data Storage; in the Android Keystore

<details><summary>Answer</summary>

**D. M9 Insecure Data Storage; Android Keystore (Keychain on iOS).** SharedPreferences, plist, SQLite, and logs are all cleartext-readable once you have the file — none is a secret store. The correct home is the hardware-backed **Keystore/Keychain**. Insecure Data Storage is the perennial top mobile flaw.
</details>

---

**Q4.** An app uses HTTPS, but you still read its API calls in Burp after installing your CA on the emulator. The app has **no certificate pinning**. Which category is this and what runtime tool bypasses pinning when it *is* present?

- A. M9 Insecure Data Storage; apktool
- B. M5 Insecure Communication; Frida/Objection
- C. M1 Improper Credential Usage; jadx
- D. M8 Security Misconfiguration; adb

<details><summary>Answer</summary>

**B. M5 Insecure Communication; Frida/Objection.** No pinning means a trusted CA is enough to MITM. When pinning *is* implemented, **Objection** (`android sslpinning disable`) or a **Frida** script hooks the pinning check at runtime so traffic can be read. Know **both** sides: pinning defeats casual MITM, Frida/Objection defeats pinning.
</details>

---

**Q5.** Why does the exam consider **SMS-based MFA** weak compared with app- or hardware-based MFA?

- A. SMS messages are encrypted end-to-end so they can't be logged
- B. SMS OTPs never expire
- C. SIM swapping and OTP interception let an attacker receive the code without the phone
- D. SMS requires rooting the device to read

<details><summary>Answer</summary>

**C.** **SIM swapping** (porting the victim's number) and **OTP interception / smishing** let an attacker receive the one-time code without possessing the device. That's why the exam wants **app-based (TOTP/push)** or, best, **phishing-resistant FIDO2 / passkeys** as the stronger answer.
</details>

---

**Q6.** A company allows personal phones (**BYOD**) but must protect corporate email and files **without** the ability to wipe the employee's personal photos. Which management approach fits best?

- A. MDM with full-device remote wipe
- B. Rooting each device for control
- C. MAM (containerize just the corporate app/data)
- D. Disabling the App Store

<details><summary>Answer</summary>

**C. MAM.** **MDM** manages the **whole device** (and can full-wipe it) — appropriate for corporate-owned hardware. **MAM** manages just the **app/corporate data** via containerization, so IT can wipe *only* the corporate container. For BYOD you pick **MAM** to avoid touching personal data.
</details>

---

**Q7.** You want to read decompiled **Java** source and the `AndroidManifest.xml` of an APK **without running it**. Which is the right tool and analysis type?

- A. Frida — dynamic analysis
- B. Drozer — dynamic analysis
- C. jadx — static analysis
- D. Burp Suite — dynamic analysis

<details><summary>Answer</summary>

**C. jadx — static analysis.** Static = decompile/inspect the package at rest (jadx for Java, apktool for smali/resources, MobSF static). **Dynamic** = run and instrument (Frida/Objection, Drozer, MobSF dynamic). Don't attach a dynamic tool to a "without running it" question.
</details>

---

**Q8.** In an `AndroidManifest.xml` you spot `android:debuggable="true"`, an activity with `exported="true"`, and `android:usesCleartextTraffic="true"`. Which OWASP (2024) category best labels these findings collectively?

- A. M10 Insufficient Cryptography
- B. M8 Security Misconfiguration
- C. M6 Inadequate Privacy Controls
- D. M2 Inadequate Supply Chain Security

<details><summary>Answer</summary>

**B. M8 Security Misconfiguration.** A debuggable production build, needlessly exported components (reachable by other apps), and permitted cleartext traffic are all misconfigurations. (The exported component is also fuel for IPC attacks you'd probe with **Drozer**; cleartext traffic overlaps with M5.)
</details>

---

**Q9.** A game app hardcodes an AES key in its code and encrypts data with **ECB mode** using **MD5** for hashing. Which category is this?

- A. M10 Insufficient Cryptography
- B. M5 Insecure Communication
- C. M9 Insecure Data Storage
- D. M4 Insufficient Input/Output Validation

<details><summary>Answer</summary>

**A. M10 Insufficient Cryptography.** Hardcoded keys, **ECB** mode (leaks patterns), weak/obsolete algorithms (MD5), and home-rolled ciphers are all weak-crypto tells. Contrast with M9 (where the secret is *stored* in cleartext) — here the *cryptography itself* is the weakness.
</details>

---

**Q10.** An attacker downloads a legitimate app, decompiles it, injects a malicious payload, **re-signs** it, and distributes it via a third-party store for users to sideload. What is this, and which control most directly blocks the delivery path?

- A. Jailbreaking; require FIDO2
- B. Repackaged/trojanized app; block sideloading + enforce app integrity (Play Integrity)
- C. Kerberoasting; rotate service keys
- D. SIM swap; number matching

<details><summary>Answer</summary>

**B.** This is a **repackaged (trojanized) app** — an OWASP **M2 Inadequate Supply Chain Security** issue. The delivery path is **sideloading** from an untrusted source, so **blocking sideloading**, using a **managed app catalog**, and enforcing **app-integrity attestation (Play Integrity)** are the direct controls.
</details>

---

**Q11.** On a rooted emulator you run `adb shell run-as com.app cat databases/users.sqlite` and find a plaintext password column. Separately, `adb logcat | grep -i token` leaks a bearer token. What single principle do both violate?

- A. Secrets should be encrypted in transit only
- B. Secrets belong in Keystore/Keychain and must never sit in app storage or logs in cleartext
- C. Apps should never use SQLite
- D. Logs must be disabled entirely in all builds

<details><summary>Answer</summary>

**B.** Both are **Insecure Data Storage (M9)**. SQLite files, SharedPreferences, plist, and **logcat/unified-log** output are all readable once you reach them — sensitive material must live in the hardware-backed **Keystore/Keychain**, and tokens/creds should never be logged.
</details>

---

**Q12.** From a **PAM** perspective, why should a phone that approves admin MFA and holds session tokens be treated as a **privileged endpoint**, and what design keeps it from holding a durable secret?

- A. Because it can silently approve elevation and replay tokens; use JIT so nothing durable is stored on the device
- B. Because phones are cheap; use longer PINs
- C. Because iOS is immune; only Android phones matter
- D. Because SMS is encrypted; rely on it exclusively

<details><summary>Answer</summary>

**A.** A compromised handset can **rubber-stamp MFA (push bombing)** and **replay stolen session tokens**. Treat it like any privileged endpoint: **JIT (just-in-time) elevation** means no durable privileged credential lives on the device, **Remote Access with biometric MFA** replaces SMS OTP, and **number matching** stops fatigue attacks. MDM enrollment with a **rooted/jailbroken block** is the enrollment gate.
</details>

---

**Q13.** Which tool would you reach for to enumerate an Android app's **exported components and IPC attack surface** (content providers, activities, services reachable by other apps)?

- A. jadx
- B. Hashcat
- C. Drozer
- D. Wireshark

<details><summary>Answer</summary>

**C. Drozer.** It probes an app's **exported IPC surface** on a running device — exported activities, services, broadcast receivers, and content providers — which maps to the `exported="true"` misconfig you'd first spot statically in the manifest. jadx is static decompilation; the other two aren't mobile-IPC tools.
</details>

---

**Q14.** You upload an APK to **MobSF** and it flags storage, crypto, network, and permission issues automatically. How does this relate to your manual jadx/apktool review?

- A. MobSF does both static and dynamic analysis and is best used to cross-check/triage what you find (and miss) by hand
- B. MobSF replaces manual review entirely and is always complete
- C. MobSF only decrypts network traffic
- D. MobSF is a device-management (MDM) console

<details><summary>Answer</summary>

**A.** **MobSF** performs **both static and dynamic** analysis and produces an automated report — ideal to **cross-check** manual findings and surface things you missed. It's a triage accelerator, not a substitute for reading the manifest/decompiled code and confirming on-device.
</details>

---

**Q15.** A SOC sees an admin's account approve a privileged action via **repeated push prompts at 3 a.m.**, several denied then one approved. Which attack is this, and which control most directly stops it?

- A. Kerberoasting; gMSA
- B. Insecure storage; remote wipe
- C. SIM swap; full-disk encryption
- D. MFA fatigue / push bombing; number matching + MFA rate-limits

<details><summary>Answer</summary>

**D. MFA fatigue (push bombing).** The attacker spams push approvals hoping the user taps *Approve*. **Number matching** (the user must type a code shown on the login screen), **rate-limits**, and **JIT approval workflows** neutralize it. FIDO2/passkeys remove the pushable prompt altogether.
</details>

---

### Score yourself
- **13–15:** solid — move on, revisit missed items in [facts.md](facts.md).
- **10–12:** re-read the OWASP Mobile Top 10 and app-flaw quartet sections.
- **< 10:** re-read [README.md](README.md) fully and redo the [lab-walkthrough.md](lab-walkthrough.md).
