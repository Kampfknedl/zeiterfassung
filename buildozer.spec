[app]
title = Zeiterfassung
package.name = zeiterfassung
package.domain = org.tkideneb2

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_dirs = android-sdk,java17,.git,__pycache__,.buildozer,bin,templates,.venv,venv,.github
source.exclude_patterns = *.md,*.bat,*.ps1,*.sh,buildozer_*.spec,*.json,*.log,Dockerfile,*.zip,*.pyc,*_old.py,main_old*.py,crash_*.txt,test_*.py,debug_*.py
# Nutze das stabile Kivy-Layout als Einstiegspunkt
source.main = main.py

version = 2.0

# Python requirements - CLEAN minimal setup (openpyxl nur für Desktop)
requirements = python3==3.10.13,kivy==2.3.0,pyjnius

# Android 16 (API 35) - Galaxy S24+
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET
android.api = 35
android.minapi = 21
android.target_api = 35
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 25b
android.skip_update = False
android.skip_compile_pyc = True

# Android FileProvider configuration for sharing PDFs
android.add_resources = res
android.gradle_dependencies = androidx.core:core:1.12.0,androidx.appcompat:appcompat:1.6.1
android.gradle_options = org.gradle.jvmargs=-Xmx2048m,org.gradle.dependency.strict=false

orientation = portrait
fullscreen = 0
icon.filename = ./icon.png

p4a.bootstrap = sdl2
p4a.arch = arm64-v8a
p4a.ndk_api = 23

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = ./.buildozer
