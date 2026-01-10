#!/usr/bin/env powershell
# Test-Skript für Zeiterfassung App

$env:PYTHONIOENCODING = 'utf-8'

Write-Host "Starte Zeiterfassung App für lokalen Test..." -ForegroundColor Green
Write-Host ""
Write-Host "Die App sollte gleich in einem Fenster starten."
Write-Host "Test folgende Funktionen:"
Write-Host "  1. App startet fehlerfrei"
Write-Host "  2. Kunde 'Oberhuber' ist vorausgewählt"
Write-Host "  3. Tätigkeit-Feld kann fokussiert werden"
Write-Host "  4. Tätigkeit eingeben + Speichern funktioniert"
Write-Host "  5. PDF Export funktioniert"
Write-Host ""
Write-Host "Console Output unten zeigt [ADD_ENTRY] und [EXPORT] Logs..."
Write-Host "============================================================"
Write-Host ""

cd "C:\Users\Bene\Desktop\Python_Programme"
& .venv\Scripts\python.exe main.py
