#!/usr/bin/env python3
"""
APK构建脚本 - 最简单的方式
适用于Windows 10，避免批处理文件编码问题
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ 命令失败: {cmd}")
            print(f"错误: {result.stderr}")
            return False
        return result
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def check_python():
    """检查Python环境"""
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        print(f"✅ Python环境: {result.stdout.strip()}")
        return True
    except:
        print("❌ Python环境检查失败")
        return False

def check_java():
    """检查Java环境"""
    result = run_command("java -version", check=False)
    if result and result.returncode == 0:
        print("✅ Java环境检查通过")
        return True
    else:
        print("⚠️ Java未找到")
        return False

def install_buildozer():
    """安装buildozer"""
    print("📦 检查buildozer...")
    result = run_command("python -c \"import buildozer\"", check=False)
    if result and result.returncode == 0:
        print("✅ Buildozer已安装")
        return True
    
    print("📦 安装buildozer...")
    result = run_command("pip install buildozer cython")
    if result:
        print("✅ Buildozer安装成功")
        return True
    else:
        print("❌ Buildozer安装失败")
        return False

def create_project_structure():
    """创建项目结构"""
    print("📁 创建项目结构...")
    
    directories = [
        "app", "app/core", "app/ui", "app/data", 
        "assets", "assets/icons", "data"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # 创建__init__.py文件
    init_files = [
        "app/__init__.py", "app/core/__init__.py", 
        "app/ui/__init__.py", "app/data/__init__.py"
    ]
    
    for init_file in init_files:
        Path(init_file).touch()
    
    print("✅ 项目结构创建完成")

def setup_buildozer_config():
    """设置buildozer配置"""
    if not Path("buildozer.spec").exists():
        if Path("buildozer-minimal.spec").exists():
            shutil.copy("buildozer-minimal.spec", "buildozer.spec")
            print("✅ 使用优化的buildozer配置")
        else:
            print("📝 初始化buildozer配置...")
            result = run_command("buildozer init")
            if result:
                print("✅ Buildozer配置初始化完成")
            else:
                print("❌ Buildozer配置初始化失败")
                return False
    else:
        print("✅ Buildozer配置已存在")
    
    return True

def build_apk(build_type="debug"):
    """构建APK"""
    print(f"🔨 开始构建{build_type} APK...")
    
    if build_type == "clean":
        print("🧹 清理构建缓存...")
        run_command("buildozer android clean")
        build_type = "debug"
    
    result = run_command(f"buildozer android {build_type}")
    
    if result:
        print("🎉 APK构建成功!")
        
        # 检查生成的APK文件
        bin_dir = Path("bin")
        if bin_dir.exists():
            apk_files = list(bin_dir.glob("*.apk"))
            if apk_files:
                print("\n📱 生成的APK文件:")
                for apk in apk_files:
                    print(f"  📄 {apk.name}")
                
                print("\n📲 安装方法:")
                print("1. 在Android设备上启用开发者选项")
                print("2. 启用USB调试")
                print("3. 连接设备并运行:")
                print(f"   adb install {apk_files[0]}")
                print("\n或者将APK文件复制到设备上手动安装")
            else:
                print("⚠️ 未找到APK文件")
        
        return True
    else:
        print("❌ APK构建失败")
        print("\n🔧 常见解决方案:")
        print("1. 确保网络连接稳定（首次构建会下载Android SDK）")
        print("2. 尝试清理构建: python build_apk.py clean")
        print("3. 检查buildozer.spec配置")
        print("4. 使用GitHub Actions云端构建")
        return False

def setup_github_actions():
    """设置GitHub Actions"""
    print("☁️ 设置GitHub Actions云端构建...")
    
    # 创建目录
    github_dir = Path(".github/workflows")
    github_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建workflow文件
    workflow_content = """name: Build Android APK

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
"""
    
    workflow_file = github_dir / "build-apk.yml"
    workflow_file.write_text(workflow_content, encoding='utf-8')
    
    print("✅ GitHub Actions配置创建完成")
    print("\n📤 后续步骤:")
    print("1. 创建GitHub仓库")
    print("2. 上传代码:")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial commit'")
    print("   git remote add origin https://github.com/yourusername/repo.git")
    print("   git push -u origin main")
    print("\n3. APK将在GitHub Actions中自动构建")
    print("4. 在Actions页面下载构建的APK")

def main():
    """主函数"""
    print("=" * 60)
    print("🐍 Python移动记账应用 - APK构建器")
    print("=" * 60)
    print()
    
    # 检查Python环境
    if not check_python():
        input("按回车键退出...")
        return
    
    # 检查Java环境
    has_java = check_java()
    
    print()
    
    if not has_java:
        print("选择构建方式:")
        print("1. 安装Java JDK 8进行本地构建")
        print("2. 使用GitHub Actions云端构建")
        print()
        
        choice = input("请选择 (1-2): ").strip()
        
        if choice == "1":
            print("\n📥 请下载并安装Java JDK 8:")
            print("https://adoptium.net/temurin/releases/?version=8")
            print("\n安装后请:")
            print("1. 将Java添加到PATH环境变量")
            print("2. 设置JAVA_HOME环境变量")
            print("3. 重新运行此脚本")
            input("\n按回车键退出...")
            return
        
        elif choice == "2":
            setup_github_actions()
            input("\n按回车键退出...")
            return
        
        else:
            print("❌ 无效选择")
            input("按回车键退出...")
            return
    
    # 本地构建流程
    print("🔨 开始本地构建流程...")
    print()
    
    # 安装buildozer
    if not install_buildozer():
        input("按回车键退出...")
        return
    
    # 创建项目结构
    create_project_structure()
    
    # 设置buildozer配置
    if not setup_buildozer_config():
        input("按回车键退出...")
        return
    
    print()
    print("选择构建类型:")
    print("1. Debug APK (快速，用于测试)")
    print("2. Release APK (优化，用于发布)")
    print("3. Clean build (清理缓存重新构建)")
    print()
    
    build_choice = input("请选择 (1-3): ").strip()
    
    build_types = {"1": "debug", "2": "release", "3": "clean"}
    build_type = build_types.get(build_choice, "debug")
    
    print()
    
    # 构建APK
    success = build_apk(build_type)
    
    print()
    print("=" * 60)
    if success:
        print("🎉 构建完成!")
    else:
        print("❌ 构建失败")
        print("\n💡 建议使用GitHub Actions进行云端构建")
    print("=" * 60)
    
    input("\n按回车键退出...")

if __name__ == "__main__":
    main()
