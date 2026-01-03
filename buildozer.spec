[app]
title = Zeiterfassung
package.name = zeiterfassung
package.domain = org.tkideneb

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 1.0

requirements = python3,kivy,pillow,pyjnius

icon.filename = ./icon.png

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 25b
android.skip_update = False
orientation = portrait

# Android FileProvider configuration for sharing PDFs
android.add_resources = res
android.gradle_dependencies = androidx.core:core:1.9.0

p4a.bootstrap = sdl2
p4a.arch = arm64-v8a
p4a.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 0