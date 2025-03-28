---
title: 哈希表part01
date: 2024/08/02
tags:
  - cpp
  - 计算机
  - leetcode
  - 秋招
  - 算法
categories:
  - cpp
  - 题解
description: 哈希表part01
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/nezuko-kamado-kimetsu-no-yaiba-hd-wallpaper-x-preview-27.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/nezuko-kamado-kimetsu-no-yaiba-hd-wallpaper-x-preview-27.jpg
poster:
  topic: 
  headline: 哈希表part01
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: true
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

# 哈希表理论基础

哈希表是根据关键码的值而直接进行访问的数据结构。**用来快速判断一个元素是否出现集合里**

![哈希表1](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210104234805168.png)

例如要查询一个名字是否在这所学校里。

要枚举的话时间复杂度是O(n)，但如果使用哈希表的话， 只需要O(1)就可以做到。

我们只需要初始化把这所学校里学生的名字都存在哈希表里，在查询的时候通过索引直接就可以知道这位同学在不在这所学校里了。

将学生姓名映射到哈希表上就涉及到了**hash function ，也就是哈希函数**。

## 哈希函数

![哈希表2](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/2021010423484818.png)



## 哈希碰撞

如图，小李和小王都映射到索引下标为1的位置，这一现象称为**哈希碰撞**。

![哈希表3](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/2021010423494884.png)

### 解决方法

1. 拉链法

   * 刚刚小李和小王在索引1的位置发生了冲突，发生冲突的元素都被存储在链表中。 这样我们就可以通过索引找到小李和小王了

   ![哈希表4](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210104235015226.png)

2. 线性探测法

   * 使用线性探测法，一定要保证tableSize大于dataSize。 我们需要依靠哈希表中的空位来解决碰撞问题。

     例如冲突的位置，放了小李，那么就向下找一个空位放置小王的信息。所以要求tableSize一定要大于dataSize ，要不然哈希表上就没有空置的位置来存放 冲突的数据了。如图所示

   ![哈希表5](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210104235109950.png)

## 常见的三种哈希结构
* 数组
* set（集合）
* map（映射）

# 242. 有效的字母异位词【简单】
## 题解
### 排序
t 是 s 的异位词等价于「两个字符串排序后相等」。因此我们可以对字符串 s 和 t 分别排序，看排序后的字符串是否相等即可判断。此外，如果 s 和 t 的长度不同，t 必然不是 s 的异位词。代码如下，【leetcode 官方题解】

```C
class Solution { 
	public: bool isAnagram(string s, string t) { 
		if (s.length() != t.length()) 
		{ 
			return false; 
		} 
		sort(s.begin(), s.end()); 
		sort(t.begin(), t.end()); 
		return s == t; 
	} 
};
```

### 哈希表
分别统计二者各个字符的出现次数，再比对哈希表，代码如下：
```C
class Solution {

public:

	bool isAnagram(string s, string t) {

		std::unordered_map<char, int> charCount1;	
		std::unordered_map<char, int> charCount2;
		
		for (char c: s) {
		
			charCount1[c]++;
		
		}
		
		for (char c: t) {
		
			charCount2[c]++;
		
		}
		
		return charCount1 == charCount2;

	}

};
```

```C
class Solution{
public:
	bool isAnagram(string s, string t) {
		if(s.length() != t.length) { // 如果两个字符串长度不同，则不可能符合条件
			return false;
		}
		unordered_map<char, int>map1;
		for(char i : s) map1[i]++;
		for(char i : t) map1[i]--;

		for(auto it : map1) {
		if(it.second != 0){
			return false;
			}
		}

		return true;
	}
}
```

# 349. 两个数组的交集【简单】

代码如下：

```C
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int> result_set;
        unordered_set<int> nums1_set(nums1.begin(), nums1.end());

        for(int num : nums2) {
            if(nums1_set.find(num) != nums1_set.end()) {
                result_set.insert(num);
            }
        }

        return vector<int>(result_set.begin(), result_set.end());
    }
};

```


我觉得个人要从这里学的大致是以下几点：

## set 相关知识

###  `std::set`

#### 特点

- **唯一性**：`std::set` 中的元素是唯一的，不允许重复。
- **有序**：元素会按照特定的顺序（通常是升序）存储。
- **底层实现**：通常使用红黑树实现。

#### 用法

cpp

```cpp
#include <iostream>
#include <set>

int main() {
    std::set<int> mySet;

    // 插入元素
    mySet.insert(5);
    mySet.insert(3);
    mySet.insert(8);
    mySet.insert(5); // 插入重复元素，失败

    // 遍历元素
    for (const auto& elem : mySet) {
        std::cout << elem << " "; // 输出: 3 5 8
    }
    std::cout << std::endl;

    // 查找元素
    if (mySet.find(3) != mySet.end()) {
        std::cout << "Found 3!" << std::endl;
    }

    // 删除元素
    mySet.erase(5);

    return 0;
}
```

