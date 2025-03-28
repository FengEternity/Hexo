---
# 基本信息
title: 理解C++中的标准输出和标准错误输出问题
date: 2024/07/11
tags: [cpp, 计算机, debug]
categories: [C++]
description: 理解C++中的标准输出和标准错误输出问题
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/202106111326352430.jpg
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  理解C++中的标准输出和标准错误输出问题 # 必选
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
---

# 问题描述

![image-20240711092552117](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711092552117.png)

如图，预期输出应该是，先输出“文件路径不存在”，再输出“请输入文件路径”，代码如下，

```C++
// 获取有效的文件路径
std::string getValidFilePath() {
    std::string filepath;
    while (true) {
        std::cout << "请输入文件路径: ";
        std::cin >> filepath;

        // 检查文件路径是否存在
        if (std::__fs::filesystem::exists(filepath)) {
            break;
        } else {
            std::cerr << "文件路径不存在: " << filepath << std::endl;
        }
    }
    return filepath;
}
```

# 问题分析

我愚蠢的问GPT，

![image-20240711092822851](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711092822851.png)

它的回复如下，

出现这种情况并不是因为 `std::cerr` 的输出速度比 `std::cout` 慢，而是因为 `std::cout` 和 `std::cerr` 的缓冲机制不同。

## 原因分析

- **`std::cout`** 是缓冲输出流，意味着它会在缓冲区满或者遇到换行符时才会刷新输出。
- **`std::cerr`** 是非缓冲输出流，意味着它会立即输出，不经过缓冲。

由于这两种流的缓冲机制不同，它们的输出顺序可能会出现混乱，特别是在快速交替使用时。

## 解决方法


### 尝试一
为了确保 `std::cout` 和 `std::cerr` 的输出顺序一致，可以在每次使用 `std::cout` 和 `std::cerr` 后立即刷新缓冲区。你可以通过调用 `std::flush` 或 `std::endl` 来实现。

给出代码如下，

```C++
std::string getValidFilePath() {
    std::string filepath;
    while (true) {
        std::cout << "请输入文件路径: ";
        std::cout.flush();  // 立即刷新缓冲区
        std::cin >> filepath;

        // 检查文件路径是否存在
        if (std::__fs::filesystem::exists(filepath)) {
            break;
        } else {
            std::cerr << "文件路径不存在: " << filepath << std::endl;
        }
    }
    return filepath;
}

```

我根据它的代码进行修改，效果如图，似乎好了一半？

![image-20240711093055888](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240711093055888.png)

### 尝试二
接着，他提出了新的方案，“为了确保 `std::cout` 和 `std::cerr` 的输出顺序一致，可以通过同步 `std::cout` 和 `std::cerr` 的缓冲区来解决这个问题。一个有效的方法是使用 `std::ios::sync_with_stdio(false)` 关闭 C++ 标准流与 C 标准流的同步，然后手动刷新缓冲区。”

然而，我觉得这种方法对程序的后续开发极为的不友好，并没有采用。

### 最终版本（成功解决）

最后的解决方法是在，调用 `std::cout` 和 `std::cerr` 后，都立即调用`std::flush` 刷新缓冲区（尝试一中只在 `std::cout` 后调用）。

```C++
std::string getValidFilePath() {
    std::string filepath;
    while (true) {
        std::cout << "请输入文件路径: ";
        std::cout.flush();  // 立即刷新缓冲区
        std::cin >> filepath;

        // 检查文件路径是否存在
        if (std::filesystem::exists(filepath)) {
            break;
        } else {
            std::cout << "文件路径不存在: " << filepath << std::endl;
            std::cout.flush(); // 立即刷新缓冲区
        }
    }
    return filepath;
}
```

