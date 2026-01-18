#!/usr/bin/env pwsh
<#
Local Android build helper (no Docker).
Prerequisites:
  - Windows + PowerShell 5.1 or 7
  - At least 10 GB free disk
  - Internet access for Android SDK
  - JDK 17 installed and JAVA_HOME set

Usage:
  powershell -ExecutionPolicy Bypass -File .\build_local_android.ps1

The script installs SDK/NDK (API 34, NDK 26), accepts licenses, exports env vars, then runs "buildozer -v android debug".
#>

param(
    [string]$SdkRoot = "$PSScriptRoot/android-sdk",
    [string]$ApiLevel = "34",
    [string]$NdkVersion = "26.1.10909125",
    [string]$BuildTools = "34.0.0"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Section([string]$text) { Write-Host "`n=== $text ===" -ForegroundColor Cyan }
function Write-Info([string]$text)     { Write-Host "-- $text" -ForegroundColor Yellow }
function Write-Ok([string]$text)       { Write-Host "OK: $text" -ForegroundColor Green }
function Fail([string]$text, [int]$code = 1) { Write-Host "ERROR: $text" -ForegroundColor Red; exit $code }

Write-Section "Local Android Build (Buildozer)"
Write-Info "SDK Root: $SdkRoot"
Write-Info "API Level: $ApiLevel"
Write-Info "NDK Version: $NdkVersion"
Write-Info "Build-Tools: $BuildTools"

if (-not $env:JAVA_HOME) {
    Fail "JAVA_HOME is not set. Install JDK 17 and set JAVA_HOME."
}

$javaExe = Join-Path $env:JAVA_HOME "bin/java.exe"
if (-not (Test-Path $javaExe)) {
    Fail "java.exe not found under JAVA_HOME ($env:JAVA_HOME)"
}

$prevEap = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
$javaVersion = & $javaExe -version 2>&1
$javaExit = $LASTEXITCODE
$ErrorActionPreference = $prevEap
if ($javaExit -ne 0) {
    Fail ("Java check failed (exit {0}): {1}" -f $javaExit, ($javaVersion -join ' | '))
}
Write-Info ("Java detected: {0}" -f ($javaVersion -join ' | '))

if (-not (Get-Command buildozer -ErrorAction SilentlyContinue)) {
    Fail "buildozer not found. Activate your venv and install buildozer first."
}

$toolsDir = Join-Path $SdkRoot "cmdline-tools"
$tmpDir   = Join-Path $env:TEMP "android-sdk-tmp"
New-Item -ItemType Directory -Force -Path $SdkRoot | Out-Null
New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null

$cmdZip = Join-Path $tmpDir "commandlinetools.zip"
$cmdUrl = "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip"
if (-not (Test-Path $cmdZip)) {
    Write-Info "Downloading Android commandline-tools"
    Invoke-WebRequest -Uri $cmdUrl -OutFile $cmdZip -UseBasicParsing
} else {
    Write-Ok "commandline-tools zip already present"
}

$latestDir = Join-Path $toolsDir "latest"
if (-not (Test-Path (Join-Path $latestDir "bin"))) {
    Write-Info "Unpacking commandline-tools"
    Expand-Archive -Path $cmdZip -DestinationPath $tmpDir -Force
    New-Item -ItemType Directory -Force -Path $latestDir | Out-Null
    $sourceTools = Join-Path $tmpDir "cmdline-tools"
    Copy-Item -Recurse -Force -Path (Join-Path $sourceTools "*") -Destination $latestDir
} else {
    Write-Ok "commandline-tools already unpacked"
}

$env:ANDROID_HOME = $SdkRoot
$env:ANDROID_SDK_ROOT = $SdkRoot
$env:ANDROIDSDK = $SdkRoot
$env:PATH = "$(Join-Path $latestDir 'bin');$env:PATH"

$sdkmanager = Join-Path (Join-Path $latestDir "bin") "sdkmanager.bat"
if (-not (Test-Path $sdkmanager)) {
    Fail "sdkmanager not found at $sdkmanager"
}

$packages = @(
    "platform-tools",
    "platforms;android-$ApiLevel",
    "build-tools;$BuildTools",
    "ndk;$NdkVersion"
)

$yes = "y`n" * 1200

Write-Section "Install SDK/NDK packages"
$installOutput = $yes | & $sdkmanager --sdk_root=$SdkRoot @packages 2>&1
Write-Host $installOutput
if ($LASTEXITCODE -ne 0) {
    Fail "sdkmanager package install failed with exit code $LASTEXITCODE"
}
Write-Ok "Packages installed"

Write-Section "Accept SDK licenses"
$licenseOutput = $yes | & $sdkmanager --sdk_root=$SdkRoot --licenses 2>&1
Write-Host $licenseOutput
if ($LASTEXITCODE -ne 0) {
    Fail "sdkmanager license acceptance failed with exit code $LASTEXITCODE"
}
Write-Ok "Licenses accepted"

$env:ANDROIDNDK = Join-Path $SdkRoot "ndk" $NdkVersion
$env:ANDROIDAPI = $ApiLevel
$env:NDKAPI = "21"

Write-Info "ANDROIDSDK = $env:ANDROIDSDK"
Write-Info "ANDROIDNDK = $env:ANDROIDNDK"
Write-Info "ANDROIDAPI = $env:ANDROIDAPI"
Write-Info "NDKAPI     = $env:NDKAPI"

Write-Section "Run buildozer -v android debug"
Push-Location $PSScriptRoot
$buildExit = -1
try {
    & buildozer -v android debug
    $buildExit = $LASTEXITCODE
} finally {
    Pop-Location
}

if ($buildExit -eq 0) {
    Write-Ok "Build finished"
    $binDir = Join-Path $PSScriptRoot "bin"
    if (Test-Path $binDir) {
        Get-ChildItem $binDir -Filter "*.apk" | ForEach-Object {
            Write-Host ("APK: {0} ({1} MB)" -f $_.Name, [Math]::Round($_.Length / 1MB, 2)) -ForegroundColor Green
            Write-Host ("Path: {0}" -f $_.FullName) -ForegroundColor Cyan
        }
    }
    exit 0
}

Write-Host "Build failed with exit code $buildExit" -ForegroundColor Red
$logDir = Join-Path $PSScriptRoot ".buildozer/logs"
if (Test-Path $logDir) {
    $latestLog = Get-ChildItem $logDir -Filter "*.txt" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestLog) {
        Write-Host "Last log file: $($latestLog.Name)" -ForegroundColor Yellow
        Get-Content $latestLog.FullName -Tail 80
    }
}
exit $buildExit
