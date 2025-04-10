---
title: vim 基本配置优化
date: 2025/4/11
tags:
  - linux
  - vim
categories:
  - linux
cover: https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/VIM-Editor.jpg.webp?imageSlim
author: Forsertee
type: tech
description: "本文介绍了作者的Vim配置，包括启动语法高亮、显示当前指令和模式、设置编码为UTF-8、Tab和缩进宽度为4空格、自动转换Tab为空格、自动缩进、设置行宽为80字符、自动折行等，旨在提高C语言程序设计的效率和可读性。"
---

该文章为个人的 vim 配置，持续优化中。

# 基本配置

```shell
syntax on           " 启动语法高亮

set showcmd         " 命令模式下，在底部显示，当前键入的指令。
set showmode        " 在底部显示，当前处于命令模式还是插入模式。

set encoding=utf-8  " 使用 utf-8 编码

set tabstop=4       " Tab 宽度为 4 空格
set shiftwidth=4    " 自动缩进宽度为 4 空格
set expandtab       " Tab 转换为空格
set softtabstop=4   " 退格时删除 4 个空格
set autoindent      " 启用自动缩进

set textwidth=80    " 设置行宽，即一行显示多少个字符。
set wrap            " 自动折行，即太长的行分成几行显示。
```


![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250410225706043.png?imageSlim)
