# Existing AGENTS.md integration snippet

If the target repository already has an `AGENTS.md`, merge the following section into it instead of replacing existing project instructions:

```md
## Project-memory workflow

Before meaningful implementation, read `docs/project-memory/INDEX.md`, then read only the relevant practices, decisions, and known solutions. Search current code and tests before creating a new pattern. Reuse verified solutions only after checking their applicability against current versions and implementation.

After meaningful work, update durable project memory, link it to implementation or verification evidence, supersede conflicting guidance, and run `python tools/memory_check.py --strict` when memory files change. Never store credentials, secrets, personal data, raw production payloads, or unverified guesses in project memory.
```
