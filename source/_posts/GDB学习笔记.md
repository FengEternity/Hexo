---
title: GDB 学习笔记
date: 2025/2/6
tags:
  - cpp
  - 计算机
  - debug
categories:
  - debug
  - cpp
description: GDB学习笔记
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/DSC01346.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/DSC01346.jpg
poster:
  topic: 
  headline: GDB 学习笔记
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: 
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

* 官方文档：https://sourceware.org/gdb/


# 1. 什么是 GDB

主要有四个方面的功能：
* 启动程序，可以按照自定义的要求随心所欲的运行程序
* 打断点，断点可以是表达式
* 当程序被停住时，可以检查此时程序所发生的事
* 可以改变程序，将一个 BUG 产生的影响修正从而测试其它 BUG

