---
title: 改进多线程管理：解决 activeTaskCount 计数问题
date: 2024/10/20
tags:
  - cpp
  - 计算机
  - debug
  - 多线程
categories:
  - debug
description: 改进多线程管理：解决 activeTaskCount 计数问题
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/unnamed.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/unnamed.jpg
poster:
  topic: 
  headline: 改进多线程管理：解决 activeTaskCount 计数问题
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

# 问题描述

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241020152021.png)



从打印的 log 信息来看，所有线程均结束了搜索任务，但是并没有结束搜索任务。

  

# 问题分析

首先定位到搜索任务结束的代码位置，如下图所示；

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241020152034.png)


从代码中可以看到，结束任务由`activeTaskCount` 变量和任务队列来控制，任务队列是 QTherd 库实现的接口函数，所以先对自定义的`activeTaskCount` 变量进行分析查看。

## activeTaskcount

分析原代码可知，`activeTaskCount` 具体工作原理：

1. 初始化与启动线程增加计数
    
    1. 在 `onSearchButtonClicked` 函数中，当开始搜索时，`activeTaskCount` 被初始化为 `0`。
        
    2. 每当创建并启动一个 `FileSearchThread` 对象时，`activeTaskCount` 就加 `1`。
        
    3. 代码如下：
        
    
    ```C++
    for (int i = 0; i < threadPool->maxThreadCount(); ++i) {
        // 创建线程并连接信号槽
        FileSearchThread *task = new FileSearchThread(searchKeyword, taskQueue, queueMutex, queueCondition);
        connect(task, &FileSearchThread::fileFound, this, &FileSearch::onFileFound);
        connect(task, &FileSearchThread::searchFinished, this, &FileSearch::onSearchFinished);
        threadPool->start(task);
        activeTaskCount++;
    }
    ```
    
2. 线程完成任务时减少计数
    
    1. 当一个搜索线程完成一个搜索任务并触发 `searchFinished` 信号时，会调用 `onSearchFinished` 槽函数。
        
    2. 在 `onSearchFinished` 中，`activeTaskCount` 减 `1`，表示这个线程已经完成它的工作。
        
    3. 代码如下：
        
    
    ```C++
    void FileSearch::onSearchFinished() {
        QMutexLocker locker(queueMutex);
        activeTaskCount--;
        progressBar->setValue(progressBar->value() + 1);
        updateProgressLabel();
    
        // 如果所有任务都完成了且任务队列为空，调用 finishSearch()
        if (activeTaskCount == 0 && taskQueue->isEmpty()) {
            finishSearch();
            qint64 elapsedTime = timer.elapsed();
            onSearchTime(elapsedTime);
            progressBar->setValue(totalDirectories);
            updateProgressLabel();
            isSearching = false;
        }
    }
    ```
    

然而，`activeTaskCount` 的计数方式存在逻辑问题。当前代码在 `FileSearchThread` 完成一个任务并触发 `searchFinished` 时，直接减少 `activeTaskCount`，然而这些线程会在任务队列中继续消费新的任务。这样就会导致 `activeTaskCount` 变得不准确，因为它没有考虑到同一个线程可能处理多个任务的情况。

从下面日志打印可以明显的看出来：

![image.png](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20241020152102.png)




# 解决方法

- 确保每次线程从任务队列中取出新任务时，`activeTaskCount` 正确增加。
    
- 每当一个任务完成时，`activeTaskCount` 减少，只有当所有任务都完成时才停止搜索。
    
- 增加日志记录，帮助监控 `activeTaskCount` 的变化过程，以及线程在不同状态下的行为。
    

## 具体实现

1. 添加 `taskStarted` 信号
    

首先，我们在 `FileSearchThread` 类中添加了一个 `taskStarted` 信号。每次线程从任务队列中取出一个新任务时，发出该信号，以便主线程更新 `activeTaskCount`。

cpp

复制代码

```C++
// FileSearchThread.h
signals:
    void taskStarted();
```

在 `FileSearchThread::run()` 方法中，当线程从队列中取出一个新任务时，发出 `taskStarted` 信号：

```C++
void FileSearchThread::run() {
    while (true) {
        QString searchPath;
        {
            QMutexLocker locker(queueMutex);
            if (taskQueue->isEmpty()) {
                if (stopped) {
                    Logger::instance().log("线程停止，退出运行循环");
                    break;
                }
                Logger::instance().log("任务队列为空，线程等待中...");
                queueCondition->wait(queueMutex);
                continue;
            }
            searchPath = taskQueue->dequeue();

            // 发出信号，通知主线程增加 activeTaskCount
            emit taskStarted();
        }

        if (searchPath.isEmpty()) {
            continue;
        }

        Logger::instance().log("线程开始处理任务：" + searchPath);
        // 文件搜索逻辑...
        emit searchFinished();
        Logger::instance().log("线程结束处理任务：" + searchPath);
    }
}
```

2. 更新 `activeTaskCount`
    

在 `FileSearch` 类中增加了一个 `onTaskStarted` 槽函数，用于在接收到 `taskStarted` 信号时增加 `activeTaskCount`。

```C++
void FileSearch::onTaskStarted() {
    QMutexLocker locker(queueMutex);
    activeTaskCount++;
    Logger::instance().log("任务开始, activeTaskCount 增加到: " + QString::number(activeTaskCount));
}
```

同时，`onSearchFinished` 函数保持不变，每当线程完成任务时，减少 `activeTaskCount`：

```C++
void FileSearch::onSearchFinished() {
    QMutexLocker locker(queueMutex);
    activeTaskCount--;
    Logger::instance().log("任务完成, activeTaskCount 减少到: " + QString::number(activeTaskCount));
    progressBar->setValue(progressBar->value() + 1);
    updateProgressLabel();

    if (activeTaskCount == 0 && taskQueue->isEmpty()) {
        Logger::instance().log("所有任务完成，进入 finishSearch()");
        finishSearch();
        qint64 elapsedTime = timer.elapsed();
        onSearchTime(elapsedTime);
        progressBar->setValue(totalDirectories);
        updateProgressLabel();
        isSearching = false;
    }
}
```

3. 增加日志记录
    

为了方便调试和监控，我们在以下位置添加了日志：

- `onTaskStarted()` 和 `onSearchFinished()` 中，记录 `activeTaskCount` 的变化。
    
- `FileSearchThread::run()` 中，在线程等待新任务和退出时添加日志，帮助了解线程状态。
    
- `onSearchButtonClicked()` 中，记录搜索启动时的初始化状态。
    

# 新的问题

让我们回溯到最初的`activeTaskCount` 初始化逻辑：

```C++
for (int i = 0; i < threadPool->maxThreadCount(); ++i) {
    // 创建线程并连接信号槽
    FileSearchThread *task = new FileSearchThread(searchKeyword, taskQueue, queueMutex, queueCondition);
    connect(task, &FileSearchThread::fileFound, this, &FileSearch::onFileFound);
    connect(task, &FileSearchThread::searchFinished, this, &FileSearch::onSearchFinished);
    threadPool->start(task);
    activeTaskCount++;
}
```

每当创建并启动一个 `FileSearchThread` 对象时，`activeTaskCount` 就加 `1`。

然而，实际上这个变量是件事处理中的任务的，并不是线程，所以只要把这里的 `activeTaskCount++` 删掉就好了。
