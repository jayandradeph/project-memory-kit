# Project Memory Kit architecture

## Authority model

Reviewed Git-tracked Markdown is authoritative. Runtime hooks and generated
indexes improve recall and learning cadence but cannot silently override accepted
records. Code, tests, schemas, and configuration remain implementation evidence.

## Autonomous learning loop

```text
SessionStart -> inject bounded project-memory context
UserPromptSubmit -> retrieve relevant project records
Agent work -> code, tools, verification, user corrections
Stop -> force one reflection/consolidation pass
             |-> update project memory
             |-> create/update a project skill when evidence threshold passes
             `-> run validation
Next session -> retrieve the reviewed result
```

## Components

- `.codex/hooks.json`: project-local Codex lifecycle wiring.
- `tools/project_memory_loop.py`: standard-library hook handler, retrieval, and
  simulation entry point.
- `.agents/skills/project-memory-learner/SKILL.md`: agent-side classification,
  evidence, consolidation, and project-skill creation policy.
- `docs/project-memory/`: authoritative context, practices, decisions, known
  solutions, and maintenance rules.
- `tools/memory_check.py`: structural, metadata, link, freshness, indexing, and
  secret-pattern validation.

## Safety boundaries

- Learning is restricted to the current Git repository.
- Raw transcripts, credentials, personal data, and machine-local paths are not
  written to tracked memory.
- A candidate becomes durable only after evidence or explicit owner correction.
- Existing active records are updated or superseded before creating duplicates.
- Hooks must be reviewed and trusted by each clone before execution.
