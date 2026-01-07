# Zeiterfassung - iOS & Android Version

## 🎉 Neue Features - Version 2.0

Diese App wurde komplett überarbeitet für **iOS und Android**!

### ✨ Was ist neu?

- **Material Design UI** mit KivyMD für natives Look & Feel
- **iOS Support** - funktioniert jetzt auch auf iPhone/iPad
- **Verbesserte Android-Kompatibilität**
- **Cross-Platform File Sharing** mit Plyer
- **Moderne Card-basierte UI**
- **Bessere Responsive Layouts**
- **Optimierte Performance**

---

## 🚀 Installation & Verwendung

### Desktop-Version testen (Windows/Mac/Linux)

```powershell
# Virtuelle Umgebung aktivieren
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Mac/Linux

# Dependencies installieren
pip install -r requirements.txt

# App starten (neue Version)
python main_new.py
```

---

## 📱 Mobile Apps bauen

### Android APK bauen

#### Option 1: Docker (empfohlen - keine SDK-Installation nötig)

```bash
# APK bauen
docker run --rm -v ${PWD}:/home/user/buildozer kivy/buildozer buildozer -v android debug

# APK finden
# Output: bin/zeiterfassung-2.0-debug.apk
```

#### Option 2: Direkter Buildozer (erfordert Android SDK/NDK)

```bash
# Buildozer installieren
pip install buildozer

# Alte buildozer.spec durch neue ersetzen
mv buildozer.spec buildozer_old.spec
mv buildozer_new.spec buildozer.spec

# Android APK bauen
buildozer android debug

# Release-Version (signiert)
buildozer android release
```

### iOS App bauen (nur auf macOS)

```bash
# Auf macOS ausführen

# Xcode Command Line Tools installieren
xcode-select --install

# Buildozer für iOS konfigurieren
pip install buildozer
pip install kivy-ios

# Alte Dateien durch neue ersetzen
mv main.py main_old.py
mv main_new.py main.py
mv buildozer.spec buildozer_old.spec
mv buildozer_new.spec buildozer.spec

# iOS App bauen (Debug)
buildozer ios debug

# iOS App bauen (Release für App Store)
buildozer ios release

# Xcode-Projekt öffnen für weitere Anpassungen
open .buildozer/ios/platform/build-*/YourApp.xcodeproj
```

#### iOS Codesigning konfigurieren

Für iOS-Builds müssen Sie in `buildozer.spec` Ihre Apple Developer Credentials eintragen:

```ini
ios.codesign.debug = "iPhone Developer: Ihr Name (XXXXXXXXXX)"
ios.codesign.release = "iPhone Distribution: Ihr Unternehmen"
```

---

## 🔧 Dateistruktur

```
Zeiterfassung/
├── main.py              # Alte Version (Android-only)
├── main_new.py          # Neue Version (iOS + Android) ⭐
├── zeiterfassung.kv     # UI Layout (Material Design)
├── db.py               # Datenbank-Logik
├── buildozer.spec       # Alte Build-Config
├── buildozer_new.spec   # Neue Build-Config (iOS + Android) ⭐
├── requirements.txt     # Python-Dependencies
├── icon.png            # App-Icon
└── res/
    └── xml/
        └── fileprovider_paths.xml  # Android FileProvider
```

---

## 🎨 UI-Komponenten

Die neue Version nutzt **KivyMD** für:

- **MDCard** - Material Design Cards
- **MDTextField** - Native Eingabefelder
- **MDRaisedButton** - Material Design Buttons
- **MDDialog** - Native Dialoge
- **MDList** - Scrollbare Listen
- **MDTopAppBar** - App-Bar mit Actions
- **Snackbar** - Toast-Nachrichten

---

## 📦 Dependencies

```txt
kivy          # Cross-Platform UI Framework
kivymd        # Material Design Components
pillow        # Bildverarbeitung
pyjnius       # Java Bridge (Android)
plyer         # Platform-spezifische Features
```

---

## 🐛 Bekannte Einschränkungen

### iOS
- **iOS-Builds erfordern macOS** mit Xcode
- FileSharing-Funktionalität erfordert zusätzliche iOS-spezifische Configuration
- Für App Store Veröffentlichung: Apple Developer Account erforderlich ($99/Jahr)

### Android
- Minimum Android-Version: API 21 (Android 5.0 Lollipop)
- FileProvider für sicheres File-Sharing konfiguriert

### Desktop
- Volle Funktionalität auf Windows/Mac/Linux
- Gut zum Testen vor Mobile-Build

---

## 🔄 Migration von v1.0 zu v2.0

Wenn Sie die alte Version verwenden:

```powershell
# Backup erstellen
Copy-Item main.py main_old.py
Copy-Item buildozer.spec buildozer_old.spec

# Neue Version aktivieren
Copy-Item main_new.py main.py
Copy-Item buildozer_new.spec buildozer.spec

# Neue Dependencies installieren
pip install kivymd plyer
```

Die **Datenbank bleibt kompatibel** - alle Ihre Kunden und Einträge bleiben erhalten!

---

## 📝 GitHub Actions CI/CD

Die `.github/workflows/build-apk-release.yml` kann für automatische Builds verwendet werden:

```yaml
# Passen Sie den Workflow an für neue Version:
# - Ersetzen Sie main.py durch main_new.py vor dem Build
# - Aktualisieren Sie buildozer.spec auf buildozer_new.spec
```

---

## 🎯 Nächste Schritte

1. **Desktop-Version testen**: `python main_new.py`
2. **Android APK bauen**: Docker-Befehl oben verwenden
3. **iOS Build** (wenn auf Mac): `buildozer ios debug`
4. **Alte Dateien durch neue ersetzen** wenn alles funktioniert

---

## 🆘 Hilfe & Support

### Häufige Probleme

**Problem**: iOS-Build schlägt fehl auf Windows
- **Lösung**: iOS-Builds funktionieren nur auf macOS mit Xcode

**Problem**: Android-Build dauert sehr lange
- **Lösung**: Beim ersten Build werden alle Dependencies heruntergeladen (20-30 Min normal)

**Problem**: "kivymd not found"
- **Lösung**: `pip install kivymd plyer`

**Problem**: Desktop-Version zeigt Fehler
- **Lösung**: Alte venv löschen und neu erstellen:
  ```powershell
  Remove-Item -Recurse .venv
  python -m venv .venv
  .venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```

---

## 📄 Lizenz

Diese App wurde entwickelt von **Benedikt Bernhart**.

---

## 🌟 Features im Detail

### Timer-Funktion
- Start/Pause/Stop mit Sekundengenauer Erfassung
- Automatische Rundung auf 0.25h-Schritte
- Pause-Zeit wird korrekt abgezogen

### Kunden-Verwaltung
- Kunden mit Adresse, Email, Telefon
- Bearbeiten und Löschen
- Automatische Sortierung

### Export & Teilen
- CSV-Export mit Monatssummen
- Direktes Teilen via native Share-Dialoge
- Speicherung in Documents-Ordner

### Cross-Platform
- Erkennt automatisch Android/iOS/Desktop
- Passt File-Handling an Platform an
- Native Look & Feel auf allen Plattformen

---

Viel Erfolg mit der neuen iOS & Android Version! 🎉
