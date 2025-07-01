# 🔧 依赖安装问题快速修复

## 🎯 问题分析

您遇到的问题：
1. **Python版本冲突**：requirements.txt中指定了python3==3.9，但您的系统是Python 3.11.9
2. **SSL证书问题**：网络连接到PyPI时出现SSL错误

## 🚀 快速解决方案

### 方案1: 最小化测试（推荐）

**立即测试ISS功能，无需安装Kivy：**

```bash
# 1. 安装最基础的依赖
pip install requests cryptography --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# 2. 运行ISS测试
python test-iss-only.py
```

**这个测试版本可以：**
- ✅ 测试ISS上传下载功能
- ✅ 验证密钥配置
- ✅ 支持贴文配置解析
- ✅ 无需Kivy依赖

### 方案2: 分步安装依赖

```bash
# 1. 运行依赖安装脚本
install-deps.bat

# 2. 如果成功，运行完整应用
simple-start.bat
```

### 方案3: 手动安装

```bash
# 1. 升级pip
python -m pip install --upgrade pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# 2. 逐个安装依赖
pip install requests --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
pip install cryptography --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
pip install kivy --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
pip install kivymd --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

# 3. 运行应用
python main.py
```

## 📋 可用的启动脚本

| 脚本名称 | 功能 | 推荐度 |
|----------|------|--------|
| `test-iss-only.py` | 最小化ISS测试 | ⭐⭐⭐⭐⭐ |
| `install-deps.bat` | 安装依赖 | ⭐⭐⭐⭐ |
| `simple-start.bat` | 简单启动（不安装依赖） | ⭐⭐⭐ |
| `quick-start.bat` | 完整启动（已修复） | ⭐⭐⭐ |

## 🎯 立即行动建议

### 第一步：测试核心功能
```bash
# 运行最小化测试
python test-iss-only.py
```

这将验证：
- ✅ Python环境正常
- ✅ ISS连接正常
- ✅ 密钥配置正确
- ✅ 贴文配置解析

### 第二步：安装完整依赖（可选）
```bash
# 如果第一步成功，可以安装完整依赖
install-deps.bat
```

### 第三步：运行完整应用
```bash
# 依赖安装成功后
simple-start.bat
```

## 🔍 故障排除

### SSL证书问题
```bash
# 方法1: 使用信任主机
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package>

# 方法2: 升级证书
pip install --upgrade certifi

# 方法3: 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ <package>
```

### Python版本问题
- ✅ **您的Python 3.11.9完全兼容**
- ✅ **已修复requirements.txt**
- ✅ **移除了版本限制**

### 网络问题
```bash
# 检查网络连接
ping pypi.org

# 使用代理（如果需要）
pip install --proxy http://proxy:port <package>
```

## 💡 推荐流程

1. **立即测试**：运行 `python test-iss-only.py`
2. **验证功能**：确认ISS上传下载正常
3. **配置测试**：测试贴文配置解析
4. **安装依赖**：运行 `install-deps.bat`
5. **完整应用**：运行 `simple-start.bat`

## 🎉 成功标志

看到以下信息表示成功：
```
✅ 核心依赖检查通过
✅ 私钥加载成功
🔐 签名生成成功
🔑 认证头生成成功
📡 开始上传
📈 响应状态: 200
✅ 上传成功!
🎉 ISS测试成功!
```

**现在就开始测试吧！运行：`python test-iss-only.py`** 🚀
