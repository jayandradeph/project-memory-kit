# Codex autonomous project learning

This integration gives Codex a Hermes-style closed learning loop whose coverage is strictly limited to one repository.

## What happens automatically

1. `SessionStart` injects a bounded map of the repository's project memory.
2. `UserPromptSubmit` retrieves the most relevant project-memory documents and project-local skills for the current request.
3. Codex inspects the current code and performs the work.
4. `Stop` blocks completion once and requests an evidence-gated reflection through `.agents/skills/project-memory-learner/SKILL.md`.
5. The learner updates an existing record first, or adds a correction, verified known solution, accepted decision, or repeatable project skill when its gate passes.
6. The second `Stop` event is allowed through, preventing a reflection loop.
7. `SessionEnd` runs the deterministic repository validator.

The hook handler does not save prompts and does not read or persist raw transcripts. The autonomous part is the lifecycle trigger and agent reflection; durable learning remains visible, reviewable, and reversible in Git.

## Activate after cloning

Project hooks are code execution, so every collaborator must review them on each machine:

1. Open the repository in Codex.
2. Open `/hooks`.
3. Review `.codex/hooks.json` and trust the project hooks.
4. Start a new session in the repository.
5. Run `python tools/project_memory_loop.py simulate` to test retrieval and lifecycle contracts without changing memory.

The repository also includes `.codex/config.toml` with the hooks feature enabled. Codex applies project configuration only after the repository is trusted.

## What the learner may retain

- Explicit project-specific corrections from the owner.
- Verified errors, root causes, working resolutions, and verification steps.
- Durable UI, validation, security, and configuration conventions.
- Accepted cross-cutting decisions.
- Repeatable project procedures that have succeeded twice, or that the owner explicitly asks to preserve as a project skill.

It must search for and update existing guidance before creating a new record.

## What it must not retain

- Raw chat or transcript content.
- Secrets, credentials, private keys, personal data, or production payloads.
- Temporary progress, guesses, failed experiments, or unexplained workarounds.
- Knowledge from another repository or a machine-global user profile.
- A new skill based on one accidental success without owner approval.

## Inspect retrieval

You can see which documents a prompt would retrieve:

```bash
python tools/project_memory_loop.py retrieve "authorization validation"
```

Retrieval is deliberately local and dependency-free. It routes Codex to likely documents; it does not claim that those documents are current. Codex must still verify their paths, versions, assumptions, and behavior against the repository.

## Relationship to Hermes

This kit implements the same practical closed-loop shape—recall, work, reflection, consolidation, and procedural skill improvement—but confines authority and retention to the current Git repository. It does not copy Hermes' global user model, cross-project memory, or raw session store.

## Troubleshooting

- No automatic context: open `/hooks` and confirm the project hooks are trusted and enabled.
- Hook command fails: confirm Python 3.9+ and Git are available on `PATH`.
- Reflection repeats: ensure the installed `tools/project_memory_loop.py` honors `stop_hook_active`.
- Memory check fails: run `python tools/memory_check.py --strict`, fix every reported structural or safety error, then retry.
