from __future__ import annotations

import tempfile
import unittest
import json
from pathlib import Path

from tools.memory_check import REQUIRED_PATHS, validate_repository


VALID_FRONT_MATTER = """---
status: accepted
last_verified: 2026-09-02
applies_to: test
owner: tests
---

# Test document
"""


class MemoryCheckTests(unittest.TestCase):
    def make_repository(self, directory: str) -> Path:
        root = Path(directory)
        for relative in REQUIRED_PATHS:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if relative == "AGENTS.md":
                path.write_text("Read docs/project-memory/INDEX.md before meaningful work.\n", encoding="utf-8")
            elif path.name == "INDEX.md" or relative == "README.md":
                path.write_text("# Index\n", encoding="utf-8")
            elif relative == ".codex/hooks.json":
                hooks = {
                    "hooks": {
                        event: [{"hooks": [{
                            "type": "command",
                            "command": "python3 tools/project_memory_loop.py hook",
                            "commandWindows": "python tools/project_memory_loop.py hook",
                            "timeout": 3,
                        }]}]
                        for event in ("SessionStart", "UserPromptSubmit", "Stop", "SessionEnd")
                    }
                }
                path.write_text(json.dumps(hooks), encoding="utf-8")
            elif relative == ".agents/skills/project-memory-learner/SKILL.md":
                path.write_text(
                    "---\nname: project-memory-learner\ndescription: Test learner.\n---\n\n# Learner\n",
                    encoding="utf-8",
                )
            elif relative == "tools/project_memory_loop.py":
                path.write_text("# test fixture\n", encoding="utf-8")
            else:
                path.write_text(VALID_FRONT_MATTER, encoding="utf-8")
        (root / ".project-memory-template").write_text("test", encoding="utf-8")
        return root

    def test_valid_minimal_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = validate_repository(self.make_repository(directory))
            self.assertEqual([], result.errors)

    def test_missing_required_file_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            (root / "AGENTS.md").unlink()
            result = validate_repository(root)
            self.assertTrue(any("missing required file: AGENTS.md" in item for item in result.errors))

    def test_invalid_status_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            path = root / "docs/project-memory/practices/UI.md"
            path.write_text(VALID_FRONT_MATTER.replace("status: accepted", "status: maybe"), encoding="utf-8")
            result = validate_repository(root)
            self.assertTrue(any("unsupported status" in item for item in result.errors))

    def test_agents_file_must_route_to_memory_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            (root / "AGENTS.md").write_text("# Existing rules only\n", encoding="utf-8")
            result = validate_repository(root)
            self.assertTrue(any("must direct agents" in item for item in result.errors))

    def test_hooks_require_all_learning_loop_events(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            hooks_path = root / ".codex/hooks.json"
            payload = json.loads(hooks_path.read_text(encoding="utf-8"))
            del payload["hooks"]["Stop"]
            hooks_path.write_text(json.dumps(payload), encoding="utf-8")
            result = validate_repository(root)
            self.assertTrue(any("missing hook events: Stop" in item for item in result.errors))

    def test_project_skill_name_must_match_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            skill = root / ".agents/skills/project-memory-learner/SKILL.md"
            skill.write_text(
                skill.read_text(encoding="utf-8").replace(
                    "name: project-memory-learner", "name: another-name"
                ),
                encoding="utf-8",
            )
            result = validate_repository(root)
            self.assertTrue(any("must match directory" in item for item in result.errors))

    def test_broken_relative_link_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            (root / "README.md").write_text("[missing](docs/missing.md)\n", encoding="utf-8")
            result = validate_repository(root)
            self.assertTrue(any("broken local link" in item for item in result.errors))

    def test_likely_secret_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            token = "AKIA" + "A" * 16
            (root / "README.md").write_text(f"Accidental value: {token}\n", encoding="utf-8")
            result = validate_repository(root)
            self.assertTrue(any("possible AWS access key" in item for item in result.errors))

    def test_unresolved_context_placeholder_is_a_warning_outside_template(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            (root / ".project-memory-template").unlink()
            context = root / "docs/project-memory/PROJECT-CONTEXT.md"
            context.write_text(VALID_FRONT_MATTER + "\nProject: `[PROJECT NAME]`\n", encoding="utf-8")
            result = validate_repository(root)
            self.assertTrue(any("unresolved template token" in item for item in result.warnings))


if __name__ == "__main__":
    unittest.main()
