---
title: Git-reset、checkout、分离头指针
date: 2025/4/22
tags:
  - Git
categories:
  - 技术学习
author: Forsertee
type: tech
description: 本文分析了Git中的reset和checkout命令对HEAD、Index和工作目录的影响。解释了这三个树结构的作用，描述了reset如何操作它们，包括移动HEAD、更新Index和工作目录，以及带路径的reset和压缩提交记录。同时讨论了checkout与reset的区别，特别是在无路径和有路径情况下的行为，以及Detached HEAD的概念。目的是帮助读者深入理解reset命令，提高使用熟练度。
---
# 引言

在我的博客中， Stellar 主题作为子模块放在了 Hexo 仓库之下。在我使用 Vercel 部署时，有时会出现下面这种部署失败的情况：
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422215925546.png?imageSlim)
他的直接原因是，Stellar主题中自定义的组件找不到，进而导致部署失败。

我进一步查看分析是哪一个Git提交导致了问题，顺着提交记录，我查看仓库的代码发现 Stellar 仓库中并没有提交这次修改。
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422220328811.png?imageSlim)

那就简单了，我只要把本地的修改提交上去就OK了。然而，如果真的可以这样解决也就不会有这篇文章了。

所以要引出这篇博客的重点：**git 分离头指针**

> 注：一下相关内容翻译自 git 官方文档 *~~（阅读官方文档好习惯，WIN）~~*

# reset 与 checkout

在深入探讨更专业的工具之前，让我们先聊聊 Git 的 reset 和 checkout 命令。当你初次接触这些命令时，它们是 Git 中最容易让人困惑的两个部分。它们的功能繁多，以至于似乎根本无法真正理解并正确使用它们。为此，我们推荐一个简单的比喻。

一种更简单的理解 reset 和 checkout 的方式是，将 Git 视为一个管理三棵不同“树”的内容管理器。这里的“树”，实际上指的是“文件集合”，而非特指某种数据结构。在某些情况下，暂存区并不完全像一棵树那样运作，但就我们目前的目的而言，这样理解会更简单一些。

Git作为一个系统，在其正常操作中管理和操作三个树结构：

| Tree  | Role         |
| ----- | ------------ |
| HEAD  | 上次提交快照，下一个父级 |
| Index | 建议的下一个提交快照   |
| 工作目录  | 沙盒           |


## HEAD

HEAD 是指向当前分支引用的指针，而该引用又是指向在该分支上进行的最后一次提交的指针。这意味着 HEAD 将成为下一个创建的提交的父提交。通常，将 HEAD 简单地理解为该分支上最后一次提交的快照是最容易的。实际上，查看该快照的样子非常容易。以下是一个获取 HEAD 快照中每个文件的实际目录列表和 SHA-1 校验和的示例。

```shell
$ git cat-file -p HEAD

tree cfda3bf379e4f8dba8717dee55aab78aef7f4daf
author Scott Chacon  1301511835 -0700
committer Scott Chacon  1301511835 -0700

initial commit

$ git ls-tree -r HEAD

100644 blob a906cb2a4a904a152...   README
100644 blob 8f94139338f9404f2...   Rakefile
040000 tree 99f1a6d12cb4b6f19...   lib
```

Git 的 cat-file 和 ls-tree 命令是用于底层操作的“基础”命令，并不常用于日常工作中，但它们有助于我们了解这里发生了什么。

## The Index

Index 是你提议的下一次提交内容。我们也一直将这个概念称为 Git 的“暂存区”，因为当你运行 git commit 时，Git 就会查看这个区域。Git 会将最后一次检出到工作目录中的所有文件内容及其最初检出时的样子列在这个 Index 中。然后你用这些文件的新版本替换其中的一些文件，git commit 会将这些更改转换为新提交对应的树结构。

```shell
$ git ls-files -s
100644 a906cb2a4a904a152e80877d4088654daad0c859 0	README
100644 8f94139338f9404f26296befa88755fc2598c289 0	Rakefile
100644 47c6340d6459e05787f644c2447d2595f5d3a54b 0	lib/simplegit.rb
```

从技术上讲，Index 并不是树状结构——实际上它是作为一个扁平化的清单来实现的。


## The Working Directory（工作区）

