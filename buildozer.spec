[app]
title = Mobile Accounting
package.name = mobileaccounting
package.domain = org.example
source.dir = .
source.include_exts = py,kv
version = 0.1
requirements = python3,kivy
orientation = portrait
android.permissions = INTERNET

# Android specific
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25.2.9519653
android.skip_update = False
android.accept_sdk_license = True
android.gradle_dependencies =

# Build configuration
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
