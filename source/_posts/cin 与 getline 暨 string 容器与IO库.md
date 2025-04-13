---
title: cin 与 getline 暨 string 容器与IO库
date: 2024/10/12
tags:
  - cpp
  - 计算机
  - debug
categories: [技术学习]
description: cin 与 getline 暨 string 容器与IO库
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241020153002.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241020153002.png
poster:
  headline: cin 与 getline 暨 string 容器与IO库
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: 
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

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241014224930.png)

> 值得一提的是，上面这是一个典型的菱形继承问题，这种继承方式主要有数据冗余和二义性的问题，由于最底层的派生类继承了两个基类，同时这两个基类有继承的是一个基类，故而会造成最顶部基类的两次调用，会造成数据冗余及二义性问题。
> 
> **解决方案：**
> 	使用虚继承，即在 istream 类和 ostream 类继承 ios 类时，使用 virtual 关键字，如 class istream : virtual public ios（这里只是为了解释虚继承，真是的代码大概率不是这么写的）。
> **虚继承的原理：**
> 	原理在于引入了虚基类表来管理基类的实例。具体来说，
> 		1. 虚基类表：每个虚继承的类会包含一个指向虚基类表的指针。虚基类表中包含了指向虚基类的指针；
> 		2. 共享基类实例：当派生类通过虚继承来继承基类时，最终派生类会共享一个基类实例，而不是每个派生路径都包含一个独立的基类实例。
当然！以下是关于C++ I/O标准库的详细扩展内容：

## IO类

C++的I/O类是标准库中处理输入输出操作的核心部分。主要的I/O类包括：

1. **istream**：用于输入操作的抽象基类。常见的派生类有 `ifstream`（文件输入流）和 `istringstream`（字符串输入流）。
2. **ostream**：用于输出操作的抽象基类。常见的派生类有 `ofstream`（文件输出流）和 `ostringstream`（字符串输出流）。
3. **iostream**：继承自 `istream` 和 `ostream`，用于同时处理输入和输出操作。常见的派生类有 `fstream`（文件输入输出流）和 `stringstream`（字符串输入输出流）。

这些类提供了丰富的成员函数和运算符重载，使得输入输出操作变得简洁和高效。例如，`<<` 和 `>>` 运算符分别用于输出和输入操作。

### 常用成员函数和运算符

- **`<<` 运算符**：用于输出数据到流中。
  ```cpp
  std::cout << "Hello, world!" << std::endl;
  ```
- **`>>` 运算符**：用于从流中输入数据。
  ```cpp
  int x;
  std::cin >> x;
  ```
- **`getline` 函数**：用于读取一整行数据。
  ```cpp
  std::string line;
  std::getline(std::cin, line);
  ```

## 文件输入输出

文件输入输出是C++中一个重要的功能，通过 `fstream` 类及其派生类 `ifstream` 和 `ofstream` 来实现文件的读写操作。

### ifstream 类

`ifstream` 用于从文件中读取数据。常用操作包括打开文件、读取数据和关闭文件。

```cpp
#include <fstream>
#include <iostream>

int main() {
    std::ifstream inFile("example.txt");
    if (!inFile) {
        std::cerr << "Unable to open file";
        return 1;
    }

    std::string line;
    while (std::getline(inFile, line)) {
        std::cout << line << std::endl;
    }

    inFile.close();
    return 0;
}
```

### ofstream 类

`ofstream` 用于向文件中写入数据。常用操作包括打开文件、写入数据和关闭文件。

```cpp
#include <fstream>
#include <iostream>

int main() {
    std::ofstream outFile("example.txt");
    if (!outFile) {
        std::cerr << "Unable to open file";
        return 1;
    }

    outFile << "Hello, world!" << std::endl;
    outFile.close();
    return 0;
}
```

### fstream 类

`fstream` 继承自 `ifstream` 和 `ofstream`，用于同时进行文件的读写操作。

```cpp
#include <fstream>
#include <iostream>

int main() {
    std::fstream file("example.txt", std::ios::in | std::ios::out | std::ios::app);
    if (!file) {
        std::cerr << "Unable to open file";
        return 1;
    }

    file << "Appending some text." << std::endl;

    file.seekg(0); // 回到文件开始位置
    std::string line;
    while (std::getline(file, line)) {
        std::cout << line << std::endl;
    }

    file.close();
    return 0;
}
```

## string 流

`stringstream` 类提供了在内存中操作字符串的功能，类似于文件流，但操作对象是字符串。

### istringstream 类

`istringstream` 用于从字符串中读取数据。

```cpp
#include <sstream>
#include <iostream>

int main() {
    std::string data = "123 456 789";
    std::istringstream iss(data);

    int a, b, c;
    iss >> a >> b >> c;

    std::cout << a << " " << b << " " << c << std::endl;
    return 0;
}
```

### ostringstream 类

`ostringstream` 用于向字符串中写入数据。

```cpp
#include <sstream>
#include <iostream>

int main() {
    std::ostringstream oss;
    oss << "Hello, " << "world!" << std::endl;

    std::string result = oss.str();
    std::cout << result;
    return 0;
}
```

### stringstream 类

`stringstream` 继承自 `istringstream` 和 `ostringstream`，用于同时进行字符串的读写操作。

