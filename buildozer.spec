[app]
title = Zeiterfassung
package.name = zeiterfassung
package.domain = org.tkideneb2

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
source.exclude_dirs = android-sdk,java17,.git,__pycache__,.buildozer,bin,templates,.venv,venv
source.exclude_patterns = *.md,*.bat,*.ps1,*.sh,buildozer_*.spec,*.json,*.log,Dockerfile,*.zip,*.pyc,main_old_backup.py
# Nutze das stabile Kivy-Layout als Einstiegspunkt
source.main = main.py

version = 2.0

# Python requirements - CLEAN minimal setup (openpyxl nur für Desktop)
requirements = python3==3.10.13,kivy==2.3.0,pillow,pyjnius

# Android-specific requirements  
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,READ_MEDIA_DOCUMENTS
android.api = 21
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 25b
android.skip_update = False
android.skip_compile_pyc = True
# Use preinstalled SDK/NDK inside Docker image
android.sdk_path = /opt/android-sdk
android.ndk_path = /opt/android-ndk
# REMOVED GLES2 enforcement - let Android choose renderer to avoid hwui mutex crashes
# android.add_env_vars = SDL_VIDEO_VULKAN=0,SDL_VIDEODRIVER=gles2,SDL_ANDROID_BLOCK_ON_PAUSE=1
# android.opengl_es_version = 0x00020000

# Android FileProvider configuration for sharing PDFs/CSVs
android.add_resources = res
android.gradle_dependencies = androidx.core:core:1.9.0,androidx.documentfile:documentfile:1.0.1

# iOS-specific settings
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0

# iOS codesign
# ios.codesign.allowed = false
# Uncomment and configure for production:
# ios.codesign.debug = "iPhone Developer: YourName (XXXXXXXXXX)"
# ios.codesign.release = "iPhone Distribution: YourCompany"

# Orientation
orientation = portrait
fullscreen = 0

# Icon and presplash
icon.filename = ./icon.png
# presplash.filename = ./presplash.png

# P4A (Python-for-Android) settings
p4a.bootstrap = sdl2
p4a.arch = arm64-v8a
p4a.ndk_api = 23

# iOS specific arch (for M1/M2 Macs, use arm64; for Intel Macs, use x86_64)
# You need to build on macOS for iOS
# ios.arch = arm64

[buildozer]
log_level = 2
warn_on_root = 0

# Build directory
build_dir = ./.buildozer

# Target platform (android or ios)
# For iOS, you need to run on macOS:
# buildozer ios debug
# buildozer ios release
