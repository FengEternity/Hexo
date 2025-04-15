---

# 基本信息
## title: 深入理解C++中的构造函数  
date: 2024/07/13  
tags: [cpp, 计算机]  
categories: [技术学习]  
description: 深入理解C++中的构造函数  
# 封面  
cover: [https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/v2-3651de3ebf61bf3c4934f32994261477_720w.gif](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/v2-3651de3ebf61bf3c4934f32994261477_720w.gif)  
banner: [https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/v2-3651de3ebf61bf3c4934f32994261477_720w.gif](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/v2-3651de3ebf61bf3c4934f32994261477_720w.gif)  
poster:  # 海报（可选，全图封面卡片）  
  topic: # 可选  
  headline:  深入理解C++中的构造函数 # 必选  
  caption:  # 可选  
  color:  # 可选  
# 插件  
sticky: # 数字越大越靠前  
mermaid:  
katex: true  
mathjax:   
# 可选  
author: Montee  
references:  
comments: # 设置 false 禁止评论  
indexing: # 设置 false 避免被搜索  
breadcrumb: # 设置 false 隐藏面包屑导航  
leftbar:   
rightbar:  
h1: # 设置为 '' 隐藏标题  
type: tech # tech/story
# 缘起
今天在优化 FileTag 项目的用户管理功能时，出现了因为构造函数不正确引起的编译错误，如下，

```bash
[ 20%] Building CXX object CMakeFiles/FileTag.dir/src/main.cpp.o
[ 40%] Building CXX object CMakeFiles/FileTag.dir/src/file_tag_system.cpp.o
/Users/montylee/NJUPT/Code/FileTag/src/file_tag_system.cpp:7:16: error: cons
tructor for 'FileTagSystem' must explicitly initialize the member 'userManager' which does not have a default constructor FileTagSystem::FileTagSystem(const std::string& tagsFile) : tagManager(tagsF
ile) { ^
/Users/montylee/NJUPT/Code/FileTag/src/file_tag_system.h:39:17: note: member
is declared here UserManager userManager; // 用户管理对象
^
/Users/montylee/NJUPT/Code/FileTag/src/user_manager.h:12:7: note: 'UserManag
er' declared here class UserManager {
^
1 error generated.
make[2]: *** [CMakeFiles/FileTag.dir/src/file_tag_system.cpp.o] Error 1
make[1]: *** [CMakeFiles/FileTag.dir/all] Error 2
make: *** [all] Error 2
```

根据错误信息，`FileTagSystem` 类的构造函数未能显式初始化 `userManager` 成员，而 `userManager` 成员没有默认构造函数。需要在 `FileTagSystem` 的构造函数初始化列表中初始化 `userManager`。

# 问题解决
修改后的代码为：

```plain
explicit FileTagSystem(const std::string& tagsFile, const std::string& usersFile);
```

很明显，这是个构造函数，用来接受标签文件路径和用户文件路径作为参数，用于初始化系统。

接下来，我将详细解释其作用、关键字 `explicit` 的意义，以及如何通过异常处理来确保系统的稳健性。

先在这里简单解释一下这条语句的含义，具体的知识点在后面给出，

+ `explicit`：防止隐式转换。
+ `FileTagSystem`：构造函数的名称，必须与类名相同。
+ `const std::string& tagsFile`：第一个参数，表示标签文件的路径，类型为常量字符串的引用。
+ `const std::string& usersFile`：第二个参数，表示用户文件的路径，类型为常量字符串的引用。

构造函数的具体实现如下，

```plain
FileTagSystem::FileTagSystem(const std::string& tagsFile, const std::string& usersFile)
    : tagManager(tagsFile), userManager(usersFile) {
    // 初始化用户管理器，添加一些默认用户
    userManager.addUser("admin", "admin123", UserRole::ADMIN);
    userManager.addUser("user", "user123", UserRole::USER);

    try {
        // 尝试加载标签和用户数据
        tagManager.loadTags();
        userManager.loadUsers();
    } catch (const std::exception& e) {
        // 如果加载失败，输出错误信息并退出程序
        std::cerr << e.what() << std::endl;
        exit(1);
    }
}

```

