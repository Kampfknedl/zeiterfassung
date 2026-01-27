# Änderungsprotokoll - Zeiterfassung APK Builder Setup
**Datum:** 27. Januar 2026  
**Status:** ✅ Aktiv - GitHub Actions APK Builder konfiguriert

---

## 📋 Zusammenfassung

GitHub Actions APK Builder für Android 16 (API 35) eingerichtet. App wird automatisch bei jedem Push zu `main` gebaut.

---

## 🔧 Vorgenommene Änderungen

### 1. GitHub Repository Setup
- **Repository:** https://github.com/Kampfknedl/zeiterfassung
- **Sichtbarkeit:** Public (erforderlich für GitHub Actions)
- **Status:** Aktiv

### 2. Android Konfiguration (buildozer.spec)
**Änderungen:**
- `android.api = 35` (Android 16 für Galaxy S24+)
- `android.target_api = 35`
- `android.minapi = 21` (Min API Level)
- `android.archs = arm64-v8a` (64-bit ARM only)
- `android.ndk = 25b` (NDK Version)

**Dependencies:**
```
androidx.core:core:1.12.0
androidx.appcompat:appcompat:1.6.1
```

**Excludes optimiert:**
- Keine .db Dateien (Datenbank nicht hochladen)
- Keine .github Ordner-Duplizierung

### 3. GitHub Actions Workflow (.github/workflows/build-apk.yml)
**Erstellt:** Vollständiger Build-Workflow mit:
- Java 17 Setup (Temurin)
- Python 3.10
- System Dependencies Installation
- Buildozer direkt (nicht Docker, wegen Image-Problemen)
- APK Check nach Build
- Artifacts Upload (30 Tage Retention)
- Release Support (Tags)

**Trigger:**
- Push zu `main` oder `develop`
- Manual via `workflow_dispatch`
- Timeout: 45 Minuten

### 4. Kotlin-Versionen-Konflikt GELÖST ✅

**Problem:**
```
Duplicate class kotlin.text.jdk8.RegexExtensionsJDK8Kt
  - Kotlin 1.8.22 (von AndroidX)
  - Kotlin 1.6.0 (von Buildozer intern)
```

**Lösungen implementiert:**

#### a) gradle.properties (neu erstellt)
```properties
kotlin.version=1.8.22
org.gradle.jvmargs=-Xmx2048m
org.gradle.parallel=true
org.gradle.workers.max=2
```

#### b) kotlin-resolution.gradle (neu erstellt)
Force-Strategy für Gradle:
```gradle
configurations.all {
    resolutionStrategy {
        force 'org.jetbrains.kotlin:kotlin-stdlib:1.8.22'
        force 'org.jetbrains.kotlin:kotlin-stdlib-jdk8:1.8.22'
        force 'org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.8.22'
    }
}
```

### 5. .gitignore optimiert
**Ignoriert (nicht zu GitHub):**
- `__pycache__/`, `.buildozer/`, `bin/`
- `android-sdk/`, `java17/`
- `*.apk`, `*.aab`, `*.dex`
- `.gradle/`, `build/`
- Alte Dateien: `*_old.py`, `test_*.py`, `debug_*.py`
- `.bat`, `.ps1`, `.sh` Skripte
- `Dockerfile`, Docker-Dateien
- Log-Dateien, temp-Dateien

---

## 📊 Build Status History

| Run | Status | Fehler | Fix |
|-----|--------|--------|-----|
| 1 | ❌ Failed | Docker Image buildozer:latest Befehl nicht gefunden | Zu Native Buildozer gewechselt |
| 2 | ❌ Failed | Kotlin Duplicate Class Konflikt | gradle.properties + kotlin-resolution.gradle |
| 3 | ⏳ Running | - | Kotlin 1.8.22 Force-Strategy |

**Latest Run:** https://github.com/Kampfknedl/zeiterfassung/actions

---

## 🎯 Nächste Session - Schnell-Anleitung

Wenn du zur nächsten Session wiederkommst:

### 1. Build Status prüfen
```powershell
cd c:\Users\Bene\Desktop\Python_Programme
$response = Invoke-RestMethod -Uri "https://api.github.com/repos/Kampfknedl/zeiterfassung/actions/runs"
$response.workflow_runs[0] | Select-Object status, conclusion, created_at
```

### 2. Neuen Build manuell triggern
```powershell
# Push irgendwelche Änderungen zu main
git add .
git commit -m "Trigger build"
git push origin main

# Oder über GitHub UI: Actions → Build APK - Android 16 → Run workflow
```

### 3. APK downloaden
1. Gehe zu: https://github.com/Kampfknedl/zeiterfassung/actions
2. Klick auf Latest Workflow
3. **Artifacts** → `zeiterfassung-apk` Download

### 4. Auf Galaxy S24+ installieren
```powershell
# APK auf Handy via USB
adb install -r bin/zeiterfassung-2.0-release-unsigned.apk

# Oder: APK kopieren, Dateimanager → tippen → Installieren
```

---

## ⚠️ Bekannte Limitationen & TODOs

### Token-Limitations
- **repo Token:** Nur `repo` Scope (keine `workflow` Scope)
- **workflow Token:** Für GitHub Actions, manuell in Workflow pushen

**Workaround:** Tokens regenerieren wenn nötig:
- https://github.com/settings/tokens
- `repo` + `workflow` Scopes
- 90 Tage Expiration

### Gradle Deprecation-Warnung
```
Deprecated Gradle features were used in this build, 
making it incompatible with Gradle 9.0
```
- ⚠️ Nicht kritisch aktuell
- 🔮 Zukünftig: Buildozer/P4A updaten

### Größe Optimierung
- `adb_tmp.txt` (79 MB) aus Git entfernt
- `.buildozer/` lokal, nicht zu GitHub

---

## 📝 Wichtige Dateien

| Datei | Zweck | Kritisch |
|-------|-------|----------|
| `buildozer.spec` | Android Build-Config | ✅ Ja |
| `.github/workflows/build-apk.yml` | GitHub Actions Workflow | ✅ Ja |
| `gradle.properties` | Gradle Kotlin-Force | ✅ Ja (für Kotlin Fix) |
| `kotlin-resolution.gradle` | Gradle Resolution-Strategy | ✅ Ja |
| `main.py` | App-Code | ✅ Ja |
| `db.py` | Datenbank-Code | ✅ Ja |
| `zeiterfassung.kv` | UI-Design | ✅ Ja |
| `requirements.txt` | Python-Abhängigkeiten | ✅ Ja |
| `.gitignore` | Optimiert | ⚠️ Beachte |

---

## 🔐 Secrets & Credentials

**GitHub Tokens (GEHEIM halten!):**
- `repo Token`: Nur für `git push` (lokal)
- `workflow Token`: Für GitHub Actions (in Workflow nicht nötig - nutzt `GITHUB_TOKEN`)

**Nie hochladen:**
- Personal Access Tokens
- Android Keystore (`.jks` Dateien)
- Private Keys

---

## 🚀 Quick Reference für nächste Session

```bash
# Status prüfen
curl https://api.github.com/repos/Kampfknedl/zeiterfassung/actions/runs

# Lokal testen (vor Push)
buildozer -v android release

# Push & Build starten
git add .
git commit -m "deine änderungen"
git push origin main

# Browser öffnen
start https://github.com/Kampfknedl/zeiterfassung/actions
```

---

## ✅ Checkliste für Nächste Session

- [ ] Repository Status prüfen: https://github.com/Kampfknedl/zeiterfassung
- [ ] Letzte Build-Logs ansehen (Falls fehlgeschlagen)
- [ ] `.gitignore` checken (Keine großen Dateien!)
- [ ] `buildozer.spec` für neue Features updaten (falls nötig)
- [ ] APK testen auf Galaxy S24+
- [ ] Neue Features hochladen und Build triggernen

---

**Status:** 🟢 Einsatzbereit
**Letztes Update:** 27.01.2026
**Nächste Überprüfung:** [Datum nächste Session]
