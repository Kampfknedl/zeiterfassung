@echo off
REM GitHub Push Script für Zeiterfassung APK Build
REM Pushed Code zu GitHub und startet den Build-Workflow

echo.
echo ╔═══════════════════════════════════════════════════════════╗
echo ║   ZEITERFASSUNG v2.0 - GitHub APK Build                   ║
echo ║   Material Design UI + PDF Export + Cross-Platform        ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git nicht installiert!
    echo Installiere Git von https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Check if we're in a git repository
if not exist ".git" (
    echo ❌ Nicht in einem Git-Repository!
    echo Dieses Skript muss im Projektordner ausgeführt werden.
    pause
    exit /b 1
)

echo 📦 Status prüfen...
git status --short
echo.

echo 🔧 Neue Dateien zum Commit hinzufügen...
git add -A

echo.
echo 💬 Commit Message eingeben (oder Enter für Default):
set /p commit_msg="Commit Message (Default: 'Update Zeiterfassung v2.0'): "
if "%commit_msg%"=="" set commit_msg=Update Zeiterfassung v2.0

git commit -m "%commit_msg%"
if errorlevel 1 (
    echo ⚠️ Commit fehlgeschlagen oder bereits committed
)

echo.
echo 📤 Zu GitHub pushen...
git push origin main
if errorlevel 1 (
    echo ❌ Push fehlgeschlagen!
    echo Prüfe deine GitHub-Verbindung und Permissions
    pause
    exit /b 1
)

echo.
echo ✅ Code erfolgreich zu GitHub gepusht!
echo.
echo 🚀 Nächste Schritte:
echo    1. Gehe zu: https://github.com/Tkideneb2/Zeiterfassung
echo    2. Klicke auf "Actions"
echo    3. Wähle "Build APK"
echo    4. Klicke "Run workflow"
echo    5. Warte auf den Build (ca. 15-20 Min)
echo    6. Download APK aus Artifacts
echo.
pause
