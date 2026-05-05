[app]
title = X-O super
package.name = xosuper
package.domain = org.kirllos
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.2

# المكتبات المطلوبة للتشغيل والاتصال
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,idna,charset-normalizer,pyjnius

# الصلاحيات المطلوبة (ستظهر للمستخدم عند فتح اللعبة)
android.permissions = INTERNET, CAMERA, RECORD_AUDIO

android.api = 34
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
orientation = portrait
fullscreen = 1
log_level = 2

[buildozer]
log_level = 2
warn_on_root = 1
