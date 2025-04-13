---
title: Hexo-stellar主题开发指南
date: 2025-04-13
tags:
  - Hexo
  - 主题开发
  - Stellar
categories:
  - 博客优化
description: Hexo-stellar是一个现代化、模块化、响应式的Hexo主题，支持多语言、搜索、评论等功能，可高度定制。主题目录结构清晰，核心配置文件包括基本信息、侧边栏、站点结构和功能配置。提供了多种页面模板和局部模板，使用Stylus编写样式，JavaScript文件组织合理。开发建议包括自定义开发、最佳实践和扩展功能，如插件开发和数据管理。调试与优化部分介绍了调试方法和性能优化策略。总结强调了遵循设计理念和保持代码整洁的重要性。
---
这篇文章是完全用 cursor 读取项目代码生成的，本意是为了帮助我后续开发时能够更快速地找到相关代码实现是在哪个位置，巧合之下想起来 cursor 可以自己设置相关的规则文档，具体可以看下面这篇文章

> [# 深入理解Cursor规则：提升AI编码助手的效率与精准度](https://cursordocs.com/cursor-prompts/understanding-cursor-rules-for-ai)

写了规则后，最明显的感受就是， cursor 不会乱写代码了……
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250413193750209.png?imageSlim)


## 1. 主题概述

Stellar 是一个现代化的 Hexo 主题，具有优雅的设计和丰富的功能。它采用模块化的设计理念，提供了灵活的配置选项和强大的扩展能力。主题的主要特点包括：

- 响应式设计：完美适配各种设备屏幕
- 多语言支持：内置中英文支持，可轻松扩展其他语言
- 丰富的功能：支持搜索、评论、文章分类等
- 高度可定制：通过配置文件轻松调整主题外观和功能
- 性能优化：采用现代化的前端技术，确保良好的加载速度

## 2. 目录结构

Stellar 主题的主要目录结构如下：

```
stellar/
├── _config.yml          # 主题配置文件，包含主题的所有配置项
├── layout/              # 布局文件目录
│   ├── _partial/       # 局部模板目录
│   │   ├── comments/   # 评论系统相关模板
│   │   ├── cover/      # 封面相关模板
│   │   ├── main/       # 主要内容区域模板
│   │   ├── scripts/    # 脚本加载相关模板
│   │   ├── sidebar/    # 侧边栏相关模板
│   │   ├── widgets/    # 小部件相关模板
│   │   ├── head.ejs    # 头部模板，包含 meta 标签等
│   │   ├── menubtn.ejs # 菜单按钮模板
│   │   └── scripts.ejs # 脚本加载模板
│   ├── _plugins/       # 插件模板目录
│   ├── *.ejs           # 页面模板文件
│   │   ├── layout.ejs  # 基础布局模板
│   │   ├── index.ejs   # 首页模板
│   │   ├── post.ejs    # 文章页面模板
│   │   ├── page.ejs    # 自定义页面模板
│   │   ├── archive.ejs # 归档页面模板
│   │   ├── categories.ejs # 分类页面模板
│   │   ├── tags.ejs    # 标签页面模板
│   │   ├── notebooks.ejs # 笔记本列表页模板
│   │   └── notes.ejs   # 笔记页面模板
├── source/             # 静态资源目录
│   ├── css/           # 样式文件目录
│   │   ├── _components/ # 组件样式
│   │   ├── _common/    # 通用样式
│   │   ├── _custom.styl # 自定义样式
│   │   ├── _defines/   # 变量定义
│   │   ├── _layout/    # 布局样式
│   │   ├── _plugins/   # 插件样式
│   │   └── main.styl   # 主样式文件
│   └── js/            # JavaScript 文件目录
│       ├── plugins/    # 插件脚本
│       ├── search/     # 搜索功能脚本
│       ├── services/   # 服务相关脚本
│       └── main.js     # 主脚本文件
├── languages/          # 多语言支持目录
├── _data/             # 数据文件目录
│   ├── icons.yml      # 图标配置
│   └── menu.yml       # 菜单配置
└── scripts/           # 主题脚本目录
```

## 3. 核心配置文件

`_config.yml` 是主题的核心配置文件，主要包含以下几个部分：

### 3.1 基本信息配置
```yaml
stellar:
  version: '1.29.1'
  homepage: 'https://xaoxuu.com/wiki/stellar/'
  repo: 'https://github.com/xaoxuu/hexo-theme-stellar'
  main_css: /css/main.css
  main_js: /js/main.js
```

