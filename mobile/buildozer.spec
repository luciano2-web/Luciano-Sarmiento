[app]
title = GatoGPT Félix
package.name = gatogptfelix
package.domain = com.luciano2web
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3,kivy,transformers,accelerate,torch,pillow,sentencepiece
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a
android.allow_backup = True
icon.filename = icon.png
presplash.filename = presplash.png
android.logcat_filters = *:S python:D
p4a.local_recipes =
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.deploy_url = https://github.com/phonegap/ios-deploy
ios.deploy_branch = 1.12.2
[buildozer]
log_level = 2
warn_on_root = 1
