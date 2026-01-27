# Docker Build - Fehleranalyse & Lösungen

## Identifiziertes Problem

### 1. **Build steckt fest bei P4A/Gradle-Phase**
- Das Log endet plötzlich bei: `zeiterfassung has compatible recipes, using this one`
- **Symptom**: Der Prozess hängt und erstellt keine APK
- **Wahrscheinliche Ursache**: 
  - NDK-Kompilierung läuft noch (lange Compilation für arm64-v8a + armeabi-v7a)
  - Memory-Limit des Docker Containers
  - Gradle-Mutex-Problem oder Deadlock

### 2. **Probleme in buildozer.spec**
- ✗ Zu viele Dateien im Build einbezogen (`.json`, `.log`, `.sqlite` Dateien)
- ✗ Fehlende ccache-Optimierung
- ✗ Keine Gradle-Optimierungen

### 3. **Docker-Image suboptimal konfiguriert**
- ✗ Kein ccache installiert (Rebuild dauert länger)
- ✗ Keine Gradle-Properties konfiguriert
- ✗ Memory-Limits nicht festgelegt

## Implementierte Lösungen

### 1. **Dockerfile optimiert** ✓
```dockerfile
# Hinzugefügt:
- ccache (Cache für C/C++ Builds)
- Gradle-Optimierungen (JVM memory, parallel builds)
- --no-install-recommends (kleineres Image)
- Warnings-Filter für saubere Ausgabe
```

### 2. **buildozer.spec erweitert** ✓
```ini
# Neue Excludes:
*.json       # Verhindert Config-Dateien im Build
*.log        # Verhindert Log-Dateien im Build
*.sqlite     # Verhindert Database-Dateien im Build
*.db3        # Verhindert Database-Dateien im Build
```

### 3. **Neues Build-Skript** ✓
- `build-apk-simple.ps1`: Einfacher, robuster Builder
- Bessere Fehlerbehandlung
- Detailliertes Logging
- Automatische APK-Verifizierung

## Nächste Schritte

### Sofort Test:
```powershell
# 1. Docker-Image vollständig bauen (braucht ~3-5 Min)
docker build -t zeiterfassung-buildozer:latest .

# 2. APK mit optimiertem Dockerfile bauen
./build-apk-simple.ps1 debug

# 3. Wenn immer noch hängt: 
# → Erhöhe Gradle Memory oder reduziere .archs auf nur arm64-v8a
```

## Debugging-Tipps

Wenn der Build immer noch hängt:

### Option 1: Mit Timeout laufen
```powershell
$TimeoutSeconds = 1800  # 30 Minuten
docker run --rm `
  --memory="4g" `
  -v "${PWD}:/app" `
  -w /app `
  zeiterfassung-buildozer:latest `
  timeout 1800 buildozer -v android debug
```

### Option 2: Nur eine Architektur bauen (schneller)
Ändere in `buildozer.spec`:
```ini
android.archs = arm64-v8a  # Nicht: arm64-v8a,armeabi-v7a
```

### Option 3: GitHub Actions verwenden (Cloud-Build)
```powershell
# Push to GitHub und lasse GitHub-Actions den Build machen
git push origin main
# Dann in GitHub → Actions → "Build APK (Release)" → Run workflow
```

## Konfiguration für Produktion

Wenn Build funktioniert, hier sind weitere Optimierungen:

### buildozer.spec Empfehlungen:
```ini
# Für schnellere Iterationen:
p4a.ndk_api = 21           # Minimal API
android.archs = arm64-v8a  # Nur 64-bit (modern phones)

# Für maximale Kompatibilität:
android.archs = arm64-v8a,armeabi-v7a,x86_64
android.api = 33           # API 34 ist zu neu für manche Geräte
```

### Docker Memory-Limits:
```powershell
# Wenn immer noch Speicher-Fehler auftreten:
docker run --rm `
  --memory="6g" `
  --memswap="8g" `
  -v "${PWD}:/app" `
  -w /app zeiterfassung-buildozer:latest `
  buildozer -v android debug
```

## Status nach dieser Korrektur

- ✅ Dockerfile optimiert
- ✅ buildozer.spec bereinigt
- ✅ Neues Build-Skript erstellt
- ⏳ Wartet auf Test-Build
- ⏳ APK-Generierung überprüfen
