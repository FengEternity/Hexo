---
# 基本信息
title: C++ 学习
date: 2024/05/09/15/44
tags: [cpp, 计算机]
categories: [cpp]
description: C++ 学习记录
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/cpp.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/cpp.png
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  C++ 学习 # 必选
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



# 学习记录

## CMake

学习文章：[CMake学习笔记（一）基本概念介绍、入门教程及CLion安装配置](https://juejin.cn/post/6844904015587704839) ~~（注：本内容仅供个人学习使用，请点击链接阅读原文）~~

### 相关概念

* **构建系统**：用来从源代码生成用户可以使用的**目标**的**自动化工具**，目标可以包括库、可执行文件、或者生成的脚本等等
* **构建（配置/项目）文件**：指导构建系统如何编译、链接生成可执行程序
* **CMake**：一个开源的跨平台构建系统，用来管理软件建置的程序

### CMake 相关知识

CLion中创建新项目后，初始结构如下，

![](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/16edf0e52ca40aae~tplv-t2oaga2asx-jj-mark-3024-0-0-0-q75.png)

* **cmake-build-debug** ：`CLion`调用`CMake`生成的默认**构建目录**。

* **CMakeLists.tx**t：`cmake`项目配置文件，准确点说是项目顶级目录的`cmake`配置文件，因为一个项目在多个目录下可以有多个`CMakeLists.txt`文件。文件内容示例如下，

  ![](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/16edf0e535537c3f~tplv-t2oaga2asx-jj-mark-3024-0-0-0-q75.png)

* **cmake_minimum_required(VERSION 3.15)** ：设置`cmake`的最低版本要求，如果`cmake`的运行版本低于最低要求版本，它将停止处理项目并报告错误。
* **project(CMakeLearnDemo)**：设置项目的名称，并将其值存储在`cmake`内置变量`PROJECT_NAME`中。当从顶级`CMakeLists.txt`调用时，还将其存储在内置变量`CMAKE_PROJECT_NAME`中。
* **set(CMAKE_CXX_STANDARD 17)**：设置`C++`标准的版本。
* **add_executable(CMakeLearnDemo main.cpp)**：添加一个**可执行文件**类型的**构建目标**到项目中。`CMakeLearnDemo`是文件名，后面是生成这个可执行文件所需要的源文件列表。



## 黑马B站教程

* [黑马程序员匠心之作|C++教程从0到1入门编程,学习编程不再难](https://www.bilibili.com/video/av41559729/?p=1&vd_source=f30eba35d0a8915376778596dfd73224)
* [黑马视频配套资料](https://github.com/Blitzer207/C-Resource)

![image-20240509175137661](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/cppheima.png)



# 时间线

{% timeline %}

<!-- node 2024 年 5 月 13 日 -->

面试通过，小声吐槽：实习待遇极差……

这几天将 C++ 基础语法过了一遍。

<!-- node 2024 年 5 月 9 日 -->

中海达面试结束，面试官说实习过程中主要是用 CPP 进行开发，于是决定利用这几天补习相关知识。

{% endtimeline %}

# 引用

* [这才是你最想要的 C++ 学习路线](https://www.zhihu.com/tardis/zm/art/435927070?source_id=1003)
* [C++那些事](https://github.com/Light-City/CPlusPlusThings?tab=readme-ov-file#c-那些事)
* [CMake学习笔记（一）基本概念介绍、入门教程及CLion安装配置](https://juejin.cn/post/6844904015587704839)