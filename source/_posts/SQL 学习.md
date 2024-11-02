---
title: SQL 学习
date: 2024/10/29
tags:
  - cpp
  - cpp
categories:
  - cpp
  - sql
description: SQL 学习记录
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241029153626.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241029153626.png
poster:
  topic: 
  headline: SQL 学习
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

本文为《MySQL 必知必会》学习笔记，仅记录个人欠缺的知识点，不具有系统学习的效用。

# 第一章 了解MySQL

# 第二章 MySQL 简介
![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241029151214.png)


MysQL 是一种基于客户机-服务器的数据库。客户机与服务器可以安装在多台电脑，也可以安装在同一台电脑上。
* 服务器部分负责所有数据的访问与处理
* 客户机是与用户打交道的机器

# 第三章 使用 MySQL

1. 登陆： `mysql -u root -p` 
	1. -u：指定用户名
	2. -p：指定密码
	3. -h：指定主机口
	4. -P：指定端口
2. `quit / exit` 退出
3. `use databaseName;` 使用数据库
4. `show DATABASES；`显示可用的数据库![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241029152005.png)
5. `show tables`; 显示数据库中的数据表

> 擅用 `help` 命令，如可以通过 `help show;` 查询 `show` 的相关用法![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241029153223.png)


# 第四章 检索数据

* select
* limit
* distinct

示例：

```mysql
SELECT DISTINCT id
from products
LIMIT 5;
```

这条 SQL 查询的作用是从 `products` 表中选择不重复的 `id` 值，并限制结果返回前 5 条记录。具体来说：

- **`SELECT DISTINCT id`**：从 `products` 表中选择 `id` 列，并确保结果中每个 `id` 都是唯一的，不会重复。
- **`LIMIT 5`**：限制查询结果的数量，只返回前 5 个唯一的 `id`。



如果是：

```mysql
SELECT DISTINCT id
from products
LIMIT 5, 5;
```

这条 SQL 查询的作用是从 `products` 表中选择不重复的 `id` 值，并返回结果中的**第 6 到第 10 条**记录。


# 第五章 排序检索数据

1. `ORDER BY`

```MySQL
SELECT id, price, name
FROM products
ORDER BY price DESC, name
limit 5;
```

这条 SQL 查询的作用是从 `products` 表中选择 `id`、`price` 和 `name` 列，并按以下规则排序和限制结果：
- **`ORDER BY price DESC, name`**：
    - 首先按 `price` 降序排序（从高到低）。
    - 如果价格相同，则按 `name` 升序排序（字母顺序）。
- **`LIMIT 5`**：限制结果集为前 5 条记录。

排序默认是升序，`DESC` 可以指定某一列为降序


# 第六章 过滤数据


where 子句操作符：

| 操作符       | 描述                                           | 示例                                      |
|--------------|------------------------------------------------|-------------------------------------------|
| =            | 等于                                           | `SELECT * FROM table WHERE column = 1;`   |
| <> 或 !=     | 不等于                                         | `SELECT * FROM table WHERE column <> 1;`  |
| >            | 大于                                           | `SELECT * FROM table WHERE column > 1;`   |
| <            | 小于                                           | `SELECT * FROM table WHERE column < 1;`   |
| >=           | 大于等于                                       | `SELECT * FROM table WHERE column >= 1;`  |
| <=           | 小于等于                                       | `SELECT * FROM table WHERE column <= 1;`  |
| BETWEEN ... AND ... | 在某个范围内                             | `SELECT * FROM table WHERE column BETWEEN 1 AND 10;` |
| LIKE         | 搜索某种模式                                   | `SELECT * FROM table WHERE column LIKE 'A%';` |
| IN           | 匹配一组值中的任意一个                         | `SELECT * FROM table WHERE column IN (1, 2, 3);` |
| IS NULL      | 为 NULL                                        | `SELECT * FROM table WHERE column IS NULL;` |
| IS NOT NULL  | 不为 NULL                                      | `SELECT * FROM table WHERE column IS NOT NULL;` |
| AND          | 两个条件都为真                                 | `SELECT * FROM table WHERE column1 = 1 AND column2 = 2;` |
| OR           | 任一条件为真                                   | `SELECT * FROM table WHERE column1 = 1 OR column2 = 2;` |
| NOT          | 否定条件                                       | `SELECT * FROM table WHERE NOT column = 1;` |
| EXISTS       | 子查询返回一个或多个行                         | `SELECT * FROM table WHERE EXISTS (SELECT * FROM other_table WHERE condition);` |

# 第七章 数据过滤


# 第八章 用通配符进行过滤


## 百分号通配符

```MySQL
SELECT id, name
FROM products
WHERE name like '%jet%'
```

上面的查询语句将返回所有 name 中包含 `jet` 的杭

## 下划线通配符

与 `%` 不同的是，`_` 仅匹配一个字符，或许把它理解为一个占位符也是个不错的思路。


## 使用通配符的技巧

1. 不要过度使用。如果有其他方法可代替，需要比较一下，因为通配符的搜索是比较耗时的
2. 注意通配符的位置

# 第九章 用正则表达式进行搜索

这部分后续将具体学习，现在不太了解正则，读起来有些吃力。


# 第十章 创建计算字符

