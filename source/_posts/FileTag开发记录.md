%% ---
# 基本信息
title: FileTag 开发记录、源码分析（CMakeLists.txt main.cpp）
date: 2024/07/17
tags: [C++, 项目开发]
categories: [项目]
description: 
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  FileTag 开发记录、源码分析 # 必选
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
type: story # tech/story
--- %%

# CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.10)
project(FileTag)

set(CMAKE_CXX_STANDARD 17)

# 启用自动生成MOC文件
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# 查找Qt6包
set(CMAKE_PREFIX_PATH "/opt/homebrew/Cellar/qt/6.7.0_1/lib/cmake")

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Network)

# 添加Qt6模块
set(QT_LIBRARIES Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Network)

# 将 main.cpp、file_tag_system.cpp 和 tag_manager.cpp 编译为可执行文件 FileTag
add_executable(FileTag
        src/main.cpp
        src/file_tag_system.cpp
        src/tag_manager.cpp
        src/user_manager.cpp
        src/file_tag_system.h
        src/tag_manager.h
        src/user_manager.h
        src/mainwindow.cpp
        src/mainwindow.h
        resources/resources.qrc
        src/MultiSelectDialog.cpp
        src/MultiSelectDialog.h
        src/Logger.cpp
        src/Logger.h
        src/FileProcessor.cpp
        src/FileProcessor.h
)

# 链接Qt6库
target_link_libraries(FileTag ${QT_LIBRARIES})

# 设置包含目录
target_include_directories(FileTag PRIVATE ${CMAKE_SOURCE_DIR}/src)

# 添加自定义目标 clean-all，用于清理生成的文件
add_custom_target(clean-all
        COMMAND ${CMAKE_COMMAND} -P ${CMAKE_BINARY_DIR}/cmake_clean.cmake
        COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}
)

# 创建 cmake_clean.cmake 文件，用于清理生成目录
file(WRITE ${CMAKE_BINARY_DIR}/cmake_clean.cmake "file(REMOVE_RECURSE ${CMAKE_BINARY_DIR})")

```

主要看这一块的代码，

```cmake
add_executable(FileTag ...)：将指定的源文件编译为可执行文件FileTag。这里列出了所有的源文件和头文件。
```

#### 项目结构

- `src/`：源代码目录，包含所有的源文件和头文件。
  - `main.cpp`：程序入口。
  - `file_tag_system.cpp` 和 `file_tag_system.h`：文件标签系统的实现。
  - `tag_manager.cpp` 和 `tag_manager.h`：标签管理器的实现。
  - `user_manager.cpp` 和 `user_manager.h`：用户管理器的实现。
  - `mainwindow.cpp` 和 `mainwindow.h`：主窗口的实现。
  - `MultiSelectDialog.cpp` 和 `MultiSelectDialog.h`：多选对话框的实现。
  - `Logger.cpp` 和 `Logger.h`：日志记录器的实现。
  - `FileProcessor.cpp` 和 `FileProcessor.h`：文件处理器的实现。
  
- `resources/`：资源文件目录，包含Qt资源文件`resources.qrc`。



# main.cpp

这部分是一个使用 Qt 框架编写的 C++入口代码，

```c++
#include <QApplication>
#include <QFile>
#include <QMainWindow>
#include "mainwindow.h"
#include "Logger.h"

void applyStyleSheet(QApplication &app) {
    QFile file(":/stylesheet.qss");
    if (!file.exists()) {
        // qWarning("未找到样式表");
        Logger::instance().log("未找到样式表");
        return;
    }
    if (file.open(QFile::ReadOnly | QFile::Text)) {
        Logger::instance().log("加载样式表");
        QTextStream stream(&file);
        QString styleSheet = stream.readAll();
        app.setStyleSheet(styleSheet);
        file.close();
    } else {
        // qWarning("无法加载样式表");
        Logger::instance().log("无法加载样式表");
    }
}

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    applyStyleSheet(app);

    MainWindow w;
    w.show();
    return app.exec();
}

```

## 头文件

## 应用样式表的函数

```c
void applyStyleSheet(QApplication &app) { 
  	// 接受一个 QApplication 对象的引用 app 作为参数
    QFile file(":/stylesheet.qss"); //创建一个 QFile 对象 file，指向资源文件 :/stylesheet.qss
    if (!file.exists()) {
        Logger::instance().log("未找到样式表");
        return;
    }
    if (file.open(QFile::ReadOnly | QFile::Text)) {
      /*
      尝试以只读和文本模式打开文件：
				QFile::ReadOnly：以只读模式打开文件。
				QFile::Text：以文本模式打开文件（处理换行符）。
      */
        Logger::instance().log("加载样式表");
        QTextStream stream(&file); //创建一个 QTextStream 对象 stream，用于读取文件内容
        QString styleSheet = stream.readAll(); //读取文件的所有内容到一个 QString 对象 styleSheet 中
        app.setStyleSheet(styleSheet); // 将读取到的样式表应用到 QApplication 对象
        file.close();
    } else {
        Logger::instance().log("无法加载样式表");
    }
}

