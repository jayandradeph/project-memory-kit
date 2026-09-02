#!/usr/bin/env python3
"""Validate a Project Memory Kit installation using only the Python standard library."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


REQUIRED_PATHS = (
    "AGENTS.md",
    "docs/project-memory/INDEX.md",
    "docs/project-memory/PROJECT-CONTEXT.md",
    "docs/project-memory/DOS-AND-DONTS.md",
    "docs/project-memory/MAINTENANCE.md",
    "docs/project-memory/practices/UI.md",
    "docs/project-memory/practices/VALIDATION.md",
    "docs/project-memory/practices/SECURITY.md",
    "docs/project-memory/practices/CONFIGURATION.md",
    "docs/project-memory/decisions/INDEX.md",
    "docs/project-memory/known-solutions/INDEX.md",
)

REQUIRED_METADATA = ("status", "last_verified", "applies_to", "owner")
ALLOWED_STATUSES = {
    "draft",
    "proposed",
    "accepted",
    "implemented",
    "build-verified",
    "runtime-verified",
    "complete",
    "superseded",
    "archived",
}
NON_ACTIVE_STATUSES = {"draft", "proposed", "superseded", "archived"}
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
TEMPLATE_TOKEN = re.compile(r"`\[[A-Z][A-Z0-9 _/.-]*\]`")
RECORD_HEADING = re.compile(r"^#\s+((?:ADR|ERR)-\d+)\b", re.MULTILINE)

SECRET_PATTERNS = (
    ("private key block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("provider token", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_front_matter(path: Path, result: ValidationResult) -> dict[str, str] | None:
    lines = read_text(path).splitlines()
    if not lines or lines[0].strip() != "---":
        result.errors.append(f"{path}: missing YAML-style front matter")
        return None

    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        result.errors.append(f"{path}: unterminated front matter")
        return None

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            result.errors.append(f"{path}: invalid front-matter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"\'')
    return metadata


def metadata_documents(root: Path) -> Iterable[Path]:
    memory = root / "docs" / "project-memory"
    direct = (
        memory / "PROJECT-CONTEXT.md",
        memory / "DOS-AND-DONTS.md",
        memory / "MAINTENANCE.md",
    )
    for path in direct:
        if path.is_file():
            yield path

    for directory in (memory / "practices", memory / "decisions", memory / "known-solutions"):
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.md")):
            if path.name != "INDEX.md":
                yield path


def markdown_documents(root: Path) -> Iterable[Path]:
    for path in sorted(root.glob("*.md")):
        if path.is_file():
            yield path
    docs = root / "docs"
    if docs.is_dir():
        yield from sorted(path for path in docs.rglob("*.md") if path.is_file())


def validate_required_paths(root: Path, result: ValidationResult) -> None:
    for relative in REQUIRED_PATHS:
        if not (root / relative).is_file():
            result.errors.append(f"missing required file: {relative}")


def validate_agents_contract(root: Path, result: ValidationResult) -> None:
    agents = root / "AGENTS.md"
    if agents.is_file() and "docs/project-memory/INDEX.md" not in read_text(agents):
        result.errors.append(
            "AGENTS.md: must direct agents to docs/project-memory/INDEX.md before meaningful work"
        )


def validate_metadata(root: Path, result: ValidationResult, max_age_days: int) -> None:
    today = date.today()
    seen_ids: dict[str, Path] = {}

    for path in metadata_documents(root):
        metadata = parse_front_matter(path, result)
        if metadata is None:
            continue

        relative = path.relative_to(root)
        for field_name in REQUIRED_METADATA:
            if not metadata.get(field_name):
                result.errors.append(f"{relative}: missing metadata field {field_name!r}")

        status = metadata.get("status", "").lower()
        if status and status not in ALLOWED_STATUSES:
            result.errors.append(
                f"{relative}: unsupported status {status!r}; expected one of {sorted(ALLOWED_STATUSES)}"
            )

        verified = metadata.get("last_verified", "")
        try:
            verified_date = datetime.strptime(verified, "%Y-%m-%d").date()
        except ValueError:
            result.errors.append(f"{relative}: last_verified must use YYYY-MM-DD")
        else:
            if verified_date > today:
                result.errors.append(f"{relative}: last_verified cannot be in the future")
            elif status not in NON_ACTIVE_STATUSES and (today - verified_date).days > max_age_days:
                result.warnings.append(
                    f"{relative}: active guidance was last verified {(today - verified_date).days} days ago"
                )

        heading_match = RECORD_HEADING.search(read_text(path))
        if heading_match:
            record_id = heading_match.group(1)
            if record_id in seen_ids:
                result.errors.append(
                    f"duplicate record id {record_id}: {seen_ids[record_id].relative_to(root)} and {relative}"
                )
            else:
                seen_ids[record_id] = path


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    elif " " in target:
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0])


def validate_links(root: Path, result: ValidationResult) -> None:
    for document in markdown_documents(root):
        relative = document.relative_to(root)
        for raw_target in MARKDOWN_LINK.findall(read_text(document)):
            target = normalize_link_target(raw_target)
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if target.startswith("/"):
                result.errors.append(f"{relative}: repository link must be relative: {raw_target}")
                continue
            resolved = (document.parent / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                result.errors.append(f"{relative}: link escapes repository: {raw_target}")
                continue
            if not resolved.exists():
                result.errors.append(f"{relative}: broken local link: {raw_target}")


def validate_index_coverage(root: Path, result: ValidationResult) -> None:
    memory = root / "docs" / "project-memory"
    for directory_name in ("decisions", "known-solutions"):
        directory = memory / directory_name
        index = directory / "INDEX.md"
        if not index.is_file():
            continue
        index_text = read_text(index)
        for record in sorted(directory.glob("*.md")):
            if record.name == "INDEX.md":
                continue
            metadata = parse_front_matter(record, result)
            if metadata and metadata.get("status", "").lower() not in {"superseded", "archived"}:
                if record.name not in index_text:
                    result.errors.append(
                        f"{record.relative_to(root)}: active record is not linked from {index.relative_to(root)}"
                    )


def validate_placeholders(root: Path, result: ValidationResult) -> None:
    if (root / ".project-memory-template").exists():
        return
    context = root / "docs" / "project-memory" / "PROJECT-CONTEXT.md"
    if context.is_file():
        for token in sorted(set(TEMPLATE_TOKEN.findall(read_text(context)))):
            result.warnings.append(f"{context.relative_to(root)}: unresolved template token {token}")


def validate_secrets(root: Path, result: ValidationResult) -> None:
    for document in markdown_documents(root):
        text = read_text(document)
        relative = document.relative_to(root)
        for label, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                result.errors.append(f"{relative}: possible {label}; remove or sanitize it")


def validate_repository(root: Path, max_age_days: int = 180) -> ValidationResult:
    root = root.resolve()
    result = ValidationResult()
    validate_required_paths(root, result)
    validate_agents_contract(root, result)
    validate_metadata(root, result, max_age_days)
    validate_links(root, result)
    validate_index_coverage(root, result)
    validate_placeholders(root, result)
    validate_secrets(root, result)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root (default: current directory)")
    parser.add_argument(
        "--max-age-days",
        type=int,
        default=180,
        help="warn when active guidance is older than this many days (default: 180)",
    )
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.max_age_days < 1:
        print("error: --max-age-days must be positive", file=sys.stderr)
        return 2
    if not args.root.is_dir():
        print(f"error: repository root does not exist: {args.root}", file=sys.stderr)
        return 2

    result = validate_repository(args.root, args.max_age_days)
    for message in result.errors:
        print(f"ERROR: {message}")
    for message in result.warnings:
        print(f"WARNING: {message}")

    if result.errors or (args.strict and result.warnings):
        print(f"Project memory validation failed: {len(result.errors)} error(s), {len(result.warnings)} warning(s).")
        return 1

    print(f"Project memory validation passed: {len(result.warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
