---
# 基本信息
title: Git 提交规范/提交流程
date: 2024/06/25
tags: [计算机, git]
categories: [技术学习]
description: 
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
poster:  # 海报（可选，全图封面卡片）
  headline:  Git 提交规范/提交流程 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: true
mathjax: 
# 可选
references:
comments: # 设置 false 禁止评论
indexing: # 设置 false 避免被搜索
breadcrumb: # 设置 false 隐藏面包屑导航
leftbar: 
rightbar:
h1: # 设置为 '' 隐藏标题
type: story # tech/story
---

# 代码提交规范
## 1. 提交信息格式
每次提交的信息应包括三个部分：**标题、正文和脚注。**

### 1.1 标题（Title）
- **简洁明了**：标题应简明扼要地描述提交的内容。
- **长度限制**：标题应控制在50个字符以内。
- **首字母大写**：标题的首字母应大写。
- **动词开头**：使用祈使动词，例如“新增”、“修复”、“更新”等。
- **不要以句号结尾**：标题不应以句号结尾。

**示例**：
```
新增用户认证模块
修复数据处理函数中的错误
更新README中的安装说明
```

### 1.2 正文（Body）
- **详细描述**：正文应详细描述提交的目的、实现方式和影响。
- **每行72个字符**：每行字符数应控制在72个字符以内。
- **解释动机**：说明为什么需要进行这次提交。
- **列出变更**：详细列出具体的变更内容。

**示例**：
```
新增用户认证模块

此次提交引入了一个新的用户认证模块。
该模块包括用户登录、注册和密码管理功能。
它与现有的用户数据库集成，并提供了安全的密码哈希。

变更内容：
- 新增认证功能
- 更新用户模型
- 为认证功能新增单元测试
```

### 1.3 脚注（Footer）
- **引用问题**：如果提交是为了修复某个问题或添加某个功能，可以在脚注中引用相关的issue或任务编号。
- **破坏性变更**：如果提交包含破坏性变更，需要在脚注中注明。

**示例**：
```
修复 #123
BREAKING CHANGE: 修改了用户登录API端点
```

## 2. 提交频率
- **小步提交**：尽量保持每次提交的变更小而清晰，每次提交应完成一个独立的功能或修复一个问题。
- **频繁提交**：频繁提交有助于追踪问题和回滚代码。

## 3. 分支命名
- **功能分支**：`feature/description`，例如`feature/user-authentication`
- **修复分支**：`fix/description`，例如`fix/login-bug`
- **发布分支**：`release/version`，例如`release/1.0.0`
- **热修复分支**：`hotfix/description`，例如`hotfix/security-patch`

## 4. 合并策略
- **使用Pull Request（PR）**：所有变更应通过PR进行代码审查后合并。
- **保持历史清晰**：避免使用`--squash`或`--rebase`强制合并，以保持提交历史清晰。

## 5. 代码审查
- **审查标准**：每次PR至少需要一名同事审查并通过。
- **自动化检查**：使用CI工具进行自动化测试和代码质量检查。

## 6. 其他建议
- **保持代码风格一致**：使用代码格式化工具和linting工具。
- **编写单元测试**：为每次提交的功能或修复编写相应的单元测试。



# 代码提交流程
使用Git进行代码提交的步骤如下：

## 1. 初始化仓库（仅需一次）
如果这是一个新的项目，你需要先初始化一个Git仓库。

```bash
git init
```

## 2. 配置用户信息（仅需一次）
设置你的用户名和电子邮件，这些信息会记录在提交历史中。

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 3. 检查当前状态
在每次提交之前，检查当前工作目录的状态，了解哪些文件被修改、添加或删除。

```bash
git status
```

## 4. 添加文件到暂存区
将你想要提交的文件添加到暂存区。你可以添加单个文件、多个文件或所有文件。

添加单个文件：
```bash
git add filename
```

添加所有文件：
```bash
git add .
```

## 5. 提交更改
使用规范的提交信息提交更改。提交信息应包括标题和可选的正文和脚注。

```bash
git commit -m "提交标题" -m "提交正文" -m "脚注"
```

例如：
```bash
git commit -m "新增用户认证模块" -m "此次提交引入了一个新的用户认证模块。该模块包括用户登录、注册和密码管理功能。" -m "修复 #123"
```

## 6. 推送到远程仓库
将本地的提交推送到远程仓库。第一次推送时可能需要指定远程分支。

```bash
git push origin branch-name
```

例如，推送到`main`分支：
```bash
git push origin main
```

## 7. 创建和切换分支（可选）
在进行新功能开发或修复bug时，建议创建新的分支。

创建新分支并切换到该分支：
```bash
git checkout -b new-branch-name
```

切换到已有分支：
```bash
git checkout branch-name
```

## 8. 合并分支（可选）
在完成新功能或修复后，将分支合并到主分支。

切换到主分支：
```bash
git checkout main
```

合并分支：
```bash
git merge new-branch-name
```

## 9. 解决冲突（如果有）
在合并过程中，如果存在冲突，Git会提示你解决冲突。

查看冲突文件：
```bash
git status
```

手动编辑冲突文件，解决冲突后将文件添加到暂存区：
```bash
git add conflict-file
```

提交合并后的更改：
```bash
git commit -m "解决合并冲突"
```

## 10. 清理分支（可选）
在合并并推送分支后，可以删除本地和远程的临时分支。

删除本地分支：
```bash
git branch -d branch-name
```

删除远程分支：
```bash
git push origin --delete branch-name
```

