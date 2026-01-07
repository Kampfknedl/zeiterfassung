# Upgrade auf v2.0 - PDF Export

## 🎉 Was ist neu?

### PDF-Export mit automatischem Öffnen und Teilen

Die neue Version v2.0 bietet:

✅ **Professionelle PDF-Reports** mit:
- Kundendaten (Name, Adresse, Email, Telefon)
- Monatliche Zusammenfassung
- Detaillierte Einträge (Datum, Tätigkeit, Stunden)
- Monatssummen und Gesamtstunden
- Material Design Styling

✅ **Automatisches Öffnen**: PDF öffnet sich direkt nach Erstellung
✅ **Direktes Teilen**: Mit "PDF erstellen & teilen" direkt weiterleiten
✅ **Schönes Design**: Farbcodierte Tabellen mit klarer Struktur

✅ **Cross-Platform**: Funktioniert auf Windows, Mac, Linux, Android und iOS

---

## 📋 Installation

### 1. Dependencies installieren

```powershell
# Im Projekt-Ordner:
pip install reportlab

# Oder alle auf einmal:
pip install -r requirements.txt
```

### 2. App starten

```powershell
python main_new.py
```

---

## 🎯 Neue Features

### PDF Export Button

In der Export-Section findet ihr jetzt:

```
📄 PDF ERSTELLEN          - PDF-Report erstellen (öffnet automatisch)
📤 PDF ERSTELLEN & TEILEN - PDF erstellen und direkt teilen
📋 CSV exportieren        - Alte CSV-Funktion
📤 CSV exportieren & teilen
```

### PDF-Inhalt

Der PDF enthält:

```
ZEITERFASSUNG - Kundenname
═══════════════════════════════════════

Kunde:        Max Mustermann
Datum:        07.01.2026
Adresse:      Musterstraße 123
Email:        max@example.com
Telefon:      +49 123 456789

Monat: 2025-12
├─ 01.12.2025  Programmierung     8.00 Std
├─ 02.12.2025  Meeting            2.00 Std
├─ 03.12.2025  Testen             1.50 Std
├─ ...
└─ Monatssumme                    11.50 Std

Monat: 2025-11
├─ ...
└─ Monatssumme                    10.25 Std

═══════════════════════════════════════
Gesamtstunden:                     21.75 Std
```

---

## 🚀 Verwendung

### Schritt-für-Schritt:

1. **Kunde auswählen** - Dropdown oben
2. **Einträge erstellen** - Timer oder manuell
3. **PDF exportieren** - "PDF ERSTELLEN" Button
4. **PDF öffnet sich automatisch**
5. **Teilen** - Verwenden Sie "PDF ERSTELLEN & TEILEN" direkt weiterzuleiten

### Auf Android/iOS:

- PDF öffnet sich in der Standard-App
- Tap "Teilen" im PDF-Viewer
- Wählen Sie E-Mail, WhatsApp, etc.

Oder direkt:
- "PDF ERSTELLEN & TEILEN" drücken
- Share-Dialog erscheint sofort
- App auswählen (E-Mail, Telegram, etc.)

---

## 🎨 PDF-Design

Das PDF nutzt ein modernes Material Design mit:

