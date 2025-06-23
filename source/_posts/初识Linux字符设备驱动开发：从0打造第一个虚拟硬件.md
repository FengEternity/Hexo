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

# 驱动初认识

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


# 字符设备驱动

上文中提到，驱动程序分为字符设备、块设备及网络设备三大类，其中字符设备驱动是最基础的一种，常见的键盘、鼠标、串口等设备都属于字符设备。

## 核心概念

字符设备的核心特征是以**字节流**形式进行数据传输，每个字节都是独立的。与块设备（如硬盘）相比，字符设备没有固定大小的数据块结构。想象一下水流（字符设备）与冰块（块设备）的区别——水流可以任意分割，而冰块有固定形态。

## 开发流程

理解了字符设备的特性后，来看如何实现一个完整的字符设备驱动。这个过程可分为四个关键步骤，完美对应Linux架构的驱动层：

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250624004706769.png?imageSlim)


### 定义设备操作集：建立驱动与VFS的契约

```C
#include <linux/fs.h>

static struct file_operations mydev_fops = {
    .owner = THIS_MODULE,       // 指向当前模块
    .open = mydev_open,         // 对应应用层open()
    .release = mydev_close,     // 对应应用层close()
    .read = mydev_read,         // 对应应用层read()
    .write = mydev_write,       // 对应应用层write()
    .unlocked_ioctl = mydev_ioctl // 自定义控制命令
};
```

这个结构体是设备驱动的核心接口，它定义了驱动如何响应应用程序的各种操作。在Linux系统中，​**虚拟文件系统(VFS)​**​ 作为一个抽象层存在，所有设备都被视为文件。当应用程序调用`open()`、`read()`、`write()`等标准文件操作时，VFS会将它们转发给对应设备的`file_operations`结构体中的函数。

**关键点解释：​**​
- ​ `.owner`：必须设置为`THIS_MODULE`，这确保了当设备被打开时，驱动模块不会被意外卸载
- ​`.open`和`.release`：分别在设备被打开和关闭时调用，用于初始化和清理资源
- ​`.read`和`.write`：处理从设备读取数据或向设备写入数据的请求
- ​`.unlocked_ioctl`​：用于实现设备特定的控制命令（如设置串口波特率）
- ​**最小实现要求**​：设备必须至少实现`.open`和`.release`方法

`file_operations`结构体就是驱动和VFS之间的**契约**，它告诉内核："我可以处理这些请求"。当用户调用`open("/dev/mydev")`时，VFS会查找该设备对应的`file_operations`结构体，然后调用其中的`.open`方法。

### 驱动初始化：在内核中建立立足点

```C
static int __init mydev_init(void)
{
    // 1. 分配设备号 - 设备的身份证
    if (alloc_chrdev_region(&dev_num, 0, 1, "mydev") < 0)
        return -EFAULT;
    
    // 2. 关联操作集与设备
    cdev_init(&my_cdev, &mydev_fops);
    
    // 3. 创建设备节点 - 在/dev目录下的门牌号
    my_class = class_create(THIS_MODULE, "mydev_class");
    device_create(my_class, NULL, dev_num, NULL, "mydev");
    
    // 4. 初始化核心数据结构
    buffer = kzalloc(BUF_SIZE, GFP_KERNEL); // 分配内核缓冲区
    sema_init(&sem, 1);                   // 初始化信号量
    
    printk(KERN_INFO "Device initialized\n");
}
```

`module_init()`函数定义了这个驱动加载时内核执行的初始化函数。设备初始化过程就像给新出生的设备办理"身份证"和"户口"：

1. ​`alloc_chrdev_region()`​ ：为设备申请设备号
    - 设备号包括主设备号和次设备号，是设备的唯一标识
    - 主设备号标识设备类型，次设备号区分同类型的不同设备
2. ​`cdev_init()`​：将之前定义的`file_operations`绑定到字符设备
    - 这就像告诉内核："这是我能处理的请求列表"
3. ​**创建用户空间接口**​：
    - `class_create()`：在`/sys/class`下创建设备类别
    - `device_create()`：在`/dev`目录下创建设备文件节点
    - 这一步完成后，用户空间就能通过`/dev/mydev`访问设备了
