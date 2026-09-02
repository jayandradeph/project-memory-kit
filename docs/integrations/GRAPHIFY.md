# Optional Graphify setup

Graphify creates a generated code knowledge graph for dependency, architecture, and impact questions. It complements project memory but does not replace reviewed practices, decisions, known solutions, code, or tests.

## Install on each developer machine

Review the current [Graphify documentation](https://www.graphiffy.com/docs) and source before installing a third-party tool. Its documented installation currently uses:

```bash
uv tool install graphifyy
graphify install
```

Inside a supported coding agent, build the graph:

```text
/graphify .
```

After meaningful code changes, update it:

```text
/graphify . --update
```

The default output directory, `graphify-out/`, is ignored because it is rebuildable and can become stale. Teams that choose to commit or centrally serve graph output should record that decision and enforce freshness in CI.

## Usage rule

Treat `EXTRACTED` relationships as code-derived evidence that still requires current-file verification. Treat `INFERRED` and `AMBIGUOUS` relationships as leads, not facts.

Do not send private documentation, schemas, or repository content to an external model backend without approval. Code parsing and non-code enrichment can have different data-handling paths; review the selected configuration.
