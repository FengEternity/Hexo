---
title: Effective CPP 学习记录
date: 2024/10/23
tags:
  - cpp
  - 计算机
categories: [技术学习]
description: 
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023160351.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023160351.png
poster:
  headline: Effective CPP 学习记录
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: 
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

> 书名为《Effective C++》， 博客地址无法解析++，故命名为CPP 

# 第一章 让自己习惯C++

## 1. 视  C++为一个语言联邦

> View C++ as a federation of languanges.

今天的C++是一门多范式编程语言，同时支持过程式、面向对象、函数式、泛型和元编程特性。这种能力和灵活性使C++成为无可比拟的工具，但也会引起一些混乱。

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023161806.png)

**把 C++ 看作由众多次语言“联邦”而来**

 1. C++ 的C语言部分
 2. C++ 的面向对象部分
 3. C++ 的模版部分
 4. C++ 的 STL 部分

## 2. 尽量使用 const enum inline 替换 # define

> Prefer consts, enums, and inlines to # defines
> 优先选择编译器替换预处理器

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023163344.png)


解决的方法是使用下面的代码：
```C
const double AspectRatio = 1.653; // 全大写通常用于宏，因此需要修改命名方式
```

存在两种特殊情况：定义常量指针、class 专属常量
### 定义常量指针

由于常量定义式通常被放在头文件中，因此有必要将指针声明为const。

```C
// #define AUTHORNAME "Scott Meyers"
// const char *const authorName "Scott Meyers；
const std::string authorName ("Scott Meyers"); // 如果是字符串，可以直接写成这样
```

上述代码语句 2 中，
1. **`const char *`**：指向字符的指针，指针指向的内容是常量，因此不能通过指针修改字符串内容。
2. **`const`（第二个）**：修饰指针本身，表示指针 `authorName` 不能指向其他地址。

### class 专属常量

> 这一部分没怎么看懂 

为了使常量的作用域限制在 class 中，必须让他成为 class 的一个成员；同时为了确保此常量至多只有一份实体，必须定义为 static 成员，如下面的代码：

```C
class GamePlayer {
private:
	// #define NunTurns 5 // 这样写无法限制作用域
	satic const int NumTurns = 5; 常量声明式
	int scores[NumTurns];
}
```

> C++中常量式与定义式的区别:
> 1. 常量式是指在编译时可以确定其值的表达式，值在程序运行期间不会改变，可以用于初始化常量、数组大小、模板参数等。 
> 2. 定义式是指声明并分配存储空间的语句。定义式不仅声明了变量或函数的类型，还为它们分配了存储空间（对于变量）或提供了函数的实现（对于函数）。

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241023172043.png)


通常，C++要求为所使用的任何东西提供定义，但类专用的静态整数类型（例如integer、char、
bool）常量是个例外。只要不获取它们的地址，就可以在不提供定义的情况下声明并使用它们。


### 形似函数的宏，使用 inline 替换

```C
#define CALL_WITH_MAX(a, b) f((a) > (b) ? (a) : (b))

// 上面的宏可以替换为：

template<typename T>
inline void callWithMax(const T& a, const T& b) {
	f(a > b ? a : b);
}
```