# Data Map

## Local Inputs

- `~/.codex/archived_sessions`: archived Codex session log files.
- `session_meta.payload.cwd`: workspace path recorded in archived session metadata.
- Local Codex workspaces, usually under `~/Documents/Codex`.

## Derived Fields

- `Title`: readable conversation title extracted from the first real user message.
- `Title` repair: common GBK/UTF-8 and Latin-1/UTF-8 mojibake is repaired before display.
- `Title` filtering: technical context such as environment blocks and `AGENTS.md` instructions is skipped.
- `Workspace`: local project path associated with the archived session.
- `Size`: approximate workspace size.
- `File count`: number of files under the workspace.
- `Directory count`: number of directories under the workspace.
- Duplicate workspace warnings when multiple archived sessions point to the same local project path.

## Cleanup Targets

- Archived conversation logs only.
- Local project files only.
- Both archived logs and local project files.
- Permanent deletion variants when explicitly requested.

## Default Output Location

- `~/Documents/Codex_Trash`: default destination for non-permanent cleanup.

## Safety Boundaries

- Dry-run by default.
- `--yes` required for execution.
- `--permanent --yes` required for irreversible deletion.
- Project deletion is restricted to the configured Codex workspace root unless explicitly overridden.

## Privacy

The tool runs locally and does not send local session logs, project paths, file contents, or cleanup metadata to a remote service.
