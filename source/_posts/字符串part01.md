---
title: 字符串part01
date: 2024/08/03
tags:
  - cpp
  - 计算机
  - leetcode
  - 秋招
  - 算法
categories:
  - cpp
  - 题解
description: 字符串part01
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240803111519.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240803111519.png
poster:
  topic: 
  headline: 字符串part01
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: true
topic: 计算机
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

# 344. 反转字符串【简单】

双指针秒了！

```C
class Solution {
public:
    void reverseString(vector<char>& s) {
        int leftIndex = 0;
        int rightIndex = s.size() - 1;

        while (leftIndex < rightIndex) {
            // 交换字符
            char tmp = s[leftIndex];
            s[leftIndex] = s[rightIndex];
            s[rightIndex] = tmp;

            // 移动指针
            leftIndex++;
            rightIndex--;
        }
    }
};
```

直接用自带的 reverse 函数……

```C
class Solution {
public:
    void reverseString(std::vector<char>& s) {
        std::reverse(s.begin(), s.end());
    }
};

```


