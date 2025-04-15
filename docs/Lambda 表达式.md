---

# 基本信息
## title: Lambda表达式  
date: 2025/03/12  
tags:  
  - cpp  
categories:  
  - 技术学习  
# 封面  
cover: [https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif)  
banner: [https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif)  
poster:  # 海报（可选，全图封面卡片）  
  headline:  Lambda表达式
Lambda 表达式是现代 C++中最重要的特征之一，它实际上是提供了一个类似于匿名函数的特性，而匿名函数则是在需要一个函数，但是又不想费力去命名一个函数的情况下去使用的。

# 1. 基础
基本语法：

```cpp
[捕获列表](参数列表) mutable(可选) 异常属性 -> 返回类型 {
 // 函数体
}
```

上面的语法规则除了 `[捕获列表]` 内的东西外，其他部分都很好理解，只是一般函数的函数名被略去， 返回值使用了一个 `->` 的形式进行。

## 捕获列表
**作用**：定义 lambda 表达式内部可以访问的外部变量。

所谓捕获列表，其实可以理解为参数的一种类型，Lambda 表达式内部函数体在默认情况下是不能够使用函数体外部的变量的， 这时候捕获列表可以起到传递外部数据的作用。根据传递的行为，捕获列表也分为以下几种：



**捕获方式**（与函数的值传递、引用传递类似）：

+ 值捕获（`=`）：默认使用`=`以值的方式捕获所有在 lambda 定义时可见的外部变量。这**意味着 lambda 内部对这些变量的修改不会影响到外部变量**。
+ 引用捕获（`&`）：lambda 内部对变量的修改会影响外部变量。
+ 混合捕获：同时使用值捕获与应用捕获
+ 默认不捕获：如果捕获列表为空，则不捕获任何外部变量

```cpp
void lambda_value_capture() {  
    int value = 1;  
    auto copy_value = [value] {  
        return value;  
    };  
    value = 100;  
    auto stored_value = copy_value();  
    std::cout << "stored_value = " << stored_value << std::endl;  
    // 这时, stored_value == 1, 而 value == 100.  
    // 因为 copy_value 在创建时就保存了一份 value 的拷贝  
}


void lambda_reference_capture() {  
    int value = 1;  
    auto copy_value = [&value] {  
        return value;  
    };  
    value = 100;  
    auto stored_value = copy_value();  
    std::cout << "stored_value = " << stored_value << std::endl;  
    // 这时, stored_value == 100, value == 100.  
    // 因为 copy_value 保存的是引用  
}

```



### 隐式捕获
指在lambda表达式的捕获列表中不明确指定要捕获哪些外部变量，而是让编译器根据函数体内部使用的变量自动决定需要捕获哪些变量

```cpp
int main() {
    int x = 10;
    int y = 20;

    // 隐式地以值捕获所有外部变量
    auto sum = [=]() { return x + y; };

    // 隐式地以引用捕获所有外部变量
    auto increment_x = [&]() { x += 1; };

    std::cout << "Sum: " << sum() << std::endl;       // 输出: Sum: 30
    std::cout << "x after increment: "<< x << std::endl; // 输出: x after increment: 11

    return 0;
}
```

### 表达式捕获
上面提到的值捕获、引用捕获都是已经在外层作用域声明的变量，因此这些捕获方式捕获的均为左值，而不能捕获右值。  
C++14 给与了我们方便，允许捕获的成员用任意的表达式进行初始化，这就允许了右值的捕获， 被声明的捕获变量类型会根据表达式进行判断，判断方式与使用 `auto` 本质上是相同的

```cpp
#include <iostream>  
#include <memory>  // std::make_unique  
#include <utility> // std::move  
  
void lambda_expression_capture() {  
    auto important = std::make_unique<int>(1);  
    auto add = [v1 = 1, v2 = std::move(important)](int x, int y) -> int {  
        return x+y+v1+(*v2);  
    };  
    std::cout << add(3,4) << std::endl;  // 9
}
```

在上面的代码中，important 是一个独占指针，是不能够被 "=" 值捕获到，这时候我们可以将其转移为右值，在表达式中初始化。

## 参数列表
**作用**：定义函数体中可接受的参数

```cpp
auto lambda = [](int a, int b) {return a + b;}
int result = lambda(3, 4); // result = 7
```

需要注意的是，C++11中 `auto` 关键字无法在参数列表中使用

## mutable 关键字
lambda表达式默认是`const`的，无法修改以值捕获的变量。而 mutable 关键字的作用是，允许在 lambda 表达式内部修改以值捕获的变量，如：

```cpp
int y = 20;
auto increment = [y]() mutable { y += 1; return y; }; // 允许修改y
```

## 异常属性（ `exception_specification`）
**作用**：指定lambda表达式抛出异常的类型或是否抛出异常。  
**语法**：

+ `noexcept`：表示lambda不会抛出任何异常。
+ 其他异常规范（如`throw(type)`，但在C++11后不推荐使用）。

```cpp
auto safe_divide = [](int a, int b) noexcept -> int {
    if (b == 0) return 0; // 避免抛出异常
    return a / b;
};
```

## 返回类型
**作用**：显式指定lambda表达式的返回类型。  
**使用场景**：

+ 当编译器无法自动推断返回类型时，需要显式指定。
+ 提高代码的可读性和可维护性。



```cpp
auto multiply = [](double a, double b) -> double {
    return a * b;
};
```

## 综合示例
```cpp
int main() {
    int a = 5;
    int b = 10;

    // 捕获a和b，以引用方式捕获，并允许修改
    auto modify = [&a, &b]() mutable {
        a += 1;
        b += 2;
    };

    modify();
    std::cout << "a: "<< a << ", b: "<< b << std::endl; // 输出: a: 6, b: 12

    // 带有参数和返回类型的lambda
    auto add = [](int x, int y) -> int {
        return x + y;
    };

    std::cout << "Add: " << add(a, b) << std::endl; // 输出: Add: 18

    return 0;
}
```

# 2. 范型 lambda
上一节中我们提到了 `auto` 关键字不能够用在参数表里，这是因为这样的写法会与模板的功能产生冲突。 但是 Lambda 表达式并不是普通函数，所以在没有明确指明参数表类型的情况下，Lambda 表达式并不能够模板化。 幸运的是，这种麻烦只存在于 C++11 中，从 C++14 开始，Lambda 函数的形式参数可以使用 `auto` 关键字来产生意义上的泛型：

```cpp
auto add = [](auto x, auto y) {  
    return x+y;  
};  
  
add(1, 2);  
add(1.1, 2.2);
```