## 成员初始化列表
```plain
: tagManager(tagsFile), userManager(usersFile)

```

+ `tagManager(tagsFile)`：使用 `tagsFile` 初始化 `tagManager` 对象。`tagsFile` 是一个字符串，表示标签文件的路径。
+ `userManager(usersFile)`：使用 `usersFile` 初始化 `userManager` 对象。`usersFile` 是一个字符串，表示用户文件的路径。

**成员初始化列表在构造函数体执行之前初始化成员变量，这种方式比在构造函数体内初始化更加高效，特别是对于常量成员或引用成员。**

## 构造函数体
函数体里需要将的一点是，**异常处理**。

在构造函数中使用异常处理可以确保在初始化过程中出现问题时，程序能够优雅地处理错误。例如，如果标签文件或用户文件无法加载，程序会输出错误信息并终止运行，而不是继续执行可能导致更多问题的代码。

# 学习
## 什么是构造函数？
构造函数是一个特殊的成员函数，当一个对象被创建时，它会自动调用。构造函数的主要目的是初始化对象的成员变量，并执行任何必要的启动任务。

一个标准的构造函数形式如下，

```cpp
class MyClass {
public:
    MyClass() {
        // 默认构造函数
    }
};

```

默认构造函数是没有参数的构造函数。如果没有定义任何构造函数，编译器会自动生成一个默认构造函数。

## 参数化构造函数
参数化构造函数接受一个或多个参数，用于初始化对象的成员变量。

```cpp
class MyClass {
public:
    MyClass(int x, int y) : x(x), y(y) {
        // 参数化构造函数
    }
private:
    int x, y;
};
```

## 拷贝构造函数
拷贝构造函数用于创建一个新的对象作为现有对象的副本。它的参数是现有对象的引用。

```cpp
class MyClass {
public:
    MyClass(const MyClass& other) : x(other.x), y(other.y) {
        // 拷贝构造函数
    }
private:
    int x, y;
};
```

`const MyClass& other` 表示传递的是一个现有对象的引用，并且是常量引用，防止在拷贝过程中对原对象进行修改。

### 深入理解拷贝构造函数
在C++中，拷贝构造函数是一个特殊的构造函数，用于创建一个新的对象作为现有对象的副本。拷贝构造函数在以下几种情况下会被调用：

1. 当一个对象以值传递的方式传递给函数时。
2. 当一个对象从函数返回时。
3. 当一个对象被另一个对象初始化时。

拷贝构造函数是C++中一个重要的特性，特别是在处理动态内存分配时。通过定义拷贝构造函数，我们可以确保对象在复制过程中正确地管理资源，避免浅拷贝带来的问题。理解拷贝构造函数的工作原理和应用场景，对于编写高效、健壮的C++代码至关重要。

#### 拷贝构造函数的实现
让我们通过一个具体的例子来详细讲解拷贝构造函数的实现。

```cpp
#include <iostream>
#include <cstring>

class String {
public:
    String(const char* str = nullptr); // 普通构造函数
    String(const String& other); // 拷贝构造函数
    ~String(); // 析构函数
    void print() const;

private:
    char* data;
};

String::String(const char* str) {
    if (str) {
        data = new char[strlen(str) + 1];
        strcpy(data, str);
    } else {
        data = new char[1];
        data[0] = '\0';
    }
}

String::String(const String& other) {
    data = new char[strlen(other.data) + 1];
    strcpy(data, other.data);
    std::cout << "拷贝构造函数被调用" << std::endl;
}

String::~String() {
    delete[] data;
}

void String::print() const {
    std::cout << data << std::endl;
}

int main() {
    String str1("Hello");
    String str2 = str1; // 调用拷贝构造函数
    str2.print();

    return 0;
}
```

在这个例子中，我们定义了一个简单的 `String` 类，用于管理字符串。这个类包括普通构造函数、拷贝构造函数和析构函数。