4. ​**初始化设备资源**​：
    - `kzalloc()`：在内核空间分配内存，用于设备的数据缓冲
    - `sema_init()`：初始化信号量，用于处理并发访问
    - 对于实际硬件设备，这里还可能需要初始化硬件、分配中断等

**关键细节**​：
- `__init`宏表示该函数仅在模块加载时使用，加载后内存可释放
- 每个步骤都要检查返回值，确保操作成功
- `printk()`是内核打印函数，替代用户空间的`printf()`

### 核心功能实现：字节流的艺术
```C
static ssize_t mydev_write(struct file *file, const char __user *buf,
                           size_t count, loff_t *pos)
{
    down(&sem);  // 获取信号量
    
    // 计算可用空间
    int free_space = CIRC_SPACE(write_pos, read_pos, BUF_SIZE);
    
    // 实际写入量
    int bytes_to_write = min(count, free_space);
    
    // 分段拷贝
    if (write_pos + bytes_to_write <= BUF_SIZE) {
        copy_from_user(buffer + write_pos, buf, bytes_to_write);
    } else {
        int first_chunk = BUF_SIZE - write_pos;
        copy_from_user(buffer + write_pos, buf, first_chunk);
        copy_from_user(buffer, buf + first_chunk, bytes_to_write - first_chunk);
    }
    
    // 更新写指针（环形回绕）
    write_pos = (write_pos + bytes_to_write) % BUF_SIZE;
    
    up(&sem);  // 释放信号量
    return bytes_to_write;
}
```

这个写函数实现了用户空间到内核空间的数据传输，包含了字符设备驱动的核心概念：

1. ​**并发控制**​：
    - `down(&sem)`获取信号量，确保同时只有一个进程访问设备
    - 避免多个进程同时修改设备状态造成数据错乱
    - `up(&sem)`在操作完成后释放信号量
2. ​**环形缓冲区管理**​：
    - `CIRC_SPACE`宏计算缓冲区剩余空间
    - 当写入位置超过缓冲区末尾时，数据自动回绕到开头
    - 环形缓冲区避免了频繁的内存分配，提高性能
3. ​**安全数据传输**​：
    - `copy_from_user()`安全地从用户空间拷贝数据到内核空间
    - 使用`__user`标记用户空间指针，避免直接访问
    - 实际拷贝前要验证用户指针的有效性（`access_ok()`）
4. ​**流式处理**​：
    - 设备可能无法一次性接收所有数据，实际写入量可能小于请求量
    - 返回实际写入字节数给用户空间
    - 应用程序需要处理部分写入的情况

​**安全要点**​：
- 用户空间指针决不能直接访问，必须使用 **`copy_to/from_user()`**
- 内核空间的内存操作不能导致系统崩溃
- 所有返回给用户空间的数据都要经过有效性检查

### 资源清理：完美退场的艺术
```C
static void __exit mydev_exit(void)
{
    // 清理顺序与初始化严格相反
    device_destroy(my_class, dev_num);     // 销毁设备节点
    class_destroy(my_class);               // 删除设备类
    
    cdev_del(&my_cdev);                   // 移除字符设备
    unregister_chrdev_region(dev_num, 1); // 注销设备号
    
    kfree(buffer);                       // 释放缓冲区
    
    printk(KERN_INFO "Device unloaded\n");
}
```

设备卸载时的清理工作必须严谨仔细，遵循**FILO**​（先进后出）原则：

1. ​**销毁用户接口**​：
    - `device_destroy()`：删除`/dev`下的设备节点
    - `class_destroy()`：删除`/sys/class`中的设备类
2. ​**注销驱动核心**​：
    - `cdev_del()`：从内核字符设备表中移除设备
    - `unregister_chrdev_region()`：释放之前分配的设备号
3. ​**释放专用资源**​：
    - `kfree()`：释放驱动程序分配的内存资源
    - 对于真实设备，可能还需要关闭硬件电源、释放中断等

​**关键准则**​：

- 清理顺序必须与初始化顺序严格相反
- 每个`create/alloc`操作都必须有对应的`destroy/free`操作
- 即使驱动加载失败，也要清理所有已分配资源
- 不要假设资源状态，确保所有资源在释放前都存在

设备驱动的生命周期管理对系统稳定性至关重要。好的驱动在卸载后应该像从未存在过一样，不留下任何痕迹。

