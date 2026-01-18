#!/usr/bin/env pwsh
# Einfaches lokales APK Build-Skript

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Building Zeiterfassung APK" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = (Get-Location).Path

# Check buildozer.spec
if (-not (Test-Path "buildozer.spec")) {
    Write-Host "ERROR: buildozer.spec not found" -ForegroundColor Red
    exit 1
}

Write-Host "Config: buildozer.spec loaded" -ForegroundColor Green
Write-Host "Target: Android Debug APK" -ForegroundColor Green
Write-Host ""
Write-Host "Starting build..." -ForegroundColor Yellow
Write-Host "This may take 10-20 minutes..." -ForegroundColor Gray
Write-Host ""

# Build mit buildozer
buildozer -v android debug

$success = $LASTEXITCODE -eq 0

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan

if ($success) {
    $binPath = Join-Path $projectPath "bin"
    $apk = Get-ChildItem -Path $binPath -Filter "zeiterfassung-*.apk" -ErrorAction SilentlyContinue | 
           Sort-Object LastWriteTime -Descending | 
           Select-Object -First 1
    
    if ($apk) {
        $size = [math]::Round($apk.Length / 1MB, 2)
        Write-Host ""
        Write-Host "SUCCESS: APK created!" -ForegroundColor Green
        Write-Host ""
        Write-Host "File: $($apk.Name)" -ForegroundColor Green
        Write-Host "Size: $size MB" -ForegroundColor Gray
        Write-Host "Path: $($apk.FullName)" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "  adb install '$($apk.FullName)'" -ForegroundColor White
    }
} else {
    Write-Host "BUILD FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check buildozer.spec configuration" -ForegroundColor Gray
    Write-Host "  2. Check requirements.txt dependencies" -ForegroundColor Gray
    Write-Host "  3. Ensure all source files exist (main_new.py, db.py, etc.)" -ForegroundColor Gray
}

Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

exit ($success ? 0 : 1)
