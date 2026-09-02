---
status: accepted
last_verified: 2026-09-02
applies_to: inputs-and-boundaries
owner: maintainers
---

# Validation practices

- Validate at every trust boundary; client validation improves UX but never replaces server validation.
- Prefer shared schemas or generated types when the stack supports them.
- Normalize only when normalization cannot change security meaning.
- Reject unknown or unexpected fields where silent acceptance creates risk.
- Return stable, non-sensitive error codes and user-safe messages.
- Test valid, invalid, missing, boundary, malformed, duplicated, and unauthorized inputs.
- Keep database constraints for invariants that must survive application bugs or concurrent requests.
- Record project-specific size, format, locale, and uniqueness rules next to their authoritative schema.

Never document real personal data or production payloads as validation examples.
