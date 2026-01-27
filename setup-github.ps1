#!/usr/bin/env powershell
<#
.SYNOPSIS
Initialisiert Git Repository und pushed zu GitHub

.DESCRIPTION
1. Git konfigurieren
2. .gitignore aktualisieren
3. Alle wichtigen Dateien adden
4. Initial commit
5. Zu GitHub pushen

.PARAMETER GitHubUsername
Dein neuer GitHub Username (z.B. "bene-2026")

.EXAMPLE
.\setup-github.ps1 -GitHubUsername "bene-2026"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$GitHubUsername
)

$projectDir = Get-Location
$repoName = "zeiterfassung"

Write-Host "=== GitHub Repository Setup ===" -ForegroundColor Cyan
Write-Host "Project: $projectDir"
Write-Host "Username: $GitHubUsername"
Write-Host "Repository: $repoName"
Write-Host ""

# Git konfigurieren
Write-Host "[1/5] Git Konfiguration..." -ForegroundColor Yellow
git config --global user.email "$GitHubUsername@users.noreply.github.com"
git config --global user.name "$GitHubUsername"

# Git initialisieren
Write-Host "[2/5] Repository initialisieren..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    git branch -M main
} else {
    Write-Host "Git repo existiert bereits."
}

# .gitignore checken
Write-Host "[3/5] .gitignore validieren..." -ForegroundColor Yellow
if (Test-Path ".gitignore") {
    Write-Host ".gitignore existiert ✓"
} else {
    Write-Host "WARNUNG: .gitignore nicht gefunden!" -ForegroundColor Red
}

# Dateien hinzufügen
Write-Host "[4/5] Dateien hinzufügen (nur essenzielle)..." -ForegroundColor Yellow
git add main.py
git add db.py
git add zeiterfassung.kv
git add requirements.txt
git add buildozer.spec
git add .gitignore
git add .github/workflows/
git add icon.png -Force -ErrorAction SilentlyContinue
git add res/xml/ -Force -ErrorAction SilentlyContinue

# Status anzeigen
Write-Host ""
Write-Host "Status:" -ForegroundColor Cyan
git status --short | Select-Object -First 20
Write-Host ""

# Initial commit
Write-Host "[5/5] Initial Commit..." -ForegroundColor Yellow
$msg = "Initial commit - Zeiterfassung App für GitHub Actions APK Builder"
git commit -m $msg

Write-Host ""
Write-Host "=== Remote hinzufügen ===" -ForegroundColor Cyan
Write-Host "Repository URL: https://github.com/$GitHubUsername/$repoName.git"
Write-Host ""
Write-Host "Stellen Sie sicher, dass das Repository auf GitHub erstellt wurde:"
Write-Host "👉 https://github.com/new"
Write-Host ""
Write-Host "Dann ausführen:"
Write-Host ""
Write-Host "    git remote add origin https://github.com/$GitHubUsername/$repoName.git"
Write-Host "    git push -u origin main"
Write-Host ""
