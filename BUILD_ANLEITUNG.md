# Android APK Build-Anleitung - Zeiterfassung App

**Datum:** 24.01.2026  
**App-Version:** 2.0 (Neuaufbau)  
**Ziel:** Android 16 kompatibel (API 34)

---

## 📋 Build-Optionen Übersicht

### Option 1: Docker (Empfohlen - Lokal)
✅ **Vorteile:** Keine SDK-Installation nötig, reproduzierbar  
❌ **Nachteile:** Braucht Docker Desktop, ~15 Min beim ersten Mal

### Option 2: GitHub Actions (Cloud)
✅ **Vorteile:** Baut automatisch, kein lokales Setup  
❌ **Nachteile:** GitHub-Probleme beim User, funktioniert aktuell nicht

### Option 3: Buildozer direkt (Komplex)
❌ Nicht empfohlen - braucht Java, Android SDK, NDK manuell

---

## 🐳 Docker-Build (Aktuelle Methode)

### Status: ✅ LÖSUNG GEFUNDEN! Build läuft...

### Finale Lösung:
```powershell
# 1. Build-Cache löschen (wichtig bei Codeänderungen!)
Remove-Item -Path ".buildozer" -Recurse -Force

# 2. APK bauen mit echo y für Root-Bestätigung
docker run --rm -v "${PWD}:/home/user/buildozer" kivy/buildozer /bin/bash -c "cd /home/user/buildozer && echo y | buildozer android debug 2>&1"
```

**Wichtig:** Dauert 15-20 Min beim ersten Mal (lädt SDK/NDK)

### Voraussetzungen:
- ✅ Docker Desktop installiert und gestartet
- ✅ PowerShell als Administrator
- ✅ Projekt in: `C:\Users\Bene\Desktop\Python_Programme`

### Versuchte Befehle (Chronologisch):

#### Versuch 1: Standard Docker-Build
```powershell
docker run --rm -v "${PWD}:/home/user/buildozer" kivy/buildozer buildozer android debug
```
**Ergebnis:** ❌ Fehlgeschlagen  
**Fehler:** EOFError - Buildozer fragt nach Root-Bestätigung, keine Eingabe möglich

#### Versuch 2: Mit `yes`-Command
```powershell
docker run --rm -v "${PWD}:/home/user/buildozer" kivy/buildozer bash -c "yes | buildozer android debug"
```
**Ergebnis:** ❌ Fehlgeschlagen  
**Fehler:** Gleicher Fehler - `yes` wird nicht an buildozer weitergegeben

#### Versuch 3: ENV-Variable BUILDOZER_WARN_ON_ROOT
```powershell
docker run --rm -v "${PWD}:/home/user/buildozer" -e "BUILDOZER_WARN_ON_ROOT=0" kivy/buildozer buildozer android debug
```
**Ergebnis:** ❌ Fehlgeschlagen  
**Fehler:** ENV-Variable wird ignoriert, Root-Check greift trotzdem

---

## 🔧 Nächste Schritte (TODO)

### Lösung 1: Non-Root User im Container
Docker mit user-Flag ausführen:
```powershell
docker run --rm -v "${PWD}:/home/user/buildozer" --user $(id -u):$(id -g) kivy/buildozer buildozer android debug
```

### Lösung 2: Buildozer-Spec anpassen
In `buildozer.spec` hinzufügen:
```ini
[buildozer]
warn_on_root = 0
```

### Lösung 3: Eigenes Dockerfile mit Workaround
Custom Dockerfile erstellen, der Root-Check überspringt

---

## 📁 Wichtige Dateien

### Kern-Dateien:
- `main.py` - Haupt-App (763 Zeilen)
- `db.py` - Datenbank-Funktionen (155 Zeilen)
- `buildozer.spec` - Android-Build-Config
- `requirements.txt` - Python-Pakete (kivy, reportlab, pillow, pyjnius)

### Backup:
- `main_old_backup.py` - Alte Version vor Neuaufbau (2089 Zeilen)

### Build-Outputs:
- `bin/zeiterfassung-*-debug.apk` - Fertige APK (noch nicht erstellt)
- `.buildozer/` - Build-Cache (wird automatisch erstellt)

---

## ✅ App-Features (Implementiert)

1. **Über-Kunden-Verwaltung**
   - Anlegen, Bearbeiten, Löschen
   - Felder: Name, Stundensatz, Adresse, E-Mail, Telefon

2. **Timer**
   - Start/Pause/Stop
   - Zeigt HH:MM:SS
   - Automatische Rundung auf 0.25h (15 Min)

3. **Manuelle Zeiterfassung**
   - Nachträgliches Eintragen
   - Datum, Startzeit, Stunden, Kommentar

4. **Einträge-Liste**
   - Zeigt letzte 10 Einträge pro Kunde
   - Format: Datum | Aktivität | Stunden | Kommentar

5. **PDF-Export**
   - Report mit allen Einträgen
   - Gesamtstunden + Betrag-Berechnung
   - Konfigurierbarer Speicherpfad

---

## 🔄 Rollback-Anleitung

Wenn der neue Build nicht funktioniert:

### 1. Alte Version wiederherstellen:
```powershell
# Backup umbenennen
Move-Item -Path "main.py" -Destination "main_new.py"
Move-Item -Path "main_old_backup.py" -Destination "main.py"
```

### 2. Alte requirements.txt wiederherstellen:
```
kivy
kivymd
pillow
pyjnius
plyer
fpdf2
reportlab
cython
androidstorage4kivy
```

### 3. Desktop-Test:
```powershell
python main.py
```

---

## 📝 Notizen

- **Python-Version:** 3.13.11 (global), 3.10.13 (Android-Build)
- **Kivy-Version:** 2.3.1 (Desktop), 2.3.0 (Android)
- **reportlab:** 4.4.9 installiert in globalem Python
- **Entwicklungsstand:** Desktop-Version läuft stabil ✅
- **Android-Build:** Noch nicht erfolgreich ❌

---

## 🐛 Bekannte Probleme

1. **Docker Root-Check:** Buildozer läuft als Root im Container → Input-Abfrage funktioniert nicht
2. **GitHub Actions:** User hat Probleme mit GitHub-Builds
3. **Alte APK:** Crashte mit "Invalid resource ID 0x00000000" → komplett neu aufgebaut

---

## 📞 Support-Info

Bei Fragen/Problemen:
- Diese Datei aktualisieren mit neuen Versuchen
- Terminal-Output speichern
- Docker-Logs checken: `docker logs -f $(docker ps -q)`
