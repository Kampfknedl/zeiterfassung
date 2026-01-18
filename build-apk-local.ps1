#!/usr/bin/env pwsh
# Build APK lokal mit Docker
# Verwendung: .\build-apk-local.ps1

Write-Host "Build APK with Docker" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

# Check Docker
Write-Host "Checking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    Write-Host "Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Docker not found" -ForegroundColor Red
    exit 1
}

# Pull image
Write-Host ""
Write-Host "Pulling Docker image..." -ForegroundColor Yellow
docker pull kivy/buildozer
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to pull Docker image" -ForegroundColor Red
    exit 1
}

# Build APK
Write-Host ""
Write-Host "Building APK (5-15 minutes)..." -ForegroundColor Yellow
$projectPath = (Get-Location).Path

docker run --rm -v "$projectPath`:/home/user/buildozer" -w /home/user/buildozer kivy/buildozer buildozer -v android debug

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Build failed" -ForegroundColor Red
    exit 1
}

# Check for APK
Write-Host ""
Write-Host "Checking for APK..." -ForegroundColor Yellow
$binPath = Join-Path $projectPath "bin"
$apkFiles = Get-ChildItem -Path $binPath -Filter "*.apk" -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

if ($apkFiles.Count -gt 0) {
    Write-Host "SUCCESS: APK built!" -ForegroundColor Green
    Write-Host ""
    foreach ($apk in $apkFiles) {
        $size = [math]::Round($apk.Length / 1MB, 2)
        Write-Host "  APK: $($apk.Name) ($size MB)" -ForegroundColor Green
    }
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  adb install bin/*.apk" -ForegroundColor Gray
} else {
    Write-Host "ERROR: No APK found" -ForegroundColor Red
    exit 1
}

Write-Host ""
