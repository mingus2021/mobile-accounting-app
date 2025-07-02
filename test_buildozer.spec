
[app]
title = Test App
package.name = testapp
package.domain = org.test
source.dir = .
version = 0.1
requirements = python3,kivy

[buildozer]
log_level = 2

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.accept_sdk_license = True
android.archs = arm64-v8a
