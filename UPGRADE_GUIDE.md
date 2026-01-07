# 🎉 Zeiterfassung v2.0 - iOS & Android mit PDF Export

## ✨ Was hat sich geändert?

Ihre Zeiterfassungs-App wurde komplett überarbeitet und erweitert:

### ✅ Neue Plattformen
- **iOS Support** - Funktioniert jetzt auf iPhone/iPad
- **Verbesserte Android-Kompatibilität**
- **Desktop-Version** zum Testen

### ✅ Material Design UI
- Modernes Interface mit KivyMD
- Native Look & Feel auf allen Plattformen
- Bessere Usability auf mobilen Geräten

### ✅ PDF Export (NEU!)
- **Professionelle PDF-Reports** mit:
  - Kundendaten (Name, Adresse, Email, Telefon)
  - Monatliche Übersichten
  - Detaillierte Eintragsauflistung
  - Gesamtstunden-Berechnung
- **Automatisches Öffnen** nach Erstellung
- **Direktes Teilen** via Email, WhatsApp, etc.

### ✅ Erweiterte Funktionen
- CSV-Export (wie bisher)
- Timer mit Pause/Resume
- Kunden-Management
- Datenbank-Persistenz

---

## 🚀 Quick Start

### 1. Desktop Version testen

```powershell
# Terminal öffnen im Projekt-Ordner

# Abhängigkeiten installieren (nur beim ersten Mal)
pip install -r requirements.txt

# App starten
python main_new.py
```

### 2. Einen Kunden erstellen

1. App öffnet sich
2. Klick: **"Neuer Kunde"**
3. Name, Adresse, Email, Telefon eingeben
4. **"SPEICHERN"**

### 3. Einträge erstellen

**Option A - mit Timer:**
1. Kunde auswählen
2. Tätigkeit eingeben
3. **START** drücken
4. **PAUSE** / **STOP** drücken
5. Eintrag wird automatisch erstellt

**Option B - manuell:**
1. Kunde auswählen
2. Tätigkeit eingeben
3. Datum (optional) eingeben
4. Stunden eingeben
5. **EINTRAG HINZUFÜGEN**

### 4. PDF erstellen & teilen

**Desktop:**
```
1. Kunde auswählen
2. Klick: "PDF ERSTELLEN"
3. PDF öffnet sich automatisch
4. Mit rechts-Klick → drucken/speichern
```

**Mobile (Android/iOS):**
```
1. Kunde auswählen
2. Klick: "PDF ERSTELLEN & TEILEN"
3. Share-Dialog öffnet sich
4. Wähle: Email, WhatsApp, Telegram, etc.
5. Fertig!
```

---

## 📁 Dateien & Struktur

### Neue Dateien
```
main_new.py           ⭐ Neue App (iOS + Android Support)
zeiterfassung.kv      ⭐ Material Design Layout
buildozer_new.spec    ⭐ iOS/Android Build-Konfiguration
PDF_EXPORT_GUIDE.md   ⭐ Ausführliche PDF-Dokumentation
test_pdf_export.py    ⭐ Test-Script mit Demo-Daten
test_report.pdf       ⭐ Beispiel-PDF (vom Test)
```

### Alte Dateien (noch da für Backup)
```
main.py               📦 Alte Version (Android-only)
buildozer.spec        📦 Alte Build-Konfiguration
README.md             📦 Alte Dokumentation
```

### Kernlogik (unverandert)
```
db.py                 ✓ Datenbank-Funktionen (Kompatibel!)
requirements.txt      ✓ Python-Abhängigkeiten
icon.png             ✓ App-Icon
```

---

## 🔄 Migration: Alt → Neu

### Automatisch (empfohlen)

```powershell
# Alle Änderungen vornehmen
.\migrate_to_v2.ps1
```

Das Skript:
- ✓ Erstellt automatisch Backups
- ✓ Aktiviert die neue Version
- ✓ Installiert neue Dependencies
- ✓ Zeigt nächste Schritte

### Manuell

```powershell
# Backup
Copy-Item main.py main_v1_backup.py
Copy-Item buildozer.spec buildozer_v1.spec

# Aktivieren
Copy-Item main_new.py main.py
Copy-Item buildozer_new.spec buildozer.spec

# Abhängigkeiten
pip install kivymd plyer reportlab
```

**⚠️ WICHTIG**: Ihre Datenbank bleibt erhalten! Alle Kunden und Einträge sind noch vorhanden.

---

## 📱 Mobile Apps bauen

### Android APK (Windows/Mac/Linux)

#### Mit Docker (empfohlen - einfach & zuverlässig)
```bash
docker run --rm -v ${PWD}:/home/user/buildozer \
  kivy/buildozer buildozer -v android debug

# Output: bin/zeiterfassung-2.0-debug.apk
```

