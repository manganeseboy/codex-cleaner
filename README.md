# Codex Cleaner

Safely review and remove archived Codex sessions together with the local workspace outputs they created.

![Codex Cleaner demo](assets/demo.gif)

Current release: `v0.1.0`

Codex Cleaner helps you answer a practical question:

> Which local files belong to this archived Codex conversation, and can I remove them safely?

The first version focuses on Windows Codex Desktop layouts, while keeping the core scanner portable Python.

## What it does

- Scans archived session logs under `~/.codex/archived_sessions`.
- Reads each session's recorded `cwd`.
- Checks whether the corresponding local workspace still exists.
- Reports file counts, directory counts, and approximate size.
- Deletes archived session logs, project folders, or both after explicit confirmation.
- Supports conversation-only cleanup when you want to keep project files.
- Supports files-only cleanup when you want to keep the archived conversation record.
- Moves deleted content into `~/Documents/Codex_Trash` by default instead of permanent deletion.
- Refuses to delete project paths outside the configured Codex workspace root unless explicitly overridden.

## Install

No package install is required for the basic CLI. Use Python 3.10 or newer.

```powershell
python .\scripts\codex_cleaner.py scan
```

## Common commands

Scan archived sessions:

```powershell
python .\scripts\codex_cleaner.py scan
```

The scan table includes a readable `Title` column generated from the conversation's first real user request. English and Chinese conversation titles are both supported, including common file-upload preambles.

Show machine-readable JSON:

```powershell
python .\scripts\codex_cleaner.py scan --json
```

Preview deleting one archived session and its workspace by row number:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both
```

Preview deleting only the archived conversation/session log while keeping project files:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --conversation-only
```

Apply conversation-only cleanup:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --conversation-only --yes
```

Preview deleting only local project files while keeping the archived conversation:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --files-only
```

Apply files-only cleanup:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --files-only --yes
```

Preview deleting by title keyword:

```powershell
python .\scripts\codex_cleaner.py clean --title "certification agency" --target both
```

Chinese title keywords work the same way:

```powershell
python .\scripts\codex_cleaner.py clean --title "认证机构" --target both
```

Preview deleting by session id:

```powershell
python .\scripts\codex_cleaner.py clean --session-id 019e25e9-0a03-7b61-bfda-64ad0fa25141 --target both
```

Actually move it to `Codex_Trash`:

```powershell
python .\scripts\codex_cleaner.py clean --session-id 019e25e9-0a03-7b61-bfda-64ad0fa25141 --target both --yes
```

Permanently delete instead of moving to `Codex_Trash`:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both --permanent
python .\scripts\codex_cleaner.py clean --index 3 --target both --permanent --yes
```

For non-technical users, the safest flow is:

```powershell
python .\scripts\codex_cleaner.py scan
python .\scripts\codex_cleaner.py clean --index 3 --target both
python .\scripts\codex_cleaner.py clean --index 3 --target both --yes
```

Clean multiple numbered rows:

```powershell
python .\scripts\codex_cleaner.py clean --indexes 2,3,5 --target both
python .\scripts\codex_cleaner.py clean --indexes 2,3,5 --target both --yes
```

Delete only a specific project folder:

```powershell
python .\scripts\codex_cleaner.py clean --project "C:\Users\you\Documents\Codex\2026-05-14\windows" --target project --yes
```

## Codex Skill

The repo includes a Codex skill at:

`skills/codex-cleaner`

After the repo is published, users can install it from Codex with:

```text
$skill-installer install https://github.com/manganeseboy/codex-cleaner/tree/main/skills/codex-cleaner
```

After installing the skill, non-technical users can simply ask Codex:

```text
Use codex-cleaner to scan my archived conversations.
```

Codex should show a numbered list, then the user can reply with `2` or `2,3,5`. The skill tells Codex to dry-run first and ask for confirmation before cleaning.

## Safety model

Codex Cleaner is intentionally conservative:

- `clean` is a dry run unless `--yes` is provided.
- Default deletion moves files to `~/Documents/Codex_Trash`.
- Permanent deletion requires `--permanent --yes`.
- Permanent deletion prints a warning and does not create a trash backup.
- Workspace deletion is limited to `~/Documents/Codex` by default.
- The scan warns when multiple archived sessions point at the same workspace.
- Users can clean by table row number, title keyword, session id, archive file, or direct project path.
- Multiple rows can be cleaned with `--indexes`, for example `--indexes 2,3,5`.
- Use `--conversation-only` to delete only archived local conversation logs and keep project files.
- Use `--files-only` to delete only local project files and keep archived conversation logs.

## Limitations

- This tool removes local archived session logs and local generated files.
- It does not delete cloud-side ChatGPT or Codex conversation history.
- It cannot hook into Codex's UI archive button.
- It depends on session logs containing a `session_meta.payload.cwd` value.

## Privacy

Codex Cleaner runs locally. It reads local Codex session logs and workspace metadata, and it does not send file contents or session data to any remote service.

## License

MIT
