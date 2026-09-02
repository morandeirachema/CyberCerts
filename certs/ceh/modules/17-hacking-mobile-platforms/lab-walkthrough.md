# Module 17 — Hacking Mobile Platforms · Guided Lab Walkthrough

> A step-by-step, **do-it-in-order** lab against **your own** environment only. Use an **Android emulator** (Android Studio AVD / Genymotion) or a **device you own**, and a **deliberately-vulnerable training app you build or download** for learning (e.g. an intentionally-broken "DIVA"-style app or one you write). **Never** decompile, tamper with, or MITM an app or account that isn't yours — that is illegal and violates the [EC-Council Candidate Agreement](https://www.eccouncil.org/). Outputs shown are **representative** — yours will differ. See [`../../labs/`](../../labs/).

**Goal:** walk the mobile app-attack chain — **static triage → secrets on the device → traffic off the device** — then *watch an MDM/MAM + PAM control turn each win into a loss.*

**Setup:** an Android emulator running, `adb devices` shows it, and `jadx`, `apktool`, and Burp Suite are installed. A vulnerable training APK named `vuln.apk` is on your Kali/host box.

**Prereqs (host):**
```bash
adb devices                 # your emulator/device is listed as "device"
which jadx apktool          # static tools present
# Burp Suite running with its CA exportable; MobSF optional (docker or local)
```

---

## Part A — Static triage (decompile & read the package)

### A1. Decompile the APK to Java and to smali/resources
```bash
jadx -d out_jadx vuln.apk                 # readable Java + resources
apktool d vuln.apk -o out_apktool          # smali + decoded AndroidManifest.xml
```
**You should see** both trees populate, including `out_apktool/AndroidManifest.xml` and `out_jadx/sources/`:
```
INFO: Using Apktool 2.x on vuln.apk
I: Decoding AndroidManifest.xml with resources...
I: Baksmaling classes.dex...
```
**Observe:** static analysis needs **no device** — you are reading the app at rest. jadx gives you readable Java; apktool gives you the *authoritative* decoded manifest.

<details><summary>Hint if jadx throws decompile errors</summary>Partial decompilation is normal on obfuscated apps — jadx still emits most classes. If a class fails, read its smali under `out_apktool/smali/` instead. Confirm the file is really an APK with `file vuln.apk` (should say "Android package").</details>

### A2. Read the manifest for the classic misconfigurations
```bash
grep -Ei 'debuggable|exported=|cleartextTraffic|usesCleartextTraffic' out_apktool/AndroidManifest.xml
```
**You should see** one or more red flags on a vulnerable app:
```
android:debuggable="true"
<activity android:name=".AdminActivity" android:exported="true">
android:usesCleartextTraffic="true"
```
**Observe:** `debuggable=true` (should never ship in prod), `exported=true` (component reachable by other apps — IPC surface), and cleartext traffic permitted — all **M8 Security Misconfiguration** (cleartext also feeds **M5**).

<details><summary>Hint: no matches?</summary>Some apps set cleartext via a `networkSecurityConfig` XML instead of the attribute. Open `res/xml/network_security_config.xml` and look for `<domain-config cleartextTrafficPermitted="true">`.</details>

### A3. Grep the decompiled source for hardcoded secrets
```bash
grep -riE "http://|password|api[_-]?key|secret|BEGIN (RSA|PRIVATE) KEY|AES" out_jadx/sources/ | head
```
**You should see** hardcoded material a real app should never embed:
```
LoginActivity.java:  String API_KEY = "AIzaSyD...hardcoded...";
CryptoUtil.java:     private static final String KEY = "0123456789abcdef";  // AES key in code
NetworkClient.java:  BASE_URL = "http://api.vuln.local/v1/";
```
**Observe:** a hardcoded AES key is **M10 Insufficient Cryptography**; an embedded API key/credential is **M1 Improper Credential Usage**; the `http://` base URL is **M5**.

**Defender/PAM view:** these are caught pre-release by **static scanning in CI** (MobSF/MASTG checks). From a PAM lens, an embedded API key is a **credential that should never live on the endpoint** — it belongs in a vaulted secret fetched **JIT**, not compiled into the binary.

---

## Part B — Secrets on the device (Insecure Data Storage, M9)

### B1. Install the app and exercise the login on the emulator
```bash
adb install vuln.apk
adb shell monkey -p com.vuln.app -c android.intent.category.LAUNCHER 1
# now log in inside the app with a test account you created (e.g. tester / Test1234)
```
**You should see** the app installed and running, and your login succeed:
```
Success
Performing Streamed Install
```
**Observe:** the app has now written its session state somewhere on disk — that's what you go find next.

### B2. Pull the app's private storage and read it
```bash
# works when the app is debuggable (run-as) or the device/emulator is rooted
adb shell run-as com.vuln.app cat shared_prefs/user_session.xml
adb shell run-as com.vuln.app ls databases/
adb exec-out run-as com.vuln.app cat databases/users.db > users.db
sqlite3 users.db "select * from users;"
```
**You should see** a cleartext token in prefs and/or a plaintext password column:
```
<string name="auth_token">eyJhbGciOiJIUzI1NiIsInR5cCI6...</string>
1|tester|Test1234|eyJhbGci...   <-- password stored in cleartext
```
**Observe:** the session token and password sit in **SharedPreferences / SQLite in cleartext** — classic **M9 Insecure Data Storage**. They should have been stored in the **Android Keystore** (Keychain on iOS), not readable files.

