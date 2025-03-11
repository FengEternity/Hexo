---
title: Qt 模型-视图结构
date: 2025/03/09
tags:
  - cpp
categories: cpp
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20220530203948_dd1b1.gif
poster:
  headline: Qt 模型-视图结构
---
在 QtQuick 中，数据通过 model-view（模型-视图）分离。对于每个 view（视图），每个数据元素的可视化都分给一个代理（delegate）。QtQuick 附带了一组预定义的模型与视图。想要使用这个系统，必须理解这些类，并且知道如何创建合适的代理来获得正确的显示和交互。
在QML中，model（模型）与view（视图）都通过delegate（代理）连接起来。功能划分如下，model（模型）提供数据。对于每个数据项，可能有多个值。在上面的电话薄例子中，每个电话薄条目对应一个名字，一个图片和一个号码。显示在view（视图）中的每项数据,都是通过delegate（代理）来实现可视化。view（视图）的任务是排列这些delegate（代理），每个delegate（代理）将model item（模型项）的值显示给用户。

# 1. 基础模型