```

相关代码的含义与功能都已经写在注释中，这里分析一下这段代码中的相关知识。

### 引用

在C++中，引用（reference）是一种轻量级的对象别名，**允许函数直接操作传入的对象，而不是其副本**。在函数定义时，接受一个`QApplication`对象的引用有以下几个主要原因和作用：

#### 作用

1. 避免对象拷贝

​	如果函数接受的是对象的值（即传值），那么每次调用函数时，都会创建一个对象的副本。这不仅会增加内存开销，还会导致性能下降，特别是对于像`QApplication`这样可能包含大量数据和状态的对象。

2. 直接修改传入对象

​	通过引用传递，函数可以直接修改传入的`QApplication`对象的状态。在这段代码中，`applyStyleSheet`函数需要调用`app.setStyleSheet(styleSheet)`来设置应用程序的样式表。如果传递的是对象的副本，那么修改副本并不会影响原始的`QApplication`对象。

3. 保持对象的一致性

​	在Qt应用程序中，`QApplication`对象通常是全局唯一的，负责管理应用程序的控制流和主要设置。通过引用传递，可以确保所有对`QApplication`对象的修改都是对同一个对象进行的，从而保持应用程序状态的一致性。

4. 提高效率

​	引用传递比传值更高效，因为它避免了对象的拷贝操作。特别是对于大型对象或复杂对象（如`QApplication`），引用传递能够显著提高函数调用的效率。

#### 弊端

当然，引用也有它的弊端和注意事项，

1. 可能导致悬空引用

​	如果引用的对象在引用的生命周期内被销毁或超出作用域，那么引用将变成悬空引用（dangling reference），使用悬空引用会导致未定义行为。

```cpp
int& getReference() {
    int x = 42;
    return x; // 返回局部变量的引用，x在函数结束后被销毁
}

int main() {
    int& ref = getReference();
    // ref 是悬空引用，使用它会导致未定义行为
}
```

2. 不能重新绑定

​	一旦引用被初始化，就不能再重新绑定到另一个对象。这与指针不同，指针可以在其生命周期内指向不同的对象。

```cpp
int a = 10;
int b = 20;
int& ref = a;
ref = b; // 这是将 b 的值赋给 a，而不是重新绑定 ref 到 b
```

3. 不能为 `null`

​	引用必须绑定到合法的对象，不能为 `null`。这与指针不同，指针可以被赋值为 `nullptr` 表示空指针。

```cpp
int* ptr = nullptr; // 合法
int& ref = *ptr; // 非法，引用不能为 null
```

4. 可能隐藏性能问题

​	引用的使用有时会隐藏性能问题，特别是在传递大型对象时。虽然引用避免了对象拷贝，但如果引用的对象位于不同的内存区域（例如，在缓存之外），仍可能导致性能问题。

5. 可能导致代码不易理解

​	引用的使用有时会使代码变得不易理解，特别是对于初学者。引用的隐式行为（例如，引用的操作实际上是对原始对象的操作）可能导致代码的意图不明确。

6. 需要谨慎使用常量引用

​	虽然常量引用（`const` 引用）可以防止修改引用的对象，但在多线程环境中，如果另一个线程修改了引用的对象，仍可能导致未定义行为。

```cpp
const int& ref = someSharedVariable;
// 如果另一个线程修改了 someSharedVariable，ref 的值可能会不一致
```



# 主函数

```c++
int main(int argc, char *argv[]) {
    QApplication app(argc, argv); // 创建一个QApplication对象，用于管理应用程序的控制流和主要设置
    applyStyleSheet(app);

    MainWindow w; // 创建一个自定义的主窗口对象
    w.show();
    return app.exec(); // 进入应用程序的事件循环，等待用户交互
}

```

## app.exec()

- `app.exec()` 启动Qt的事件循环，进入主事件循环后，应用程序开始处理用户输入和其他事件。
- `app.exec()` 会阻塞，直到 `QApplication` 对象发出 `quit()` 信号，通常是在用户关闭所有窗口或调用 `QApplication::quit()` 时。
- `main` 函数返回 `app.exec()` 的返回值，通常是应用程序的退出状态。

### 事件循环的作用

在Qt应用程序中，进入事件循环（或称用户循环）并不是一个简单的无限循环，而是一个复杂的过程，涉及到事件的处理、资源的管理和应用程序的退出。因此，`QApplication::exec()` 函数启动这个事件循环，**并且会一直运行**，直到应用程序退出。

### `QApplication::exec()` 返回值的意义

当事件循环结束时，`QApplication::exec()` 返回一个整数值，这个值通常用于指示应用程序的退出状态。这个退出状态可以被操作系统或其他程序检测到，用于判断应用程序是否正常退出。

### 为什么需要返回值

1. **指示退出状态**：返回值通常用于指示应用程序的退出状态。例如，返回0通常表示应用程序正常退出，而非0值可能表示某种错误或异常退出。
2. **与操作系统交互**：操作系统可以通过检查应用程序的返回值来判断应用程序的退出状态。这在脚本或其他自动化工具中非常有用。
3. **错误处理**：返回值可以用于错误处理和调试。例如，如果应用程序因某种错误而退出，返回一个特定的错误码可以帮助开发者或系统管理员诊断问题。
