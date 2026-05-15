---
name: codex-cleaner
description: Safely scan and clean local Codex archived sessions and their generated workspace files. Use when the user wants to find, review, delete, trash, or clean archived Codex conversations, local Codex projects, or files produced by archived Codex sessions.
---

# Codex Cleaner

Use the bundled script for deterministic cleanup work. Do not manually delete files unless the script cannot handle the case.

## Workflow

1. Run a scan first:

```powershell
python scripts/codex_cleaner.py scan
```

2. Explain the matched archived sessions and workspace paths to the user.

3. Prefer cleanup by scan table index or title keyword for non-technical users:

```powershell
python scripts/codex_cleaner.py clean --index 3 --target both
```

```powershell
python scripts/codex_cleaner.py clean --title "title keyword" --target both
```

4. For cleanup by session id, do a dry run first:

```powershell
python scripts/codex_cleaner.py clean --session-id SESSION_PREFIX --target both
```

5. Apply only after the user confirms:

```powershell
python scripts/codex_cleaner.py clean --index 3 --target both --yes
```

6. If the user explicitly asks for permanent deletion, dry-run first, then apply with both `--permanent` and `--yes`:

```powershell
python scripts/codex_cleaner.py clean --index 3 --target both --permanent
python scripts/codex_cleaner.py clean --index 3 --target both --permanent --yes
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
