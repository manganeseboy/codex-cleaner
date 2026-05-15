from pathlib import Path
import unittest


class SkillBundleTest(unittest.TestCase):
    def test_skill_bundles_current_cli_script(self) -> None:
        root = Path(__file__).resolve().parents[1]
        root_script = root / "scripts" / "codex_cleaner.py"
        skill_script = root / "skills" / "codex-cleaner" / "scripts" / "codex_cleaner.py"

        self.assertTrue(skill_script.exists())
        self.assertEqual(root_script.read_text(encoding="utf-8"), skill_script.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
