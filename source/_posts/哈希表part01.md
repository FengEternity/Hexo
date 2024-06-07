---
# 基本信息
title: 哈希表part01
date: 2024/06/06
tags: [cpp, 计算机, leetcode, 秋招, 算法]
categories: [cpp, 题解]
description: 哈希表part01
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/nezuko-kamado-kimetsu-no-yaiba-hd-wallpaper-x-preview-27.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/nezuko-kamado-kimetsu-no-yaiba-hd-wallpaper-x-preview-27.jpg
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  哈希表part01 # 必选
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

# 哈希表理论基础

哈希表是根据关键码的值而直接进行访问的数据结构。**用来快速判断一个元素是否出现集合里**

![哈希表1](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210104234805168.png)

例如要查询一个名字是否在这所学校里。

要枚举的话时间复杂度是O(n)，但如果使用哈希表的话， 只需要O(1)就可以做到。

我们只需要初始化把这所学校里学生的名字都存在哈希表里，在查询的时候通过索引直接就可以知道这位同学在不在这所学校里了。

将学生姓名映射到哈希表上就涉及到了**hash function ，也就是哈希函数**。

## 哈希函数

![哈希表2](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/2021010423484818.png)



## 哈希碰撞

如图，小李和小王都映射到索引下标为1的位置，这一现象称为**哈希碰撞**。

![哈希表3](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/2021010423494884.png)

### 解决方法

1. 拉链法

   * 刚刚小李和小王在索引1的位置发生了冲突，发生冲突的元素都被存储在链表中。 这样我们就可以通过索引找到小李和小王了

   ![哈希表4](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210104235015226.png)

2. 线性探测法

   * 使用线性探测法，一定要保证tableSize大于dataSize。 我们需要依靠哈希表中的空位来解决碰撞问题。

     例如冲突的位置，放了小李，那么就向下找一个空位放置小王的信息。所以要求tableSize一定要大于dataSize ，要不然哈希表上就没有空置的位置来存放 冲突的数据了。如图所示

   ![哈希表5](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210104235109950.png)

