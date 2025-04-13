---
menu_id: about
title: 关于
---
# 自我介绍
苏格拉底：我唯一知道的就是我一无所知

真正的智者在面对知识时，应该是保持敬畏于谨慎的，而不是浅尝辄止就好为人师。

# 开源项目
## IntelliSearch

> 项目链接：https://github.com/FengEternity/IntelliSearch

IntelliSearch 是一个基于AI大语言模型的对话式搜索引擎，旨在通过自然语言交互提升用户的信息检索体验。项目结合了大语言模型、搜索引擎和数据管理技术，开发了一个支持跨平台的智能搜索系统。通过创新的混合检索架构和检索增强生成（RAG）技术，IntelliSearch 能够提供更精准、更智能的搜索结果。

这个项目是我的本科毕业设计。其实写到现在，内心还是有很大的挫败感的，因为从 21 年上大学开始，就可是接触到 AI、图像处理、深度学习相关的知识，我也算得上是 LLM 的第一批用户。从最初的 ChatGPT，到国内百度的第一波跟风，再到 Kimi、智谱、Claude等等……LLM 真正进入非技术人员的普通大众视野中，应该是 DeepSeek 的爆火，当初使用它的时候，也不得不感慨，其推理链的惊艳。

本人并不是 LLM 的研究者，甚至没有什么的学习过相关的知识，只是通过一下技术博客与开源项目做一些自己武断的推论。

写这个项目的初衷是，在使用 ChatGPT 时，会发现它出现胡乱回答的现象，甚至也会顺着自己错误的理论不断推导，得到错上加错的结果。随着后来的学习，我知道这种现象叫做大模型幻觉，而想要解决这个问题，最为关键的一点就是从源头出发，减少错误输入​。去修改模型架构以及自己去训练模型这些方法是我无法实现的，所以我换了个思路。是否可以将传统的搜索引擎与 LLM 结合起来，来提高输入的质量呢？提高输入质量这个办法很快得到了印证，那就是 RAG 技术，相关的开源项目也很多，比如 RAGflow、Dify等。我的想法随之就转变为了将搜索引擎与 LLM 结合起来并实现一个本地的RAG数据库。

解释一下为什么在最初提到有着莫大的挫败感。实在是因为 LLM 发展的太快了，我的技术方法在开始做的时候虽说不上有多么独特，更谈不上先进。但也是中规中矩，并不落后。但是随着 MCP 技术的提出，它就变成一个笑话了。


![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250411235533355.png?imageSlim)

## autoDescription

> 项目链接：https://github.com/FengEternity/autoDescription

一个用于 Obsidian 的插件，可以使用 Kimi AI 自动为文章生成摘要、类别、标签等信息，并将其添加到文章的 Front Matter 中。

# 技术栈

* C/C++ | Python ……
* Linux | Cmake | LLM | Qt | 数据分析 | 图像处理 | 深度学习 | ……
* 多线程编程 | 网络编程 | ……


# 博客更新日志

{% timeline %}

<!-- node 2025 年 4 月 13 日 -->
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