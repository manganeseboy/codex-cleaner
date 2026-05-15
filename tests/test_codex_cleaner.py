import json
import tempfile
import unittest
from pathlib import Path

from scripts.codex_cleaner import scan_sessions


def write_session(path: Path, session_id: str, cwd: Path) -> None:
    payload = {
        "timestamp": "2026-05-15T00:00:00Z",
        "type": "session_meta",
        "payload": {
            "id": session_id,
            "timestamp": "2026-05-15T00:00:00Z",
            "cwd": str(cwd),
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


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


if __name__ == "__main__":
    unittest.main()
