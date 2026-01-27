# GitHub Actions APK Builder - Setup

## ✅ Dateien vorbereitet

Folgende Dateien wurden optimiert für GitHub Actions:

- **buildozer.spec**: Android 16 (API 35) - Galaxy S24+ Konfiguration
- **.github/workflows/build-apk.yml**: Docker-basierter APK Builder (speicheroptimiert)
- **.gitignore**: Optimiert (keine großen Dateien zu GitHub)

## 📋 Schritte zum Hochladen

### 1️⃣ GitHub Repository erstellen

Gehe zu https://github.com/new und erstelle ein Repository:
- Name: `zeiterfassung`
- Beschreibung: "Android time tracking app - Kivy based"
- Typ: **Public** (erforderlich für GitHub Actions)
- Nicht initialisieren (leer lassen)

### 2️⃣ PowerShell öffnen und ausführen

```powershell
cd c:\Users\Bene\Desktop\Python_Programme

# Setup Script ausführen
.\setup-github.ps1 -GitHubUsername "DEIN_GITHUB_USERNAME"

# Beispiel:
# .\setup-github.ps1 -GitHubUsername "bene-2026"
```

### 3️⃣ Zu GitHub pushen

```powershell
git remote add origin https://github.com/DEIN_USERNAME/zeiterfassung.git
git push -u origin main
```

## 🔨 Workflow starten

Nach dem Push wird der Workflow automatisch starten:
1. Gehe zu https://github.com/DEIN_USERNAME/zeiterfassung
2. Klicke auf **Actions** Tab
3. Du siehst "Build APK - Android 16"
4. Warte ~15 Minuten
5. Download: Artifacts → `zeiterfassung-apk`

## ⚙️ Was ist optimiert?

✅ **Docker-basierter Build** - Nur ~5GB RAM statt 20GB+
✅ **.gitignore** - android-sdk, java17, venv, etc. werden NICHT hochgeladen
✅ **Speicheroptimiert** - Nur essentielle Dateien: main.py, db.py, buildozer.spec, etc.
✅ **Android 16 Ready** - API 35 für Galaxy S24+
✅ **Cleanup** - Automatisches Aufräumen nach Build

## 📦 APK Installation auf Galaxy S24+

```powershell
# Nach Download:
adb install -r zeiterfassung-2.0-release-unsigned.apk

# Oder: APK auf Handy kopieren → Tippen → Installieren
```

## ❌ Alte Dateien (NICHT hochladen!)

Diese sind redundant und werden von .gitignore ignoriert:
- `buildozer_*.spec` (nur buildozer.spec verwenden)
- `main_old*.py` (nur main.py verwenden)
- `test_*.py`, `debug_*.py` (nicht nötig für Build)
- `*.bat`, `*.ps1`, `*.sh` (lokale Scripts)
- Alle `.md` Dateien außer README.md

## 🆘 Falls es nicht funktioniert

1. **Repository nicht gefunden?**
   - Stelle sicher: https://github.com/new hat dich zur Repo-Seite umgeleitet
   - URL in Git-Befehl muss exakt sein

2. **Push fehlgeschlagen?**
   - `git config --global user.email "DEIN_EMAIL@github.com"`
   - `git config --global user.name "DEIN_USERNAME"`
   - Erneut versuchen

3. **Workflow zeigt nicht?**
   - Gehe zu Actions Tab
   - Falls leer: Warte 30 Sekunden
   - Aktualisieren (F5)

4. **Build fehlgeschlagen?**
   - Workflow Logs prüfen (Actions → Workflow → Logs)
   - Typisch: Python-Fehler in main.py
   - .gitignore prüfen (zu viel hochgeladen?)

---

**Fertig?** Dein APK wird innerhalb von ~15 Minuten gebaut! 🚀
