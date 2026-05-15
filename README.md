# Codex Cleaner

Safely review and remove archived Codex sessions together with the local workspace outputs they created.

Codex Cleaner helps you answer a practical question:

> Which local files belong to this archived Codex conversation, and can I remove them safely?

The first version focuses on Windows Codex Desktop layouts, while keeping the core scanner portable Python.

## What it does

- Scans archived session logs under `~/.codex/archived_sessions`.
- Reads each session's recorded `cwd`.
- Checks whether the corresponding local workspace still exists.
- Reports file counts, directory counts, and approximate size.
- Deletes archived session logs, project folders, or both after explicit confirmation.
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

Show machine-readable JSON:

```powershell
python .\scripts\codex_cleaner.py scan --json
```

Preview deleting one archived session and its workspace:

```powershell
python .\scripts\codex_cleaner.py clean --session-id 019e25e9-0a03-7b61-bfda-64ad0fa25141 --target both
```

Actually move it to `Codex_Trash`:

```powershell
python .\scripts\codex_cleaner.py clean --session-id 019e25e9-0a03-7b61-bfda-64ad0fa25141 --target both --yes
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

## Safety model

Codex Cleaner is intentionally conservative:

- `clean` is a dry run unless `--yes` is provided.
- Default deletion moves files to `~/Documents/Codex_Trash`.
- Permanent deletion requires `--permanent --yes`.
- Workspace deletion is limited to `~/Documents/Codex` by default.
- The scan warns when multiple archived sessions point at the same workspace.

## Limitations

- This tool removes local archived session logs and local generated files.
- It does not delete cloud-side ChatGPT or Codex conversation history.
- It cannot hook into Codex's UI archive button.
- It depends on session logs containing a `session_meta.payload.cwd` value.

## Privacy

Codex Cleaner runs locally. It reads local Codex session logs and workspace metadata, and it does not send file contents or session data to any remote service.

## License

MIT
