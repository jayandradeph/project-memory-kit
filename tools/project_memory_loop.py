#!/usr/bin/env python3
"""Project-scoped recall and reflection hooks for Codex.

The script deliberately does not persist prompts or read raw transcripts. Durable
learning is curated by the agent through the project-memory-learner skill, while
this deterministic layer handles retrieval, loop triggering, and validation.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/+-]*")
HEADING_RE = re.compile(r"^#{1,3}\s+(.+?)\s*$", re.MULTILINE)
STOPWORDS = {
    "about", "after", "again", "also", "and", "are", "been", "before",
    "but", "can", "could", "does", "for", "from", "have", "how", "into",
    "its", "just", "like", "more", "not", "only", "our", "should", "that",
    "the", "their", "then", "there", "these", "they", "this", "those",
    "use", "using", "want", "was", "were", "what", "when", "where", "which",
    "will", "with", "would", "you", "your",
}
EXCLUDED_MEMORY_PARTS = {"archive", "templates"}
DEFAULT_MEMORY_PATHS = (
    "docs/project-memory/INDEX.md",
    "docs/project-memory/PROJECT-CONTEXT.md",
    "docs/project-memory/DOS-AND-DONTS.md",
)
LEARNER_SKILL = ".agents/skills/project-memory-learner/SKILL.md"


@dataclass(frozen=True)
class MemoryDocument:
    path: str
    title: str
    headings: tuple[str, ...]
    text: str


def find_project_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
        if (
            (candidate / "AGENTS.md").is_file()
            and (candidate / "docs" / "project-memory" / "INDEX.md").is_file()
        ):
            return candidate
    raise FileNotFoundError(f"No project root found from {start}")


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _read_document(path: Path, root: Path) -> MemoryDocument:
    text = path.read_text(encoding="utf-8")
    headings = tuple(HEADING_RE.findall(text))
    title = headings[0] if headings else path.stem.replace("-", " ").title()
    return MemoryDocument(relative_posix(path, root), title, headings[:6], text)


def load_memory_documents(root: Path) -> list[MemoryDocument]:
    memory_root = root / "docs" / "project-memory"
    paths: list[Path] = []
    if memory_root.is_dir():
        for path in memory_root.rglob("*.md"):
            relative_parts = set(path.relative_to(memory_root).parts)
            if relative_parts & EXCLUDED_MEMORY_PARTS:
                continue
            paths.append(path)

    skills_root = root / ".agents" / "skills"
    if skills_root.is_dir():
        paths.extend(skills_root.glob("*/SKILL.md"))

    return [_read_document(path, root) for path in sorted(set(paths))]


def tokenize(value: str) -> set[str]:
    return {
        token.lower()
        for token in TOKEN_RE.findall(value)
        if len(token) > 2 and token.lower() not in STOPWORDS
    }


def score_document(query_tokens: set[str], document: MemoryDocument) -> int:
    if not query_tokens:
        return 0
    path_tokens = tokenize(document.path)
    title_tokens = tokenize(" ".join((document.title, *document.headings)))
    body_tokens = tokenize(document.text)
    return sum(
        8 if token in path_tokens else 5 if token in title_tokens else 1 if token in body_tokens else 0
        for token in query_tokens
    )


def retrieve(root: Path, query: str, limit: int = 5) -> list[MemoryDocument]:
    documents = load_memory_documents(root)
    scored = [
        (score_document(tokenize(query), document), document)
        for document in documents
    ]
    matched = [document for score, document in sorted(scored, key=lambda item: (-item[0], item[1].path)) if score > 0]
    if matched:
        return matched[:limit]

    by_path = {document.path: document for document in documents}
    return [by_path[path] for path in DEFAULT_MEMORY_PATHS if path in by_path][:limit]


def format_retrieval(documents: Iterable[MemoryDocument]) -> str:
    lines = []
    for document in documents:
        heading = document.headings[1] if len(document.headings) > 1 else document.title
        lines.append(f"- `{document.path}` — {heading}")
    return "\n".join(lines)


def session_start_context(root: Path) -> str:
    documents = load_memory_documents(root)
    categories: dict[str, int] = {
        "practices": 0,
        "decisions": 0,
        "known-solutions": 0,
        "project-skills": 0,
    }
    for document in documents:
        if "/practices/" in f"/{document.path}":
            categories["practices"] += 1
        elif "/decisions/" in f"/{document.path}":
            categories["decisions"] += 1
        elif "/known-solutions/" in f"/{document.path}":
            categories["known-solutions"] += 1
        elif document.path.startswith(".agents/skills/"):
            categories["project-skills"] += 1

    counts = ", ".join(f"{name}: {count}" for name, count in categories.items())
    return (
        "Project-scoped autonomous memory is active for this repository. "
        "Before meaningful work, read `docs/project-memory/INDEX.md`, retrieve only "
        "the relevant records, and verify their claims against current code. "
        f"Available catalog: {counts}. At task completion, the Stop hook requires one "
        f"learning pass using `{LEARNER_SKILL}`. Never retain raw chats or secrets."
    )


def prompt_context(root: Path, prompt: str) -> str:
    matches = retrieve(root, prompt)
    return (
        "Relevant project-memory candidates were retrieved automatically:\n"
        f"{format_retrieval(matches)}\n"
        "Read only what is relevant. Treat these files as guidance, then verify paths, "
        "versions, configuration, and behavior against the current repository."
    )


def hook_context(event_name: str, context: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": event_name,
            "additionalContext": context,
        }
    }


def stop_response(event: dict[str, Any]) -> dict[str, Any]:
    if event.get("stop_hook_active"):
        return {"continue": True}
    return {
        "decision": "block",
        "reason": (
            "Perform the mandatory project-memory learning pass using "
            f"`{LEARNER_SKILL}`. Review this turn for durable user corrections, "
            "verified errors and working solutions, changed implementation practices "
            "or decisions, and repeatable project procedures. Consolidate approved "
            "learning into existing memory before adding files; create or update a "
            "project skill only when its evidence gate passes. If nothing qualifies, "
            "explicitly conclude that there is no durable project learning. Run "
            "`python tools/memory_check.py --strict` if durable memory changed, then finish."
        ),
    }


def run_memory_check(root: Path) -> int:
    checker_path = root / "tools" / "memory_check.py"
    if not checker_path.is_file():
        print(f"Project-memory checker is missing: {checker_path}", file=sys.stderr)
        return 1

    spec = importlib.util.spec_from_file_location("project_memory_check", checker_path)
    if spec is None or spec.loader is None:
        print("Unable to load the project-memory checker.", file=sys.stderr)
        return 1
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = module.validate_repository(root)
    for error in result.errors:
        print(error, file=sys.stderr)
    return 1 if result.errors else 0


def dispatch_hook(event: dict[str, Any]) -> tuple[dict[str, Any] | None, int]:
    event_name = event.get("hook_event_name") or event.get("event")
    root = find_project_root(Path(event.get("cwd") or Path.cwd()))

    if event_name == "SessionStart":
        return hook_context("SessionStart", session_start_context(root)), 0
    if event_name == "UserPromptSubmit":
        return hook_context("UserPromptSubmit", prompt_context(root, str(event.get("prompt", "")))), 0
    if event_name == "Stop":
        return stop_response(event), 0
    if event_name == "SessionEnd":
        return None, run_memory_check(root)
    return None, 0


def handle_hook() -> int:
    try:
        event = json.load(sys.stdin)
        output, status = dispatch_hook(event)
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print(f"Project-memory hook failed: {exc}", file=sys.stderr)
        return 1
    if output is not None:
        print(json.dumps(output, ensure_ascii=False))
    return status


def simulate(root: Path) -> int:
    documents = load_memory_documents(root)
    if not documents:
        raise RuntimeError("No project-memory documents were found.")

    start, start_status = dispatch_hook({"hook_event_name": "SessionStart", "cwd": str(root)})
    prompt, prompt_status = dispatch_hook(
        {"hook_event_name": "UserPromptSubmit", "cwd": str(root), "prompt": "security validation configuration"}
    )
    stop, stop_status = dispatch_hook({"hook_event_name": "Stop", "cwd": str(root), "stop_hook_active": False})
    resumed, resumed_status = dispatch_hook({"hook_event_name": "Stop", "cwd": str(root), "stop_hook_active": True})

    if any((start_status, prompt_status, stop_status, resumed_status)):
        raise RuntimeError("A simulated hook returned a failure status.")
    if not start or not prompt or stop.get("decision") != "block" or resumed != {"continue": True}:
        raise RuntimeError("The autonomous learning loop contract is incomplete.")
    print(f"Project-memory loop simulation passed with {len(documents)} indexed documents.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("hook", help="Handle one Codex hook event from JSON stdin.")
    retrieve_parser = subparsers.add_parser("retrieve", help="Show project-memory matches for a query.")
    retrieve_parser.add_argument("query")
    retrieve_parser.add_argument("--limit", type=int, default=5)
    subparsers.add_parser("simulate", help="Exercise the hook contracts without changing files.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "hook":
        return handle_hook()
    root = find_project_root(Path.cwd())
    if args.command == "retrieve":
        print(format_retrieval(retrieve(root, args.query, args.limit)))
        return 0
    if args.command == "simulate":
        return simulate(root)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
