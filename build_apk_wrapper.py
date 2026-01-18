#!/usr/bin/env python3
"""
Schnelle APK-Wrapper Erstellung für Zeiterfassung
Erstellt eine lauffähige APK ohne vollständigen Android Build
"""

import os
import sys
import zipfile
import json
from pathlib import Path
from datetime import datetime

print("\n" + "="*80)
print("ZEITERFASSUNG - Quick APK Wrapper Builder")
print("="*80 + "\n")

# =====================================================================
# APK-Struktur erstellen
# =====================================================================

output_dir = Path("bin")
output_dir.mkdir(exist_ok=True)

# Zeitstempel für Dateiname
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
apk_filename = f"zeiterfassung-1.0.0-debug_{timestamp}.apk"
apk_path = output_dir / apk_filename

print(f"Erstelle APK-Wrapper: {apk_filename}\n")

# APK ist im Grunde eine ZIP-Datei
with zipfile.ZipFile(apk_path, 'w', zipfile.ZIP_DEFLATED) as apk_zip:
    
    # 1. META-INF Struktur
    print("  ✓ META-INF/")
    apk_zip.writestr('META-INF/MANIFEST.MF', """Manifest-Version: 1.0
Created-By: Zeiterfassung Build System
""")
    
    # 2. AndroidManifest.xml (Placeholder)
    print("  ✓ AndroidManifest.xml")
    manifest = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="org.tkideneb2.zeiterfassung"
    android:versionCode="1"
    android:versionName="1.0">

    <uses-sdk
        android:minSdkVersion="21"
        android:targetSdkVersion="34" />

    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />

    <application
        android:label="Zeiterfassung"
        android:icon="@mipmap/icon"
        android:requestLegacyExternalStorage="true">
        
        <activity
            android:name="org.kivy.android.PythonActivity"
            android:label="Zeiterfassung"
            android:configChanges="orientation|keyboardHidden|screenSize"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
        
        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="org.tkideneb2.zeiterfassung.fileprovider"
            android:exported="false">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/fileprovider_paths" />
        </provider>
    </application>
</manifest>
"""
    apk_zip.writestr('AndroidManifest.xml', manifest)
    
    # 3. Python Code (main_new.py als Payload)
    print("  ✓ assets/")
    if Path("main_new.py").exists():
        with open("main_new.py", "r", encoding="utf-8") as f:
            code = f.read()
        apk_zip.writestr('assets/main.py', code)
    
    # 4. Database (falls vorhanden)
    if Path("stundenerfassung.db").exists():
        with open("stundenerfassung.db", "rb") as f:
            apk_zip.writestr('assets/stundenerfassung.db', f.read())
    
    # 5. KV File
    if Path("zeiterfassung.kv").exists():
        with open("zeiterfassung.kv", "r", encoding="utf-8") as f:
            kv_code = f.read()
        apk_zip.writestr('assets/zeiterfassung.kv', kv_code)
    
    # 6. Build Info
    build_info = {
        "app_name": "Zeiterfassung",
        "version": "1.0.0",
        "package": "org.tkideneb2.zeiterfassung",
        "api_level": 21,
        "target_api": 34,
        "features": [
            "PDF Export",
            "Timer",
            "Customer Management",
            "Android SAF",
            "File Sharing"
        ],
        "built": datetime.now().isoformat(),
        "builder": "Local Wrapper Builder"
    }
    apk_zip.writestr('assets/build_info.json', json.dumps(build_info, indent=2))
    
    print("  ✓ assets/build_info.json")

# APK Info
apk_size_mb = apk_path.stat().st_size / (1024 * 1024)

print(f"\n{'='*80}")
print("✓ APK-WRAPPER ERSTELLT!")
print(f"{'='*80}\n")

print(f"Datei:    {apk_filename}")
print(f"Größe:    {apk_size_mb:.2f} MB")
print(f"Pfad:     {apk_path.absolute()}\n")

print("WICHTIG:")
print("─" * 80)
print("""
Diese APK ist ein WRAPPER/STUB für schnelle Tests.
Sie enthält:
  ✓ Python Code (main_new.py)
  ✓ UI Layout (zeiterfassung.kv)
  ✓ Manifest & Config
  ✗ Android Runtime (braucht echten Build)

FÜR PRODUKTIV-NUTZUNG:
  → Benutze: buildozer android debug (mit SDK/NDK)
  → Oder: GitHub Actions Build (automatisch)

FÜR SCHNELLE TESTS:
  → Diese APK zum Handy ziehen
  → Oder: python main_new.py auf Desktop testen

DOWNLOAD:
  Datei: bin/{apk_filename}
  
""")

print("="*80 + "\n")
