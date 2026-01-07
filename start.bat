@echo off
REM Quick Start Script für Zeiterfassung v2.0

echo.
echo ================================================================
echo   ZEITERFASSUNG v2.0 - iOS & Android mit PDF Export
echo ================================================================
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo [!] Virtuelle Umgebung nicht gefunden!
    echo.
    echo Erstelle virtuelle Umgebung...
    python -m venv .venv
    echo [✓] Virtuelle Umgebung erstellt
    echo.
)

REM Activate venv
call .venv\Scripts\activate.bat

REM Check dependencies
echo [*] Überprüfe Abhängigkeiten...
pip show kivymd > nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Abhängigkeiten fehlen, installiere diese...
    pip install -r requirements.txt -q
    echo [✓] Abhängigkeiten installiert
    echo.
)

REM Menu
:menu
echo.
echo ================================================================
echo   MENÜ - Wähle eine Option:
echo ================================================================
echo.
echo   1) App starten (Desktop Version)
echo   2) Test PDF-Export durchführen
echo   3) Auf neue Version v2.0 upgraden
echo   4) Abhängigkeiten neu installieren
echo   5) Exit
echo.
set /p choice="Wähle Option (1-5): "

if "%choice%"=="1" (
    cls
    echo [*] Starte Zeiterfassung v2.0...
    echo.
    python main_new.py
    goto menu
)

if "%choice%"=="2" (
    cls
    echo [*] Teste PDF-Export mit Demo-Daten...
    echo.
    python test_pdf_export.py
    echo.
    echo [✓] PDF erstellt: test_report.pdf
    echo    Öffne die Datei um das Ergebnis zu sehen.
    echo.
    pause
    goto menu
)

if "%choice%"=="3" (
    cls
    echo [*] Upgrade zu v2.0...
    echo.
    powershell -File migrate_to_v2.ps1
    echo.
    pause
    goto menu
)

if "%choice%"=="4" (
    cls
    echo [*] Installiere Abhängigkeiten neu...
    echo.
    pip install --upgrade -r requirements.txt
    echo.
    echo [✓] Abhängigkeiten aktualisiert
    echo.
    pause
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo Auf Wiedersehen!
    echo.
    exit /b 0
)

echo [!] Ungültige Option. Versuche es nochmal.
goto menu
