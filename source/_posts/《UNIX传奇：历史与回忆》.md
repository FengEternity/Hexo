---
title: 《UNIX传奇：历史与回忆》
date: 2025-04-09
tags: [读书笔记, UNIX]
categories: 日常杂谈
description: 《UNIX传奇：历史与回忆》是一部讲述Unix操作系统历史和影响的书籍，作者以轻松幽默的笔触记录Unix的起源、发展及其重要性。书中不仅展现了Unix创造者的谦逊和对计算机领域的热爱，还揭示了"一切皆文件"的核心思想，即把硬件资源抽象成文件系统中的特殊文件，简化了对硬件的调用。这本书适合对计算机历史感兴趣的读者，无需专业技术背景即可欣赏Unix的思想和重要性。
cover: https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/v2-2429c2222d0680eadf76d9ee34adab7b_720w.jpg.png?imageSlim
katex: true
mathjax: true
author: Forsertee
type: tech
topic: read
---
> 自1969年在贝尔实验室的阁楼上诞生以来，Unix操作系统的发展远远超出其创造者们的想象。它带动了许多创新软件的开发，影响了无数程序员，改变了整个计算机技术的发展轨迹。本书不但书写Unix的历史，而且记录作者的回忆，一探Unix的起源，试图解释什么是Unix，Unix是如何产生的，以及Unix为何如此重要。除此之外，本书以轻松的口吻讲述了一群在贝尔实验室工作的发明天才的有趣往事，本书中每一个故事都是鲜为人知却又值得传播的宝贵资源。本书适合对计算机或相关历史感兴趣的人阅读。读者不需要有太多的专业技术背景，就可以欣赏Unix背后的思想，了解它的重要性。(引用自微信读书)

首先这不是一个 Unix 参考手册，也说不上是什么技术类的书籍，而仅仅是大佬以一种诙谐风趣的口吻在缓缓叙述 Unix 的诞生。

Unix 的伟大毋庸置疑，甚至不是我这一个计算机初学者可以评价的，通知这本书我也只能算是在 Unix 的门口浅浅徘徊了一阵，至于后面会不会深入的学习，还是一个未知数。

在阅读完整本书后，给我留下最深的是以下两点：
* 天才们的谦逊
* 热爱在计算机领域的重要性

而在技术方面，其实并没有什么非常显著的提升，如果非要说学到了什么，大概是：更加深刻地理解了一句话：**一切皆文件**


# 谦逊

> 我只浅尝过B语言。为了自娱，我写了一本教程，帮助别人学习。丹尼斯创造出C语言后，我没花多少工夫就把那本B语言教程修改成了C语言教程。事实证明，C语言教程很受欢迎

书中不止一次体现了作者的谦逊，不像许多人"学习式"的虚假谦逊，大佬的谦逊更像是一种自然而然的表达。过于谦逊，甚至让人产生出一种，"我上我也行"的错乱感，哈哈哈。

就像我引用的这一段，作者说自己知识浅过B语言，可是C语言的本身就是B语言演化，甚至在短暂的时间里被称为 new B *~~（牛逼）~~* 语言，如果C语言延续 new B 语言的名字，也不失为是中文程序员的一件趣事。
# 热爱

在中科创达面试的环节，面试官 *~~（应该是为未来的leader）~~* 强调了多次，"这个岗位（BSP驱动开发）大多数时候是很枯燥的，需要兴趣，没有兴趣是不行的"。我是认同这句话的，没有兴趣想要长久地做一件事人真的会疯掉。

而在阅读这本书时，对于兴趣我又有了不一样的认知。对这些计算机领域的天才来岁，用兴趣来形容已经不是一个合适的词语了，用热爱更为贴切，甚至用痴迷也不为过。

比如肯只用了一小时就在操作系统中添加了管道系统调用，甚至形容管道时"超级小菜"，因为 I/O 重定向的机制早已实现。这里固然体现了肯的天才，但是如果不是热爱，也很难在短时间内从萌生一个想法到执行，再到实现。

# 风趣

在上一篇文章中，我说过程序员在日积月累的编码生活中，会变得越来越理性，以至于丧失了感性的认知。可是在我读这本书时，在作者的只言片语中，不难领略到贝尔实验室各位巨星的风趣幽默。比如下面这一段对话：

> 罗布.派克曾经问肯，如果重写Unix，他会做哪些修改。他的答案是什么？​"我会在creat后头加上字母e。​"

# 一切皆文件

> Unix的另一创新是把磁盘、终端等外围设备都看作文件系统中的文件，磁盘是功能列表中提到的"可拆卸卷"​。访问设备的系统调用和访问文件的系统调用是一样的，所以同样的代码既可以操作文件也可以操作设备。当然实际上并没那么简单，因为真实的设备有奇怪的属性要处理，所以还有其他系统调用来处理这些特殊性，尤其是终端的特殊性。这部分系统并不漂亮。

Unix 中"一切皆文件"的思想是通过将外围设备都抽象成文件系统中的特殊文件，以此来实现对硬件资源的统一访问接口。通过这样的方式，大大简化了对于外围设备的调用，也规范了接口。例如：

- **打开设备**​：`int fd = open("/dev/tty", O_RDWR);` 与打开普通文件使用相同的 `open()` 系统调用。
- ​**读写数据**​：`read(fd, buffer, size)` 和 `write(fd, buffer, size)` 直接操作终端输入输出流。

这种设计使得程序无需区分设备类型，例如 `cat` 命令可以读取文件或键盘输入（`/dev/tty`），输出到文件或终端（`/dev/console`）。

当然，这一重要的思想肯定不是我三言两语就可以说明白的，上面的文字也仅仅是对这个思想有了浅薄的感知。不得不佩服天才们的脑子。







