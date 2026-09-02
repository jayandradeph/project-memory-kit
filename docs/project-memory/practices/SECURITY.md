---
status: accepted
last_verified: 2026-09-02
applies_to: security-and-privacy
owner: maintainers
---

# Security practices

- Enforce authentication and authorization on trusted server-side boundaries.
- Apply least privilege to identities, tokens, database roles, filesystem access, and automation.
- Keep secrets outside source control; document names and secret-manager locations, never values.
- Use parameterized queries and context-appropriate output encoding.
- Protect state-changing operations against replay, duplication, and cross-site request forgery where applicable.
- Avoid leaking credentials, tokens, personal data, internal identifiers, or stack traces through logs and errors.
- Review dependency, data-flow, identity, encryption, and retention changes proportionate to risk.
- Add regression tests for fixed vulnerabilities when safe to do so.
- Treat generated or AI-suggested security conclusions as hypotheses until verified.

Security exceptions require an accepted decision record with owner, scope, compensating controls, and expiration or review date.
