@echo off
title Python Mobile App - APK Builder

echo ========================================
echo Python Mobile Accounting App
echo APK Builder Script
echo ========================================
echo.

:: Check buildozer
buildozer --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Buildozer not found
    echo Installing buildozer...
    pip install buildozer
    
    if errorlevel 1 (
        echo ERROR: Failed to install buildozer
        echo Please install manually: pip install buildozer
        pause
        exit /b 1
    )
)

echo SUCCESS: Buildozer found
buildozer --version
echo.

:: Check Android SDK
if not defined ANDROID_HOME (
    echo WARNING: ANDROID_HOME not set
    echo Please install Android SDK and set ANDROID_HOME
    echo.
)

:: Initialize buildozer (if needed)
if not exist "buildozer.spec" (
    echo Initializing buildozer...
    buildozer init
)

echo.
echo Choose build type:
echo 1. Debug APK (faster, for testing)
echo 2. Release APK (optimized, for distribution)
echo 3. Clean build (remove cache and rebuild)
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Building debug APK...
    buildozer android debug
) else if "%choice%"=="2" (
    echo Building release APK...
    buildozer android release
) else if "%choice%"=="3" (
    echo Cleaning and rebuilding...
    buildozer android clean
    buildozer android debug
) else (
    echo Invalid choice, building debug APK...
    buildozer android debug
)

if errorlevel 1 (
    echo.
    echo ERROR: Build failed
    echo Check the error messages above
    echo.
    echo Common solutions:
    echo 1. Install Android SDK and NDK
    echo 2. Set ANDROID_HOME environment variable
    echo 3. Install Java JDK 8
    echo 4. Check buildozer.spec configuration
    echo.
) else (
    echo.
    echo SUCCESS: APK built successfully!
    echo.
    echo APK location: bin\
    dir bin\*.apk
    echo.
    echo To install on device:
    echo adb install bin\accounting-1.0.0-debug.apk
    echo.
)

pause
