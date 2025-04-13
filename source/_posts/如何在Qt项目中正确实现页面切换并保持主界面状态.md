---
title: 如何在Qt项目中正确实现页面切换并保持主界面状态
date: 2024/07/21
tags:
  - cpp
  - 计算机
  - debug
categories:
  - 技术学习
description: 如何在Qt项目中正确实现页面切换并保持主界面状态
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/bc9d1a2b4219f9c23dde4bc39fe3fbd8f6a4b13d_2_1380x776.jpeg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/bc9d1a2b4219f9c23dde4bc39fe3fbd8f6a4b13d_2_1380x776.jpeg
poster:
  topic: 
  headline: 如何在Qt项目中正确实现页面切换并保持主界面状态
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
# 问题描述
![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240721181505.png)


如上图所示，我要实现在 `文件搜索` 界面点击左上角的 `Home` 键会到首页，实现起来似乎也很简单代码如下，

```C++
void MainWindow::on_actionHome_triggered() {
    QWidget *currentCentralWidget = takeCentralWidget();
    if (currentCentralWidget) {
        delete currentCentralWidget;
    }
    // 恢复初始化时的中央控件设置
    setCentralWidget(ui->centralWidget);

    // 如果需要重新设置文件视图模型和其他控件，可以在这里执行
    ui->fileView->setModel(fileModel);
    ui->fileView->setRootIndex(fileModel->index(QDir::currentPath()));
    ui->fileView->setViewMode(QListView::IconMode);
    ui->fileView->setIconSize(QSize(64, 64));

    // 重新连接信号和槽（如果有必要）
    connect(ui->tagListWidget, &QListWidget::itemClicked, this, &MainWindow::onTagSelected);
    connect(ui->fileView, &QListView::clicked, this, &MainWindow::onFileClicked);

    populateTags(); // 填充标签列表
}

```

然而……

# 问题分析与探索

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20240721182509.png)

很显然，是一个内存访问的问题，`ui->centralwidget` 在被访问时已经无效，这意味着它可能在某处被删除或未正确初始化。那就检查一下，是什么原因导致`ui->centralwidget` 被错误的删除吧。

初步猜测，是文件搜索页面在进行析构时释放UI导致的，

```C
// 析构函数，释放资源  
FileSearch::~FileSearch() {  
    threadPool->waitForDone();  
    delete ui;  
}
```

我尝试把 `delete ui;`注释掉，然而问题并没有得到解决，反而导致了，文件搜索界面的 UI 组件没有得到释放，错误地显示在界面中。

# 问题解决

现在已经锁定了问题的根源，尝试了上述方法也行不通，那么就要找到一种很为合适的解决方案，为了确保在切换中央控件时不会重复删除，我在`MainWindow`类中添加了一个新的成员变量`homeWidget`，并在构造函数中初始化该控件：

```C
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      ui(new Ui::MainWindow),
      fileModel(new QFileSystemModel(this)),
      fileTagSystem("tags.csv", "users.csv"),
      homeWidget(nullptr) {

    ui->setupUi(this); // 确保 setupUi 被正确调用

    // 初始化 homeWidget
    homeWidget = new QWidget(this);
    QHBoxLayout *layout = new QHBoxLayout(homeWidget);
    layout->addWidget(ui->splitter);  // 将 splitter 添加到 homeWidget

    setCentralWidget(homeWidget);  // 设置 homeWidget 为中央控件

    // 其他初始化代码...
}

```

接着，修改了`on_actionHome_triggered`方法，确保返回主界面并清空文件视图，以保持初始状态：

```C
void MainWindow::on_actionHome_triggered() {
    qDebug() << "进入 on_actionHome_triggered";

    // 检查 homeWidget 指针是否有效
    if (!homeWidget) {
        qDebug() << "homeWidget 指针为空！";
        return;
    }

    qDebug() << "设置中央控件为 homeWidget。";
    setCentralWidget(homeWidget);

    // 清空文件视图
    initializeView();

    // 重新连接信号和槽
    connect(ui->tagListWidget, &QListWidget::itemClicked, this, &MainWindow::onTagSelected);
    connect(ui->fileView, &QListView::clicked, this, &MainWindow::onFileClicked);

    populateTags(); // 填充标签列表
}

```

# 总结
一句话总结一下：解决这个问题的关键在于**正确管理中央控件的生命周期**。