这些配置项定义了主题的基本信息和资源路径。`version` 用于标识主题版本，`homepage` 和 `repo` 分别指向主题的文档和代码仓库。

### 3.2 侧边栏配置
侧边栏配置包括两个主要部分：

1. Logo 配置：
```yaml
logo:
  avatar: '[{config.avatar}](/about/)'
  title: '[{config.title}](/)'
  subtitle: '{config.subtitle}'
```
这里可以设置网站的头像、标题和副标题，支持 HTML 标签和链接。

2. 菜单栏配置：
```yaml
menubar:
  columns: 4
  items:
    - id: post
      theme: '#1BCDFC'
      icon: solar:documents-bold-duotone
      title: 博客
      url: /
```
可以配置菜单项的数量、图标、颜色和链接等。

### 3.3 站点结构配置
`site_tree` 定义了不同类型页面的布局结构，包括：

1. 列表类页面：
```yaml
home:
  leftbar: welcome, recent
  rightbar: 
index_blog:
  base_dir: blog
  menu_id: post
  leftbar: welcome, recent
  rightbar: 
```

2. 内容类页面：
```yaml
post:
  menu_id: post
  leftbar: related, recent
  rightbar: ghrepo, toc
wiki:
  menu_id: wiki
  leftbar: tree, related, recent
  rightbar: ghrepo, toc
```

3. 其他页面：
```yaml
error_page:
  menu_id: post
  '404': '/404.html'
  leftbar: recent, timeline
  rightbar: timeline
```

### 3.4 功能配置

#### 3.4.1 搜索功能
```yaml
search:
  service: local_search
  local_search:
    field: all
    path: /search.json
    content: true
```
支持本地搜索和 Algolia 搜索，可配置搜索范围和字段。

#### 3.4.2 评论系统
```yaml
comments:
  service: giscus
  giscus:
    src: https://giscus.app/client.js
    data-repo: xxx/xxx
    data-repo-id: xxx
```
支持多种评论服务，包括 Giscus、Utterances 等。

#### 3.4.3 文章配置
```yaml
article:
  type: tech
  indent: false
  auto_cover: false
  cover_ratio: 2.4
  auto_excerpt: 128
```
可配置文章类型、缩进、封面等属性。

## 4. 布局系统

### 4.1 页面模板
主题提供了多种页面模板，每种模板都有特定的用途：

1. `layout.ejs`: 基础布局模板，定义了页面的基本结构
2. `index.ejs`: 首页模板，展示博客文章列表
3. `post.ejs`: 文章页面模板，用于展示单篇文章
4. `page.ejs`: 自定义页面模板，用于创建特殊页面
5. `archive.ejs`: 归档页面模板，按时间展示文章
6. `categories.ejs`: 分类页面模板，按分类展示文章
7. `tags.ejs`: 标签页面模板，按标签展示文章

### 4.2 局部模板
`_partial/` 目录包含多个可重用的模板组件：

1. 头部组件：
   - `head.ejs`: 定义页面的 meta 标签和资源引用
   - `scripts.ejs`: 管理页面脚本的加载

2. 侧边栏组件：
   - `sidebar/index_leftbar.ejs`: 左侧边栏模板
   - `sidebar/index_rightbar.ejs`: 右侧边栏模板

3. 内容组件：
   - `main/article.ejs`: 文章内容模板
   - `main/footer.ejs`: 页脚模板

4. 功能组件：
   - `comments/*.ejs`: 评论系统相关模板
   - `widgets/*.ejs`: 各种小部件模板

## 5. 静态资源

### 5.1 样式文件
主题使用 Stylus 预处理器编写样式，主要文件包括：

1. 基础样式：
   - `main.styl`: 主样式文件，导入其他样式模块
   - `_custom.styl`: 自定义样式文件

2. 组件样式：
   - `_components/`: 各种UI组件的样式
   - 每个组件独立文件，便于维护

3. 通用样式：
   - `_common/`: 定义通用样式类
   - 包括颜色、间距等基础样式

4. 布局样式：
   - `_layout/`: 定义页面布局相关样式
   - 包括响应式布局规则

5. 插件样式：
   - `_plugins/`: 插件相关的样式定义
   - 保持插件的样式隔离

### 5.2 JavaScript 文件
主题的 JavaScript 文件组织如下：

