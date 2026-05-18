import json
import tempfile
import unittest
from pathlib import Path

from scripts.codex_cleaner import main, scan_sessions


def write_session(
    path: Path,
    session_id: str,
    cwd: Path,
    user_text: str = "Clean old Codex project",
    include_environment_context: bool = False,
) -> None:
    meta = {
        "timestamp": "2026-05-15T00:00:00Z",
        "type": "session_meta",
        "payload": {
            "id": session_id,
            "timestamp": "2026-05-15T00:00:00Z",
            "cwd": str(cwd),
        },
    }
    user_message = {
        "timestamp": "2026-05-15T00:00:01Z",
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": "user",
            "content": [{"type": "input_text", "text": user_text}],
        },
    }
    lines = [json.dumps(meta)]
    if include_environment_context:
        environment_message = {
            "timestamp": "2026-05-15T00:00:00Z",
            "type": "response_item",
            "payload": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "<environment_context>\n  <cwd>C:\\demo</cwd>\n</environment_context>"}],
            },
        }
        lines.append(json.dumps(environment_message))
    lines.append(json.dumps(user_message))
    path.write_text("\n".join(lines), encoding="utf-8")


class ScanSessionsTest(unittest.TestCase):
    def test_scan_sessions_reads_cwd_and_stats(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / "archived_sessions"
            archive_dir.mkdir()
            project = tmp_path / "Documents" / "Codex" / "2026-05-15" / "demo"
            project.mkdir(parents=True)
            (project / "hello.txt").write_text("hello", encoding="utf-8")

            write_session(archive_dir / "rollout-demo.jsonl", "abc123", project)

            records = scan_sessions(archive_dir)

            self.assertEqual(len(records), 1)
            self.assertEqual(records[0].session_id, "abc123")
            self.assertEqual(records[0].title, "Clean old Codex project")
            self.assertEqual(records[0].cwd, str(project))
            self.assertTrue(records[0].project_exists)
            self.assertEqual(records[0].project_file_count, 1)
            self.assertEqual(records[0].project_size_bytes, 5)

    def test_scan_sessions_marks_shared_projects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / "archived_sessions"
            archive_dir.mkdir()
            project = tmp_path / "Documents" / "Codex" / "shared"
            project.mkdir(parents=True)

            write_session(archive_dir / "one.jsonl", "one", project)
            write_session(archive_dir / "two.jsonl", "two", project)

            records = scan_sessions(archive_dir)

            self.assertEqual({record.shared_project_count for record in records}, {2})

    def test_scan_sessions_falls_back_to_project_name_for_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / "archived_sessions"
            archive_dir.mkdir()
            project = tmp_path / "Documents" / "Codex" / "fallback-name"
            project.mkdir(parents=True)

            payload = {
                "timestamp": "2026-05-15T00:00:00Z",
                "type": "session_meta",
                "payload": {"id": "fallback", "timestamp": "2026-05-15T00:00:00Z", "cwd": str(project)},
            }
            (archive_dir / "fallback.jsonl").write_text(json.dumps(payload), encoding="utf-8")

            records = scan_sessions(archive_dir)

            self.assertEqual(records[0].title, "fallback-name")

    def test_scan_sessions_skips_environment_context_for_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / "archived_sessions"
            archive_dir.mkdir()
            project = tmp_path / "Documents" / "Codex" / "demo"
            project.mkdir(parents=True)

            write_session(
                archive_dir / "rollout-demo.jsonl",
                "abc123",
                project,
                user_text="Build a cleanup tool for Codex",
                include_environment_context=True,
            )

            records = scan_sessions(archive_dir)

            self.assertEqual(records[0].title, "Build a cleanup tool for Codex")

    def test_scan_sessions_uses_request_after_files_preamble_for_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / "archived_sessions"
            archive_dir.mkdir()
            project = tmp_path / "Documents" / "Codex" / "demo"
            project.mkdir(parents=True)

            write_session(
                archive_dir / "rollout-demo.jsonl",
                "abc123",
                project,
                user_text="# Files mentioned by the user:\n\n## Report: C:/demo/report.xlsx\n\n## My request for Codex:\nSummarize this report",
            )

            records = scan_sessions(archive_dir)

            self.assertEqual(records[0].title, "Summarize this report")

    def test_scan_sessions_supports_english_title_keyword(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / "archived_sessions"
            archive_dir.mkdir()
            project = tmp_path / "Documents" / "Codex" / "demo"
            project.mkdir(parents=True)

            write_session(
                archive_dir / "rollout-demo.jsonl",
                "abc123",
                project,
                user_text="Create a Windows app for image-based product analysis",
            )

            records = scan_sessions(archive_dir)

            self.assertEqual(records[0].title, "Create a Windows app for image-based product analysis")

    def test_scan_sessions_supports_chinese_request_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / "archived_sessions"
            archive_dir.mkdir()
            project = tmp_path / "Documents" / "Codex" / "demo"
            project.mkdir(parents=True)

            write_session(
                archive_dir / "rollout-demo.jsonl",
                "abc123",
                project,
                user_text="# 用户提到的文件：\n\n## 表格: C:/demo/report.xlsx\n\n## 我的请求：\n汇总这个表格",
            )

            records = scan_sessions(archive_dir)

            self.assertEqual(records[0].title, "汇总这个表格")


class CleanSessionsTest(unittest.TestCase):
    def test_permanent_clean_deletes_archive_and_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / ".codex" / "archived_sessions"
            archive_dir.mkdir(parents=True)
            codex_root = tmp_path / "Documents" / "Codex"
            project = codex_root / "2026-05-15" / "demo"
            project.mkdir(parents=True)
            (project / "hello.txt").write_text("hello", encoding="utf-8")
            archive_file = archive_dir / "rollout-demo.jsonl"
            write_session(archive_file, "abc123", project)
            trash_dir = tmp_path / "Documents" / "Codex_Trash"

            exit_code = main(
                [
                    "--archive-dir",
                    str(archive_dir),
                    "--codex-root",
                    str(codex_root),
                    "--trash-dir",
                    str(trash_dir),
                    "clean",
                    "--index",
                    "1",
                    "--target",
                    "both",
                    "--yes",
                    "--permanent",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertFalse(project.exists())
            self.assertFalse(archive_file.exists())
            self.assertFalse(trash_dir.exists())

    def test_permanent_clean_without_yes_is_dry_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / ".codex" / "archived_sessions"
            archive_dir.mkdir(parents=True)
            codex_root = tmp_path / "Documents" / "Codex"
            project = codex_root / "2026-05-15" / "demo"
            project.mkdir(parents=True)
            (project / "hello.txt").write_text("hello", encoding="utf-8")
            archive_file = archive_dir / "rollout-demo.jsonl"
            write_session(archive_file, "abc123", project)

            exit_code = main(
                [
                    "--archive-dir",
                    str(archive_dir),
                    "--codex-root",
                    str(codex_root),
                    "clean",
                    "--index",
                    "1",
                    "--target",
                    "both",
                    "--permanent",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(project.exists())
            self.assertTrue(archive_file.exists())

    def test_clean_supports_multiple_indexes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / ".codex" / "archived_sessions"
            archive_dir.mkdir(parents=True)
            codex_root = tmp_path / "Documents" / "Codex"

            project_one = codex_root / "one"
            project_two = codex_root / "two"
            project_one.mkdir(parents=True)
            project_two.mkdir(parents=True)
            archive_one = archive_dir / "one.jsonl"
            archive_two = archive_dir / "two.jsonl"
            write_session(archive_one, "one", project_one, user_text="First cleanup")
            write_session(archive_two, "two", project_two, user_text="Second cleanup")

            exit_code = main(
                [
                    "--archive-dir",
                    str(archive_dir),
                    "--codex-root",
                    str(codex_root),
                    "clean",
                    "--indexes",
                    "1,2",
                    "--target",
                    "archive",
                    "--yes",
                    "--permanent",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertFalse(archive_one.exists())
            self.assertFalse(archive_two.exists())
            self.assertTrue(project_one.exists())
            self.assertTrue(project_two.exists())

    def test_clean_multiple_indexes_deduplicates_shared_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / ".codex" / "archived_sessions"
            archive_dir.mkdir(parents=True)
            codex_root = tmp_path / "Documents" / "Codex"
            project = codex_root / "shared"
            project.mkdir(parents=True)
            (project / "hello.txt").write_text("hello", encoding="utf-8")

            write_session(archive_dir / "one.jsonl", "one", project, user_text="First cleanup")
            write_session(archive_dir / "two.jsonl", "two", project, user_text="Second cleanup")
            trash_dir = tmp_path / "Documents" / "Codex_Trash"

            exit_code = main(
                [
                    "--archive-dir",
                    str(archive_dir),
                    "--codex-root",
                    str(codex_root),
                    "--trash-dir",
                    str(trash_dir),
                    "clean",
                    "--indexes",
                    "1,2",
                    "--target",
                    "both",
                    "--yes",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertFalse(project.exists())
            self.assertTrue(trash_dir.exists())
            self.assertEqual(len(list(trash_dir.glob("*_project_shared*"))), 1)
            self.assertEqual(len(list(trash_dir.glob("*_archive_*.jsonl"))), 2)

    def test_conversation_only_keeps_project_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / ".codex" / "archived_sessions"
            archive_dir.mkdir(parents=True)
            codex_root = tmp_path / "Documents" / "Codex"
            project = codex_root / "2026-05-15" / "demo"
            project.mkdir(parents=True)
            (project / "hello.txt").write_text("hello", encoding="utf-8")
            archive_file = archive_dir / "rollout-demo.jsonl"
            write_session(archive_file, "abc123", project)
            trash_dir = tmp_path / "Documents" / "Codex_Trash"

            exit_code = main(
                [
                    "--archive-dir",
                    str(archive_dir),
                    "--codex-root",
                    str(codex_root),
                    "--trash-dir",
                    str(trash_dir),
                    "clean",
                    "--index",
                    "1",
                    "--conversation-only",
                    "--yes",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(project.exists())
            self.assertTrue((project / "hello.txt").exists())
            self.assertFalse(archive_file.exists())
            self.assertEqual(len(list(trash_dir.glob("*_archive_*.jsonl"))), 1)
            self.assertEqual(len(list(trash_dir.glob("*_project_*"))), 0)

    def test_files_only_keeps_archived_conversation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            archive_dir = tmp_path / ".codex" / "archived_sessions"
            archive_dir.mkdir(parents=True)
            codex_root = tmp_path / "Documents" / "Codex"
            project = codex_root / "2026-05-15" / "demo"
            project.mkdir(parents=True)
            (project / "hello.txt").write_text("hello", encoding="utf-8")
            archive_file = archive_dir / "rollout-demo.jsonl"
            write_session(archive_file, "abc123", project)
            trash_dir = tmp_path / "Documents" / "Codex_Trash"

            exit_code = main(
                [
                    "--archive-dir",
                    str(archive_dir),
                    "--codex-root",
                    str(codex_root),
                    "--trash-dir",
                    str(trash_dir),
                    "clean",
                    "--index",
                    "1",
                    "--files-only",
                    "--yes",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertFalse(project.exists())
            self.assertTrue(archive_file.exists())
            self.assertEqual(len(list(trash_dir.glob("*_project_demo*"))), 1)
            self.assertEqual(len(list(trash_dir.glob("*_archive_*.jsonl"))), 0)


if __name__ == "__main__":
    unittest.main()
