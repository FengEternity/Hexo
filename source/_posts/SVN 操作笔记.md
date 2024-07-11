---
# 基本信息
title: SVN 使用笔记
date: 2024/05/29
tags: [计算机, SVN]
categories: [版本控制工具]
description: SVN 使用笔记
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211518_nNfZE.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211518_nNfZE.gif
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  SVN 使用笔记 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: true
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

# 前言
此文档仅供个人在实际操作中记录使用，如需详细学习请至 **学习文档** 部分

# 回滚代码
1. TortoiseSVN -> Show log.
2. 右键点击你想撤回的**提交**-> Revert changes from this revision.
3. 右键点击你想撤回**提交**的前一个**提交**-> Revert to this version.
4. 将你的**代码**修改正确之后-> 重新**SVN** Commit.



# 解决冲突（svn conflict ）

更为详细的教程请参考：[解决冲突](https://tortoisesvn.net/docs/release/TortoiseSVN_zh_CN/tsvn-dug-conflicts.html)

## svn update ：
查看是否存在冲突（即两个人对同一个地方作出修改，导致从仓库拉取代码时，不一致产生冲突）

文件中冲突区域示例如下，

```bash
<<<<<<< filename
your changes
=======
code merged from repository
>>>>>>> revision
```

## svn conflict ：解决冲突

1. **理解冲突标记**：
    
    - `<<<<<<< filename`：这部分标记了你当前分支的内容（即“your changes”）。
    - `=======`：这部分是分隔符，分隔了冲突的两个版本。
    - `>>>>>>> revision`：这部分标记了你尝试合并进来的分支的内容（即“code merged from repository”）。
    
2. **分析冲突内容**：
    - 你的版本：`your changes`
    - 合并进来的版本：`code merged from repository`

3. **决定保留哪部分内容**：
    - 你需要决定保留哪部分内容，可以是你的更改、合并进来的更改，或者是两者的结合。

4. **编辑文件以解决冲突**：
    - 删除冲突标记，并保留你决定要的内容。例如：
        - 如果你决定保留你的更改，可以将代码修改为：

        ```plaintext
        your changes
        ```

        - 如果你决定保留合并进来的更改，可以将代码修改为：

        ```plaintext
        code merged from repository
        ```

        - 如果你决定结合两者的更改，可以将代码修改为：

        ```plaintext
        your changes
        code merged from repository
        ```

## 最后点击 resolve

# 学习文档

> * [SVN 回滚（撤回）提交的代码](https://blog.csdn.net/k358971707/article/details/78519179)
> * [SVN 菜鸟教程](https://www.runoob.com/svn/svn-tutorial.html)
>   * 具体介绍了 SVN 相关的知识，重点在于命令行相关的操作
>   * 缺少 TortoiseSVN 的详细使用教程
> * [TortoiseSVN 使用教程](https://www.cnblogs.com/DreamingFishZIHao/p/12982944.html)
> * [TortoiseSVN 使用教程2](https://tortoisesvn.net/docs/release/TortoiseSVN_zh_CN/tsvn-preface-readingguide.html)