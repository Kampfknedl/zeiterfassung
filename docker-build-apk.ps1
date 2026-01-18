#!/usr/bin/env pwsh
<#
.SYNOPSIS
Docker-basierter APK Builder für Zeiterfassung
.DESCRIPTION
Erstellt eine Android APK mit Docker (keine lokale SDK-Installation erforderlich)
#>

param(
    [ValidateSet("debug", "release")]
    [string]$BuildType = "debug",
    
    [switch]$SkipDockerPull,
    [switch]$KeepContainerLogs,
    [switch]$AutoInstall,
    [switch]$OpenFinder
)

# ============================================================================
# KONFIGURATION
# ============================================================================
$DOCKER_IMAGE = "kivy/buildozer"
$DOCKER_TAG = "latest"
$PROJECT_NAME = "Zeiterfassung"
$APK_NAME_PATTERN = "zeiterfassung-*.apk"

# Farben
$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"
$ColorGray = "DarkGray"

# ============================================================================
# FUNKTIONEN
# ============================================================================

function Write-Log {
    param([string]$Message, [string]$Type = "Info")
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    $color = @{
        "Info"    = $ColorInfo
        "Success" = $ColorSuccess
        "Error"   = $ColorError
        "Warning" = $ColorWarning
    }[$Type]
    
    Write-Host "[$timestamp] " -NoNewline -ForegroundColor $ColorGray
    Write-Host $Message -ForegroundColor $color
}

function Test-Docker {
    Write-Log "Überprüfe Docker-Installation..." "Info"
    
    try {
        $version = docker --version 2>&1
        Write-Log "Docker gefunden: $version" "Success"
        return $true
    } catch {
        Write-Log "Docker nicht gefunden oder nicht im PATH" "Error"
        Write-Log "Bitte installiere Docker Desktop von https://www.docker.com/products/docker-desktop" "Warning"
        return $false
    }
}

function Pull-DockerImage {
    Write-Log "Pullen des Docker-Images ($DOCKER_IMAGE)..." "Info"
    
    docker pull "$DOCKER_IMAGE:$DOCKER_TAG" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Log "Docker-Image erfolgreich gepullt" "Success"
        return $true
    } else {
        Write-Log "Fehler beim Pullen des Docker-Images" "Error"
        return $false
    }
}

function Build-APK {
    param([string]$BuildType, [string]$ProjectPath)
    
    Write-Log "Starte APK-Build ($BuildType)..." "Info"
    Write-Log "Projekt-Pfad: $ProjectPath" "Info"
    Write-Log ""
    
    $buildCommand = "buildozer -v android $BuildType"
    
    Write-Log "Docker-Befehl: docker run --rm -v '$ProjectPath`:/home/user/buildozer' -w /home/user/buildozer $DOCKER_IMAGE $buildCommand" "Info"
    Write-Log ""
    Write-Log "Dies kann 5-15 Minuten dauern..." "Warning"
    Write-Log ""
    
    # Build ausführen
    docker run --rm -v "$ProjectPath`:/home/user/buildozer" -w /home/user/buildozer $DOCKER_IMAGE $buildCommand 2>&1 | Tee-Object -Variable buildLog
    
    $buildSuccess = $LASTEXITCODE -eq 0
    return @{
        Success = $buildSuccess
        Log     = $buildLog
    }
}

function Find-APK {
    param([string]$ProjectPath)
    
    $binPath = Join-Path $ProjectPath "bin"
    
    if (-not (Test-Path $binPath)) {
        return $null
    }
    
    $apkFiles = @(Get-ChildItem -Path $binPath -Filter $APK_NAME_PATTERN -ErrorAction SilentlyContinue)
    
    if ($apkFiles.Count -gt 0) {
        return $apkFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    }
    
    return $null
}

function Get-FileSize {
    param([string]$FilePath)
    
    if (Test-Path $FilePath) {
        $size = (Get-Item $FilePath).Length / 1MB
        return "{0:N2}" -f $size
    }
    
    return "N/A"
}

function Show-Results {
    param([object]$BuildResult, [string]$ProjectPath)
    
    Write-Log ""
    Write-Log "════════════════════════════════════════" "Info"
    
    if ($BuildResult.Success) {
        Write-Log "✓ BUILD ERFOLGREICH" "Success"
        
        $apk = Find-APK $ProjectPath
        if ($apk) {
            $size = Get-FileSize $apk.FullName
            Write-Log ""
            Write-Log "APK-Informationen:" "Info"
            Write-Log "  Datei: $($apk.Name)" "Success"
            Write-Log "  Größe: $size MB" "Info"
            Write-Log "  Pfad: $($apk.FullName)" "Info"
            Write-Log "  Erstellt: $($apk.LastWriteTime)" "Info"
            Write-Log ""
            Write-Log "Nächste Schritte:" "Info"
            
            if (Get-Command adb -ErrorAction SilentlyContinue) {
                Write-Log "  1. Gerät verbinden" "Gray"
                Write-Log "  2. Installieren: adb install `"$($apk.FullName)`"" "Gray"
            } else {
                Write-Log "  1. APK auf Android-Gerät übertragen" "Gray"
                Write-Log "  2. APK öffnen und installieren" "Gray"
                Write-Log "  (adb nicht im PATH gefunden)" "Warning"
            }
            
            if ($OpenFinder) {
                Write-Log ""
                Write-Log "Öffne bin-Ordner..." "Info"
                explorer.exe (Split-Path $apk.FullName)
            }
        } else {
            Write-Log "⚠ Warnung: APK-Datei nicht gefunden" "Warning"
        }
    } else {
        Write-Log "✗ BUILD FEHLGESCHLAGEN" "Error"
        Write-Log ""
        Write-Log "Troubleshooting:" "Warning"
        Write-Log "  1. Überprüfe Docker: docker ps" "Gray"
        Write-Log "  2. Überprüfe buildozer.spec" "Gray"
        Write-Log "  3. Überprüfe requirements.txt" "Gray"
        Write-Log "  4. Logs im bin/buildozer_output.log anschauen" "Gray"
    }
    
    Write-Log "════════════════════════════════════════" "Info"
    Write-Log ""
}

# ============================================================================
# HAUPT-SKRIPT
# ============================================================================

function Main {
    Clear-Host
    
    Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor $ColorInfo
    Write-Host "║  Docker APK Builder - $PROJECT_NAME" -ForegroundColor $ColorInfo
    Write-Host "║  Build Type: $BuildType" -ForegroundColor $ColorInfo
    Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor $ColorInfo
    Write-Host ""
    
    # 1. Docker-Check
    if (-not (Test-Docker)) {
        exit 1
    }
    
    # 2. Docker-Image pullen (optional)
    Write-Host ""
    if (-not $SkipDockerPull) {
        if (-not (Pull-DockerImage)) {
            exit 1
        }
    } else {
        Write-Log "Docker-Pull übersprungen" "Info"
    }
    
    # 3. APK bauen
    Write-Host ""
    $projectPath = (Get-Location).Path
    $result = Build-APK -BuildType $BuildType -ProjectPath $projectPath
    
    # 4. Ergebnisse anzeigen
    Show-Results -BuildResult $result -ProjectPath $projectPath
    
    # 5. Optional: Auto-Install
    if ($AutoInstall -and $result.Success) {
        $apk = Find-APK $projectPath
        if ($apk -and (Get-Command adb -ErrorAction SilentlyContinue)) {
            Write-Log "Installiere APK auf Gerät..." "Info"
            adb install "$($apk.FullName)"
        }
    }
    
    exit ($result.Success ? 0 : 1)
}

# Skript ausführen
Main
