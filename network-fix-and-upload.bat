@echo off
chcp 65001 >nul
title Network Fix and Upload

echo ========================================
echo Network Connection Fix and Upload
echo ========================================
echo.

echo Step 1: Test network connectivity
echo ----------------------------------------
echo Testing GitHub connection...
ping github.com -n 2 >nul 2>&1
if errorlevel 1 (
    echo ❌ GitHub connection failed
    echo.
    echo Possible solutions:
    echo 1. Check your internet connection
    echo 2. Try using VPN if in restricted network
    echo 3. Use mobile hotspot temporarily
    echo 4. Try different DNS servers
    echo.
    goto :network_solutions
) else (
    echo ✅ GitHub connection successful
    goto :upload
)

:network_solutions
echo Step 2: Network troubleshooting
echo ----------------------------------------
echo.
echo Option A: Change DNS servers
echo ----------------------------------------
echo Run these commands as Administrator:
echo netsh interface ip set dns "Wi-Fi" static 8.8.8.8
echo netsh interface ip add dns "Wi-Fi" 8.8.4.4 index=2
echo.
echo Option B: Flush DNS cache
echo ----------------------------------------
echo ipconfig /flushdns
echo.
echo Option C: Reset network adapter
echo ----------------------------------------
echo netsh winsock reset
echo netsh int ip reset
echo.
echo Option D: Use mobile hotspot
echo ----------------------------------------
echo 1. Enable mobile hotspot on your phone
echo 2. Connect computer to hotspot
echo 3. Run this script again
echo.
echo Option E: Try VPN connection
echo ----------------------------------------
echo If you're behind a firewall, try connecting to VPN
echo.

echo Attempting automatic DNS fix...
echo ----------------------------------------
nslookup github.com 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    echo DNS resolution failed
) else (
    echo DNS resolution works with Google DNS
    echo Try changing your DNS to 8.8.8.8 and 8.8.4.4
)
echo.

echo Waiting 30 seconds before retry...
timeout /t 30 /nobreak >nul
echo.

echo Retrying GitHub connection...
ping github.com -n 2 >nul 2>&1
if errorlevel 1 (
    echo ❌ Still cannot connect to GitHub
    echo.
    echo Manual steps required:
    echo 1. Fix your internet connection
    echo 2. Run this command when connection is restored:
    echo    git push origin main
    echo.
    goto :manual_instructions
) else (
    echo ✅ Connection restored!
    goto :upload
)

:upload
echo Step 3: Upload to GitHub
echo ----------------------------------------
echo Pushing changes to GitHub...
git push origin main

if errorlevel 1 (
    echo Push failed, trying force push...
    git push origin main --force
    
    if errorlevel 1 (
        echo All push methods failed
        goto :manual_instructions
    )
)

echo.
echo ========================================
echo SUCCESS: Changes uploaded to GitHub!
echo ========================================
echo.
echo GitHub Actions will automatically start building
echo Monitor progress at: https://github.com/mingus2021/mobile-accounting-app/actions
echo.
goto :end

:manual_instructions
echo ========================================
echo MANUAL UPLOAD REQUIRED
echo ========================================
echo.
echo Your changes are committed locally but not uploaded.
echo When your internet connection is restored, run:
echo.
echo    cd mobile-app
echo    git push origin main
echo.
echo Or use GitHub Desktop:
echo 1. Open GitHub Desktop
echo 2. Select this repository
echo 3. Click "Push origin"
echo.

:end
echo Press any key to exit...
pause >nul
