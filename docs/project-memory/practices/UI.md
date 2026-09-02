---
status: accepted
last_verified: 2026-09-02
applies_to: user-interfaces
owner: maintainers
---

# UI practices

These are safe defaults until the project records more specific conventions.

- Reuse established components, spacing, typography, interaction patterns, and design tokens.
- Preserve keyboard access, visible focus, meaningful labels, sufficient contrast, and reduced-motion preferences.
- Design loading, empty, error, success, disabled, and permission-denied states with the primary flow.
- Keep validation messages close to the affected control and preserve user input after recoverable errors.
- Do not encode authorization only through hidden or disabled UI; the server must enforce it.
- Verify responsive behavior at the project's supported breakpoints.
- Add or update visual, component, accessibility, or end-to-end tests according to project risk.

Document project-specific components and screenshots only when they are stable and approved for the repository's audience.
