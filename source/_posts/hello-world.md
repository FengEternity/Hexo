---
# 基本信息
title: Blog 更新日志暨Hello World
date: 2024/05/07
tags: [Blog]
categories: [博客优化]
description: 作者使用Hexo和Stellar主题搭建个人博客，通过GitHub和Vercel实现无服务器部署。文章记录了从2024年5月7日部署到2025年4月22日Bing收录的关键更新和优化，包括图床、友链、评论插件等，并列出待完善和已完成的任务。
# 封面
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/hello.png 
banner: 
poster: # 海报（可选，全图封面卡片）
  headline: Blog 更新日志暨Hello World # 必选
  caption: 用于记录此博客的更新日志；同时，程序员不可越少的一集：问候世界 # 可选
  color: # 可选
# 插件
sticky: tagcloud # 数字越大越靠前
mermaid:
katex: true
mathjax: 
# 可选
author: Montee
references:
comments: # 设置 false 禁止评论
indexing: # 设置 false 避免被搜索
breadcrumb: # 设置 false 隐藏面包屑导航
leftbar: 
rightbar:
h1: # 设置为 '' 隐藏标题
type: story # tech/story
---
{% quot 1. 起航 %}

偶然之下看到 [cayzlh](https://www.cayzlh.com) 的博客，非常简洁，脑子一热决定跟个风，经过一个晚上的折腾，终于成功部署。

1. 本站由 [Monty Lee](https://www.montylee.cn) 基于 [Hexo](https://hexo.io/zh-cn/) 框架下的 [Stellar](https://github.com/xaoxuu/hexo-theme-stellar/tree/1.28.1) 主题创建
2. 使用 [GitHub](https://github.com) 托管代码，[Vercel](https://vercel.com) 实现无服务器部署

{% quot 2. 更新时间线 %}

{% timeline %}
<!-- node 2025 年 4 月 22 日 -->
* Bing收录，并提交站点地图

<!-- node 2025 年 4 月 21 日 -->
添加首页，实现开屏动画
![Uploading file...r6d2h]()


<!-- node 2025 年 4 月 13 日 -->
加入[开往](https://www.travellings.cn)，一个让“友链”活跃起来的开源项目。

<!-- node 2025 年 4 月 11 日 -->
开始做一些自定义的美化：
* [侧边栏时间轴样式优化](https://www.montylee.cn/2025/04/11/Hexo-stellar%E4%B8%BB%E9%A2%98%E4%BE%A7%E8%BE%B9%E6%A0%8F%E6%97%B6%E9%97%B4%E8%BD%B4%E6%A0%B7%E5%BC%8F%E4%BC%98%E5%8C%96/)
* [文章更新的热力图设计实现](https://www.montylee.cn/2025/04/12/Hexo-stellar%E5%8D%9A%E5%AE%A2%E7%83%AD%E5%8A%9B%E5%9B%BE%E8%AE%BE%E8%AE%A1%E4%B8%8E%E5%AE%9E%E7%8E%B0/)


<!-- node 2025 年 4 月 9 日 -->
* 谷歌收录，并提交站点地图
* 实现RSS订阅

<!-- node 2024 年 6 月 7 日 -->
评论功能设置成功

<!-- node 2024 年 5 月 8 日 -->
完成图床、静态友链的配置

<!-- node 2024 年 5 月 7 日 -->
部署成功啦！
{% image https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/hello.png width:300px %}

{% endtimeline %}


{% quot 3. 待完善 %}

- [ ] 参考这个博客做一些美化：https://innei.in/
	- [ ] 开屏动画的设置，可以结合我的 Github 首页修改


{% quot 4. 已完成 %}


- [x] ~~**图床**~~
    - [x] ~~暂时使用 [imgtp](https://imgtp.com) 这个在线的免费图床~~
    - [x] ~~不过觉得安全性不高，后续考虑使用 GitHub 作为图床，本地使用 PigGo 上传，jsDelivr 实现 CDN 加速，参加 [如何使用jsDelivr+Github 实现免费CDN加速?](https://zhuanlan.zhihu.com/p/346643522)~~
    - [x] ~~实现使用腾讯云 COS+PicGo 实现图床（新买了一个存储桶后，发现去年买的还没过期，伤心了）~~
    - [x] PicGo 图床插件设置

- [x] **友链和关于页面**
  - [x] ~~尝试动态友链失败，最终还是选择了静态的友链~~
  
- [x] 评论插件配置
  - [x] 使用 [giscus](https://giscus.app/zh-CN) 作为评论系统
  
- [x] 文章页面发布和更新时间有问题

  {% image https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/image-20240508230949859.png  %}

  发现是写文章时填写时间有误，只能写年/月/日

- [x] **footer 部分的倒计时功能**

  - [x] ~~初步实现功能~~

  - [x] 美化，参见 [cayzlh](https://www.cayzlh.com)  

- [x] **右侧栏公告及索引**

  {% image https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/undefinedrightsides.png width:200px padding:16px bg:white %}

- [x] **RSS 订阅**
- [x] 博客文章密码验证阅读
- [x] [小组件配置](https://xaoxuu.com/wiki/stellar/widgets/)

---
{% quot 引用 %}
  - [如何使用jsDelivr+Github 实现免费CDN加速?](https://zhuanlan.zhihu.com/p/346643522)
  - [如何利用 Github 搭建自己的免费图床？](https://zhuanlan.zhihu.com/p/353775844)
  - [Stellar - 每个人的独立博客](https://xaoxuu.com/wiki/stellar/#start)
  - ...

---