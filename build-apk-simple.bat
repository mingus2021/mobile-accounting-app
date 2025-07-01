@echo off
chcp 65001 >nul
title APK Builder

echo ========================================
echo Python Mobile App APK Builder
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo SUCCESS: Python found
python --version
echo.

echo Checking Java...
java -version >nul 2>&1
if errorlevel 1 (
    echo Java not found. Choose option:
    echo 1. Install Java JDK 8 for local build
    echo 2. Use GitHub Actions for cloud build
    echo.
    set /p choice="Enter choice (1-2): "
    if "%choice%"=="1" (
        echo.
        echo Download Java JDK 8 from:
        echo https://adoptium.net/temurin/releases/?version=8
        echo.
        echo After installation, run this script again
        pause
        exit /b 1
    ) else (
        goto github_setup
    )
) else (
    echo SUCCESS: Java found
    java -version
    goto local_build
)

:local_build
echo.
echo Installing buildozer...
pip install buildozer cython

echo.
echo Creating buildozer config...
if not exist "buildozer.spec" (
    copy buildozer-minimal.spec buildozer.spec
)

echo.
echo Building APK...
buildozer android debug

if errorlevel 1 (
    echo BUILD FAILED
    echo Try: buildozer android clean
) else (
    echo BUILD SUCCESS!
    dir bin\*.apk
)

goto end

:github_setup
echo.
echo Setting up GitHub Actions...

if not exist ".github" mkdir .github
if not exist ".github\workflows" mkdir .github\workflows

echo GitHub Actions workflow created
echo.
echo Next steps:
echo 1. Create GitHub repository
echo 2. Upload code: git add . && git commit -m "init" && git push
echo 3. APK will build automatically
echo.

:end
pause
