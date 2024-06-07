---
# 基本信息
title: QT 学习记录
date: 2024/05/31
tags: [cpp, QT]
categories: [cpp, QT]
description: QT 学习记录
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  QT 学习记录 # 必选
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



{% timeline %}

<!-- node 2024 年 6 月 1 日 -->

1. 开始学习。

2. 看完第一部分：Qt 简介、Qt 项目模块、按钮控件、信号槽的概念；

3. lambda表达式那里没听懂

{% endtimeline %}

# 0531【01-05】

1. QT 简介、历史、优点**（跨平台、接口简单、一定程度上简化了内存回收）**、版本、成功案例
2. 创建第一个QT程序 ([MacOS配置Clion的Qt环境的详细步骤（完整版）](https://blog.csdn.net/weixin_45571585/article/details/127074832))
   1. QT Creator 配置了半天也没成功，决定还是使用 CLion 了

# 0601【06-15】

1. 创建一个按钮，设置按钮大小
2. 固定窗口大小 `setFixesSize();`
3. QT 的窗口坐标系，左上角为(0, 0)

## 对象树

* 父类释放内存，子类也自动释放（一定程度上简化了内存管理）
* 构造自上而下，析构自下而上

![IMG_5985](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/IMG_5985.jpg)

## 信号和槽

优点：松散耦合，信号的发送端和接收端本身并没有关联，通过 connect 连接，将两端耦合在一起。

```cpp
connect(信号的发送者，信号发送端，信号接收者，信号的处理（槽）)
```

* 信号发送端是一个地址
* 信号可以连接信号
* 一个信号可以连接多个槽函数
* 多个信号可以连接同一个槽函数
* 信号与槽函数的类型要一一对应
* 信号的参数个数可以多于槽函数的参数个数

![image-20240601170731941](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240601170731941.png)



### 自定义信号与槽

1. 自定义信号：
   * 返回为 void
   * 需要声明，无需实现
   * **可以有参数（可以重载）**
   * 可以写在 signals 下
2. 自定义槽：
   * 返回为 void
   * 需要声明，也需要实现
   * 可以有参数，可以重载
   * 可以写到 public slot 或者 public 下



## lambda表达式

~~有点复杂，听不懂~~

一种在被调用的位置或作为参数传递给函数的位置定义匿名函数对象（闭包）的简便方法。

声明格式如下：

```cpp
[capture list] (params list) mutable exception-> return type { function body }
```

各项具体含义如下，

1. capture list：捕获外部变量列表
2. params list：形参列表
3. mutable指示符：用来说用是否可以修改捕获的变量
4. exception：异常设定
5. return type：返回类型
6. function body：函数体



# 0602【16】

复习之前所学的内容

# 0603【17-19】

## QMainWindow

![image-20240603102947005](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240603102947005.png)

* 菜单栏（Menu Bar）、工具栏(Tool Bar Area) 、状态栏、浮动窗口、中心部件的创建与相关设置

```cpp
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMenuBar>
#include <QToolBar>
#include <QStatusBar>
#include <QLabel>
#include <QDockWidget>
#include <QTextEdit>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    resize(600,400);

    // 菜单栏只能有一个
    // 创建菜单栏
    QMenuBar *bar =  menuBar();
    setMenuBar(bar);

    // 创建菜单
    QMenu *fileMeanu =  bar->addMenu("File");
    QMenu *editMeanu =  bar->addMenu("Edit");

    // 创建菜单项
    QAction *newAction = fileMeanu->addAction("New");
    fileMeanu->addSeparator();
    QAction *openAction = fileMeanu->addAction("Open");

    // 工具栏 可以有多个
    QToolBar *toolbar = new QToolBar(this);
    addToolBar(Qt::LeftToolBarArea, toolbar);

    toolbar->addAction("Debug");
    toolbar->addSeparator();
    toolbar->addAction("More");

    // toolbar->addAction(newAction);
    // 状态栏
    QStatusBar *staBar = statusBar();
    setStatusBar(staBar);
    QLabel *label = new QLabel("Montee", this);
    staBar->addPermanentWidget(label);


    // 浮动窗口
    QDockWidget *dockWidget = new QDockWidget("fudong", this);
    addDockWidget(dockWidget);

    // 中心部件
    QTextEdit *edit = new QTextEdit(this);
    setCentralWidget(edit);
}

MainWindow::~MainWindow()
{
    delete ui;
}
```

效果如图：

![image-20240603144423162](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240603144423162.png)

## 资源文件添加

1. Qt Creator 中 UI 设计的使用
2. Qt Resource File

# 0605【20-】

## 模态和非模态对话框的实现

* 模态对话框：
* 非模态对话框：



9712 3876
