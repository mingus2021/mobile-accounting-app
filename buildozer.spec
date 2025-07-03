[app]
title = Hello World
package.name = helloworld
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25.2.9519653
android.sdk = 33
android.accept_sdk_license = True
android.skip_update = False
android.debug_artifact = True
