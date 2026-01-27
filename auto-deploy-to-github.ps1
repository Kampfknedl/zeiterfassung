#!/usr/bin/env powershell
<#
.SYNOPSIS
Vollautomatische GitHub Repository Setup und APK Builder Deployment

.DESCRIPTION
Macht ALLES automatisch:
1. GitHub CLI prüfen/installieren
2. GitHub Login (einmalig)
3. Repository auf GitHub erstellen
4. Git lokal konfigurieren
5. Code hochladen
6. APK Builder Workflow starten

.PARAMETER Username
GitHub Username (z.B. "bene-2026")

.EXAMPLE
.\auto-deploy-to-github.ps1 -Username "bene-2026"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Username
)

$ErrorActionPreference = "Stop"

Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Zeiterfassung - GitHub APK Builder Auto Deploy          ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# 1. GitHub CLI prüfen
Write-Host "[1/6] GitHub CLI prüfen..." -ForegroundColor Yellow
$ghInstalled = $null -ne (Get-Command gh -ErrorAction SilentlyContinue)

if (-not $ghInstalled) {
    Write-Host "❌ GitHub CLI nicht installiert" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installation starten..." -ForegroundColor Cyan
    Write-Host "Bitte im Installer 'Add gh to PATH' auswählen!"
    Write-Host ""
    
    # Mit Scoop oder Chocolatey installieren
    $hasScoop = $null -ne (Get-Command scoop -ErrorAction SilentlyContinue)
    $hasChoco = $null -ne (Get-Command choco -ErrorAction SilentlyContinue)
    
    if ($hasScoop) {
        Write-Host "Installiere mit Scoop..." -ForegroundColor Cyan
        scoop install gh
    } elseif ($hasChoco) {
        Write-Host "Installiere mit Chocolatey..." -ForegroundColor Cyan
        choco install gh -y
    } else {
        Write-Host "Bitte manuell installieren:" -ForegroundColor Red
        Write-Host "  https://github.com/cli/cli/releases"
        Write-Host "  oder: winget install GitHub.cli"
        exit 1
    }
}

Write-Host "✅ GitHub CLI gefunden" -ForegroundColor Green

# 2. GitHub Login prüfen
Write-Host ""
Write-Host "[2/6] GitHub Authentifizierung prüfen..." -ForegroundColor Yellow

$ghAuth = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Nicht authentifiziert - Öffne GitHub Login..." -ForegroundColor Red
    gh auth login --web
} else {
    Write-Host "✅ Bereits authentifiziert" -ForegroundColor Green
}

# 3. Repository prüfen/erstellen
Write-Host ""
Write-Host "[3/6] GitHub Repository erstellen..." -ForegroundColor Yellow

$repoName = "zeiterfassung"
$repoUrl = "https://github.com/$Username/$repoName"

# Prüfe ob Repo existiert
$repoExists = gh repo view "$Username/$repoName" 2>&1 | Select-String "resource not found" -Quiet

if ($repoExists) {
    Write-Host "Creating repository: $repoName" -ForegroundColor Cyan
    gh repo create $repoName --public --description "Android time tracking app - Kivy based" --source=. --remote=origin --push
    Write-Host "✅ Repository erstellt und gepusht!" -ForegroundColor Green
} else {
    Write-Host "✅ Repository existiert bereits: $repoUrl" -ForegroundColor Green
    
    # Prüfe ob remote existiert
    $hasRemote = git remote | Select-String "origin" -Quiet
    if (-not $hasRemote) {
        Write-Host "Remote 'origin' hinzufügen..." -ForegroundColor Cyan
        git remote add origin "https://github.com/$Username/$repoName.git"
    }
}

# 4. Git Konfiguration
Write-Host ""
Write-Host "[4/6] Git konfigurieren..." -ForegroundColor Yellow

$gitUser = git config --global user.name
$gitEmail = git config --global user.email

if (-not $gitUser) {
    git config --global user.name "$Username"
    Write-Host "✅ Git user name gesetzt: $Username" -ForegroundColor Green
} else {
    Write-Host "✅ Git user name: $gitUser" -ForegroundColor Green
}

if (-not $gitEmail) {
    $email = "$Username@users.noreply.github.com"
    git config --global user.email "$email"
    Write-Host "✅ Git email gesetzt: $email" -ForegroundColor Green
} else {
    Write-Host "✅ Git email: $gitEmail" -ForegroundColor Green
}

# 5. Code hochladen
Write-Host ""
Write-Host "[5/6] Code zu GitHub hochladen..." -ForegroundColor Yellow

# Check wenn bereits ein Commit existiert
$hasCommits = git log --oneline 2>&1 | Measure-Object -Line

if ($hasCommits.Lines -eq 0) {
    Write-Host "Neuer Repository - erstelle Initial Commit..." -ForegroundColor Cyan
    
    # Stage alle wichtigen Dateien
    git add main.py db.py zeiterfassung.kv requirements.txt buildozer.spec .gitignore 2>/dev/null
    git add .github/workflows/ 2>/dev/null
    git add icon.png 2>/dev/null
    git add res/ 2>/dev/null
    
    $msg = "Initial commit - Zeiterfassung APK Builder"
    git commit -m $msg
    git branch -M main
}

# Push
Write-Host "Pushing zu GitHub..." -ForegroundColor Cyan
git push -u origin main --force-with-lease 2>&1 | Where-Object { $_ -notmatch "^$" } | ForEach-Object { Write-Host "  $_" }

Write-Host "✅ Code hochgeladen!" -ForegroundColor Green

# 6. Status und Workflow Info
Write-Host ""
Write-Host "[6/6] Workflow Status..." -ForegroundColor Yellow

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ DEPLOYMENT ERFOLGREICH!                              ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📊 Repository: $repoUrl" -ForegroundColor Cyan
Write-Host "🔨 Workflow: $repoUrl/actions" -ForegroundColor Cyan
Write-Host ""

Write-Host "Die APK wird jetzt gebaut! Fortschritt:" -ForegroundColor Yellow
Write-Host "  1. Gehe zu $repoUrl/actions" -ForegroundColor White
Write-Host "  2. Du siehst 'Build APK - Android 16'" -ForegroundColor White
Write-Host "  3. Warte ~15 Minuten" -ForegroundColor White
Write-Host "  4. Download: Artifacts → zeiterfassung-apk" -ForegroundColor White
Write-Host ""

Write-Host "Öffne Workflow im Browser? (j/n)" -ForegroundColor Yellow
$response = Read-Host

if ($response -eq "j" -or $response -eq "J") {
    $workflowUrl = "$repoUrl/actions"
    Start-Process $workflowUrl
}

Write-Host ""
Write-Host "Done! 🚀" -ForegroundColor Green
