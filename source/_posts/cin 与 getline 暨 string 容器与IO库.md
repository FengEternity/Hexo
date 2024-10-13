---
title: cin 与 getline 暨 string 容器与IO库
date: 2024/10/12
tags:
  - cpp
  - 计算机
  - debug
categories:
  - debug
  - cpp
description: cin 与 getline 暨 string 容器与IO库
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
poster:
  topic: 
  headline: cin 与 getline 暨 string 容器与IO库
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
# 问题复现

你觉得下面这个代码在输入`1 +1`(注意中间有一个空格)时，会输出什么呢？

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241012223632.png)



按照设想，是不是应该输出：`1 +1`，然而并没有，输出如下：

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241012223803.png)


# 问题分析

要解决这个问题很简单，使用我注释掉的那一行代码就可以，原因在于，二者的读取方式不同：

* cin：读取输入直到遇到空格、换行或其他空白字符。只会读取第一个单词或数字，剩下的内容会留在输入缓冲区中，等待下次读取。
* getline：读取整行输入，包括空格，直到遇到换行符为止。读取整行后，输入缓冲区会被清空，直接进入下一行。



> 但是，这次面试让我认识到，这是不够的！！！
> 所以，借此机会深入的学习一下：`C++ 标准库中的 I/O库` ， `STL 中的 string容器` 

> 注：参考书籍为：《C++ Primer（第5版）》

# string 容器

## 定义和初始化

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241013212701.png)

上述的示例中，分为两种初始化方式：**直接初始化**和**拷贝初始化**

如果使用等号 `(= )` 初始化一个变量，实际上执行的是拷贝初始化(copy initialization)，编译器把等号右侧的初始值拷贝到新创建的对象中去。与之相反，如果不使用等号，则执行的是直接初始化(direct initialization).

需要注意的是`string s2(s1);`属于直接初始化，而不是拷贝初始化。

## string 对象上的操作

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241013214047.png)


### 读写 string 对象

```C
int main() {
	string s;
	cin >> s;
	cout << s << endl; 
	return 0;
}

int compare() {
	string s1, s2;
	cin >> s1 >> s2;
	cout << s1 << s2;
	return 0;
}
```

在执行读 取 操 作 时 ， `string` 对 象 会 自 动 忽 略 开 头 的 空 白 (即 空 格 符 、 换 行 符 、 制 表 符 等 ) 并 从 第一个真正的字符开始读起，直到遇见下一处空白为止。

如上所述，如果程序输入`   Hello World    `，`main`函数将会输出`Hello`输出结果中不含任何空格。而与之对比的`compare`函数将会输出`HelloWorld`**（这也就是本文所遇到的BUG）**，解决方案就是使用 `getline`来读取一阵行。

`getline` 函数的参数是一个输入流和一个`string`对象，函数从给定的输入流中读入内容，直到遇到换行符为止 (注意换行符也被读进 来了)，然后把所读的内容存入到那个 `string` 对象中去 ( 注 意 不 存 换 行 符 )。 `getline` 只要一遇到换行符就结束读取操作并返回结果，哪怕输入的一开始就是换行符也是如此。如果输入真的 一开始就是换行符，那么所得的结果是个空`string`。

### 比较 string 对象

相等性运算符( == 和 != )分别检验两个string对象相等或不相等，string对象相等意味着它们的长度相同而且所包含的字符也全都相同。关系运算符 < 、<= 、> 、 >= 分别检验一个 string 对象是否小于、小于等于、大于、大于等于另外一个string 对象。上述这些运算符都依照 (大小写敏感的)字典顺序:

1. 如果两个 string 对象的长度不同，而且较短 string 对象的每个字符都与较长 string 对象对应位置上的字符相同 ，就说较短 string 对象小于较长 string 对象。
2. 如果两个 string 对象在某些对应的位置上不一致，则string对象比较的结果 其实是 string 对象中第一对相异字符比较的结果。

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241013220711.png)


### string 类型相加

因为某些历史原因，也为了与 C 兼容，所以 C++ 语言中的字符串字面值并不是标准库类型 string 的对象。切记，字符串字面值与 string 是不同的类型。

而 string 类型重载的 `+`运算符要求运算符左右两侧必须有一个是 string 类型，这就导致了下面代码中 s3 和 s4 语句是错误的

```C
string s1 = "Hello";
string s2 = "World";

string s3 = "Hello" + " , " + "World"; // 错误
string s4 = "Hello" + " , " + s2; // 错误,该语句等价于 string temp = "Hello" + " , "; string s4 = temp + s2;
string s5 = s1 + " , " + "World";
```

## 处理 string 对象中的字符

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241013221758.png)


# I/O 库

## IO类
## 文件输入输出
## string 流
