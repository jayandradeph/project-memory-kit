# Contributing

Thank you for improving Project Memory Kit.

## Development setup

The project requires Python 3.9 or newer and has no third-party runtime dependencies.

Run the complete local check:

```bash
python tools/memory_check.py --strict
python -m unittest discover -s tests -v
```

## Pull requests

- Keep `AGENTS.md` concise and move detailed guidance into project memory.
- Add tests for validator or installer behavior changes.
- Update documentation when a public command or file contract changes.
- Do not commit real credentials, private repository content, or production data in fixtures.
- Mark the delivered state as Implemented, Build Verified, Runtime Verified, or Complete.

## Project-memory contributions

Active records must include front matter with `status`, `last_verified`, `applies_to`, and `owner`.

Use the templates in `docs/project-memory/templates/`. A known solution should describe the symptom, root cause, working solution, exceptions, and verification. A decision record should explain context, decision, consequences, alternatives, and evidence.

When replacing guidance, set the previous record to `superseded`, link its replacement, and move it to `archive/` when it no longer belongs in active navigation.
