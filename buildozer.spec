[app]
title = Zeiterfassung
package.name = zeiterfassung
package.domain = org.tkideneb

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,xml

version = 1.0

requirements = python3,kivy,fpdf2,fonttools==4.38.0,pillow,defusedxml

icon.filename = ./icon.png

android.add_res_dirs = res
android.resource_dirs = res

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True
android.meta_data = android.support.FILE_PROVIDER_PATHS=@xml/fileprovider_paths
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0
