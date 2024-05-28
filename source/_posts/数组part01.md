---
# 基本信息
title: 数组part01
date: 2024/05/28/17/52
tags: [cpp, 计算机, leetcode, 秋招, 算法]
categories: [cpp, 题解]
description: 代数组part01
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/cpp.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/cpp.png
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  代码随想录刷题记录 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: 
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
type: tech # tech/story
---



# 数组理论基础

1. 数组是存放在连续内存空间上的相同类型数据的集合。

   ![image-20240522193029336](/Users/montylee/Library/Application Support/typora-user-images/image-20240522193029336.png)

* 数组下标都是从0开始的

* 数组内存空间的地址是连续的（**因为数组的在内存空间的地址是连续的，所以我们在删除或者增添元素的时候，就难免要移动其他元素的地址**）

2. 二维数组

   ![image-20240522193547234](/Users/montylee/Library/Application Support/typora-user-images/image-20240522193547234.png)

   不同语言内存管理不同，C++中二维数组是连续分布的，Java 不是。

# 704. 二分查找

[代码随想录](https://programmercarl.com/0704.二分查找.html#思路)

> 大家写二分法经常写乱，主要是因为**对区间的定义没有想清楚，区间的定义就是不变量**。要在二分查找的过程中，保持不变量，就是在while寻找中每一次边界的处理都要坚持根据区间的定义来操作，这就是**循环不变量**规则。~~*(不是很理解)*~~

## 第一种写法

定义 target 是在一个在左闭右闭的区间里，**也就是[left, right] （这个很重要非常重要）**。

* while (left <= right) 要使用 <= ，因为left == right是有意义的，所以使用 <=
* if (nums[middle] > target) right 要赋值为 middle - 1，因为当前这个nums[middle]一定不是target，那么接下来要查找的左区间结束下标位置就是 middle - 1

![image-20240524103229994](/Users/montylee/Library/Application Support/typora-user-images/image-20240524103229994.png)

## 第二种写法

target 是在一个在左闭右开的区间里，也就是**[left, right)**

```cpp
// 版本二
class Solution {
public:
    int search(vector<int>& nums, int target) {
        int left = 0;
        int right = nums.size(); // 定义target在左闭右开的区间里，即：[left, right)
        while (left < right) { // 因为left == right的时候，在[left, right)是无效的空间，所以使用 <
            int middle = left + ((right - left) >> 1);
            if (nums[middle] > target) {
                right = middle; // target 在左区间，在[left, middle)中
            } else if (nums[middle] < target) {
                left = middle + 1; // target 在右区间，在[middle + 1, right)中
            } else { // nums[middle] == target
                return middle; // 数组中找到目标值，直接返回下标
            }
        }
        // 未找到目标值
        return -1;
    }
};
```

# 27. 移除元素

## 暴力解（两层循环）

* 自己写的错误解
  * 第二层循环的遍历范围有误
  * 手欠把多打了一个 = ，把赋值写成了判断

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int size = nums.size();
        for(int i = 0; i < size; i++) {
            if(nums[i] == val) {
                for(int j = i; j < size; j++) { // 错误1:j只需要遍历到size-1的位置，修改为： j < size-1
                    nums[j] == nums[j+1]; // 错误2:此处应该是=，进行赋值操作
                }
                size--;
                i--;
            }
        }
        return size;

    }
};
```

* 正确解

```cpp
// 时间复杂度：O(n^2)
// 空间复杂度：O(1)
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int size = nums.size();
        for (int i = 0; i < size; i++) {
            if (nums[i] == val) { // 发现需要移除的元素，就将数组集体向前移动一位
                for (int j = i + 1; j < size; j++) {
                    nums[j - 1] = nums[j];
                }
                i--; // 因为下标i以后的数值都向前移动了一位，所以i也向前移动一位
                size--; // 此时数组的大小-1
            }
        }
        return size;

    }
};
```

## 双指针法

双指针法（快慢指针法）： **通过一个快指针和慢指针在一个for循环下完成两个for循环的工作。**

### [力扣官方题解](https://leetcode.cn/problems/remove-element/solutions/730203/yi-chu-yuan-su-by-leetcode-solution-svxi/)

由于题目要求删除数组中等于$val$ 的元素，因此输出数组的长度一定小于等于输入数组的长度，我们可以把输出的数组直接写在输入数组上。可以使用双指针：右指针 $right$ 指向当前将要处理的元素，左指针 $left$ 指向下一个将要赋值的位置。

如果右指针指向的元素不等于 $val$，它一定是输出数组的一个元素，我们就将右指针指向的元素复制到左指针位置，然后将左右指针同时右移；

如果右指针指向的元素等于 $val$，它不能在输出数组里，此时左指针不动，右指针右移一位。

整个过程保持不变的性质是：区间  $[0,left)$ 中的元素都不等于 $val$。当左右指针遍历完输入数组以后，left 的值就是输出数组的长度。

这样的算法在最坏情况下（输入数组中没有元素等 于$val$），左右指针各遍历了数组一次。

![27.移除元素-双指针法](https://code-thinking.cdn.bcebos.com/gifs/27.%E7%A7%BB%E9%99%A4%E5%85%83%E7%B4%A0-%E5%8F%8C%E6%8C%87%E9%92%88%E6%B3%95.gif)


* 自己写的错误解

  * 按照我的这种写法，慢指针就起不到对数组进行移动的效果，最后只是得到了数组里有几个目标值，得不到删除目标值后的数组
  * 正确解更新在下面的代码中

```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int n = nums.size();
        int slow = 0;
        for (int fast = 0; fast < n; fast++) {
            if(nums[fast] != val) {
              // 添加 nums[slow] = nums[fast];
                slow++;
            }
        }
        return slow;

    }
};
```

