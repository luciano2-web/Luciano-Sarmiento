# buildozer.spec para compilar GatoGPT Félix a APK/AAB
# Usar: buildozer android debug

[app]
title = GatoGPT Félix Mobile
package.name = gato_gpt_felix
package.domain = org.luciano

source.dir = ../..
source.include_exts = py,png,jpg,kv,atlas,yaml

version = 1.0.0

requirements = python3,kivy,bleak==3.0.1,pyjnius,numpy,pillow,torch,transformers,accelerate,bitsandbytes,diffusers,safetensors

orientation = portrait
fullscreen = 0
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA
android.api = 31
android.minapi = 21
android.ndk = 25c
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
