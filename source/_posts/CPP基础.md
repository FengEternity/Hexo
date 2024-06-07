---
# 基本信息
title: C++ 基础
date: 2024/05/13
tags: [cpp, 计算机]
categories: [cpp]
description: C++ 学习记录，基础语法学习，较为详细介绍指针和结构体的基础语法。
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  C++ 基础 # 必选
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

# C++ 基础入门
~~注：本文章仅供个人学习使用，如需系统学习，请阅读[C++基础入门](https://github.com/Blitzer207/C-Resource/blob/master/第1阶段C%2B%2B%20匠心之作%20从0到1入门/C%2B%2B基础入门讲义/C%2B%2B基础入门.md)~~
# 零散知识
1. 科学计数法： 
    ```C++
       float f1 = 3e2; // 3 * 10 ^ 2
       float f2 = 3e-2; // 3 * 0.1 ^ 2
    ```


2. 使用 ASCII 码给字符型变量赋值

    ```C++
        char ch = 'a';
        cout << ch << endl;
        cout << sizeof (ch) << endl;
    
        ch = 98; // 使用 ASCII 码给字符型变量赋值
        cout << ch << endl;
    ```
    输出：![img.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/img.png)


3. 输入 bool 型变量
    ```C++
       bool flag = true;
       cout << "输入布尔型变量：" << endl;
       cin >> flag;
       cout << !flag << endl;
    ```
   输出：![img_1.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/img_1.png)


4. 前++和后++
   
    前置递增：先让变量+1，然后进行表达式运算赋值
    后置递增：先进行表达式计算赋值，再让变量+1
   ![img_2.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/img_2.png)


5. ![img_3.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/img_3.png)


6. 三目运算符
   * 语法：表达式1 ? 表达式2 : 表达式3
   * 解释：
     * 如果表达式1的值为真，执行表达式2，并返回表达式2的结果；
     * 如果表达式1的值为假，执行表达式3，并返回表达式3的结果。

# 指针
~~相关内容源自黑马课程~~
作用：可以通过指针间接访问内存
![img_4.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/img_4.png)

指针变量可以通过" * "操作符，操作指针变量指向的内存空间，这个过程称为解引用
具体定义如下：
```C++
int a = 10;
int *p;
// &a = p;
// *p = a;
```

* 所有指针类型在32位操作系统下是4个字节 
## 空指针
* 指针变量指向内存中编号为0的空间
* 用途：初始化指针
* 注意：空指针指向的内存是不可以访问的
* 0-255之间的内存编号是系统占用的，不可以访问 
## 野指针
* 类比开房，并不是走到哪个门口想进就能进的，
必须实现开好房间（申请好内存）
## const 修饰指针 
* const 修饰指针 --- 常量指针 
  * 特点：指针的指向可以修改，但是指向的指不能修改
* const 修饰常量 --- 指针常量 
  * 特点：常量指针相反
* const 即修饰指针，又修饰常量
      
```C++
  int main() {
    
      int a = 10;
      int b = 10;
    
      //const 修饰的是指针，指针指向可以改，指针指向的值不可以更改
      const int * p1 = &a; 
      p1 = &b; //正确
      //*p1 = 100;  报错
        
    
      //const 修饰的是常量，指针指向不可以改，指针指向的值可以更改
      int * const p2 = &a;
      //p2 = &b; //错误
      *p2 = 100; //正确
    
      //const 既修饰指针又修饰常量
      const int * const p3 = &a;
      //p3 = &b; //错误
      //*p3 = 100; //错误
    
      return 0;
  }
```

## 指针和数组
作用：利用指针访问数组中的元素

## 指针和函数
利用指针作函数参数，可以修改实参的值

# 结构体
结构体是属于用户自定义的数据类型，允许用户存储不同的数据类型。


```C++
//结构体定义
struct student
{
//成员列表
string name;  //姓名
int age;      //年龄
int score;    //分数
}stu3; //结构体变量创建方式3


int main() {

    //结构体变量创建方式1
    struct student stu1; //struct 关键字可以省略

    stu1.name = "张三";
    stu1.age = 18;
    stu1.score = 100;
    
    cout << "姓名：" << stu1.name << " 年龄：" << stu1.age  << " 分数：" << stu1.score << endl;

    //结构体变量创建方式2
    struct student stu2 = { "李四",19,60 };

    cout << "姓名：" << stu2.name << " 年龄：" << stu2.age  << " 分数：" << stu2.score << endl;


    stu3.name = "王五";
    stu3.age = 18;
    stu3.score = 80;
    

    cout << "姓名：" << stu3.name << " 年龄：" << stu3.age  << " 分数：" << stu3.score << endl;

    system("pause");

    return 0;
}
```

* 总结1：定义结构体时的关键字是struct，不可省略
* 总结2：创建结构体变量时，关键字struct可以省略
* 总结3：结构体变量利用操作符 ''.'' 访问成员

## 结构体数组
```C++
struct  结构体名 数组名[元素个数] = {  {} , {} , ... {} }
```

## 结构体指针
通过指针访问结构体中的成员

```C++
//结构体定义
struct student
{
//成员列表
string name;  //姓名
int age;      //年龄
int score;    //分数
};


int main() {

    struct student stu = { "张三",18,100, };
    
    struct student * p = &stu;
    
    p->score = 80; //指针通过 -> 操作符可以访问成员

    cout << "姓名：" << p->name << " 年龄：" << p->age << " 分数：" << p->score << endl;
    
    system("pause");

    return 0;
}
```

## 结构体嵌套结构体

## 结构体做函数参数
将结构体作为参数向函数中传递

## 结构体中 const 使用场景

