---
title: C 程序设计语言（二）—— 类型、运算符与表达式
date: 2025/4/11
tags:
  - C语言
  - 程序设计
  - 技术教程
categories: [技术学习]
description: 本章讲解变量命名规则和数据类型。变量名由字母数字序列构成，首字符必须是字母，下划线也视为字母。局部变量名较短，外部变量名较长。基本数据类型可加限定符如short、long，int表示自然长度整数。signed和unsigned可用于char和整型。
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

## 常量

前缀为 0 的整型常量表示八进制形式；0x \ 0X 表示十六进制。

字符常量也是一个整数。如 ASCII 字符集中，字符 `0` 的值为 48 ，与整数 0 没有关系。