## 实战演示：虚拟串口设备

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250624004809512.png?imageSlim)


现在我们通过一个虚拟串口设备的实现，展示字符设备驱动的真实应用：
### 1. 定义虚拟寄存器
```C
#define VIRT_UART_BASE 0x3F8

// 串口寄存器布局
struct uart_regs {
    u32 data_reg;    // 数据寄存器
    u32 status_reg;  // 状态寄存器
};

static struct uart_regs *virt_regs;

// 状态寄存器位定义
#define TX_READY  (1 << 0)  // 发送就绪
#define RX_READY  (1 << 1)  // 接收就绪
```

这个结构模拟了真实UART芯片的寄存器。通过定义寄存器偏移和标志位，我们可以在没有真实硬件的情况下，模拟串口的基本行为。
### 2. 设备初始化增强
```C
static int __init virt_uart_init(void)
{
    // 分配寄存器空间
    virt_regs = ioremap_nocache(VIRT_UART_BASE, sizeof(struct uart_regs));
    
    // 初始化硬件状态
    virt_regs->status_reg = TX_READY | RX_READY;
    
    // 注册驱动...
}
```

`ioremap_nocache()`将物理地址映射到内核虚拟地址空间。即使这里使用虚拟硬件，这个过程也模拟了真实硬件驱动的工作方式：

- 设置初始状态寄存器值
- 创建发送和接收队列
- 初始化统计数据计数器

对于真实硬件，我们还需要：

- 探测物理地址和中断号
- 注册中断处理程序
- 复位设备并进行初始化
### 3. 写入函数（模拟真实串口行为）
```C
static ssize_t virt_uart_write(struct file *file, const char __user *buf,
                               size_t count, loff_t *pos)
{
    int sent = 0;
    
    while (sent < count) {
        // 等待发送就绪
        if (!(readl(&virt_regs->status_reg) & TX_READY)) {
            if (file->f_flags & O_NONBLOCK) 
                break;  // 非阻塞模式直接返回
            
            wait_event_interruptible(tx_queue, 
                (readl(&virt_regs->status_reg) & TX_READY));
        }
        
        // 发送单个字节
        char ch;
        copy_from_user(&ch, buf + sent, 1);
        writel(ch, &virt_regs->data_reg);
        sent++;
        
        // 模拟硬件延迟
        udelay(50);  // 每个字节发送延迟
    }
    
    return sent;
}
```

这个写函数模拟了真实串口设备的两个关键行为：

1. ​**硬件就绪等待**​：
    
    - 检查状态寄存器的发送就绪标志位(TX_READY)
    - 阻塞模式：使用`wait_event_interruptible()`等待条件满足
    - 非阻塞模式：当设备不可用时直接返回EAGAIN错误
2. ​**数据传输时序**​：
    
    - 每次只传输一个字节
    - `udelay()`模拟硬件传输时间
    - 真实设备通过设置波特率控制传输速度

​**核心要点**​：
- 模拟了真实硬件的工作方式
- 支持阻塞和非阻塞两种I/O模式
- 处理了硬件传输延迟的特性

### 4. 添加IOCTL控制接口
```C
long virt_uart_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
{
    switch (cmd) {
    case UART_SET_BAUD:  // 设置波特率
        virt_regs->baud = arg;
        break;
    case UART_GET_STATS: // 获取统计信息
        copy_to_user((void __user *)arg, &stats, sizeof(stats));
        break;
    default:
        return -ENOTTY;  // 不支持的命令
    }
    return 0;
}
```

`ioctl`是实现设备特殊控制命令的标准方法：

- `UART_SET_BAUD`：设置波特率参数
    - 验证波特率值是否在有效范围
    - 更新设备状态信息
- `UART_GET_STATS`：获取设备统计数据
    - 安全拷贝内核数据到用户空间
- 返回标准错误码处理各种边界情况

在实际应用中，IOCTL接口可以扩展更多功能，如：

- 设置奇偶校验等通信参数
- 查询设备状态
- 清空缓冲区
- 软件复位设备

通过这个虚拟串口设备的例子，我们完整展示了从基础概念到功能实现的字符设备驱动开发全流程。无论是虚拟设备还是真实硬件，核心的开发模式和思路是一致的。