---
status: accepted
last_verified: 2026-09-02
applies_to: project-memory-system
owner: maintainers
---

# Memory maintenance

## What deserves memory

Record knowledge when it is durable, non-obvious, reusable, and costly to rediscover. Examples include an accepted architectural choice, a verified recovery procedure, a security boundary, or a project-specific implementation convention.

Do not record task narration, temporary debugging guesses, unreviewed opinions, or information immediately obvious from a single current file.

The Codex `Stop` hook triggers the project-memory learner once before task completion. The learner must explicitly conclude that there is no durable project learning when the evidence gate does not pass. A hook trigger is not itself permission to retain the interaction.

Create a project-local skill only for a repeatable, project-specific procedure that has succeeded at least twice or that the project owner explicitly asks to preserve. Skills remain subject to the same review, secret-safety, freshness, and supersession rules as memory documents.

## Freshness

Every active practice, decision, and known solution has a `last_verified` date and applicability statement. Verification means checking the guidance against current code, tests, configuration, and dependency versions—not merely rereading it.

The validator warns when active records exceed its configured age threshold. Strict CI treats warnings as failures so maintainers must revalidate, supersede, or archive stale records.

## Conflicts

When two active records conflict:

1. Stop applying either record as unquestioned guidance.
2. Inspect the current implementation, tests, and accepted decisions.
3. Decide which guidance remains valid.
4. Update the surviving record.
5. Mark the replaced record `superseded` and link the replacement.

## Archive policy

Archived records remain searchable for historical debugging but are excluded from active guidance. Keep the reason for retirement and the replacement link in the archived record.

## Review cadence

- Review affected memory during every meaningful implementation change.
- Run the validator on every pull request.
- Run the scheduled strict validation at least monthly.
- Review security and configuration practices after dependency, deployment, identity, or data-flow changes.
