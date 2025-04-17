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
           1. Keep output within 100 characters
           2. Preserve core information and key content
           3. Remove unnecessary modifiers
           4. Use concise expressions
           5. Maintain natural flow`;
    } else {
      return config.language === 'zh'
        ? `你是一个专业的文章摘要生成器。请为以下文章生成一个中文摘要，要求：
           1. 字数在${lengthConfig.minLength}-${lengthConfig.maxLength}字之间
           2. 完整概括文章主要内容
           3. 突出文章的关键信息
           4. 保持逻辑连贯
           5. 语言简洁清晰`
        : `You are a professional article summarizer. Please generate an English summary that:
           1. Contains ${lengthConfig.minLength}-${lengthConfig.maxLength} words
           2. Comprehensively covers main points
           3. Highlights key information
           4. Maintains logical flow
           5. Uses concise language`;
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