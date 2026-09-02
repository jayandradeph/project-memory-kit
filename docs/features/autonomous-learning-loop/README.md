# Autonomous project learning loop

- Lifecycle state: **Build Verified**
- Evidence state: **Implemented and locally verified**
- Last verified: **2026-09-02**
- Project status: [Project dashboard](../../project/STATUS.md)

## Goal

Give Project Memory Kit a Hermes-style closed learning loop scoped to one
repository: automatically retrieve relevant project memory, force a reflection
pass before an agent stops, persist verified learning, consolidate conflicts,
and create or improve reusable project skills when the evidence threshold is
met.

## Scope

- Project-local Codex lifecycle hooks for start, prompt retrieval, stop-time
  reflection, and end-of-session validation.
- Standard-library deterministic retrieval and hook output.
- A project-local learner skill that controls classification, verification,
  persistence, supersession, and skill creation.
- Installer support, strict validation, documentation, and cross-platform tests.
- A trust/review guide for collaborators and new machines.

## Non-goals

- Global user profiling or cross-project memory.
- Silent model training or weight updates.
- Treating raw chat history, generated summaries, or learned skills as higher
  authority than reviewed project records.
- Storing secrets, personal data, raw production payloads, or full transcripts.
- Adding a hosted database or runtime dependency.

## Acceptance criteria

- A project clone installs `.codex/hooks.json`, the hook handler, and the
  project-memory learner skill without overwriting existing files.
- `SessionStart` injects a bounded memory contract and active-memory routes.
- `UserPromptSubmit` ranks and suggests relevant project-memory documents.
- `Stop` triggers exactly one learning reflection continuation and avoids an
  infinite continuation loop.
- The learner distinguishes corrections, practices, decisions, known solutions,
  and procedural skills; it updates existing records before adding new ones.
- New project skills require repeatable procedure evidence or explicit owner
  confirmation and remain under `.agents/skills/`.
- Strict validation checks the autonomous-loop files and project-skill safety.
- Unit tests cover retrieval, hook JSON contracts, stop-loop protection,
  installer behavior, and validation.
- The full suite passes on supported Python versions without third-party
  packages.

## Implementation summary

Implemented a dependency-free project-local loop:

- `.codex/hooks.json` connects session start, prompt submission, stop, and
  session end to `tools/project_memory_loop.py` on Windows, macOS, and Linux.
- The handler maps project memory at startup, ranks relevant records for each
  prompt, requests exactly one stop-time learning pass, and validates memory at
  session end without retaining prompts or transcripts.
- `.agents/skills/project-memory-learner/SKILL.md` classifies durable learning
  and enforces evidence, consolidation, secret-safety, and project-skill gates.
- The installer, strict validator, documentation, and tests cover the new
  components.

## Verification matrix

| Gate | State | Evidence |
|---|---|---|
| Strict project-memory validation | Passed | `python tools/memory_check.py --strict`: 0 warnings |
| Unit tests | Passed | 17 tests passed; one Windows symlink test skipped where privileges were unavailable |
| Hook event simulation | Passed | 14 documents indexed; lifecycle contract passed |
| Learner skill validation | Passed | Skill Creator `quick_validate.py` |
| Live trusted Codex hook run | Not run | Requires a new trusted session |

## Open items

- Exercise the trusted hooks in a fresh Codex session.
- Let GitHub Actions verify the suite on Linux, Windows, and macOS after an
  explicitly requested push.

## Next step

Exercise the trusted hooks in a fresh Codex session. The verified components
were installed and customized in RAN-ONLINE on 2026-09-02.
