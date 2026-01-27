#!/usr/bin/env pwsh
<#
.SYNOPSIS
Docker-basierter APK Builder fuer Zeiterfassung
.DESCRIPTION
Erstellt eine Android APK mit Docker (keine lokale SDK-Installation erforderlich)
#>

param(
    [ValidateSet("debug", "release")]
    [string]$BuildType = "debug",
    [switch]$SkipDockerPull = $true,
    [switch]$KeepContainerLogs,
    [switch]$AutoInstall,
    [switch]$OpenFinder
)

$DOCKER_IMAGE = "zeiterfassung-buildozer"
$DOCKER_TAG = "latest"
$PROJECT_NAME = "Zeiterfassung"
$APK_NAME_PATTERN = "zeiterfassung-*.apk"

$ColorSuccess = "Green"
$ColorError = "Red"
$ColorWarning = "Yellow"
$ColorInfo = "Cyan"
$ColorGray = "DarkGray"

function Write-Log {
    param([string]$Message, [string]$Type = "Info")
    $timestamp = Get-Date -Format "HH:mm:ss"
    $color = @{
        "Info"    = $ColorInfo
        "Success" = $ColorSuccess
        "Error"   = $ColorError
        "Warning" = $ColorWarning
        "Gray"    = $ColorGray
    }[$Type]
    if (-not $color) { $color = $ColorInfo }
    Write-Host "[$timestamp] " -NoNewline -ForegroundColor $ColorGray
    Write-Host $Message -ForegroundColor $color
}

function Test-Docker {
    Write-Log "Pruefe Docker-Installation..." "Info"
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
    Write-Log "Skip Docker pull (lokales Image erwartet)." "Info"
    return $true
}

function Build-APK {
    param([string]$BuildType, [string]$ProjectPath)
    Write-Log "Starte APK-Build ($BuildType)..." "Info"
    Write-Log "Projekt-Pfad: $ProjectPath" "Info"
    Write-Log "" "Info"
    $buildArgs = @("buildozer", "-v", "android", $BuildType)
    $buildCommandText = ($buildArgs -join " ")
    Write-Log "Docker-Befehl: docker run --rm -v \"${ProjectPath}:/app\" -w /app $DOCKER_IMAGE $buildCommandText" "Info"
    Write-Log "" "Info"
    Write-Log "Dies kann 5-15 Minuten dauern..." "Warning"
    Write-Log "" "Info"
    $binPath = Join-Path $ProjectPath "bin"
    if (-not (Test-Path $binPath)) { New-Item -ItemType Directory -Path $binPath | Out-Null }
    $logFile = Join-Path $binPath "build_log_docker.txt"
    docker run --rm -v "${ProjectPath}:/app" -w /app $DOCKER_IMAGE @buildArgs 2>&1 |
        Tee-Object -Variable buildLog |
        Tee-Object -FilePath $logFile
    $buildSuccess = $LASTEXITCODE -eq 0
    return @{
        Success = $buildSuccess
        Log     = $buildLog
    }
}

function Find-APK {
    param([string]$ProjectPath)
    $binPath = Join-Path $ProjectPath "bin"
    if (-not (Test-Path $binPath)) { return $null }
    $apkFiles = @(Get-ChildItem -Path $binPath -Filter $APK_NAME_PATTERN -ErrorAction SilentlyContinue)
    if ($apkFiles.Count -gt 0) { return $apkFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1 }
    return $null
}

function Get-FileSize {
    param([string]$FilePath)
    if (Test-Path $FilePath) { return "{0:N2}" -f ((Get-Item $FilePath).Length / 1MB) }
    return "N/A"
}

function Show-Results {
    param([object]$BuildResult, [string]$ProjectPath)
    Write-Log "" "Info"
    Write-Log "========================================" "Info"
    if ($BuildResult.Success) {
        Write-Log "Build erfolgreich." "Success"
        $apk = Find-APK $ProjectPath
        if ($apk) {
            $size = Get-FileSize $apk.FullName
            Write-Log "APK-Datei: $($apk.Name)" "Info"
            Write-Log "Groesse: $size MB" "Info"
            Write-Log "Pfad: $($apk.FullName)" "Info"
            Write-Log "Zeit: $($apk.LastWriteTime)" "Info"
            if (Get-Command adb -ErrorAction SilentlyContinue) {
                Write-Log "adb install \"$($apk.FullName)\"" "Gray"
            } else {
                Write-Log "adb nicht gefunden; APK manuell kopieren" "Warning"
            }
            if ($OpenFinder) {
                explorer.exe (Split-Path $apk.FullName)
            }
        } else {
            Write-Log "APK-Datei nicht gefunden." "Warning"
        }
    } else {
        Write-Log "Build fehlgeschlagen." "Error"
        Write-Log "Pruefe bin/buildozer_output.log oder buildozer.log" "Warning"
    }
    Write-Log "========================================" "Info"
    Write-Log "" "Info"
}

function Main {
    Clear-Host
    Write-Host "=== Docker APK Builder: $PROJECT_NAME ===" -ForegroundColor $ColorInfo
    Write-Host "Build Type: $BuildType" -ForegroundColor $ColorInfo
    Write-Host ""
    if (-not (Test-Docker)) { exit 1 }
    Write-Host ""
    if (-not $SkipDockerPull) {
        if (-not (Pull-DockerImage)) { exit 1 }
    } else { Write-Log "Docker-Pull uebersprungen" "Info" }
    Write-Host ""
    $projectPath = (Get-Location).Path
    $result = Build-APK -BuildType $BuildType -ProjectPath $projectPath
    Show-Results -BuildResult $result -ProjectPath $projectPath
    if ($AutoInstall -and $result.Success) {
        $apk = Find-APK $projectPath
        if ($apk -and (Get-Command adb -ErrorAction SilentlyContinue)) {
            Write-Log "Installiere APK auf Geraet..." "Info"
            adb install "$($apk.FullName)"
        }
    }
    if ($result.Success) { exit 0 } else { exit 1 }
}

Main
