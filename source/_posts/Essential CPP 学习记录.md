---
title: Essential CPP 学习记录
date: 2024/10/23
tags:
  - cpp
  - 计算机
categories:
  - cpp
description: 
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023201325.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023201325.png
poster:
  topic: 
  headline: Essential CPP 学习记录
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
> 本篇文章，仅为个人学习的记录。
# 1. C++ 基础编程

## 1.1 如何撰写 C++ 程序

由于之前已经学习过相关内容，就不再记录简单的知识点，在这里记录一下课后习题中几个有意思的点，并且是这解释一下。

先看一段简单的代码：

```C
#include <iostream>  
#include <string>  
  
using namespace std;  
  
int main() {  
    string name;  
    cout << "Enter your name: ";  
    cin >> name;  
    cout << "Hello, " << name << "!" << endl;  
    return 0;  
}
```

1. 将头文件 string 注释掉会发生什么？
2. 将 using namespace std; 注释掉呢？
3. 将 main 修改成 mymain 呢？

### 问题一

与预期不同，这样做并没有产生错误信息，而是正常编译通过，运行时也没有错误。但并不代表这就是正确的！！！

可能是以下几点导致的：
1. 间接包含，能在其他包含的头文件（如 `<iostream>`）中间接地包含了 `<string>`。不过标准库 iostream 并不包含 string，所以可以排除这一点
2. 编译器宽松设置：编译器可能在宽松的设置下忽略一些缺失的头文件声明，但这不是标准行为，可能会导致不可移植的代码。**所以，请不要这么干！！！**
 
### 问题二

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023203318.png)

如上图所示，产生了很多 undeclared identifier 的错误，想要在不使用命名空间的情况下解决这个问题，就要在使用标准库的名称前加上 `std::` 前缀。

想要解释这个问题，需要先理解什么是命名空间参考： [C++ 命名空间](https://www.runoob.com/cplusplus/cpp-namespaces.html)


### 问题三

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023203235.png)

简单解释一下：`main` 函数是程序的入口点，必须存在并且名称必须是 `main`。修改成其他名称后，程序仍然可以编译，但无法正常执行，因为没有定义入口点。

上面解释了为什么需要 main ，但是在执行 main 前，程序还做了许多工作，参考：[# CPP程序从诞生到死亡做了什么？](https://www.montylee.cn/2024/08/02/CPP%E7%A8%8B%E5%BA%8F%E4%BB%8E%E8%AF%9E%E7%94%9F%E5%88%B0%E6%AD%BB%E4%BA%A1%E9%83%BD%E5%81%9A%E4%BA%86%E4%BB%80%E4%B9%88%EF%BC%9F/)

## 1.2 对象的定义与初始化

### 初始化语法

为了解决 “=” 运算符无法赋多个初值的问题，引入了**构造函数语法**，如在标准库中的复数类，在初始化时就要写成`complex<double> purei(0, 7);` 表示 `0 + 7i`。


## 1.3 撰写表达式

## 1.4 条件语句与循环语句

## 1.5 如何运用 Array 和 vector

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023210656.png)
## 1.6 指针带来弹性

## 1.7 文件的读写

要进行文件的读写操作，首先得包含 fstream 头文件： `#include <fstream>`；
为了打开一个可供输出的文件，我们定义一个 ofstream 对象，并将文件名传入：

```C
// 1. 打开文件并清空
ofstream outfile("test.txt"); // 以输出模式开启文件

// 2. 打开文件以追加形式写入
ofstream outfile("test.txt", ios_base::app);

ifstream infile("test.txt"); // 以读取模式打开 infile
```

如果指定文件不存在，则创建文件并用于输出，如果存在则打开进行输出。


# 2. 面向过程的编程风格

## 2.1 如何编写函数

一个函数由四个部分组成：返回类型、函数名、函数体和参数列表。

## 2.2 调用函数

