# GitHub Repository Setup für Zeiterfassung APK Builder

## Schritt 1: Neues GitHub Repository erstellen

1. Gehe zu https://github.com/new
2. Repository Name: `zeiterfassung` (oder dein Wunschname)
3. Beschreibung: "Android time tracking app with Kivy - Built for Galaxy S24+ (Android 16/API 35)"
4. Sichtbarkeit: **Public** (erforderlich für kostenlose GitHub Actions)
5. Klicke "Create repository"

## Schritt 2: Repository lokal initialisieren

```powershell
cd c:\Users\Bene\Desktop\Python_Programme

# Git initialisieren (falls noch nicht geschehen)
git init
git add .
git commit -m "Initial commit - Zeiterfassung App"

# Remote hinzufügen (DEIN_USERNAME ersetzen)
git remote add origin https://github.com/DEIN_USERNAME/zeiterfassung.git

# Auf main branch wechseln
git branch -M main

# Hochladen
git push -u origin main
```

## Schritt 3: GitHub Actions Workflow überprüfen

1. Gehe zu deinem GitHub Repository
2. Klicke auf "Actions" Tab
3. Du solltest "Build APK for Android 16 (Galaxy S24+)" sehen
4. Der Workflow startet automatisch bei jedem Push zu `main` oder `develop`

## Schritt 4: APK manuell bauen

### Option A: GitHub Actions (empfohlen)
1. Gehe zu "Actions" → "Build APK for Android 16"
2. Klicke "Run workflow" → "Run workflow"
3. Warte ~10-15 Minuten
4. Nach dem Build: "Artifacts" → Download "APK-Android16"

### Option B: Lokal mit Docker
```powershell
# Docker muss installiert sein
docker run --rm -v $(pwd):/home/user/buildozer -w /home/user/buildozer kivy/buildozer buildozer -v android release
```

## Wichtige Dateien

- **buildozer_android16.spec**: Konfiguration für Android 16 (API 35) - Galaxy S24+
- **.github/workflows/build-apk-android16.yml**: GitHub Actions Workflow
- **main.py**: Kivy App (bei Änderungen neu builden)
- **db.py**: SQLite Datenbank

## Troubleshooting

### APK startet nicht?
- Überprüfe: `Android 16 ist API 35, nicht API 36`
- Galaxy S24+ läuft aktuell Android 14-15, aber API 35 ist kompatibel
- Wenn Absturz: Aktiviere Logcat
```powershell
adb logcat | grep zeiterfassung
```

### Build fehlgeschlagen?
- Überprüfe Workflow Logs in GitHub Actions
- Stelle sicher, dass `.github/workflows/build-apk-android16.yml` existiert
- Verwende immer `buildozer_android16.spec` (nicht die alte Datei)

### APK Key Fehler
Der neue Workflow erstellt automatisch einen neuen Key für dein Repository. Der alte Key funktioniert nicht mehr, da er wahrscheinlich in die `buildozer.spec` hardcoded war.

## App auf Galaxy S24+ installieren

```powershell
# APK von Artifacts herunterladen, dann:
adb install -r bin/zeiterfassung-2.0-release-unsigned.apk

# Oder über USB Installation:
# 1. APK auf Handy kopieren
# 2. Dateimanager → APK tippen → Installieren
```

## Wichtig für Android 16!

Android 16 (API 35) benötigt:
- ✅ `android.api = 35` in buildozer.spec
- ✅ `android.target_api = 35` 
- ✅ Moderne Gradle-Dependencies (androidx.core 1.12.0+)
- ✅ Berechtigung `READ_MEDIA_DOCUMENTS` statt `READ_EXTERNAL_STORAGE` (optional, für zukünftige Versionen)

Die `buildozer_android16.spec` hat alle diese Einstellungen!

---

**Nächste Schritte:**
1. GitHub Account verknüpfen
2. Repository erstellen
3. Code hochladen (`git push`)
4. Workflow automatisch starten oder manuell triggern
5. APK innerhalb von 10-15 Minuten herunterladen ✅
