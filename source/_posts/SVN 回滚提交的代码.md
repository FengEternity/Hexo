---
# 基本信息
title: SVN 回滚提交的代码
date: 2024/05/29/14/19
tags: [计算机, debug]
categories: [debug]
description: SVN 回滚提交的代码
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/SouthEast.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/SouthEast.png
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  SVN 回滚提交的代码 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: 
mathjax: 
# 可选
topic: 计算机 # 专栏 id
author: Montee
references:
comments: # 设置 false 禁止评论
indexing: # 设置 false 避免被搜索
breadcrumb: # 设置 false 隐藏面包屑导航
leftbar: 
rightbar:
h1: # 设置为 '' 隐藏标题
type: tech # tech/story
---



# 操作步骤

1. TortoiseSVN -> Show log.
2. 右键点击你想撤回的**提交**-> Revert changes from this revision.
3. 右键点击你想撤回**提交**的前一个**提交**-> Revert to this version.
4. 将你的**代码**修改正确之后-> 重新**SVN** Commit.



# 学习文档

没想好起什么名字，实际上是我在解决这个问题时，查找阅读的相关文章。

> * [SVN 回滚（撤回）提交的代码](https://blog.csdn.net/k358971707/article/details/78519179)