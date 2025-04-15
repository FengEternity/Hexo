---

# 基本信息
## title: C++编译相关知识  
date: 2024/07/11  
tags: [cpp, 计算机]  
categories: [技术学习]  
description: C++编译相关知识  
# 封面  
cover: [https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220629231150_51a75.gif](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220629231150_51a75.gif)  
banner: [https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220629231150_51a75.gif](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220629231150_51a75.gif)  
poster:  # 海报（可选，全图封面卡片）  
  headline:  C++编译相关知识 # 必选  
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
# 编译流程
![](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711145639987.png)

预处理->编译->汇编->链接

## 静态链接和动态链接
对于外部库的链接，又分为静态链接和动态链接，区别如下

![](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711145830818.png)

读者可以把自己源代码编译后的目标文件（像上图的`main.cpp.obj`文件）想象成一个块不完整的拼图，对于外部库文件想象成拼图剩下的部分。

+ 对于静态链接来说，在最后的链接过程，相当于把两块拼图组成完成的“图片”，这个图片就是可执行程序（像上图的`my-app.exe`）；
+ 对于动态链接来说，这个过程不会将两块拼图完整的拼接在一起，而是给我们自己的“拼图”缺失的位置添加一个上下文信息（包括动态库的查找方式、内存地址等），程序运行的时候，会动态的加载这些库文件并执行这些外部动态库的程序代码等。

更为学术的定义与比较如下，

**静态链接**： 静态链接是在编译时将所有需要的库代码直接嵌入到可执行文件中。这意味着生成的可执行文件包含了所有的依赖代码，不需要在运行时加载额外的库。

+ **Windows**：`.lib`
+ **Unix/Linux**：`.a`（archive）

**动态链接**：动态链接是在运行时将库代码加载到内存中，并与可执行文件链接。这意味着生成的可执行文件在运行时依赖于外部的动态库（如Windows上的DLL或Unix/Linux上的.so文件）。

+ **Windows**：`.dll`（Dynamic Link Library）
+ **Unix/Linux**：`.so`（Shared Object）
+ **macOS**：`.dylib`（Dynamic Library）

以下是静态链接和动态链接的详细对比表格：

| 特性 | 静态链接 | 动态链接 |
| --- | --- | --- |
| **定义** | 在编译时将库代码嵌入到可执行文件中 | 在运行时将库代码加载到内存中并链接 |
| **独立性** | 生成的可执行文件是独立的，不依赖外部库 | 生成的可执行文件依赖于外部动态库 |
| **文件大小** | 较大 | 较小 |
| **内存使用** | 每个程序有独立的库代码 | 多个程序共享库代码 |
| **启动时间** | 较快 | 可能较慢（需要加载库） |
| **更新方式** | 需要重新编译整个程序 | 只需更新库文件 |
| **依赖管理** | 不依赖外部库 | 依赖于外部动态库 |
| **分发和部署** | 简单 | 复杂（需要确保库的存在和版本） |
| **性能** | 运行时性能较高 | 运行时性能可能略低 |
| **共享性** | 无法共享库代码 | 多个程序可以共享同一个动态库 |
| **磁盘空间** | 占用更多磁盘空间 | 占用较少磁盘空间 |
| **更新难度** | 更新库需要重新编译应用程序 | 更新库无需重新编译应用程序 |
| **适用场景** | 嵌入式系统、独立分发的应用程序 | 多个程序共享库、需要频繁更新库的应用 |


# 编译工具链
以下是一些常用的C++编译工具链及其特点：

### 1. GNU Compiler Collection (GCC)
**特点：**

+ **跨平台支持**：GCC支持多种操作系统，包括Linux、Windows（通过MinGW或Cygwin）、macOS等。
+ **开源**：GCC是自由软件基金会（FSF）维护的开源项目。
+ **优化**：提供多种优化选项，可以生成高效的机器代码。
+ **多语言支持**：除了C++，GCC还支持C、Fortran、Ada、Go等多种编程语言。

**常用命令：**

```bash
g++ -o my_program my_program.cpp
```

### 2. Clang/LLVM
**特点：**

+ **模块化设计**：Clang是LLVM项目的一部分，具有模块化和可扩展性。
+ **快速编译**：**Clang通常比GCC编译速度更快。**
+ **优质的错误和警告信息**：Clang提供的错误和警告信息更易于理解和调试。
+ **跨平台支持**：支持Linux、Windows、macOS等操作系统。

**常用命令：**

```bash
clang++ -o my_program my_program.cpp
```

### 3. Microsoft Visual C++ (MSVC)
**特点：**

+ **集成开发环境**：MSVC通常**与Visual Studio集成**，提供强大的IDE功能。
+ **Windows专用**：主要用于Windows平台的开发。
+ **优化和调试工具**：提供丰富的优化选项和调试工具，特别适合Windows应用程序的开发。
+ **标准库实现**：MSVC提供了一个高性能的C++标准库实现。

**常用命令：**

```bash
cl /EHsc my_program.cpp
```

### 4. Intel C++ Compiler (ICC)
**特点：**

+ **高性能优化**：特别针对Intel处理器进行优化，能够生成高度优化的机器代码。
+ **并行编程支持**：提供对并行编程模型的支持，如OpenMP和Intel TBB。
+ **跨平台支持**：支持Linux、Windows和macOS。

