---
title: Hexo-stellar博客热力图设计与实现
date: 2025-4-12
tags:
  - Hexo
  - JavaScript
  - ECharts
  - 热力图
  - 前端开发
categories:
  - Blog
description: 本文介绍了在Hexo博客中使用ECharts实现热力图的方法，包括容器初始化、数据处理、主题配置和ECharts配置。解决了主题切换适配、提示框样式重叠和响应式适配问题，并提供了性能、交互和样式优化建议，增强了博客的丰富性和个性化。
cover: https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250413140902265.png?imageSlim
---

## 前言

事情的起因看到了下面这位大佬的博客，觉的很好看，就想着在自己的归档页面也实现一个热力图的组件。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250412230613464.png?imageSlim)

在 GitHub 也找到了类似的开源项目——[hexo-graph](https://github.com/codepzj/hexo-graph)，效果如下图：
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250412230932965.png?imageSlim)

巧合的是，这位佬使用的主题还是和我一样的，但是我并没有在他的主题仓库里找到相关的代码……遂放弃，还是想着自己写一个。

## 技术栈

- ECharts：百度开源的数据可视化图表库
- JavaScript：实现热力图的核心逻辑
- CSS：样式调整和主题适配

## 实现思路

最终实现的效果如图
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250413140902265.png?imageSlim)


具体的实现代码可以参考仓库的提交源码：[feat: 添加热力图功能及相关样式](https://github.com/FengEternity/stellar/commit/2a478f22bdf7b93d5a0c2561a41c080ec0d17905)

- 在配置文件中添加ECharts和热力图服务的链接。 
- 在归档页面中集成热力图展示，显示文章发布情况。 
- 新增热力图生成器，提供API接口返回文章数据。 
- 添加热力图的样式，优化展示效果。

### 1. 容器初始化

首先，我们需要创建一个容器来承载热力图。通过 JavaScript 动态创建 DOM 元素，并设置基本样式：

```javascript
const chartDom = document.createElement('div');
chartDom.style.cssText = 'height:110px;margin:1rem 0;padding:0.5rem;';
el.appendChild(chartDom);

const myChart = echarts.init(chartDom);
```

### 2. 数据处理

热力图的数据来源是博客文章的发布日期。我们需要将文章数据转换为热力图所需的格式：

```javascript
const dataMap = new Map();

posts.forEach(function(post) {
  const date = new Date(post.date);
  const key = date.getFullYear() + '-' + 
            String(date.getMonth() + 1).padStart(2, '0') + '-' + 
            String(date.getDate()).padStart(2, '0');
            
  const value = dataMap.get(key);
  if (value == null) {
    dataMap.set(key, [{
      link: post.url,
      title: post.title
    }]);
  } else {
    value.push({
      link: post.url,
      title: post.title
    });
  }
});
```

### 3. 主题配置

为了适应博客的明暗主题，我们定义了两套颜色方案：

```javascript
const themes = {
  light: {
    backgroundColor: 'rgba(246, 248, 250, 0.95)',
    blockColor: '#f6f8fa',
    highlightColor: ['#f6f8fa', '#aff5b4', '#7ee787', '#4ac26b', '#2da44e'],
    textColor: style.getPropertyValue('--text-p2').trim() || '#999'
  },
  dark: {
    backgroundColor: 'rgba(22, 27, 34, 0.95)',
    blockColor: '#161b22',
    highlightColor: ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353'],
    textColor: style.getPropertyValue('--text-p2').trim() || '#666'
  }
};
```

### 4. ECharts 配置

热力图的核心配置包括：

```javascript
const option = {
  tooltip: {
    hideDelay: 1000,
    enterable: true,
    backgroundColor: currentTheme.backgroundColor,
    formatter: function (p) {
      // 自定义提示框内容
    }
  },
  calendar: {
    cellSize: [13, 13],
    range: [formatDate(startDate), formatDate(endDate)],
    itemStyle: {
      borderRadius: 2,
      shadowBlur: 2
    }
  },
  series: {
    type: 'heatmap',
    coordinateSystem: 'calendar',
    data: data
  }
};
```

## 开发过程中遇到的问题

### 1. 主题切换适配

**问题**：在切换博客主题时，热力图的颜色方案没有及时更新。

**解决方案**：使用 MutationObserver 监听主题变化，动态更新配置：

```javascript
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.attributeName === 'data-theme') {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const theme = isDark ? themes.dark : themes.light;
      
      // 更新配置
      option.tooltip.backgroundColor = theme.backgroundColor;
      option.visualMap.inRange.color = theme.highlightColor;
      // ... 其他配置更新
      
      myChart.setOption(option);
    }
  });
});
```

### 2. 提示框样式重叠

**问题**：热力图提示框与底部内容重叠，影响可读性。

**解决方案**：
1. 调整提示框背景色的透明度
2. 增加提示框的显示延迟
3. 优化提示框的内容布局

```javascript
tooltip: {
  hideDelay: 1000,
  backgroundColor: 'rgba(246, 248, 250, 0.95)', // 半透明背景
  padding: [10, 15],
  textStyle: {
    fontSize: 12
  }
}
```

### 3. 响应式适配

**问题**：在窗口大小变化时，热力图没有自适应调整。

**解决方案**：添加窗口resize事件监听：

```javascript
window.addEventListener('resize', () => myChart.resize());
```

## 参考资料

1. [ECharts 官方文档](https://echarts.apache.org/zh/index.html)
2. [GitHub Contributions 图表设计](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/managing-contribution-settings-on-your-profile/viewing-contributions-on-your-profile) 