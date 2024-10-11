---
title: FileTAG 中的多线程
date: 2024/10/09
tags:
  - cpp
  - QT
categories:
  - C++
description: 
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
poster:
  topic: 
  headline: FileTAG 中的多线程
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
# 前言

之前问过“雪豹”，有什么推荐的 C++ 学习课程，他说没有，**都是东一点西一点，慢慢积累的** 。通过这次项目的开发，我还是深有感触的。

早在操作系统的课程中，就学习过 **进程、死锁、消息队列、调度算法** 这些内容，可是知道实际任务中，才能够真的理解这些概念。

本文结合 FileTAG 的开发过程，详细阐述本人的多线程学习路径以及相关知识点。

好了，正文开始。

# 1. 多线程初探：分离搜索线程与主界面UI线程

这个在之前的文章写过，这里就不做过多叙述，参见[多线程初探：在Qt中实现多线程文件搜索](https://www.montylee.cn/2024/07/18/%E5%A4%9A%E7%BA%BF%E7%A8%8B%E5%88%9D%E6%8E%A2/)


> 但是写文章埋的坑也是填上了。

在这一部分，主要涉及到两个线程：
1. **主线程（GUI线程）**：负责处理用户界面和用户交互；
2. **文件搜索线程（工作线程）**：负责执行耗时的文件搜索操作。

**通过线程分离的操作，很好的解决了文件搜索过程中，出现的UI界面卡顿问题。**

# 2. 数据竞争（Race Condition）

在多线程编程当中，不可避免的会涉及到数据竞争问题，即**多个线程同时访问或修改同一资源**。

举一个简单的例子，如下：

```C
int counter = 0;

void increment() {
    for (int i = 0; i < 1000; ++i) {
        counter++; // 可能出现数据竞争
    }
}

void decrement() {
    for (int i = 0; i < 1000; ++i) {
        counter--; // 可能出现数据竞争
    }
}

```

上面的代码中，如果分别开辟两个线程，执行 `increment()` 与 `decrement()`，对共享变量 `counter` 进行操作，会导致 `counter` 的值不确定 。这是因为 `counter++` 和 `counter--` 不是原子操作，它们实际上是多个操作的组合，可能会在两线程之间交错执行。

解决数据竞争问题的方法有很多，如：互斥锁、读写锁、原子操作、线程局部存储、消息传递和避免共享状态等。

关于互斥锁和条件变量的使用，具体案例可以看这篇[Logger 类的实现与改进](https://www.montylee.cn/2024/10/07/Logger%20%E7%B1%BB%E7%9A%84%E5%AE%9E%E7%8E%B0%E4%B8%8E%E6%94%B9%E8%BF%9B/)

## 互斥锁
在这里简单地介绍一下，

```C
void Logger::log(const QString &message) {
    {
        QMutexLocker locker(&mutex); // 锁定互斥锁
        logQueue.enqueue(message);  // 将消息放入队列
    } // 互斥锁自动解锁

    condition.wakeOne();  // 唤醒工作线程
}

void Logger::run() {
    while (running) {
        QString message;

        {
            QMutexLocker locker(&mutex); // 锁定互斥锁
            if (logQueue.isEmpty()) {
                condition.wait(&mutex);  // 如果队列为空，等待唤醒
            }
            if (!logQueue.isEmpty()) {
                message = logQueue.dequeue();  // 从队列中取出消息
            }
        } // 互斥锁自动解锁

        // 处理和写入日志的代码
    }
}

```

- 代码中定义了一个 `QMutex` 类型的成员变量 `mutex`，用于保护对共享资源（如 `logQueue` 和 `running`）的访问。
- 在 `log` 和 `run` 方法中，使用 `QMutexLocker` 来自动锁定和解锁 `mutex`。这样可以确保在访问 `logQueue` 和 `running` 时，只有一个线程可以进入临界区，从而避免数据竞争。

## 条件变量

```C
void Logger::log(const QString &message) {
    {
        QMutexLocker locker(&mutex);
        logQueue.enqueue(message);  // 将消息放入队列
    }
    condition.wakeOne();  // 唤醒工作线程
}

```

- 使用 `QWaitCondition` 类型的成员变量 `condition` 来管理线程的唤醒和等待。在 `log` 方法中，如果 `logQueue` 中有新消息，工作线程会被唤醒；如果队列为空，工作线程会等待。
- 这样确保了只有在有消息可处理时，工作线程才会尝试从队列中取出消息，从而避免不必要的忙等待。


# 3. 基于线程池实现文件搜索

在项目中，主要是使用了`Qt`的多线程机制来提高搜索性能。
* 使用了`QThreadPool`来管理线程，确保最大化资源利用，同时通过`QQueue`作为任务队列来存储待搜索的目录路径；
* 为了保证线程安全，我们引入了`QMutex`和`QWaitCondition`来同步对共享资源的访问；
* 此外，使用Qt的信号和槽机制来实现线程间的通信，确保在找到文件时及时更新UI，提供良好的用户体验。

## 线程池（`QThreadPool`）

线程池是一种管理线程的高效方式，允许多个线程同时运行，避免频繁创建和销毁线程带来的性能开销。在项目中，使用了Qt的 `QThreadPool` 来实现这一点。

> 推荐学习视频 [# 线程池原理与实现](https://www.bilibili.com/video/BV1sk4y1P7UM/?spm_id_from=333.337.search-card.all.click&vd_source=f30eba35d0a8915376778596dfd73224)
> 博客：[C++ 线程池](https://wangpengcheng.github.io/2019/05/17/cplusplus_theadpool/)

线程池可以看做由三个主要部分组成：**任务队列（Task Queue）、线程池（Thread Pool）和完成队列（Completed Tasks）**。下面我将结合我的代码分别进行描述：

### 任务队列

在代码中，任务队列使用了 `QQueue<QString>` 来存储待搜索的目录路径。这个队列允许多个线程从中获取任务，实现并行处理。任务队列的主要目的是管理待处理的任务，使得线程可以在执行时灵活地从队列中获取任务。

```C
taskQueue = new QQueue<QString>();
```

任务队列具有入队和出队两个操作，在代码中的具体体现为：

* **入队操作**：在 `enqueueDirectories` 方法中，将待搜索的目录路径添加到任务队列中。这里的关键是要确保添加操作是线程安全的。
* 
```C
if (!uniquePaths.contains(subDirPath)) {
    uniquePaths.insert(subDirPath);
    taskQueue->enqueue(subDirPath); // 将任务添加到队列
    totalDirectories++;
}

```

* **出队操作**： 在线程执行时，线程会尝试从任务队列中取出任务。在 `FileSearchThread::run()` 方法中，我们使用 `QMutexLocker` 确保在访问任务队列时的线程安全。

```C
{
    QMutexLocker locker(queueMutex);
    if (taskQueue->isEmpty()) {
        if (stopped) {
            break;
        }
        queueCondition->wait(queueMutex); // 如果队列为空，等待
        continue;
    }
    searchPath = taskQueue->dequeue(); // 从队列中取出任务
}

```

### 线程池

线程池的实现通过 `QThreadPool` 类完成。代码中创建了一个线程池实例，并设置其最大线程数为系统推荐的理想线程数。这样做的目的是在高负载情况下优化资源的利用率。

```C
threadPool = new QThreadPool(this);
threadPool->setMaxThreadCount(QThread::idealThreadCount());
```

在 `FileSearch::onSearchButtonClicked()` 方法中，根据线程池的最大线程数创建并启动多个 `FileSearchThread` 实例。每个线程实例都会接收搜索关键词、任务队列、互斥锁和条件变量。

```C
for (int i = 0; i < threadPool->maxThreadCount(); ++i) {
    FileSearchThread *task = new FileSearchThread(searchKeyword, taskQueue, queueMutex, queueCondition);
    connect(task, &FileSearchThread::fileFound, this, &FileSearch::onFileFound);
    connect(task, &FileSearchThread::searchFinished, this, &FileSearch::onSearchFinished);
    threadPool->start(task); // 启动线程
    activeTaskCount++;
}
```


### 完成队列

在代码中，没有明确使用单独的“完成队列”来存储完成的任务，但可以通过对 `filesBatch` 变量的更新来视为一种完成队列。`filesBatch` 是一个静态成员变量，用于存储在搜索过程中找到的文件路径。

- **记录找到的文件**： 在线程执行过程中，当找到符合搜索条件的文件时，线程会将文件路径添加到 `filesBatch` 中。pp
    ```C
    if (!uniqueFiles.contains(filePath)) {
    uniqueFiles.insert(filePath);
    filesBatch.append(filePath); // 添加到完成队列
}

    ```
- **批量更新UI**： 在 `onFileFound` 方法中，根据 `filesBatch` 中的内容更新UI。为了避免频繁更新，我们在文件数量不足500时直接更新UI；超过500时，每1000次更新一次。
    ```C
    if (firstSearch || filesBatch.size() < 500) {
    QVector<QString> filesBatchCopy = filesBatch;
    filesBatch.clear(); // 清空完成队列

    // 执行UI更新
    auto updateUI = [this, filesBatchCopy]() {
        // 更新表格视图模型
    };
    QMetaObject::invokeMethod(this, updateUI, Qt::QueuedConnection);
    firstSearch = false;
}

    ```

## 线程安全

线程安全主要是通过互斥锁来实现的，在上面的内容中已经进行了叙述。

## 线程通信

在多线程环境中，线程之间的通信至关重要，尤其是在处理需要更新UI的任务时。Qt的信号和槽机制提供了一种高效且灵活的线程间通信方式。

- 信号的定义与发射

在文件搜索线程中，当找到文件时会发出 `fileFound` 信号，以便主线程能够及时接收找到的文件路径：

```C
emit fileFound(filePath);
```

- 信号槽的实现

通过连接信号与槽，我们能够在找到文件时调用相应的处理函数。例如，在 `FileSearch::onSearchButtonClicked()` 方法中，我们将 `fileFound` 信号连接到 `onFileFound` 槽：

```C
connect(task, &FileSearchThread::fileFound, this, &FileSearch::onFileFound);
```


- 确保 UI 线程安全更新

为了安全地更新UI，我们在找到文件后使用 `QMetaObject::invokeMethod()` 来在主线程中执行UI更新。这确保了UI更新不会在工作线程中直接执行，从而避免潜在的线程安全问题：

```C
QMetaObject::invokeMethod(this, updateUI, Qt::QueuedConnection);

```



# 多线程优化

关于优化的过程，实际上也就是我开发的过程，或者说就是上述文字中的技术栈，包括：
1. 使用线程池管理多线程，提高并发行能
2. 任务队列与多线程处理，避免阻塞
3. 条件变量避免忙等待
4. 分批处理和异步更新UI，提升用户体验
5. 文件搜索过程中的事件循环处理
6. 停止机制优化
7. 多线程的日志管理

这里在提一下之前没有提到的几点：

## 文件搜索过程中的事件循环处理

在文件搜索任务中，遍历文件系统可能会花费较长时间，尤其当搜索范围较大时，应用程序可能会出现卡顿或无响应的情况。这是因为长时间的阻塞操作会占用主线程（尤其是GUI主线程）的处理能力，使得应用无法及时响应用户的交互请求。

为了解决这一问题，代码中引入了 `QEventLoop` 来处理事件循环。通过在文件搜索过程中周期性地处理事件，确保即使在执行耗时操作时，应用程序仍然可以响应用户的输入等事件。

```C
QEventLoop loop;
while (it.hasNext() && !stopped) {
    QString filePath = it.next();
    QString fileName = it.fileName();

    if (fileName.contains(searchKeyword, Qt::CaseInsensitive)) {
        emit fileFound(filePath); // 找到文件后发出信号
    }

    loop.processEvents(QEventLoop::AllEvents, 50); // 保持事件响应
}

```



## 停止机制优化

在文件搜索任务中，用户可能希望随时中断搜索操作，而不是等搜索任务全部完成。这要求程序具备一个可靠且高效的机制，允许用户停止任务，并确保在任务停止时释放所有资源，避免产生“僵尸线程”或资源泄漏。

**优化方式：通过标志变量和互斥锁实现安全停止**

在代码中，搜索线程的停止通过 `stopped` 标志变量和互斥锁 (`QMutex`) 实现，确保线程在接收到停止信号时能够安全退出。

```C
// 停止线程
void FileSearchThread::stop() {
    stopped = true; // 设置停止标志，表示线程需要停止
}

// 在线程中检查停止标志
while (it.hasNext() && !stopped) {
    QString filePath = it.next();
    QString fileName = it.fileName();

    if (fileName.contains(searchKeyword, Qt::CaseInsensitive)) {
        emit fileFound(filePath); // 找到文件后发出信号
    }

    loop.processEvents(QEventLoop::AllEvents, 50); // 处理事件，保持响应
}

// 搜索任务的停止逻辑
void FileSearch::stopAllTasks() {
    QMutexLocker locker(queueMutex); // 加锁，确保停止操作是线程安全的
    isStopping = true; // 标记为正在停止
    while (!taskQueue->isEmpty()) {
        taskQueue->dequeue(); // 清空任务队列，防止新任务继续执行
    }
    queueCondition->wakeAll(); // 唤醒所有等待任务的线程
}

```


使用标志位 `stopped`、互斥锁 `QMutex` 和条件变量 `QWaitCondition`，实现了安全、优雅的线程停止，确保资源被正确释放，同时避免线程资源泄漏或无响应状态。

## 动态任务分配与任务队列

在文件搜索的多线程任务中，可能会遇到这样的情况：有些线程处理的文件夹路径较深，文件数量较多，导致这些线程需要更长的时间完成任务，而其他线程可能只需要搜索较浅的目录或文件较少的目录，较快地完成任务。为了避免这种工作分配不均，代码采取了一些优化措施，使任务分配更加均衡，线程资源利用更加高效。

为了应对这种问题，代码通过 **任务队列** 和 **动态任务分配** 的方式，确保线程处理工作负载时能够均衡分配，避免某些线程过度繁忙，某些线程过早完成任务。

1. 使用任务队列进行任务分配

代码通过 `QQueue<QString>` 作为任务队列来存储待搜索的文件夹路径。所有线程从同一个任务队列中取出任务进行处理，这样即使某个线程搜索的文件夹很深且包含大量文件，它也不会占用过多的时间，因为任务队列中仍然有其他待处理的文件夹，其他空闲的线程可以继续从任务队列中获取新的任务。

```C
taskQueue = new QQueue<QString>();  // 定义任务队列
queueMutex = new QMutex();          // 互斥锁保护任务队列
queueCondition = new QWaitCondition(); // 条件变量

```

通过这个任务队列，文件夹搜索任务不再是一次性分配，而是 **按需动态分配**。任何线程处理完当前任务后，都可以从队列中获取新的任务继续执行。

2. 动态任务分发

每个线程从任务队列中 **动态获取任务**，通过互斥锁确保线程安全地访问队列。在文件搜索的主循环中，每个线程从任务队列中取出一个目录进行处理。如果一个线程完成了某个目录的搜索，它会继续获取下一个任务，直到队列为空。这样，即使某个线程分配到的目录结构较复杂，任务队列的动态任务分发可以让其他线程继续工作，而不是等待所有任务一次性分配完毕。

```C
void FileSearchThread::run() {
    while (true) {
        QString searchPath;
        {
            QMutexLocker locker(queueMutex);  // 加锁，安全访问任务队列
            if (taskQueue->isEmpty()) {
                if (stopped) {
                    break; // 如果任务队列为空且停止标志为真，退出
                }
                queueCondition->wait(queueMutex); // 等待任务
                continue;
            }
            searchPath = taskQueue->dequeue();  // 从任务队列取任务
        }

        // 对取出的目录进行搜索处理
        if (!searchPath.isEmpty()) {
            Logger::instance().log("线程开始：" + searchPath);
            QDirIterator it(searchPath, QDir::Files | QDir::Dirs | QDir::NoDotAndDotDot, QDirIterator::Subdirectories);
            QEventLoop loop;
            while (it.hasNext() && !stopped) {
                QString filePath = it.next();
                QString fileName = it.fileName();

                if (fileName.contains(searchKeyword, Qt::CaseInsensitive)) {
                    emit fileFound(filePath);  // 找到文件后发送信号
                }
                loop.processEvents(QEventLoop::AllEvents, 50);  // 保持事件响应
            }
            emit searchFinished();  // 任务完成，发出信号
            Logger::instance().log("线程结束：" + searchPath);
        }
    }
}

```

3. 任务入队（递归添加目录）

当搜索某个目录时，代码不仅会搜索当前目录，还会将子目录递归地加入任务队列中。这样深层目录会被逐渐分解成多个任务，这些任务可以被其他线程并行处理，进一步减轻某个线程因为处理深层目录而过度忙碌的问题。

```C
void FileSearch::enqueueDirectories(const QString &path, int depth) {
    QDirIterator dirIt(path, QDir::Dirs | QDir::NoDotAndDotDot, QDirIterator::NoIteratorFlags);
    while (dirIt.hasNext()) {
        dirIt.next();
        QString subDirPath = dirIt.filePath();
        if (!uniquePaths.contains(subDirPath)) {  // 确保目录唯一
            uniquePaths.insert(subDirPath);
            taskQueue->enqueue(subDirPath);  // 子目录作为新任务加入队列
            totalDirectories++;

            if (depth > 1) {  // 如果递归深度允许，继续将子目录的子目录入队
                QDirIterator subDirIt(subDirPath, QDir::Dirs | QDir::NoDotAndDotDot, QDirIterator::NoIteratorFlags);
                while (subDirIt.hasNext()) {
                    subDirIt.next();
                    QString subSubDirPath = subDirIt.filePath();
                    if (!uniquePaths.contains(subSubDirPath)) {
                        uniquePaths.insert(subSubDirPath);
                        taskQueue->enqueue(subSubDirPath);  // 子目录的子目录也入队
                        totalDirectories++;
                    }
                }
            }
        }
    }
}

```

