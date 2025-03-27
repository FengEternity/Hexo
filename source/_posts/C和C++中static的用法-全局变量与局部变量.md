---
title: C和C++中static的用法-全局变量与局部变量
date: 2025/3/27
tags:
  - cpp
  - 基础知识
categories:
  - cpp
description: C和C++中static的用法-全局变量与局部变量
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/8d292a50b52ad3f0d1a2f4e673b0a7e7fa338c3f203df-aaDHPb_fw1200.jpeg
katex: true
mathjax: true
topic: 计算机
author: Montee
type: tech
---

> 文章转载自：https://www.cnblogs.com/33debug/p/7223869.html

在小米的面试环节被问了这个问题，面试官问我的是在C语言中作用，但是本人已经太久没有写过C语言，所以知识磕磕绊绊地回答出了C++中的作用。

# 1. 什么是 static

static 是C/C++中很常用的修饰符，他被用来控制变量的存储方式和可见性。

## 1.1 static 的引入

我们知道在函数内部定义的变量，当程序执行到它的定义处时，编译器为它在栈上分配空间，函数在栈上分配的空间在此函数执行完成结束时会被释放掉，这样就产生了一个问题：如果想将函数中此变量的值保存至下一次调用时，如何实现？最容易想到的办法是定义为全局变量，但定义全局变量有许多缺点，最明显的缺点是破坏了此变量的访问范围（使得在此函数中定义的变量，不只受此函数控制）。static 关键字则很好的解决了这个问题。

另外，在C++中，需要一个数据对象为整个类服务而非某个对象副，同时又力求不破坏类的封装性，即要求此成员隐藏在类的内部，对外不可见时，可将其定义为静态数据。

## 1.2 静态数据的存储
