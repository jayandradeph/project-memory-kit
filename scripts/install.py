#!/usr/bin/env python3
"""Install Project Memory Kit files into an existing repository without overwriting files."""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path


COPY_PATHS = (
    "docs/project-memory",
    "docs/integration/AGENTS-snippet.md",
    "docs/integrations/OBSIDIAN.md",
    "docs/integrations/GRAPHIFY.md",
    "tools/__init__.py",
    "tools/memory_check.py",
    ".github/workflows/project-memory.yml",
)


@dataclass
class InstallResult:
    copied: list[Path] = field(default_factory=list)
    skipped: list[Path] = field(default_factory=list)


def source_files(kit_root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in COPY_PATHS:
        source = kit_root / relative
        if source.is_dir():
            files.extend(sorted(path for path in source.rglob("*") if path.is_file()))
        elif source.is_file():
            files.append(source)
        else:
            raise FileNotFoundError(f"kit source is missing: {relative}")
    return files


def render_content(source: Path, relative: Path, project_name: str) -> bytes:
    content = source.read_bytes()
    if relative.as_posix() == "docs/project-memory/PROJECT-CONTEXT.md":
        text = content.decode("utf-8").replace("[PROJECT NAME]", project_name)
        return text.encode("utf-8")
    return content


def ensure_within_target(path: Path, target: Path) -> None:
    try:
        path.resolve().relative_to(target.resolve())
    except ValueError as error:
        raise OSError(f"destination escapes target directory: {path}") from error


def install_into(
    kit_root: Path,
    target: Path,
    project_name: str,
    dry_run: bool = False,
) -> InstallResult:
    kit_root = kit_root.resolve()
    target = target.resolve()
    if not target.is_dir():
        raise NotADirectoryError(f"target directory does not exist: {target}")

    result = InstallResult()
    for source in source_files(kit_root):
        relative = source.relative_to(kit_root)
        destination = target / relative
        ensure_within_target(destination, target)
        if destination.exists() or destination.is_symlink():
            result.skipped.append(relative)
            continue
        result.copied.append(relative)
        if dry_run:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(render_content(source, relative, project_name))

    agents_source = kit_root / "AGENTS.md"
    agents_destination = target / "AGENTS.md"
    ensure_within_target(agents_destination, target)
    if agents_destination.exists() or agents_destination.is_symlink():
        result.skipped.append(Path("AGENTS.md"))
    else:
        result.copied.append(Path("AGENTS.md"))
        if not dry_run:
            shutil.copy2(agents_source, agents_destination)

    gitignore_source = kit_root / ".gitignore"
    gitignore_destination = target / ".gitignore"
    ensure_within_target(gitignore_destination, target)
    if gitignore_destination.exists() or gitignore_destination.is_symlink():
        result.skipped.append(Path(".gitignore"))
    else:
        result.copied.append(Path(".gitignore"))
        if not dry_run:
            shutil.copy2(gitignore_source, gitignore_destination)

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path, required=True, help="existing repository directory")
    parser.add_argument("--project-name", required=True, help="name inserted into PROJECT-CONTEXT.md")
    parser.add_argument("--dry-run", action="store_true", help="show actions without writing files")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.project_name.strip() or "\n" in args.project_name or "\r" in args.project_name:
        print("error: --project-name must be a non-empty single line", file=sys.stderr)
        return 2
    kit_root = Path(__file__).resolve().parents[1]
    try:
        result = install_into(kit_root, args.target, args.project_name, args.dry_run)
    except (FileNotFoundError, NotADirectoryError, OSError, UnicodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    action = "Would copy" if args.dry_run else "Copied"
    for relative in result.copied:
        print(f"{action}: {relative.as_posix()}")
    for relative in result.skipped:
        print(f"Skipped existing: {relative.as_posix()}")

    if Path("AGENTS.md") in result.skipped:
        print("Merge docs/integration/AGENTS-snippet.md into the existing AGENTS.md.")
    if Path(".gitignore") in result.skipped:
        print("Review the kit's .gitignore and add the Obsidian and graphify-out entries if needed.")
    print("Review docs/project-memory/PROJECT-CONTEXT.md, then run the strict validator from the target root.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
