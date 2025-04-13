---
# 基本信息
title: C++11 新特性 
date: 2025/03/06
tags:
  - cpp
categories: [技术学习]
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

## 7. 右值引用

之所以需要右值引用，是因为右值往往是没有名称的，在实际开发中可能需要对其进行修改，因此只能使用引用的方法。

C++标准委员会在选定右值引用符号时，既希望选用现有 C++内部已有的符号，还不能与 C++98/03 标准冲突，最终选择 `&&`。

### 左值与右值

* 左值：表示可以**获取地址的表达式**，可以出现在赋值语句的左边
* 右值：无法获取地址的对象，有**常量值、函数返回值、lambda表达式**等。

### 语法

语法：`类型&& 引用变量的名字 = 右值； `

```c++
int && a = 10;
a = 100;
cout << a << endl;// 输出结果为 100

int num  = 10;
// int && b = num;  // 语法错误。右值引用不能初始化为左值
```

### 移动语义

在C++中定义类时，如果该类包含需要特殊处理的资源，比如动态分配的内存（通过指针管理），则需要你手动提供拷贝构造函数、赋值运算符重载和析构函数。这是因为默认的编译器生成的行为可能不是你想要的，特别是对于资源的复制和释放操作，若不正确处理，可能会导致内存泄漏、资源竞争或悬挂指针等问题。

> 悬挂指针（Dangling Pointer）是一种指针，它指向的是一个已经被释放（deallocated）或已经不再被程序所控制的内存区域。

系统默认的拷贝构造函数是一个浅拷贝构造函数，在下面的例子从就会出现问题：

```c++
class Resource {
public:
    Resource() : data(new int) {
        *data = 0;  // 动态分配内存，并初始化一个整数
    }
    // 省略默认拷贝构造函数、赋值运算符和析构函数

private:
    int* data;
};

```

如果此时想要复制这个对象：

```c++
Resource r1;  // 初始对象
Resource r2 = r1;  // 尝试拷贝

// 或者
Resource r1;  // 初始对象
Resource r3;
r3 = r1;  // 尝试赋值

```

均会使用默认的拷贝构造函数和赋值运算符，这意味着两个不同的对象`r2`和`r3`都将包含同样的指针指向同一个动态分配的整数。当这些对象析构时，都会尝试释放同一个内存块，导致第二次释放（double-free）错误。

正确的处理方式如下：

```c++
class Resource {
public:
    Resource() : data(new int) {
        *data = 0;  // 动态分配内存，并初始化一个整数
    }

    // 拷贝构造函数
    Resource(const Resource& other) {
        data = new int(*other.data);
    }

    // 赋值运算符
    Resource& operator=(const Resource& other) {
        if (this != &other) {  // 检查自我赋值
            delete data;
            data = new int(*other.data);
        }
        return *this;
    }

    // 析构函数
    ~Resource() {
        delete data;
    }

private:
    int* data;
};

```

通过这种方式，每次对象复制或赋值都将分配新的内存，这样就不会存在资源释放的问题。当对象析构时，也会正确地释放它们各自分配的内存资源。

正如我们所见，`Resource` 类初始化时会分配内存，并在析构时释放这块内存。拷贝构造函数简单地复制整数值。在一个只有简单数据类型复制的场景里，这还不算问题，但在处理更大规模的数据或者更复杂的资源管理时，这种深拷贝会引发效率问题和资源浪费。

当我们考虑诸如临时对象、返回值优化（RVO）和异常安全等C++概念时，深拷贝变得尤为低效。类的移动构造函数和移动赋值运算符应运而生，它们旨在通过采用资源的所有权转移，而不是复制，来优化性能。

下面的代码展示了移动语义：

```c++
#include <iostream>

class Resource {
public:
    // 默认构造函数
    Resource() : data(new int) {
        *data = 0;  // 动态分配内存，并初始化一个整数
    }

    // 拷贝构造函数
    Resource(const Resource& other) {
        data = new int(*other.data);
    }

    // 移动构造函数
    Resource(Resource&& other) noexcept : data(other.data) {
        other.data = nullptr;  // 将临时对象的内部指针置空，以避免析构时释放资源
    }

    // 赋值运算符
    Resource& operator=(const Resource& other) {
        if (this != &other) {  // 检查自我赋值
            delete data;
            data = new int(*other.data);
        }
        return *this;
    }

    // 移动赋值运算符
    Resource& operator=(Resource&& other) noexcept {
        if (this != &other) {  // 避免自我赋值
            delete data;  // 释放当前对象的资源
            data = other.data;  // 窃取其他对象的资源
            other.data = nullptr;  // 将其他对象的指针置空
        }
        return *this;
    }

    // 析构函数
    ~Resource() {
        delete data;
    }

    // 友元函数，用于打印内部的整数值，以方便测试
    friend std::ostream& operator<<(std::ostream& os, const Resource& res) {
        os << *res.data;
        return os;
    }

private:
    int* data;
};

int main() {
    Resource r1;
    Resource r2 = r1;  // 测试拷贝构造函数
    Resource r3(r1);   // 测试拷贝构造函数
    Resource r4;      // 测试默认构造函数
    r4 = std::move(r1);  // 测试移动赋值运算符
    Resource r5(std::move(r2));  // 测试移动构造函数

    std::cout << "r4: " << r4 << std::endl;  // 输出 r4 的值，应为 0（从 r1 移动后 r1 的值）
    std::cout << "r1: " << r1 << std::endl;  // 输出 r1 的值，应为 1431655762（移动后变为未定义的值）

    return 0;
}

```

在移动构造函数中，我们接收了一个**右值引用**。就如同在类的传统构造函数中，我们管理新分配的内存一样，此处我们直接获取了传入对象的内存资源。重要的是，在所有操作完成后，我们将传入对象的资源指针清零，防止在它的消亡过程中重复释放。

移动赋值运算符的实现与构造函数类似，但是涉及到现有对象的资源管理。在将新资源赋给`this`之前，我们首先需要释放当前拥有的资源。利用C++的异常安全保证，这种处理确保了即便在复制操作中抛出异常，现有资源也被正确清理。

## 8. move 函数
作用：将一个左值强制转化为右值引用，通过右值引用使用该值，实现移动语义。