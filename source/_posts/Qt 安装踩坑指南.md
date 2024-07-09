---
# 基本信息
title: Qt 安装踩坑指南
date: 2024/07/09
tags: [cpp, QT]
categories: [cpp, QT]
description: Qt 安装踩坑指南
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/006BFMdqly1gfcskjuy1ij31kw13gjz0.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/006BFMdqly1gfcskjuy1ij31kw13gjz0.jpg
poster:  # 海报（可选，全图封面卡片）
  topic: # 可选
  headline:  Qt 安装踩坑指南 # 必选
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

1. 无法从网络位置安装，请将安装程序复制到本地驱动器

![image-20240709145847463](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709145847463.png)

* 问题分析：虚拟机的问题，默认把文件下载在Mac的文件目录下
* 解决方法：将安装包复制到虚拟机中的文件夹下就可以了

2. 下载“http://download.qt.io/online/qtsdkrepository/all_os/android/qt6_680/qt6_680_x86/2024-06-10-0933_meta.7z”时出现网络错误：Error transferring http://download.qt.io/online/qtsdkrepository/all_os/android/qt6_680/qt6_680_x86/2024-06-10-0933_meta.7z - server replied: Bad Gateway。

![image-20240709150601759](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709150601759.png)

* 问题分析：网络问题

* 解决方法：[使用国内镜像](https://download.qt.io/online/qtsdkrepository/windows_x86/root/qt/Updates.xml.mirrorlist)

  * 遗憾的是，并没有解决，产生了新的问题，见下方

* 最终解决：

  ```bash
  ./qt-unified-windows-x64-online.exe --mirror https://download.qt.io/online/qtsdkrepository/windows_x86/root/qt/Updates.xml.mirrorlist
  ```

  

3. 无法连接服务器，请检查您的网络连接，然后重试

![image-20240709150819203](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240709150819203.png)

* 解决方法见2

