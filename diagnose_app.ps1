# Zeiterfassung App - Quick Diagnostics
Write-Host "`n=== ZEITERFASSUNG APP DIAGNOSTICS ===" -ForegroundColor Cyan

# 1. Check if device is connected
Write-Host "`n1. Checking ADB connection..." -ForegroundColor Yellow
adb devices

# 2. Check if app is installed
Write-Host "`n2. Checking if app is installed..." -ForegroundColor Yellow
adb shell pm list packages | Select-String "tkideneb2"

# 3. Try to start app and capture immediate logs
Write-Host "`n3. Starting app and capturing logs..." -ForegroundColor Yellow
Write-Host "   (If app crashes, you'll see error messages below)" -ForegroundColor Gray

# Clear old logs
adb logcat -c

# Start app
adb shell am start -n org.tkideneb2.zeiterfassung/.PoCApp

# Wait a bit for startup
Start-Sleep -Seconds 3

# Capture logs
Write-Host "`n4. Log output:" -ForegroundColor Yellow
adb logcat -d | Select-String "python|org.tkideneb2|APP|KV_POST|AndroidRuntime|FATAL" | Select-Object -First 50

Write-Host "`n=== DONE ===" -ForegroundColor Cyan
Write-Host "Wenn Sie 'FATAL' oder 'AndroidRuntime' Fehler sehen, kopieren Sie diese bitte." -ForegroundColor Red