1. 核心脚本：
   - `main.js`: 主脚本文件，初始化主题功能

2. 功能模块：
   - `plugins/`: 各种插件脚本
   - `search/`: 搜索功能相关脚本
   - `services/`: 服务相关脚本

## 6. 开发建议

### 6.1 自定义开发
进行自定义开发时，建议遵循以下步骤：

1. 修改主题配置：
   - 在 `_config.yml` 中调整主题设置
   - 使用主题提供的配置项进行定制

2. 自定义样式：
   - 在 `_custom.styl` 中添加自定义样式
   - 使用主题提供的变量和混合器
   - 遵循 BEM 命名规范

3. 添加功能：
   - 在 `source/js/` 中添加新脚本
   - 在 `layout/_partial/` 中添加新模板
   - 在 `_config.yml` 中添加配置项

4. 修改模板：
   - 根据需要调整 `layout/` 中的模板文件
   - 保持与主题设计风格一致

### 6.2 最佳实践
开发过程中应遵循以下最佳实践：

1. 保持目录结构清晰：
   - 遵循主题的目录组织方式
   - 合理组织自定义文件

2. 遵循命名规范：
   - 使用有意义的文件名
   - 保持命名风格一致

3. 使用模块化方式：
   - 将功能拆分为独立模块
   - 保持代码的可复用性

4. 注意多语言支持：
   - 使用主题提供的多语言机制
   - 保持翻译的完整性

5. 确保响应式设计：
   - 测试不同设备的显示效果
   - 优化移动端体验

## 7. 扩展功能

### 7.1 插件开发
开发自定义插件的步骤：

1. 创建插件模板：
   - 在 `_plugins/` 目录下创建模板文件
   - 定义插件的 HTML 结构

2. 配置插件：
   - 在 `_config.yml` 中添加插件配置
   - 设置插件的启用状态和参数

3. 实现功能：
   - 编写插件相关的 JavaScript 代码
   - 添加必要的样式定义

### 7.2 数据管理
`_data/` 目录用于管理主题数据：

1. 菜单配置：
   - 在 `menu.yml` 中定义菜单项
   - 设置菜单的显示顺序和属性

2. 图标配置：
   - 在 `icons.yml` 中定义图标
   - 支持多种图标格式和来源

3. 其他数据：
   - 可以添加其他 YAML 文件
   - 用于存储主题需要的静态数据

## 8. 调试与优化

### 8.1 调试方法
调试主题时可以使用以下方法：

1. 浏览器开发者工具：
   - 使用 Elements 面板检查 DOM 结构
   - 使用 Console 面板查看错误信息
   - 使用 Network 面板分析资源加载

2. 主题调试模式：
   - 启用主题的调试选项
   - 查看详细的日志输出

3. 代码检查：
   - 使用 ESLint 检查 JavaScript 代码
   - 使用 Stylelint 检查样式代码

### 8.2 性能优化
优化主题性能的方法：

1. 资源优化：
   - 压缩 CSS 和 JavaScript 文件
   - 优化图片资源
   - 使用 CDN 加速静态资源

2. 代码优化：
   - 减少不必要的 DOM 操作
   - 优化事件处理函数
   - 使用缓存机制

3. 加载优化：
   - 实现资源的延迟加载
   - 优化首屏加载速度
   - 使用预加载技术

## 9. 总结

Stellar 主题提供了完整的开发框架和丰富的功能支持。通过本文的指南，开发者可以更好地理解主题架构，进行自定义开发和功能扩展。建议在开发过程中遵循主题的设计理念，保持代码的整洁和可维护性。

## 10. 技术细节

### 10.1 布局系统详解

#### 10.1.1 基础布局结构
主题采用三栏式布局，具体结构如下：

1. 左侧栏：
   - 导航菜单
   - 功能区域
   - 可折叠设计

2. 中间栏：
   - 主要内容区域
   - 文章列表或内容
   - 响应式布局

3. 右侧栏：
   - 辅助信息
   - 功能组件
   - 可隐藏设计

#### 10.1.2 页面类型判断
主题通过以下代码判断页面类型：

```javascript
// 页面类型：索引页面还是内容页面
var page_type = 'index'
if (['post', 'page', 'wiki', null].includes(page.layout)) {
  if (!page.nav_tabs) {
    page_type = 'content'
  }
}
```

