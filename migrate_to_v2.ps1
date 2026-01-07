# Migration Script - Wechsel zur iOS/Android-Version
# Dieses Skript aktiviert die neue Version

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Zeiterfassung v2.0 Migration" -ForegroundColor Cyan
Write-Host "iOS & Android Support" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

# Backup erstellen
Write-Host "[1/4] Erstelle Backups..." -ForegroundColor Yellow
if (Test-Path "main.py") {
    Copy-Item "main.py" "main_old_backup.py" -Force
    Write-Host "  ✓ main.py -> main_old_backup.py" -ForegroundColor Green
}

if (Test-Path "buildozer.spec") {
    Copy-Item "buildozer.spec" "buildozer_old_backup.spec" -Force
    Write-Host "  ✓ buildozer.spec -> buildozer_old_backup.spec" -ForegroundColor Green
}

# Neue Dateien aktivieren
Write-Host "`n[2/4] Aktiviere neue Version..." -ForegroundColor Yellow
if (Test-Path "main_new.py") {
    Copy-Item "main_new.py" "main.py" -Force
    Write-Host "  ✓ main_new.py -> main.py" -ForegroundColor Green
} else {
    Write-Host "  ✗ main_new.py nicht gefunden!" -ForegroundColor Red
    exit 1
}

if (Test-Path "buildozer_new.spec") {
    Copy-Item "buildozer_new.spec" "buildozer.spec" -Force
    Write-Host "  ✓ buildozer_new.spec -> buildozer.spec" -ForegroundColor Green
} else {
    Write-Host "  ✗ buildozer_new.spec nicht gefunden!" -ForegroundColor Red
    exit 1
}

# Dependencies installieren
Write-Host "`n[3/4] Installiere neue Dependencies..." -ForegroundColor Yellow
$venvPath = ".venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    & $venvPath
    pip install kivymd plyer --quiet
    Write-Host "  ✓ kivymd und plyer installiert" -ForegroundColor Green
} else {
    Write-Host "  ! Virtuelle Umgebung nicht gefunden" -ForegroundColor Yellow
    Write-Host "    Bitte manuell ausführen:" -ForegroundColor Yellow
    Write-Host "    pip install kivymd plyer" -ForegroundColor Yellow
}

# Zusammenfassung
Write-Host "`n[4/4] Migration abgeschlossen!" -ForegroundColor Green
Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "Neue Features aktiviert:" -ForegroundColor Cyan
Write-Host "  ✓ iOS Support" -ForegroundColor Green
Write-Host "  ✓ Android Support (verbessert)" -ForegroundColor Green
Write-Host "  ✓ Material Design UI" -ForegroundColor Green
Write-Host "  ✓ Cross-Platform File Sharing" -ForegroundColor Green
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "Nächste Schritte:" -ForegroundColor Yellow
Write-Host "1. Desktop testen:  python main.py" -ForegroundColor White
Write-Host "2. Android bauen:   buildozer android debug" -ForegroundColor White
Write-Host "3. iOS bauen (Mac): buildozer ios debug`n" -ForegroundColor White

Write-Host "Backups erstellt:" -ForegroundColor Yellow
Write-Host "  - main_old_backup.py" -ForegroundColor White
Write-Host "  - buildozer_old_backup.spec`n" -ForegroundColor White

Write-Host "Weitere Infos: README_NEW.md`n" -ForegroundColor Cyan
