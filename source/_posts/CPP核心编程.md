---
# 基本信息
title: C++ 核心编程
date: 2024/07/11
tags: [cpp, 计算机]
categories: [cpp]
description: C++ 核心编程
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220629231150_70886.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220629231150_70886.gif
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  C++ 核心编程 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: true
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

> 本文为个人自学笔记，系统学习请寻找其他资料

# 1. 内存分区模型

C++程序在执行时，将内存大方向划分为**4个区域**

- 代码区：存放函数体的二进制代码，由操作系统进行管理的
- 全局区：存放全局变量和静态变量以及常量
- **栈区：由编译器自动分配释放, 存放函数的参数值,局部变量等**
- **堆区：由程序员分配和释放,若程序员不释放,程序结束时由操作系统回收**

**内存四区意义：**

不同区域存放的数据，赋予不同的生命周期, 给我们更大的灵活编程

## 1.1 程序运行前

* 只有代码区和全局区
* 代码区具有**只读** **共享**的特点
* 全局区存放全局变量、静态变量、常量
* 常量区中存放 const修饰的 **全局常量** 和 **字符串常量**

## 1.2 程序运行后

* 栈区：由编译器自动分配释放, 存放函数的参数值,局部变量等
* 堆区：由程序员分配释放,若程序员不释放,程序结束时由操作系统回收（**new出来的空间**）



# 2. 引用

* 作用：给变量起别名

* 本质：**引用的本质在c++内部实现是一个指针常量.**

# 3. 函数提高

## 3.3 函数重载

**函数重载满足条件：**

- 同一个作用域下
- 函数名称相同
- 函数参数**类型不同** 或者 **个数不同** 或者 **顺序不同**

**注意:** 函数的返回值不可以作为函数重载的条件

# 4. 类和对象

## 4.1 封装

1. 封装的意义：

   - 将属性和行为作为一个整体，表现生活中的事物

   - 将属性和行为加以权限控制

2. 在C++中 struct和class唯一的**区别**就在于 **默认的访问权限不同**

   - struct 默认权限为公共

   - class 默认权限为私有

## 4.2 对象的初始化与清理

### 4.2.1 构造函数与析构函数

**编译器提供的构造函数和析构函数是空实现。**

- 构造函数：主要作用在于创建对象时为对象的成员属性赋值，构造函数由编译器自动调用，无须手动调用。
- 析构函数：主要作用在于对象**销毁前**系统自动调用，执行一些清理工作。

**构造函数语法：**`类名(){}`

1. 构造函数，没有返回值也不写void
2. 函数名称与类名相同
3. 构造函数可以有参数，因此可以发生重载
4. 程序在调用对象时候会自动调用构造，无须手动调用，而且只会调用一次

**析构函数语法：** `~类名(){}`

1. 析构函数，没有返回值也不写void
2. 函数名称与类名相同,在名称前加上符号 ~
3. 析构函数不可以有参数，因此不可以发生重载
4. 程序在对象销毁前会自动调用析构，无须手动调用，而且只会调用一次

代码示例：

```c++
class Person
{
public:
	//构造函数
	Person()
	{
		cout << "Person的构造函数调用" << endl;
	}
	//析构函数
	~Person()
	{
		cout << "Person的析构函数调用" << endl;
	}

};

void test01()
{
	Person p;
}

int main() {
	
	test01();

	system("pause");

	return 0;
}
```

### 4.2.2 构造函数的分类及调用

* 两种分类方式：
  * 按参数分为： 有参构造和无参构造
  * 按类型分为： 普通构造和拷贝构造

* 三种调用方式：
  * 括号法
  * 显示法
  * 隐式转换法
  
  **析构的顺序与构造相反**

### 4.2.4 构造函数的调用规则

1. 创建用个类，C++编译器会给每个类都添加至少三个函数
   1. 默认构造
   2. 析构函数
   3. 拷贝构造

构造函数调用规则如下：

- **如果用户定义有参构造函数，c++不在提供默认无参构造，但是会提供默认拷贝构造**
- **如果用户定义拷贝构造函数，c++不会再提供其他构造函数**

### 4.2.5 深拷贝与浅拷贝

深浅拷贝是面试经典问题，也是常见的一个坑

* 浅拷贝：简单的赋值拷贝操作

* 深拷贝：在堆区重新申请空间，进行拷贝操作

总结：如果属性有在堆区开辟的，一定要自己提供拷贝构造函数，防止浅拷贝带来的问题

### 4.2.6 初始化列表

**语法：**`构造函数()：属性1(值1),属性2（值2）... {}`

![image-20240713174807633](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240713174807633.png)

### 4.2.8 静态成员函数

静态成员就是在成员变量和成员函数前加上关键字static，称为静态成员

静态成员分为：

- 静态成员变量
  - 所有对象共享同一份数据
  - 在编译阶段分配内存
  - 类内声明，类外初始化
- 静态成员函数
  - 所有对象共享同一个函数
  - 静态成员函数只能访问静态成员变量



## 4.3 C++对象模型和 this 指针

### 4.3.2 this 指针

**this指针指向被调用的成员函数所属的对象**

this指针的用途：

- 当形参和成员变量同名时，可用this指针来区分
- 在类的非静态成员函数中返回对象本身，可使用return *this



### 4.3.4 const修饰成员函数

**常函数：**

- 成员函数后加const后我们称为这个函数为**常函数**
- 常函数内不可以修改成员属性
- 成员属性声明时加关键字mutable后，在常函数中依然可以修改

**常对象：**

- 声明对象前加const称该对象为常对象
- 常对象只能调用常函数

## 4.4 友元

友元的目的就是让一个函数或者类 访问另一个类中私有成员

友元的关键字为 ==friend==

友元的三种实现

- 全局函数做友元
- 类做友元
- 成员函数做友元



1. 全局函数作友元
2. 类作友元
