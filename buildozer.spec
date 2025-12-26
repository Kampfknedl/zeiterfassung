[app]
title = Zeiterfassung
package.name = zeiterfassung
package.domain = org.tkideneb

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 1.0

requirements = python3,kivy

icon.filename = ./icon.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
