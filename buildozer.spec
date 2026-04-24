[app]
title = XO Neon Pro
package.name = xoneonpro
package.domain = org.krollos
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات اللي بتنجح دايماً
requirements = python3,kivy==2.3.0,requests

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

# الزتونة هنا (إعدادات الـ Toolchain الصح)
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_path = 
android.sdk_path = 
android.accept_sdk_license = True

# حددنا نوع المعالج بالظبط عشان ما يقعدش يدور
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
