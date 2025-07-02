#!/bin/bash

echo "=== GitHub 分支清理脚本 ==="
echo

echo "当前分支状态:"
git branch -a
echo

echo "检查当前分支:"
git branch --show-current
echo

echo "准备删除远程 master 分支..."
echo "注意: 请先在 GitHub 网页上将默认分支改为 main"
echo

read -p "按 Enter 继续，或 Ctrl+C 取消..."

echo "删除远程 master 分支..."
if git push origin --delete master; then
    echo "✅ 成功删除远程 master 分支"
else
    echo "❌ 删除失败，请确保已在 GitHub 上更改默认分支"
    echo "请访问: https://github.com/mingus2021/mobile-accounting-app/settings/branches"
    exit 1
fi

echo
echo "清理本地远程引用..."
git remote prune origin

echo
echo "最终分支状态:"
git branch -a

echo
echo "✅ 分支清理完成！"
echo "现在只保留 main 分支作为唯一的工作分支。"
