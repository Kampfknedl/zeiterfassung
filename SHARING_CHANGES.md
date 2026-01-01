# PDF-Sharing Feature - Implementierung

## 🎯 Ziel
Die PDF-Reports können nun direkt geteilt werden via Email, WhatsApp, Google Drive, OneDrive, Telegram etc.

## ✅ Implementierte Änderungen

### 1. **main.py** - Neue Share-Funktion
- **`share_pdf_fileprovider(filepath)`** - Neue Hauptfunktion
  - Nutzt `androidx.core.content.FileProvider` für sichere URI-Generierung
  - Unterstützt API 24+ (Android 7+)
  - Erstellt einen `ACTION_SEND` Intent mit Share-Dialog
  - Gibt `True/False` zurück für Fehlerbehandlung

### 2. **show_pdf_viewer()** - Erweiterte Popup-Funktion
Hinzugefügte Buttons im Report-Dialog:
- **"📤 Teilen"** - Ruft `share_pdf_fileprovider()` auf
- **"🔍 Öffnen"** - Öffnet PDF mit Standard-Viewer
- **"✓ OK"** - Schließt Dialog

### 3. **export_pdf(auto_share=True)** - Auto-Share Support
- Wenn `auto_share=True` wird aufgerufen, zeigt sich der Dialog + Share wird automatisch getriggert
- Beide Buttons ("Report (PDF)" und "Report + Teilen") zeigen jetzt einen Dialog mit Share-Option

### 4. **buildozer.spec** - Android-Konfiguration
```ini
android.add_resources = res
android.gradle_dependencies = androidx.core:core:1.9.0
android.manifest_additions = <provider android:name="androidx.core.content.FileProvider" 
                               android:authorities="org.tkideneb.zeiterfassung.fileprovider" 
                               android:exported="false">
                               <meta-data android:name="android.support.FILE_PROVIDER_PATHS" 
                                         android:resource="@xml/fileprovider_paths" />
                             </provider>
```

### 5. **res/xml/fileprovider_paths.xml** - Bereits vorhanden
Definiert welche Dateien geteilt werden dürfen:
```xml
<external-path name="documents" path="Documents/" />
<external-files-path name="external_files" path="." />
```

### 6. **README.md** - Dokumentation
- Neue Sektion "📤 PDF-Sharing Funktion" mit Anleitung
- Technische Details erklärt
- Konfigurationsbeispiele

## 🔒 Sicherheit
- **FileProvider**: Sicherer als `file://` URIs (API 24+)
- **Restricted Access**: Nur explizit erlaubte Dateien können geteilt werden
- **Permission Handling**: Keine zusätzlichen Runtime-Permissions nötig (FileProvider übernimmt das)

## 🚀 Verwendung

### Desktop (Windows/Mac/Linux)
```bash
python main.py
# PDF wird erstellt und kann manuell geöffnet werden
```

### Android
1. Kunde auswählen
2. Einträge hinzufügen
3. **"Report (PDF)"** oder **"Report + Teilen"** klicken
4. Im Dialog auf **"📤 Teilen"** klicken
5. Wähle: Email, WhatsApp, Google Drive, etc.

## 📋 Kompatibilität
- ✅ Android 5.0+ (API 21+) - mit FileProvider
- ✅ Android 7.0+ (API 24+) - optimal
- ✅ Desktop (Windows/Mac/Linux)

## 🔧 Troubleshooting

### "FileProvider share failed"
- Stelle sicher, dass `buildozer.spec` die FileProvider-Config enthält
- Prüfe, dass `res/xml/fileprovider_paths.xml` existiert
- Die APK muss mit den neuen Konfigurationen neu gebaut werden

### "android.os.FileUriExposedException"
- Betrifft nur alte API-Levels
- FileProvider-Code sollte das umgehen
- Fallback zu `file://` URI ist implementiert (Android 6 und älter)

## 📦 Dependencies
Keine neuen Dependencies! Alles wurde mit bereits vorhandenen Paketen implementiert:
- `pyjnius` - Für Android Java Interop
- `kivy` - Für UI
- `fpdf` - Für PDF-Generierung
- `androidx.core:core:1.9.0` - Für FileProvider (Gradle-Dependency)

## ✨ Nächste Schritte
1. APK neu bauen: `docker run --rm -v $(pwd):/home/user/buildozer kivy/buildozer buildozer -v android debug`
2. Auf Android-Gerät testen
3. "Report + Teilen" Button clicken und Sharing-Dialog testen
