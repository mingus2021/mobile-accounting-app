# PowerShell script for building APK
# Run with: PowerShell -ExecutionPolicy Bypass -File Build-APK.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Python Mobile App APK Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "SUCCESS: Python found" -ForegroundColor Green
    Write-Host $pythonVersion -ForegroundColor Yellow
} catch {
    Write-Host "ERROR: Python not found" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Check Java
try {
    $javaVersion = java -version 2>&1
    Write-Host "SUCCESS: Java found" -ForegroundColor Green
    Write-Host $javaVersion[0] -ForegroundColor Yellow
    $hasJava = $true
} catch {
    Write-Host "WARNING: Java not found" -ForegroundColor Yellow
    $hasJava = $false
}

Write-Host ""

if (-not $hasJava) {
    Write-Host "Choose build method:" -ForegroundColor Cyan
    Write-Host "1. Install Java JDK 8 for local build" -ForegroundColor White
    Write-Host "2. Use GitHub Actions for cloud build" -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Enter choice (1-2)"
    
    if ($choice -eq "1") {
        Write-Host ""
        Write-Host "Download Java JDK 8 from:" -ForegroundColor Yellow
        Write-Host "https://adoptium.net/temurin/releases/?version=8" -ForegroundColor Blue
        Write-Host ""
        Write-Host "After installation:" -ForegroundColor Yellow
        Write-Host "1. Add Java to PATH" -ForegroundColor White
        Write-Host "2. Set JAVA_HOME environment variable" -ForegroundColor White
        Write-Host "3. Run this script again" -ForegroundColor White
        Read-Host "Press Enter to exit"
        exit 1
    } elseif ($choice -eq "2") {
        # GitHub Actions setup
        Write-Host ""
        Write-Host "Setting up GitHub Actions..." -ForegroundColor Cyan
        
        # Create directories
        if (-not (Test-Path ".github")) { New-Item -ItemType Directory -Path ".github" }
        if (-not (Test-Path ".github\workflows")) { New-Item -ItemType Directory -Path ".github\workflows" }
        
        # Create workflow file
        $workflowContent = @"
name: Build Android APK

on:
  push:
    branches: [ main, master ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython
    
    - name: Create missing directories
      run: |
        mkdir -p app/core app/ui app/data assets/icons data
        touch app/__init__.py app/core/__init__.py app/ui/__init__.py app/data/__init__.py
    
    - name: Copy buildozer config
      run: |
        if [ ! -f buildozer.spec ]; then
          cp buildozer-minimal.spec buildozer.spec
        fi
    
    - name: Build APK
      run: |
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: accounting-app-debug
        path: bin/*.apk
"@
        
        $workflowContent | Out-File -FilePath ".github\workflows\build-apk.yml" -Encoding UTF8
        
        Write-Host "SUCCESS: GitHub Actions workflow created" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Cyan
        Write-Host "1. Create GitHub repository" -ForegroundColor White
        Write-Host "2. Upload code:" -ForegroundColor White
        Write-Host "   git init" -ForegroundColor Gray
        Write-Host "   git add ." -ForegroundColor Gray
        Write-Host "   git commit -m 'Initial commit'" -ForegroundColor Gray
        Write-Host "   git remote add origin https://github.com/yourusername/repo.git" -ForegroundColor Gray
        Write-Host "   git push -u origin main" -ForegroundColor Gray
        Write-Host ""
        Write-Host "3. APK will build automatically in GitHub Actions" -ForegroundColor White
        Write-Host "4. Download APK from Actions artifacts" -ForegroundColor White
        
        Read-Host "Press Enter to exit"
        exit 0
    } else {
        Write-Host "Invalid choice" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Local build with Java
Write-Host "Starting local build..." -ForegroundColor Cyan
Write-Host ""

# Check if buildozer is installed
try {
    python -c "import buildozer" 2>$null
    Write-Host "SUCCESS: Buildozer found" -ForegroundColor Green
} catch {
    Write-Host "Installing buildozer..." -ForegroundColor Yellow
    pip install buildozer cython
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install buildozer" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host "SUCCESS: Buildozer installed" -ForegroundColor Green
}

Write-Host ""

# Create missing directories
Write-Host "Creating project structure..." -ForegroundColor Yellow
$directories = @("app", "app\core", "app\ui", "app\data", "assets", "assets\icons", "data")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

# Create __init__.py files
$initFiles = @("app\__init__.py", "app\core\__init__.py", "app\ui\__init__.py", "app\data\__init__.py")
foreach ($file in $initFiles) {
    if (-not (Test-Path $file)) {
        "" | Out-File -FilePath $file -Encoding UTF8
    }
}

Write-Host "SUCCESS: Project structure created" -ForegroundColor Green
Write-Host ""

# Copy buildozer config if not exists
if (-not (Test-Path "buildozer.spec")) {
    if (Test-Path "buildozer-minimal.spec") {
        Copy-Item "buildozer-minimal.spec" "buildozer.spec"
        Write-Host "SUCCESS: Buildozer config created" -ForegroundColor Green
    } else {
        Write-Host "Initializing buildozer..." -ForegroundColor Yellow
        buildozer init
    }
}

Write-Host ""

# Build options
Write-Host "Choose build type:" -ForegroundColor Cyan
Write-Host "1. Debug APK (faster, for testing)" -ForegroundColor White
Write-Host "2. Release APK (optimized, for distribution)" -ForegroundColor White
Write-Host "3. Clean build (remove cache and rebuild)" -ForegroundColor White
Write-Host ""

$buildChoice = Read-Host "Enter choice (1-3)"

Write-Host ""
Write-Host "Building APK..." -ForegroundColor Cyan

switch ($buildChoice) {
    "1" {
        Write-Host "Building debug APK..." -ForegroundColor Yellow
        buildozer android debug
    }
    "2" {
        Write-Host "Building release APK..." -ForegroundColor Yellow
        buildozer android release
    }
    "3" {
        Write-Host "Cleaning and rebuilding..." -ForegroundColor Yellow
        buildozer android clean
        buildozer android debug
    }
    default {
        Write-Host "Invalid choice, building debug APK..." -ForegroundColor Yellow
        buildozer android debug
    }
}

Write-Host ""

if ($LASTEXITCODE -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "BUILD SUCCESS!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    if (Test-Path "bin") {
        Write-Host "APK files created:" -ForegroundColor Cyan
        Get-ChildItem "bin\*.apk" | ForEach-Object { Write-Host $_.Name -ForegroundColor Yellow }
        Write-Host ""
        Write-Host "To install on device:" -ForegroundColor Cyan
        Write-Host "1. Enable Developer Options on Android" -ForegroundColor White
        Write-Host "2. Enable USB Debugging" -ForegroundColor White
        Write-Host "3. Run: adb install bin\accounting-1.0.0-debug.apk" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Or copy APK to device and install manually" -ForegroundColor White
    }
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "BUILD FAILED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "1. Android SDK will be auto-downloaded on first run" -ForegroundColor White
    Write-Host "2. Ensure stable internet connection" -ForegroundColor White
    Write-Host "3. Try clean build: buildozer android clean" -ForegroundColor White
    Write-Host "4. Check buildozer.spec configuration" -ForegroundColor White
    Write-Host ""
    Write-Host "Alternative: Use GitHub Actions for cloud build" -ForegroundColor Cyan
}

Write-Host ""
Read-Host "Press Enter to exit"
