[app]
title = XO Neon Pro
package.name = xoneonpro
package.domain = org.krollos
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات اللي بيحتاجها Kivy دايماً
requirements = python3,kivy==2.3.0,requests

# إعدادات الأندرويد اللي المطورين بيثبتوها
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

# دي عشان الصور والملفات تظهر صح في التطبيق
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