最后，你拥有了自己的工作目录（通常也被称为“工作树”）。另外两个树以高效但不便的方式将其内容存储在 .git 文件夹内。工作目录会将它们解压成实际文件，这使得你编辑它们变得更加容易。可以把工作目录想象成一个沙盒，在这里你可以尝试进行更改，然后再将它们提交到暂存区（索引），最后提交到历史记录中。

```shell
$ tree
.
├── README
├── Rakefile
└── lib
    └── simplegit.rb

1 directory, 3 files
```

## The Workflow
Git 的典型工作流程是通过操作这三个树结构，依次将项目的状态以快照的形式记录下来，使其逐步完善。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422223814356.png?imageSlim)

让我们来可视化这个过程：假设你进入一个新目录，里面有一个文件。我们将这个文件称为版本1，并用蓝色表示。现在我们运行 git init，这将创建一个 Git 仓库，其中包含一个 HEAD 引用，该引用指向尚未创建的 master 分支。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422223901247.png?imageSlim)

此时，只有工作目录树中有内容。现在我们要提交这个文件，因此使用 `git add` 将工作目录中的内容复制到暂存区。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422225839819.png?imageSlim)

然后我们运行 git commit 命令，它会将暂存区的内容保存为一个永久快照，创建一个指向该快照的提交对象，并更新 master 分支以指向该提交。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422225926988.png?imageSlim)
如果我们运行 git status，将看不到任何变更，因为这三个树结构是完全相同的。

现在我们要对该文件进行修改并提交。我们将重复相同的过程；首先，在工作目录中修改该文件。我们称这个版本为文件的第二版，并用红色标注它。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422230033942.png?imageSlim)

如果我们现在运行 git status，会看到该文件以红色显示为“Changes not staged for commit”（未暂存的更改），因为该条目在 Index 和工作目录之间存在差异。接下来我们对其运行 git add 以将其暂存到索引中。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422230116250.png?imageSlim)
此时，如果我们运行 git status，会看到文件以绿色显示在“Changes to be committed”（待提交的更改）下，这是因为索引和 HEAD 不同——也就是说，我们提议的下一次提交现在与上一次提交不同。最后，我们运行 git commit 来完成提交。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422230149735.png?imageSlim)

现在 `git status` 不会给出任何输出，因为三个树又变得相同了。切换分支或克隆的过程与此类似。当你检出某个分支时，它会将 HEAD 更改为指向新的分支引用，用该提交的快照填充你的暂存区，然后将暂存区的内容复制到你的工作目录中。

## reset 的作用

为了演示 reset 的作用，假设我们再次修改了file.txt文件，并进行了第三次提交。所以现在我们的历史记录看起来是这样的：

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422230351757.png?imageSlim)

让我们现在详细了解一下调用 reset 时它具体会做些什么。它会以一种简单且可预测的方式直接操作这三棵树。它最多会执行三个基本操作。

### 移动 HEAD 指针

reset 首先执行的操作是移动 HEAD 所指向的内容。这与更改 HEAD 本身（这是 checkout 的功能）不同；reset 是移动 HEAD 所指向的分支。这意味着，如果 HEAD 设置在 master 分支上（即你当前位于 master 分支），运行 git reset 9e5e6a4 将首先使 master 指向 9e5e6a4。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422230459917.png?imageSlim)
无论你调用哪种带有提交记录的重置形式，这总是它首先要尝试执行的操作。使用 reset --soft 时，它将仅止步于此。

现在花点时间看看那个图表并弄明白发生了什么：它本质上撤销了上一次的 `git commit` 命令。当你运行 `git commit` 时，Git 会创建一个新的提交，并将 HEAD 所指向的分支移动到该提交上。当你重置回 `HEAD~`（HEAD 的父提交）时，你实际上是将分支移回到之前的位置，而不会改变暂存区或工作目录。此时，你可以更新暂存区并再次运行 `git commit`，以实现 `git commit --amend` 所能达到的效果（参见修改最后一次提交）。


### 更新 Index（--mixed）

请注意，如果你现在运行 git status，你会看到以绿色显示的索引与新 HEAD 之间的差异。reset 接下来要做的事情是用 HEAD 现在所指向的快照内容来更新索引。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422231525797.png?imageSlim)

