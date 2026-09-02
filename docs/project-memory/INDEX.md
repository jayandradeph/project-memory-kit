# Project memory index

This index is the routing layer for project knowledge. Read only the sections relevant to the current task, then verify them against current code and tests.

## Start here

- [Project context](PROJECT-CONTEXT.md): purpose, stack, architecture, commands, and important paths.
- [Do's and don'ts](DOS-AND-DONTS.md): project-wide behavioral rules.
- [Memory maintenance](MAINTENANCE.md): freshness, superseding, archiving, and verification.

## Implementation practices

- [UI](practices/UI.md)
- [Validation](practices/VALIDATION.md)
- [Security](practices/SECURITY.md)
- [Configuration](practices/CONFIGURATION.md)

## Historical knowledge

- [Decisions](decisions/INDEX.md)
- [Known solutions](known-solutions/INDEX.md)
- [Archive](archive/README.md)

## Templates

- [Decision record](templates/DECISION.md)
- [Known solution](templates/KNOWN-SOLUTION.md)

## Routing rules

- UI or accessibility change: read UI and validation practices.
- Input, API, database, or form change: read validation and security practices.
- Authentication, authorization, secrets, privacy, or logging change: read security and configuration practices.
- Environment, dependency, deployment, or feature-flag change: read configuration and relevant decisions.
- Repeated or unfamiliar failure: search known solutions by exact error text, component, dependency, and symptom.
- Cross-cutting or irreversible choice: search decisions before proposing a new one.
