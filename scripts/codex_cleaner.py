#!/usr/bin/env python3
"""Safely inspect and clean local Codex archived sessions and workspaces."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class SessionRecord:
    archive_file: str
    archive_path: str
    session_id: str
    title: str
    timestamp: str
    cwd: str
    project_exists: bool
    project_size_bytes: int
    project_file_count: int
    project_dir_count: int
    shared_project_count: int = 1


def default_home() -> Path:
    return Path.home()


def default_archive_dir() -> Path:
    return default_home() / ".codex" / "archived_sessions"


def default_codex_root() -> Path:
    return default_home() / "Documents" / "Codex"


def default_trash_dir() -> Path:
    return default_home() / "Documents" / "Codex_Trash"


def resolve_path(value: str | Path) -> Path:
    return Path(value).expanduser().resolve()


def is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def read_session_details(path: Path) -> tuple[dict | None, str]:
    meta: dict | None = None
    first_user_text = ""

    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                item = json.loads(line)
                if item.get("type") == "session_meta":
                    meta = item.get("payload") or {}
                    if first_user_text:
                        break
                    continue

                if not first_user_text:
                    first_user_text = extract_user_text(item)
                if meta and first_user_text:
                    break
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None, ""

    return meta, first_user_text


def extract_user_text(item: dict) -> str:
    payload = item.get("payload") or {}
    if payload.get("type") != "message" or payload.get("role") != "user":
        return ""

    parts: list[str] = []
    content = payload.get("content") or []
    if isinstance(content, str):
        return content if is_meaningful_user_text(content) else ""

    for part in content:
        if not isinstance(part, dict):
            continue
        if part.get("type") in ("input_text", "text"):
            text = part.get("text")
            if isinstance(text, str):
                parts.append(text)
    text = " ".join(parts)
    return text if is_meaningful_user_text(text) else ""


def is_meaningful_user_text(text: str) -> bool:
    normalized = text.strip()
    if not normalized:
        return False
    technical_prefixes = (
        "<environment_context>",
        "<image>",
    )
    return not normalized.startswith(technical_prefixes)


def make_title(meta: dict, first_user_text: str, cwd: str, session_id: str) -> str:
    explicit = meta.get("title") or meta.get("name") or meta.get("conversation_title")
    source = normalize_title_source(str(explicit or first_user_text or ""))
    source = " ".join(source.split())

    if not source and cwd:
        source = Path(cwd).name
    if not source:
        source = session_id[:8] or "Untitled session"

    return truncate(source, 64)


def normalize_title_source(text: str) -> str:
    text = text.strip()
    markers = (
        "## My request for Codex:",
        "## My request:",
        "My request for Codex:",
        "My request:",
        "## 我的请求：",
        "## 我的请求:",
        "我的请求：",
        "我的请求:",
        "## 给 Codex 的请求：",
        "## 给 Codex 的请求:",
        "给 Codex 的请求：",
        "给 Codex 的请求:",
        "## 给Codex的请求：",
        "## 给Codex的请求:",
        "给Codex的请求：",
        "给Codex的请求:",
        "## 我对 Codex 的请求：",
        "## 我对 Codex 的请求:",
        "我对 Codex 的请求：",
        "我对 Codex 的请求:",
    )
    for marker in markers:
        if marker in text:
            return text.split(marker, 1)[1].strip()
    return text


def truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def dir_stats(path: Path) -> tuple[int, int, int]:
    if not path.exists():
        return 0, 0, 0

    total_size = 0
    file_count = 0
    dir_count = 0

    for root, dirs, files in os.walk(path):
        dir_count += len(dirs)
        root_path = Path(root)
        for filename in files:
            file_count += 1
            try:
                total_size += (root_path / filename).stat().st_size
            except OSError:
                pass

    return total_size, file_count, dir_count


def scan_sessions(archive_dir: Path) -> list[SessionRecord]:
    records: list[SessionRecord] = []

    if not archive_dir.exists():
        return records

    for path in sorted(archive_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True):
        meta, first_user_text = read_session_details(path)
        if not meta:
            continue

        session_id = str(meta.get("id") or "")
        cwd = str(meta.get("cwd") or "")
        cwd_path = Path(cwd) if cwd else Path()
        exists = bool(cwd and cwd_path.exists())
        size, files, dirs = dir_stats(cwd_path) if exists else (0, 0, 0)

        records.append(
            SessionRecord(
                archive_file=path.name,
                archive_path=str(path),
                session_id=session_id,
                title=make_title(meta, first_user_text, cwd, session_id),
                timestamp=str(meta.get("timestamp") or ""),
                cwd=cwd,
                project_exists=exists,
                project_size_bytes=size,
                project_file_count=files,
                project_dir_count=dirs,
            )
        )

    cwd_counts: dict[str, int] = {}
    for record in records:
        if record.cwd:
            cwd_counts[record.cwd] = cwd_counts.get(record.cwd, 0) + 1
    for record in records:
        record.shared_project_count = cwd_counts.get(record.cwd, 1)

    return records


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{num_bytes} B"


def print_table(records: Iterable[SessionRecord]) -> None:
    rows = list(records)
    if not rows:
        print("No archived Codex sessions found.")
        return

    headers = ["#", "Title", "Session", "Exists", "Size", "Files", "Shared", "Workspace"]
    table: list[list[str]] = []
    for index, record in enumerate(rows, start=1):
        table.append(
            [
                str(index),
                truncate(record.title, 42),
                record.session_id[:8] if record.session_id else "(unknown)",
                "yes" if record.project_exists else "no",
                human_size(record.project_size_bytes),
                str(record.project_file_count),
                str(record.shared_project_count),
                record.cwd or "(none)",
            ]
        )

    widths = [len(header) for header in headers]
    for row in table:
        widths = [max(width, len(cell)) for width, cell in zip(widths, row)]

    fmt = "  ".join(f"{{:<{width}}}" for width in widths)
    print(fmt.format(*headers))
    print(fmt.format(*["-" * width for width in widths]))
    for row in table:
        print(fmt.format(*row))


def choose_record(
    records: list[SessionRecord],
    session_id: str | None,
    archive_file: str | None,
    index: int | None,
    title: str | None,
) -> SessionRecord | None:
    if index is not None:
        if index < 1 or index > len(records):
            raise SystemExit(f"Index {index} is out of range. Run scan to see available indexes.")
        return records[index - 1]
    if title:
        query = title.casefold()
        matches = [record for record in records if query in record.title.casefold()]
    elif session_id:
        matches = [record for record in records if record.session_id.startswith(session_id)]
    elif archive_file:
        matches = [record for record in records if record.archive_file == archive_file or record.archive_file.startswith(archive_file)]
    else:
        return None

    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        previews = ", ".join(f"{records.index(record) + 1}:{record.title}" for record in matches[:5])
        raise SystemExit(f"Ambiguous selector. Matched {len(matches)} sessions: {previews}. Use --index or a longer title.")
    return None


def unique_destination(trash_dir: Path, source: Path, label: str) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = source.name.replace(" ", "_") or "item"
    destination = trash_dir / f"{stamp}_{label}_{safe_name}"
    counter = 2
    while destination.exists():
        destination = trash_dir / f"{stamp}_{label}_{safe_name}_{counter}"
        counter += 1
    return destination


def remove_or_trash(path: Path, trash_dir: Path, permanent: bool, dry_run: bool, label: str) -> str:
    if not path.exists():
        return f"missing: {path}"

    if dry_run:
        action = "permanently delete" if permanent else "move to trash"
        return f"dry-run: would {action}: {path}"

    if permanent:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return f"deleted: {path}"

    trash_dir.mkdir(parents=True, exist_ok=True)
    destination = unique_destination(trash_dir, path, label)
    shutil.move(str(path), str(destination))
    return f"moved: {path} -> {destination}"


def clean(args: argparse.Namespace) -> int:
    archive_dir = resolve_path(args.archive_dir)
    codex_root = resolve_path(args.codex_root)
    trash_dir = resolve_path(args.trash_dir)
    records = scan_sessions(archive_dir)

    selected_archive: Path | None = None
    selected_project: Path | None = None

    if args.project:
        selected_project = resolve_path(args.project)
    else:
        record = choose_record(records, args.session_id, args.archive_file, args.index, args.title)
        if not record:
            print("No matching archived session found.", file=sys.stderr)
            return 2
        print(f"Selected: [{records.index(record) + 1}] {record.title}")
        selected_archive = resolve_path(record.archive_path)
        if record.cwd:
            selected_project = resolve_path(record.cwd)

    if args.target in ("archive", "both") and not selected_archive:
        print("No archive file selected.", file=sys.stderr)
        return 2

    if args.target in ("project", "both") and not selected_project:
        print("No project folder selected.", file=sys.stderr)
        return 2

    if selected_archive and not is_relative_to(selected_archive, archive_dir):
        print(f"Refusing archive outside archive dir: {selected_archive}", file=sys.stderr)
        return 3

    if selected_project and not args.allow_outside_codex_root and not is_relative_to(selected_project, codex_root):
        print(f"Refusing project outside Codex root: {selected_project}", file=sys.stderr)
        print(f"Codex root: {codex_root}", file=sys.stderr)
        return 3

    dry_run = not args.yes
    if dry_run:
        print("Dry run only. Re-run with --yes to apply.")

    actions: list[str] = []
    if args.target in ("project", "both") and selected_project:
        actions.append(remove_or_trash(selected_project, trash_dir, args.permanent, dry_run, "project"))
    if args.target in ("archive", "both") and selected_archive:
        actions.append(remove_or_trash(selected_archive, trash_dir, args.permanent, dry_run, "archive"))

    for action in actions:
        print(action)

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inspect and safely clean local Codex archived sessions and workspaces.")
    parser.add_argument("--archive-dir", default=str(default_archive_dir()), help="Archived sessions directory.")
    parser.add_argument("--codex-root", default=str(default_codex_root()), help="Allowed Codex workspace root.")
    parser.add_argument("--trash-dir", default=str(default_trash_dir()), help="Trash directory for non-permanent cleanups.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="List archived sessions and their workspaces.")
    scan_parser.add_argument("--json", action="store_true", help="Output JSON.")

    clean_parser = subparsers.add_parser("clean", help="Clean an archive file, project directory, or both.")
    selector = clean_parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--index", type=int, help="1-based row number from the scan table.")
    selector.add_argument("--title", help="Text contained in the conversation title.")
    selector.add_argument("--session-id", help="Session id prefix to clean.")
    selector.add_argument("--archive-file", help="Archived session file name or prefix to clean.")
    selector.add_argument("--project", help="Project directory to clean directly.")
    clean_parser.add_argument("--target", choices=("archive", "project", "both"), default="both", help="What to clean.")
    clean_parser.add_argument("--yes", action="store_true", help="Apply changes. Without this, clean is a dry run.")
    clean_parser.add_argument("--permanent", action="store_true", help="Permanently delete instead of moving to trash.")
    clean_parser.add_argument("--allow-outside-codex-root", action="store_true", help="Allow project cleanup outside --codex-root.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        records = scan_sessions(resolve_path(args.archive_dir))
        if args.json:
            print(json.dumps([asdict(record) for record in records], indent=2, ensure_ascii=False))
        else:
            print_table(records)
        return 0

    if args.command == "clean":
        return clean(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
