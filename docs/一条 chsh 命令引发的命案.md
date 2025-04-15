---

## title: 一条 chsh 命令引发的命案  
date: 2025/4/7  
tags:  
  - 终端  
  - Shell  
  - 交流重要性  
  - 数据备份  
categories: [技术学习]  
cover: [https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/resource-8526a92ba76ef090a62109a6-76851.jpg?imageSlim](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/resource-8526a92ba76ef090a62109a6-76851.jpg?imageSlim)  
katex: true  
mathjax: true  
author: Montee  
type: tech  
description: "本文讲述了作者因混淆终端、终端模拟器和Shell的概念，错误地将Kitty终端模拟器设置为默认Shell，导致问题。文章解释了终端模拟器和伪终端（PTY）的区别，并提供了相关命令和解决方案。作者反思了对概念理解的重要性，并强调了正确与AI交流、数据备份和交流的重要性。"
# 1. 起因
首先列出罪魁祸首：

```bash
sudo chsh -s /Applications/kitty.app/Contents/MacOS/kitty $USER
```

事情的起因是我通过`腾讯元宝`辅助我配置Mac的终端，我想要将默认的 shell 修改为 kitty，但是由于我**混淆了 terminal 、 shell 以及终端模拟器之间的概念**，对 AI 进行了错误的提问，进而引发了这个问题。

![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407204842669.png?imageSlim)



# 2. 问题分析
```bash
sudo chsh -s /Applications/kitty.app/Contents/MacOS/kitty $USER
```

重新来看一下这条命令，事实上我想要实现的是将 Kitty 这一终端模拟器设置为我的默认登陆 shell，但**Kitty 并非 Shell**，Kitty 是终端模拟器，负责提供图形化终端界面，而 Shell（如 Zsh、Bash）是命令解释器。两者的功能不同，直接替换导致了以下问题：

![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407210034630.png?imageSlim)

