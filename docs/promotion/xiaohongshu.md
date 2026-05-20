# Xiaohongshu Promotion Pack

## Cover Text Ideas

- Codex 用久了？废项目一键看清
- 归档不等于删除，本地文件还在
- 清理 Codex 废弃项目，我做了个小工具
- 不懂命令行也能清理 Codex 归档会话

## Title Options

1. Codex 用久了电脑越来越乱？我做了个本地清理 Skill
2. 原来 Codex 归档后，本地生成文件可能还在
3. 写给 Codex 用户：别再手动猜哪个文件夹能删了
4. 我做了个 Codex Cleaner，可以按对话名称清理废项目
5. 小白也能用的 Codex 归档会话清理工具

## Main Post

最近我发现一个很真实的问题：

Codex 里的对话归档了，但本地生成的项目文件不一定会一起消失。用久了以后，`Documents/Codex` 下面会堆很多实验项目，看名字也不一定知道对应哪次对话。

所以我做了一个小工具：Codex Cleaner。

它可以帮你扫描本地 Codex 归档会话，把对话名称和本地项目文件夹对应起来，然后直接显示编号让你选。

现在支持 4 种清理方式：

1. 只删除归档对话记录，保留项目文件。
2. 只删除本地项目文件，保留对话记录。
3. 对话和项目文件都清理，先移动到 Codex_Trash。
4. 彻底删除清空，不进回收区，需要二次确认。

对小白比较友好的点是：安装成 Codex Skill 后，不需要自己敲复杂命令。你直接对 Codex 说：

```text
使用 codex-cleaner 帮我扫描归档对话
```

它会把归档对话列出来，你回复编号就可以。

我做这个不是为了“自动删东西”，而是为了让删除之前先看清楚：

- 这个归档对话叫什么？
- 它对应哪个本地项目？
- 项目大概占多少空间？
- 我要删会话、删文件，还是两个都清？

GitHub 地址：

```text
https://github.com/manganeseboy/codex-cleaner
```

适合经常用 Codex 做实验、生成项目、测试小工具的人。尤其是像我这种：试了很多想法，最后电脑里全是“好像可以删但又不敢删”的文件夹。

## Comment Prompts

- 你们的 `Documents/Codex` 文件夹现在多大了？
- 你更需要“只删对话”还是“只删项目文件”？
- 如果你也在用 Codex，可以试试这个 Skill，有问题我继续改。

## Hashtags

#Codex #AI工具 #效率工具 #GitHub开源 #程序员工具 #AI编程 #电脑清理 #小白工具 #开源项目 #CodexSkill
