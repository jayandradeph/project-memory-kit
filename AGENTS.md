# Project working agreements

This repository uses Git-tracked project memory to prevent context loss and context rot.

Codex project hooks automatically load the memory map, retrieve relevant records, require one evidence-gated learning pass before stopping, and validate memory at session end. The hook-triggered pass uses `.agents/skills/project-memory-learner/SKILL.md`. Hooks assist the workflow; reviewed repository files remain authoritative.

## Before meaningful work

1. Read `docs/project-memory/INDEX.md`.
2. Read only the practice, decision, and known-solution documents relevant to the task.
3. Search the current code and tests before proposing a new pattern.
4. Reuse an existing verified solution when its applicability still matches.
5. Verify documented file paths, versions, configuration, and assumptions against the current repository.
6. If approved policy and implementation disagree, report and reconcile the discrepancy; do not silently choose one.

For read-only explanations, navigation, or trivial formatting changes, a full memory audit is not required.

## Implementation rules

- Prefer the smallest change consistent with existing project patterns.
- Do not create a parallel UI, validation, security, or configuration convention without documenting why the existing convention is insufficient.
- Treat generated graphs, search indexes, summaries, and chat history as secondary evidence.
- Never treat an inferred graph relationship as verified implementation behavior.
- Preserve unrelated user changes.

## Verification states

Use these terms precisely:

- **Implemented:** code or documentation changed; checks may not have run.
- **Build Verified:** automated build, lint, or unit checks passed.
- **Runtime Verified:** relevant behavior was exercised in a running environment.
- **Complete:** requested outcome is delivered, required verification passed, and durable memory is current.

## After meaningful work

1. Run checks proportionate to the change.
2. Update project memory only with durable, reusable knowledge.
3. Add or update a known solution for a non-obvious error or recovery procedure.
4. Link durable guidance to implementation, tests, or verification commands.
5. Supersede or archive obsolete guidance instead of leaving conflicting active rules.
6. Run `python tools/memory_check.py --strict` when project-memory files change.

Do not store progress narration, unverified guesses, raw production payloads, credentials, secrets, personal data, or private keys in project memory.

## Repository changes

- Do not commit, push, publish, or open a pull request unless the user explicitly requests it.
- Do not add runtime dependencies for the memory system without an accepted decision record.
- Keep `AGENTS.md` concise. Put detailed and changing guidance under `docs/project-memory/`.
