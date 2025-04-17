---
title: FileTAG 为文件搜索模块添加数据库索引
date: 2024/10/29
tags:
  - cpp
  - QT
  - 多线程
  - 数据库
categories: [项目开发, C++]
description: 
cover: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
banner: https://blog-imges-1313931661.cos.ap-nanjing.myqcloud.com/20200317211943_Ts5Y5.gif
poster:
  headline: 为文件搜索模块添加数据库索引
  caption: 
  color: 
sticky: 
mermaid: 
katex: true
mathjax: true
author: Montee
references: 
comments: 
indexing: 
breadcrumb: 
leftbar: 
rightbar: 
h1: 
type: tech
---

这个模块起初是基于一篇文章的启发：[Everything 原理与实现](https://www.cnblogs.com/xuanxu233/p/16083526.html) 当然，Everything 并不是一个开源的软件，其真实的原理，我也没有查到。

在 101 询问了一下，或许可以通过使用数据库索引的方式来优化文件索引过程，提高搜索速度。本篇博客将分享如何通过引入 SQLite 数据库，实现文件信息的持久化存储和高效索引，显著提升文件搜索的性能。

当然这只是初步实现，问题还“非常的多”！！！。

# 1. 设计方案

## 引入 SQLite 数据库

### 架构概述

* FileDatabase 类：用于管理数据库的连接、表的创建、文件信息的插入与查询。

现阶段实现的主要功能模块如下：
1. 数据库的连接：负责与SQLite数据库建立连接。
2. 表创建：定义文件信息和关键词的存储结构。
3. 文件信息插入：将文件的路径、名称等信息存入数据库。
4. 关键词管理：为每个文件存储关键词以便于快速检索。
5. 文件搜索：基于文件路径、名称或关键词进行模糊搜索。

下面结合代码逐一介绍。

### 数据库的连接与管理

```C
bool FileDatabase::openDatabase() {
    if (QSqlDatabase::contains("file_db_connection")) {
        db = QSqlDatabase::database("file_db_connection");
    } else {
        db = QSqlDatabase::addDatabase("QSQLITE", "file_db_connection");
        db.setDatabaseName(databaseName);
    }

    if (!db.open()) {
        QString errorMessage = QString("无法打开数据库: %1").arg(db.lastError().text());
        qDebug() << errorMessage;
        LOG_ERROR(errorMessage);
        return false;
    }

    LOG_INFO("数据库连接成功：" + databaseName);
    return createTables();
}
```


在这个函数中，我们首先检查是否已经存在名为 `"file_db_connection"` 的数据库连接，如果存在则复用该连接，否则创建一个新的连接，并指定使用的数据库类型为 `QSQLITE`。数据库成功打开后，会调用 `createTables()` 方法创建所需的数据表。

在数据库的造作过程中，随时可能遇到连接失败、查询语句错误等问题。因此为了便于调试和维护，在数据库操作的各个函数中都添加了详细的错误记录信息，同时输出到控制台和 log 日子中。


### 数据库表设计

在项目中，定义了两个主要的表：`files` 和 `file_keywords`。下面是表的创建代码及其设计解释：

```C
QString sqlCreateFiles = R"(
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        name TEXT,
        extension TEXT,
        birth_time TEXT,
        last_modified TEXT
    )
)";
```

- `id`：主键，用于唯一标识文件记录。
- `path`：文件的绝对路径，保证唯一性，便于后续的快速检索。
- `name` 和 `extension`：分别记录文件的名称和扩展名，便于用户按名称或类型进行搜索。
- `birth_time` 和 `last_modified`：记录文件的创建时间和最后修改时间，用于时间范围内的查询。

```C
QString sqlCreateFileKeywords = R"(
    CREATE TABLE IF NOT EXISTS file_keywords (
        file_id INTEGER,
        keyword TEXT,
        FOREIGN KEY (file_id) REFERENCES files(id)
    )
)";
```

- `file_id`：关联到 `files` 表的 `id` 字段，表示该关键词属于哪一个文件。
- `keyword`：存储文件相关的关键词，用于内容搜索。
### 数据的插入与更新

```C
bool FileDatabase::insertFileInfo(const QString &filePath) {
    if (!db.isOpen()) {
        LOG_ERROR("数据库未打开，无法插入文件信息。");
        return false;
    }

    QFileInfo fileInfo(filePath);
    QSqlQuery query(db);
    query.prepare(R"(
        INSERT OR REPLACE INTO files (path, name, extension, birth_time, last_modified)
        VALUES (?, ?, ?, ?, ?)
    )");
    query.addBindValue(fileInfo.absoluteFilePath());
    query.addBindValue(fileInfo.fileName());
    query.addBindValue(fileInfo.suffix());
    query.addBindValue(fileInfo.birthTime().toString("yyyy-MM-dd HH:mm:ss"));
    query.addBindValue(fileInfo.lastModified().toString("yyyy-MM-dd HH:mm:ss"));

    if (!query.exec()) {
        QString errorMessage = QString("插入文件信息失败: %1").arg(query.lastError().text());
        qDebug() << errorMessage;
        LOG_ERROR(errorMessage);
        return false;
    }

    LOG_INFO("文件信息插入成功：" + filePath);
    return true;
}
```



### 关键词插入

```C
void FileDatabase::insertFileKeywords(int fileId, const QVector<QString> &keywords) {
    if (!db.isOpen()) {
        LOG_ERROR("数据库未打开，无法插入关键词。");
        return;
    }

    QSqlQuery query(db);
    for (const QString &keyword : keywords) {
        query.prepare("INSERT INTO file_keywords (file_id, keyword) VALUES (?, ?)");
        query.addBindValue(fileId);
        query.addBindValue(keyword);

        if (!query.exec()) {
            QString errorMessage = QString("插入关键词失败，文件 ID: %1, 关键词: %2, 错误信息: %3")
                    .arg(fileId)
                    .arg(keyword)
                    .arg(query.lastError().text());
            qDebug() << errorMessage;
            LOG_ERROR(errorMessage);
        } else {
            LOG_INFO("关键词插入成功，文件 ID: " + QString::number(fileId) + ", 关键词: " + keyword);
        }
    }
}

```

### 文件搜索功能实现

```C
QVector<QString> FileDatabase::searchFiles(const QString &keyword) {
    QVector<QString> resultPaths;
    if (!db.isOpen()) {
        LOG_ERROR("数据库未打开，无法搜索文件。");
        return resultPaths;
    }

    QSqlQuery query(db);
    QString sql = R"(
        SELECT path FROM files
        WHERE path LIKE '%' || ? || '%'
        OR name LIKE '%' || ? || '%'
        OR EXISTS (
            SELECT 1 FROM file_keywords
            WHERE file_keywords.file_id = files.id
            AND file_keywords.keyword LIKE ?
        )
    )";
    query.prepare(sql);
    query.addBindValue(keyword);
    query.addBindValue(keyword);
    query.addBindValue(keyword);

    if (query.exec()) {
        while (query.next()) {
            resultPaths.append(query.value(0).toString());
        }
        LOG_INFO(QString("搜索完成，找到 %1 个匹配文件。").arg(resultPaths.size()));
    } else {
        QString errorMessage = QString("执行搜索查询失败: %1").arg(query.lastError().text());
        LOG_ERROR(errorMessage);
    }

    return resultPaths;
}

```



## 文件搜索逻辑修改



在 `FileSearch` 类中集成 `FileDatabase` 实例，使得文件搜索逻辑可以使用数据库：

- **初始化与连接**：
    - 在 `FileSearch` 的构造函数中，初始化 `FileDatabase` 对象，并调用 `openDatabase()` 和 `createTables()` 确保数据库连接和表结构就绪。
- **搜索流程优化**：
    - 修改 `onSearchButtonClicked()` 方法，在用户发起搜索请求时，先从数据库中查找匹配的文件。如果数据库中没有结果，再执行传统的文件系统遍历搜索。
    - 通过 `onFileFound()` 方法，当文件被找到时，除了在 UI 上展示，还将文件信息插入数据库，以便后续搜索更快速。

## 提取关键词与搜索优化

我们为文件搜索模块新增了关键词提取功能，使得用户可以通过关键词快速定位文件：

- `extractKeywordsFromFile()`：使用正则表达式匹配文件内容中的关键词，并通过停用词过滤，生成关键词列表。
- 将这些关键词与文件 ID 一起存入 `file_keywords` 表，使得用户可以通过关键词直接找到相关文件。

详细代码如下：

```C
QVector<QString> FileSearch::extractKeywordsFromFile(const QString &filePath) {  
    QVector<QString> keywords;  
    QFile file(filePath);  
  
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {  
        qDebug() << "无法打开文件进行关键词提取:" << filePath;  
        return keywords;  
    }  
  
    QTextStream in(&file);  
    QString content = in.readAll();  
    file.close();  
  
    // 使用正则表达式匹配所有单词  
    QRegularExpression wordRegex("\\b\\w+\\b");  
    QRegularExpressionMatchIterator it = wordRegex.globalMatch(content.toLower());  
  
    // 停用词列表（可以根据需要添加更多停用词）  
    QSet<QString> stopwords = {"the", "and", "is", "in", "to", "of", "a", "an"};  
  
    // 提取并过滤关键词  
    while (it.hasNext()) {  
        QRegularExpressionMatch match = it.next();  
        QString word = match.captured(0);  
  
        // 过滤掉长度小于等于2的词和停用词  
        if (word.length() > 2 && !stopwords.contains(word)) {  
            keywords.append(word);  
        }  
    }  
  
    return keywords;  
}
```

在实际运行过程中发现，有些文件会给出 **“无法打开文件进行关键词提取:”** 的提示，定位到这个地方。发现在判断语句中要先尝试能否以只读和文本模式打开文件，如果打开失败，输出调试信息并返回空的关键词列表。

然而我们的实际需求是：只是从文件名中提取关键词，而不是文件内容，所以并不需要打开文件。故修改代码为：

```C
QVector<QString> FileSearch::extractKeywordsFromFile(const QString &filePath) {  
    QVector<QString> keywords;  
      
    QString filename = QFileInfo(filePath).fileName();  
  
    // 使用正则表达式匹配所有单词  
    QRegularExpression wordRegex("\\b\\w+\\b");  
    QRegularExpressionMatchIterator it = wordRegex.globalMatch(filename.toLower());  
  
    // 停用词列表（可以根据需要添加更多停用词）  
    QSet<QString> stopwords = {"the", "and", "is", "in", "to", "of", "a", "an"};  
  
    // 提取并过滤关键词  
    while (it.hasNext()) {  
        QRegularExpressionMatch match = it.next();  
        QString word = match.captured(0);  
  
        // 过滤掉长度小于等于2的词和停用词  
        if (word.length() > 2 && !stopwords.contains(word)) {  
            keywords.append(word);  
        }  
    }  
  
    return keywords;  
}
```
# 2. 现阶段问题

1. 批量更新搜索文件功能缺失
2. 现在的代码完全基于数据库搜索，如何平衡数据库搜索与遍历文件系统
3. 如何高效地创建于定时更新数据库
4. 搜索结果显示错误，只要路径中含有 keyword 就会被显示
5. 如何合理的设计索引表，即如何把文件书转化为关系型数据库，要能够在不占用过多磁盘空间的前提下，设计出一种便于搜索的数据表
6. 在程序启动时，要能对数据库进行判断，是建立新的文件索引数据库，或者是检查更新
7. 数据库安全问题
8. ……  