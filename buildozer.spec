[app]
title = XO Neon Pro
package.name = xoneonpro
package.domain = org.krollos
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات الأساسية
requirements = python3,kivy==2.3.0,requests,urllib3

# إعدادات الأندرويد (دي اللي كانت بتعمل Error)
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0

# الأرقام دي "مقدسة" عشان يشتغل على جيت هاب
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_path = 
android.sdk_path = 
android.accept_sdk_license = True
android.archs = arm64-v8a

# عشان لو فيه أي صور أو ملفات ناقصة ما يوقفش الـ Build
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
