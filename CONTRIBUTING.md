# Contributing Guide

Thank you for improving zypto.

## Branching & Commits
- Create focused branches per change set.
- Use descriptive commit messages with a clear scope.
- Keep PRs small enough for effective review.

## Pull Request Requirements
- Explain motivation, implementation details, and rollout impact.
- Link related issues/tasks where applicable.
- Include test/verification commands and outcomes.
- Update relevant documentation for behavior/configuration changes.

## Quality Gates
- Ensure linting/formatting/testing pass for affected components.
- Avoid unrelated refactors in the same PR.
- Preserve backward compatibility unless explicitly coordinated.

## Security & Compliance
- Never commit secrets, credentials, or private keys.
- Respect tenant isolation and data handling boundaries.
- Document high-risk changes with mitigation notes.

## Review Process
- CODEOWNERS approval is required for protected areas.
- Address all review comments before merge.
