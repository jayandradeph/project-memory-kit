# Project Memory Kit

Project Memory Kit is a Git-backed memory system for AI-assisted software projects. It gives each new AI session a small, reliable entry point and keeps durable project knowledge close to the code it describes.

The kit is designed to reduce two different failures:

- **Context loss:** a new session does not know what previous sessions learned.
- **Context rot:** stored guidance becomes stale, duplicated, contradictory, or impossible to verify.

The repository works without a database, hosted service, account, or API key. Obsidian and Graphify are optional additions.

## What is included

- A concise [`AGENTS.md`](AGENTS.md) that enforces a memory-first workflow.
- Structured project memory for UI, validation, security, and configuration practices.
- Decision and known-solution templates with freshness and verification metadata.
- A standard-library Python validator that checks structure, metadata, links, placeholders, and likely secrets.
- Cross-platform tests and GitHub Actions validation.
- Optional guides for Obsidian and Graphify.

## Quick start: use this as a new repository

1. Clone or use this repository as a GitHub template.
2. Replace the bracketed values in [`PROJECT-CONTEXT.md`](docs/project-memory/PROJECT-CONTEXT.md).
3. Review the default practices and remove anything that does not apply.
4. Run the validator:

   ```bash
   python tools/memory_check.py --strict
   ```

   On Windows, `py -3 tools/memory_check.py --strict` works as an alternative.

5. Ask your coding agent:

   > Read AGENTS.md and summarize the active project memory before making changes.

## Add the kit to an existing repository

From a clone of this kit, run:

```bash
python scripts/install.py --target /path/to/your/project --project-name "My Project"
```

The installer is deliberately conservative:

- It never overwrites an existing file.
- It does not initialize Git, install dependencies, or modify agent settings.
- If the target already has an `AGENTS.md`, it installs an integration snippet instead of replacing the file.
- It reports every copied and skipped file.

After installation, review the generated project context and run:

```bash
python tools/memory_check.py --strict
```

## Daily workflow

```text
New task
  -> read AGENTS.md
  -> open the memory index
  -> read only relevant practices and prior solutions
  -> inspect current code and tests
  -> implement and verify
  -> update durable memory
  -> supersede or archive stale guidance
```

Chat history is never the source of truth. Generated indexes are never the source of truth. The repository remains reviewable through normal pull requests.

## Source-of-truth model

| Information | Authority |
| --- | --- |
| Required behavior and security policy | Approved project documentation |
| Current implementation | Code, tests, schemas, and configuration |
| Design intent | Accepted decision records |
| Previous errors and fixes | Verified known-solution records |
| Generated code relationships | Fresh generated graph output |
| Chat history | Temporary, non-authoritative context |

If implementation and approved policy disagree, treat the discrepancy as work to reconcile. Do not silently choose one.

## Optional tools

### Obsidian

Open `docs/project-memory/` as an Obsidian vault. Obsidian becomes a human-friendly editor and graph viewer over the same Markdown committed to Git. Do not create a separate copy of the memory.

See [`docs/integrations/OBSIDIAN.md`](docs/integrations/OBSIDIAN.md).

### Graphify

Graphify can generate a rebuildable code knowledge graph for dependency and impact questions. Its output is secondary evidence and must be checked against current code.

See [`docs/integrations/GRAPHIFY.md`](docs/integrations/GRAPHIFY.md).

### Semantic or temporal memory

Do not add a memory database by default. Consider Cognee or Graphiti only after the project has a demonstrated cross-repository, multi-agent, or temporal-retrieval requirement and an owner for memory lifecycle and security.

## Validation

Run all checks locally:

```bash
python tools/memory_check.py --strict
python -m unittest discover -s tests -v
```

The reusable GitHub Actions workflow validates memory on every push and pull request. This kit's own test workflow additionally runs the validator and installer tests on Linux, Windows, and macOS.

## Compatibility

- Python 3.9 or newer; no third-party Python packages are required.
- GitHub Actions, Windows, macOS, and Linux.
- Codex automatically discovers `AGENTS.md`. Other coding agents can use the same memory if configured to read `AGENTS.md` and `docs/project-memory/INDEX.md` at the start of a task.

## Reference documentation

- [Codex custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex Model Context Protocol setup](https://learn.chatgpt.com/docs/extend/mcp)
- [Obsidian Graph View](https://help.obsidian.md/plugins/graph)
- [Graphify quickstart](https://www.graphiffy.com/docs)

## Contributing and security

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for development rules and [`SECURITY.md`](SECURITY.md) for responsible reporting and memory-safety guidance.

## License

MIT. See [`LICENSE`](LICENSE).