#### 关键点解析
1. **普通构造函数**

```cpp
String::String(const char* str) {
    if (str) {
        data = new char[strlen(str) + 1];
        strcpy(data, str);
    } else {
        data = new char[1];
        data[0] = '\0';
    }
}
```

普通构造函数用于初始化字符串。如果传入的字符串不为空，则分配足够的内存并复制字符串内容；否则，分配一个空字符串。

1. **拷贝构造函数**

```cpp
String::String(const String& other) {
    data = new char[strlen(other.data) + 1];
    strcpy(data, other.data);
    std::cout << "拷贝构造函数被调用" << std::endl;
}
```

拷贝构造函数用于创建一个新的 `String` 对象作为现有对象的副本。它首先分配足够的内存，然后复制源对象的字符串内容。在复制过程中，输出一条消息以指示拷贝构造函数被调用。

1. **析构函数**

```cpp
String::~String() {
    delete[] data;
}
```

析构函数用于释放分配的内存，防止内存泄漏。

#### 深入理解拷贝构造函数的用途
拷贝构造函数在许多情况下非常有用，特别是在处理动态内存分配时。通过定义拷贝构造函数，我们可以确保对象在复制过程中正确地管理资源，避免浅拷贝带来的问题。

##### 浅拷贝 vs 深拷贝
+ **浅拷贝**：
    - 默认情况下，C++编译器生成的拷贝构造函数执行浅拷贝，即逐位复制对象的成员变量。这对于简单的数据类型是可以的，但对于动态分配的内存会导致问题，因为两个对象将共享同一块内存。
    - 浅拷贝是指对对象的成员进行逐位复制（bitwise copy）。对于简单的数据类型（如基本类型和没有动态分配内存的类），浅拷贝是足够的。然而，对于包含指针成员或动态分配内存的类，浅拷贝可能会导致问题。
+ **深拷贝**：
    - 深拷贝需要显式定义拷贝构造函数，确保每个对象都有自己的独立副本。这样可以避免多个对象共享同一块内存，从而防止潜在的内存管理问题。
    - 深拷贝是指不仅复制对象的成员，还要复制指针所指向的内存。这样，每个对象都有自己独立的内存空间，互不干扰。

#### 拷贝构造函数的调用场景
1. **以值传递的方式传递对象**

```cpp
void function(String str) {
    str.print();
}

int main() {
    String str1("Hello");
    function(str1); // 调用拷贝构造函数
    return 0;
}
```

2. **从函数返回对象**

```cpp
String createString() {
    String str("Hello");
    return str; // 调用拷贝构造函数
}

int main() {
    String str2 = createString();
    str2.print();
    return 0;
}
```

3. **对象初始化**

```cpp
int main() {
    String str1("Hello");
    String str2 = str1; // 调用拷贝构造函数
    str2.print();
    return 0;
}
```

## 移动构造函数
移动构造函数用于从一个临时对象（右值）中“移动”资源，而不是复制它们。它的参数是一个右值引用。

```cpp
class MyClass {
public:
    MyClass(MyClass&& other) noexcept : x(other.x), y(other.y) {
        other.x = 0;
        other.y = 0;
        // 移动构造函数
    }
private:
    int x, y;
};
```

## 委托构造函数
委托构造函数允许一个构造函数调用另一个构造函数。这可以减少代码重复。

```cpp
class MyClass {
public:
    MyClass() : MyClass(0, 0) {
        // 委托构造函数
    }
    MyClass(int a, int b) : x(a), y(b) {
        // 实际的初始化逻辑
    }
private:
    int x, y;
};
```

## 构造函数的初始化顺序
构造函数的成员初始化列表按照成员变量在类中声明的顺序进行初始化，而不是在初始化列表中的顺序。

```cpp
class MyClass {
public:
    MyClass(int a, int b) : y(b), x(a) {
        // x 和 y 的初始化顺序是 x 然后 y
    }
private:
    int x, y;
};
```

