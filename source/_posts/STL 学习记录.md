> [菜鸟教程](https://www.runoob.com/cplusplus/cpp-stl-tutorial.html)
> [黑马C++ 讲义](https://github.com/Blitzer207/C-Resource/blob/master/第5阶段-C++提高编程资料/提高编程能力资料/讲义/C++提高编程.md#31-string容器)

C++ 标准模板库（Standard Template Library，STL）是一套功能强大的 C++ 模板类和函数的集合，它提供了一系列通用的、可复用的算法和数据结构。

使用 STL 有以下好处（对现阶段的我来说，就是刷 leetcode 比较舒服）：
* **代码复用**：STL 提供了大量的通用数据结构和算法，可以减少重复编写代码的工作。
* **性能优化**：STL 中的算法和数据结构都经过了优化，以提供最佳的性能。
* **泛型编程**：使用模板，STL 支持泛型编程，使得算法和数据结构可以适用于任何数据类型。
- **易于维护**：STL 的设计使得代码更加模块化，易于阅读和维护。

以下列举了关于C++标准模板库（STL）核心组件：

| 组件           | 描述                                                         |
|----------------|--------------------------------------------------------------|
| 容器 (Containers) | 容器是 STL 中最基本的组成部分之一，提供了各种数据结构，包括向量 (vector)、链表 (list)、队列 (queue)、栈 (stack)、集合 (set) 和映射 (map) 等。这些容器具有不同的特性和用途，可以根据实际需求选择合适的容器。 |
| 算法 (Algorithms) | STL 提供了大量的算法，用于对容器中的元素进行各种操作，包括排序、搜索、复制、移动、变换等。这些算法在使用时不需要关心容器的具体类型，只需指明要操作的范围即可。 |
| 迭代器 (Iterators) | 迭代器用于遍历容器中的元素，允许以统一的方式访问容器中的元素，而不关心容器的内部实现细节。STL 提供了多种类型的迭代器，包括随机访问迭代器、双向迭代器、前向迭代器和输出迭代器等。 |
| 函数对象 (Function Objects) | 函数对象是可以像函数一样调用的对象，可以用于算法中的各种操作。STL 提供了多种函数对象，包括一元函数对象、二元函数对象、谓词等，可以满足不同的需求。 |
| 适配器 (Adapters) | 适配器用于将一种容器或迭代器适配成另一种容器或迭代器，以满足特定的需求。STL 提供了多种适配器，包括栈适配器 (stack adapter)、队列适配器 (queue adapter) 和优先级队列适配器 (priority queue adapter) 等。 |

# 容器

STL 的常用容器大致可以分为以下几类：**序列容器、关联容器、容器适配器**
1. 序列容器：
	1. vector：动态数组，在尾部添加和删除元素效率高，支持随机访问。
		- vector<int> vec = {10, 20, 30}
	2. list：双向链表，在任意位置插入和删除元素效率高，但不支持随机访问。
		- list<string> names = {"Alice", "Bob", "Charlie"};
	3. deque：双端队列，在头部和尾部添加和删除元素效率高。
		- deque<double> values = {1.1, 2.2, 3.3}; 
2. 关联容器：
	1. set：元素唯一且自动排序。
		- set<int> uniqueNums = {5, 10, 15};
	2. multiset：允许元素重复，自动排序。
		- multiset<char> repeatedChars = {'a', 'a', 'b', 'b'};
	3. map：键值对存储，键唯一，按照键自动排序。
		- map<string, int> wordCount = {{"hello", 5}, {"world", 3}};
	4. multimap：允许键重复。
		- multimap<int, string> multipleMappings = {{1, "one"}, {1, "uno"}, {2, "two"}};
3. 容器适配器
	1. stack：后进先出（LIFO）的栈结构。
	2. queue：先进先出（FIFO）的队列结构。
4. 字符串容器
	1. string


## string

### 基本概念

**string和char * 区别：**

- char * 是一个指针
- string 是一个类，类内部封装了char*，管理这个字符串，是一个char*型的容器。

### string 构造函数

构造函数原型：

- `string();` //创建一个空的字符串 例如: string str; 
- `string(const char* s);` //使用字符串s初始化
- `string(const string& str);` //使用一个string对象初始化另一个string对象
- `string(int n, char c);` //使用n个字符c初始化

下面分别给出这些函数原型的使用示例与分析：

#### string()

* 特点：创建一个空的字符串对象，不包含任何字符。
* 示例：
	```C
	string str1;
	```

#### string(const char* s);

* 特点：通过一个以空字符结尾的 C 风格字符串（`const char*`）来初始化 `string` 对象。
* 方便将现有的 C 风格字符串转换为 `string` 类型进行处理。
* 示例；
	```C
	string str2 = "Hello, World!";
	```


#### string(const string& str);

* 特点：使用另一个已存在的 `string` 对象来初始化新的 `string` 对象，进行深拷贝。
* 用途：
	* 在需要复制一个已有的 `string` 对象时，确保新对象与原对象相互独立，修改其中一个不会影响另一个。
	* 作为函数参数传递或返回值时，避免不必要的复制开销。
* 示例：
	```C
	string str3 = str2;
	```

#### string(int n, char c);

* 特点：创建一个包含指定数量的相同字符的字符串。
* 示例：
	```C
	string str4(5, 'a');
	```

string 的多种构造方式没有可比性，灵活使用即可

### string 赋值操作

赋值的函数原型：

- `string& operator=(const char* s);` //char*类型字符串 赋值给当前的字符串
	```C 
	string str; 
	str = "Hello";
	```
- `string& operator=(const string &s);` //把字符串s赋给当前的字符串
	```C 
	string str1 = "World"; 
	string str2; str2 = str1;
	```
- `string& operator=(char c);` //字符赋值给当前的字符串
- `string& assign(const char *s);` //把字符串s赋给当前的字符串
- `string& assign(const char *s, int n);` //把字符串s的前n个字符赋给当前的字符串
	```C
	string str; 
	str.assign("HelloWorld", 5); // str 将被赋值为 "Hello"
	```
- `string& assign(const string &s);` //把字符串s赋给当前字符串
- `string& assign(int n, char c);` //用n个字符c赋给当前字符串
	```C
	string str; 
	str.assign(3,  'x'); // str 将被赋值为 "xxx"
	```

### string 字符串拼接

拼接操作大致分为两类：`+=`重载与append函数的运用。

**函数原型：**

- `string& operator+=(const char* str);` //重载+=操作符
- `string& operator+=(const char c);` //重载+=操作符
- `string& operator+=(const string& str);` //重载+=操作符
- `string& append(const char *s);`  //把字符串s连接到当前字符串结尾
- `string& append(const char *s, int n);` //把字符串s的前n个字符连接到当前字符串结尾
- `string& append(const string &s);` //同operator+=(const string& str)
- `string& append(const string &s, int pos, int n);`//字符串s中从pos开始的n个字符连接到字符串结尾
	```C
	string str1 = "Hello"; 
	string str2 = "WorldWide"; 
	str1.append(str2, 5, 3); // str1 将变为 "HelloWid"
	```


### string 查找与替换

- find 查找是从左往后，rfind 从右往左
- find 找到字符串后返回查找的第一个字符位置，找不到返回-1
- replace 在替换时，要指定从哪个位置起，多少个字符，替换成什么样的字符串

**函数原型：**

- `int find(const string& str, int pos = 0) const;` //查找str第一次出现位置,从pos开始查找
- `int find(const char* s, int pos = 0) const;`  //查找s第一次出现位置,从pos开始查找
- `int find(const char* s, int pos, int n) const;`  //从pos位置查找s的前n个字符第一次位置
- `int find(const char c, int pos = 0) const;`  //查找字符c第一次出现位置
- `int rfind(const string& str, int pos = npos) const;` //查找str最后一次位置,从pos开始查找
- `int rfind(const char* s, int pos = npos) const;` //查找s最后一次出现位置,从pos开始查找
- `int rfind(const char* s, int pos, int n) const;` //从pos查找s的前n个字符最后一次位置
- `int rfind(const char c, int pos = 0) const;`  //查找字符c最后一次出现位置
- `string& replace(int pos, int n, const string& str);`  //替换从pos开始n个字符为字符串str
- `string& replace(int pos, int n,const char* s);`  //替换从pos开始的n个字符为字符串s


### string 字符串比较

按字符的ASCII码进行对比（等于 返回 0 ; 大于 返回 1 ; 小于 返回  -1  ; ）

**函数原型：**

- `int compare(const string &s) const;`  //与字符串s比较
- `int compare(const char *s) const;` //与字符串s比较

### string 字符串获取

string中单个字符存取方式有两种

- `char& operator[](int n);`  //通过[]方式取字符
- `char& at(int n);`  //通过at方法获取字符

二者的区别如下：

**越界处理**：
- `operator[]` ：不进行边界检查，如果索引越界，可能会导致未定义的行为。
- `at` ：会进行边界检查，如果索引越界，会抛出 `out_of_range` 异常。

  

**错误处理方式**：
- 使用 `operator[]` 时，如果出现越界访问，程序可能会崩溃或者产生不可预测的结果，这对于调试和程序的稳定性是不利的。
- 而 `at` 方法通过抛出异常，可以让程序在运行时捕获这个错误，并进行相应的处理，增加了程序的健壮性。


### string 字符串插入和删除

**函数原型：**

- `string& insert(int pos, const char* s);`  //插入字符串
- `string& insert(int pos, const string& str);`  //插入字符串
- `string& insert(int pos, int n, char c);` //在指定位置插入n个字符c
- `string& erase(int pos, int n = npos);` //删除从Pos开始的n个字符



### string 子串

- `string substr(int pos = 0, int n = npos) const;` //返回由pos开始的n个字符组成的字符串
- 使用示例：
```C
//子串
void test01()
{

	string str = "abcdefg";
	string subStr = str.substr(1, 3);
	cout << "subStr = " << subStr << endl;

	string email = "hello@sina.com";
	int pos = email.find("@");
	string username = email.substr(0, pos);
	cout << "username: " << username << endl;

}

int main() {

	test01();

	system("pause");

	return 0;
}
```


## vector

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240731165334.png)


**功能：**

- vector数据结构和**数组非常相似**，也称为**单端数组**

**vector与普通数组区别：**

- 不同之处在于数组是静态空间，而vector可以**动态扩展**

**动态扩展：**

- 并不是在原空间之后续接新空间，而是找更大的内存空间，然后将原数据拷贝新空间，释放原空间

### 构造函数

**函数原型：**

- `vector<T> v;`  //采用模板实现类实现，默认构造函数
- `vector(v.begin(), v.end());`  //将v[begin(), end())区间中的元素拷贝给本身。
- `vector(n, elem);` //构造函数将n个elem拷贝给本身。
- `vector(const vector &vec);` //拷贝构造函数。


### vector 容量和大小

- 判断是否为空 --- empty
- 返回元素个数 --- size
- 返回容器容量 --- capacity
- 重新指定大小 --- resize

**函数原型：**

- `empty();`  //判断容器是否为空
    
- `capacity();` //容器的容量
    
- `size();` //返回容器中元素的个数
    
- `resize(int num);` //重新指定容器的长度为num，若容器变长，则以默认值填充新位置。
    
    ​ //如果容器变短，则末尾超出容器长度的元素被删除。
    
- `resize(int num, elem);` //重新指定容器的长度为num，若容器变长，则以elem值填充新位置。
    
    ​ //如果容器变短，则末尾超出容器长度的元素被删除


在当时听这部分内容的视频课程时，一直有一个疑问：
> vector是动态添加元素，为什么还需要使用resize函数区调整容器长度？
> 下面是AI的回复：
> 1. 提前规划内存：在某些情况下，您可能提前知道最终需要的容器大小，通过 `resize` 可以一次性分配足够的内存，避免多次动态扩展导致的性能开销。 
> 2. 初始化特定长度的容器：如果希望创建一个具有特定长度并且初始值已知的 `vector` ，使用 `resize` 可以方便地实现。 
> 3. 与其他代码或接口的交互：可能存在与其他部分的代码或外部接口的交互，要求 `vector` 具有特定的长度。 
> 4. 数据填充和规整：例如在一些算法或数据处理中，需要将 `vector` 的长度调整到特定值，并进行相应的数据填充或删除，以满足后续处理的要求。 
> 5. 性能优化：有时提前调整好容器长度，可以使后续的操作（如遍历、访问等）更加高效，因为不需要频繁地处理容器的扩容。 


### vector插入和删除

**函数原型：**

- `push_back(ele);` //尾部插入元素ele
- `pop_back();` //删除最后一个元素
- `insert(const_iterator pos, ele);` //迭代器指向位置pos插入元素ele
- `insert(const_iterator pos, int count,ele);`//迭代器指向位置pos插入count个元素ele
- `erase(const_iterator pos);` //删除迭代器指向的元素
- `erase(const_iterator start, const_iterator end);`//删除迭代器从start到end之间的元素
- `clear();` //删除容器中所有元素

这部分要注意 erase() 这个函数，它是基于位置迭代器进行删除的。示例如下：

```C
#include <iostream> 
#include <vector> 
int main() { 
	std::vector<int> numbers = {10, 20, 30, 40, 50}; 
	// 删除单个元素 
	std::vector<int>::iterator it = numbers.begin() + 2; // 指向 30
	numbers.erase(it); // 删除 30 
	
	for (int num : numbers) { 
		std::cout << num << " "; 
		} 
		
	std::cout << std::endl; 
	
	// 删除一段元素 
	std::vector<int>::iterator startIt = numbers.begin() + 1; // 指向 20 
	std::vector<int>::iterator endIt = numbers.begin() + 3; // 指向 40 
	numbers.erase(startIt, endIt); // 删除 20 和 40 
	
	for (int num : numbers) { 
		std::cout << num << " "; 
		} 
	return 0; 
}
```


### vector 数据存取

**函数原型：**

- `at(int idx);`  //返回索引idx所指的数据
- `operator[];`  //返回索引idx所指的数据
- `front();`  //返回容器中第一个数据元素
- `back();` //返回容器中最后一个数据元素


### vector 互换容器

**函数原型：**

- `swap(vec);` // 将vec与本身的元素互换

### vector 预留空间

**功能描述：**

- 减少vector在动态扩展容量时的扩展次数

**函数原型：**

- `reserve(int len);`//容器预留len个元素长度，预留位置不初始化，元素不可访问。

reserve 与 resize的区别和联系：
`reserve` 和 `resize` 是 `vector` 中两个不同但又有些关联的操作。


**区别**：

1. 功能不同：
    
    - `resize` 用于改变 `vector` 中元素的数量。如果新的大小大于原来的大小，新增的元素会根据指定的方式（默认值或给定值）进行初始化；如果新的大小小于原来的大小，超出的元素会被删除。
    - `reserve` 只是预先分配一定的内存空间，以减少后续插入元素时频繁重新分配内存的开销，但它不会改变元素的数量。
2. 对元素的影响不同：
    
    - `resize` 会直接操作元素，增加或删除元素，并可能对元素进行初始化。
    - `reserve` 不操作元素，只是预留内存空间。
3. 容量和大小的变化：
    
    - `resize` 会同时改变 `vector` 的大小（`size`），可能也会改变容量（`capacity`）。~~（在 `vector` 中，“大小（`size`）”指的是当前实际存储的元素数量，而“容量（`capacity`）”指的是在不重新分配内存的情况下，`vector` 能够容纳的元素数量。）~~
    - `reserve` 只改变容量，不会改变大小。

**联系**：

1. 目的相似：都是为了更有效地管理 `vector` 的内存和元素操作。
    
2. 相互配合：在某些情况下，可以先使用 `reserve` 预分配足够的内存空间，然后再使用 `resize` 来设置元素的数量，以提高性能和避免不必要的内存重新分配。

以下是示例代码来说明它们的区别：


```C
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec1;

    vec1.reserve(10);  // 预留 10 个元素的空间，但 size 仍为 0
    std::cout << "Size: " << vec1.size() << ", Capacity: " << vec1.capacity() << std::endl;

    std::vector<int> vec2;

    vec2.resize(5);  // size 变为 5，新元素用默认值 0 初始化
    std::cout << "Size: " << vec2.size() << ", Capacity: " << vec2.capacity() << std::endl;

    return 0;
}
```


## deque 容器

==大部分操作与vector类似==

- 双端数组，可以对头端进行插入删除操作

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240801161331.png)