这段代码根据页面的 `layout` 属性和 `nav_tabs` 配置来确定页面类型，从而应用不同的样式和功能。

#### 10.1.3 文章类型判断
文章类型的判断逻辑如下：

```javascript
// 文章类型：技术类文章/文学类文章
var article_type = theme.article.type
if (page.type?.length > 0) {
  article_type = page.type
} else if (theme.topic.tree[page.topic]?.type != null) {
  article_type = theme.topic.tree[page.topic]?.type
}
```

主题支持多种文章类型，可以根据需要设置不同的样式和布局。

### 10.2 样式系统详解

#### 10.2.1 样式文件组织
主题的样式文件采用模块化组织方式：

1. 组件样式：
   - `_components/`: 包含各种UI组件的样式
   - 每个组件独立文件，便于维护

2. 通用样式：
   - `_common/`: 定义通用样式类
   - 包括颜色、间距等基础样式

3. 布局样式：
   - `_layout/`: 定义页面布局相关样式
   - 包括响应式布局规则

4. 插件样式：
   - `_plugins/`: 插件相关的样式定义
   - 保持插件的样式隔离

#### 10.2.2 响应式设计
主题使用媒体查询实现响应式布局：

```css
@media screen and (max-width: 768px) {
  .l_body {
    padding: 0;
  }
  .l_left {
    display: none;
  }
  .l_right {
    display: none;
  }
}
```

这些样式规则确保主题在不同设备上都能良好显示。

### 10.3 功能模块详解

#### 10.3.1 搜索功能
搜索功能的主要特点：

1. 搜索类型：
   - 本地搜索：基于 JSON 文件的搜索
   - Algolia 搜索：使用第三方搜索服务

2. 配置选项：
   - 搜索范围：可配置搜索文章、页面或全部
   - 搜索字段：可指定搜索标题、内容或标签
   - 搜索结果：支持高亮显示匹配内容

3. 使用示例：
```yaml
search:
  service: local_search
  local_search:
    field: all
    path: /search.json
    content: true
```

#### 10.3.2 评论系统
评论系统支持多种服务：

1. Giscus：
   - 基于 GitHub Discussions
   - 支持主题切换
   - 可配置映射方式

2. Utterances：
   - 基于 GitHub Issues
   - 轻量级实现
   - 无需数据库

3. 配置示例：
```yaml
comments:
  service: giscus
  giscus:
    src: https://giscus.app/client.js
    data-repo: xxx/xxx
    data-repo-id: xxx
```

#### 10.3.3 文章功能
文章功能包括：

1. 文章分类：
   - 支持多级分类
   - 可配置分类颜色
   - 自动生成分类页面

2. 文章标签：
   - 支持多个标签
   - 标签云展示
   - 标签页面生成

3. 文章置顶：
   - 支持置顶功能
   - 可设置置顶顺序
   - 在列表页优先显示

4. 文章封面：
   - 支持自定义封面
   - 自动生成封面
   - 封面比例可配置

### 10.4 开发技巧

#### 10.4.1 自定义样式
自定义样式的建议：

1. 使用 `_custom.styl`：
   - 在此文件中添加自定义样式
   - 避免直接修改主题文件

2. 使用主题变量：
   - 利用主题定义的变量
   - 保持样式的一致性

3. 遵循 BEM 规范：
   - 使用块、元素、修饰符的命名方式
   - 提高样式的可维护性

#### 10.4.2 添加新功能
添加新功能的步骤：

1. 规划功能：
   - 确定功能需求
   - 设计实现方案

2. 开发实现：
   - 创建必要的模板文件
   - 编写 JavaScript 代码
   - 添加样式定义

3. 配置集成：
   - 在配置文件中添加选项
   - 确保与其他功能兼容

## 11. 参考资料

1. [Hexo 官方文档](https://hexo.io/zh-cn/docs/)
   - 包含 Hexo 的详细使用说明
   - 提供主题开发指南
   - 介绍插件开发方法

2. [Stellar 主题文档](https://xaoxuu.com/wiki/stellar/)
   - 主题的官方文档
   - 配置说明和示例
   - 常见问题解答

3. [EJS 模板语法](https://ejs.co/)
   - 模板引擎的使用说明
   - 语法规则和示例
   - 高级特性介绍

4. [Stylus CSS 预处理器](https://stylus-lang.com/)
   - CSS 预处理器的使用
   - 语法特性和示例
   - 最佳实践指南