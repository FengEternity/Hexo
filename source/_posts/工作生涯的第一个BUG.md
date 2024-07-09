---
# 基本信息
title: 工作生涯修的第一个BUG
date: 2024/07/09
tags: [cpp, 计算机, debug]
categories: [debug, cpp]
description: 工作生涯修的第一个BUG
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  工作生涯修的第一个BUG # 必选
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

# 问题描述

![image-20240709191136256](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709191136256.png)



# 问题分析

## 初步分析

原因应该是分幅时，是先根据幅块大小，把hlz的文件建立出来了，如果某个幅块一个点都没有写，那么就只有一个头，是100M，修改方案为：如果一个幅块一个点都没有，那么删除这个hlz文件。

![image-20240709191318342](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709191318342.png)

# 问题解决

由于对项目不熟悉，所以解决起来还是比较困难的

1. 锁定问题出现的位置：经过对代码逻辑的梳理，大致确定了是在**文件删除**时出了问题

2. 由于我不确定下面这行代码的作用，所以就先没有注释掉

   ```c++
   writers[sheet_index]->remove();
   ```

   通过增加

   ```c++
   std::remove(sheet[sheet_index].path.c_str());
   ```

   成功解决BUG！

   ![image-20240709192042152](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709192042152.png)

   ![image-20240709192108926](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709192108926.png)


然而，事情真的就这么简单的解决了吗？当然不是！

我兴奋地 commit 我修改的代码，然而收到的回复是：**“你要弄懂为什么那段代码不起作用！”**

# 问题深入

继续Debug，打断点，调试，我还和朋友开玩笑说，“今天的工作量，打了5个断点。”

通过我不断的F11，最终大致明白了它的删除逻辑，不得不说，对比起来，上学时写的代码真的是玩具啊。

![image-20240709193251564](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709193251564.png)

这里的判断逻辑应该是有问题的，代码在 ``if(!creator)``判断为 ``true``，导致其直接返回，而没有进入``return creator->remove();``语句。

既然，代码没有进入``remove()``函数，那我就自己找找吧！我傻傻地点击右键“转到定义”，结果发现事情好像不太对，怎么在不断地调用类，这一刻我突然冒出一个念头，

>  “面向对象的设计固然好，理论上也增加了代码的可维护性，可是如我今天遇到的问题，本来直接执行一个文件删除语句就可以了，但是偏偏嵌套这么深，真的提高代码可维护性了吗？”

不过，千辛万苦之下，还是让我找到了，删除语句，可笑的是，

![image-20240709193916196](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709193916196.png)

这和我写的不是一样的吗？？？



# 遗留问题

![image-20240709193955633](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709193955633.png)

在单步调试的过程中，出现了这个错误，可是后来没有复现。
