---
# 基本信息
title: VMware Fusion 踩坑笔记（M1 Pro）
date: 2024/06/17
tags: [计算机, debug]
categories: [虚拟机]
description: VMware Fusion 踩坑笔记（M1 Pro）
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/006BFMdqly1gfcskjuy1ij31kw13gjz0.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/006BFMdqly1gfcskjuy1ij31kw13gjz0.jpg
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  VS 去除程序运行时的控制台 # 必选
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

> 一个好用的 Mac 软件下载库：https://www.macat.vip

> 2024/7/2，放弃VM了，改用Parallels Desktop

# 1. 在设置里给虚拟机分配了内存，但是虚拟机运行起来依然没有

先简单介绍一下我的环境：

1. 电脑：Mac M1 Pro
2. 虚拟机软件：Vmware Fusion
3. 虚拟系统：Windows 11

## 正确步骤

1. 第一步：虚拟机扩容

   在设置里修改一下就好了

2. 调整系统内的磁盘分区

   1. 打开 “磁盘管理”，找不到的建议直接在Windows的搜索框里搜索![磁盘管理器.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/71537be41e173309a801f9a59da0f0c7.png)
   2. 选中左下角未分配的磁盘空间，新建一个盘就OK了