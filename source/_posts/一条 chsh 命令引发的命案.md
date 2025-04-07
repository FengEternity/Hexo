---
title: 一条 chsh 命令引发的命案
date: 2025/4/7
tags:
  - 终端
  - Shell
  - PTY
categories:
  - linux
cover: https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/resource-8526a92ba76ef090a62109a6-76851.jpg?imageSlim
katex: true
mathjax: true
author: Montee
type: tech
description: 本文讲述了作者因混淆终端、终端模拟器和Shell的概念，错误地将Kitty终端模拟器设置为默认Shell，导致问题。文章解释了终端模拟器和伪终端（PTY）的区别，并提供了相关命令和解决方案。作者反思了对概念理解的重要性。
---
# 起因

首先列出罪魁祸首：

```bash
sudo chsh -s /Applications/kitty.app/Contents/MacOS/kitty $USER
```

事情的起因是我通过`腾讯元宝`辅助我配置Mac的终端，我想要将默认的 shell 修改为 kitty，但是由于我**混淆了 terminal 、 shell 以及终端模拟器之间的概念**，对 AI 进行了错误的提问，进而引发了这个问题。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407204842669.png?imageSlim)


# 问题分析

```bash
sudo chsh -s /Applications/kitty.app/Contents/MacOS/kitty $USER
```
重新来看一下这条命令，事实上我想要实现的是将 Kitty 这一终端模拟器设置为我的默认登陆 shell，但**Kitty 并非 Shell**，​Kitty 是终端模拟器，负责提供图形化终端界面，而 Shell（如 Zsh、Bash）是命令解释器。两者的功能不同，直接替换导致了以下问题：

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407210034630.png?imageSlim)

## 概念区分
> [理解 Linux 终端、终端模拟器和伪终端的区别](https://xie.infoq.cn/article/a6153354865c225bdce5bd55e)
> 本章节大量参考 *~~（抄袭）~~* 上文 


### 概述

```plainText
用户输入 → 终端模拟器 → Shell → 操作系统内核 → 执行结果 → Shell → 终端模拟器 → 显示输出
```

- **终端模拟器**作为中间层，负责与图形界面交互。
- ​**Shell**作为命令解释器，处理具体逻辑

### 终端模拟器

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407212644352.png?imageSlim)

现在我们用 **TTY** 代表计算机终端（**terminal**），只是沿用了历史习惯，电传打字机（**teletypewriter**）曾经是计算机的终端，它的缩写便是 **TTY**(**T**ele**TY**pewriter)，其作用就是将用户的输入数据发送到计算机，并打印出响应。


而计算机发展至今，终端不再是一个需要通过 UART（Universal Asynchronous Receiver and Transmitter，通用异步接收和发送器） 连接到计算机上物理设备。终端成为内核的一个模块，它可以直接向 TTY 驱动发送字符，并从 TTY 驱动读取响应然后打印到屏幕上。也就是说，用内核模块模拟物理终端设备，因此被称为**终端模拟器**(terminal emulator)。

**line discipline** 负责转换特殊字符（如退格、擦除字、清空行），并将收到的内容回传给电传打字机，以便用户可以看到输入的内容。**line discipline** 还负责对字符进行缓冲，当按下回车键时，缓冲的数据被传递给与 `TTY` 相关的前台用户进程。用户可以并行的执行几个进程，但每次只与一个进程交互，其他进程在后台工作。

上图是一个典型的 Linux 桌面系统。终端模拟器就像过去的物理终端一样，它监听来自键盘的事件将其发送到 TTY 驱动，并从 TTY 驱动读取响应，通过显卡驱动将结果渲染到显示器上。TTY 驱动 和 **line discipline** 的行为与原先一样，但不再有 UART 和 物理终端参与。

```bash
$ tty
/dev/ttys000
```

`tty` 命令用于**显示当前 Shell 进程所连接的终端设备路径**，执行该命令得到的结果中`ttyS` 前缀通常表示**串行终端（Serial Terminal）**，`s000`表示串口设备，即**图形界面下的终端模拟器可能映射到虚拟串口设备**。

可以使用下面的命令来进行验证查询：

```bash
# 查看终端类型
echo $TERM
# 输出示例：xterm-256color（表示图形终端模拟器）

# 查看终端设备属性
stty -a < /dev/ttys000

# 将日志输出到当前终端
echo "Test" > /dev/ttys000
```

### 伪终端（pseudo terminal, PTY）
**终端模拟器(terminal emulator)** 是运行在内核的模块，我们也可以让终端模拟程序运行在用户区。运行在用户区的终端模拟程序，就被称为**伪终端（pseudo terminal, PTY）**。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407214433801.png?imageSlim)
**终端模拟器(terminal emulator)** 是运行在内核的模块，我们也可以让终端模拟程序运行在用户区。**运行在用户区的终端模拟程序**，就被称为**伪终端（pseudo terminal, PTY）**。

### shell

位于操作系统内核与用户之间的命令解释器，负责解析用户输入的命令并调用内核执行

> [计算机教育缺失的一课 第一讲 课程概览与shell](https://www.bilibili.com/video/BV1uc411N7eK/?spm_id_from=333.788.recommend_more_video.-1&vd_source=f30eba35d0a8915376778596dfd73224)
# 问题的解决



# 一点思考
