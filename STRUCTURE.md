# 📂 Projekt-Struktur - Zeiterfassung v2.0

## 🚀 QUICK START
```
start.bat                    ← Doppelklick hier! (Windows)
START_HERE.md               ← Lese das zuerst!
```

---

## 📋 Dokumentation (In dieser Reihenfolge lesen)

```
START_HERE.md               ⭐ Anfänger - Quick Start
UPGRADE_GUIDE.md            📖 Komplette Anleitung für v2.0
PDF_EXPORT_GUIDE.md         📋 PDF Export im Detail
CHANGES_SUMMARY.md          📊 Was sich geändert hat
README_NEW.md               📚 Erweiterte Features
README.md                   (alt - Android v1.0)
```

---

## 🎯 Hauptdateien

### App Version v2.0 (NEU - verwenden!)
```
main_new.py                 ✅ Neue App mit iOS/Android Support
zeiterfassung.kv           ✅ Material Design UI Layout
```

### Alte Version (Backup - nicht löschen)
```
main.py                    📦 Alte Android-only Version v1.0
README.md                  📦 Alte Dokumentation
```

### Build-Konfiguration
```
buildozer_new.spec         ✅ Neue iOS/Android Build Config
buildozer.spec             📦 Alte Android-only Config
```

### Python Abhängigkeiten
```
requirements.txt           ✅ Alle notwendigen Packages
```

---

## 🔧 Werkzeuge & Scripts

### Windows Scripts
```
start.bat                  🎯 Quick-Start Menu (Doppelklick!)
migrate_to_v2.ps1          🔄 Auto-Migration zu v2.0
```

### Datenbanklogik
```
db.py                      ✓ Datenbank-Funktionen (unverändert)
```

### Tests & Demos
```
test_pdf_export.py         🧪 PDF-Export Test
test_report.pdf            📄 Beispiel PDF (vom Test)
test_zeiterfassung.db      💾 Test-Datenbank
```

---

## 📱 Mobile & Icons

```
icon.png                   🎨 App Icon
res/
  └─ xml/
      └─ fileprovider_paths.xml    ✓ Android FileProvider Config
templates/
  └─ AndroidManifest.tmpl.xml     (Android Manifest Template)
```

---

## 📂 Verzeichnisbaum (vollständig)

```
Zeiterfassung/
│
├── 🎯 START HERE
│   ├── START_HERE.md                   ⭐ BEGIN HERE
│   ├── start.bat                       ⭐ DOPPELKLICK ZUM STARTEN
│   └── UPGRADE_GUIDE.md                ⭐ Quick Start Guide
│
├── 📚 DOKUMENTATION
│   ├── PDF_EXPORT_GUIDE.md             📋 PDF-Funktionen
│   ├── CHANGES_SUMMARY.md              📊 Was sich geändert hat
│   ├── README_NEW.md                   📖 Feature-Übersicht v2.0
│   └── README.md                       📦 Alte Dokumentation v1.0
│
├── 💻 APP CODE (v2.0 - NEUE VERSION)
│   ├── main_new.py                     ✅ Hauptapp (597 Zeilen)
│   ├── zeiterfassung.kv                ✅ Material Design Layout
│   └── db.py                           ✓ Datenbank-Logik
│
├── 📦 APP CODE (v1.0 - ALTE VERSION)
│   ├── main.py                         📦 Alte Version (Backup)
│   └── (alte requirements.txt)
│
├── 🔧 BUILD & CONFIG
│   ├── buildozer_new.spec              ✅ iOS/Android Build v2.0
│   ├── buildozer.spec                  📦 Android-only Build v1.0
│   ├── requirements.txt                ✅ Python Dependencies
│   └── icon.png                        🎨 App Icon
│
├── 🚀 TOOLS & SCRIPTS
│   ├── start.bat                       🎯 Quick-Start Menu (Win)
│   ├── migrate_to_v2.ps1               🔄 Auto-Migration Script
│   ├── test_pdf_export.py              🧪 PDF-Test Script
│   ├── test_report.pdf                 📄 Beispiel-PDF
│   └── test_zeiterfassung.db           💾 Test-Datenbank
│
├── 📱 ANDROID/iOS RESOURCES
│   ├── res/
│   │   └── xml/
│   │       └── fileprovider_paths.xml  ✓ Android FileProvider
│   ├── templates/
│   │   └── AndroidManifest.tmpl.xml   (Android Manifest)
│   └── icon.png                        🎨 App Icon
│
├── 🔐 VERSION CONTROL
│   ├── .git/                           Git Repository
│   ├── .gitignore                      Git Ignore Rules
│   └── .github/workflows/              CI/CD Workflows
│
├── 🐍 PYTHON ENVIRONMENT
│   └── .venv/                          Virtual Environment
│       ├── Scripts/
│       │   ├── python.exe              Python Interpreter
│       │   └── pip.exe                 Package Manager
│       └── Lib/
│           └── site-packages/          Installed Packages
│
└── 📋 PROJEKT DATEIEN
    ├── .gitignore                      
    ├── SHARING_CHANGES.md              (Alt)
    ├── buildozer-output.log            Build Log
    └── __pycache__/                    Python Cache

```

