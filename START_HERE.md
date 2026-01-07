# 🚀 SCHNELLEINSTIEG - Zeiterfassung v2.0

## ⚡ 3 Sekunden Start

Doppelklick auf:
```
start.bat
```

Dann wähle Option `1) App starten`

---

## 📋 Was wurde geändert?

✅ **iOS & Android Support** (statt nur Android)
✅ **Material Design UI** (modernes Aussehen)
✅ **PDF Export** (automatisch öffnend + teilbar)
✅ **100% Daten-kompatibel** (alle Kunden/Einträge bleiben)

---

## 🎯 Die wichtigsten Dateien

### Zum Starten:
- **start.bat** ← Doppelklick zum Starten! 🎉
- **main_new.py** - Die neue App (v2.0)

### Dokumentation:
- **UPGRADE_GUIDE.md** - Quick Start & Migration
- **PDF_EXPORT_GUIDE.md** - PDF-Funktionen
- **CHANGES_SUMMARY.md** - Was hat sich geändert

### Testing:
- **test_pdf_export.py** - PDF-Test durchführen
- **test_report.pdf** - Beispiel PDF (vom Test)

### Alte Version (Backup):
- **main.py** - Alte Version (still funktioniert)
- **README.md** - Alte Dokumentation

---

## 💻 Manuelle Commands

```powershell
# App starten
python main_new.py

# PDF-Test
python test_pdf_export.py

# Upgrade
.\migrate_to_v2.ps1

# Abhängigkeiten
pip install -r requirements.txt
```

---

## 🎨 Neue Features - Kurz erklärt

### PDF Export 📄
- Klick: **"PDF ERSTELLEN"**
- PDF öffnet sich automatisch
- Klick: **"PDF ERSTELLEN & TEILEN"** um direkt zu teilen
- Professionelles Design mit Kundeninformationen

### Material Design 🎨
- Modernes, farbenfrohes Interface
- Native Buttons und Cards
- Besseres Aussehen auf Handys

### iOS Support 📱
- App funktioniert jetzt auch auf iPhone/iPad
- Same Features wie Android

---

## 📱 Für Mobile (Android/iOS)

```bash
# Android APK bauen (mit Docker)
docker run --rm -v %cd%:/home/user/buildozer kivy/buildozer buildozer -v android debug

# iOS (nur auf Mac mit Xcode)
buildozer ios debug
```

---

## ❓ Häufige Fragen

**Q: Sind meine Daten weg?**
A: Nein! 100% kompatibel. Alle Kunden und Einträge bleiben.

**Q: Kann ich die alte Version noch nutzen?**
A: Ja, `main.py` ist noch da.

**Q: Wie teile ich PDFs?**
A: Klick "PDF ERSTELLEN & TEILEN" → choose App (Email, WhatsApp, etc.)

**Q: Funktioniert das auf meinem Handy?**
A: Android 5.0+ oder iOS 12.0+. Generelle Info siehe UPGRADE_GUIDE.md

---

## 🛠️ Troubleshooting

**App startet nicht?**
```powershell
pip install -r requirements.txt
python main_new.py
```

**PDF funktioniert nicht?**
```powershell
pip install reportlab
```

**Weitere Probleme?**
Siehe: **UPGRADE_GUIDE.md** → Troubleshooting

---

## 📚 Weitere Infos

```
📖 UPGRADE_GUIDE.md        - Komplette Anleitung
📖 PDF_EXPORT_GUIDE.md     - PDF-Dokumentation  
📖 README_NEW.md           - Feature-Details
📖 CHANGES_SUMMARY.md      - Was sich geändert hat
```

---

## ✨ Zusammenfassung

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Android | ✅ | ✅ |
| iOS | ❌ | ✅ |
| Desktop | ✓ Limited | ✅ Voll |
| CSV Export | ✅ | ✅ |
| PDF Export | ❌ | ✅ |
| PDF Sharing | ❌ | ✅ |
| Material Design | ❌ | ✅ |

---

## 🎉 Let's Go!

1. **Doppelklick** `start.bat`
2. Wähle `1`
3. Viel Spaß! 🎊

---

*Made by Benedikt Bernhart*
*Zeiterfassung v2.0 - Production Ready* ✅
