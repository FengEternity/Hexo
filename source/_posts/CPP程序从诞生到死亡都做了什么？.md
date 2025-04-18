---
title: CPP程序从诞生到死亡做了什么？
date: 2024/08/02
tags:
  - cpp
  - 计算机
categories: [技术学习]
description: CPP程序从诞生到运行都做了什么？
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
poster:
  headline: CPP程序从诞生到死亡都做了什么？
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: true
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
程序的执行可以分为多个阶段，每个阶段都有特定的任务和作用。下图是典型的程序执行阶段：
> 图中的顺序有问题，正确初始顺序是：预处理阶段->加载时阶段->运行时阶段->终止阶段

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240802095246.png)

下面将详细解释每个阶段具体做了什么处理。

# 编译阶段

## 预处理

- **功能**：处理所有的预处理指令，例如`#include`、`#define`、`#ifdef`等。
- **具体操作**：
    - 展开宏定义。
    - 处理文件包含（将`#include`的头文件内容插入到源文件中）。
    - 处理条件编译指令。
    - 移除注释。
- **生成结果**：生成一个纯C++代码文件（.i文件），这个文件不再包含任何预处理指令。
## 编译

- **功能**：将预处理后的C++代码转换成汇编代码。
- **具体操作**：
    - 词法分析：将代码转换成一个个的词法单元（tokens）。
    - 语法分析：将词法单元组织成语法树（AST）。
    - 语义分析：检查语法树的语义正确性，例如类型检查、变量作用域等。
    - 生成汇编代码：将语法树转换成汇编代码。
- **生成结果**：生成汇编代码文件（.s文件）。
## 汇编

- **功能**：将汇编代码转换成机器码（目标代码）。
- **具体操作**：
    - 汇编器（Assembler）将汇编代码逐行转换成机器指令，并生成目标文件。
- **生成结果**：生成目标文件（.o或.obj文件）。
## 链接

- **功能**：将一个或多个目标文件和库文件组合成一个可执行文件。
- **具体操作**：
    - 符号解析：确定所有函数和变量的地址。
    - 重定位：调整代码和数据地址以生成一个连续的地址空间。
    - 合并代码段和数据段：将不同模块的代码段和数据段合并。
    - 处理外部库：将使用到的外部库链接到最终的可执行文件中。
- **生成结果**：生成可执行文件（在Windows下通常是.exe文件，在Linux下通常是无扩展名的可执行文件）。

## 示例

下面是一个简单的C++源文件的编译过程示例：

```C
// example.cpp

#include <iostream>
#define PI 3.14

int main() {
    std::cout << "The value of PI is: " << PI << std::endl;
    return 0;
}

```

1. **预处理**：
    - 展开头文件`<iostream>`的内容。
    - 展开宏`PI`。
    - 移除注释。
    - 生成预处理后的文件（example.i）。
2. **编译**：
    - 进行词法分析、语法分析、语义分析。
    - 生成汇编代码（example.s）。
3. **汇编**：
    - 将汇编代码转换成目标文件（example.o）。
4. **链接**：
    - 链接器将example.o和标准库（如libc++）链接在一起。
    - 生成最终的可执行文件（example.exe或a.out）。

通过这些阶段，C++源代码最终转换为**可执行的机器码**。


# 加载阶段

**功能**：将可执行文件从磁盘加载到内存，准备程序的运行环境。

## 内存分配

**功能**：操作系统分配内存给程序，包括代码段、数据段、堆和栈。

- 代码段（Code Segment）：存储程序的机器指令。
- 数据段（Data Segment）：存储全局变量和静态变量。分为已初始化数据段（BSS段）和未初始化数据段。
- 堆（Heap）：用于动态内存分配。
- 栈（Stack）：用于函数调用、局部变量和控制信息。

## 解析动态链接库

