# buildozer.spec para compilar GatoGPT Félix a APK/AAB
# Usar: buildozer android debug

[app]
title = GatoGPT Félix Mobile
package.name = gato_gpt_felix
package.domain = org.luciano

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,yaml

version = 1.0.0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
add_src = gatogpt_felix_mobile.py
main_activity = org.kivy.android.PythonActivity

requirements = python3,kivy,numpy,pillow,torch,transformers,accelerate,bitsandbytes,diffusers,safetensors

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA
android.api = 31
android.minapi = 21
android.ndk = 25c
android.accept_sdk_license = True

[app:ios]
ios.kivy_ios_branch = master
ios.requirements = python3,kivy,numpy,pillow,torch,transformers
ios.deployment_target = 15.0
