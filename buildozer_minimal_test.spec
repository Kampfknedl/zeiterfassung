[app]
title = Zeiterfassung Minimal Test
package.name = zeiterfassung_minimal_test
package.domain = org.tkideneb2.test

source.dir = .
source.include_exts = py
source.exclude_dirs = android-sdk,java17,.git,__pycache__,.buildozer,bin,templates
source.exclude_patterns = *.md,*.txt,*.bat,*.ps1,*.sh,*.kv,Dockerfile,*.zip,*.db
source.main = main_minimal_test.py

version = 1.0

# MINIMAL: Only Kivy, no extra dependencies
requirements = python3==3.10.13,kivy

# Android config
android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.ndk = 25b
android.skip_update = False
android.sdk_path = /opt/android-sdk
android.ndk_path = /opt/android-ndk

# Orientation
orientation = portrait
fullscreen = 0
