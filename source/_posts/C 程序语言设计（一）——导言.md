---
title: C 程序语言设计（一）——导言
date: 2025/4/10
tags:
  - C语言
  - 程序设计
  - 技术教程
categories:
  - C语言
description: "本文是关于C程序语言设计的导言，涵盖了C语言的基本概念。主要内容包括：C程序由函数和变量组成，main函数是程序起点；变量声明和使用规则；for语句和符号常量定义；字符输入输出处理，包括getchar和putchar函数；文件复制、字符统计、行计数和单词计数程序示例；数组和函数；参数传值调用；字符数组；外部变量与作用域。最后提供了一个制表符处理的C程序示例。"
author: Forsertee
type: tech
topic: cpl
---
## 1.1 入门
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250409170128617.png?imageSlim)

一个C语言程序，无论其大小如何，都是由函数和变量组成的。main 函数是一个特殊的函数，每个程序都从 main 函数的起点开始执行，这也意味着每个程序都必须在某个位置包含 main 函数。


## 1.2 变量与算术运算符

C 语言中，所有变量都得先声明后使用。
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250409180905538.png?imageSlim)
## 1.3 for 语句

## 1.4 符号常量

`#define` 指令可以把符号名（或称为符号常量）定义为一个特定的字符串：
```c
#define 名字 替换文本

// #define lower 0
```

## 1.5 字符输入 / 输出

无论文本从何处输入输出，其输出输出都是按照字符流的方式处理。

`getchar` 函数从文本流中读入在一个输入字符，并将其作为结果值返回。

```c
c = getchar();
```

之后，变量 c 将包含输入流的下一个字符。


### 1.5.1 文件复制

```c
int main() {
    int c;
	c = getchar();
	while(c != EOF) {
		putchar(c);
		c = getchar();
	} 
}

// 上面的代码可以改写为

int main() {
	int c; 
	while((c = getchar()) != EOF) putchar(c);
}
```

字符无论存放在任何位置，它在机器内部都是以位模式存储的。

getchar()返回值是 int 类型。此外，当输入流结束时，`getchar()`会返回一个特殊的整数值`EOF`（通常定义为`-1`）。若用`char`类型存储，可能因字符编码范围（如`signed char`的`-128~127`或`unsigned char`的`0~255`）无法正确表示`EOF`，导致循环无法终止。

### 1.5.2 字符统计

### 1.5.3 行计数

### 1.5.4 单词计数

下面是 UNIX 系统中 `wc` 命令的实现
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250409185339116.png?imageSlim)
## 1.6 数组

## 1.7 函数

## 1.8 参数——传值调用

值传递方式，传递给调用函数的参数值存放在临时变量中，而不是存放在原来的变量中。与之对应的是引用穿的。

## 1.9 字符数组

## 1.10  外部变量与作用域

**定义在所有函数体之外、且只能定义一次**的变量称为外部变量，可以在全局范围内访问。外部变量定义后编译程序将为它分配存储单元。在每个需要访问外部变量的函数中，必须声明相应的外部变量，此时说明其类型。声明时可以使用`extern` 语句显式声明，也可以通过上下文隐式声明。

当外部变量在函数调用前已定义时，可直接使用，无需`extern`。然而，若变量类型复杂（如数组），隐式声明可能导致编译错误，建议始终显式声明。

> 定义（define）表示创建变量或分配内存单元；而声明（declaration）指的是说明变量的性质，但并不分配存储单元。


## Q1-20

```c
#include<stdio.h>

#define TAB_STOP 8 // 制表符终止位的间隔通常是固定的（如每8列），且在程序中可能多次使用。

int main() {
    int c;
    int pos = 0;
    while((c = getchar()) != EOF) {
        if(c == '\t') {
            int spaces = TAB_STOP - (pos % TAB_STOP);
            for(int i = 0; i < spaces; ++i) {
                putchar('_');
                pos++;
            }
        } else {
            putchar(c);
            pos++;
        }
    }
    return 0;
}
```

