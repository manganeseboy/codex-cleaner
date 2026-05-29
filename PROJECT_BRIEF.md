# Project Brief

## Product

Codex Cleaner is a local Codex Skill and Python cleanup tool for reviewing archived Codex sessions and the local project folders those sessions created.

## Problem

Codex users can archive conversations, but local generated project folders may remain under `Documents/Codex`. After many experiments, users may not know which archived conversation maps to which local workspace, or whether it is safe to delete only the conversation record, only the project files, or both.

## Target Users

- Codex Desktop users with many archived conversations.
- Non-technical users who prefer a numbered menu inside Codex.
- Developers who want a conservative dry-run cleanup workflow.
- Users who need bilingual Chinese and English conversation title support.

## Current Scope

- Scan local archived session logs under `~/.codex/archived_sessions`.
- Read `session_meta.payload.cwd` to map archived conversations to local workspaces.
- Show readable conversation titles generated from the first real user message.
- Repair common GBK/UTF-8 or Latin-1/UTF-8 mojibake in conversation titles.
- Skip technical context blocks such as environment context and `AGENTS.md` instructions when choosing a title.
- Support cleanup by index, title, session id, archive file, or project path.
- Support conversation-only, files-only, trash-based both, and permanent both cleanup modes.
- Prefer dry-run and explicit confirmation before deletion.

## Out Of Scope

- Deleting cloud-side ChatGPT or Codex history.
- Hooking into Codex's native archive button.
- Adding telemetry, analytics, or remote network calls.
- Automatic background cleanup without user confirmation.

## Distribution Goal

Make the tool understandable from the GitHub first screen, easy to install as a Codex Skill, and easy to share through Chinese and English community posts.
