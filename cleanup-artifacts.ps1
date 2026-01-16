# GitHub Artifacts & Caches Cleanup Script
# Löscht alle Artefakte und Caches älter als 1 Tag

$repo = "Tkideneb2/Zeiterfassung"
$cutoffDate = (Get-Date).AddDays(-1)

Write-Host "=== GitHub Artifacts & Caches Cleanup ===" -ForegroundColor Cyan
Write-Host "Repository: $repo"
Write-Host "Cutoff Date: $cutoffDate"
Write-Host ""

# Check if authenticated
Write-Host "Prüfe GitHub-Authentifizierung..." -ForegroundColor Yellow
gh auth status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Nicht authentifiziert. Starte Browser-Login..." -ForegroundColor Yellow
    gh auth login -w
}

# Delete Artifacts
Write-Host ""
Write-Host "=== Lösche alte Artefakte ===" -ForegroundColor Cyan
$artifacts = gh api repos/$repo/actions/artifacts --paginate -q '.artifacts[] | select(.expired==false) | {id: .id, name: .name, created: .created_at, size: .size_in_bytes}' | ConvertFrom-Json -AsHashtable

if ($artifacts.Count -eq 0) {
    Write-Host "Keine Artefakte gefunden."
} else {
    $deleted = 0
    $artifacts | ForEach-Object {
        $created = [DateTime]::Parse($_.created)
        if ($created -lt $cutoffDate) {
            Write-Host "Lösche: $($_.name) (ID: $($_.id), Size: $($_.size / 1MB) MB)" -ForegroundColor Red
            gh api --method DELETE repos/$repo/actions/artifacts/$($_.id)
            $deleted++
        }
    }
    Write-Host "Total gelöscht: $deleted Artefakte" -ForegroundColor Green
}

# Delete Caches
Write-Host ""
Write-Host "=== Lösche alte Caches ===" -ForegroundColor Cyan
$caches = gh api repos/$repo/actions/caches --paginate -q '.actions_caches[] | {id: .id, key: .key, last_accessed: .last_accessed_at, size: .size_in_bytes}' | ConvertFrom-Json -AsHashtable

if ($caches.Count -eq 0) {
    Write-Host "Keine Caches gefunden."
} else {
    $deleted = 0
    $caches | ForEach-Object {
        $lastAccessed = [DateTime]::Parse($_.last_accessed)
        if ($lastAccessed -lt $cutoffDate) {
            Write-Host "Lösche Cache: $($_.key) (ID: $($_.id), Size: $($_.size / 1MB) MB)" -ForegroundColor Red
            gh api --method DELETE repos/$repo/actions/caches/$($_.id)
            $deleted++
        }
    }
    Write-Host "Total gelöscht: $deleted Caches" -ForegroundColor Green
}

Write-Host ""
Write-Host "Cleanup abgeschlossen!" -ForegroundColor Green
Write-Host "Warte 6-12 Stunden bis GitHub die Quota neu berechnet hat."
