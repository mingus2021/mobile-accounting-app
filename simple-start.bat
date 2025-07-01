@echo off
title Python Mobile Accounting App - Simple Start

echo ========================================
echo Python Mobile Accounting App
echo Simple Start (No Dependencies Install)
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

:: Create missing directories
echo Creating project structure...
if not exist "app" mkdir app
if not exist "app\core" mkdir app\core
if not exist "app\ui" mkdir app\ui
if not exist "app\data" mkdir app\data
if not exist "assets" mkdir assets
if not exist "assets\icons" mkdir assets\icons
if not exist "data" mkdir data

:: Create __init__.py files
echo. > app\__init__.py
echo. > app\core\__init__.py
echo. > app\ui\__init__.py
echo. > app\data\__init__.py

echo SUCCESS: Project structure created
echo.

:: Check if dependencies are installed
echo Checking dependencies...
python -c "import kivy" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Kivy not found
    echo Please install manually: pip install kivy kivymd requests cryptography
    echo.
    echo Or run: quick-start.bat to auto-install
    echo.
    set /p choice="Continue anyway? (y/n): "
    if /i not "%choice%"=="y" (
        pause
        exit /b 1
    )
) else (
    echo SUCCESS: Dependencies found
)

echo.

:: Run the app
echo Starting the mobile app...
echo.
python main.py

echo.
echo App closed
pause
