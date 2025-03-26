---
# 基本信息
title: 在 Linux 中将 VSCode 添加到应用启动器，并使用 `code` 命令启动
date: 2024/12/19
tags:
  - arch
  - linux
categories: 
  - linux

# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/41370f2e263ceb323994939fe9f9ae4e.jpg
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/41370f2e263ceb323994939fe9f9ae4e.jpg
poster:  # 海报（可选，全图封面卡片）
  headline:  在 Linux 中将 VSCode 添加到应用启动器，并使用 `code` 命令启动
---



只是以 VSCode 作为示例，自己手动解压的应用都可以通过这个方法完成标题操作。

先贴一个系统概述吧，真的很喜欢我的配置：

![image-20241219195052198](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/undefinedimage-20241219195052198.png)

# 1. 解压文件

```bash
tar -xzf <file_name> -C /opt
```

上述命令作用为解压文件到 `/opt`目录中，Linux操作系统中，`/opt` 是常用的安装附加软件包的标准目录，用于存放第三方或自定义的软件，而不是系统默认的软件。对我而言，其实就是方便管理，比如……卸载的时候直接`cd`进去，然后`sudo rm -rf *`。

# 2. 创建桌面图标文件

```bash
vim ~/.local/share/applications/vscode.desktop
```

创建桌面图标文件后，需要在其中写入以下内容：

```bash
[Desktop Entry]
# 应用程序的名称
Name=Visual Studio Code

# 简短描述应用程序的功能
Comment=Code Editing. Redefined.

# 启动应用程序的命令
# /usr/bin/code 是 Visual Studio Code 的可执行文件
# --unity-launch 参数用于在 Unity 桌面环境下启动
# %F 是占位符，表示传递给应用程序的文件路径
Exec=/usr/bin/code --unity-launch %F

# 应用程序的图标路径
Icon=/opt/VSCode/resources/app/resources/linux/code.png

# 定义条目的类型，这里是应用程序
Type=Application

# 启动时显示通知，表示应用程序正在启动
StartupNotify=true

# 应用程序所属的类别，这有助于系统将应用程序分类到不同的组
Categories=Utility;TextEditor;Development;IDE;

# 应用程序支持的 MIME 类型，这里指定了纯文本文件
MimeType=text/plain;

# 定义一个额外的动作：创建一个新空窗口
Actions=new-empty-window;

# 该动作的详细定义
[Desktop Action new-empty-window]
# 动作的名称，显示在菜单中
Name=New Empty Window

# 执行该动作时启动一个新的空窗口
Exec=/usr/bin/code --new-window %F

# 该动作的图标路径
Icon=/opt/VSCode/resources/app/resources/linux/code.png
```

> 友情提醒，vim 中按`i`进入编辑模式，按`exc`后输入`:wq`写入保存并退出。

# 3. 创建符号链接

为了能够在终端使用 `code` 命令，需要创建一个符号链接。执行下面的命令：

```bash
sudo ln -s /opt/VSCode/bin/code /usr/bin/code
```



# 4. 更新桌面数据库

创建完桌面图标文件后，更新桌面数据库，以确保系统能识别到新的快捷方式。执行以下命令：

```bash
sudo update-desktop-database ~/.local/share/applications
```



成功添加！

![image-20241219203951487](https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/undefinedimage-20241219203951487.png)
