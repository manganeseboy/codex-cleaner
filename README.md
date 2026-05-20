# Codex Cleaner

Clean local Codex archive clutter without guessing which folder belongs to which conversation.

![Codex Cleaner demo](assets/demo.gif)

Current release: `v0.1.3` | Chinese README: [README.zh-CN.md](README.zh-CN.md)

Codex Cleaner is a local Codex Skill and Python cleanup tool. It scans archived Codex sessions, shows readable conversation titles, maps each archived conversation to its local workspace folder, then lets you choose exactly what to clean.

## Why This Exists

Codex can archive conversations, but archived local projects and generated files can still remain on your computer. After enough experiments, your `Documents/Codex` folder may contain many abandoned workspaces that are hard to identify safely.

Codex Cleaner helps answer:

> Which archived conversation created this local folder, and can I delete only the part I no longer need?

## Best For

- Codex Desktop users who archive many conversations.
- Non-technical users who want Codex to show a numbered cleanup menu.
- Developers who want a dry-run-first cleanup tool for local Codex workspaces.
- Users who need separate choices for deleting conversation logs, project files, or both.

## What It Can Clean

Codex Cleaner gives four clear choices:

1. Delete archived conversation only and keep project files.
2. Delete local project files only and keep the archived conversation.
3. Move both conversation logs and project files to `Codex_Trash`.
4. Permanently delete both, with an extra confirmation.

By default, cleanup is conservative. It previews first, moves content to `~/Documents/Codex_Trash`, and refuses project paths outside the configured Codex workspace root unless explicitly overridden.

## Install The Skill

Ask Codex to install the skill from GitHub:

```text
$skill-installer install https://github.com/manganeseboy/codex-cleaner/tree/main/skills/codex-cleaner
```

Restart Codex after installation so the new skill instructions are loaded.

## Use It Without Commands

After installing the skill, ask Codex:

```text
Use codex-cleaner to scan my archived conversations.
```

Codex should show a numbered list of archived conversations. Reply with one number, such as `2`, or several numbers, such as `2,3,5`.

Then Codex should show this menu:

```text
What should I clean?
1. Delete archived conversation only - keep project files
2. Delete local project files only - keep the archived conversation
3. Delete both conversation and project files - move to Codex_Trash
4. Permanently delete everything - cannot be restored
```

Codex will preview the exact local paths first. Cleanup only happens after confirmation. Option 4 is irreversible and requires an extra explicit confirmation.

## CLI Quick Start

The CLI is useful for technical users and tests. Python 3.10 or newer is recommended.

Scan archived sessions:

```powershell
python .\scripts\codex_cleaner.py scan
```

Show machine-readable JSON:

```powershell
python .\scripts\codex_cleaner.py scan --json
```

Preview deleting only the archived conversation/session log while keeping project files:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --conversation-only
```

Preview deleting only local project files while keeping the archived conversation:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --files-only
```

Preview moving both the archived conversation and workspace to `Codex_Trash`:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both
```

Apply a dry-run result:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both --yes
```

Permanently delete instead of moving to `Codex_Trash`:

```powershell
python .\scripts\codex_cleaner.py clean --index 3 --target both --permanent
python .\scripts\codex_cleaner.py clean --index 3 --target both --permanent --yes
```

## Search By Title

The scan table includes a readable `Title` column generated from the conversation's first real user request. English and Chinese conversation titles are both supported, including common file-upload preambles.

English title keyword:

```powershell
python .\scripts\codex_cleaner.py clean --title "certification agency" --target both
```

Chinese title keyword:

```powershell
python .\scripts\codex_cleaner.py clean --title "认证机构" --target both
```

## Update An Installed Skill

Installed users do not receive automatic push updates from GitHub. The skill is copied into the user's local Codex skills folder, so updating means replacing the old local copy with the latest GitHub version.

Tell users to ask Codex:

```text
I already installed codex-cleaner. Please remove the old local codex-cleaner skill and reinstall the latest version from:
https://github.com/manganeseboy/codex-cleaner/tree/main/skills/codex-cleaner
```

After updating, restart Codex. Users can watch the GitHub repository or follow the [Releases page](https://github.com/manganeseboy/codex-cleaner/releases) for new version reminders.

## Safety Model

- `clean` is a dry run unless `--yes` is provided.
- Default deletion moves files to `~/Documents/Codex_Trash`.
- Permanent deletion requires `--permanent --yes`.
- Workspace deletion is limited to `~/Documents/Codex` by default.
- The scan warns when multiple archived sessions point at the same workspace.
- This tool removes local archived session logs and local generated files only.
- It does not delete cloud-side ChatGPT or Codex conversation history.
- It cannot hook into Codex's UI archive button.

## Privacy

Codex Cleaner runs locally. It reads local Codex session logs and workspace metadata, and it does not send file contents or session data to any remote service.

## Community Sharing

Want to introduce Codex Cleaner to friends or communities? See:

- [Xiaohongshu promotion copy](docs/promotion/xiaohongshu.md)
- [Community posts](docs/promotion/community-posts.md)
- [Friend sharing guide](docs/promotion/share-with-friends.md)

## License

MIT