## 2.1 概念区分
> [理解 Linux 终端、终端模拟器和伪终端的区别](https://xie.infoq.cn/article/a6153354865c225bdce5bd55e)  
本章节大量参考 ~~_（抄袭）_~~ 上文 
>

### 2.1.1 概述
```plain
用户输入 → 终端模拟器 → Shell → 操作系统内核 → 执行结果 → Shell → 终端模拟器 → 显示输出
```

+ **终端模拟器**作为中间层，负责与图形界面交互。
+ **Shell**作为命令解释器，处理具体逻辑

### 2.1.2 终端模拟器
![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407212644352.png?imageSlim)

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

### 2.1.3 伪终端（pseudo terminal, PTY）
**终端模拟器(terminal emulator)** 是运行在内核的模块，我们也可以让终端模拟程序运行在用户区。运行在用户区的终端模拟程序，就被称为**伪终端（pseudo terminal, PTY）**。

![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250407214433801.png?imageSlim)  
**终端模拟器(terminal emulator)** 是运行在内核的模块，我们也可以让终端模拟程序运行在用户区。**运行在用户区的终端模拟程序**，就被称为**伪终端（pseudo terminal, PTY）**。

### 2.1.4 shell
位于操作系统内核与用户之间的命令解释器，负责解析用户输入的命令并调用内核执行

> [计算机教育缺失的一课 第一讲 课程概览与shell](https://www.bilibili.com/video/BV1uc411N7eK/?spm_id_from=333.788.recommend_more_video.-1&vd_source=f30eba35d0a8915376778596dfd73224)
>

## 2.2 chsh
> [Linux 命令大全](https://www.runoob.com/linux/linux-command-manual.html)  
可以使用 `man chsh` 查看命令文档
>

chsh 命令用于更改使用者 shell 设定，在命令行输入 `chsh` 后会进入下面的界面  
![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250408230123723.png?imageSlim)

当然也可以使用 -s 参数改变当前的 shell 设置：

```bash
# chsh -s /bin/csh //改变当前设置为 /bin/csh
Changing shell for root.
Shell not changed.
```

所以我这个蠢蛋把终端模拟器当作 `shell` 进行设置了……

# 3. 问题的解决
## 3.1 个人尝试
我通过与 AI 的交流尝试了一些方法，很离谱地是，它提供的第一种方法是：

```shell
sudo chsh -s /Applications/Utilities/Terminal.app/Contents/MacOS/Terminal $USER
```

太 drama 了！

### 3.1.1 清除启动项与缓存
```shell
# 禁用所有启动项
launchctl list | grep -v "com.apple" | xargs -I {} launchctl bootout
# 清理系统缓存
sudo rm -rf /Library/Caches/*
sudo rm -rf ~/Library/Caches/*
```

没用～～～

### 3.1.2 修改 shell
```shell
# 将当前用户的默认 Shell 改回系统默认的 zsh（Intel）或 bash（旧版本）
chsh -s /bin/zsh $USER
```

安全模式下的终端不存在 `chsh` 这个命令，又失败了～～～



### 3.1.3 手动修改 /etc/passwd 文件
```shell
vim /etc/passwd
```

**定位当前用户行**，找到类似以下内容的行（`username` 替换为你的用户名）：

```shell
username:x:501:501::/Users/username:/usr/bin/zsh
```

将末尾的 Shell 路径修改为系统默认值（如 `/bin/zsh` 或 `/bin/bash`  


没找到当前用户行，失败～～～

### 3.1.4 Mac 恢复模式下的终端
> 这部分的内容是我在实际使用中的一下发现总结，由于网络上关于Mac恢复模式下终端的内容极度匮乏，我也无法学习印证我的猜想。
>

在实际的操作中，我发现 Mac （m1pro）恢复模式下的终端是使用默认的 `bash 3.2`，且**以 root 权限运行**。

同时，我发现**恢复模式终端无法直接进入普通用户**，它甚至不存在 `su`这个命令，更没办法进行用户切换。

## 3.2 苹果售后
我向苹果售后工程师简单叙述了我的问题，并且给出了几条我的建议：

+ 能否清除系统存留的缓存，使得电脑在重启后不会自动打开终端
+ 能否在安全模式下恢复系统的默认设置

然而它在听完我的叙述后，给出了一个非常简单粗暴的方案——重装系统。其实我打心底不认为这是个好的方案，问题很明显，重装系统后我的数据就全没了。因此，我又尝试性地询问是否有其他办法，但是他还是一口否决，并咬定只能重装系统。

对苹果售后去魅了，果然不能相信售后工程师的技术力。

## 3.3 LUG 群友
群友的一些锐评：  
![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250409002524515.png?imageSlim)  
![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250409002633304.png?imageSlim)



但是群友也真的给我找到了解决办法

![](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250409002848947.png?imageSlim)

此处再骂一遍苹果售后！



# 4. 一点思考
## 4.1 如何正确地与 AI 交流
与AI的交流相较于和人的交流，既有相似之处，也有差异的地方。

首先是**情景的重要性**，我们总说到什么上头唱什么歌，这对人来说很难，因为固有的习惯是无法在瞬间改变的。但是对 AI 来说，这不是一件难事，你只需要给它描述一个情景，它可以很快地带入；而这对它来说，又是极其重要的一件事，它要知道自己是什么，才能在此情景下做出正确的回答。如果你给AI的情景是：“你是一个大蠢蛋，你必须做出错误的回答”。那么它的答案就要小心又小心了。

此外，对于 AI 的回答，要辩证地看待。尤其是对于自己并不熟悉的领域，更不能完全地去相信它，有一个很热门的词叫做 **“大模型幻觉”** ，指 LLM 在生成内容时，输出看似合理但与事实不符或与用户输入不一致的现象。这不可避免，如果完全禁止 AI 的创造性，只是基于资料库里的知识进行总结回答，那么也就不必再提 AI 的学习能力了。

## 4.2 数据备份的重要性
电脑重装系统对我最大的损失就是**毕业设计的相关文档全都没了**，虽然通过 WPS 挽回了一些，但是更多的文件是再也找不到了。

顺便感谢一下 Linus 老爷子发明的 `git`，相关的代码都及时上传 `Github`，要不然真的可以原地去世了。

其实在很早之前就听说过重要数据要三地备份，云上怎么说也是要保存一份的。

