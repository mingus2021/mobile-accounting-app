# 📱 Windows 10 Python APK打包指南

## 🎯 最简化方案（推荐）

### 方案1: 使用GitHub Actions（零本地工具）

**优势**：
- ✅ 无需本地安装Android SDK
- ✅ 无需配置复杂环境
- ✅ 云端自动构建
- ✅ 支持多架构APK

#### 步骤：

1. **创建GitHub仓库**
```bash
# 将代码上传到GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/mobile-accounting.git
git push -u origin main
```

2. **创建GitHub Actions配置**
```yaml
# .github/workflows/build-apk.yml
name: Build APK

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install buildozer cython
    
    - name: Build APK
      run: |
        cd mobile-app
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: accounting-apk
        path: mobile-app/bin/*.apk
```

3. **推送代码，自动构建**
```bash
git add .github/workflows/build-apk.yml
git commit -m "Add APK build workflow"
git push
```

### 方案2: 本地最小化安装

**仅需安装的工具**：
1. Python（已有）
2. Java JDK 8
3. Buildozer

#### 详细步骤：

**第一步：安装Java JDK 8**
```bash
# 下载并安装 OpenJDK 8
# https://adoptium.net/temurin/releases/?version=8

# 设置环境变量（添加到系统环境变量）
JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-8.0.392.8-hotspot
PATH=%PATH%;%JAVA_HOME%\bin
```

**第二步：安装Buildozer**
```bash
pip install buildozer cython
```

**第三步：初始化和构建**
```bash
cd mobile-app
buildozer init
buildozer android debug
```

### 方案3: 使用Docker（推荐给有Docker的用户）

**优势**：
- ✅ 环境隔离
- ✅ 一次配置，多次使用
- ✅ 无需本地Android SDK

```dockerfile
# Dockerfile
FROM kivy/buildozer:latest

WORKDIR /app
COPY . .

RUN buildozer android debug

CMD ["cp", "bin/*.apk", "/output/"]
```

```bash
# 构建命令
docker build -t mobile-accounting .
docker run -v %cd%\output:/output mobile-accounting
```

## 🔧 buildozer.spec 优化配置

```ini
[app]
title = 记账本
package.name = accounting
package.domain = com.accounting.app

# 最小化依赖
requirements = python3,kivy,requests,cryptography

# 减小APK体积
android.archs = arm64-v8a
android.permissions = INTERNET

# 优化构建
android.gradle_dependencies = 
android.add_src = 
android.add_aars = 

[buildozer]
log_level = 2
```

## 🚀 一键构建脚本

```batch
@echo off
title APK Builder - Minimal Setup

echo ========================================
echo Python Mobile App - APK Builder
echo Minimal Setup for Windows 10
echo ========================================

:: Check Java
java -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Java not found
    echo Please install OpenJDK 8 from:
    echo https://adoptium.net/temurin/releases/?version=8
    pause
    exit /b 1
)

echo SUCCESS: Java found
java -version

:: Install buildozer if not exists
python -c "import buildozer" >nul 2>&1
if errorlevel 1 (
    echo Installing buildozer...
    pip install buildozer cython
)

:: Initialize if needed
if not exist "buildozer.spec" (
    echo Initializing buildozer...
    buildozer init
)

:: Build APK
echo Building APK...
buildozer android debug

if errorlevel 1 (
    echo BUILD FAILED
    echo Common solutions:
    echo 1. Install Android SDK manually
    echo 2. Use GitHub Actions instead
    echo 3. Use Docker method
) else (
    echo BUILD SUCCESS!
    echo APK location: bin\
    dir bin\*.apk
)

pause
```

## 📦 APK体积优化

### 减小APK大小的方法：

1. **最小化依赖**
```python
# 只包含必需的模块
requirements = python3,kivy,requests,cryptography
```

2. **单架构构建**
```ini
# 只构建arm64（现代设备）
android.archs = arm64-v8a
```

3. **移除不必要文件**
```ini
# 排除测试文件
source.exclude_dirs = tests,docs,examples
source.exclude_exts = md,txt,rst
```

## 🎯 推荐流程

### 对于初学者（推荐）：
1. **使用GitHub Actions**
   - 零本地配置
   - 云端构建
   - 自动化流程

### 对于有经验用户：
1. **本地Buildozer**
   - 快速迭代
   - 本地调试
   - 完全控制

### 对于Docker用户：
1. **Docker构建**
   - 环境隔离
   - 可重现构建
   - 团队协作

## 🔍 故障排除

### 常见问题：

1. **Android SDK未找到**
```bash
# 让buildozer自动下载
buildozer android debug

# 或手动设置
set ANDROID_HOME=C:\Users\%USERNAME%\.buildozer\android\platform\android-sdk
```

2. **构建失败**
```bash
# 清理重建
buildozer android clean
buildozer android debug
```

3. **APK安装失败**
```bash
# 启用开发者选项
# 允许未知来源安装
adb install bin\accounting-1.0.0-debug.apk
```

## 💡 最终建议

**立即行动方案**：

1. **快速验证**：使用GitHub Actions
2. **本地开发**：安装Java JDK 8 + Buildozer
3. **持续集成**：设置自动化构建

**最少工具安装**：
- ✅ Python（已有）
- ✅ Java JDK 8（必需）
- ✅ Buildozer（pip安装）

**零工具方案**：
- ✅ GitHub Actions（推荐）
- ✅ 在线构建服务

现在您的ISS功能已经验证成功，可以选择任一方案开始APK构建！🚀
