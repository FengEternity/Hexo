---
title: LeetCode3175. 找到连续赢 K 场比赛的第一位玩家(回溯 贪心 模拟)
date: 2024/10/24
tags:
  - cpp
  - 计算机
  - leetcode
  - 秋招
  - 算法
categories:
  - cpp
  - 题解
description: LeetCode3175. 找到连续赢 K 场比赛的第一位玩家(回溯 贪心 模拟)
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241024171628.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241024171628.png
poster:
  topic: 
  headline: LeetCode3175. 找到连续赢 K 场比赛的第一位玩家(回溯 贪心 模拟)
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

> 1024 程序员节快乐！

今天也是坚持每日一题的一天，题目如下：[3175. 找到连续赢 K 场比赛的第一位玩家](https://leetcode.cn/problems/find-the-first-player-to-win-k-games-in-a-row/?envType=daily-question&envId=2024-10-24)：
![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241024172953.png)

# 回溯求解

拿到这个题目，我一下子就想到了暴力回溯求解，还沾沾自喜，“小样，我一眼看到了你的本质”。回溯的思想其实就是递归的模拟每一场对战，直到某个选手达到连续胜利 `k`次，具体做法如下：
1. 记录当前胜者和胜利次数。
2. 每次比较当前胜者与下一个挑战者，更新胜者和胜利次数。
3. 当胜者连续胜利次数达到 `k`，返回该选手。

代码示例：
```C
class Solution {
public:
    void backTracking(std::vector<int>& nums, int k, int& curr) {
        int n = nums.size();
        while (curr < k) {
            if (nums[0] > nums[1]) {
                curr++;
                int temp = nums[1];
                for (int i = 1; i < n - 1; i++) {
                    nums[i] = nums[i + 1];
                }
                nums[n - 1] = temp;
            } else {
                curr = 1;
                int temp = nums[0];
                for (int i = 0; i < n - 1; i++) {
                    nums[i] = nums[i + 1];
                }
                nums[n - 1] = temp;
            }
        }
    }

    int findWinningPlayer(std::vector<int>& skills, int k) {
        std::vector<int> nums(skills);
        int curr = 0;
        backTracking(nums, k, curr);

        int resultNum = nums[0];
        for (int i = 0; i < skills.size(); i++) {
            if (skills[i] == resultNum) {
                return i; // 返回索引
            }
        }
        return -1;
    }
};
```

这个算法在最坏情况下，需要循环 `k` 次，并且每次循环都涉及到数组元素的移动操作，时间复杂度大约是 $O(k×n)$，其中  $n$ 是选手数量。

## 回溯算法的优缺点

**优点**：
- **全面性**：回溯通过递归遍历所有可能的状态，可以找到符合条件的解，适合组合、排列、路径等问题。
- **简洁性**：使用递归结构，代码简洁易读，逻辑直观。
- **易于实现剪枝**：可以在不满足条件时提前回溯，避免不必要的计算。

**缺点**：
- **时间复杂度高**：回溯往往需要遍历所有可能的状态，时间复杂度可能是指数级别$O(2^n)$ 或 $O(n!)$。
- **空间复杂度高**：递归调用占用栈空间，可能导致栈溢出，特别是在深度较大时。
- **不适合大规模问题**：回溯是暴力搜索，对大规模输入的性能较差，通常需要结合其他优化策略。

## 适用场景

回溯算法本质上还是一种暴力搜索，但是有一些场景却必须使用回溯，如下：

- **组合与排列问题**：求子集、组合总和、全排列等。
- **路径问题**：如迷宫、数独、八皇后问题等。
- **图的遍历**：深度优先搜索中的路径问题。


而在这道题目中，为什么不适合呢？

1. 问题本质是状态的持续更新，而非多路径选择
	这个问题的核心是模拟选手对战，最终确定能连续胜利 `k` 次的选手。每次对战结果是确定的，胜负只有一个结果，不需要遍历多种可能性。
2. 无需遍历所有状态
	回溯算法往往用于探索所有可能路径，而这个问题只需要一次遍历就可以找到胜者。在每次胜负比较后，只需更新当前胜者和胜利次数，不需要回退到先前状态。
3. 回溯会增加不必要的复杂度
	使用回溯将导致额外的递归调用和栈空间占用，而该问题可以通过一次线性遍历 $O(n)$ 解决。因此，回溯在这里只会增加时间和空间开销。

# 优化解法：使用贪心（模拟）算法

对于该问题，贪心算法更为适用。贪心算法的策略是每次选择当前对战的胜者，并更新其连胜次数。如果某个选手达到 `k` 次连续胜利，就立即返回。

具体实现代码如下：

```C
int findWinningPlayer(std::vector<int>& skills, int k) {
    int n = skills.size();
    int winner = skills[0];
    int curr = 0;

    for (int i = 1; i < n; ++i) {
        if (winner > skills[i]) {
            curr++;
        } else {
            winner = skills[i];
            curr = 1;
        }
        if (curr == k) {
            return std::find(skills.begin(), skills.end(), winner) - skills.begin();
        }
    }
    return std::find(skills.begin(), skills.end(), winner) - skills.begin();
}

```

**解释**：

- 初始时，假定 `skills[0]` 为当前胜者 `winner`，连胜次数 `curr` 为 0。
- 遍历 `skills` 数组，比较 `winner` 和当前挑战者 `skills[i]`：
    - 如果 `winner` 比挑战者强，增加 `curr`。
    - 如果挑战者胜出，则更新 `winner` 并重置 `curr`。
- 当 `curr` 达到 `k` 时，返回 `winner` 的索引。
- 如果遍历完所有选手还未达到 `k` 连胜，则返回最后的胜者。

## 优化分析

**时间复杂度**：$O(n)$，只需要一次遍历，找到符合条件的选手。相比回溯算法的指数级时间复杂度，这大大提高了效率。

**空间复杂度**：$O(1)$，只需要几个变量来跟踪当前胜者和连胜次数，不占用额外栈空间。

