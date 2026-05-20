# Codex Cleaner

一个帮你清理本地 Codex 归档会话和废弃项目文件的小工具。

![Codex Cleaner 演示](assets/demo.gif)

当前版本：`v0.1.3` | English README: [README.md](README.md)

Codex Cleaner 是一个本地 Codex Skill，也可以当作 Python 命令行工具使用。它会扫描本地归档会话，显示可读的对话名称，找到每个归档对话对应的本地项目目录，然后让你选择到底删哪一部分。

## 它解决什么问题

Codex 里把对话归档以后，本地项目文件和生成内容可能仍然留在电脑里。时间久了，`Documents/Codex` 下面会出现很多不知道还能不能删的实验项目。

Codex Cleaner 解决的就是这个问题：

> 这个归档对话生成了哪个本地项目？我能不能只删会话、只删文件，或者一起清掉？

## 适合谁

- 经常使用 Codex Desktop、归档了很多对话的人。
- 不懂命令行，希望 Codex 直接显示编号菜单的小白用户。
- 想安全清理 `Documents/Codex` 废弃项目的开发者。
- 想分别选择“只删会话”“只删项目文件”“全部清理”的用户。

## 可以清理什么

Codex Cleaner 会让用户直接选择：

1. 只删除本地归档对话记录，保留项目文件。
2. 只删除本地项目文件，保留归档对话记录。
3. 对话记录和项目文件都清理，移动到 `Codex_Trash`。
4. 彻底删除清空，不进入 `Codex_Trash`，无法恢复。

默认模式很保守：先预览，不直接删；默认移动到 `~/Documents/Codex_Trash`；默认只清理 `~/Documents/Codex` 里的项目，避免误删其他目录。

## 安装 Skill

在 Codex 里输入：

```text
$skill-installer install https://github.com/manganeseboy/codex-cleaner/tree/main/skills/codex-cleaner
```

安装后重启 Codex，让新的 Skill 生效。

## 小白怎么用

安装 Skill 后，直接对 Codex 说：

```text
使用 codex-cleaner 帮我扫描归档对话
```

Codex 会展示归档对话编号列表。你只需要回复一个编号，比如 `2`，或者多个编号，比如 `2,3,5`。

然后 Codex 会展示清理方式菜单：

```text
你想清理哪一部分？
1. 只删除本地归档对话记录，保留项目文件
2. 只删除本地项目文件，保留归档对话记录
3. 对话记录和项目文件都清理，移动到 Codex_Trash
4. 彻底删除清空，不进入 Codex_Trash，无法恢复
```

Codex 会先预览具体会影响哪些本地路径。你确认以后才会真正清理。第 4 项是永久删除，需要额外明确确认。

## 命令行用法

对普通用户，更推荐上面的 Skill 流程。下面命令主要给技术用户和测试使用。

扫描归档会话：

```powershell
python .\scripts\codex_cleaner.py scan
```

输出 JSON：

```powershell
python .\scripts\codex_cleaner.py scan --json
```

只删除会话记录、保留项目文件：

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --conversation-only
```

只删除项目文件、保留会话记录：

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --files-only
```

对话记录和项目文件都移动到 `Codex_Trash`：

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both
```

真正执行清理：

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both --yes
```

永久删除，不进入 `Codex_Trash`：

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both --permanent
python .\scripts\codex_cleaner.py clean --index 3 --target both --permanent --yes
```

## 支持中英文对话名称

扫描表会显示 `Title` 列，也就是从对话里的第一条真实用户需求自动生成的可读名称。中文和英文对话名称都支持，也会尽量跳过常见的文件上传前缀。

按中文关键词预览清理：

```powershell
python .\scripts\codex_cleaner.py clean --title "认证机构" --target both
```

按英文关键词预览清理：

```powershell
python .\scripts\codex_cleaner.py clean --title "certification agency" --target both
```

## 已安装用户如何更新

已经安装过的用户不会自动收到 GitHub 推送更新。Skill 会被复制到用户本机的 Codex skills 文件夹里，所以更新的本质是：删除旧的本地副本，再从 GitHub 重新安装最新版。

可以让用户直接对 Codex 说：

```text
我已经安装过 codex-cleaner，请帮我删除旧版本并重新安装最新版。
地址：
https://github.com/manganeseboy/codex-cleaner/tree/main/skills/codex-cleaner
```

更新后需要重启 Codex，让新的 skill 说明生效。想收到新版本提醒的用户，可以关注 GitHub 仓库，或者查看 [Releases 页面](https://github.com/manganeseboy/codex-cleaner/releases)。

## 安全原则

- `clean` 默认只是 dry-run，必须加 `--yes` 才会执行。
- 默认移动到 `~/Documents/Codex_Trash`。
- 永久删除必须显式加 `--permanent --yes`。
- 默认不会删除 `~/Documents/Codex` 之外的项目。
- 检测多个归档会话是否指向同一个项目目录。
- 本工具只清理本地文件和本地归档日志。
- 本工具不会删除云端 ChatGPT/Codex 历史。
- 本工具不会接管 Codex UI 里的归档按钮。
- 本工具在本地运行，不会把会话记录或文件内容发送到远程服务。

## 推广素材

如果你想把这个工具分享给朋友或社区，可以直接参考：

- [小红书推广文案](docs/promotion/xiaohongshu.md)
- [社区发布文案](docs/promotion/community-posts.md)
- [朋友安装教学](docs/promotion/share-with-friends.md)

## 许可证

MIT