**deque与vector区别：**

- vector对于头部的插入删除效率低，数据量越大，效率越低
- deque相对而言，对头部的插入删除速度回比vector快
- vector访问元素时的速度会比deque快,这和两者内部实现有关


### deque 构造函数

**函数原型：**

- `deque<T>` deqT; //默认构造形式
- `deque(beg, end);` //构造函数将[beg, end)区间中的元素拷贝给本身。
- `deque(n, elem);` //构造函数将n个elem拷贝给本身。
- `deque(const deque &deq);` //拷贝构造函数




### deque赋值操作


**功能描述：**

- 给deque容器进行赋值

**函数原型：**

- `deque& operator=(const deque &deq);`  //重载等号操作符
    
- `assign(beg, end);` //将[beg, end)区间中的数据拷贝赋值给本身。
    
- `assign(n, elem);` //将n个elem拷贝赋值给本身。

### deque 大小操作

与 vector 不同的是，deque没有容量的概念 

**函数原型：**

- `deque.empty();` //判断容器是否为空
    
- `deque.size();` //返回容器中元素的个数
    
- `deque.resize(num);` //重新指定容器的长度为num,若容器变长，则以默认值填充新位置。
    
    ​ //如果容器变短，则末尾超出容器长度的元素被删除。
    
- `deque.resize(num, elem);` //重新指定容器的长度为num,若容器变长，则以elem值填充新位置。
    
    ​ //如果容器变短，则末尾超出容器长度的元素被删除。


