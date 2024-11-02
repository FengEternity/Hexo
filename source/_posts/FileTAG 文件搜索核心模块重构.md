---
title: FileTAG 文件搜索核心模块重构
date: 2024/11/2
tags:
  - cpp
  - 计算机
  - 文件搜索
categories:
  - cpp
  - FileTAG
description: FileTAG 文件搜索核心模块重构
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241102133113.png
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241102133113.png
poster:
  topic: 
  headline: FileTAG 文件搜索核心模块重构
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: 
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

在软件开发的过程中，去 refactor（重构）自己的代码，绝对是一个痛苦的事情。但是看着自己曾经写的恶臭的代码（仅限于笔者），又实在不忍心继续受它的毒害，无奈，乖乖 refactor 吧。

# 1. 背景

保持代码的**清晰**和**可维护性**是项目开发中至关重要的两点，这次对文件搜索模块的重构，起因是想要将 UI 与文件搜索、数据库操作分离，以达到在不实例化 UI 的条件下，就可以进行创建一个文件搜索对象，以便在后台进行执行。

最初的 `FileSearch` 类中包含了大量与用户界面（UI）相关的代码和文件搜索逻辑、数据库操作，导致代码变得复杂且难以维护。为了改善这一点，们决定将核心逻辑与 UI 操作分离，使得每个类的职责更加清晰。

# 2. 问题分析

先看看原先的 `FileSearch` 类，继承自 `QWidget`，用于实现文件搜索功能 ：

```C
class FileSearch : public QWidget {  
Q_OBJECT  
  
public:  
    explicit FileSearch(QWidget *parent = nullptr);  
    ~FileSearch();  
  
private slots:  
    void onSearchButtonClicked();  
    void onFileFound(const QString &filePath);  
    void onSearchFinished();  
    void onFinishButtonClicked();  
    void onSearchFilterChanged(const QString &text);  
    void onFileInserted(const QString &filePath);  
    // void onSearchFinished(const QVector<QString> &result);  
  
  
private:  
    Ui::FileSearch *ui;  
    QThreadPool *threadPool;  
    QPushButton *searchButton;  
    QLineEdit *searchLineEdit;  
    QLineEdit *pathLineEdit;  
    QLineEdit *filterLineEdit;  
    QTableView *resultTableView;  
    QStandardItemModel *tableModel;  
    QSortFilterProxyModel *proxyModel;  
    QPushButton *finishButton;  
    QProgressBar *progressBar;  
    QLabel *progressLabel;  
    QElapsedTimer timer;  
    int updateCounter;  
    int activeTaskCount;  
    int totalDirectories;  
  
    void onSearchTime(qint64 elapsedTime);  
    void updateProgressLabel();  
    void finishSearch();  
    void stopAllTasks();  
    void onTaskStarted();  
    void initFileDatabase();  
  
    bool isSearching;  
    bool firstSearch;  
    bool isStopping;  
    static QVector<QString> filesBatch; // 声明静态变量  
    QSet<QString> uniquePaths; // 用于记录已处理的目录  
    QSet<QString> uniqueFiles; // 用于记录已记录的文件  
  
    QVector<FileSearchThread *> activeTasks; // 新增保存活动任务的成员变量  
  
    // 新增任务队列和同步机制的变量  
    QQueue<QString> *taskQueue;  
    QMutex *queueMutex;  
    QWaitCondition *queueCondition;  
  
    void enqueueDirectories(const QString &path, int depth); // 新增方法声明  
    QVector<QString> extractKeywordsFromFile(const QString &filePath);  // 声明提取关键词的方法  
  
    FileDatabase *db;  
    DatabaseThread *dbThread;  
};
```

可以看到，上面的代码提供了在 GUI 应用程序中执行多线程文件搜索的功能，结合了用户界面组件、线程管理和数据库支持，并且支持异步搜索和结果显示。听起来还不错，但是也可以看到类中定义了大量的私有成员，不同的功能耦合过紧，也增加代码负责程度，降低了可维护性，具体表现为：
- **功能混合**：`FileSearch` 中的文件搜索逻辑与 UI 更新混杂在一起，使得一个类承担了过多的责任。这不仅使得代码难以理解，也使得任何功能的修改都可能影响到其他功能。
- **缺乏模块化**：原有代码未能将相关功能进行模块化，导致代码变动时需要对多个部分进行修改，增加了出错的风险。例如，在修改文件搜索算法时，可能需要同时调整 UI 逻辑。

> 耦合过紧：指系统中的不同模块或组件之间依赖关系过于紧密，导致它们难以独立修改或替换。

# 3. 重构策略

上述的主要问题总结起来就是耦合度过高，所以重构的策略也是比较明确的：
## 3.1 职责单一化

我的修改思路是：
1. 原有的 FileSearch 类保留用户界面的交互，处理用户输入和更新显示
2. 定义新的 FileSearchCore 类，负责文件搜索的核心逻辑，包括搜索策略、结果处理和数据库操作等。

这样分离确保了每个类功能的相对单一，降低了各个组件之间的耦合度。例如，当需要修改文件搜索逻辑时，只需调整 `FileSearchCore`，而不必担心影响 UI 逻辑。也很好的实现了，我希望在程序启动时，就开始文件搜索去建立文件索引的数据库。

在原 FileSearch 保留 UI 交互功能，而不是创建新的类来进行 UI 交互还有一个重要的原因是：在这个类创建之初，就是一个 Qt UI 类，定义新的类进行功能代码迁移相比现在的实现方法要负责许多。

具体修改后的头文件如下：

