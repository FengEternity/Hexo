---
# 基本信息
title: 链表part01
date: 2024/05/31
tags: [cpp, 计算机, leetcode, 秋招, 算法]
categories: [算法]
description: 链表part01
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image.jpeg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image.jpeg
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

# 203. [移除链表元素【简单】](https://leetcode.cn/problems/remove-linked-list-elements/description/)

先补一下链表使用C++语言的相关实现，概念知识在上一片博文：

学习文档：[链表的C++实现](https://majorli.github.io/algo_guide/ch03/sec01/318_linkedlist_2.html)

## 基本结构

```cpp
template<typename T>
struct Node {
        T _value;            // 元素值
        Node<T> *_next;      // 后继链指针

        // 构造函数
        Node() { _next = NULL; }                             // 默认构造函数
        Node(const T &val) { _value = val; _next = NULL; }   // 指定元素值的构造器
        // 访问器函数
        T &value() { return _value; }                        // 访问元素值
        Node<T> *next() { return _next; }                    // 返回后继指针
        void set_next(Node<T> *next) { _next = next; }       // 设置后继指针
};
```

元素值的访问器 `value()` 返回的是成员变量 `_value` 的引用，所以只要这一个访问器就能同时满足外部程序对元素值进行读写的功能要求，例如：

```cpp
Node<int> n(2);      // 创建一个元素值为2的节点
int v = n.value();   // 读取元素值
n.value()--;         // 元素值减一
n.value() = 3 * 3;   // 设置元素值
```

## 元素增删

```cpp
// 模板类定义，用于创建一个泛型链表
template<typename T>
struct LinkedList {
    // 插入和删除操作
    void push_front(const T &val); // 在链表头部插入一个新元素
    void insert(const T &val, const LinkedList<T>::Indicator prev); // 在指定位置后插入一个新元素

private:
    struct _Node; // 前向声明节点结构体
    _Node *_head; // 链表的头节点指针
    size_t _size; // 链表的大小

    // 内部类，用于指示链表中的位置
    struct Indicator {
        _Node *_ptr; // 指向链表中某个节点的指针
    };
};

// 在链表头部插入一个新元素
template<typename T>
void LinkedList<T>::push_front(const T &val)
{
    // 创建一个新节点，并将其值初始化为val
    LinkedList<T>::_Node *new_node = new LinkedList<T>::_Node(val);
    
    // 将新节点的_next指针指向当前头节点的下一个节点
    new_node->_next = _head->_next;
    
    // 将头节点的_next指针指向新节点
    _head->_next = new_node;
    
    // 链表大小加1
    ++_size;
}

// 在指定位置后插入一个新元素
template<typename T>
void LinkedList<T>::insert(const T &val, const LinkedList<T>::Indicator prev)
{
    // 创建一个新节点，并将其值初始化为val
    LinkedList<T>::_Node *new_node = new LinkedList<T>::_Node(val);
    
    // 将新节点的_next指针指向prev指针所指节点的下一个节点
    new_node->_next = prev._ptr->_next;
    
    // 将prev指针所指节点的_next指针指向新节点
    prev._ptr->_next = new_node;
    
    // 链表大小加1
    ++_size;
}

```



```cpp
// 模板类定义，用于创建一个泛型链表
template<typename T>
struct LinkedList {
    // 删除操作
    void pop_front(); // 删除链表头部的元素
    void erase(LinkedList<T>::Indicator prev); // 删除指定位置后的元素
    void clear(); // 清空链表

private:
    struct _Node; // 前向声明节点结构体
    _Node *_head; // 链表的头节点指针
    size_t _size; // 链表的大小

    // 内部类，用于指示链表中的位置
    struct Indicator {
        _Node *_ptr; // 指向链表中某个节点的指针
    };
};

// 删除链表头部的元素
template<typename T>
void LinkedList<T>::pop_front()
{
    // 如果链表为空，直接返回
    if (_size == 0) return;

    // 指向头节点后的第一个节点
    LinkedList<T>::_Node *node = _head->_next;

    // 将头节点的_next指针指向第二个节点
    _head->_next = node->_next;

    // 删除第一个节点
    delete node;

    // 链表大小减1
    --_size;
}

// 删除指定位置后的元素
template<typename T>
void LinkedList<T>::erase(LinkedList<T>::Indicator prev)
{
    // 如果prev指针无效或其后的节点不存在，直接返回
    if (!prev._ptr || !prev._ptr->_next) return;

    // 指向prev指针后的第一个节点
    LinkedList<T>::_Node *node = prev._ptr->_next;

    // 将prev指针的_next指针指向第二个节点
    prev._ptr->_next = node->_next;

    // 删除第一个节点
    delete node;

    // 链表大小减1
    --_size;
}

// 清空链表
template<typename T>
void LinkedList<T>::clear()
{
    // 指向头节点后的第一个节点
    LinkedList<T>::_Node *p = _head->_next, *next;

    // 遍历链表，逐个删除所有节点
    while (p) {
        next = p->_next; // 保存下一个节点的指针
        delete p; // 删除当前节点
        p = next; // 移动到下一个节点
    }

    // 链表大小置0
    _size = 0;
    
    // 将头节点的_next指针置空
    _head->_next = NULL;
}

```

## 题解

![203_链表删除元素6](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20210316095619221.png)

```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* removeElements(ListNode* head, int val) {
        while(head != NULL && head->val == val) {
            ListNode* tmp = head;
            head = head->next;
            delete tmp;
        }

        ListNode* cur = head;
        while(cur != NULL && cur->next != NULL) {
            if(cur->next->val == val) {
                ListNode* tmp = cur->next;
                cur->next = cur->next->next;
                delete tmp;
            }
            else cur = cur->next;
        }

        return head;
    }
};
```

### 代码逻辑

1. **删除头节点中所有值等于 `val` 的节点**：

   - `while (head != NULL && head->val == val)`：只要头节点存在且值等于 `val`，就删除头节点。
   - `ListNode* tmp = head; head = head->next; delete tmp;`：保存当前头节点，更新头节点指针，然后删除原头节点。

2. **删除链表中间部分值等于 `val` 的节点**：

   - `ListNode* cur = head;`：初始化 `cur` 指针，指向当前节点。
   - `while (cur != NULL && cur->next != NULL)`：遍历链表，直到 `cur` 或其下一个节点为 `NULL`。
   - `if (cur->next->val == val)` ：如果 `cur` 的下一个节点值等于 `val`，则删除该节点。
      - `ListNode* tmp = cur->next; cur->next = cur->next->next; delete tmp;`：保存要删除的节点，更新 `cur` 的 `next` 指针，删除节点。
   
      - `else { cur = cur->next; }`：如果 `cur` 的下一个节点值不等于 `val`，则移动到下一个节点。
   
3. 返回值

- `return head;`：返回更新后的链表头节点指针。

### 为什么需要 `tmp`

定义一个 `tmp` 变量是**为了安全地删除节点**。删除节点时，需要先保存该节点的地址，以便在更新指针后能够正确地释放该节点的内存。如果直接修改指针而不保存节点地址，可能会导致内存泄漏或访问已经释放的内存。

# 707. [设计链表【中等】](https://leetcode.cn/problems/design-linked-list/description/)

LeetCode 官方题解写的挺好的，跟着敲了一遍，熟悉一下链表增删改查等相关操作。

在链表类中实现这些功能：

- get(index)：获取链表中第 index 个节点的值。如果索引无效，则返回-1。
- addAtHead(val)：在链表的第一个元素之前添加一个值为 val 的节点。插入后，新节点将成为链表的第一个节点。
- addAtTail(val)：将值为 val 的节点追加到链表的最后一个元素。
- addAtIndex(index,val)：在链表中的第 index 个节点之前添加值为 val 的节点。如果 index 等于链表的长度，则该节点将附加到链表的末尾。如果 index 大于链表长度，则不会插入节点。如果index小于0，则在头部插入节点。
- deleteAtIndex(index)：如果索引 index 有效，则删除链表中的第 index 个节点。

```cpp
class MyLinkedList {
public:
    // 构造函数：初始化链表，设置大小为0，并创建一个哨兵节点
    MyLinkedList() {
        this->size = 0;
        this->head = new ListNode(0);
    }
    
    // 获取链表中第index个节点的值。如果索引无效，则返回-1
    int get(int index) {
        // 检查索引是否有效
        if (index < 0 || index >= size) {
            return -1;
        }
        // 初始化指针指向哨兵节点
        ListNode *cur = head;
        // 遍历链表，找到第index个节点
        for (int i = 0; i <= index; i++) {
            cur = cur->next;
        }
        // 返回第index个节点的值
        return cur->val;
    }
    
    // 在链表头部添加一个值为val的节点
    void addAtHead(int val) {
        // 在索引0处添加新节点
        addAtIndex(0, val);
    }
    
    // 在链表尾部添加一个值为val的节点
    void addAtTail(int val) {
        // 在链表的末尾添加新节点
        addAtIndex(size, val);
    }
    
    // 在链表的第index个节点之前插入值为val的节点
    // 如果index等于链表的长度，则插入到链表的末尾
    // 如果index大于链表的长度，则不插入节点
    void addAtIndex(int index, int val) {
        // 如果索引大于链表的大小，则不进行插入
        if (index > size) {
            return;
        }
        // 确保索引不小于0
        index = max(0, index);
        // 链表大小加1
        size++;
        // 初始化指针指向哨兵节点
        ListNode *pred = head;
        // 遍历链表，找到第index个节点的前驱节点
        for (int i = 0; i < index; i++) {
            pred = pred->next;
        }
        // 创建新节点
        ListNode *toAdd = new ListNode(val);
        // 插入新节点
        toAdd->next = pred->next;
        pred->next = toAdd;
    }
    
    // 删除链表中第index个节点
    void deleteAtIndex(int index) {
        // 检查索引是否有效
        if (index < 0 || index >= size) {
            return;
        }
        // 链表大小减1
        size--;
        // 初始化指针指向哨兵节点
        ListNode *pred = head;
        // 遍历链表，找到第index个节点的前驱节点
        for (int i = 0; i < index; i++) {
            pred = pred->next;
        }
        // 保存要删除的节点
        ListNode *p = pred->next;
        // 更新前驱节点的next指针
        pred->next = pred->next->next;
        // 删除节点，释放内存
        delete p;
    }
    
private:
    // 链表的大小
    int size;
    // 指向哨兵节点的指针
    ListNode *head;
};

```



# 206. 反转链表【简单】

## 个人思路

两个方法：

1. 定义一个新的链表，然后找到原链表的最后一个元素，作为新链表的头节点(

   * **发现这种方法反而很复杂，因为链表找最后一个元素很麻烦，而且单链表是不知道前一个元素是什么的，因此无论时间还是空间都比第二种更复杂**

2. 第二种，把所有链表的指针原地反转即可，如图：

   ![img](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/206.%E7%BF%BB%E8%BD%AC%E9%93%BE%E8%A1%A8.gif)


## 题解（双指针法）

   ```cpp
   /**
    * Definition for singly-linked list.
    * struct ListNode {
    *     int val;
    *     ListNode *next;
    *     ListNode() : val(0), next(nullptr) {}
    *     ListNode(int x) : val(x), next(nullptr) {}
    *     ListNode(int x, ListNode *next) : val(x), next(next) {}
    * };
    */
   class Solution {
   public:
       ListNode* reverseList(ListNode* head) {
           ListNode* prev = nullptr;
           ListNode* curr = head;
           while(curr != NULL) {
               ListNode* next = curr->next;
               curr->next = prev;
               prev = curr;
               curr = next;
           }
           return prev;
       }
   };
   ```

   



## 个人问题

* 对指针的相关操作还是过于陌生

