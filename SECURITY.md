# Security policy

## Reporting a vulnerability

Do not open a public issue containing exploit details, credentials, private repository content, or personal data. Use the repository owner's private security-reporting channel when one is configured.

Before publishing a fork of this template, replace this section with a concrete private contact or enable GitHub private vulnerability reporting.

## Project-memory safety

Project memory must never contain:

- Passwords, access tokens, API keys, private keys, or session cookies.
- Raw production payloads, customer data, or personal information.
- Private incident details that are not approved for the repository's audience.
- Instructions that weaken authentication, authorization, validation, encryption, logging, or audit controls without an accepted decision record.

Use environment-variable names and secret-manager references instead of values. Sanitize logs and examples before adding them to known-solution records.

The validator performs only high-confidence secret-pattern checks. It is not a substitute for repository secret scanning or human review.