#### Mit Buildozer direkt
```bash
pip install buildozer
buildozer android debug

# Debug APK: bin/zeiterfassung-*-debug.apk
# Release APK: bin/zeiterfassung-*-release-unsigned.apk
```

### iOS App (nur auf macOS)

```bash
# macOS erforderlich!

pip install buildozer kivy-ios

# Debug Build
buildozer ios debug

# Release für App Store
buildozer ios release
```

---

## 📊 PDF-Format

Der generierte PDF sieht professionell aus:

```
┌─────────────────────────────────────────┐
│  ZEITERFASSUNG - Kundenname             │
│                                         │
│  Kunde:   Max Mustermann                │
│  Datum:   07.01.2026                    │
│  Adresse: Musterstraße 123, 12345 Stadt │
│  Email:   max@example.com               │
│  Tel:     +49 123 456789                │
├─────────────────────────────────────────┤
│  Monat: 2025-12                         │
│  ┌─────────┬──────────────┬───────────┐ │
│  │ Datum   │ Tätigkeit    │ Stunden   │ │
│  ├─────────┼──────────────┼───────────┤ │
│  │ 01.12   │ Programmier  │ 8.00      │ │
│  │ 02.12   │ Meeting      │ 2.00      │ │
│  │ ...     │ ...          │ ...       │ │
│  └─────────┴──────────────┴───────────┘ │
│  Monatssumme: 10.00 Std                 │
├─────────────────────────────────────────┤
│  Gesamtstunden: 10.00 Std               │
└─────────────────────────────────────────┘
```

---

## 🔧 Technische Details

### Dependencies

```txt
kivy          # Cross-Platform UI Framework
kivymd        # Material Design Components  
pillow        # Bildbearbeitung
reportlab     # PDF-Generierung ⭐ NEU
pyjnius       # Android Java Bridge
plyer         # Platform-Funktionen
```

### Unterstützte Plattformen

| Plattform | Min. Version | Status |
|-----------|-------------|--------|
| Windows   | 10          | ✓ Voll unterstützt |
| macOS     | 10.14       | ✓ Voll unterstützt |
| Linux     | Ubuntu 18+  | ✓ Voll unterstützt |
| Android   | 5.0 (API 21) | ✓ Voll unterstützt |
| iOS       | 12.0+       | ✓ Voll unterstützt |

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'kivymd'"

```powershell
# Lösung:
pip install -r requirements.txt

# Oder einzeln:
pip install kivymd reportlab plyer
```

### Problem: App crasht beim Starten

```powershell
# Cache löschen:
Remove-Item -Recurse .venv
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Problem: PDF öffnet sich nicht

- **Windows**: PDF-Reader (Adobe, Microsoft Edge) installieren
- **Mac**: Preview sollte automatisch öffnen
- **Linux**: `sudo apt install evince` (PDF Viewer)

### Problem: Share funktioniert nicht auf Android

Überprüfen Sie:
```ini
# In buildozer.spec:
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.add_resources = res
```

---

## 📚 Weitere Ressourcen

- **[PDF_EXPORT_GUIDE.md](PDF_EXPORT_GUIDE.md)** - Detaillierte PDF-Dokumentation
- **[README_NEW.md](README_NEW.md)** - Komplette Feature-Dokumentation
- **[test_pdf_export.py](test_pdf_export.py)** - Test-Script mit Demo

---

## 🎯 Nächste Schritte

### Sofort testen:
```powershell
python main_new.py
```

### Für Production:
```bash
# Android
docker run --rm -v ${PWD}:/home/user/buildozer kivy/buildozer buildozer -v android release

# iOS (auf Mac)
buildozer ios release
```

---

## 💡 Pro-Tipps

1. **Testdaten erstellen**: `python test_pdf_export.py`
   - Erstellt Demo-DB und Beispiel-PDF

2. **Alte Version vergleichen**: 
   - `main.py` ist noch da zum Vergleichen
   - Datenbank ist 100% kompatibel

3. **Für App Stores**:
   - Android: Signieren und hochladen auf Google Play
   - iOS: Erfordert Apple Developer Account ($99/Jahr)

4. **GitHub Actions**:
   - Workflow bereits vorbereitet
   - Automatische APK-Builds möglich

---

## 📞 Support

Probleme oder Fragen?

1. Schauen Sie in die Logs: `.kivy/logs/`
2. Testen Sie mit: `python test_pdf_export.py`
3. Überprüfen Sie die ausführliche Doku: [PDF_EXPORT_GUIDE.md](PDF_EXPORT_GUIDE.md)

---

**🎉 Viel Spaß mit der neuen Version!**

Die App ist bereit für iOS und Android. 
Nutzen Sie den PDF-Export für professionelle Reports.

---

*Zeiterfassung v2.0 - Build 2026-01-07*
*Kompatibel mit allen Kunden- und Eintragsdaten aus v1.0*