如果你指定了 --mixed 选项，reset 将在此处停止。这也是默认行为，所以如果你完全不指定任何选项（在这种情况下仅使用 git reset HEAD~），命令也会在此处停止。现在再花一秒钟看看那个图表，弄清楚发生了什么：它仍然撤销了你的最后一次提交，但同时也取消暂存了所有内容。你回退到了运行所有 git add 和 git commit 命令之前的状态。
### 更新工作区

重置的第三件事是使工作目录与 Index 保持一致。如果你使用 --hard 选项，它将继续执行到这一阶段。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422231848031.png?imageSlim)

所以让我们来思考一下刚刚发生了什么。你撤销了上一次提交、`git add` 和 `git commit` 命令，以及你在工作目录中所做的所有工作。

需要注意的是，`--hard` 标志是让 `reset` 命令变得危险的唯一方式，也是 **Git 实际上会销毁数据的极少数情况之一**。其他任何形式的 `reset` 都可以很容易地撤销，但 `--hard` 选项却不行，因为它会强制覆盖工作目录中的文件。在这个特定的案例中，我们仍然可以在 Git 数据库的某个提交中找到文件的 v3 版本，并且可以通过查看引用日志将其恢复，但如果我们没有提交它，Git 仍然会覆盖该文件，并且它将无法恢复。

### 回顾

重置命令会按照特定顺序覆盖这三个树结构，并在你指示时停止：
1. 将分支 HEAD 指向指定记录（如果使用--soft则在此停止）。
2. 使 Index（暂存区）与HEAD（除非使用--hard，否则在此停止）。
3. 使工作目录与Index（暂存区一致）。

## 带路径的 reset

这涵盖了重置（reset）在其基本形式下的行为，但你也可以为它提供一个路径以对其执行操作。如果你指定了一个路径，重置将跳过第一步，并将其后续操作限制在特定的文件或一组文件上。这实际上是有道理的——HEAD 只是一个指针，你不能既指向一个提交的部分内容，又指向另一个提交的部分内容。但Index和工作目录可以部分更新，所以重置会继续执行第二步和第三步。

所以，假设我们运行 git reset file.txt。这种形式（因为你没有指定提交的 SHA - 1 值或分支，并且你也没有指定 --soft 或 --hard）是 git reset --mixed HEAD file.txt 的简写形式，它将：
1. 移动分支 HEAD 所指向的位置（跳过）
2. 让暂存区看起来和 HEAD 一样（到此为止）

因此，它本质上只是将 file.txt 从 HEAD 复制到Index暂存区中。
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422232750158.png?imageSlim)

这实际上会产生取消暂存文件的效果。如果我们查看该命令的示意图，并思考 git add 的作用，它们恰好完全相反。
![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422232827923.png?imageSlim)

这就是为什么 git status 命令的输出会建议你运行此命令来取消暂存文件（有关更多信息，请参阅“取消暂存已暂存的文件”）。我们同样可以轻松地不让 Git 默认我们认为的“从 HEAD 拉取数据”，而是指定一个特定的提交来拉取该文件版本。我们只需运行类似 git reset eb43bf file.txt 的命令即可。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422232906701.png?imageSlim)

这实际上与我们在工作目录中将文件内容恢复到 v1 版本，对其执行 `git add` 操作，然后再将其恢复到 v3 版本（但实际上并未经历所有这些步骤）所产生的效果是一样的。如果我们现在运行 `git commit` 命令，它会记录一次变更，将文件恢复到 v1 版本，尽管我们实际上从未再次将其恢复到工作目录中。

值得注意的是，与 git add 类似，reset 命令也接受 --patch 选项，以便基于块（hunk）逐块取消暂存内容。因此，你可以选择性地取消暂存或还原内容。

## Squashing
让我们来看看如何利用这新获得的能力做一些有趣的事情——压缩提交（squashing commits）。

假设你有一系列提交信息类似“oops”、“WIP”和“forgot this file”的提交记录。你可以使用 reset 命令快速且轻松地将它们压缩成一个让你看起来非常聪明的提交记录。《压缩提交记录》展示了另一种实现此操作的方法，但在本例中使用 reset 更简单。

假设你的项目中，第一次提交包含一个文件，第二次提交添加了一个新文件并对第一个文件进行了修改，第三次提交又对第一个文件进行了修改。第二次提交是进行中的工作，你想要将其压缩。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422233412117.png?imageSlim)


你可以运行 `git reset --soft HEAD~2` 命令将 HEAD 分支回退到较旧的提交（即保留的最新提交）。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422233433990.png?imageSlim)

