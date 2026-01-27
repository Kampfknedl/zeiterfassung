# Android Crash Debugging Guide

## 🔴 Was Wir Behoben Haben

### Kritische Fehler Behoben:
1. **Crash Logger beim Import**: ✅ Moved from module-level to `App.on_start()`
2. **Fehlende Android 13+ Permissions**: ✅ Added `READ_MEDIA_DOCUMENTS`
3. **Kivy/reportlab Imports**: ✅ All at module level or in functions, never at import time

### Neue APK Features:
- **Detailliertes Logging**: `[APP]`, `[KV_POST]`, `[PDF]` Tags zeigen Ausführungsfluss
- **Crash Logger deferral**: Läuft jetzt NACH App init, nicht beim Module import
- **Android 13+ Support**: Alle nötigen Permissions in buildozer.spec

---

## 📱 So Testest Du Die Neue APK

### Schritt 1: APK Installieren
```powershell
# Alte Version deinstallieren
adb uninstall org.tkideneb2.zeiterfassung

# Neue APK installieren
adb install -r bin/zeiterfassung-2.0-arm64-v8a_armeabi-v7a-debug.apk
```

### Schritt 2: App Starten & Logcat Lesen
```powershell
# Terminal 1: Logcat (live Ausgabe)
adb logcat | findstr "python\|org.tkideneb2\|APP\|KV_POST"

# Terminal 2: App starten
adb shell am start -n org.tkideneb2.zeiterfassung/.PoCApp
```

⚠️ **WICHTIG**: Beide Terminals offen halten, dann siehst du ALLE Logs

---

## 🔍 Was Du In Logcat Suchen Sollst

### ✅ GUTES Startup (App startet erfolgreich):
```
[APP] KV loaded successfully
[APP] RootWidget created successfully
[APP] on_start() called
[APP] Crash logger installed
[APP] DB initialized at: /data/data/org.tkideneb2.zeiterfassung/...
[KV_POST] on_kv_post() called
[KV_POST] Customers loaded
[KV_POST] RootWidget children count: 5
```

### ❌ CRASH Patterns (zeige Fehler):

**Pattern A: ImportError beim App-Start**
```
ModuleNotFoundError: No module named 'tkinter'
ImportError: No module named 'subprocess'
```
→ Modul existiert auf Android nicht

**Pattern B: FileNotFoundError beim DB Init**
```
FileNotFoundError: [Errno 2] No such file or directory: '/sdcard/...'
PermissionError: [Errno 13] Permission denied
```
→ Permissions Problem

**Pattern C: JNI/pyjnius Error**
```
jnius.jnius.JavaException: ...
AttributeError: 'NoneType' object has no attribute 'getAbsolutePath'
```
→ Android-spezifisches Java-Interface Problem

---

## 🛠️ Schritt-für-Schritt Debugging

### A) APK Startet gar nicht (sofort crash)
```powershell
# Crash-Log abholen
adb shell cat /data/data/org.tkideneb2.zeiterfassung/crash.txt

# Oder:
adb shell find /sdcard/Documents -name "crash.txt" -exec cat {} \;
```

### B) APK Startet, aber UI ist leer
- Logcat schauen - suche nach `KV_POST`-Fehler
- Likely: `on_kv_post()` crasht bei Kundeninitialisierung

### C) APK Startet, Timer/PDF funktioniert nicht
- Features sind nach UI startup erreichbar
- Fehler in Funktionen, nicht beim Startup

---

## 📋 Minimal Test APK (optional)

Wenn selbst die neue Version crasht, können wir ein **absolutes Minimum** testen:

```powershell
# Nur Kivy + Label, KEIN Code outside Funktionen
buildozer -f -v android debug -f buildozer_minimal_test.spec

# Das sollte DEFINITIV auf Android funktionieren:
# - Wenn ja → unser App-Code ist das Problem
# - Wenn nein → Android / ABI / Build-System kaputt
```

---

## 📲 Wenn Logcat Zu Viel Zeigt

Nur Python-Logs filtern:
```powershell
adb logcat | findstr "python"
adb logcat python:V *:S

# Oder mit Tag-Filter:
adb logcat "APP:V" "KV_POST:V" "*:S"
```

---

## 🎯 Nächste Schritte

### Szenario 1: APK Startet Jetzt! ✅
1. Teste Timer Funktion
2. Teste PDF Export
3. Teste Customer Management

### Szenario 2: Immer noch Crash ❌
1. **Gib mir deine Logcat-Ausgabe** (komplett, vom Start bis Crash)
2. **Gib mir die Inhalte von `/data/data/org.tkideneb2.zeiterfassung/crash.txt`**
3. Ich debugge dann den EXAKTEN Fehler

### Szenario 3: Minimal Test APK crasht auch
→ Problem ist Android-Infrastruktur (ABI, SDK, etc), nicht unser Code

---

## 📞 Kontakt für Debug

Wenn immer noch Fehler:

Bitte gib mir:
1. **Logcat Output** (von App-Start bis Crash)
2. **Crash-Datei** (falls vorhanden)
3. **Dein Android Device** (Modell, API-Level)
4. **Screenshot** oder genaue Beschreibung was passiert
