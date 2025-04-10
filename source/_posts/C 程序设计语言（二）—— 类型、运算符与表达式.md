---
title: C 程序设计语言（二）—— 类型、运算符与表达式
date: 2025/4/11
tags:
  - C语言
  - 程序设计
  - 技术教程
categories:
  - C语言
description: 本文是关于C程序语言设计的导言，涵盖了C语言的基本概念。主要内容包括：C程序由函数和变量组成，main函数是程序起点；变量声明和使用规则；for语句和符号常量定义；字符输入输出处理，包括getchar和putchar函数；文件复制、字符统计、行计数和单词计数程序示例；数组和函数；参数传值调用；字符数组；外部变量与作用域。最后提供了一个制表符处理的C程序示例。
author: Forsertee
type: tech
topic: cpl
---
## 2.1 变量名

名字是由字母和数字组成的序列，但其第一个字符必须是字母。下划线 `“_” `被看作是字母，通常用于命名较长的变量名，以提高可读性。

局部变量一般使用较短的变量名，外部变量则相反。

## 2.2. 数据类型及长度
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250409213115026.png?imageSlim)
在基本数据类型的前面可以加一下限定符，如 `short` `long` 如 `short int sh;`,也可以简写为 `short sh;` 

`int` 通常代表机器中整数的自然长度。各种编译器可能根据硬件特点选择合适的长度，但是，`short` 类型通常且至少为 16 位，`long` 类型通常且至少为 32 位，并且 `short` 不得长于 `int`，`long` 不得短于 `int`。

类型限定符 `signed` 于 `unsigned` 可用于限定 `char` 类型或任何整型。