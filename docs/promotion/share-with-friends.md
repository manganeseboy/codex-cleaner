# Share With Friends

## One-Sentence Explanation

Codex Cleaner helps Codex users safely find and clean local project folders created by archived Codex conversations.

## Who Should Use It

Use it if your friend:

- Uses Codex Desktop.
- Has archived many Codex conversations.
- Has many old folders under `Documents/Codex`.
- Wants to clean files without guessing which folder belongs to which conversation.

## Beginner Install Script To Send

Tell your friend to open Codex and paste:

```text
$skill-installer install https://github.com/manganeseboy/codex-cleaner/tree/main/skills/codex-cleaner
```

Then tell them to restart Codex.

## Beginner Usage Script To Send

After restart, tell them to paste:

```text
Use codex-cleaner to scan my archived conversations.
```

If they prefer Chinese:

```text
使用 codex-cleaner 帮我扫描归档对话
```

Codex should show a numbered list. Your friend can reply with a number such as:

```text
2
```

Or multiple numbers:

```text
2,3,5
```

Then Codex should ask what to clean:

```text
1. Delete archived conversation only
2. Delete local project files only
3. Delete both and move to Codex_Trash
4. Permanently delete everything
```

Recommend option 3 for ordinary cleanup because it moves content to `Codex_Trash` instead of permanently deleting it.

## Safety Reminder

Codex Cleaner is local. It does not delete cloud-side ChatGPT or Codex history. It previews paths before cleaning, and permanent deletion requires extra confirmation.
