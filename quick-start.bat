@echo off
title Python Mobile Accounting App - Quick Start

echo ========================================
echo Python Mobile Accounting App
echo Quick Start Script
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo SUCCESS: Python found
python --version
echo.

:: Install dependencies
echo Installing dependencies...
echo Using trusted hosts to avoid SSL issues...

:: Try with trusted hosts first
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

if errorlevel 1 (
    echo Trying with alternative method...
    pip install kivy kivymd requests cryptography certifi --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo.
        echo Possible solutions:
        echo 1. Check internet connection
        echo 2. Try: pip install --upgrade pip
        echo 3. Try: pip install --upgrade certifi
        echo 4. Use VPN if behind firewall
        pause
        exit /b 1
    )
)

echo SUCCESS: Dependencies installed
echo.

:: Create missing directories
if not exist "app\core" mkdir app\core
if not exist "app\ui" mkdir app\ui
if not exist "app\data" mkdir app\data
if not exist "assets\icons" mkdir assets\icons
if not exist "data" mkdir data

:: Create __init__.py files
echo. > app\__init__.py
echo. > app\core\__init__.py
echo. > app\ui\__init__.py
echo. > app\data\__init__.py

echo SUCCESS: Project structure created
echo.

:: Run the app
echo Starting the mobile app...
echo.
python main.py

echo.
echo App closed
pause
