---
status: accepted
last_verified: 2026-09-02
applies_to: configuration-and-deployment
owner: maintainers
---

# Configuration practices

- Keep configuration explicit, typed or schema-validated where possible, and separated by environment.
- Commit safe examples and defaults; never commit credentials or production-only values.
- Fail early when required configuration is missing or malformed.
- Document precedence among files, environment variables, command-line options, and remote configuration.
- Prefer one canonical name for each setting and provide migrations for renamed settings.
- Keep secure production defaults; local convenience must not silently weaken deployed environments.
- Record feature-flag ownership, default state, rollout conditions, and removal plan.
- Verify configuration changes in the environments they affect and document rollback steps for high-risk changes.

Use `.env.example` only for variable names and non-sensitive example values.
