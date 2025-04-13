---
title: Qt实现关闭主窗口时也关闭其他所有窗口
date: 2024/07/20
tags:
  - cpp
  - QT
categories:
  - 项目开发
description: Qt实现关闭主窗口时也关闭其他所有窗口
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
poster:
  headline: Qt实现关闭主窗口时也关闭其他所有窗口
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

> 总结起来就是一句话，重写 mainwindow 的 `closeEvent` 事件，使其调用父类的`closeEvent`


在开发基于 Qt 的应用程序时，有时需要在关闭主窗口时同时关闭所有其他窗口。本文将介绍如何通过信号和槽机制实现这一功能。

# 步骤一：定义自定义信号

首先，在主窗口类（例如 `MainWindow`）中定义一个自定义信号 `mainWindowClosed`。这个信号将在主窗口关闭时发出。

```cpp
// mainwindow.h
class MainWindow : public QMainWindow {
Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

signals:
    void mainWindowClosed();  // 添加自定义信号

protected:
    void closeEvent(QCloseEvent *event) override;  // 重载closeEvent
};
```

# 步骤二：发出信号

在主窗口类的 `closeEvent` 方法中，发出 `mainWindowClosed` 信号。这是在用户关闭主窗口时触发的。

```cpp
// mainwindow.cpp
void MainWindow::closeEvent(QCloseEvent *event) {
    emit mainWindowClosed();  // 发出自定义信号
    QMainWindow::closeEvent(event);  // 调用父类的 closeEvent 方法
}
```

## 父类解释

在 `QMainWindow` 类中，`closeEvent` 是一个虚函数，它重载了 `QWidget` 类中的 `closeEvent` 函数。因此，当你调用 `QMainWindow::closeEvent(event);` 时，实际上是调用了 `QWidget` 类的 `closeEvent` 方法。

### 继承关系

`QMainWindow` 类是从 `QWidget` 类继承而来的，`QWidget` 是 Qt 框架中所有可视化组件的基类。具体继承关系如下：

- `QObject`
  - `QWidget`
    - `QFrame`
      - `QAbstractScrollArea`
        - `QMainWindow`

### 调用父类的方法

当你在一个子类中重载了一个虚函数（例如 `closeEvent`），但仍希望在重载的函数中调用父类的实现，可以使用 `父类名::函数名` 的形式来调用父类的实现。这样做可以确保父类中定义的行为仍然会被执行。

在 `QMainWindow` 中调用 `closeEvent` 的实现就是调用其父类 `QWidget` 的 `closeEvent` 实现：

```cpp
void MainWindow::closeEvent(QCloseEvent *event) {
    emit mainWindowClosed();  // 发出自定义信号
    QMainWindow::closeEvent(event);  // 调用父类的 closeEvent 方法
}
```

这里的 `QMainWindow::closeEvent(event)` 实际上是调用 `QWidget` 中的 `closeEvent` 方法，因为 `QMainWindow` 并未重载 `closeEvent` 方法，它直接使用了从 `QWidget` 继承的实现。

### `QWidget` 的 `closeEvent` 实现

`QWidget` 的 `closeEvent` 方法负责处理窗口关闭事件。当用户尝试关闭窗口时，Qt 会生成一个 `QCloseEvent` 对象并将其传递给 `closeEvent` 方法。默认情况下，`QWidget` 的 `closeEvent` 方法会处理此事件并关闭窗口。如果你希望在关闭窗口时执行额外的操作，可以在子类中重载此方法，并在合适的位置调用父类的实现。


# 步骤三：连接信号和槽

在 `main.cpp` 中，将主窗口的 `mainWindowClosed` 信号连接到其他窗口的关闭槽函数。例如，如果有一个关于窗口（`About`），可以将主窗口的关闭信号连接到关于窗口的 `close` 槽。

```cpp
// main.cpp
int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    MainWindow mainWindow;
    mainWindow.show();

    std::unique_ptr<About> aboutWindow = std::make_unique<About>();

    // 连接主窗口的关闭信号到关于窗口的关闭槽
    QObject::connect(&mainWindow, &MainWindow::mainWindowClosed, aboutWindow.get(), &QWidget::close);

    return app.exec();
}
```

# 工作原理

1. **定义信号**：在主窗口类中定义一个自定义信号 `mainWindowClosed`。
2. **发出信号**：当主窗口接收到关闭事件时（即用户点击关闭按钮或调用 `close()` 方法），重载的 `closeEvent` 方法会发出 `mainWindowClosed` 信号。
3. **连接信号和槽**：在 `main.cpp` 中，将主窗口的 `mainWindowClosed` 信号连接到其他窗口的关闭槽函数。这样，当主窗口关闭时，`mainWindowClosed` 信号会被触发，继而调用其他窗口的关闭槽函数，使它们也关闭。

### 总结

通过上述步骤，我们可以确保在用户关闭主窗口时，应用程序的其他窗口也会被关闭。这种方法利用了 Qt 的信号和槽机制，确保了窗口间的通信和同步关闭。通过定义自定义信号并在适当的时机发出，再将信号连接到目标窗口的关闭槽，可以方便地实现这一功能。