---
title: 初识Linux字符设备驱动开发：从0打造第一个“虚拟硬件”
date: 2025/6/22
tags:
  - 操作系统
  - 驱动开发
categories:
  - 技术学习
author: Forsertee
type: tech
description:
---
![1726920221831_0.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/1726920221831_0.png?imageSlim)

在 Linux 系统中，设备驱动是连接硬件和软件的桥梁。上面这张图清晰的展示了Linux系统的分层架构：用户日常操作中直接面对的就是应用层和GNU C库。而这些应用与计算机硬件打交道的第一步就是跨过用户空间进入内核空间的最上层——系统调用层；

系统调用层（SCI）作为网关接收用户请求，交由虚拟文件系统（VFS）进行统一调度；VFS作为"万物皆文件"的核心抽象层，向下路由到字符设备、块设备及网络设备三大类驱动程序，最终通过Linux核心模块实现对底层硬件的操作控制，完整呈现了从应用层到物理硬件的垂直调用链路。​

举一个简单的例子：用户通过命令行终端发送“Hello World”到串口设备
1. **应用层**：`echo "Hello" > /dev/ttyS0` 命令调用Bash应用程序；Bash通过glibc库函数解析命令，调用`open()`和`write()`系统调用
2. **用户/内核边界**：系统调用接口（SCI）触发0x80中断，CPU从用户态切换到内核态
3. **VFS路由层**：VFS识别设备类型为字符设备，路由到字符设备驱动栈
	```C
	// 内核路径解析
	if (路径为"/dev/ttyS0")
	    return 字符设备操作集; // 指向串口驱动的file_operations
	```
4. **设备驱动层**：
	1. 串口驱动程序执行核心操作：
	```C
	static ssize_t serial_write(struct file *file, const char __user *buf) {
	    copy_from_user(kbuf, buf, len);  // 从用户空间拷贝数据
	    while (!(status_reg & TX_READY)); // 等待发送就绪
	    write_reg(TX_REG, *kbuf++);      // 写入串口数据寄存器
	}
	```
	2. 驱动直接操作硬件寄存器，控制物理设备
5. **硬件交互**：驱动程序通过CPU的IO端口指令：
	```C
	mov dx, 0x3F8   ; 串口COM1基址
	out dx, al       ; 将AL寄存器的字节发送到串口
	```
	电信号通过UART芯片转换为串行数据流，最终在物理串口线(TX引脚)上产生"Hello"的电压波形。
