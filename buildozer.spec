[app]
title = Zeiterfassung
package.name = zeiterfassung
package.domain = org.tkideneb2

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
source.exclude_dirs = android-sdk,java17,.git,__pycache__,.buildozer,bin,templates
source.exclude_patterns = *.md,*.txt,*.bat,*.ps1,*.sh,*.spec,Dockerfile,*.zip
# Nutze das stabile Kivy-Layout als Einstiegspunkt
source.main = main.py

version = 2.0

# Python requirements for iOS and Android
# IMPORTANT: Exact patch version required (python-for-android needs full version number)
# Python 3.10.13 is the last stable 3.10 release, fully compatible with reportlab on Android
requirements = python3==3.10.13,kivy,kivymd,pillow,plyer,pyjnius,reportlab,cython,androidstorage4kivy

# Android-specific requirements  
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,INTERNET,READ_MEDIA_DOCUMENTS
android.api = 34
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
android.ndk = 25b
android.skip_update = False
# Use preinstalled SDK/NDK inside Docker image
android.sdk_path = /opt/android-sdk
android.ndk_path = /opt/android-ndk

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
p4a.ndk_api = 21

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