---

## 🎯 USE CASES

### Ich will die App testen
```
1. Doppelklick: start.bat
2. Wähle: 1) App starten
3. Fertig!
```

### Ich will zur v2.0 upgraden
```
1. Doppelklick: start.bat
2. Wähle: 3) Upgrade zu v2.0
3. Fertig!

ODER manuell:
powershell .\migrate_to_v2.ps1
```

### Ich will PDF-Export testen
```
1. Doppelklick: start.bat
2. Wähle: 2) Test PDF-Export
3. Siehe: test_report.pdf
```

### Ich will Android APK bauen
```
1. Update buildozer.spec:
   mv buildozer.spec buildozer_v1.spec
   mv buildozer_new.spec buildozer.spec

2. Mit Docker (empfohlen):
   docker run --rm -v %cd%:/home/user/buildozer kivy/buildozer buildozer -v android debug

3. APK in: bin/zeiterfassung-*.apk
```

### Ich will iOS App bauen (macOS only)
```
1. Update buildozer.spec (siehe oben)

2. Kommando:
   buildozer ios debug

3. App in: .buildozer/ios/platform/build-*/
```

---

## 📊 CHANGES v1.0 → v2.0

| Aspekt | v1.0 | v2.0 | Status |
|--------|------|------|--------|
| Plattform | Android | iOS + Android + Desktop | ✅ Erweitert |
| UI | Kivy Standard | Material Design (KivyMD) | ✅ Modernisiert |
| Export | CSV | CSV + PDF | ✅ Erweitert |
| PDF Sharing | ❌ | ✅ Auto-Open + Share | ✅ Neu |
| Datenbank | SQLite | SQLite | ✅ Kompatibel |
| File Handling | Android-specific | Cross-Platform | ✅ Erweitert |

---

## 🔄 VERSIONS-VERWALTUNG

### Backup vorhanden
- `main.py` ← Alte Version
- `buildozer.spec` ← Alte Config
- `README.md` ← Alte Doku

### Aktuelle Version
- `main_new.py` ← Neue Version
- `buildozer_new.spec` ← Neue Config
- `zeiterfassung.kv` ← Neue UI

### Fallback
Falls etwas schiefgeht:
```powershell
# Alte Version wiederherstellen
Copy-Item main.py main_broken.py
Copy-Item main_old_backup.py main.py
python main.py
```

---

## 💾 DATENBANK-STRUKTUR

```sql
Customers Table:
├─ id (INTEGER PRIMARY KEY)
├─ name (TEXT UNIQUE)
├─ address (TEXT)
├─ email (TEXT)
└─ phone (TEXT)

Entries Table:
├─ id (INTEGER PRIMARY KEY)
├─ customer (TEXT)
├─ activity (TEXT)
├─ start (TEXT - ISO Format)
├─ end (TEXT - ISO Format)
├─ duration_hours (REAL)
└─ notes (TEXT)

Location:
- Desktop: ~/.kivy/zeiterfassung/stundenerfassung.db
- Android: /sdcard/Android/data/org.tkideneb.zeiterfassung/files/
- iOS: ~/Documents/Zeiterfassung/
```

---

## 🚀 DEPLOYMENT

### Development (Desktop)
```
python main_new.py
```

### Production (Mobile)
```
# Android Release
buildozer android release
→ bin/zeiterfassung-*-release-unsigned.apk

# iOS Release (macOS)
buildozer ios release
→ Xcode für Signing verwenden
```

---

## 📞 SUPPORT MATRIX

| Problem | Lösung | Ort |
|---------|--------|-----|
| App startet nicht | `pip install -r requirements.txt` | Terminal |
| PDF öffnet nicht | PDF-Reader installieren | System |
| Daten verloren | DB-Backup checken | `.kivy/` Folder |
| Alte Version? | `main.py` noch vorhanden | Projekt-Ordner |
| iOS Build? | Nur macOS mit Xcode | UPGRADE_GUIDE.md |

---

## 📈 PROJEKT-STATISTIKEN

```
Gesamt Code:          ~1200 Zeilen (App + Tests)
App v2.0:              597 Zeilen
Test Scripts:          229 Zeilen
Dokumentation:        ~3000 Zeilen
Datenbank:            171 Zeilen (unverändert)

Plattformen:          5 (Windows, Mac, Linux, Android, iOS)
Dependencies:         6 (Kivy, KivyMD, Plyer, ReportLab, PIL, pyjnius)
```

---

**Status: ✅ PRODUCTION READY**

Alles ist bereit für iOS, Android und Desktop! 🎉
