[app]
# App metadata
title = Stundenerfassung
package.name = zeiterfassung
package.domain = org.bene

# Source settings
source.dir = .
source.include_exts = py,kv,png,jpg,db
version = 0.1.0

# Runtime requirements
requirements = python3,kivy,sqlite3,fpdf2
orientation = portrait
fullscreen = 0

# Android settings
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a,armeabi-v7a

# (optional) reduce size by excluding tests
android.add_src = .

[buildozer]
log_level = 2
warn_on_root = 1