<details><summary>Hint: run-as denied?</summary>`run-as` only works if the app is `debuggable="true"` (you confirmed this in A2). On a non-debuggable app use a **rooted emulator** and `adb root` then `adb shell cat /data/data/com.vuln.app/shared_prefs/*.xml`. Never do this to an app that isn't your training target.</details>

### B3. Confirm log leakage
```bash
adb logcat -d | grep -iE "token|password|Authorization"
```
**You should see** the app helpfully logging secrets:
```
D/AuthDebug: sending Authorization: Bearer eyJhbGci...
```
**Observe:** secrets in **logcat** are readable by anything with log access — another face of M9.

**Defender/PAM view:** the corporate fix isn't per-app patching — it's **MAM containerization** (corporate data encrypted in a managed container, no run-as), **no secrets in logs**, and using the **Keystore/Keychain**. For privileged users, **JIT tokens** mean any token skimmed off the device is short-lived and useless after the window closes.

---

## Part C — Traffic off the device (MITM + SSL-pinning bypass, M5)

### C1. Route emulator traffic through Burp and read the API
Set the emulator proxy to your host's Burp listener and install Burp's CA as a user cert, then use the app.
```bash
# push Burp's exported CA (DER) — user store; then use the app and watch Burp's HTTP history
adb push burp_ca.der /sdcard/burp_ca.der
# emulator: Settings > Wi-Fi > proxy = <host-ip>:8080 ; then Security > install CA cert
```
**You should see** the app's API calls appear in Burp when there is **no pinning**:
```
POST http://api.vuln.local/v1/login   200
{"user":"tester","token":"eyJhbGci..."}
```
**Observe:** with a trusted CA and no pinning, you read (and can tamper with) every request — **M5 Insecure Communication**.

<details><summary>Hint: HTTPS calls not showing?</summary>Two causes: (1) on Android 7+ apps ignore **user** CAs unless the app opts in — test apps usually do, or use a rooted emulator to place the CA in the **system** store; (2) the app uses **certificate pinning** and drops the connection — that's Part C2.</details>

### C2. Bypass certificate pinning with Objection/Frida
When the app pins and C1 shows connection failures, disable pinning at runtime.
```bash
# frida-server running on the emulator; then:
objection -g com.vuln.app explore
# inside the objection REPL:
android sslpinning disable
```
**You should see** Objection hook the pinning routines, after which the traffic reappears in Burp:
```
(agent) Custom, or modified SSL Pinning method found. Overriding.
(agent) [OkHttp] Bypassing OkHTTP pinner
```
**Observe:** pinning defeats *casual* MITM, but a **runtime instrumentation** framework (Frida/Objection) hooks the check on a device you control. Know **both** sides — this is the exam's favorite mobile pairing.

<details><summary>Hint: objection can't attach?</summary>Confirm the matching `frida-server` is running on the emulator (`adb shell "/data/local/tmp/frida-server &"`) and that `frida-ps -U` lists the app. Version-match the Frida client and server.</details>

### C3. (Optional) Cross-check with a MobSF report
```bash
# MobSF web UI (local/docker): upload vuln.apk → run static, then dynamic
```
**You should see** MobSF auto-flag the same issues you found by hand — cleartext traffic, hardcoded secrets, insecure storage, weak crypto, exported components — with a severity score.
**Observe:** MobSF is a **triage accelerator** that does **both static and dynamic** analysis; use it to catch what you missed, not to replace reading the code.

**Defender/PAM view:** the durable controls are **TLS + certificate pinning + a network-security-config**, **MDM conditional access** that **blocks rooted/jailbroken** (so Frida can't run on a managed device), and **phishing-resistant MFA (FIDO2/passkeys)** so a skimmed token or SMS OTP isn't enough. Full mapping in [`../../defender-pam/attack-to-control-matrix.md`](../../defender-pam/attack-to-control-matrix.md).

---

## What you should conclude
Every "win" above has a specific control that turns it into a logged, contained "loss":

| You did | The control that stops it |
|---|---|
| Decompiled the app, found hardcoded secrets (A) | No secrets in the binary; vaulted/JIT credentials; static scanning in CI |
| Read cleartext token/password from prefs & SQLite (B) | Keystore/Keychain, MAM containerization, no secrets in logs |
| MITM'd the API, bypassed pinning with Frida (C) | TLS + cert pinning + net-security-config; **MDM block on rooted/jailbroken** |
| Replayed a stolen session token | **JIT** short-lived tokens + phishing-resistant MFA |

Mobile findings cluster into **secrets on the device** and **traffic off the device** — and the corporate defense is **MDM/MAM policy + phishing-resistant MFA**, not fixing each app one at a time.

## Cleanup
```bash
adb uninstall com.vuln.app
rm -rf out_jadx out_apktool users.db
# remove the Burp CA from the emulator and reset its proxy to none
# if you used a rooted emulator/AVD snapshot, revert it to a clean snapshot
```

## Record it
Log commands, outputs, and what surprised you in the **My lab log** table at the bottom of [README.md](README.md), and note any misses in [PROGRESS.md](../../PROGRESS.md).
