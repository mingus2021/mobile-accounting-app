@echo off
chcp 65001 >nul
title Fix Git and Upload to GitHub

echo ========================================
echo Fix Git Repository and Upload to GitHub
echo ========================================
echo.

echo Step 1: Check current Git status
echo ----------------------------------------
git status
echo.

echo Step 2: Check remote repository
echo ----------------------------------------
git remote -v
echo.

echo Step 3: Update remote repository URL
echo ----------------------------------------
git remote set-url origin https://github.com/mingus2021/mobile-accounting-app.git
echo Remote URL updated
git remote -v
echo.

echo Step 4: Check tracked files
echo ----------------------------------------
echo Tracked files:
git ls-files
echo.
echo All files in directory:
dir /b
echo.

echo Step 5: Force add all important files
echo ----------------------------------------
git add main.py --force
git add app/ --force
git add requirements.txt --force
git add buildozer-minimal.spec --force
git add .github/ --force
git add test-iss-only.py --force
git add build_apk.py --force
git add *.md --force
git add .gitignore --force

echo Files added to staging area
git status
echo.

echo Step 6: Create commit if there are changes
echo ----------------------------------------
git diff --cached --quiet
if errorlevel 1 (
    echo Creating commit...
    git commit -m "Add Python mobile accounting app with ISS support and GitHub Actions"
    echo Commit created successfully
) else (
    echo No changes to commit, checking if we need to push existing commits...
)
echo.

echo Step 7: Check if GitHub repository exists
echo ----------------------------------------
echo Please make sure you have created the repository on GitHub:
echo https://github.com/mingus2021/mobile-accounting-app
echo.
set /p continue="Have you created the GitHub repository? (y/n): "
if /i not "%continue%"=="y" (
    echo.
    echo Please create the repository first:
    echo 1. Go to https://github.com/new
    echo 2. Repository name: mobile-accounting-app
    echo 3. Description: Python mobile accounting app with ISS support
    echo 4. Public repository
    echo 5. Do NOT initialize with README, .gitignore, or license
    echo 6. Click "Create repository"
    echo.
    pause
    exit /b 1
)

echo Step 8: Push to GitHub
echo ----------------------------------------
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo Push failed. Trying alternative methods...
    echo.
    
    echo Method 1: Force push
    git push -u origin main --force
    
    if errorlevel 1 (
        echo.
        echo Method 2: Push to master branch
        git push -u origin main:master
        
        if errorlevel 1 (
            echo.
            echo All push methods failed. Manual steps needed:
            echo.
            echo 1. Check your GitHub credentials
            echo 2. Make sure the repository exists
            echo 3. Try: git push -u origin main --verbose
            echo.
            pause
            exit /b 1
        )
    )
)

echo.
echo ========================================
echo SUCCESS: Code uploaded to GitHub!
echo ========================================
echo.
echo Repository URL: https://github.com/mingus2021/mobile-accounting-app
echo.
echo Next steps:
echo 1. Visit your GitHub repository
echo 2. Go to Actions tab
echo 3. GitHub Actions will automatically build APK
echo 4. Download APK from Actions artifacts
echo.
echo GitHub Actions workflow will start automatically!
echo.
pause
