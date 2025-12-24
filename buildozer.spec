[app]
title = Stundenerfassung
package.name = zeiterfassung
package.domain = org.bene
source.dir = .
source.include_exts = py,db
version = 0.1.0
requirements = python3,kivy,sqlite3,fpdf2,pyjnius
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
api = 31
minapi = 21
ndk = 25b
accept_sdk_license = True
archs = arm64-v8a,armeabi-v7a
