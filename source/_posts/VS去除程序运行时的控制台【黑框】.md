---
# 基本信息
title: VS 去除程序运行时的控制台
date: 2024/05/29
tags: [cpp, 计算机, debug]
categories: [技术学习]
description: VS 去除程序运行时的控制台
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/006BFMdqly1gfcskjuy1ij31kw13gjz0.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/006BFMdqly1gfcskjuy1ij31kw13gjz0.jpg
poster:  # 海报（可选，全图封面卡片）
  headline:  VS 去除程序运行时的控制台 # 必选
  caption:  # 可选
  color:  # 可选
# 插件
sticky: # 数字越大越靠前
mermaid:
katex: true
mathjax: 
# 可选
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
# 问题

如图所示，在程序运行时，会出现控制台窗口，一开始以为是QT的问题，解决后觉得应该不是？

![IMG_5939](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/IMG_5939.JPG)

# 解决步骤

大体流程和前面几篇文章类似，在这里主要说一下我在实际操作过程中遇到的问题，

1. 右键：项目\属性\链接器\系统\子系统

   * **如果你的项目工程文件很多，需要先看一下运行时控制台窗口的进入地址（上图控制台窗口右上角），在解决方案资源管理器中找到对应的项目进行右击进入属性面板**

2. 子系统 选择 窗口（/SUBSYSTEM:WINDOWS）原来可能是 控制台（/SUBSYSTEM:CONSOLE）

   ![img](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/watermark%2Ctype_d3F5LXplbmhlaQ%2Cshadow_50%2Ctext_Q1NETiBA6Zu36Zi15aSq6Ziz%2Csize_20%2Ccolor_FFFFFF%2Ct_70%2Cg_se%2Cx_16.png) 



如果你需要在 GUI 应用程序中显示控制台窗口，可以在代码中显式创建控制台窗口。

```c++
#include <windows.h>

void createConsole() {
    AllocConsole();
    freopen("CONOUT$", "w", stdout);
    freopen("CONOUT$", "w", stderr);
    freopen("CONIN$", "r", stdin);
}

int main(int argc, char *argv[]) {
    QApplication a(argc, argv);

    createConsole();  // 创建控制台窗口

    MainWindow w;
    w.show();
    return a.exec();
}

```



# 学习文档

没想好起什么名字，实际上是我在解决这个问题时，查找阅读的相关文章。

> * [VS2010/VS2013/VS2015/vs2017隐藏控制台程序的黑框](https://blog.csdn.net/zy_505775013/article/details/107432177)
> * [去掉console黑窗口的方法（qt和vs）](https://www.cnblogs.com/yimaochun/archive/2011/07/29/2120653.html)
> * [【vs】如何去掉控制台](https://blog.csdn.net/sinat_29158831/article/details/123503032)