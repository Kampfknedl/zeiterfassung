# 🐳 Docker APK Builder - Anleitung

## ✅ Voraussetzungen

- ✓ Docker Desktop installiert (Windows/Mac) oder Docker Engine (Linux)
- ✓ Projekt im Verzeichnis `C:\Users\Bene\Desktop\Python_Programme`
- ✓ `buildozer.spec` konfiguriert
- ✓ Python-Dateien und KV-Layouts vorhanden

## 🚀 Quick Start

### 1. PowerShell öffnen
```powershell
cd C:\Users\Bene\Desktop\Python_Programme
```

### 2. Build-Skript ausführen
```powershell
.\docker-build-apk.ps1
```

Das war's! Docker kümmert sich um alles.

---

## 📋 Befehle & Optionen

### Standard Debug-Build
```powershell
.\docker-build-apk.ps1
```

### Release Build
```powershell
.\docker-build-apk.ps1 -BuildType release
```

### Docker-Image nicht erneut pullen (schneller bei mehreren Builds)
```powershell
.\docker-build-apk.ps1 -SkipDockerPull
```

### APK nach Build automatisch installieren (mit ADB)
```powershell
.\docker-build-apk.ps1 -AutoInstall
```

### Finder/Explorer öffnen nach Build
```powershell
.\docker-build-apk.ps1 -OpenFinder
```

### Kombiniert: Debug + Logs behalten + Auto-Install
```powershell
.\docker-build-apk.ps1 -BuildType debug -KeepContainerLogs -AutoInstall
```

---

## 📊 Was passiert im Build?

```
1. Docker-Installation überprüfen
2. Docker-Image "kivy/buildozer" pullen (einmalig ~500MB)
3. Container starten und Projekt einbinden
4. buildozer -v android debug ausführen
5. APK generieren (5-15 Minuten)
6. APK im bin/-Ordner speichern
7. Ergebnisse anzeigen
```

---

## 📁 Output & APK-Dateien

Nach erfolgreichem Build findest du die APK hier:
```
C:\Users\Bene\Desktop\Python_Programme\bin\zeiterfassung-2.0-debug.apk
```

### Größe
- Debug APK: ~50-80 MB
- Release APK: ~30-50 MB (mit Optimierung)

---

## 🔧 Installation auf Android-Gerät

### Mit ADB (über USB)
```powershell
# Gerät verbinden (USB-Debugging aktiviert)
adb install "bin\zeiterfassung-2.0-debug.apk"

# oder mit Auto-Install Skript-Option:
.\docker-build-apk.ps1 -AutoInstall
```

### Manuell
1. APK-Datei auf Gerät übertragen (USB, Email, etc.)
2. Datei-Manager öffnen → APK antippen
3. Installation bestätigen

---

## 🐛 Troubleshooting

### ❌ "Docker not found"
```
Lösung: Docker Desktop installieren
https://www.docker.com/products/docker-desktop
```

### ❌ "Build failed - Permission denied"
```powershell
# Pfad muss absolute Windows-Pfade sein
# Sollte automatisch funktionieren, aber prüfe:
(Get-Location).Path  # sollte C:\Users\Bene\Desktop\Python_Programme zeigen
```

### ❌ "Build zu langsam"
```powershell
# Zuerst Docker-Image vorziehen:
docker pull kivy/buildozer

# Dann mit -SkipDockerPull
.\docker-build-apk.ps1 -SkipDockerPull
```

### ❌ "APK not found after build"
```
Überprüfe buildozer.spec:
- [app] section: title, package.name
- [app:android] section: alle Pfade korrekt?
- Logs: bin/buildozer_output.log oder buildozer-output.log
```

---

## 📈 Performance-Tipps

### 1. Erstes Build (mit Docker-Pull)
- ⏱️ 15-30 Minuten
- 📥 ~500 MB Download

### 2. Nachfolgende Builds (mit `-SkipDockerPull`)
- ⏱️ 5-10 Minuten (nur Kompilierung)

### 3. Docker-Caching optimieren
```powershell
# Nutze SSD für schnellere I/O
# Stelle sicher, dass ausreichend RAM verfügbar ist
```

---

## 🔐 Debug vs. Release

### Debug Build (Standard)
```powershell
.\docker-build-apk.ps1 -BuildType debug
```
- ✓ Schneller zu kompilieren
- ✓ Mit Debug-Symbolen
- ✗ Nicht signiert
- ✗ Größer
- ✗ Nur zum Testen

### Release Build
```powershell
.\docker-build-apk.ps1 -BuildType release
```
- ✓ Optimiert & kleiner
- ✓ Kann im Play Store hochgeladen werden
- ✗ Muss signiert werden (Android keystore nötig)
- ✗ Länger zu kompilieren

---

## 🔗 Zusätzliche Docker-Befehle

### Docker-Image Infos
```powershell
docker image ls | Select-String buildozer
```

### Laufende Container anschauen
```powershell
docker ps
```

### Docker-Cleanup (alte Images löschen)
```powershell
docker system prune -a
```

---

## 📝 Projekt-Struktur (für Docker)

```
C:\Users\Bene\Desktop\Python_Programme\
├── main.py                 # App-Code
├── db.py                   # Datenbank
├── buildozer.spec          # Build-Config (wichtig!)
├── requirements.txt        # Python-Deps
├── zeiterfassung.kv        # Kivy Layout
├── res/                    # Android-Ressourcen
│   └── xml/
│       └── fileprovider_paths.xml
├── icon.png                # App-Icon
└── bin/                    # Output (erstellt vom Build)
    └── zeiterfassung-2.0-debug.apk
```

---

## 🚦 Häufige Fragen

**F: Brauche ich Android SDK/NDK lokal?**
A: Nein! Docker enthält alles.

**F: Kann ich auf Linux/Mac bauen?**
A: Ja, dieses Skript funktioniert auf Windows/Mac/Linux.

**F: Muss ich Buildozer lokal installieren?**
A: Nein, es läuft im Docker-Container.

**F: Kann ich Release-APK signieren?**
A: Ja, aber braucht einen Android Keystore. Siehe [Android Developer Docs](https://developer.android.com/studio/publish/app-signing).

---

## 💡 Best Practices

1. **Vor jedem Build** testen:
   ```powershell
   python main.py  # Desktop-Test
   ```

2. **buildozer.spec** überprüfen:
   - Version aktualisieren
   - Requirements stimmen

3. **Regelmäßig Docker-Image aktualisieren:**
   ```powershell
   docker pull kivy/buildozer
   ```

4. **APKs archivieren:**
   ```powershell
   mkdir builds
   Copy-Item bin/*.apk builds/
   ```

---

## 📞 Support

Falls Build fehlschlägt:
1. Logs anschauen: `bin/buildozer_output.log`
2. buildozer.spec validieren
3. Lokalen Desktop-Test: `python main.py`
4. Docker-Verbindung testen: `docker run hello-world`

---

**Version:** 1.0  
**Letzte Aktualisierung:** 2026-01-16  
**Status:** Production-ready ✅
