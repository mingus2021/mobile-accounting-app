# GitHub 分支清理指南

## 🎯 目标
删除多余的 `master` 分支，只保留 `main` 分支作为唯一的工作分支。

## 📊 当前状态
- ✅ **main** - 工作分支 (5个提交，包含所有Android构建修复)
- ❌ **master** - 旧分支 (2个提交，只有初始代码)

## 🔧 操作步骤

### 步骤 1: 更改GitHub默认分支
1. 访问: https://github.com/mingus2021/mobile-accounting-app/settings/branches
2. 在 "Default branch" 部分，点击切换按钮
3. 选择 `main` 作为新的默认分支
4. 点击 "Update" 确认更改

### 步骤 2: 删除master分支
在GitHub网页上：
1. 访问: https://github.com/mingus2021/mobile-accounting-app/branches
2. 找到 `master` 分支
3. 点击删除按钮（垃圾桶图标）
4. 确认删除

### 步骤 3: 清理本地引用
```bash
# 清理本地远程引用
git remote prune origin

# 检查最终状态
git branch -a
```

## 🚀 自动化脚本
如果您更喜欢使用脚本：

### Windows:
```cmd
cleanup-branches.bat
```

### Linux/Mac:
```bash
./cleanup-branches.sh
```

## ✅ 预期结果
完成后，您应该只看到：
```
* main
  remotes/origin/main
```

## 📋 验证
运行以下命令验证清理成功：
```bash
git branch -a
git log --oneline -3
```

应该显示：
- 只有 `main` 分支
- 最新提交包含Android构建修复

## 🔍 为什么要清理分支？
1. **避免混淆** - 只有一个主分支，避免在错误分支上工作
2. **简化工作流** - 所有开发都在 `main` 分支上进行
3. **保持整洁** - 删除过时的分支，保持仓库整洁
4. **符合现代实践** - `main` 是现代Git仓库的标准主分支名称

## 🎉 完成后
- ✅ 只保留 `main` 分支
- ✅ 所有Android构建修复都在 `main` 分支上
- ✅ GitHub Actions workflow 正常工作
- ✅ 可以正常提交和推送代码
