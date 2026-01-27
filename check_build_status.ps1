# Build Status Checker
Write-Host "`n=== ZEITERFASSUNG BUILD STATUS ===" -ForegroundColor Cyan

# Check if Docker container is running
$dockerRunning = docker ps --format "{{.Command}}" | Select-String "buildozer"
if ($dockerRunning) {
    Write-Host "✓ Docker Build läuft..." -ForegroundColor Green
} else {
    Write-Host "✗ Kein Build-Container aktiv" -ForegroundColor Red
}

# Check build log
if (Test-Path "build_log.txt") {
    $logSize = (Get-Item "build_log.txt").Length / 1KB
    Write-Host "✓ Build Log: $([math]::Round($logSize, 1)) KB" -ForegroundColor Gray
    
    # Show last few lines
    Write-Host "`nLetzte Log-Einträge:" -ForegroundColor Yellow
    Get-Content "build_log.txt" -Tail 10
}

# Check for APK
if (Test-Path "bin") {
    $apks = Get-ChildItem -Path "bin" -Filter "*.apk" -ErrorAction SilentlyContinue
    if ($apks) {
        Write-Host "`n✓ APK gefunden!" -ForegroundColor Green
        foreach ($apk in $apks) {
            $size = [math]::Round($apk.Length / 1MB, 2)
            Write-Host "  - $($apk.Name) ($size MB)" -ForegroundColor White
        }
    } else {
        Write-Host "`n⏳ Noch keine APK (Build läuft noch)" -ForegroundColor Yellow
    }
}

Write-Host "`n=================================`n" -ForegroundColor Cyan
