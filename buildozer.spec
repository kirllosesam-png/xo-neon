[app]

# (section) عنوان التطبيق واسم الحزمة
title = Neon XO
package.name = xoneon
package.domain = org.kirllos

# (section) مسار الكود والمستندات
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# --- أهم جزء: المكتبات المطلوبة ---
# زودنا websocket-client و urllib3 عشان الـ Socket.io يشتغل من غير ما يخرج
requirements = python3, kivy==2.3.0, plyer, python-socketio, websocket-client, requests, urllib3, setuptools

orientation = portrait

# --- ثاني أهم جزء: الصلاحيات ---
# هنا بنطلب الكاميرا والصوت والموقع والإنترنت
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (section) إعدادات الشاشة والأيقونات
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# --- إعدادات الأندرويد SDK و NDK ---
# يفضل استخدام إصدارات مستقرة
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# (section) منع الشاشة من الإغلاق أثناء اللعب
android.wakelock = True

[buildozer]
log_level = 2
warn_on_root = 1
