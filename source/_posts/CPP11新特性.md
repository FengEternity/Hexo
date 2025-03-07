---
# 基本信息
title: C++11 新特性 
date: 2025/03/06
tags:
  -cpp
categories: 
  -cpp
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/aeecc37df29a25610d3d185900e38f8a.mp4.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/aeecc37df29a25610d3d185900e38f8a.mp4.jpg
poster:  # 海报（可选，全图封面卡片）
  headline:  C++11 新特性
---

# C++ 11 新特性

## 1. auto 类型推导

作用：编译器会在编译期间自动推导出变量的类型，这样我们就不用手动指明变量的数据类型。

## 注意事项

* **推导时不能有二义性**：如 `auto a = 10, b = 12.3;  `; 此处推导 a 为 int 类型，但是 b 为 double，auto 无法进行推导

## 限制

1. 使用 auto 时必须对变量进行初始化
2. auto 不能在函数的参数中使用，因为在函数的定义时，只是对参数进行声明，指明了参数的类型，但是并没有进行初始化
3. 不能用于定义数组，如`auto str[] = "hello";`

## 应用

使用 auto 定义迭代器，如：

```c++
vector<int> vec = {1, 2, 3, 4, 5};
vector<int>::iterator it = vector.begin();
auto it = vector.begin();
```

两种定义迭代器的方法是等效的。



## 2. decltype 类型推导

1. 作用：与 auto 类似，用于在编译时期进行自动类型推导。

   > RTTI(Run-Time Type Identification 运行时类型识别)：程序运行时才知道实际类型，缺陷是会降低程序运行效率

2.  decltype 是根据表达式的实际类型推导出定义变量时所用的类型，例如

   1. 推演表达式类型作为变量的定义类型

      ```c++
      short a = 32670;
      short b = 32670;
      decltype(a + b) c;
      cout << typeid(c).name() << endl; // 输出： i，即 int 类型
      ```

      这里不是 short 的原因是，编译器防止溢出进行类型提升

      > ![image-20250306232555269](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20250306232555269.png)

   2. 推导函数返回值类型

      ![image-20250306233422600](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20250306233422600.png)

      需要注意的是，不要直接推导不带参的函数，因为函数本质上是一个地址即 void* （感觉这个例子不好，应该定义一个返回值不是 void * 的函数进行区分）

      ```c++
      #include <iostream>
      
      // 使用模板替代 auto 参数
      template<typename T, typename U>
      auto sum(T a, U b) -> decltype(a + b) { return a + b; }
      
      int main() {
          std::cout << typeid(decltype(sum<int, int>)).name() << std::endl; // FiiiiE, 代表函数指针类型
          std::cout << typeid(decltype(sum(10, 10))).name() << std::endl; // i，代表 int
      
          return 0;
      }
      ```

      第一行，使用了显式模版实例化，直接指定了模版参数类型为 <int, int>，这里获取的是函数模版实例化后的函数类型。

      第二行，使用了模版参数推导，编译器根据参数自动推导出模版参数类型，这里获取的函数返回值的类型。

## 3. 基于范围的 for 循环

```c++
for(declaration : expression) {
  // 循环体
}
```

* declaration：表示此处要定义一个变量，该变量的类型为要遍历序列中存储元素的类型。C++11中，此处可以使用 auto 进行推导
* expression：表示要进行遍历的序列

> 使用基于范围的 for 循环，如果在遍历时想要修改元素的值，将 declaration 参数处定义为**引用类型**即可。

## 4. 列表初始化

C++ 11 标准下，初始化列表的适用性被大大增加，它可以用于任意类型对象的初始化。

```c++
// 定义一个学生类
class Student {
private:
    string name;
    double gradePointAverage;

public:
    Student(const string &n): name(n), gradePointAverage(0.0) {}

    void addGrade(double gpa) {
        gradePointAverage += gpa / 10.0;
    }
};

Student students[3]{{"Tom", 3.5},{ "Jerry", 3.8 }, {"Spike", 3.2}}; 

```

 如果类中有成员变量是 const 类型，那么只能使用列表初始化的方式进行初始化。

此外需要注意的是，**在上面代码中成员变量初始化的顺序并非此处构造函数的书写顺序，而是在类中声明的顺序。**为了避免错误，在编码过程中要使成员变量声明顺序，构造函数初始化顺序，和实例化对象时的初始化顺序三者一致。

## 5. 使用 using 定义别名

 写法：`using db = double;` 等同于 `typedef double db;`

## 6. final 关键字

* 用来修饰类：表示这个类不能被继承
* 用来修饰虚函数：表示该函数不可被子类重写

