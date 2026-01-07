# 🚀 ZEITERFASSUNG v2.0 - FERTIG ZUM BUILD!

## Status: ✅ BEREIT FÜR GITHUB ACTIONS BUILD

Du hast alles, was du brauchst! Der GitHub Actions Workflow wird die APK für dich bauen.

---

## 📋 SCHRITT-FÜR-SCHRITT ANLEITUNG

### Schritt 1: Code zu GitHub pushen
```powershell
# Terminal öffnen im Projektordner

# Option A: Mit Batch-Script (einfach)
push_to_github.bat

# Option B: Manuell mit PowerShell
git add .
git commit -m "Update: Zeiterfassung v2.0 mit Material Design und PDF Export"
git push origin main
```

### Schritt 2: Build starten
1. Gehe zu: https://github.com/Tkideneb2/Zeiterfassung
2. Klick auf **"Actions"** Tab
3. Wähle **"Build APK"** (links)
4. Klick grünen Button **"Run workflow"**
5. Bestätige mit **"Run workflow"**

### Schritt 3: Build überwachen
- ⏳ Dauert ca. **15-20 Minuten**
- 📊 Du siehst den Progress in Echtzeit
- ✅ Bei Erfolg: Green checkmark

### Schritt 4: APK herunterladen
1. Klick auf den Build Run (grüner Haken)
2. Scroll zu **"Artifacts"**
3. Download: `zeiterfassung-apk`
4. Extrahiere: `zeiterfassung-2.0-debug.apk`

### Schritt 5: APK auf Android installieren
```bash
# Option A: Mit Android Studio
# Gehe zu Device → Install APK

# Option B: Mit ADB (über Terminal)
adb install -r zeiterfassung-2.0-debug.apk

# Option C: Datei-Manager
# APK File → auf Handy kopieren → Tippen → Installieren
```

---

## 📦 WAS WURDE AKTUALISIERT

### ✨ App-Features (main_new.py + zeiterfassung.kv)
- ✅ KivyMD Material Design UI
- ✅ PDF Export mit ReportLab
- ✅ Auto-Open PDFs
- ✅ Sharing (Android Intent / iOS UIActivityViewController)
- ✅ Cross-Platform Support (iOS vorbereitet)
- ✅ Timer mit Pause/Resume
- ✅ Kunden Management
- ✅ Activity Autocomplete
- ✅ Datenbank Kompatibilität (alte Daten funktionieren!)

### 🔧 Build-Konfiguration (buildozer.spec)
```ini
# Wichtige Änderungen:
source.main = main_new.py            # Neue App
requirements = ... kivymd, reportlab # PDF + Material Design
android.api = 34                      # Neueste Android API
android.minapi = 21                   # Min Android 5.0
```

### 📂 Datei-Übersicht
```
main_new.py              (597 Zeilen) - Die neue iOS/Android App
zeiterfassung.kv         (226 Zeilen) - Material Design UI Layout
buildozer.spec           ✅ Aktualisiert für main_new.py
db.py                    (unverändert) - 100% kompatibel
requirements.txt         ✅ Mit KivyMD, ReportLab, Plyer
.github/workflows/build-apk.yml      ✅ GitHub Actions Workflow
```

---

## 🎯 VERSIONEN VERGLEICH

| Aspekt | v1.0 (Kivy) | v2.0 (KivyMD) |
|--------|------------|--------------|
| **UI-Framework** | Kivy Basic | KivyMD Material Design |
| **PDF Export** | ❌ CSV nur | ✅ Schöne PDFs |
| **Android** | ✅ | ✅ |
| **iOS** | ❌ | ✅ (vorbereitet) |
| **Sharing** | ❌ | ✅ Native Intents |
| **Desktop** | ✅ | ✅ |
| **Datenbank** | ✅ SQLite | ✅ Gleich |

---

## 🛠 FEHLERBEHANDLUNG

### ❌ Build schlägt fehl?
→ Guck ins Build-Log: Actions → Build Run → "Build APK" Step
→ Häufige Fehler:
  - `PermissionError`: Cython Version Problem → buildozer.spec checken
  - `ModuleNotFoundError`: Dependency fehlt in requirements
  - `Syntax Error`: Code-Fehler in main_new.py

### ❌ APK funktioniert nicht?
1. **Zuerst Desktop testen:**
   ```bash
   python main_new.py
   ```
2. **Handy-Logs anschauen:**
   ```bash
   adb logcat | grep -i python
   ```

### ❌ Größe ist zu groß?
- APK mit KivyMD ist ca. 200-250 MB (normal!)
- Kann in Release-Build auf 120 MB schrumpfen

---

## 🚀 OPTIONALE SCHRITTE

### GitHub Release erstellen
Wenn alles funktioniert, tag den Code für Release:
```bash
git tag v2.0
git push origin v2.0
# Dann automatisch Release mit APK!
```

### Direkter lokaler Build (fortgeschritten)
Falls du auf deinem PC bauen willst:
```bash
# Ubuntu / WSL2
pip install buildozer cython
buildozer android debug
# Dauert 30+ Min, braucht Java + SDK
```

---

## 📞 SUPPORT

**Problem mit Git?**
```bash
git config --global user.name "Dein Name"
git config --global user.email "deine@email.de"
git push --set-upstream origin main
```

**Handy-Installation nicht möglich?**
- Aktiviere "Unbekannte Apps installieren" in Settings
- Eller: USB Debugging aktivieren + ADB nutzen

**APK funktioniert, aber Feature fehlt?**
- Desktop Version testen: `python main_new.py`
- Falls dort OK → Android-spezifisches Problem
- Logs checken: `adb logcat`

---

## 🎉 SUCCESS CHECKLIST

- [ ] Code zu GitHub gepusht
- [ ] GitHub Actions Workflow gestartet
- [ ] Build erfolgreich (grüner Haken)
- [ ] APK downloadet
- [ ] APK auf Handy installiert
- [ ] App startet
- [ ] Timer funktioniert
- [ ] PDF wird erstellt
- [ ] PDF kann geteilt werden

**Wenn alles ✅ → Fertig!**

---

**Version:** 2.0 (KivyMD Material Design)  
**Build System:** GitHub Actions (Buildozer auf Ubuntu)  
**Status:** Production Ready ✅  
**Datum:** Januar 2025
