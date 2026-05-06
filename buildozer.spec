[app]
title = Neon XO
package.name = xoneon
package.domain = org.kirllos
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات البرمجية
requirements = python3,kivy,plyer,python-socketio,requests,websocket-client,urllib3

orientation = portrait

# الصلاحيات المطلوبة (Permissions)
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# إعدادات الأندرويد
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

# أيقونة التطبيق (اختياري)
# android.icon.filename = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
