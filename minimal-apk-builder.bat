@echo off
title Minimal APK Builder for Windows 10

echo ========================================
echo Python Mobile App - Minimal APK Builder
echo Windows 10 Optimized
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo SUCCESS: Python found
python --version
echo.

:: Check Java
echo Checking Java JDK...
java -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: Java not found
    echo.
    echo To build APK locally, you need Java JDK 8:
    echo 1. Download from: https://adoptium.net/temurin/releases/?version=8
    echo 2. Install and add to PATH
    echo 3. Set JAVA_HOME environment variable
    echo.
    echo Alternative: Use GitHub Actions (no local Java needed)
    echo.
    set /p choice="Continue with GitHub Actions setup? (y/n): "
    if /i not "%choice%"=="y" (
        pause
        exit /b 1
    )
    goto github_actions
) else (
    echo SUCCESS: Java found
    java -version
    echo.
    goto local_build
)

:local_build
echo ========================================
echo Local APK Build Setup
echo ========================================
echo.

:: Install buildozer
echo Checking buildozer...
python -c "import buildozer" >nul 2>&1
if errorlevel 1 (
    echo Installing buildozer and dependencies...
    pip install buildozer cython
    
    if errorlevel 1 (
        echo ERROR: Failed to install buildozer
        echo Try: pip install buildozer cython --user
        pause
        exit /b 1
    )
) else (
    echo SUCCESS: Buildozer found
)

echo.

:: Initialize buildozer if needed
if not exist "buildozer.spec" (
    echo Initializing buildozer configuration...
    buildozer init
    
    echo.
    echo Optimizing buildozer.spec for minimal build...
    
    :: Create optimized buildozer.spec
    echo [app] > buildozer_minimal.spec
    echo title = 记账本 >> buildozer_minimal.spec
    echo package.name = accounting >> buildozer_minimal.spec
    echo package.domain = com.accounting.app >> buildozer_minimal.spec
    echo source.dir = . >> buildozer_minimal.spec
    echo version = 1.0.0 >> buildozer_minimal.spec
    echo requirements = python3,kivy,requests,cryptography >> buildozer_minimal.spec
    echo orientation = portrait >> buildozer_minimal.spec
    echo android.permissions = INTERNET >> buildozer_minimal.spec
    echo android.archs = arm64-v8a >> buildozer_minimal.spec
    echo [buildozer] >> buildozer_minimal.spec
    echo log_level = 2 >> buildozer_minimal.spec
    
    copy buildozer_minimal.spec buildozer.spec
    del buildozer_minimal.spec
    
    echo SUCCESS: Optimized configuration created
)

echo.
echo Choose build option:
echo 1. Debug APK (faster, for testing)
echo 2. Release APK (optimized, for distribution)
echo 3. Clean build (remove cache and rebuild)
echo.

set /p build_choice="Enter choice (1-3): "

if "%build_choice%"=="1" (
    echo Building debug APK...
    buildozer android debug
) else if "%build_choice%"=="2" (
    echo Building release APK...
    buildozer android release
) else if "%build_choice%"=="3" (
    echo Cleaning and rebuilding...
    buildozer android clean
    buildozer android debug
) else (
    echo Invalid choice, building debug APK...
    buildozer android debug
)

if errorlevel 1 (
    echo.
    echo ========================================
    echo BUILD FAILED
    echo ========================================
    echo.
    echo Common solutions:
    echo 1. Android SDK will be auto-downloaded on first run
    echo 2. Ensure stable internet connection
    echo 3. Try clean build: buildozer android clean
    echo 4. Check buildozer.spec configuration
    echo.
    echo Alternative: Use GitHub Actions for cloud build
    echo.
) else (
    echo.
    echo ========================================
    echo BUILD SUCCESS!
    echo ========================================
    echo.
    echo APK files created:
    if exist "bin" (
        dir bin\*.apk
        echo.
        echo To install on device:
        echo 1. Enable Developer Options on Android
        echo 2. Enable USB Debugging
        echo 3. Run: adb install bin\accounting-1.0.0-debug.apk
        echo.
        echo Or copy APK to device and install manually
    )
)

goto end

:github_actions
echo ========================================
echo GitHub Actions Setup
echo ========================================
echo.

echo Creating GitHub Actions workflow...

if not exist ".github" mkdir .github
if not exist ".github\workflows" mkdir .github\workflows

echo name: Build APK > .github\workflows\build-apk.yml
echo. >> .github\workflows\build-apk.yml
echo on: >> .github\workflows\build-apk.yml
echo   push: >> .github\workflows\build-apk.yml
echo     branches: [ main ] >> .github\workflows\build-apk.yml
echo   workflow_dispatch: >> .github\workflows\build-apk.yml
echo. >> .github\workflows\build-apk.yml
echo jobs: >> .github\workflows\build-apk.yml
echo   build: >> .github\workflows\build-apk.yml
echo     runs-on: ubuntu-latest >> .github\workflows\build-apk.yml
echo. >> .github\workflows\build-apk.yml
echo     steps: >> .github\workflows\build-apk.yml
echo     - uses: actions/checkout@v3 >> .github\workflows\build-apk.yml
echo. >> .github\workflows\build-apk.yml
echo     - name: Setup Python >> .github\workflows\build-apk.yml
echo       uses: actions/setup-python@v4 >> .github\workflows\build-apk.yml
echo       with: >> .github\workflows\build-apk.yml
echo         python-version: '3.9' >> .github\workflows\build-apk.yml
echo. >> .github\workflows\build-apk.yml
echo     - name: Install dependencies >> .github\workflows\build-apk.yml
echo       run: ^| >> .github\workflows\build-apk.yml
echo         python -m pip install --upgrade pip >> .github\workflows\build-apk.yml
echo         pip install buildozer cython >> .github\workflows\build-apk.yml
echo. >> .github\workflows\build-apk.yml
echo     - name: Build APK >> .github\workflows\build-apk.yml
echo       run: ^| >> .github\workflows\build-apk.yml
echo         buildozer android debug >> .github\workflows\build-apk.yml
echo. >> .github\workflows\build-apk.yml
echo     - name: Upload APK >> .github\workflows\build-apk.yml
echo       uses: actions/upload-artifact@v3 >> .github\workflows\build-apk.yml
echo       with: >> .github\workflows\build-apk.yml
echo         name: accounting-apk >> .github\workflows\build-apk.yml
echo         path: bin/*.apk >> .github\workflows\build-apk.yml

echo SUCCESS: GitHub Actions workflow created
echo.
echo Next steps:
echo 1. Create GitHub repository
echo 2. Push code to GitHub:
echo    git init
echo    git add .
echo    git commit -m "Initial commit"
echo    git remote add origin https://github.com/yourusername/mobile-accounting.git
echo    git push -u origin main
echo.
echo 3. APK will be built automatically in GitHub Actions
echo 4. Download APK from Actions artifacts
echo.

:end
echo ========================================
echo Setup Complete
echo ========================================
pause