- **Farben**:
  - Kopfzeile: Material Blue (#1976D2)
  - Alternating Rows: Beige
  - Total Row: Light Blue (#E3F2FD)

- **Schriftarten**:
  - Title: 24px Blue Bold
  - Month Header: 16px Blue Bold
  - Content: Standard Helvetica

- **Layout**:
  - A4 Format (21 x 29.7 cm)
  - Responsive Table-Layout
  - Professioneller Look

---

## 🔧 Technische Details

### PDF-Generierung

Das PDF wird mit **reportlab** erstellt:

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# PDF wird als Bytes in den Documents-Ordner geschrieben
doc = SimpleDocTemplate(filepath, pagesize=A4)
doc.build(elements)
```

### Datei-Speicherung

PDFs werden gespeichert in:
- **Android**: `/sdcard/Android/data/org.tkideneb.zeiterfassung/files/Documents/Zeiterfassung/`
- **iOS**: `~/Documents/Zeiterfassung/`
- **Desktop**: `~/Documents/Zeiterfassung/`

Dateiname: `report_{Kundenname}.pdf`

### Teilen (Android/iOS)

```python
# Android: Nutzt FileProvider für sichere Freigabe
Intent.ACTION_SEND mit MimeType "application/pdf"

# iOS: Nutzt UIActivityViewController
Share-Dialog mit allen installierten Apps
```

---

## 📱 Mobile Builds

### Mit PDF-Support bauen:

```bash
# Alte buildozer.spec durch neue ersetzen
mv buildozer.spec buildozer_old.spec
mv buildozer_new.spec buildozer.spec

# Android mit reportlab
buildozer android debug

# iOS (auf Mac)
buildozer ios debug
```

Die buildozer.spec wurde aktualisiert mit:
```ini
requirements = python3,kivy,kivymd,pillow,plyer,pyjnius,reportlab
```

---

## 🐛 Häufige Probleme

### Problem: "ModuleNotFoundError: No module named 'reportlab'"

```powershell
# Lösung:
pip install reportlab
```

### Problem: PDF öffnet sich nicht auf Desktop

```powershell
# Windows: Sicherstellen, dass PDF-Reader installiert ist
# Mac: Sollte automatisch mit Preview funktionieren
# Linux: sudo apt install evince (PDF Viewer)
```

### Problem: Share funktioniert nicht auf Android

```
- Sicherstellen, dass App die Berechtigung hat
- Check buildozer.spec: android.permissions = ... READ_EXTERNAL_STORAGE
```

---

## 🔄 Migration von v1 zu v2

### Automatisch mit Skript:

```powershell
.\migrate_to_v2.ps1
```

### Manuell:

```powershell
# Backup alte Version
Copy-Item main.py main_v1_backup.py
Copy-Item buildozer.spec buildozer_v1.spec

# Neue Version aktivieren
Copy-Item main_new.py main.py
Copy-Item buildozer_new.spec buildozer.spec

# Dependencies
pip install reportlab
```

**Wichtig**: Ihre Datenbank bleibt erhalten - alle Kunden und Einträge sind noch da!

---

## 📊 PDF-Beispiel

Hier ist ein Beispiel, wie der PDF aussieht:

```
ZEITERFASSUNG - ACME Corp
═══════════════════════════════════════════════════════════════════

Kunde:     ACME Corp
Datum:     07.01.2026
Adresse:   Industriestraße 42, 12345 Berlin
Email:     contact@acme.corp
Telefon:   +49 30 12345678

Monat: 2025-12
┌─────────────┬──────────────────────┬────────────┐
│ Datum       │ Tätigkeit            │ Stunden    │
├─────────────┼──────────────────────┼────────────┤
│ 01.12.2025  │ Softwareentwicklung  │ 8.00       │
│ 02.12.2025  │ Code Review          │ 4.00       │
│ 03.12.2025  │ Bug Fixing           │ 6.00       │
│ 04.12.2025  │ Datenbank Design     │ 5.00       │
│ 05.12.2025  │ Testing              │ 3.00       │
├─────────────┼──────────────────────┼────────────┤
│             │ Monatssumme          │ 26.00      │
└─────────────┴──────────────────────┴────────────┘

═══════════════════════════════════════════════════════════════════
Gesamtstunden: 26.00 Std
```

---

## 🎓 Weitere Info

- Alte Version: `main.py` (v1.0 - Android only)
- Neue Version: `main_new.py` (v2.0 - iOS + Android)
- KV Layout: `zeiterfassung.kv`
- Build Config: `buildozer_new.spec`

---

**Viel Spaß mit der neuen PDF-Export-Funktion!** 🎉
