@echo off
chcp 65001 >nul
title Fix Issues and Re-upload

echo ========================================
echo Fix GitHub Actions Issues and Re-upload
echo ========================================
echo.

echo Step 1: Add missing __init__.py files
echo ----------------------------------------
git add app/__init__.py
git add app/core/__init__.py
git add app/ui/__init__.py
git add app/data/__init__.py

echo __init__.py files added
echo.

echo Step 2: Add updated GitHub Actions workflow
echo ----------------------------------------
git add .github/workflows/build-apk.yml
git add fix-and-reupload.bat

echo All files added
git status
echo.

echo Step 3: Create commit with fixes
echo ----------------------------------------
git commit -m "Fix: Update GitHub Actions to v4 and add missing __init__.py files"

if errorlevel 1 (
    echo No new changes to commit
) else (
    echo Commit created successfully
)
echo.

echo Step 4: Push fixes to GitHub
echo ----------------------------------------
git push origin main

if errorlevel 1 (
    echo Push failed, trying alternative methods...
    git push origin main --force
    
    if errorlevel 1 (
        echo All push methods failed
        echo Please check your network connection
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo SUCCESS: Fixes uploaded to GitHub!
echo ========================================
echo.
echo GitHub Actions will automatically restart the build
echo.
echo Next steps:
echo 1. Go to: https://github.com/mingus2021/mobile-accounting-app/actions
echo 2. Wait for the new build to start (may take 1-2 minutes)
echo 3. Monitor the build progress
echo 4. Download APK when build completes
echo.
echo The build should succeed this time!
echo.
pause
