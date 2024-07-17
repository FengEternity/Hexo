---
# 基本信息
title: Qt 样式表
date: 2024/07/15
tags: [cpp, QT]
categories: [cpp, QT]
description: Qt 样式表
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline: Qt 样式表 # 必选
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

# 1. QSS的作用

几乎和 CSS 一模一样，用来设计界面组件样式

# 2. QSS的句法

## 一般句法格式

```css
QTextEdit {
    background-color: #ffffff;
    border: 1px solid #dddddd;
    padding: 5px;
    font-size: 14px; /* 字体大小 */
}
```

## 选择器

支持 CSS2 中定义的所有选择器

![image-20240715135623009](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240715135623009.png)

## 子控件

对于一些组合的界面组件，需要对子控件进行选择，如

```css
QComboBox::drop-down{}
```

![image-20240715141134752](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240715141134752.png)

## 伪状态

伪状态使得样式规则只能应用于某个状态，这就是一种条件应用规则。伪状态出现在选择器后面，用一个冒号(:)隔开。示例如下，

```css
QLineEdit:hover{
	background-color: black;
}
```

这表明当鼠标移动到QLineEdit上方时，该表 QLineEdit的背景色。

![image-20240715142704943](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240715142704943.png)

## 属性

