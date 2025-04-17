---
title: hexo-auto-description：AI生成文章摘要
date: 2025/4/17
tags:
  - Hexo
  - Blog
  - AI
categories:
  - 项目开发
  - JavaScript
author: Forsertee
type: tech
description: hexo-auto-description是Hexo插件，自动生成博客摘要。它利用MoonShot AI API，提供配置选项和环境变量设置。技术实现包括Prompt设计、长度控制、请求控制和错误处理。插件代码支持并发处理和API状态验证。
---
# 引言

在使用 Hexo 写博客时，经常需要为文章添加摘要（description）。手动编写摘要不仅耗时，而且容易出现摘要与文章内容不够匹配的情况。为了解决这个问题，我开发了 `hexo-auto-description` 插件，利用 MoonShot AI 的能力，自动为文章生成高质量的摘要。

其实之前有写过一个 Obsidian 的插件：[Obsidian auto-description插件开发](https://www.montylee.cn/2025/03/27/Obsidian%20auto-description%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91/)，但是不知道为啥 Obsidian 加载我本地自己写的插件总是加载不出来，所以就换成写一个 Hexo 的插件。

# 功能特性

功能就很简单了，在文章生成时自动检测是否需要生成摘要信息，调用 Kimi 的 API，自动根据文章内容生成一个摘要。其他的一些特性可以从下面的配置选项中大概了解一下：

## 配置选项
在 Hexo 的 `_config.yml` 文件中添加以下配置：

```yaml
kimi_api_key: your_api_key_here  # MoonShot API 密钥
auto_description:
  # API 配置
  apiKey: ''                # API 密钥（优先级低于环境变量）
  # AI 模型配置
  model: 'moonshot-v1-8k'  # 使用的模型
  temperature: 0.7         # 生成温度，越低越保守
  max_tokens: 200          # 最大生成令牌数
  
  # 摘要配置
  maxLength: 100          # 最大长度限制（字数）
  minRatio: 0.1          # 最小摘要比例（相对原文）
  maxRatio: 0.3          # 最大摘要比例（相对原文）
  minLength: 20          # 最小摘要长度
  language: 'zh'         # 支持 'zh' 或 'en'
  
  # 更新策略
  updateWindow: 300000   # 更新时间窗口（5分钟，单位：毫秒）
  forceUpdate: false     # 是否强制更新所有文章
  
  # 错误处理
  maxRetries: 3         # 最大重试次数
  retryDelay: 1000      # 重试延迟（毫秒）
  
  # 并发处理
  concurrency: 3        # 并发处理数量
  
  # API 验证
  validateApi: true           # 是否启用 API 验证
  validateInterval: 3600000   # API 验证间隔（1小时）
```

## 环境变量
注意，除了在 `_config.yml` 中配置，也支持通过环境变量设置，并且我个人不推荐把密钥写在 Hexo 的配置文件中，而应该写进自己的环境变量：

```bash
# Linux/Mac
export KIMI_API_KEY=your_api_key_here

# Windows
set KIMI_API_KEY=your_api_key_here
```
## 命令行选项

```bash
hexo generate-descriptions [options]
```

支持的选项：
- `--force`: 强制更新所有文章
- `--concurrency`: 设置并发处理数量
- `--validate`: 仅验证 API 密钥
- `--show-key`: 显示当前使用的 API 密钥来源

# 技术实现

## Prompt 设计

插件的核心是使用 MoonShot AI 的 API 进行摘要生成。主要包含两个阶段：

```javascript
// 第一阶段：初始摘要生成
const firstPrompt = `你是一个专业的文章摘要生成器。请为以下文章生成摘要，要求：
  1. 字数在${minLength}-${maxLength}字之间
  2. 完整概括文章主要内容
  3. 突出文章的关键信息
  4. 保持逻辑连贯
  5. 语言简洁清晰`;

// 第二阶段：摘要优化
const secondPrompt = `你是一个专业的文章精简专家。请按照以下要求精简摘要：
  1. 输出长度控制在110字以内
  2. 保留核心信息和关键内容
  3. 删除不必要的修饰词
  4. 使用简练的表达
  5. 保持语言通顺自然`;
```
昨天还和 SAST 的群友在讨论 Agent、RAG、MCP 这些近期火热的相关技术。不过对于大多数 LLM 使用者，最最重要的还是设计出一个优秀的 Prompt。上面所说的两个阶段，第一阶段是根据文章内容生成摘要信息，但是虽然我限制了它的字数，可是 LLM 现在好像还不能调用工具计算生成文本的数量，所以我就加了一个二次摘要。

## 长度控制策略

LLM 不知道自己生成了多少文本这个问题着实是让我很头疼，最后我妥协了……首先是增加了容差机制，允许摘要的长度有一定的弹性空间（±10字），其次对于第二次优化后的摘要，不做检测，直接采用。

## 请求控制与错误处理

```shell
INFO  Start processing
[1/1] hexo-auto-description：AI生成文章摘要.md: 正在生成摘要...
遇到限流，等待4秒后重试...
遇到限流，等待8秒后重试...
遇到限流，等待16秒后重试...
```
如果频繁的对 API 接口进行访问，会触发服务器端的限流保护，拒绝访问，因此要添加请求控制和错误处理。下面详细的介绍一下这部分的实现：

### 1. 速率限制器（Rate Limiter）

```javascript
const rateLimiter = {
  lastRequestTime: 0,
  cooldownSeconds: 1,
  consecutiveErrors: 0,
  maxConsecutiveErrors: 3,
  
  async waitForCooldown() {
    const now = Date.now();
    const timeSinceLastRequest = (now - this.lastRequestTime) / 1000;
    const waitTime = this.cooldownSeconds * (1 + this.consecutiveErrors);
    
    if (timeSinceLastRequest < waitTime) {
      const actualWaitTime = (waitTime - timeSinceLastRequest) * 1000;
      console.log(`等待 ${actualWaitTime/1000} 秒后重试...`);
      await new Promise(resolve => setTimeout(resolve, actualWaitTime));
    }
    
    this.lastRequestTime = Date.now();
  }
}
```

速率限制器的主要功能：
1. **请求间隔控制**：基础冷却时间：1秒，根据连续错误次数动态增加等待时间
   - 计算公式：`waitTime = cooldownSeconds * (1 + consecutiveErrors)`
2. **错误计数**：记录连续错误次数，最大允许连续错误：3次，在成功后重置错误计数

### 2. 重试机制

```javascript
async function generateSummary(text, isRecursive = false, retryCount = 0) {
  try {
    // ... API 调用代码 ...
  } catch (error) {
    if (error.response?.status === 429) {
      const waitTime = Math.min(2000 * Math.pow(2, retryCount), 16000);
      console.log(`遇到限流，等待${waitTime/1000}秒后重试...`);
      await delay(waitTime);
      if (retryCount < 3) {
        return await generateSummary(text, isRecursive, retryCount + 1);
      }
    }
    throw error;
  }
}
```

重试策略：
1. **指数退避（Exponential Backoff）**
   - 基础等待时间：2000ms
   - 退避公式：`waitTime = 2000 * 2^retryCount`
   - 最大等待时间：16000ms（16秒）
   - 最大重试次数：3次

2. **错误类型处理**
   - 特别处理 429 状态码（请求过多）
   - 其他错误直接抛出

### 3. 二次摘要的延迟控制

```javascript
// 首次摘要到二次摘要的间隔
if (!isRecursive && summaryLength > (100 + TOLERANCE)) {
  console.log(`生成的摘要(${summaryLength}字)超出容差范围，等待3秒后进行精简...`);
  await delay(3000);
  return await generateSummary(summary, true);
}

// 二次摘要的重试间隔
if (isRecursive && summaryLength > (100 + TOLERANCE)) {
  if (retryCount < 2) {
    console.log(`精简后的摘要(${summaryLength}字)仍超出容差范围，等待2秒后重试第${retryCount + 1}次...`);
    await delay(2000);
    return await generateSummary(text, true, retryCount + 1);
  }
}
```

延迟控制策略：
1. **首次到二次摘要**：3秒固定延迟
2. **二次摘要重试**：2秒固定延迟
3. **最大重试次数**：2次

### 4. API 状态验证

```javascript
async function checkApiStatus(config) {
  if (!config.validateApi) {
    return true;
  }

  const now = Date.now();
  if (now - apiStatus.lastValidated < config.validateInterval && apiStatus.isValid) {
    return true;
  }

  try {
    await validateApiKey(config);
    return true;
  } catch (error) {
    console.error('API 验证失败:', error.message);
    return false;
  }
}
```

API 验证机制：
1. **验证间隔**
   - 默认间隔：1小时（3600000ms）
   - 可通过配置调整：`validateInterval`
   - 可禁用验证：`validateApi: false`

2. **验证状态缓存**
   ```javascript
   let apiStatus = {
     lastValidated: 0,
     isValid: false,
     error: null
   };
   ```

### 5. 并发控制

```javascript
async function processPostsConcurrently(posts, config) {
  const queue = [];
  for (const post of posts) {
    if (queue.length >= config.concurrency) {
      await Promise.race(queue);
    }
    
    const task = processSinglePost(post, config, progress)
      .then(() => {
        const index = queue.indexOf(task);
        if (index !== -1) {
          queue.splice(index, 1);
        }
      });
    
    queue.push(task);
  }
  
  await Promise.all(queue);
}
```

并发处理机制：
1. **队列控制**
   - 最大并发数：默认 3
   - 动态队列管理
   - 任务完成自动移出队列

2. **任务状态追踪**
   ```javascript
   const processedFiles = new Set();
   const processingFiles = new Set();
   ```
   - 防止重复处理
   - 跟踪处理状态
   - 生成完成后自动清理

# 完整代码

{% folding child:codeblock open:false  点击查看完整代码 %}

```javascript
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);
const stat = promisify(fs.stat);

// 在文件顶部声明 apiKey
const apiKey = process.env.KIMI_API_KEY || hexo.config.kimi_api_key;

// 默认配置
const DEFAULT_CONFIG = {
  // API 配置
  apiKey: '', // API 密钥，优先级低于环境变量
  // AI 模型配置
  model: 'moonshot-v1-8k',
  temperature: 0.7,
  max_tokens: 200,
  // 摘要配置
  maxLength: 100,      // 最大长度限制为100字
  minRatio: 0.1,      // 最小摘要比例（相对于原文）
  maxRatio: 0.3,      // 最大摘要比例（相对于原文）
  minLength: 20,      // 最小摘要长度
  language: 'zh',     // 支持 'zh' 或 'en'
  // 更新策略
  updateWindow: 5 * 60 * 1000, // 5分钟，单位：毫秒
  forceUpdate: false, // 是否强制更新所有文章
  // 错误处理
  maxRetries: 3,
  retryDelay: 1000, // 重试延迟，单位：毫秒
  // 并发处理
  concurrency: 3, // 并发处理数量
  // API 验证
  validateApi: true, // 是否启用 API 验证
  validateInterval: 3600000, // API 验证间隔，默认1小时
};

// API 状态缓存
let apiStatus = {
  lastValidated: 0,
  isValid: false,
  error: null
};

// 添加全局处理状态记录
const processedFiles = new Set();
const processingFiles = new Set();

// 获取 API 密钥
function getApiKey(config) {
  // 优先使用环境变量
  if (process.env.KIMI_API_KEY) {
    return process.env.KIMI_API_KEY;
  }
  // 其次使用配置文件中的密钥
  if (config.apiKey) {
    return config.apiKey;
  }
  return null;
}

// 验证 API 密钥
async function validateApiKey(config) {
  try {
    const apiKey = getApiKey(config);
    
    // 检查 API 密钥是否存在
    if (!apiKey) {
      throw new Error('未设置 API 密钥，请在环境变量 KIMI_API_KEY 或配置文件中设置');
    }

    // 检查 API 密钥格式
    // if (!/^[a-zA-Z0-9]{32,}$/.test(apiKey)) {
    //   throw new Error('API 密钥格式不正确');
    // }

    // 测试 API 调用
    const response = await axios.post('https://api.moonshot.cn/v1/chat/completions', {
      model: config.model,
      messages: [
        {
          role: "user",
          content: "test"
        }
      ],
      max_tokens: 5
    }, {
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      timeout: 5000 // 5秒超时
    });

    // 检查响应状态
    if (response.status !== 200) {
      throw new Error(`API 返回错误状态码: ${response.status}`);
    }

    // 更新 API 状态
    apiStatus = {
      lastValidated: Date.now(),
      isValid: true,
      error: null
    };

    return true;
  } catch (error) {
    // 更新 API 状态
    apiStatus = {
      lastValidated: Date.now(),
      isValid: false,
      error: error.message
    };

    throw error;
  }
}

// 检查 API 状态
async function checkApiStatus(config) {
  // 如果禁用了验证，直接返回 true
  if (!config.validateApi) {
    return true;
  }

  // 检查是否需要重新验证
  const now = Date.now();
  if (now - apiStatus.lastValidated < config.validateInterval && apiStatus.isValid) {
    return true;
  }

  try {
    await validateApiKey(config);
    return true;
  } catch (error) {
    console.error('API 验证失败:', error.message);
    return false;
  }
}

// 获取配置
function getConfig(hexo) {
  return Object.assign({}, DEFAULT_CONFIG, hexo.config.auto_description);
}

// 计算合适的摘要长度
function calculateSummaryLength(contentLength, config) {
  // 根据原文长度计算初始摘要长度
  let minLength = Math.max(config.minLength, Math.floor(contentLength * config.minRatio));
  let maxLength = Math.floor(contentLength * config.maxRatio);
  
  // 限制最大长度为100字
  if (maxLength > 100) {
    maxLength = 100;
    minLength = Math.min(minLength, 90); // 确保最小长度不会超过最大长度
  }
  
  // 确保最大长度至少比最小长度大10个字
  maxLength = Math.max(maxLength, minLength + 10);
  
  // 再次确保不超过100字的限制
  maxLength = Math.min(maxLength, 100);
  
  // console.log(`原文长度：${contentLength}字，调整后的目标摘要长度：${minLength}-${maxLength}字`);
  
  return {
    minLength,
    maxLength
  };
}

// 修改生成摘要的函数
async function generateDescription(content, config) {
  const apiValid = await checkApiStatus(config);
  if (!apiValid) {
    throw new Error('API 验证失败，无法生成摘要');
  }

  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  
  // 添加容差范围配置
  const TOLERANCE = 10; // 允许超出10个字符的容差
  
  // 添加速率限制器
  const rateLimiter = {
    lastRequestTime: 0,
    cooldownSeconds: 1,
    consecutiveErrors: 0,
    maxConsecutiveErrors: 3,
    
    async waitForCooldown() {
      const now = Date.now();
      const timeSinceLastRequest = (now - this.lastRequestTime) / 1000;
      
      // 根据连续错误次数增加等待时间
      const waitTime = this.cooldownSeconds * (1 + this.consecutiveErrors);
      
      if (timeSinceLastRequest < waitTime) {
        const actualWaitTime = (waitTime - timeSinceLastRequest) * 1000;
        console.log(`等待 ${actualWaitTime/1000} 秒后重试...`);
        await new Promise(resolve => setTimeout(resolve, actualWaitTime));
      }
      
      this.lastRequestTime = Date.now();
    },
    
    handleSuccess() {
      this.consecutiveErrors = 0;
      this.cooldownSeconds = 1;
    },
    
    handleError() {
      this.consecutiveErrors++;
      // 指数退避策略
      this.cooldownSeconds *= 2;
      
      if (this.consecutiveErrors >= this.maxConsecutiveErrors) {
        throw new Error('连续请求失败次数过多，停止处理');
      }
    }
  };

  function getSystemPrompt(isRecursive, lengthConfig) {
    if (isRecursive) {
      return config.language === 'zh' 
        ? `你是一个专业的文章精简专家。请按照以下要求精简摘要：
           1. 输出长度控制在100字以内
           2. 保留核心信息和关键内容
           3. 删除不必要的修饰词
           4. 使用简练的表达
           5. 保持语言通顺自然`
        : `You are a professional summary condenser. Please follow these requirements:
           6. Keep output within 100 characters
           7. Preserve core information and key content
           8. Remove unnecessary modifiers
           9. Use concise expressions
           10. Maintain natural flow`;
    } else {
      return config.language === 'zh'
        ? `你是一个专业的文章摘要生成器。请为以下文章生成一个中文摘要，要求：
           11. 字数在${lengthConfig.minLength}-${lengthConfig.maxLength}字之间
           12. 完整概括文章主要内容
           13. 突出文章的关键信息
           14. 保持逻辑连贯
           15. 语言简洁清晰`
        : `You are a professional article summarizer. Please generate an English summary that:
           16. Contains ${lengthConfig.minLength}-${lengthConfig.maxLength} words
           17. Comprehensively covers main points
           18. Highlights key information
           19. Maintains logical flow
           20. Uses concise language`;
    }
  }

  async function generateSummary(text, isRecursive = false, retryCount = 0) {
    const contentLength = text.trim().replace(/\s+/g, '').length;
    const lengthConfig = isRecursive 
      ? { minLength: 20, maxLength: 100 }
      : calculateSummaryLength(contentLength, config);
    
    // console.log(`${isRecursive ? '二次摘要' : '原文'}长度：${contentLength}字，目标摘要长度：${lengthConfig.minLength}-${lengthConfig.maxLength}字`);

    try {
      await rateLimiter.waitForCooldown();

      const response = await axios.post('https://api.moonshot.cn/v1/chat/completions', {
        model: config.model || 'moonshot-v1-8k',
        messages: [
          {
            role: "system",
            content: getSystemPrompt(isRecursive, lengthConfig)
          },
          {
            role: "user",
            content: text
          }
        ],
        temperature: isRecursive ? 0.2 : (config.temperature || 0.7),
        max_tokens: lengthConfig.maxLength * 2
      }, {
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json'
        },
        timeout: 30000
      });

      const summary = response.data.choices[0].message.content.trim();
      const summaryLength = config.language === 'zh' 
        ? summary.length 
        : summary.split(/\s+/).length;

      // 检查摘要长度（允许容差）
      if (!isRecursive && summaryLength > (100 + TOLERANCE)) {
        console.log(`生成的摘要(${summaryLength}字)超出容差范围，等待3秒后进行精简...`);
        await delay(3000);
        return await generateSummary(summary, true);
      }
      
      // 二次摘要时也允许容差
      if (isRecursive && summaryLength > (1000 + TOLERANCE)) {
        if (retryCount < 2) {
          console.log(`精简后的摘要(${summaryLength}字)仍超出容差范围，等待2秒后重试第${retryCount + 1}次...`);
          await delay(2000);
          return await generateSummary(text, true, retryCount + 1);
        } else {
          // 如果重试后仍然超出容差范围太多，才进行截断
          if (summaryLength > (100 + TOLERANCE * 2)) {
            console.log(`精简后的摘要显著超出限制，进行截断...`);
            return summary.slice(0, 100 + TOLERANCE);
          }
          return summary; // 在容差范围内则接受
        }
      }

      return summary;
    } catch (error) {
      if (error.response?.status === 429) {
        const waitTime = Math.min(2000 * Math.pow(2, retryCount), 16000);
        console.log(`遇到限流，等待${waitTime/1000}秒后重试...`);
        await delay(waitTime);
        if (retryCount < 3) {
          return await generateSummary(text, isRecursive, retryCount + 1);
        }
      }
      throw error;
    }
  }

  return await generateSummary(content);
}

// 检查文件是否需要更新
async function shouldUpdateFile(filePath, config) {
  try {
    // 如果设置了强制更新，则始终返回 true
    if (config.forceUpdate) {
      return true;
    }

    const stats = await stat(filePath);
    const lastModified = stats.mtime;
    const now = new Date();
    const timeDiff = now - lastModified;
    
    return timeDiff < config.updateWindow;
  } catch (error) {
    console.error('检查文件状态时出错:', error);
    return false;
  }
}

// 修改处理函数
async function processSinglePost(filePath, config, progress) {
  // 检查文件是否正在处理或已处理
  if (processingFiles.has(filePath)) {
    console.log(`[${progress.current}/${progress.total}] ${path.basename(filePath)}: 文件正在处理中，跳过`);
    return;
  }
  
  if (processedFiles.has(filePath)) {
    console.log(`[${progress.current}/${progress.total}] ${path.basename(filePath)}: 文件已处理，跳过`);
    return;
  }

  try {
    processingFiles.add(filePath);

    if (!await shouldUpdateFile(filePath, config)) {
      console.log(`[${progress.current}/${progress.total}] ${path.basename(filePath)}: 文件未更新，跳过处理`);
      return;
    }

    const content = await readFile(filePath, 'utf8');
    const frontMatterMatch = content.match(/^---\n([\s\S]*?)\n---/);
    
    if (!frontMatterMatch) {
      console.log(`[${progress.current}/${progress.total}] ${path.basename(filePath)}: 未找到 front-matter，跳过处理`);
      return;
    }

    const frontMatter = frontMatterMatch[1];
    const postContent = content.slice(frontMatterMatch[0].length).trim();

    console.log(`[${progress.current}/${progress.total}] ${path.basename(filePath)}: 正在生成摘要...`);
    const description = await generateDescription(postContent, config);
    
    if (!description) {
      console.log(`[${progress.current}/${progress.total}] ${path.basename(filePath)}: 生成摘要失败`);
      return;
    }

    let frontMatterLines = frontMatter.split('\n');
    let descriptionFound = false;
    let newFrontMatterLines = frontMatterLines.map(line => {
      if (line.startsWith('description:')) {
        descriptionFound = true;
        return `description: ${description}`;
      }
      return line;
    });

    if (!descriptionFound) {
      newFrontMatterLines.push(`description: ${description}`);
    }

    const newFrontMatter = newFrontMatterLines.join('\n');
    const newContent = '---\n' + newFrontMatter + '\n---\n' + postContent;

    await writeFile(filePath, newContent, 'utf8');
    console.log(`[${progress.current}/${progress.total}] ${path.basename(filePath)}: 成功更新文章摘要`);

    // 处理成功后添加到已处理集合
    processedFiles.add(filePath);
  } finally {
    // 无论成功失败都从处理中集合移除
    processingFiles.delete(filePath);
  }
}

// 并发处理文章
async function processPostsConcurrently(posts, config) {
  // 检查 API 状态
  const apiValid = await checkApiStatus(config);
  if (!apiValid) {
    console.error('API 验证失败，无法处理文章');
    return;
  }

  const total = posts.length;
  let current = 0;
  const progress = { current, total };

  // 创建并发处理队列
  const queue = [];
  for (const post of posts) {
    current++;
    progress.current = current;
    
    // 如果队列已满，等待一个任务完成
    if (queue.length >= config.concurrency) {
      await Promise.race(queue);
    }
    
    // 添加新任务到队列
    const task = processSinglePost(post, config, progress)
      .then(() => {
        // 任务完成后从队列中移除
        const index = queue.indexOf(task);
        if (index !== -1) {
          queue.splice(index, 1);
        }
      });
    
    queue.push(task);
  }
  
  // 等待所有任务完成
  await Promise.all(queue);
}

// 修改后的插件入口
let processedPosts = new Set(); // 用于记录已处理的文章

hexo.extend.filter.register('before_post_render', async function(data) {
  if (data.layout === 'post' && !processedPosts.has(data.full_source)) {
    processedPosts.add(data.full_source);
    const config = getConfig(this);
    
    // 检查是否需要更新
    if (!config.forceUpdate && !await shouldUpdateFile(data.full_source, config)) {
      return data;
    }
    
    const posts = [data.full_source];
    await processPostsConcurrently(posts, config);
  }
  return data;
});

// 在生成完成后清理状态
hexo.extend.filter.register('after_generate', function() {
  processedFiles.clear();
  processingFiles.clear();
});

// 添加命令行命令
hexo.extend.console.register('generate-descriptions', 'Generate descriptions for all posts', {
  options: [
    { name: '--force', desc: 'Force update all posts' },
    { name: '--concurrency', desc: 'Number of concurrent processes' },
    { name: '--validate', desc: 'Validate API key only' },
    { name: '--show-key', desc: 'Show API key source' }
  ]
}, async function(args) {
  const config = getConfig(this);
  
  // 处理命令行参数
  if (args.force) {
    config.forceUpdate = true;
  }
  if (args.concurrency) {
    config.concurrency = parseInt(args.concurrency, 10);
  }

  // 显示 API 密钥来源
  if (args['show-key']) {
    const apiKey = getApiKey(config);
    if (!apiKey) {
      console.log('未设置 API 密钥');
    } else if (process.env.KIMI_API_KEY) {
      console.log('使用环境变量中的 API 密钥');
    } else {
      console.log('使用配置文件中的 API 密钥');
    }
    return;
  }

  // 如果只需要验证 API
  if (args.validate) {
    try {
      await validateApiKey(config);
      console.log('API 验证成功');
    } catch (error) {
      console.error('API 验证失败:', error.message);
    }
    return;
  }

  // 获取所有文章
  const posts = this.model('Post').toArray().map(post => post.full_source);
  
  if (posts.length === 0) {
    console.log('没有找到需要处理的文章');
    return;
  }

  console.log(`开始处理 ${posts.length} 篇文章...`);
  await processPostsConcurrently(posts, config);
  console.log('所有文章处理完成');
}); 
```

{% endfolding %}