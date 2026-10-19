[app]
title = PS5 App
package.name = ps5app
package.domain = org.ps5
source.dir = .
source.include_exts = py
version = 1.0
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0,pyjnius
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_WIFI_STATE,ACCESS_NETWORK_STATE,CHANGE_WIFI_MULTICAST_STATE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
