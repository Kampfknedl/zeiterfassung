#!/usr/bin/env pwsh
<#
.SYNOPSIS
Einfacher Docker APK Builder für Zeiterfassung
.DESCRIPTION
Erstellt Android APK mit Buildozer im Docker Container
#>

param(
    [ValidateSet("debug", "release")]
    [string]$BuildType = "debug"
)

$ErrorActionPreference = "Stop"

# Farben für Ausgabe
$colors = @{
    Info    = "Cyan"
    Success = "Green"
    Error   = "Red"
    Warning = "Yellow"
}

function Write-Log {
    param([string]$Message, [string]$Type = "Info")
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] " -NoNewline -ForegroundColor DarkGray
    Write-Host $Message -ForegroundColor $colors[$Type]
}

function Main {
    Clear-Host
    Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "Zeiterfassung APK Builder (Docker)" -ForegroundColor Cyan
    Write-Host "═══════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""

    # 1. Docker-Image bauen
    Write-Log "Schritt 1: Baue Docker-Image..." "Info"
    Write-Log "Dies kann 1-2 Minuten dauern..." "Warning"
    
    docker build -t zeiterfassung-buildozer:latest -f Dockerfile . 2>&1 | Out-Null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Log "Docker-Image-Build fehlgeschlagen" "Error"
        exit 1
    }
    Write-Log "✓ Docker-Image gebaut" "Success"
    Write-Host ""

    # 2. APK bauen
    Write-Log "Schritt 2: Baue APK ($BuildType)..." "Info"
    Write-Log "Dies kann 10-30 Minuten dauern..." "Warning"
    Write-Host ""

    $projectPath = (Get-Location).Path
    $logFile = Join-Path $projectPath "build_docker_$BuildType.log"

    # Starte Build mit Logging
    Write-Log "Buildozer läuft... Output wird in $logFile gespeichert" "Info"
    
    docker run --rm `
        -v "${projectPath}:/app" `
        -w /app `
        zeiterfassung-buildozer:latest `
        buildozer -v android $BuildType 2>&1 | Tee-Object -FilePath $logFile

    if ($LASTEXITCODE -ne 0) {
        Write-Log "Build fehlgeschlagen. Siehe $logFile für Details" "Error"
        Write-Log "Letzte 50 Zeilen des Logs:" "Warning"
        Get-Content $logFile -Tail 50
        exit 1
    }

    Write-Host ""
    Write-Log "✓ APK erfolgreich gebaut!" "Success"
    Write-Host ""

    # 3. Suche die APK
    Write-Log "Schritt 3: Verifiziere APK..." "Info"
    
    $binPath = Join-Path $projectPath "bin"
    $apkFiles = Get-ChildItem -Path $binPath -Filter "zeiterfassung-*.apk" -ErrorAction SilentlyContinue | 
        Sort-Object LastWriteTime -Descending

    if ($apkFiles.Count -eq 0) {
        Write-Log "WARNUNG: APK-Datei nicht gefunden im bin/ Verzeichnis" "Warning"
        exit 1
    }

    $apk = $apkFiles[0]
    $sizeMB = "{0:N2}" -f ($apk.Length / 1MB)

    Write-Host ""
    Write-Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Success"
    Write-Log "APK fertig!" "Success"
    Write-Log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Success"
    Write-Log "Datei: $($apk.Name)" "Info"
    Write-Log "Größe: $sizeMB MB" "Info"
    Write-Log "Pfad: $($apk.FullName)" "Info"
    Write-Log "Erstellt: $($apk.LastWriteTime)" "Info"
    Write-Host ""

    # 4. Installation anbieten
    if (Get-Command adb -ErrorAction SilentlyContinue) {
        Write-Log "adb gefunden. Installation möglich:" "Info"
        Write-Host "  adb install ""$($apk.FullName)""" -ForegroundColor Green
    } else {
        Write-Log "adb nicht gefunden. APK manuell kopieren oder installieren." "Warning"
    }

    Write-Host ""
    Write-Log "Build komplett! ✓" "Success"
}

try {
    Main
} catch {
    Write-Log "Fehler: $_" "Error"
    exit 1
}
