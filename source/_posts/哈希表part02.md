---
title: 哈希表part02
date: 2024/08/02
tags:
  - cpp
  - 计算机
  - leetcode
  - 秋招
  - 算法
categories:
  - 技术学习
description: 哈希表part02
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/nezuko-kamado-kimetsu-no-yaiba-hd-wallpaper-x-preview-27.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/nezuko-kamado-kimetsu-no-yaiba-hd-wallpaper-x-preview-27.jpg
poster:
  topic: 
  headline: 哈希表part02
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

# 454. 四数相加II【中等】

emmmm，猪脑子解法（特指我自己）
```C
class Solution {

public:

int fourSumCount(vector<int>& nums1, vector<int>& nums2, vector<int>& nums3, vector<int>& nums4) {
	
	int result = 0;
	
	for(int i = 0; i < nums1.size(); i++) {
	
		for(int j = 0; j < nums1.size(); j++) {
		
			for(int k = 0; k < nums1.size(); k++) {
			
				for(int l = 0; l < nums1.size(); l++)
				
				if(nums1[i] + nums2[j] + nums3[k] + nums4[l] == 0) result++;
			
			}
		
		}
	
	}
	
	return result;
	
	}

};
```

果不其然，超时了！

```C
class Solution {
public:
    int fourSumCount(vector<int>& nums1, vector<int>& nums2, vector<int>& nums3, vector<int>& nums4) {
        unordered_map<int, int> sumCount;
        int result = 0;

        // 计算 nums1 和 nums2 的所有可能和
        for (int a : nums1) {
            for (int b : nums2) {
                sumCount[a + b]++;
            }
        }

        // 计算 nums3 和 nums4 的所有可能和，并查找其负和
        for (int c : nums3) {
            for (int d : nums4) {
                result += sumCount[-(c + d)];
            }
        }

        return result;
    }
};

```

使用哈希表来存储 `nums1` 和 `nums2` 所有可能的和，然后再遍历 `nums3` 和 `nums4` 来查找相应的负和。这样可以将时间复杂度降低到 $O(n^2)$。


# 383. 赎金信【简单】

```C
class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        unordered_map<char, int> ransomNoteMap;

        // 统计 ransomNote 中每个字符的出现次数
        for (char a : ransomNote) {
            ransomNoteMap[a]++;
        }

        // 遍历 magazine，减少对应字符的计数
        for (char b : magazine) {
            if (ransomNoteMap[b] > 0) {
                ransomNoteMap[b]--;
            }
        }

        // 检查是否所有字符都能满足
        for (char a : ransomNote) {
            if (ransomNoteMap[a] > 0) {
                return false;
            }
        }

        return true;
    }
};

```

# 15. 三数之和【中等】

我的思路：
* 使用 set 对结果进行去重
* 先对数组进行排序以便于去重操作
* 然后进行三重循环暴力解决以查找符合要求的结果

```C
class Solution {

public:

	vector<vector<int>> threeSum(vector<int>& nums) {
		set<vector<int>>resultSet;	  
		
		sort(nums.begin(), nums.end());
		
		for(int i = 0; i < nums.size(); i++) {
		
			for(int j = i + 1; j < nums.size(); j++) {
			
					for (int k = j + 1; k < nums.size(); k++) {
					
					if(nums[i] + nums[j] + nums[k] == 0) {
					
					vector<int> ijk;					
					ijk.push_back(nums[i]);				
					ijk.push_back(nums[j]);					
					ijk.push_back(nums[k]);					
					resultSet.insert(ijk);					
					}			
				}		
			}	
		}
			
		// 将 set 转换为 vector
		vector<vector<int>> result(resultSet.begin(), resultSet.end());
		
		return result;
	
	}

};
```

很不幸，超时了……

## 双指针法

```C
#include <vector>
#include <algorithm>

class Solution {
public:
    std::vector<std::vector<int>> threeSum(std::vector<int>& nums) {
        std::vector<std::vector<int>> result;
        std::sort(nums.begin(), nums.end());

        for (int i = 0; i < nums.size(); i++) {
            // 跳过重复元素
            if (i > 0 && nums[i] == nums[i - 1]) continue;

            int left = i + 1;
            int right = nums.size() - 1;

            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];
                if (sum == 0) {
                    result.push_back({nums[i], nums[left], nums[right]});
                    // 跳过重复元素
                    while (left < right && nums[left] == nums[left + 1]) left++;
                    while (left < right && nums[right] == nums[right - 1]) right--;
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        return result;
    }
};

```

### 解决思路

1. **排序**：
   - 首先对数组进行排序。排序后，能够方便地使用双指针法，并且可以轻松跳过重复的元素。

2. **外层循环**：
   - 使用一个循环遍历数组的每个元素，将当前元素视为三元组的第一个元素 \( a \)。
   - 为了避免重复，检查当前元素是否与前一个元素相同。如果相同，则跳过。

3. **双指针法**：
   - 初始化两个指针：`left` 指向当前元素的下一个位置，`right` 指向数组的最后一个元素。
   - 使用这两个指针来寻找另外两个元素 \( b \) 和 \( c \)，使得 \( a + b + c = 0 \)。

4. **计算和**：
   - 在 `left` 小于 `right` 的情况下，计算三元组的和：
     - 如果和为零，找到一个有效的三元组，将其存入结果中，并移动指针，同时跳过重复的元素。
     - 如果和小于零，说明需要增大和，因此移动 `left` 指针向右。
     - 如果和大于零，说明需要减小和，因此移动 `right` 指针向左。

5. **避免重复**：
   - 在找到有效三元组后，使用循环跳过所有相同的 `left` 和 `right` 元素，确保结果中的三元组是唯一的。

6. **返回结果**：
   - 最后，返回所有找到的三元组。

### 整体流程

- **时间复杂度**：排序的时间复杂度为 \( O(n \log n) \)，而双指针遍历的时间复杂度为 \( O(n^2) \)。因此整体的时间复杂度为 \( O(n^2) \)。
- **空间复杂度**：主要使用了额外的空间来存储结果，空间复杂度为 \( O(k) \)，其中 \( k \) 是找到的三元组的数量。

# 18. 四数之和【中等】

思路与上面那题一致

```C
class Solution {
public:
    vector<vector<int>> fourSum(vector<int>& nums, int target) {
        vector<vector<int>> result;
        sort(nums.begin(), nums.end());
        for (int i = 0; i < nums.size(); i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue; // 跳过重复的 i
            for (int j = i + 1; j < nums.size(); j++) {
                if (j > i + 1 && nums[j] == nums[j - 1]) continue; // 跳过重复的 j
                int left = j + 1;
                int right = nums.size() - 1;
                while (left < right) {
                    // 使用 long long 避免溢出
                    long long sum = static_cast<long long>(nums[i]) + nums[j] + nums[left] + nums[right];
                    if (sum < target) {
                        left++;
                    } else if (sum > target) {
                        right--;
                    } else {
                        result.push_back({nums[i], nums[j], nums[left], nums[right]});
                        // 跳过重复的 left
                        while (left < right && nums[left] == nums[left + 1]) left++;
                        // 跳过重复的 right
                        while (left < right && nums[right] == nums[right - 1]) right--;
                        left++;
                        right--;
                    }
                }
            }
        }
        return result;
    }
};

```