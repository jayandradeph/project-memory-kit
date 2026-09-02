from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.install import install_into


class InstallerTests(unittest.TestCase):
    @property
    def kit_root(self) -> Path:
        return Path(__file__).resolve().parents[1]

    def test_installs_without_copying_template_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = install_into(self.kit_root, target, "Example Project")

            self.assertIn(Path("AGENTS.md"), result.copied)
            self.assertTrue((target / "tools/memory_check.py").is_file())
            self.assertFalse((target / ".project-memory-template").exists())
            context = (target / "docs/project-memory/PROJECT-CONTEXT.md").read_text(encoding="utf-8")
            self.assertIn("Example Project", context)
            self.assertNotIn("[PROJECT NAME]", context)

    def test_preserves_existing_agents_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            existing = "# Existing project rules\n"
            (target / "AGENTS.md").write_text(existing, encoding="utf-8")

            result = install_into(self.kit_root, target, "Example Project")

            self.assertIn(Path("AGENTS.md"), result.skipped)
            self.assertEqual(existing, (target / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertTrue((target / "docs/integration/AGENTS-snippet.md").is_file())

    def test_dry_run_does_not_write(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            result = install_into(self.kit_root, target, "Example Project", dry_run=True)
            self.assertTrue(result.copied)
            self.assertEqual([], list(target.iterdir()))

    def test_does_not_follow_destination_symlink_outside_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside_directory:
            target = Path(directory)
            outside = Path(outside_directory)
            try:
                (target / "docs").symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("directory symlinks are not available on this platform")

            with self.assertRaises(OSError):
                install_into(self.kit_root, target, "Example Project")


if __name__ == "__main__":
    unittest.main()
