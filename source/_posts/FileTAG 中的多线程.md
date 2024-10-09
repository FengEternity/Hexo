---
title: FileTAG 中的多线程
date: 2024/10/09
tags:
  - cpp
  - QT
categories:
  - C++
description: 
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
poster:
  topic: 
  headline: FileTAG 中的多线程
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: true
topic: 计算机
author: Montee
references: 
comments: 
indexing: 
breadcrumb: 
leftbar: 
rightbar: 
h1: 
type: tech
---
# 前言

之前问过“雪豹”，有什么推荐的 C++ 学习课程，他说没有，**都是东一点西一点，慢慢积累的** 。通过这次项目的开发，我还是深有感触的。

早在操作系统的课程中，就学习过 **进程、死锁、消息队列、调度算法** 这些内容，可是知道实际任务中，才能够真的理解这些概念。

本文结合 FileTAG 的开发过程，详细阐述本人的多线程学习路径以及相关知识点。

好了，正文开始。

# 1. 多线程初探：分离搜索线程与主界面UI线程

这个在之前的文章写过，这里就不做过多叙述，参见[多线程初探：在Qt中实现多线程文件搜索](https://www.montylee.cn/2024/07/18/%E5%A4%9A%E7%BA%BF%E7%A8%8B%E5%88%9D%E6%8E%A2/)


> 但是写文章埋的坑也是填上了。

在这一部分，主要涉及到两个线程：
1. **主线程（GUI线程）**：负责处理用户界面和用户交互；
2. **文件搜索线程（工作线程）**：负责执行耗时的文件搜索操作。

**通过线程分离的操作，很好的解决了文件搜索过程中，出现的UI界面卡顿问题。**

# 2. 数据竞争（Race Condition）

在多线程编程当中，不可避免的会涉及到数据竞争问题




