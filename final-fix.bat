@echo off
cd /d f:\work\electron-accounting\mobile-app

echo Fixing final upload-artifact version...
git add .github/workflows/build-apk.yml
git commit -m "Fix: Update remaining upload-artifact to v4"
git push origin main

echo Done! Check GitHub Actions again.
pause