### deque 插入和删除

deque 与 vector 最大的区别就在于插入和删除：

**插入操作**：

- `vector` ：在尾部插入元素效率高，但在头部或中间插入元素效率较低，因为可能需要移动大量元素来为新元素腾出空间，并可能导致重新分配内存和复制现有元素。
- `deque` ：在头部和尾部插入元素都具有较高的效率，因为其内部结构允许在两端快速添加元素，而不需要移动大量其他元素。在中间插入元素的效率相对较低，但通常比 `vector` 在中间插入要好一些。

  

**删除操作**：

- `vector` ：删除尾部元素效率高，删除头部或中间元素效率低，原因与插入类似，可能涉及大量元素的移动和内存调整。
- `deque` ：删除头部和尾部元素效率高，删除中间元素效率相对较低。

**函数原型：**

两端插入操作：

- `push_back(elem);` //在容器尾部添加一个数据
- `push_front(elem);` //在容器头部插入一个数据
- `pop_back();` //删除容器最后一个数据
- `pop_front();` //删除容器第一个数据

指定位置操作：

- `insert(pos,elem);` //在pos位置插入一个elem元素的拷贝，返回新数据的位置。
    
- `insert(pos,n,elem);` //在pos位置插入n个elem数据，无返回值。
    
- `insert(pos,beg,end);` //在pos位置插入[beg,end)区间的数据，无返回值。
    
- `clear();` //清空容器的所有数据
    
- `erase(beg,end);` //删除[beg,end)区间的数据，返回下一个数据的位置。
    
- `erase(pos);` //删除pos位置的数据，返回下一个数据的位置。


### deque 数据存储

**函数原型：**

- `at(int idx);`  //返回索引idx所指的数据
- `operator[];`  //返回索引idx所指的数据
- `front();`  //返回容器中第一个数据元素
- `back();` //返回容器中最后一个数据元素
