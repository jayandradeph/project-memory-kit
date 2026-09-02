---
status: runtime-verified
last_verified: 2026-09-02
applies_to: git-2.35-or-newer-managed-or-sandboxed-workspaces
owner: maintainers
---

# ERR-001: Git rejects a workspace as dubious ownership

## Symptoms and signature

Git reports `detected dubious ownership in repository` even though the repository path is correct. Tools that call Git indirectly may instead report that the current directory is not a Git repository.

This can occur when a managed coding-agent or sandbox process runs under a different operating-system identity from the user who owns the workspace.

## Root cause

Git's ownership safety check does not trust the repository because the filesystem owner and current process identity differ. GitHub CLI inherits this behavior when it inspects a local source repository.

## Working solution

First verify the absolute repository path and its owner. Prefer a one-command exception while diagnosing:

```bash
git -c safe.directory=/absolute/verified/repository status
```

If tools such as GitHub CLI must call Git repeatedly, add only the exact verified path:

```bash
git config --global --add safe.directory /absolute/verified/repository
```

On Windows, forward-slash absolute paths avoid quoting and escape ambiguity.

## Do not use when

- Do not set `safe.directory=*`.
- Do not trust a broad parent directory containing unreviewed repositories.
- Do not add a path supplied by untrusted content without resolving and checking it.
- Do not use this workaround when unexpected ownership indicates a genuinely compromised or incorrectly mounted workspace.

## Verification

- `git status` recognized the repository after the exact-path exception.
- GitHub CLI then created the public repository and pushed `main` successfully.
- Final state: Runtime Verified on Windows in a managed sandbox.

## Security and privacy notes

The safe-directory exception bypasses an ownership protection for the listed repository. Keep the scope exact and remove obsolete entries from global Git configuration when they are no longer needed.

## Regression prevention

Use exact paths in automated environments and retain Git's default ownership checks everywhere else. Do not recommend wildcard safe-directory configuration in project documentation or automation.
