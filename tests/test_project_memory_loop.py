from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.project_memory_loop import dispatch_hook, find_project_root, retrieve


class ProjectMemoryLoopTests(unittest.TestCase):
    def make_repository(self, directory: str) -> Path:
        root = Path(directory)
        (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
        memory = root / "docs/project-memory"
        (memory / "practices").mkdir(parents=True)
        (memory / "INDEX.md").write_text("# Project memory\n", encoding="utf-8")
        (memory / "PROJECT-CONTEXT.md").write_text("# Context\nRAN Online server.\n", encoding="utf-8")
        (memory / "DOS-AND-DONTS.md").write_text("# Rules\nDo verify changes.\n", encoding="utf-8")
        (memory / "practices/SECURITY.md").write_text(
            "# Security practices\nValidate authorization on the server.\n", encoding="utf-8"
        )
        learner = root / ".agents/skills/project-memory-learner/SKILL.md"
        learner.parent.mkdir(parents=True)
        learner.write_text("# Project Memory Learner\n", encoding="utf-8")
        return root

    def test_finds_project_root_from_nested_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            nested = root / "src/deep"
            nested.mkdir(parents=True)
            self.assertEqual(root.resolve(), find_project_root(nested))

    def test_retrieval_prefers_relevant_practice(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            matches = retrieve(root, "How should server authorization be validated?")
            self.assertEqual("docs/project-memory/practices/SECURITY.md", matches[0].path)

    def test_stop_requests_exactly_one_learning_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            first, status = dispatch_hook(
                {"hook_event_name": "Stop", "cwd": str(root), "stop_hook_active": False}
            )
            second, second_status = dispatch_hook(
                {"hook_event_name": "Stop", "cwd": str(root), "stop_hook_active": True}
            )
            self.assertEqual(0, status)
            self.assertEqual("block", first["decision"])
            self.assertEqual(0, second_status)
            self.assertEqual({"continue": True}, second)

    def test_prompt_hook_injects_paths_without_persisting_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_repository(directory)
            output, status = dispatch_hook(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "cwd": str(root),
                    "prompt": "Please review authorization security",
                }
            )
            context = output["hookSpecificOutput"]["additionalContext"]
            self.assertEqual(0, status)
            self.assertIn("practices/SECURITY.md", context)
            self.assertNotIn("Please review authorization security", context)


if __name__ == "__main__":
    unittest.main()