## 显式构造函数
使用 `explicit` 关键字用于修饰构造函数，以防止编译器在某些情况下进行隐式类型转换。它主要用于避免意外的隐式转换和单参数构造函数的自动调用，从而增强代码的安全性和可读性。

```cpp
class MyClass {
public:
    explicit MyClass(int x) {
        // 显式构造函数
    }
};
```



#### 隐式转换
当一个类具有单参数构造函数时，编译器可能会使用该构造函数进行隐式类型转换。例如：

```cpp
class MyClass {
public:
    MyClass(int x) {
        value = x;
    }
private:
    int value;
};

void func(MyClass obj) {
    // do something with obj
}

int main() {
    func(42); // 隐式转换：int 被转换为 MyClass
    return 0;
}
```

在上面的代码中，整数 `42` 被隐式转换为 `MyClass` 对象。这种隐式转换有时可能会导致意外的行为。

#### 使用 `explicit` 关键字
为了防止这种隐式转换，可以使用 `explicit` 关键字：

```cpp
class MyClass {
public:
    explicit MyClass(int x) {
        value = x;
    }
private:
    int value;
};

void func(MyClass obj) {
    // do something with obj
}

int main() {
    // func(42); // 编译错误：不能隐式转换
    func(MyClass(42)); // 必须显式转换
    return 0;
}
```

在这个例子中，加上 `explicit` 关键字后，`func(42)` 将导致编译错误，因为编译器不再允许隐式转换。必须显式创建 `MyClass` 对象，如 `func(MyClass(42))`。

#### 详细示例
让我们看一个更详细的示例，展示 `explicit` 关键字如何影响代码行为：

```cpp
#include <iostream>

class Complex {
public:
    explicit Complex(double r, double i = 0.0) : re(r), im(i) {}

    void display() const {
        std::cout << "Complex number: " << re << " + " << im << "i" << std::endl;
    }

private:
    double re, im;
};

void printComplex(const Complex& c) {
    c.display();
}

int main() {
    Complex c1(3.0, 4.0);
    c1.display();

    // Complex c2 = 5.0; // 编译错误：不能隐式转换
    Complex c2(5.0); // 必须显式转换
    c2.display();

    // printComplex(6.0); // 编译错误：不能隐式转换
    printComplex(Complex(6.0)); // 必须显式转换

    return 0;
}
```

在这个示例中，`Complex` 类的构造函数被 `explicit` 修饰，这样可以防止 `double` 类型隐式转换为 `Complex` 对象。所有的转换必须显式进行，确保代码的意图更加明确。

#### 使用 `explicit` 的好处
1. **避免意外的隐式转换**：防止编译器进行不必要的隐式转换，减少潜在的错误。
2. **提高代码可读性和可维护性**：显式转换使得代码的意图更加清晰，便于理解和维护。
3. **增强类型安全性**：通过限制隐式转换，可以提高类型安全性，减少类型相关的错误。

### 析构函数
虽然析构函数不是构造函数，但它与构造函数密切相关。析构函数用于在对象销毁时执行清理操作。

```cpp
class MyClass {
public:
    ~MyClass() {
        // 析构函数
    }
};
```

### 禁止拷贝和移动
通过删除拷贝构造函数和拷贝赋值运算符，可以禁止对象的拷贝和移动。

```cpp
class MyClass {
public:
    MyClass(const MyClass&) = delete;
    MyClass& operator=(const MyClass&) = delete;
    MyClass(MyClass&&) = delete;
    MyClass& operator=(MyClass&&) = delete;
};
```

### 默认和删除的构造函数
可以显式地默认或删除构造函数。

```cpp
class MyClass {
public:
    MyClass() = default; // 显式默认构造函数
    MyClass(const MyClass&) = delete; // 显式删除拷贝构造函数
};
```

### 多态和虚构造函数
构造函数不能是虚函数，但可以通过其他方式实现多态行为，如使用工厂模式。

```cpp
class Base {
public:
    virtual ~Base() = default; // 虚析构函数
};

class Derived : public Base {
public:
    Derived() {
        // Derived 构造函数
    }
};
```