**常用命令：**

```bash
icc -o my_program my_program.cpp
```

### 5. MinGW (Minimalist GNU for Windows)
**特点：**

+ **GCC在Windows上的移植**：MinGW是GCC在Windows上的一个移植版本，允许在Windows上使用GCC编译器。
+ **轻量级**：比Cygwin更轻量，不依赖于POSIX兼容层。
+ **开源**：同样是开源项目。

**常用命令：**

```bash
g++ -o my_program.exe my_program.cpp
```

### 6. Cygwin
**特点：**

+ **POSIX兼容层**：提供一个POSIX兼容层，使得Unix/Linux程序可以在Windows上运行。
+ **包含GCC**：Cygwin包含了GCC编译器，可以在Windows上使用GCC。
+ **丰富的软件包**：Cygwin提供了大量的Unix/Linux工具和库。

**常用命令：**

```bash
g++ -o my_program my_program.cpp
```

### 7. Emscripten
**特点：**

+ **WebAssembly编译**：Emscripten可以将C++代码编译成WebAssembly，使得C++代码可以在浏览器中运行。
+ **基于LLVM**：Emscripten使用LLVM作为后端编译器。
+ **适用于Web开发**：非常适合将现有的C++代码库移植到Web平台。

**常用命令：**

```bash
emcc my_program.cpp -o my_program.html
```

### 8. ARM Compiler
**特点：**

+ **嵌入式系统**：专为ARM架构的嵌入式系统设计，广泛用于嵌入式开发。
+ **高效优化**：针对ARM处理器进行优化，生成高效的机器代码。
+ **集成开发环境**：通常与Keil或其他嵌入式开发IDE集成。

**常用命令：**

```bash
armcc -o my_program my_program.cpp
```

# 构建系统
随着项目工程越来越复杂，源代码文件越来越多，编译配置项根据场景的不同越来越复杂（例如，Debug模式和Release模式下编译参数不一样）的时候，依然通过直接调用这些命令的时候就会很复杂，我们需要编写大量复杂的命令行才能完成一个复杂项目的编译工作。基于这样的背景，我们诞生了构建系统（Build System）。

如何理解构建系统呢？如果把上一节介绍的编译工具链比作炒菜的铲子，把源代码、库文件比作食材，那么最原始的方式，就是人工使用铲子，先炒什么，再放什么调料，再炒什么，最终制作出一盘菜。而构建系统，可以理解为一个炒菜的机器人，它接收炒菜的**图纸文件**，只要启动以后，就会自己拿着锅铲摆弄食材来制作出一盘菜。当然，即使是炒菜机器人，底层依然用的锅铲和食材，只是炒菜的流程自动化、机器化了。也就是说，构建系统在底层依赖使用的是编译工具链，只是进行了一定的用户友好的抽象，并降低了项目编译的复杂度。

在不同的平台上，构建系统是不一样的。接下来我们就进一步介绍不同平台的构建系统。

### CMake
![](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711151946065.png)

**特点：**

+ **跨平台支持**：支持多种操作系统和编译器。
+ **生成器**：可以生成各种构建系统的配置文件，如Makefile、Ninja、Visual Studio项目等。
+ **模块化**：支持模块化配置，易于管理大型项目。

**常用命令：**

```bash
cmake .
make
```

**示例CMakeLists.txt：**

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 11)

add_executable(my_program main.cpp utils.cpp)
```

### Make
![](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711151927513.png)

**特点：**

+ **历史悠久**：Make是最早的构建工具之一，广泛用于Unix/Linux系统。
+ **Makefile**：通过编写Makefile来定义构建规则和依赖关系。
+ **灵活性**：非常灵活，可以用于几乎任何类型的项目，但需要手动管理依赖关系。

**常用命令：**

```bash
make
```

**示例Makefile：**

```makefile
all: my_program

my_program: main.o utils.o
    g++ -o my_program main.o utils.o

main.o: main.cpp
    g++ -c main.cpp

utils.o: utils.cpp
    g++ -c utils.cpp

clean:
    rm -
```



### MSBuild
![](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711151909863.png)

**特点：**

+ **集成开发环境**：与Visual Studio深度集成，适合Windows平台开发。
+ **XML配置文件**：使用XML格式的项目文件（.csproj、.vcxproj等）来定义构建过程。
+ **灵活性**：支持自定义任务和目标，适应各种构建需求。
+ **跨平台支持**：虽然主要用于Windows，MSBuild也可以在其他平台上运行（例如，通过.NET Core）。

**常用命令：**

```bash
msbuild my_project.vcxproj
```

**示例项目文件（.vcxproj）：**

```xml
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    <ClCompile Include="main.cpp" />
    <ClCompile Include="utils.cpp" />
  </ItemGroup>

  <PropertyGroup>
    <OutDir>.\bin\</OutDir>

    <IntDir>.\obj\</IntDir>

    <ConfigurationType>Application</ConfigurationType>

    <PlatformToolset>v142</PlatformToolset>

    <TargetName>my_program</TargetName>

  </PropertyGroup>

  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
</Project>

```



# 引用
> [C与C++常见编译工具链与构建系统简介](https://www.cnblogs.com/w4ngzhen/p/17695080.html)
>

