@echo off
title Install Dependencies for Mobile App

echo ========================================
echo Installing Dependencies
echo ========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

:: Upgrade pip first
echo Upgrading pip...
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

echo.
echo Installing core dependencies...

:: Install dependencies one by one
echo Installing requests...
pip install requests --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

echo Installing cryptography...
pip install cryptography --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

echo Installing certifi...
pip install certifi --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

echo Installing kivy...
pip install kivy --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

echo Installing kivymd...
pip install kivymd --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

echo.
echo Verifying installation...
python -c "import requests; print('✓ requests')"
python -c "import cryptography; print('✓ cryptography')"
python -c "import certifi; print('✓ certifi')"
python -c "import kivy; print('✓ kivy')"
python -c "import kivymd; print('✓ kivymd')"

echo.
echo SUCCESS: All dependencies installed!
echo You can now run: simple-start.bat
echo.
pause