```C
/*  
 * FileSearch.h 
 * Author: Montee 
 * CreateDate: 2024-11-1 
 * Updater: Montee 
 * UpdateDate: 2024-11-1 
 * Summary: 文件搜索窗口类的实现文件  
 */
 
#ifndef FILESEARCH_H  
#define FILESEARCH_H  
  
#include <QWidget>  
#include <QLineEdit>  
#include <QTableView>  
#include <QPushButton>  
#include <QStandardItemModel>  
#include <QProgressBar>  
#include <QLabel>  
#include <QSortFilterProxyModel>  
  
#include "FileSearchCore.h"  
  
namespace Ui {  
    class FileSearch;  
}  
  
class FileSearch : public QWidget {  
Q_OBJECT  
  
public:  
    explicit FileSearch(QWidget *parent = nullptr);  
    ~FileSearch();  
  
private slots:  
    void onSearchButtonClicked();  
    void onFinishButtonClicked();  
    void onSearchFilterChanged(const QString &text);  
    void onFileFound(const QString &filePath);  
    void onSearchFinished();  
    void updateProgress(int value, int total);  
  
private:  
    Ui::FileSearch *ui;  
    QPushButton *searchButton;  
    QLineEdit *searchLineEdit;  
    QLineEdit *pathLineEdit;  
    QLineEdit *filterLineEdit;  
    QTableView *resultTableView;  
    QStandardItemModel *tableModel;  
    QSortFilterProxyModel *proxyModel;  
    QPushButton *finishButton;  
    QProgressBar *progressBar;  
    QLabel *progressLabel;  
  
    FileSearchCore *searchCore;  
  
    void updateProgressLabel(int value, int total);  
};  
  
#endif // FILESEARCH_H
```

```C
/*  
 * FileSearchCore.h 
 * Author: Montee 
 * CreateDate: 2024-11-1 
 * Updater: Montee 
 * UpdateDate: 2024-11-1 
 * Summary: 文件文件搜索核心逻辑  
 */  
 
#ifndef FILESEARCHCORE_H  
#define FILESEARCHCORE_H  
  
#include <QObject>  
#include <QThreadPool>  
#include <QElapsedTimer>  
#include <QQueue>  
#include <QMutex>  
#include <QWaitCondition>  
#include <QSet>  
  
#include "FileSearchThread.h"  
#include "FileIndexDatabase.h"  
#include "DatabaseThread.h"  
  
class FileSearchCore : public QObject {  
Q_OBJECT  
  
public:  
    explicit FileSearchCore(QObject *parent = nullptr);  
    ~FileSearchCore();  
  
    void startSearch(const QString &keyword, const QString &path);  
    void stopSearch();  
    void initFileDatabase();  
  
signals:  
    void fileFound(const QString &filePath);  
    void searchFinished();  
    void progressUpdated(int value, int total);  
  
private slots:  
    void onFileInserted(const QString &filePath);  
    void onSearchFinished();  
    void onTaskStarted();  
    void onFileFound(const QString &filePath);  
  
private:  
    void enqueueDirectories(const QString &path, int depth);  
    void finishSearch();  
    void stopAllTasks();  
    void onSearchTime(qint64 elapsedTime);  
  
    // 成员变量  
    int activeTaskCount;  
    int totalDirectories;  
    int updateCounter;  
    bool isSearching;  
    bool firstSearch;  
    bool isStopping;  
    static QVector<QString> filesBatch;  
  
    QThreadPool *threadPool;  
    QElapsedTimer timer;  
    QSet<QString> uniquePaths;  
    QSet<QString> uniqueFiles;  
    QQueue<QString> *taskQueue;  
    QMutex *queueMutex;  
    QWaitCondition *queueCondition;  
    QMutex uniqueFilesMutex;  
  
    FileIndexDatabase *db;  
    DatabaseThread *dbThread;  
};  
  
#endif // FILESEARCHCORE_H
```

## 3.2 信号与槽的合理应用

在重构过程中，充分利用了 Qt 的信号与槽机制。`FileSearchCore` 中的文件找到信号 `fileFound` 被用来通知 `FileSearch` 更新 UI。这一改变实现了以下几点：

- **解耦合**：`FileSearchCore` 不再直接与 UI 组件交互，降低了与 UI 的耦合性。
- **增强可扩展性**：将来可以轻松添加新的 UI 组件或更换 UI 逻辑，而不需要修改核心搜索逻辑。

```C
// 在 FileSearchCore 中发出信号
emit fileFound(filePath);

// 在 FileSearch 中连接信号
connect(fileSearchCore, &FileSearchCore::fileFound, this, &FileSearch::onFileFound);

```

通过这种方式，`FileSearchCore` 的逻辑与 UI 更新分开，减少了系统整体的耦合度。

然而修改了 UI 更新的思想逻辑后，也带来了一些新的问题，如：
1. 批量更新搜索文件功能缺失
2. 现在的代码完全基于数据库搜索，如何平衡数据库搜索与遍历文件系统
3. 如何高效地创建于定时更新数据库
4. 搜索结果显示错误，只要路径中含有 keyword 就会被显示
5. 如何合理的设计索引表，即如何把文件书转化为关系型数据库，要能够在不占用过多磁盘空间的前提下，设计出一种便于搜索的数据表
6. 在程序启动时，要能对数据库进行判断，是建立新的文件索引数据库，或者是检查更新
7. 数据库安全问题
8. ……
不过这个问题主要是由于搜索逻辑改变顺带形成的，将会在增加数据库文章中，进行详细介绍。