然后再简单地运行 git commit 命令:

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422233524596.png?imageSlim)

现在你可以看到，你的可追溯历史（即你将推送的历史）现在看起来像是你有一个提交包含了 file-a.txt 的 v1 版本，然后第二个提交同时将 file-a.txt 修改为 v3 版本并添加了 file-b.txt 文件。而包含该文件 v2 版本的提交已不再存在于历史记录中。

## Check IT Ouut

最后，你可能会想知道“checkout”和“reset”之间有什么区别。与reset一样，checkout会操作三个树结构，并且根据你是否给该命令提供文件路径，它的行为会有所不同。

### Without Paths
运行 `git checkout [分支]` 与运行 `git reset --hard [分支]` 非常相似，因为它们都会将你的三个树结构更新为与 [分支] 相同的状态，但两者之间存在两个重要的区别。

首先，与 `reset --hard` 不同，`checkout` 对工作目录是安全的；它会检查以确保不会覆盖那些已被修改的文件。实际上，它比这更智能——它会尝试在工作目录中进行平凡合并（trivial merge），因此所有你未修改的文件都会被更新。而 `reset --hard` 则会直接替换所有内容，不做任何检查。

第二个重要的区别在于checkout操作更新 HEAD 的方式。reset会移动 HEAD 所指向的分支，而检出操作则会移动 HEAD 本身，使其指向另一个分支。

例如，假设我们有一个主分支（master）和一个开发分支（develop），它们指向不同的提交，而我们当前位于开发分支（develop），因此 HEAD 指向它。如果我们运行 git reset master，那么 develop 分支本身现在将指向与 master 相同的提交。如果我们改为运行 git checkout master，develop 分支不会移动，而是 HEAD 本身会移动。现在 HEAD 将指向 master。

因此，在这两种情况下，我们都是将 HEAD 移动到指向提交 A，但我们这样做的方法是截然不同的。reset 会移动分支 HEAD 所指向的位置，而 checkout 则是移动 HEAD 本身。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422234016064.png?imageSlim)

### With Paths
另一种运行checkout操作的方式是使用文件路径，这与 reset 类似，不会移动 HEAD。它就像 git reset [branch] file 一样，会将索引更新为该提交下该文件的状态，但它还会覆盖工作目录中的文件。这完全类似于 git reset --hard [branch] file（如果 reset 允许你这样运行），它不安全，不会移动工作目录，也不会移动 HEAD。此外，像 git reset 和 git add 一样，checkout 也接受 --patch 选项，允许你以块为单位选择性地还原文件内容。

## 总结
希望你现在对 reset 命令有了更深入的理解，并且使用起来更加得心应手，但可能仍然对它与 checkout 命令的具体区别感到困惑，而且不太可能记住所有不同调用方式的规则。

以下是关于哪些命令会影响哪些树的速查表。“HEAD”列显示为“REF”表示该命令会移动 HEAD 所指向的引用（分支），显示为“HEAD”则表示会移动 HEAD 本身。特别注意“WD Safe?”列——如果显示为 NO，在执行该命令前请三思。

![image.png](https://blog-image-0407-1313931661.cos.ap-nanjing.myqcloud.com/20250422234441388.png?imageSlim)

# 头指针分离（ Detached HEAD）

分离头指针是Git中的一种状态，表示HEAD指针不再指向任何分支的引用(如master、develop等)，而是直接指向一个特定的提交(commit)。


正常情况下，HEAD 指向一个分支引用，分支引用再指向最新的提交；但是如果发生分离头指针，HEAD则会指向一个具体的提交记录。

也就是发生在上一个章节描述的 `git checkout` 指令中。

如果 checkout 的是某次提交的 id，如：

```shell
git checkout abc1234
```

就会出现分离头指针的情况。

在这个状态下，做的任何提交都不会更新任何分支。并且这个状态下的提交如果不创建分支或标签，可能会被 Git 的垃圾回收清理。

这也就是我在本文最初讲述的为什么 Hexo 仓库找不到 子仓库 push 的原因。

处理头指针分离通常采用，创建新分支的方法：
```shell
git branch new-feature
git checkout new-feature
```
# 引用
* [# 7.7 Git Tools - Reset Demystified](https://git-scm.com/book/en/v2/Git-Tools-Reset-Demystified.html#_the_head)