---
status: accepted
last_verified: 2026-09-02
applies_to: codex-project-memory-lifecycle
owner: maintainers
---

# ADR-002: Use a guarded project-local autonomous learning loop

## Context

Manual instructions reduce context loss, but they cannot ensure that every new Codex session recalls relevant project learning or that every completed task evaluates new corrections and verified fixes for retention. The desired behavior is a Hermes-style closed loop while preventing cross-project leakage, indiscriminate chat retention, and stale hidden memory.

## Decision

Use trusted project-local Codex hooks for lifecycle automation and a project-local learner skill for evidence-gated consolidation:

- `SessionStart` injects the project-memory map.
- `UserPromptSubmit` retrieves relevant repository documents.
- `Stop` requires exactly one learning pass before completion.
- `SessionEnd` validates the durable memory structure.
- `.agents/skills/project-memory-learner/SKILL.md` defines what may become a correction, known solution, decision, practice, or repeatable project skill.

The hook handler will not store prompts or consume raw transcripts. Git-tracked Markdown and project-local skills remain the only durable memory, subject to ADR-001.

## Consequences

- New sessions and collaborators receive the same project learning after cloning and trusting the hooks.
- Learning changes are reviewable in ordinary diffs and pull requests.
- Codex automatically evaluates new learning, but may correctly conclude that nothing durable should be retained.
- Each machine must explicitly trust the repository hooks because they execute local commands.
- Other agents can read the memory but need equivalent lifecycle integration for automatic recall and reflection.
- The loop improves project procedures, not model weights, and does not create a global user profile.

## Alternatives considered

- Global or machine-local memory: rejected for authority because it is not reliably shared and can leak context between projects.
- Store every transcript and summarize later: rejected because it increases privacy, secret-retention, and context-rot risk.
- Fully automatic file mutation without an evidence gate: rejected because it can promote guesses and duplicate or contradict approved rules.
- Manual reminders only: rejected because the learning pass is easy to omit at session boundaries.

## Verification and evidence

- `python tools/project_memory_loop.py simulate`
- `python tools/memory_check.py --strict`
- `python -m unittest discover -s tests -v`
- Review `.codex/hooks.json` and exercise the trusted hooks in Codex.

## Supersession

This decision extends ADR-001 and does not supersede it.
