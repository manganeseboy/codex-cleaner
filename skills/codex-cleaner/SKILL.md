---
name: codex-cleaner
description: Safely scan and clean local Codex archived sessions and their generated workspace files. Use when the user wants to find, review, delete, trash, or clean archived Codex conversations, local Codex projects, or files produced by archived Codex sessions.
---

# Codex Cleaner

Use the bundled script for deterministic cleanup work. Do not manually delete files unless the script cannot handle the case.

This skill should feel like a simple cleanup assistant. Do not ask non-technical users to type commands. Run the commands yourself, present numbered choices, and let the user reply with numbers such as `2` or `2,3,5`.

## Language Behavior

Mirror the user's language.

- If the user writes in Chinese, respond in Chinese.
- If the user writes in English, respond in English.
- If the user mixes languages, use the dominant language and preserve conversation titles as-is.
- Do not force Chinese labels for English users or English labels for Chinese users.
- Commands, paths, and flags remain unchanged because they are CLI syntax.

## Script Location

The CLI script is bundled at `scripts/codex_cleaner.py` relative to this `SKILL.md`. When running commands, resolve that script relative to the installed skill folder. If the current working directory is not the skill folder, use the script's absolute path.

## Conversational Workflow

1. Run a JSON scan first so you can parse titles and sizes reliably:

```powershell
python scripts/codex_cleaner.py scan --json
```

2. Summarize the scan as a numbered list. Show only the user-friendly fields by default:

English example:

```text
1. Conversation title
   Size: 242.2 MB
   Workspace: C:\Users\...\Documents\Codex\...
```

Chinese example:

```text
1. 对话名称
   大小：242.2 MB
   项目目录：C:\Users\...\Documents\Codex\...
```

3. Ask the user to reply with the number or numbers to clean. Accept formats like:

```text
2
2,3,5
```

4. Ask what to clean unless the user already said it:

English:

```text
What should I clean?
1. Conversation only - keep project files
2. Project files only - keep the conversation
3. Conversation and project files
```

Chinese:

```text
你想清理哪一部分？
1. 只删除会话记录，保留项目文件
2. 只删除项目文件，保留会话记录
3. 会话记录和项目文件都清理
```

Use mode mapping:

- conversation only -> `--conversation-only`
- project/files only -> `--files-only`
- conversation and project files -> default `--target both`

5. Convert the user's reply into `--index` or `--indexes`. Always dry-run first:

```powershell
python scripts/codex_cleaner.py clean --index 2 --conversation-only
python scripts/codex_cleaner.py clean --indexes 2,3,5 --files-only
python scripts/codex_cleaner.py clean --indexes 2,3,5 --target both
```

6. Explain the exact local paths that would be moved or deleted. Ask for confirmation in plain language. If using conversation-only mode, explicitly say project files will be kept.

English confirmation wording:

```text
I will move these local files to Codex_Trash. This will not delete cloud-side ChatGPT/Codex history. Reply "confirm" to continue.
```

Chinese confirmation wording:

```text
我会把这些本地文件移动到 Codex_Trash，不会删除云端 ChatGPT/Codex 历史。回复“确认”后继续。
```

7. Apply only after the user confirms:

```powershell
python scripts/codex_cleaner.py clean --index 2 --conversation-only --yes
python scripts/codex_cleaner.py clean --indexes 2,3,5 --files-only --yes
python scripts/codex_cleaner.py clean --indexes 2,3,5 --target both --yes
```

8. If the user explicitly asks for permanent deletion, dry-run first, then apply with both `--permanent` and `--yes`:

```powershell
python scripts/codex_cleaner.py clean --index 2 --conversation-only --permanent
python scripts/codex_cleaner.py clean --index 2 --conversation-only --permanent --yes
```

## Advanced Selectors

```powershell
python scripts/codex_cleaner.py clean --index 3 --target both
```

```powershell
python scripts/codex_cleaner.py clean --title "title keyword" --target both
```

Conversation-only cleanup:

```powershell
python scripts/codex_cleaner.py clean --index 3 --conversation-only --yes
```

Files-only cleanup:

```powershell
python scripts/codex_cleaner.py clean --index 3 --files-only --yes
```

For cleanup by session id:

```powershell
python scripts/codex_cleaner.py clean --session-id SESSION_PREFIX --target both
```

## Safety Rules

- Prefer moving content to `~/Documents/Codex_Trash`.
- Use `--permanent` only when the user explicitly asks for permanent deletion.
- Permanent deletion requires `--permanent --yes` and does not create a trash backup.
- Keep cleanup limited to `~/Documents/Codex` unless the user explicitly confirms an outside path.
- Warn when multiple archived sessions point at the same workspace.
- Make clear that this removes local logs and files only. It does not delete cloud-side ChatGPT or Codex history.
- Use the readable Title column when explaining options to the user.
- English and Chinese title keywords are both supported. Prefer the user's own language when suggesting `--title`.
- For ordinary users, prefer row numbers over session IDs, archive filenames, or paths.
- For English users, say "move to Codex_Trash" and "permanently delete".
- For Chinese users, say "移动到 Codex_Trash" and "永久删除".
- If the user says "delete/clear conversation only", "keep project files", "只删除会话", "清空会话", or "保留项目文件", use `--conversation-only`.
- If the user says "delete generated files only", "keep conversation", "只删除项目文件", or "保留会话记录", use `--files-only`.

## Useful Commands

Scan as JSON:

```powershell
python scripts/codex_cleaner.py scan --json
```

Clean only the archived session log:

```powershell
python scripts/codex_cleaner.py clean --session-id SESSION_PREFIX --target archive --yes
```

Clean only the local workspace:

```powershell
python scripts/codex_cleaner.py clean --session-id SESSION_PREFIX --target project --yes
```

Clean a direct project path:

```powershell
python scripts/codex_cleaner.py clean --project "C:\Users\you\Documents\Codex\2026-05-14\windows" --target project --yes
```