**功能**：
- 如果程序依赖于动态链接库（如Windows上的`.dll`文件或Linux上的`.so`文件），操作系统会找到这些库并将其加载到内存中。
- 动态链接器（Linker/Loader）负责解析和链接这些库，确保程序能够调用库中的函数和使用库中的变量。

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240802103210.png)

图中这个经典的问题就是发生在这个阶段，也是初学者一头雾水的问题，图上这种问题一般都是以下几个原因：

1. **缺失的动态链接库**：`mfc100u.dll`文件未安装或未找到。
2. **路径问题**：程序无法定位到DLL文件的位置。
3. **版本不匹配**：DLL的版本不兼容。

解决思路，首先查看自己的电脑是否存在 mfc100u.dll 文件，不存在需要手动下载并且存放到链接库的目录下；如果存在但是路径不对，那直接复制粘贴过去就可以了。

## 重定位

如果在这个阶段出问题，大概率

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240802113625.png)

- 调整内存中的地址，使得程序可以正确引用代码和数据。
- 将相对地址转换为绝对地址，确保程序在内存中的各个部分能够正确地相互引用。

# 启动阶段

**功能**：初始化程序的运行环境，包括初始化全局和静态变量、执行构造函数等。

## 运行时初始化

- 初始化全局变量和静态变量。
- 执行全局和静态对象的构造函数。
- 初始化未初始化数据段（BSS段）中的变量，将其值设为零。

> **与加载阶段分配内存的区别与联系（个人理解）**：
> 
> 如在代码中有下面这行代码 `int a;`
> 那么在分配内存时，是操作系统开辟了 4 个字节的内存空间，但是里面没有具体的值；到了运行初始化阶段，会给它赋初值，由于这里代码中没有明确指出初值是什么，默认设置为0。
## 库初始化

- 初始化C++标准库和其他依赖的库。
- 运行库的初始化代码，确保库中的全局状态正确设置。

## 设置栈

- 为主线程分配栈空间。
    - 设置栈指针（Stack Pointer），准备函数调用。

## 调用入口函数

- 准备调用`main`函数。
    - 一些系统和库会在调用`main`函数之前执行一些初始化代码，例如在C++中，可能会调用`__libc_start_main`函数来执行这些任务。

# 执行（运行）阶段

**功能**：执行程序的主逻辑，进行函数调用、内存管理和异常处理等。

**具体操作**：

1. **调用`main`函数**：
    
    - 从`main`函数开始执行程序的主逻辑。
    - `main`函数是程序的入口点，通常由系统调用来启动。
2. **函数调用和返回**：
    
    - 根据程序的逻辑进行函数调用和返回。
    - 栈用于管理函数调用和返回地址，局部变量在栈上分配。
3. **内存管理**：
    
    - 根据需要分配和释放内存，例如通过`new`和`delete`操作符。
    - 动态内存分配在堆上进行，程序需要负责管理这些内存，以避免内存泄漏和悬空指针。
4. **异常处理**：
    
    - 处理C++异常（如`try`、`catch`块）。
    - 确保程序能够捕获和处理运行时错误，避免程序崩溃。

**结果**：程序按照编写的逻辑执行，直到程序结束或遇到不可恢复的错误。

# 终止阶段

**功能**：清理和释放资源，确保程序正常退出并返回操作系统。

**具体操作**：

1. **调用析构函数**：
    
    - 调用所有全局和静态对象的析构函数。
    - 释放这些对象占用的资源，确保清理工作完成。
2. **释放内存**：
    
    - 释放程序分配的所有内存，包括堆和栈。
    - 确保动态分配的内存（通过`new`分配的内存）被正确释放。
3. **关闭文件和资源**：
    
    - 关闭程序打开的所有文件和其他资源（如网络连接、设备句柄等）。
    - 确保所有资源被正确释放，避免资源泄漏。
4. **返回退出状态**：
    
    - 返回`main`函数的返回值或调用`exit`函数的参数作为程序的退出状态。
    - 通知操作系统程序的退出状态，以便操作系统可以进行相应的处理。

**结果**：程序清理完毕，返回操作系统。