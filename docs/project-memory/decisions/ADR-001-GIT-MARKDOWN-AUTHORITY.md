---
status: accepted
last_verified: 2026-09-02
applies_to: project-memory-architecture
owner: maintainers
---

# ADR-001: Keep Git-tracked Markdown authoritative

## Context

AI chat history is session-bound, while automatically accumulated memory can become stale, duplicated, difficult to review, or inaccessible to collaborators. The project also needs to work after a public clone on Windows, macOS, and Linux without requiring a hosted memory service.

## Decision

Reviewed Markdown committed with the project is the canonical memory layer. `AGENTS.md` is the concise bootstrap that routes agents to `docs/project-memory/INDEX.md`. Code, tests, schemas, and configuration remain the evidence for current implementation.

Obsidian may edit and visualize the same Markdown. Generated graphs and semantic-memory services may improve retrieval, but their output is secondary, rebuildable evidence and cannot silently override reviewed records.

## Consequences

- Memory changes are visible in ordinary commits and pull requests.
- New machines and collaborators receive the same baseline by cloning the repository.
- Maintainers must curate, verify, supersede, and archive records rather than automatically retaining every interaction.
- Semantic or graph retrieval remains optional and can be added without migrating the authority layer.

## Alternatives considered

- Chat history alone: rejected because it is not a stable, project-wide source of truth.
- Obsidian-only vault: rejected because a separate vault can diverge from the repository.
- Automatically ingested vector or graph database as authority: rejected because ingestion can preserve incorrect or obsolete statements without review.
- One large `AGENTS.md`: rejected because detailed context consumes startup budget and becomes difficult to route or maintain.

## Verification and evidence

- `python tools/memory_check.py --strict`
- `python -m unittest discover -s tests -v`
- GitHub Actions validation on Ubuntu, Windows, and macOS.
- Installer and validator tests exercise fresh target repositories without relying on machine-local memory.

## Supersession

This is the initial authority decision and supersedes no earlier record.
