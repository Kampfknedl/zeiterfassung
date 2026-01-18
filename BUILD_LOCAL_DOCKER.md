# 🔨 Lokaler APK Build mit Docker

Einfaches PowerShell-Script zum lokalen Bauen der Zeiterfassung APK.

## Voraussetzungen

- **Docker Desktop** installiert: https://www.docker.com/products/docker-desktop
- Windows, Mac oder Linux

## Verwendung

```powershell
.\build-apk-local.ps1
```

Das Script wird:
1. ✓ Docker prüfen
2. ✓ kivy/buildozer Image pullen (falls nicht vorhanden)
3. ✓ APK mit Buildozer bauen (~5-15 Minuten)
4. ✓ APK im `bin/` Ordner speichern
5. ✓ Erfolgsmeldung anzeigen

## Was passiert im Hintergrund?

```bash
docker run --rm \
  -v $(pwd):/home/user/buildozer \
  kivy/buildozer \
  buildozer -v android debug
```

Das Docker-Image:
- Baut die APK vollständig isoliert
- Braucht keine lokale SDK/NDK Installation
- Alles läuft in einem Container

## Nach erfolgreichem Build

Die APK findest du hier:
```
bin/zeiterfassung-*-debug.apk
```

### APK testen

**Via ADB (Android Device Bridge):**
```powershell
adb install bin/*.apk
```

**Manuell:**
1. Datei auf Telefon kopieren (USB, Email, etc.)
2. Auf Telefon öffnen → Installation starten
3. App testen

## Troubleshooting

### Docker nicht gefunden
```
❌ Docker not found. Install Docker Desktop.
```
→ Installiere Docker Desktop von: https://www.docker.com/products/docker-desktop

### Fehler während Build
Schau in der Console-Ausgabe nach der exakten Fehlermeldung. Häufige Probleme:
- `requirements.txt` hat ungültige Packages
- `buildozer.spec` hat Syntax-Fehler
- Pfad zu Python/Java nicht gesetzt

### Disk Space voll
Docker Images brauchen ~10-15 GB. Falls Problem:
```powershell
docker system prune -a  # Räumt alte Images auf
```

## Performance-Tipps

1. **Erster Build dauert länger** (~15 min) - Image wird gecacht
2. **Spätere Builds sind schneller** (~5 min)
3. **Parallel bauen nicht möglich** - Docker braucht die Resources

## Alternativen

Falls Docker nicht gewünscht:

### Buildozer direkt (Windows/Linux)
```bash
buildozer android debug
```
Braucht aber lokale SDK/NDK Installation.

### GitHub Actions (Cloud)
Push zu GitHub → Automatischer Build (kostenlos, aber Quota-Limit)

## Logs & Debug

Das Script speichert Build-Logs. Bei Fehler:
```powershell
docker run --rm -v ${pwd}:/home/user/buildozer kivy/buildozer buildozer -v android debug 2>&1 | Tee-Object build.log
```

Dann `build.log` prüfen.
