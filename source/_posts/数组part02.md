---
# 基本信息
title: 数组part02
date: 2024/05/28
tags: [cpp, 计算机, leetcode, 秋招, 算法]
categories: [算法]
description: 代数组part02
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211518_nNfZE.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211518_nNfZE.gif
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  数组part02 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: true
mathjax: 
# 可
references:
comments: # 设置 false 禁止评论
indexing: # 设置 false 避免被搜索
breadcrumb: # 设置 false 隐藏面包屑导航
leftbar: 
rightbar:
h1: # 设置为 '' 隐藏标题
type: tech # tech/story
---



# 977. 有序数组平方【简单】

[LeetCode 官方题解](https://leetcode.cn/problems/squares-of-a-sorted-array/solutions/447736/you-xu-shu-zu-de-ping-fang-by-leetcode-solution/)

## 暴力排序

思路：先平方，再排序

```cpp
class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        for(int i = 0; i < nums.size(); i++) {
            nums[i] *= nums[i];
        }
        sort(nums.begin(), nums.end());
        return nums;
    }
};
```



[【C++】sort函数使用方法](https://zhuanlan.zhihu.com/p/309291783) : sort 函数是快排的改良版，结合了堆排序等排序方法。

## 双指针

* 思路
  * 个人理解：
    * 定义两个指针：**队首指针、队尾指针**
    * 定义一个与原数组**相同大小**的空数组
    * 队首指针遍历，同时与队尾指针比较平方后大小，大的那一个放到空数组的队尾
      * 放到队尾这里也需要定义一个指针用于记录位置信息，如下面代码的 right_result ~~（所以为啥不叫三指针法）~~
    * 指针重合即停止 (这个判断条件有误，应该是 left <= right，否则会进入死循环)

```cpp
#include <vector>
#include <cmath>
using namespace std;

class Solution {
public:
    vector<int> sortedSquares(vector<int>& nums) {
        int left = 0;
        int right = nums.size() - 1;
        int right_result = right;
        vector<int> result(nums.size(), 0);
        
        while (left <= right) {
            int left_square = nums[left] * nums[left];
            int right_square = nums[right] * nums[right];
            
            if (left_square > right_square) {
                result[right_result] = left_square;
                left++;
            } else {
                result[right_result] = right_square;
                right--;
            }
            right_result--;
        }
        return result;
    }
};

```

### [C++ vector容器简析](https://www.runoob.com/w3cnote/cpp-vector-container-analysis.html)

```cpp
vector<int> result(nums.size(), 0);
```

上述代码：创建并初始化了一个名为 result 的 vector<int> 类型的对象，vector<int> 是一个构造函数，可以接受两个参数：

* size：表示vector的大小
* value：表示vector中每个元素的初始大小

下面详细解释上述代码的含义：

* vector<int>：`vector<int>` 是 C++ 标准库中的一个模板类，用于表示一个动态数组。`vector` 是一个模板类，`<int>` 表示这个 `vector` 将存储 `int` 类型的元素。
* result：`result` 是这个 `vector<int>` 对象的名称。它是一个变量名，表示我们将使用这个名称来引用这个 `vector` 对象
* nums.size()：`nums` 是一个 `vector<int>` 类型的对象。`nums.size()` 返回 `nums` 中元素的个数，即 `nums` 的大小。这个大小是一个无符号整数类型（通常是 `size_t`）。



# 209. 长度最小的子数组【中等】

[代码随想录](https://programmercarl.com/0209.长度最小的子数组.html#算法公开课)

## 个人思路（暴力解）

我的思路应该就是暴力解……

1. 定义外循环用于遍历整个数组
2. 内循环用于把 i 与后面的元素想加，直到出现 >= target的情况，或者遍历完
3. 定义一个 int 类型变量 result = 0，用于记录最小连续子数组的长度

```cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int result = 0;
        for (int i = 0; i < nums.size(); i++) {
            int sum = 0;
            for (int j = i; j < nums.size(); j++) {
                sum += nums[j];
                if (sum == target) { // 判断条件有误
                    result = j - i + 1;
                    continue; // 这里应该修改为 break
                }
            }
        }
        return result;
    }
};
```



很遗憾，我的代码错了，GPT给出的问题如下：

1. **条件判断错误**：你在内部循环中检查 `sum == target`，但题目要求的是总和大于等于 `target`。
2. **结果更新错误**：你没有正确更新 `result`。你需要在找到满足条件的子数组时更新 `result`，并且应该保留最小的长度。
3. **效率问题**：你的算法是一个 O(n2)*O*(*n*2) 的暴力解法，对于较大的输入数组会导致超时。

修改后的代码如下，

```cpp
class Solution {
public:
    int minSubArrayLen(int target, vector<int>& nums) {
        int result = INT_MAX; // 用于存储最小长度，初始值设为一个很大的数
        for (int i = 0; i < nums.size(); i++) {
            int sum = 0;
            for (int j = i; j < nums.size(); j++) {
                sum += nums[j];
                if (sum >= target) {
                    result = min(result, j - i + 1);
                    break; // 找到一个符合条件的子数组，跳出内层循环
                }
            }
        }
        return result == INT_MAX ? 0 : result; // 如果result没有被更新过，返回0
    }
};

```

**修改说明：**

1. **条件判断修正**：
   - 将 `if (sum == target)` 修改为 `if (sum >= target)`，以满足题目要求。
2. **更新结果**：
   - 在找到符合条件的子数组时，使用 `result = min(result, j - i + 1)` 来更新最小长度。
3. **跳出内层循环**：
   - 一旦找到一个符合条件的子数组，立即跳出内层循环，因为在当前起点 `i` 继续寻找更长的子数组是没有意义的。
4. **返回结果**：
   - 如果 `result` 没有被更新，说明没有找到符合条件的子数组，返回 0。
   - 否则返回 `result`。

> 思路应该是没什么问题了，很不幸，超时了，leetcode给了一个超级离谱的测试样例。

### 三元运算符

```cpp
condition ? value_if_true : value_if_false
```

- **condition**：这是一个布尔表达式，计算结果要么是 `true`，要么是 `false`。
- **value_if_true**：如果 `condition` 为 `true`，则返回这个值。
- **value_if_false**：如果 `condition` 为 `false`，则返回这个值。



## 滑动窗口

![209.长度最小的子数组](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/209.%E9%95%BF%E5%BA%A6%E6%9C%80%E5%B0%8F%E7%9A%84%E5%AD%90%E6%95%B0%E7%BB%84.gif)

所谓滑动窗口，**就是不断的调节子序列的起始位置和终止位置，从而得出我们要想的结果**。

在本题中实现滑动窗口，主要确定如下三点：

- 窗口内是什么？

  - 窗口就是 满足其和 ≥ s 的长度最小的 连续 子数组。

- 如何移动窗口的起始位置？

  - 窗口的起始位置如何移动：如果当前窗口的值大于等于s了，窗口就要向前移动了（也就是该缩小了）。

    ![leetcode_209](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210312160441942.png)

- 如何移动窗口的结束位置？

  - 窗口的结束位置如何移动：窗口的结束位置就是遍历数组的指针，也就是for循环里的索引。

```cpp
class Solution {
public:
    int minSubArrayLen(int s, vector<int>& nums) {
        int result = INT32_MAX;
        int sum = 0; // 滑动窗口数值之和
        int i = 0; // 滑动窗口起始位置
        int subLength = 0; // 滑动窗口的长度
        for (int j = 0; j < nums.size(); j++) {
            sum += nums[j];
            // 注意这里使用while，每次更新 i（起始位置），并不断比较子序列是否符合条件
            while (sum >= s) {
                subLength = (j - i + 1); // 取子序列的长度
                result = result < subLength ? result : subLength;
                sum -= nums[i++]; // 这里体现出滑动窗口的精髓之处，不断变更i（子序列的起始位置）
            }
        }
        // 如果result没有被赋值的话，就返回0，说明没有符合条件的子序列
        return result == INT32_MAX ? 0 : result;
    }
};
```



# 59. 螺旋矩阵II【中等】

[视频讲解](https://www.bilibili.com/video/BV1SL4y1N7mV/?vd_source=f30eba35d0a8915376778596dfd73224)

这题……毫无思路，可见我对多维矩阵的理解极弱。

题解也看不懂，感觉就是硬套啊，这就是**模拟**的精髓吗？

据说这还是**高频考题**？看来得背下来了。

```cpp
class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> res(n, vector<int>(n, 0)); // 使用vector定义一个二维数组
        int startx = 0, starty = 0; // 定义每循环一个圈的起始位置
        int loop = n / 2; // 每个圈循环几次，例如n为奇数3，那么loop = 1 只是循环一圈，矩阵中间的值需要单独处理
        int mid = n / 2; // 矩阵中间的位置，例如：n为3， 中间的位置就是(1，1)，n为5，中间位置为(2, 2)
        int count = 1; // 用来给矩阵中每一个空格赋值
        int offset = 1; // 需要控制每一条边遍历的长度，每次循环右边界收缩一位
        int i,j;
        while (loop --) {
            i = startx;
            j = starty;

            // 下面开始的四个for就是模拟转了一圈
            // 模拟填充上行从左到右(左闭右开)
            for (j; j < n - offset; j++) {
                res[i][j] = count++;
            }
            // 模拟填充右列从上到下(左闭右开)
            for (i; i < n - offset; i++) {
                res[i][j] = count++;
            }
            // 模拟填充下行从右到左(左闭右开)
            for (; j > starty; j--) {
                res[i][j] = count++;
            }
            // 模拟填充左列从下到上(左闭右开)
            for (; i > startx; i--) {
                res[i][j] = count++;
            }

            // 第二圈开始的时候，起始位置要各自加1， 例如：第一圈起始位置是(0, 0)，第二圈起始位置是(1, 1)
            startx++;
            starty++;

            // offset 控制每一圈里每一条边遍历的长度
            offset += 1;
        }

        // 如果n为奇数的话，需要单独给矩阵最中间的位置赋值
        if (n % 2) {
            res[mid][mid] = count;
        }
        return res;
    }
};
```

