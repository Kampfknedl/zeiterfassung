# Zeiterfassung - Android App

Eine Kivy-basierte Zeiterfassungsanwendung für Android mit Kundenverwaltung und PDF-Export.

## 🚀 Automatischer APK-Build via GitHub Actions

Diese Repository hat GitHub Actions konfiguriert, um automatisch eine APK zu bauen und bereitzustellen.

### APK herunterladen

1. **Gehe zu:** [GitHub Actions](../../actions) oder [Releases](../../releases)
2. **Klicke auf den neuesten Build** unter "Build and Release APK"
3. **Scrolle nach unten** zu "Artifacts"
4. **Lade die APK herunter:** `zeiterfassung-apk.zip`
5. **Entpacke die ZIP-Datei** und installiere die APK auf dein Android-Gerät

### Manueller Trigger des Builds

Falls du einen neuen Build manuell starten möchtest:

1. Gehe zu [Actions → Build and Release APK](../../actions/workflows/build-apk-release.yml)
2. Klicke auf **"Run workflow"** (rechts oben, grüner Button)
3. Bestätige mit **"Run workflow"**
4. Warte auf die Fertigstellung (dauert ca. 3-5 Minuten)

### Build-Status

![Build Status](../../workflows/Build%20and%20Release%20APK/badge.svg)

---

## 📱 Features

- ✅ Kundenverwaltung mit Kontaktdaten
- ✅ Stundenerfassung mit Datum
- ✅ PDF-Export für Reports
- ✅ **Direktes PDF-Sharing via Email, WhatsApp, Google Drive etc.**
- ✅ Automatische Monatszusammenstellung
- ✅ Timer-Funktion für Stundentracking
- ✅ Android 5+ Support (FileProvider API 24+)

## 🛠 Lokale Entwicklung

### Voraussetzungen

- Python 3.9+
- Kivy Framework
- fpdf2 für PDF-Export

### Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Lokal testen

```bash
python main.py
```

### APK lokal bauen (mit Buildozer + Docker)

```bash
# Option 1: Mit Docker (empfohlen)
docker run --rm -v $(pwd):/home/user/buildozer kivy/buildozer buildozer -v android debug

# Option 2: Mit Buildozer (benötigt Java SDK + Android SDK/NDK)
pip install buildozer
buildozer android debug
```

Die fertige APK findest du in `bin/`.

---

## � PDF-Sharing Funktion

Die Anwendung unterstützt direktes PDF-Sharing ohne zusätzliche Schritte:

### Verwendung

1. **Wähle einen Kunden** aus dem Dropdown-Menü
2. **Klick auf "Report (PDF)"** oder **"Report + Teilen"**
3. **PDF wird erzeugt** und dir wird ein Dialog angezeigt
4. **Klick auf "📤 Teilen"** um die PDF direkt zu teilen via:
   - Email
   - WhatsApp
   - Google Drive
   - OneDrive
   - Telegram
   - oder jede andere Sharing-App auf dem Gerät

### Technische Details

- **FileProvider**: Nutzt `androidx.core.content.FileProvider` für sichere PDF-Freigabe (API 24+)
- **Speicherort**: Dateien werden in `Android/data/<app>/files/Documents/` gespeichert
- **Automatisches Sharing**: Der Button "Report + Teilen" öffnet direkt den Share-Dialog
- **Fallback**: Desktop-Version speichert PDFs in `~/Documents/Zeiterfassung/`

### Konfiguration (buildozer.spec)

Die FileProvider-Konfiguration ist bereits eingerichtet:

```ini
android.add_resources = res
android.gradle_dependencies = androidx.core:core:1.9.0
android.manifest_additions = <provider android:name="androidx.core.content.FileProvider" .../>
```

---

## �📁 Projektstruktur

```
.
├── main.py              # Hauptanwendung
├── db.py                # Datenbank-Management
├── buildozer.spec       # Build-Konfiguration
├── requirements.txt     # Python-Dependencies
├── res/
│   └── xml/
│       └── fileprovider_paths.xml  # Android FileProvider Konfiguration
├── icon.png             # App-Icon
└── .github/workflows/
    └── build-apk-release.yml  # GitHub Actions Workflow
```

---

## 🐛 Troubleshooting

### "resource xml/fileprovider_paths not found"

Die Datei `res/xml/fileprovider_paths.xml` muss existieren. Sie ist bereits vorhanden, aber stelle sicher, dass `buildozer.spec` diese enthält:

```ini
android.add_res_dirs = res
android.meta_data = android.support.FILE_PROVIDER_PATHS=@xml/fileprovider_paths
```

### Build fehlgeschlagen

Schau in die [Actions](../../actions) und prüfe die Buildozer-Logs:

1. Öffne den fehlgeschlagenen Build
2. Scrolle zu "Artifacts"
3. Lade `buildozer-logs` herunter

---

## 📄 Lizenz

MIT

## 👤 Autor

Erstellt mit Kivy
