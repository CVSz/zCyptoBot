# Safe Project Guidelines (GitHub-Aligned)

> Purpose: translate GitHub Community Guidelines into practical repository rules for maintainers, contributors, and automation.

## 1) Community behavior baseline

- Be welcoming to new contributors and different experience levels.
- Critique code and ideas, never people.
- Assume good intent, ask clarifying questions, and de-escalate disagreements.
- Use inclusive, professional language across issues, PRs, commits, and discussions.

## 2) Project moderation model

### Maintainer actions

- Document expectations in `README.md`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md`.
- Moderate PR/issue comments when they become abusive, unsafe, or off-topic.
- Lock conversations that become hostile or unproductive.
- Apply temporary interaction limits if the repository is targeted by spam/trolling.

### Contributor expectations

- Keep discussions on-topic and technically focused.
- Report suspected policy violations through GitHub reporting/support channels.
- Avoid sharing sensitive/private data in issues, PRs, logs, or screenshots.

## 3) Content safety rules

The project does **not** permit:

- Harassment, bullying, hate speech, threats, or intimidation.
- Doxxing, privacy violations, or exposure of personal/confidential data.
- Malicious instructions intended to damage systems, evade controls, or abuse users.
- Spam, coordinated manipulation, or deceptive impersonation.

## 4) Secure collaboration controls

- Enforce branch protection for default branch.
- Require pull request review before merge.
- Require passing CI checks (lint, tests, security scans) before merge.
- Enable secret scanning and dependency vulnerability alerts.
- Use least-privilege repo roles and regularly audit collaborator access.

## 5) Incident response workflow

1. **Detect:** identify harmful content/behavior via reports or maintainer review.
2. **Triage:** classify severity (low/medium/high/critical).
3. **Contain:** hide/delete harmful content, lock thread, limit interactions, or block actor.
4. **Notify:** document internally and notify relevant maintainers.
5. **Recover:** reopen collaboration channels after risk is addressed.
6. **Improve:** add preventive controls and update policy docs.

## 6) AI/automation safety guardrails

- AI-generated output must be reviewed by a human before merge.
- Disallow automated content that targets individuals or protected groups.
- Require manual approval for automation that changes access controls, billing, or production infrastructure.
- Log high-impact automation actions for traceability and audit.

## 7) Enforcement and appeals

- Maintainers may remove violating content and restrict abusive users.
- Escalate severe/repeated abuse through official GitHub support/report mechanisms.
- Permit appeal requests through maintainer contact path with documented rationale.

## 8) Reviewer inline comment templates (for “Files changed”)

Use these in PR review comments on specific lines:

- `Safety:` “This change may expose sensitive data in logs; please redact/tokenize.”
- `Respect:` “Please rephrase this comment to focus on implementation details, not author intent.”
- `Abuse-risk:` “This logic could be misused for spam/abuse; add explicit rate limits and validation.”
- `Governance:` “This production-impacting change needs one additional maintainer approval.”

## Source basis

This document is derived from GitHub Community Guidelines and mapped into repository-specific practices.
