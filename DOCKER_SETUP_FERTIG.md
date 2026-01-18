# ✅ Docker APK Builder - Setup abgeschlossen

## 🎯 Status
- ✅ Docker installiert (Version: 29.1.3)
- ✅ Build-Skripte erstellt
- ✅ Konfiguration geprüft
- ✅ Ready to Build!

---

## 🚀 Sofort Starten

### 1. PowerShell öffnen
```powershell
cd C:\Users\Bene\Desktop\Python_Programme
```

### 2. Schneller Build starten
```powershell
.\build.ps1
```

**Oder mit mehr Optionen:**
```powershell
.\docker-build-apk.ps1
```

---

## 📋 Verfügbare Skripte

### `build.ps1` - ⚡ Schnelle Variante
- Einfach & schnell
- Minimal Output
- Perfekt zum Schnellbauen
```powershell
.\build.ps1
```

### `docker-build-apk.ps1` - 🛠️ Erweiterte Variante
- Mehr Optionen & Konfiguration
- Detailliertes Logging
- Unterstützt Debug/Release
```powershell
# Standard Debug Build
.\docker-build-apk.ps1

# Release Build
.\docker-build-apk.ps1 -BuildType release

# Auto-Install mit ADB
.\docker-build-apk.ps1 -AutoInstall

# Skip Docker-Pull (schneller)
.\docker-build-apk.ps1 -SkipDockerPull
```

---

## 🎬 Was passiert beim Build

```
┌─────────────────────────────────────┐
│ docker-build-apk.ps1ausgeführt      │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ 1. Docker-Version überprüfen        │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ 2. Image "kivy/buildozer" pullen    │ (einmalig ~500MB)
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ 3. Docker-Container starten         │
│    Projekt einbinden (/home/user..) │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ 4. buildozer -v android debug       │ (5-15 Min)
│    - Android SDK/NDK compilieren    │
│    - Python kompilieren             │
│    - Kivy compilieren               │
│    - APK assembeln                  │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ 5. APK im bin/ Ordner speichern     │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│ 6. Ergebnisse anzeigen              │
│    Größe, Pfad, Größe               │
└─────────────────────────────────────┘
```

---

## ⏱️ Zeitaufwand

### Erster Build
- **15-30 Minuten**
- Docker-Image pullen: ~5 Minuten (~500 MB)
- Compilation: ~10-25 Minuten

### Nachfolgende Builds (mit `-SkipDockerPull`)
- **5-10 Minuten**
- Cache wird genutzt
- Nur Neucompilation

---

## 📁 Output & APK

Nach erfolgreichem Build:
```
📂 C:\Users\Bene\Desktop\Python_Programme\
   └── bin/
       └── zeiterfassung-2.0-debug.apk (50-80 MB)
```

---

## 📱 Installation auf Android

### Variante 1: Mit ADB (USB + Debugging aktiviert)
```powershell
adb install "bin\zeiterfassung-2.0-debug.apk"
```

### Variante 2: Auto-Install via Skript
```powershell
.\docker-build-apk.ps1 -AutoInstall
```

### Variante 3: Manuell
1. APK auf Gerät übertragen
2. Datei-Manager öffnen
3. APK antippen → Installation bestätigen

---

## 🔧 Projekt-Struktur (wichtig!)

Das Skript nutzt diese Struktur:
```
C:\Users\Bene\Desktop\Python_Programme\
├── main.py                        ← App-Einstiegspunkt
├── db.py                          ← Datenbank
├── buildozer.spec                 ← BUILD-KONFIGURATION
├── requirements.txt               ← Dependencies
├── zeiterfassung.kv               ← UI-Layout
├── icon.png                       ← App-Icon
├── res/
│   └── xml/
│       └── fileprovider_paths.xml ← Android-Ressourcen
└── bin/                           ← OUTPUT (wird erstellt)
    └── zeiterfassung-2.0-debug.apk
```

---

## 🔐 Sicherheit & Best Practices

### ✅ Checkliste vor dem Build

- [ ] `main.py` lokal getestet: `python main.py`
- [ ] `buildozer.spec` überprüft
- [ ] `requirements.txt` aktuell
- [ ] `icon.png` vorhanden (mindestens 512x512)
- [ ] Git-Changes committed (optional, aber empfohlen)

### 📝 Tipps
- Teste immer lokal vor dem Docker-Build
- Halte buildozer.spec aktuell
- Archiviere alte APKs
- Versionsnummer in buildozer.spec inkrementieren

---

## 🚨 Troubleshooting

### Docker-Fehler
```powershell
# Docker Status überprüfen
docker ps

# Image prüfen
docker image ls | Select-String buildozer

# Vollständiger Reset
docker pull kivy/buildozer
docker system prune -a
```

### Build-Fehler
```
Überprüfe:
1. buildozer.spec Syntax
2. requirements.txt Abhängigkeiten
3. Pfade in buildozer.spec
4. Logs: bin/buildozer_output.log
```

### APK nicht gefunden
```
Prüfe:
- [app] section in buildozer.spec
- title = Zeiterfassung
- package.name = zeiterfassung
- Logs für Fehler
```

---

## 📊 Projekt-Infos

**App:** Zeiterfassung  
**Version:** 2.0  
**Zielplattform:** Android 21+ (Lollipop und später)  
**Unterstützte Architekturen:** arm64-v8a, armeabi-v7a  
**Größe (Debug):** 50-80 MB  
**Größe (Release):** 30-50 MB  

---

## 🎓 Weiterführende Ressourcen

- **Kivy Docs:** https://kivy.org/doc/
- **Buildozer Docs:** https://buildozer.readthedocs.io/
- **Android Developer:** https://developer.android.com/

---

## ✨ Nächste Schritte

```powershell
# 1. Terminal öffnen und ins Projekt gehen
cd C:\Users\Bene\Desktop\Python_Programme

# 2. Schneller Build starten
.\build.ps1

# 3. Warten... (5-15 Minuten)

# 4. APK im bin/ Ordner finden

# 5. Auf Android installieren:
adb install bin/*.apk

# 6. App auf Gerät starten und testen!
```

---

## 🎉 Fertig!

Der Docker APK Builder ist jetzt einsatzbereit. Starten Sie mit:

```powershell
.\build.ps1
```

Viel Spaß beim Bauen! 🚀

---

**Setup-Datum:** 2026-01-16  
**Docker-Version:** 29.1.3  
**Status:** ✅ Production-ready