```cpp
#include <sstream>
#include <iostream>

int main() {
    std::stringstream ss;
    ss << 123 << " " << 456 << " " << 789;

    int a, b, c;
    ss >> a >> b >> c;

    std::cout << a << " " << b << " " << c << std::endl;
    return 0;
}
```

# 输入输出缓冲区（I/O Buffer）

输入输出缓冲区（I/O Buffer）是计算机系统中用于临时存储数据的区域，以便在输入输出操作时提高效率。缓冲区的主要目的是减少I/O操作的频率和提高系统性能。以下是输入输出缓冲区的详细解释：

## 输入输出缓冲区的概念

缓冲区是内存中的一块区域，用于临时存储数据。在输入输出操作中，缓冲区在数据传输的源和目的地之间充当中介。C++标准库中的输入输出流类（如 `iostream`、`ifstream`、`ofstream` 等）都使用缓冲区来管理数据的读写操作。

### 输入缓冲区

输入缓冲区用于存储从输入设备（如键盘、文件、网络等）读取的数据。在程序请求数据之前，数据已经被预先读入缓冲区，从而减少了实际读取操作的次数，提高了数据读取的效率。

### 输出缓冲区

输出缓冲区用于存储即将写入输出设备（如显示器、文件、网络等）的数据。数据首先被写入缓冲区，当缓冲区满时，或者在某些特定条件下（如调用 `flush` 函数或程序结束时），数据才会被实际写入输出设备。

## 缓冲区的工作机制

1. **输入缓冲区**：
   - 当程序请求输入数据时，数据首先从输入设备读入缓冲区。
   - 程序从缓冲区中读取数据，而不是直接从输入设备读取。
   - 当缓冲区中的数据被读取完毕时，再从输入设备读取新的数据填充缓冲区。

2. **输出缓冲区**：
   - 当程序请求输出数据时，数据首先被写入缓冲区。
   - 当缓冲区满时，或者程序显式地请求刷新缓冲区，数据才会被实际写入输出设备。
   - 这减少了对输出设备的频繁访问，从而提高了性能。

## 缓冲区的刷新

缓冲区的刷新（flush）是指将缓冲区中的数据强制写入输出设备。C++ 提供了多种方式来刷新输出缓冲区：

1. **自动刷新**：
   - 当缓冲区满时，系统会自动刷新缓冲区。
   - 当程序正常结束时，缓冲区也会自动刷新。

2. **手动刷新**：
   - 可以使用 `std::flush` 操作符来手动刷新缓冲区。
     ```cpp
     std::cout << "Hello, world!" << std::flush;
     ```
   - `std::endl` 操作符不仅会输出换行符，还会刷新缓冲区。
     ```cpp
     std::cout << "Hello, world!" << std::endl;
     ```

3. **显式刷新函数**：
   - 可以调用流对象的 `flush` 成员函数来刷新缓冲区。
     ```cpp
     std::cout.flush();
     ```

## 缓冲区的类型

C++ 中的缓冲区根据其刷新策略可以分为以下几种类型：

1. **全缓冲（Fully Buffered）**：
   - 数据在缓冲区满时才会被写入输出设备。文件输出流（如 `ofstream`）通常是全缓冲的。

2. **行缓冲（Line Buffered）**：
   - 数据在遇到换行符时会被刷新到输出设备。标准输出流（如 `std::cout`）通常是行缓冲的。

3. **无缓冲（Unbuffered）**：
   - 数据不会使用缓冲区，直接写入输出设备。标准错误流（如 `std::cerr`）通常是无缓冲的。
## 缓冲区的作用

1. **减少I/O操作的频率**：
    
    - I/O操作（如读取文件、写入文件、网络通信等）通常是相对较慢的操作，因为它们涉及与外部设备（如硬盘、网络等）的交互。每次I/O操作都可能导致系统调用和硬件访问，这些操作的开销较大。
    - 通过使用缓冲区，可以将多个小的I/O操作合并为一个大的I/O操作，从而减少系统调用的次数和硬件访问的频率，提高整体效率。
2. **提高数据传输效率**：
    
    - 缓冲区允许数据在内存中暂存，从而可以批量处理数据。批量处理数据比逐个处理每个数据项要高效得多，因为批量操作可以更好地利用CPU缓存和内存带宽。
3. **平滑数据流**：
    
    - 缓冲区可以平滑数据流，避免因数据传输速度不一致而导致的性能瓶颈。例如，网络数据传输速度可能不稳定，通过缓冲区可以暂存数据，避免程序等待数据到达。
4. **减少CPU等待时间**：
    
    - 在没有缓冲区的情况下，CPU可能需要频繁等待I/O操作完成，这会导致CPU资源的浪费。缓冲区可以在后台进行I/O操作，CPU可以继续执行其他任务，从而提高系统整体性能。

## 示例代码

以下是一个简单的示例，展示了缓冲区的使用和刷新：

```cpp
#include <iostream>
#include <fstream>

int main() {
    // 输出缓冲区示例
    std::cout << "This is a buffered output." << std::flush;
    // std::cout << "This is a buffered output." << std::endl; // 也会刷新缓冲区

    // 文件输出缓冲区示例
    std::ofstream outFile("example.txt");
    outFile << "Buffered file output.";
    outFile.flush(); // 强制刷新缓冲区，将数据写入文件

    return 0;
}
```

通过理解和合理使用输入输出缓冲区，可以显著提高程序的性能和效率。