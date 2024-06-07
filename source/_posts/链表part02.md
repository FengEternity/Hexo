---
# 基本信息
title: 链表part02
date: 2024/05/31
tags: [cpp, 计算机, leetcode, 秋招, 算法]
categories: [cpp, 题解]
description: 链表part02
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/C8167B63922595B3E70BC8E35E68A4A5.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/C8167B63922595B3E70BC8E35E68A4A5.png
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  链表part01 # 必选
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
type: tech # tech/story
---

# 24. 两两交换链表中的节点【中等】

## 题解

没有什么特殊的方法，不过要注意一下几点：

1. 画图理解思路，注意每个结点的位置（前链是否还存在，后链连接的是谁）
2. 理解临时结点的作用
   * 如果不设置临时结点，以`cur->next = cur->next->next;`为例，在进行这条语句后，之前的 `cur` 的下一个结点将会找不到自己的位置
3. while 循环的判断条件
   1. `cur->next != nullptr`：这个条件确保了当前节点 `cur` 的下一个节点存在，即保证了在执行交换操作时不会出现空指针异常。
   2. `cur->next->next != nullptr`：这个条件确保了当前节点 `cur` 的下下个节点存在，即保证了至少有两个节点可以进行交换操作。


## 虚拟头结点

虚拟头节点是一个在链表头部添加的额外节点，它不存储任何实际的数据，只是作为辅助。虚拟头节点的引入可以简化链表操作的逻辑，并解决一些特殊情况下的边界问题。

通过引入虚拟头节点，我们可以在处理链表时统一操作逻辑。**无论是在链表的开头、中间还是末尾插入或删除节点，我们都可以使用相同的逻辑进行操作**。这减少了代码中的条件判断，使得代码更加简洁和易于理解。

虚拟头节点还能够**解决空链表的情况**。如果链表为空且没有虚拟头节点，我们需要对空链表和非空链表进行不同的处理。然而，通过添加虚拟头节点，链表的头部始终存在，我们可以统一对链表进行处理，无论链表是否为空。

`GPT` 的回答：

虚拟头节点在这段代码中的作用是简化链表操作，特别是在处理头节点时的边界情况处理。具体来说，虚拟头节点的作用包括以下几点：

1. **简化边界情况处理**：通过引入虚拟头节点，可以避免在处理头节点时需要特殊处理的情况。在这段代码中，虚拟头节点 `dumyHead` 的存在使得整个链表的操作更加统一，不需要单独考虑头节点的情况。

2. **方便链表操作**：虚拟头节点可以作为一个占位符，使得链表操作更加灵活。在这段代码中，虚拟头节点的 `next` 指针指向真正的头节点，通过操作虚拟头节点，可以方便地操作链表的头部和其他部分。

3. **简化节点插入操作**：在链表中插入节点时，如果没有虚拟头节点，需要特殊处理头节点的情况。有了虚拟头节点，插入操作可以变得更加统一和简单，不需要单独处理头节点。

4. **避免空指针异常**：通过引入虚拟头节点，可以避免在链表操作中出现空指针异常。在这段代码中，虚拟头节点的存在保证了 `cur->next` 不会为空，避免了空指针异常的可能性。

# 19. 删除链表的倒数第N个节点【中等】

## 思路

### 个人思路

两次循环，显然时间复杂度为 $O(n^2)$

1. 第一层循环用于确定链表的长度
2. 第二次循环用于找到倒数第 N 个结点

代码如下，

```cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode *dummyHead = new ListNode(0); // 创建一个虚拟头节点
        dummyHead->next = head; // 将虚拟头节点指向链表头部
        ListNode *cur = dummyHead;
        int size = 0;

        // 计算链表长度
        while(cur->next != nullptr) {
            size++;
            cur = cur->next;
        }

        int index = size - n;
        cur = dummyHead;

        // 移动到要删除节点的前一个节点
        for(int i = 0; i < index; i++) {
            cur = cur->next;
        }

        // 删除倒数第 n 个节点
        ListNode *tmp = cur->next;
        cur->next = cur->next->next;
        delete tmp;

        return dummyHead->next; // 返回链表头部
    }
};

```

### 快慢指针

双指针的经典应用，如果要删除倒数第 n 个节点，让 fast 移动 n 步，然后让 fast 和 slow 同时移动，直到 fast 指向链表末尾。删掉 slow 所指向的节点就可以了。

