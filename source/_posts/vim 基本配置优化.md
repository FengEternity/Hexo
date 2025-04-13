---
title: vim 基本配置优化
date: 2025/4/11
tags:
  - Vim
  - 配置优化
  - 插件安装
categories:
  - 技术学习
cover: https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/VIM-Editor.jpg.webp?imageSlim
author: Forsertee
type: tech
description: 本文介绍了作者的Vim配置，包括启动语法高亮、显示当前指令和模式等，旨在提高C语言程序设计的效率和可读性。同时，文章还介绍了如何安装插件管理器、配置NERDTree和Tagbar插件，以增强Vim的文件浏览和代码结构查看功能。
---
> 注：由于开始使用 [lazyvim](https://lazyvim-github-io.vercel.app/zh-Hans/), 后续将不会继续优化该文章配置

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250411150400029.png?imageSlim)

该文章为个人的 vim 配置，持续优化中。

# 基本配置

```shell
syntax on           " 启动语法高亮

set showcmd         " 命令模式下，在底部显示，当前键入的指令。
set showmode        " 在底部显示，当前处于命令模式还是插入模式。

" set mouse=a         " 启动鼠标支持，启用后会导致剪切板不正常
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

# 插件

## 安装
首先要安装一个插件管理器

```shell
# Linux/macOS
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

# Windows（PowerShell）
iwr -useb https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim | Out-File "$HOME/.vim/autoload/plug.vim" -Encoding utf8
```

在安装成功后，对 .vimrc 进行配置

```shell
call plug#begin('~/.vim/plugged')  " 插件目录
Plug 'preservim/nerdtree'         " 文件树插件
Plug 'tpope/vim-fugitive'         " Git 集成
Plug 'morhetz/gruvbox'            " 主题
call plug#end()
```

然后在 vim 中执行

```
:PlugInstall
```

执行完上面的命令，安装成功提示如下图：
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250411001248289.png?imageSlim)


## NERDTree
NERDTree 是一个在 Vim 中显示文件系统目录结构的插件，以树形结构展示文件系统目录，支持文件浏览、打开、创建、删除等操作。

相关配置项：

```shell
" 基础设置
let g:nerdtree_winpos = 'left'    " 侧边栏位置（left/right）
let g:nerdtree_width = 30         " 侧边栏宽度
let g:nerdtree_hide_cursor = 1    " 隐藏光标时自动关闭
let g:nerdtree_show_line_numbers = 1  " 显示行号

" 快捷键绑定
nnoremap <leader>n :NERDTreeToggle<CR>  " 默认 <leader> 是 \
nnoremap <leader>f :NERDTreeFind<CR>    " 定位当前文件在树中的位置

" 自动打开（可选）
autocmd VimEnter * NERDTree       " 启动 Vim 时自动打开
autocmd BufEnter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif  " 最后一个窗口关闭时退出
```

## Tagbar
Tagbar则是一个显示当前文件内部结构（如类、函数、变量等）的插件，帮助用户快速定位代码中的各个部分，类似于大纲视图。

安装Tagbar 之前，需提前安装 `ctags`（推荐 Exuberant Ctags）

相关配置：
```shell
" 基础设置
let g:tagbar_width = 30           " 侧边栏宽度
let g:tagbar_autoclose = 1        " 离开文件时自动关闭
let g:tagbar_foldlevel = 0        " 默认展开所有折叠
let g:tagbar_sort = 0             " 按代码出现顺序排序

" 快捷键绑定
nnoremap <leader>t :TagbarToggle<CR>

" 自动检测文件类型
autocmd BufReadPost *.cpp,*.c,*.h,*.py call tagbar#autoopen()

" 支持自定义语言（以 Markdown 为例）
let g:tagbar_type_markdown = {
    \ 'ctagstype': 'markdown',
    \ 'kinds': ['h:headings'],
    \ 'sort': 0,
\ }
```

安装完成后效果如下：

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250411000155491.png?imageSlim)
