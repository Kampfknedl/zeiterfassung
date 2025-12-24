[app]
title = Zeiterfassung
package.name = zeiterfassung
package.domain = org.tkideneb

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 1.0

requirements = python3,kivy,sqlite3,fpdf2,pyjnius

presplash.filename = %(source.dir)s/data/presplash.png
icon.filename = %(source.dir)s/data/icon.png

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
p4a.bootstrap = sdl2
p4a.hook = buildozer_hooks.py

[buildozer]
log_level = 2
warn_on_root = 1