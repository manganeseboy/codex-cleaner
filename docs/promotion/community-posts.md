# Community Promotion Posts

## GitHub Discussion

Title:

```text
Codex Cleaner: safely map archived Codex conversations to local workspace folders
```

Body:

```text
I built Codex Cleaner because archived Codex conversations can leave local generated workspaces behind. After many experiments, it becomes hard to know which folder belongs to which archived conversation.

Codex Cleaner scans local archived session logs, extracts readable conversation titles, maps each session to its recorded cwd, and lets users choose:

1. Delete archived conversation only.
2. Delete local project files only.
3. Move both to Codex_Trash.
4. Permanently delete both with extra confirmation.

It is designed as a Codex Skill first, so non-technical users can ask Codex to scan, pick numbers from a list, and confirm cleanup safely.

Repo:
https://github.com/manganeseboy/codex-cleaner
```

## V2EX

标题：

```text
做了一个 Codex Cleaner，用来清理归档会话对应的本地废项目
```

正文：

```text
最近用 Codex 做实验比较多，发现一个问题：对话归档以后，本地 Documents/Codex 里的项目文件并不一定会同步清掉。

时间久了以后，本地会有很多不知道能不能删的目录。手动删又怕删错。

所以做了一个小工具 Codex Cleaner：

- 扫描本地归档 Codex 会话。
- 显示可读的中英文对话名称。
- 找到每个归档会话对应的本地项目目录。
- 可以选择只删会话、只删项目文件、两者都移到 Codex_Trash，或者二次确认后永久删除。

它也可以作为 Codex Skill 安装。安装后直接让 Codex 扫描归档对话，然后回复编号就行，不需要用户自己敲复杂命令。

GitHub:
https://github.com/manganeseboy/codex-cleaner

欢迎试用和提建议，尤其是 Codex Desktop 用户。
```

## Reddit

Title:

```text
I made a local Codex cleanup skill for archived sessions and generated workspaces
```

Body:

```text
I built a small local tool called Codex Cleaner.

The problem: after archiving Codex conversations, local generated workspace folders can still remain on disk. After enough experiments, it becomes difficult to know which folder belongs to which archived conversation.

The tool scans local archived Codex sessions, extracts readable titles, maps them to the recorded workspace path, and offers four cleanup choices:

1. Delete archived conversation logs only.
2. Delete local project files only.
3. Move both to Codex_Trash.
4. Permanently delete both with extra confirmation.

It is designed to run locally and does not send session data anywhere.

GitHub:
https://github.com/manganeseboy/codex-cleaner
```

## X / Twitter

```text
I made Codex Cleaner, a local Codex Skill for cleaning archived sessions and generated workspace folders.

It shows readable conversation titles, maps them to local project paths, and lets you delete conversation logs, project files, or both after dry-run confirmation.

https://github.com/manganeseboy/codex-cleaner
```