```cpp
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode* dummyHead = new ListNode(0);
        dummyHead->next = head;
        ListNode* slow = dummyHead;
        ListNode* fast = dummyHead;
        while(n-- && fast != NULL) {
            fast = fast->next;
        }
        fast = fast->next; // fast再提前走一步，因为需要让slow指向删除节点的上一个节点
        while (fast != NULL) {
            fast = fast->next;
            slow = slow->next;
        }
        slow->next = slow->next->next; 
        
        // ListNode *tmp = slow->next;  C++释放内存的逻辑
        // slow->next = tmp->next;
        // delete tmp;
        
        return dummyHead->next;
    }
};
```

# 160. 链表相交【简单】

## 思路和代码

### 我的思路（暴力解）

* 两层循环进行比对，代码如下（这是我个人写的代码，相关错误已在注释中指出）

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
      // 不需要的代码
      //  ListNode* dummyHeadA = new ListNode(0);
      //  dummyHeadA->next = headA;
        ListNode* dummyHeadB = new ListNode(0);
        dummyHeadB->next = headB;

        ListNode* curA = headA;
        ListNode* curB = headB;
        while(curA != NULL) {
            while(curB != NULL) {
              // 错误1:应该是比较结点本身，而不是结点的值
                if(curA->val == curB->val) {
                    return curA->val; // 错误2:题目要求返回的是链表
                }
                curB = curB->next;
            }
            curA = curA->next;
          //错误3:内存循环后没有重置curB指针
        }
        return NULL;
    }
};

```

修改都的代码如下，

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        ListNode* dummyHeadB = new ListNode(0);
        dummyHeadB->next = headB;

        ListNode* curA = headA;
        ListNode* curB = headB;
        while(curA != NULL) {
            while(curB != NULL) {
                if(curA == curB) {
                    return curA;
                }
                curB = curB->next;
            }
            curA = curA->next;
            curB = dummyHeadB;
        }
        return NULL;
    }
};
```

### 双指针

代码如下，

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        // 如果任意一个链表为空，则不可能有相交节点
        if (headA == NULL || headB == NULL) return NULL;

        // 初始化两个指针
        ListNode* a = headA;
        ListNode* b = headB;

        // 遍历两个链表
        while (a != b) {
            // 如果指针a到达链表A的末尾，则将其重置到链表B的头节点
            a = (a == NULL) ? headB : a->next;
            // 如果指针b到达链表B的末尾，则将其重置到链表A的头节点
            b = (b == NULL) ? headA : b->next;
        }

        // 如果两个指针相遇，则返回相交节点；否则返回NULL
        return a;
    }
};

```

其中比较难以理解的是遍历链表部分，有点取巧的成分在里面，可以画个图模拟一下，

```cpp
// while (a != b) {
//     a = (a == NULL) ? headB : a->next;
//     b = (b == NULL) ? headA : b->next;
// }
// 三元表达式含义同下面的代码：

if (a == NULL) {
    a = headB;
} else {
    a = a->next;
}

if (b == NULL) {
    b = headA;
} else {
    b = b->next;
}

```

- **循环条件**：当 `a` 和 `b` 不相等时继续循环。
- **指针移动**：
  - 如果 `a` 到达了链表 `A` 的末尾（即 `a == NULL`），则将 `a` 指向链表 `B` 的头节点 `headB`。否则，将 `a` 移动到下一个节点 `a->next`。
  - 同样地，如果 `b` 到达了链表 `B` 的末尾（即 `b == NULL`），则将 `b` 指向链表 `A` 的头节点 `headA`。否则，将 `b` 移动到下一个节点 `b->next`。

# 142. 环形链表II[中等]

## 思路

看不懂，直接上代码吧！

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        ListNode* fast = head;
        ListNode* slow = head;
        while(fast != NULL && fast->next != NULL) {
            slow = slow->next;
            fast = fast->next->next;
            // 快慢指针相遇，此时从head 和 相遇点，同时查找直至相遇
            if (slow == fast) {
                ListNode* index1 = fast;
                ListNode* index2 = head;
                while (index1 != index2) {
                    index1 = index1->next;
                    index2 = index2->next;
                }
                return index2; // 返回环的入口
            }
        }
        return NULL;
    }
};
```

