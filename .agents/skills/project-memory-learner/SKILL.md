---
name: project-memory-learner
description: Perform the repository's project-scoped learning pass when a user corrects a project fact, a verified error and working solution emerges, a durable implementation convention or decision changes, or a repeatable project procedure should be retained. Also use when a Codex Stop hook requests the mandatory project-memory reflection. Do not use for transient progress, unverified guesses, raw chat retention, or knowledge unrelated to this repository.
---

# Project Memory Learner

Turn durable project learning into reviewed, Git-tracked memory that future sessions can retrieve.

## Scope

- Keep every learning specific to the current repository.
- Treat `docs/project-memory/` and project-local skills under `.agents/skills/` as the durable authority.
- Never copy learning to a global profile or another project.
- Do not store raw transcripts, prompt history, credentials, secrets, private keys, personal data, or production payloads.

## Learning pass

1. Read `docs/project-memory/INDEX.md` and `docs/project-memory/MAINTENANCE.md`.
2. Review only the current turn and the repository evidence it produced.
3. Decide whether anything is durable and reusable. If not, explicitly conclude that there is no durable project learning and stop.
4. Search the active memory and project-local skills for an existing entry before adding one.
5. Update an existing entry when possible. Do not create a competing rule or duplicate solution.
6. Classify accepted learning:
   - A user correction about project behavior or policy: update project context, do's and don'ts, or the relevant practice.
   - A verified error, root cause, and working recovery: add or update a known solution.
   - A durable cross-cutting technical choice: add or supersede a decision record.
   - A repeatable multi-step procedure: update an existing project-local skill, or create one only when the skill gate below passes.
7. Link the learning to code, tests, configuration, or a reproducible verification command.
8. Supersede or archive obsolete guidance so active documents do not conflict.
9. Run `python tools/memory_check.py --strict` after memory or project-local skill changes.

## Evidence gate

Record a learning only when at least one of these is true:

- The user explicitly corrected or approved a project-specific rule.
- Repository code, tests, configuration, or runtime verification supports it.
- A fix was exercised successfully and its applicability is understood.

Do not promote speculation, one-off narration, incomplete experiments, or an unexplained workaround into project memory.

## Skill gate

Create a new `.agents/skills/<skill-name>/SKILL.md` only when:

- the procedure is project-specific and likely to recur;
- it has succeeded at least twice, or the project owner explicitly asks to preserve it as a skill;
- its trigger is narrow and distinguishable from existing skills;
- it contains no secret, machine-specific absolute path, or raw transcript content; and
- it includes verification and failure boundaries.

Use lowercase letters, digits, and hyphens for the skill directory and frontmatter `name`. Keep detailed reference material outside `SKILL.md` when the instructions would otherwise become unwieldy.

## Known-solution quality

A known solution must include the observable symptom, confirmed cause, applicable environment or version, exact working resolution, verification, and evidence. If the cause or verification is unknown, keep it out of the verified index.

## Boundaries

- Never weaken validation or security policy merely because a workaround appeared to work.
- Never generalize a project rule into a universal rule from one example.
- Never commit, push, publish, or open a pull request unless the user explicitly requests it.
- Never claim autonomous learning occurred when no durable file was updated; report "no durable learning" instead.
