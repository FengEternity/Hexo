---
title: Hexo-stellar主题侧边栏时间轴样式优化
date: 2025-04-11
tags:
  - Hexo
  - 主题开发
  - 样式优化
categories:
  - 博客优化
description: 本文介绍了Hexo Stellar主题侧边栏时间轴样式的优化过程，包括数据配置、模板优化和样式美化。通过调整HTML结构、添加CSS样式，实现了清晰视觉层次、精致细节处理、合理间距布局和优雅交互效果，提升了时间轴的美观度和用户体验。
---

## 前言

在原生的 Hexo  Stellar 主题中，侧边栏并不支持静态的时间轴数据，因此需要对其进行优化改进。

## 实现过程

### 1. 数据配置

首先在 `source/_data/widgets.yml` 中配置时间轴数据：

```yaml
timeline:
  layout: timeline
  title: 近期动态
  data:
    - date: 2025-04-11
      title: 重新学习 C 语言
      content: |
        重新开始学习 C 语言。与大一不同的是，在这次学习时，会学习更多的东西，如 vim、gdb...... 并且结合操作系统、计算机组成原理等相关知识去深入了解 C 语言究竟是怎么和顶层打交道的。

    - date: 2025-03-29
      title: 春招 Offer
      content: |
        拿到春招第一个offer，重新开始写博客了，删除了之前如同简历一样的自我介绍。

    # ... 更多数据项
```

### 2. 模板优化

修改 `themes/stellar/layout/_partial/widgets/timeline.ejs`，优化时间轴的 HTML 结构：

```ejs
<%
function formatDate(date) {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/\//g, '年').replace(/\//, '月') + '日';
}

function layoutDiv() {
  var el = '';
  if (!item.api && !item.data) {
    return el;
  }
  
  el += `<widget class="widget-wrapper${scrollreveal(' ')} timeline">`;
  if (item.title) {
    el += '<div class="widget-header dis-select">';
    el += '<span class="name">' + item.title + '</span>';
    el += '</div>';
  }
  el += '<div class="widget-body fs14">';
  
  // 静态数据模式
  if (item.data) {
    el += '<div class="tag-plugin timeline">';
    item.data.forEach((node, i) => {
      el += '<div class="timenode" index="' + i + '">';
      // 时间头部
      el += '<div class="header">';
      el += '<span>' + formatDate(node.date) + '</span>';
      el += '</div>';
      // 内容主体
      el += '<div class="body">';
      if (node.title) {
        el += '<div class="title">' + node.title + '</div>';
      }
      const content = node.content.split('\n').map(line => line.trim()).filter(line => line).join('\n');
      el += markdown(content);
      el += '</div>';
      el += '</div>';
    });
    el += '</div>';
  }
  
  el += '</div>';
  el += '</widget>';
  return el;
}
%>
```

#### 模板优化详解

##### 2.1 日期格式化函数

```javascript
function formatDate(date) {
  return new Date(date).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).replace(/\//g, '年').replace(/\//, '月') + '日';
}
```

这个函数的主要功能是：
- 接收一个日期参数
- 使用 `toLocaleString` 将日期格式化为中文格式
- 将格式化后的斜杠替换为"年"、"月"、"日"
- 最终输出类似 "2025年04月11日" 的格式

##### 2.2 主要布局函数

```javascript
function layoutDiv() {
  var el = '';
  if (!item.api && !item.data) {
    return el;
  }
  
  el += `<widget class="widget-wrapper${scrollreveal(' ')} timeline">`;
  if (item.title) {
    el += '<div class="widget-header dis-select">';
    el += '<span class="name">' + item.title + '</span>';
    el += '</div>';
  }
  el += '<div class="widget-body fs14">';
  
  // 静态数据模式
  if (item.data) {
    el += '<div class="tag-plugin timeline">';
    item.data.forEach((node, i) => {
      el += '<div class="timenode" index="' + i + '">';
      // 时间头部
      el += '<div class="header">';
      el += '<span>' + formatDate(node.date) + '</span>';
      el += '</div>';
      // 内容主体
      el += '<div class="body">';
      if (node.title) {
        el += '<div class="title">' + node.title + '</div>';
      }
      const content = node.content.split('\n').map(line => line.trim()).filter(line => line).join('\n');
      el += markdown(content);
      el += '</div>';
      el += '</div>';
    });
  }
  
  el += '</div>';
  el += '</widget>';
  return el;
}
```

