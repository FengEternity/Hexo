---
# 基本信息
title: SQL 学习
date: 2024/10/29
tags: [cpp, cpp]
categories: [cpp, sql]
description: SQL 学习记录
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241029153626.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241029153626.png
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  SQL 学习 # 必选
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

