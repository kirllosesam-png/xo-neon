[app]
title = XO Neon
package.name = xoneon
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET, CAMERA, RECORD_AUDIO, ACCESS_FINE_LOCATION, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, FOREGROUND_SERVICE, WAKE_LOCK, REQUEST_IGNORE_BATTERY_OPTIMIZATIONS
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