### 2. `std::multiset`

#### 特点

- **允许重复**：`std::multiset` 中的元素可以重复。
- **有序**：元素会按照特定的顺序存储。
- **底层实现**：同样使用红黑树实现。

#### 用法

cpp

```cpp
#include <iostream>
#include <set>

int main() {
    std::multiset<int> myMultiSet;

    // 插入元素
    myMultiSet.insert(5);
    myMultiSet.insert(3);
    myMultiSet.insert(8);
    myMultiSet.insert(5); // 插入重复元素，成功

    // 遍历元素
    for (const auto& elem : myMultiSet) {
        std::cout << elem << " "; // 输出: 3 5 5 8
    }
    std::cout << std::endl;

    // 查找元素
    auto range = myMultiSet.equal_range(5);
    std::cout << "Count of 5: " << std::distance(range.first, range.second) << std::endl; // 输出: 2

    // 删除元素
    myMultiSet.erase(5); // 删除一个5

    return 0;
}
```

### 3. `std::unordered_set`

#### 特点

- **唯一性**：与 `std::set` 一样，`std::unordered_set` 中的元素是唯一的。
- **无序**：元素的存储顺序是不确定的，可能会根据哈希函数的实现而变化。
- **底层实现**：使用哈希表实现。

#### 用法

cpp

```cpp
#include <iostream>
#include <unordered_set>

int main() {
    std::unordered_set<int> myUnorderedSet;

    // 插入元素
    myUnorderedSet.insert(5);
    myUnorderedSet.insert(3);
    myUnorderedSet.insert(8);
    myUnorderedSet.insert(5); // 插入重复元素，失败

    // 遍历元素
    for (const auto& elem : myUnorderedSet) {
        std::cout << elem << " "; // 输出顺序不确定
    }
    std::cout << std::endl;

    // 查找元素
    if (myUnorderedSet.find(3) != myUnorderedSet.end()) {
        std::cout << "Found 3!" << std::endl;
    }

    // 删除元素
    myUnorderedSet.erase(5);

    return 0;
}
```

### 总结

- **`std::set`**：适用于需要唯一且有序的元素集合。
- **`std::multiset`**：适用于需要唯一性但允许重复的有序元素集合。
- **`std::unordered_set`**：适用于需要唯一性但不关心元素顺序的集合，通常具有更快的查找性能。

## for(int num : nums2)

`or(int num : nums2)` 是一种范围基于的 `for` 循环（range-based for loop），用于遍历容器（如数组或向量）中的每个元素。具体来说：

- **`int num`**: 在每次迭代中， `num` 将被赋值为 `nums2` 中**当前元素的值**，而不是索引。
- **`: nums2`**: 指定要遍历的容器，这里是 `nums2` 向量。

### 功能

这个循环的作用是依次访问 `nums2` 中的每一个元素，执行循环体内的代码。它的简洁性使得代码更易读，避免了使用传统的索引方式。

### 示例

假设 `nums2` 的内容是 `{1, 2, 3}`，那么循环将依次执行：

- 第一次：`num` 为 `1`
- 第二次：`num` 为 `2`
- 第三次：`num` 为 `3`

在每次迭代中，可以对 `num` 进行操作，比如检查它是否在 `nums1_set` 中。

## nums1_set.find(num) != nums1_set.end()

这段代码的作用是检查 `num` 是否存在于 `nums1_set` 中，需要注意的是 `find` 方法用于查找集合中是否存在指定的元素 `num`，
- 如果找到该元素，`find` 返回一个指向该元素的迭代器。
- 如果没有找到该元素，这返回迭代器的末尾


# 202. 快乐数【简单】

```C
#include <unordered_set>

class Solution {
public:
    bool isHappy(int n) {
        std::unordered_set<int> seen; // 创建哈希集
        while (n != 1 && seen.find(n) == seen.end()) {
            seen.insert(n); // 将当前数字加入哈希集
            n = getNext(n); // 计算下一个数字
        }
        return n == 1; // 如果最终得到 1，返回 true
    }

private:
    int getNext(int n) {
        int sum = 0;
        while (n > 0) {
            int digit = n % 10; // 获取最后一位数字
            sum += digit * digit; // 计算平方和
            n /= 10; // 去掉最后一位数字
        }
        return sum; // 返回平方和
    }
};

```


注意看这行代码 `seen.find(n) == seen.end()`

### 哈希集的工作原理

1. **定义哈希集**:
    
    - 使用一个哈希集 `seen` 来存储已经计算过的数字。
    - 哈希集允许快速查找、插入和删除操作，平均时间复杂度为 O(1)。
2. **检测循环**:
    
    - 在每次计算平方和后，检查当前数字是否已经存在于 `seen` 中。
    - 如果存在，说明我们已经计算过这个数字，意味着进入了循环。
    - 如果不存在，则将当前数字加入 `seen`，继续计算下一个平方和。