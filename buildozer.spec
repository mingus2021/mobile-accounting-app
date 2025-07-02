[app]
title = Mobile Accounting
package.name = mobileaccounting
package.domain = org.example
source.dir = .
source.include_exts = py
version = 0.1
requirements = python3,kivy
orientation = portrait
android.permissions = INTERNET

# Android specific
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.skip_update = False
android.accept_sdk_license = True

[buildozer]
log_level = 2