代码实现了：
- 数据有效性检查
- 创建时间轴的基本容器结构
- 添加标题区域（如果存在标题）

##### 2.3 时间轴内容生成

```javascript
  el += '<div class="widget-body fs14">';
  if (item.data) {
    el += '<div class="tag-plugin timeline">';
    item.data.forEach((node, i) => {
      el += '<div class="timenode" index="' + i + '">';
      // 时间头部
      el += '<div class="header">';
      el += '<span>' + formatDate(node.date) + '</span>';
      el += '</div>';
      // 内容主体
      el += '<div class="body">';
      if (node.title) {
        el += '<div class="title">' + node.title + '</div>';
      }
      const content = node.content.split('\n')
        .map(line => line.trim())
        .filter(line => line)
        .join('\n');
      el += markdown(content);
      el += '</div>';
      el += '</div>';
    });
  }
```

主要功能是：
- 遍历每个时间节点数据
- 为每个节点创建时间头部，显示格式化后的日期
- 创建内容主体，包含标题和正文
- 对内容进行格式化处理，移除多余空行和空格
- 使用 markdown 函数处理内容的 Markdown 格式

### 3. 样式美化

此外，在支持静态时间轴后，发现存在以下问题：
1. 时间轴线与内容重叠
2. 节点样式过于简单
3. 缺乏交互效果
4. 内容布局不够紧凑

下面这个博客就是没有进行优化的，注意侧边栏的时间轴，界面主区域的时间轴不会出现样式问题：
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250412002611918.png?imageSlim)

具体的优化措施如下：创建或修改主题的样式文件，添加以下样式：

```stylus
// 时间轴容器
.widget-wrapper.timeline
  .tag-plugin.timeline
    position: relative
    padding-left: 24px
    
    // 主时间线
    &:before
      content: ''
      position: absolute
      left: 6px
      top: 0
      bottom: 0
      width: 2px
      background: #e5e6eb
      border-radius: 2px

    .timenode
      position: relative
      padding-bottom: 32px
      
      // 时间节点圆点
      .header
        position: relative
        margin-bottom: 12px
        
        &:before
          content: ''
          position: absolute
          left: -24px
          top: 50%
          transform: translateY(-50%)
          width: 12px
          height: 12px
          border-radius: 50%
          background: #fff
          border: 2px solid #e5e6eb
          z-index: 2
        
        span
          font-size: 14px
          color: #86909c
      
      // 内容区域
      .body
        background: #fff
        border-radius: 12px
        padding: 16px 20px
        margin: 0
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05)
        
        .title
          font-size: 16px
          font-weight: 600
          color: #1d2129
          margin-bottom: 8px
          line-height: 1.5
        
        p
          margin: 8px 0
          color: #4e5969
          font-size: 14px
          line-height: 1.8
          white-space: pre-wrap

      &:last-child
        padding-bottom: 0

      // 悬停效果
      &:hover
        .header:before
          background: #fff
          border-color: var(--theme-color)
```

## 优化效果

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250412002741247.png?imageSlim)

## 结语

通过以上优化，我们实现了一个结构清晰、功能完善的时间轴模板。这个模板不仅提供了良好的用户体验，也为后续的样式优化和功能扩展提供了坚实的基础。在实际应用中，我们可以根据具体需求，进一步调整和优化模板的结构和功能。

