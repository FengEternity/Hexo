---
# 基本信息
title: 解决 Qt 应用程序中的 EXC_BAD_ACCESS 异常：以删除中央窗口部件为例
date: 2024/07/17
tags: [cpp, 计算机, debug]
categories: [C++]
description: 解决 Qt 应用程序中的 EXC_BAD_ACCESS 异常：以删除中央窗口部件为例
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  解决 Qt 应用程序中的 EXC_BAD_ACCESS 异常：以删除中央窗口部件为例 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: true
mathjax: 
# 可选
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

在开发 C++ 应用程序时，由于指针这一利器的使用，内存管理问题是常见的挑战之一。在开发  FileTag 时，遇到了一个 `EXC_BAD_ACCESS` 异常。这个异常通常是由于访问了无效的内存地址，具体表现为试图访问已经被释放的内存或空指针。

本文将分享我如何分析和解决这一问题，并结合指针和堆栈的相关知识，帮助大家更好地理解内存管理。

# 问题描述

在我的 Qt 应用程序中，有一个槽函数 `onFileSearchClicked`，用于在用户点击按钮时更新主窗口的中央部件。代码如下：

```c++
void MainWindow::onFileSearchClicked() {
    // 清空现有的中央窗口部件
    if (centralWidget) {
        delete centralWidget;
        setCentralWidget(nullptr);
    }

    // 创建新的 FileSearch 并设置为中央窗口部件
    FileSearch *fileSearch = new FileSearch(this);
    setCentralWidget(fileSearch);
}

```
![image-20240717113114410](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240717113114410.png)

![image-20240717113132255](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240717113132255.png)



如上图所示，程序初始界面如图一，在第一次点击文件下的搜索按钮时，功能正常。但在第二次点击时，程序崩溃并抛出 `EXC_BAD_ACCESS` 异常。

# 异常分析

### 指针和堆栈的相关知识

在深入分析异常之前，我们需要了解一些关于指针和堆的基本知识。

1. **指针**：
   - 指针是一个变量，它存储的是另一个变量的内存地址。
   - 在 C++ 中，指针的使用需要非常小心，特别是在涉及动态内存分配和释放时。
2. **堆**：
   - 堆是用于动态内存分配的区域，程序可以在运行时向堆申请内存。
   - 使用 `new` 操作符分配的内存位于堆上，需要使用 `delete` 操作符**手动释放**。



下面具体分析一下所遇到的问题。

从调试信息中可以看到，异常类型是 `EXC_BAD_ACCESS`，地址为 `0x80006000036109a0`。这意味着程序试图访问一个无效的内存地址。以下是调试信息截图：

![image-20240717113512751](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240717113512751.png)

从代码断掉的位置来看，其实问题已经很明显了，在第二次触发这个函数时，再一次对 centralWidget 进行 delete 操作，而这是 centralWidget 已经是一个被删除的对象了。![image-20240717115346572](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240717115346572.png)

## 调试方法

1. **检查调用栈**：
   - 查看调用栈可以帮助你确定异常发生时的调用路径。
   - 确定是哪一行代码引发了异常。
2. **验证指针有效性**：
   - 在 `delete centralWidget;` 之前添加一些调试输出，检查 `centralWidget` 是否为有效指针。
   - 确保在删除指针后将其设置为 `nullptr`，避免重复删除。

## 分析步骤

1. **异常信息**：
   - 异常类型：`EXC_BAD_ACCESS`
   - 地址：`0x80006000036109a0`
   - 这表明程序试图访问一个无效的内存地址。
2. **寄存器信息**：
   - 从寄存器信息中可以看到多个寄存器的值，但这些值本身并不能直接告诉我们问题的根源。
3. **`this` 指针**：
   - `this` 指针的值是 `0x16fbdb158`，这表示当前对象的内存地址。
   - `QMainWindow` 是一个有效的对象，但问题可能出在它的成员或方法调用上。

进一步分析`线程和变量`，查找引发异常的位置，如下图

![image-20240717135512595](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240717135512595.png)

从图中的调试信息可以看出，程序在访问 `centralWidget` 时发生了内存读取失败的情况。这些信息表明程序试图访问已经被释放的内存或无效的内存地址，导致 `EXC_BAD_ACCESS` 异常。以下是对图中各个部分的详细解释：

#### 图中信息的详细解释

1. **`centralWidget = {QWidget \*} 0x600000ee0930`**:
   - 这是一个指向 `QWidget` 对象的指针，内存地址为 `0x600000ee0930`。
   - 从这里可以看出，`centralWidget` 变量本身是有效的指针。
2. **`QObject = {QObject}`**:
   - `QWidget` 继承自 `QObject`，因此包含 `QObject` 类的成员。
3. **`d_ptr = {QScopedPointer<QObjectData>}`**:
   - `d_ptr` 是一个 `QScopedPointer`，用于管理 `QObjectData` 的生命周期。
   - `QScopedPointer` 是一种智能指针，负责自动管理对象的内存，当指针超出作用域时自动删除对象。
4. **`d = {QObjectData \*} 0x155`**:
   - `d` 是一个指向 `QObjectData` 的指针，内存地址为 `0x155`。
   - 这个地址显然是无效的，因为它太小，通常指针地址是一个较大的数值。
5. **`q_ptr = read memory from 0x15d failed (0 of 8 bytes read)`**:
   - 读取 `q_ptr` 成员时失败，无法从地址 `0x15d` 读取 8 个字节。
   - 这表明 `q_ptr` 所在的内存地址无效或已被释放。
6. **`parent = read memory from 0x165 failed (0 of 8 bytes read)`**:
   - 读取 `parent` 成员时失败，无法从地址 `0x165` 读取 8 个字节。
   - 这表明 `parent` 所在的内存地址无效或已被释放。
7. **`children = {QObjectList}`**:
   - `children` 是一个 `QObjectList` 对象，用于存储子对象列表。
8. **其他读取失败的成员**:
   - `isWidget`, `blockSig`, `wasDeleted`, `isDeletingChildren`, `sendChildEvents`, `receiveChildEvents`, `isWindow`, `deleteLaterCalled`, `isQuickItem`, `willBeWidget`, `wasWidget`, `receiveParentEvents`, `unused` 等成员在尝试读取时均失败。
   - 这些成员的读取失败表明 `QObjectData` 对象的内存已经无效，可能是由于对象已经被删除或指针指向了错误的内存地址。

# 问题解决

经过分析，我决定使用 `takeCentralWidget` 方法来取回当前的中央部件，并在需要时删除它。以下是修正后的代码：

```c++
void MainWindow::onFileSearchClicked() {
    // 取回现有的中央窗口部件
    QWidget *currentCentralWidget = takeCentralWidget();
    if (currentCentralWidget) {
        delete currentCentralWidget;
    }

    // 创建新的 FileSearch 并设置为中央窗口部件
    FileSearch *fileSearch = new FileSearch(this);
    setCentralWidget(fileSearch);
}

```

# 总结

本文详细了在开发 C++ 应用程序时常见的内存管理挑战，特别是指针使用中可能导致的 `EXC_BAD_ACCESS` 异常。主要是希望自己之后遇到类似问题时，能看懂堆栈的相关问题，以及知道如何分析解决问题。
