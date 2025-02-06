---
# 基本信息
title: cmake  学习笔记
date: 2024/12/18
tags: [cpp, 计算机, cmake]
categories: [cpp]
description: cmkae 学习笔记
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/undefinedokEUIAAAeWU6AEzyCfDlt963F0IAYhAgNpijCt~tplv-dy-aweme-images%3Aq75.webp
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/undefinedokEUIAAAeWU6AEzyCfDlt963F0IAYhAgNpijCt~tplv-dy-aweme-images%3Aq75.webp
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:   cmkae 学习笔记 # 必选
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
type: tech # tech/story篇
---



> [菜鸟教程](https://www.runoob.com/cmake/cmake-tutorial.html)
>
> [CMakeTutorialCN](https://github.com/shendeguize/CMakeTutorialCN?tab=readme-ov-file#%E7%9B%AE%E5%BD%95)

# 1. CMake 简介

CMake  是一个开源的跨平台自动化构建工具，优点包括：跨平台支持、简化配置、自动化构建、灵活性。

其基本工作流程，如下图：

![image-20241218190432018](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/undefinedimage-20241218190432018.png)

1. 编写 CMakeList.txt 文件：定义项目的构建规则和依赖关系
2. 生成构建文件
3. 执行构建



# 2. CMake 基础

## CMakeLists.txt

CMakeLists.txt 是 CMake 的配置文件，用于定义项目的构建规则、依赖关系、编译选项等。每个 CMake可以有一个或多个该文件。

## 文件结构和基本语法

常见指令：

1. 指定 CMake 的最低版本要求 `cmake_minimum_required(VERSION 3.10)`

2. 定义项目名称和使用的编程语言 `project(MyProject CXX)`

3. 指定要生成的可执行文件和其源文件 `add_executable(<target> <source_files> ...)`

4. 创建一个库（静态库或者动态库）及其源文件`add_library(<target> <source_files>...)`

5. 链接目标文件与其他库`target_link_libraries(<target> <libraries>...)`

6. 添加头文件搜索路径`include_directories(<dirs>...)`，例如`include_directories(${PROJECT_SOURCE_DIR}/include)`

7. 设置变量的值`set(<variable><value>)...`，如`set(CMAKE_CXX_STANDARD 11)`

8. 安装规则:

   ```cmake
   install(TARGETS target1 [target2 ...]
           [RUNTIME DESTINATION dir]
           [LIBRARY DESTINATION dir]
           [ARCHIVE DESTINATION dir]
           [INCLUDES DESTINATION [dir ...]]
           [PRIVATE_HEADER DESTINATION dir]
           [PUBLIC_HEADER DESTINATION dir])
   ```

   如：`install(TARGETS MyExecutable RUNTIME DESTINATION bin)`

9. 设置目标属性：

   ```cmake
   target_include_directories(TARGET target_name
                             [BEFORE | AFTER]
                             [SYSTEM] [PUBLIC | PRIVATE | INTERFACE]
                             [items1...])
   ```

   如：`target_include_directories(MyExecutable PRIVATE ${PROJECT_SOURCE_DIR}/include)`

10. 条件语句（if elseif endif）

11. 自定义命令

    ```cmake
    add_custom_command(
       TARGET target
       PRE_BUILD | PRE_LINK | POST_BUILD
       COMMAND command1 [ARGS] [WORKING_DIRECTORY dir]
       [COMMAND command2 [ARGS]]
       [DEPENDS [depend1 [depend2 ...]]]
       [COMMENT comment]
       [VERBATIM]
    )
    ```

    如：

    ```cmake
    add_custom_command(
       TARGET MyExecutable POST_BUILD
       COMMAND ${CMAKE_COMMAND} -E echo "Build completed."
    )
    ```

## 变量和缓存

CMake 使用变量来存储和传递信息，这些变量可以在 CMakeLists.txt 文件中定义和使用。变量分为普通变量和缓存变量。

### 变量的定义与使用

* 定义：`set (MY_VAR "Helle CMake")`
* 使用：`message(STATUS "Variable MY_VAR is ${MY_VAR}")`

### 缓存变量

缓存变量存储在 CMake 的缓存文件中，用户可以在CMAke配置是修改这些值、缓存变量通常用于用户输入的设置，例如编译选项和路径。

* 定义：`set(MY_CACHE_VAR "DefaultValue" CACHE STRING "A cache variable")`
* 使用：`message(STATUS "Cache variable MY_CACHE_VAR is ${MY_CACHE_VAR}")`

##  查找库和包

CMake 通过 `find_package()`指令自动检测和配置外部库和包。常用于系统安装的库和第三方库。

* 基本用法：

  ```cmake
  find_package(Boost REQUIRED)
  ```

* 指定版本：

  ```cmake
  find_package(Boost 1.70 REQUIRED)
  ```

* 查找库并指定路径：

  ```cmake
  find_package(OpenCV REQUIRED PATHS /path/to/opencv)
  ```

* 使用查找到的库：

  ```cmake
  target_link_libraries(MyExcutable Boost::Boost)
  ```

* 设置包含目录和链接目录

  ```cmake
  inlude_directories(${Boost_INCLUDE_DIRS})
  link_directories(${Boost_LIBRART_DIRS})
  ```

下面是一个使用第三方库的实例：

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject CXX)

# 查找 Boost 库
find_package(Boost REQUIRED)

# 添加源文件
add_executable(MyExecutable main.cpp)
cmake
# 链接 Boost 库
target_link_libraries(MyExecutable Boost::Boost)
```



# 3. CMake 构建流程

1. 创建构建目录：保持源代码目录整洁，如创建`build`
2. 使用CMake生成构建文件：配置项目并生成适合执行的构建文件 `cmake ..`
3. 编译和构造：使用生成好的构建文件执行编译和构建 `make`
4. 清理构建文件：删除中间文件和目标文件
5. 重新配置和构建：处理项目设置的更改

![image-20241218211356800](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/undefinedimage-20241218211356800.png)

# 4. 构建实例

```tex
MyProject/
├── CMakeLists.txt
├── src/
│   ├── main.cpp
│   └── mylib.cpp
└── include/
    └── mylib.h
```

1. 创建 CMakeLists.txt

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   
   project(MyProject VERSION 1.0)
   
   set(CMAKE_CXX_STANDARD 11)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   
   # 设置头文件搜索目录
   include_directories(${PROJECT_SOURCE_DIR}/include) 
   
   # 添加源文件
   add_library(MyLib src/mylib.cpp) 	# 创建一个库目标 MyLib
   add_executable(MyExecutable src/main.cpp)	 #创建一个可执行文件目标 MyExecutable
   
   # 链接库到可执行文件
   target_link_libraries(MyExecutable MyLib)
   ```

2. 创建构建目录

   ```bash
   mkdir build && cd build
   ```

3. 配置项目

   在构建目录(build)使用CMake构建醒目，这将生成适合平台的构建文件（如 Makefile）

   ```bash
   cmake ..
   ```

   * cmake ..：指向源代码目录，即包含 CMakeLists.txt 文件的目录。CMake 将读取 CMakeLists.txt 文件并生成构建系统文件。

4. 编译项目

   使用生成的构建系统文件编译项目。根据生成的构建文件系统，使用相应的构建命令。

   ```bash
   make
   ```

   * make：编译项目并生成可执行文件 MyExecutable

5. 运行可执行文件

   ```bash
   ./MyExecutable
   ```

6. 清理构建文件

   用于删除生成的中间文件和目标文件

   ```bash
   make clean
   ```

   
