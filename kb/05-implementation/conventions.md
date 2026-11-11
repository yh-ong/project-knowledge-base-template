---
title: Implementation Conventions
owner: "@tech-lead"
status: active
last_reviewed: YYYY-MM-DD
---

# Implementation Conventions

> Everything a developer or AI agent needs to make a correct change on day one.

## 1. Repo map
```
/src/…        ← what lives here
/tests/…      ← unit / integration split
/scripts/…    ← one-off and ops scripts
/kb/…         ← this knowledge base
```
Generated / do-not-edit paths: see [`AGENTS.md §3`](../../AGENTS.md).

## 2. Setup
Day-to-day commands (install, run, test, lint) are canonical in [`AGENTS.md §3`](../../AGENTS.md) — don't repeat them here. This section holds only what doesn't fit there:

- **Prerequisites (versions):** …
- **First-time setup** (accounts, local services, certificates): …
- **DB migrate / seed data:** …
- **Troubleshooting setup:** …

## 3. Code conventions
<!-- Only what a linter does NOT already enforce. Each rule with a one-line reason. -->
- **Structure:** e.g. feature folders, layering rules (UI → service → repo; never skip).
- **Naming:**
- **Errors:** how to raise, wrap, and surface errors.
- **Logging:** what to log, what never to log (PII, secrets).
- **Config:** read via `…`, never `process.env` directly in business code.
- **Dependencies:** how to add one; what's banned.

## 4. Testing strategy
| Level | What it covers | Where | Must-have for |
|---|---|---|---|
| Unit | | | every PR |
| Integration | | | changes to DB / external calls |
| E2E | | | user-facing flows in REQ acceptance criteria |

## 5. Branching, PRs, release
- Branch naming: `feat/REQ-012-guest-checkout`
- Commit / PR title includes the REQ or RM ID.
- PR must: pass CI, include KB checklist, have ≥ 1 review.
- Release process: see `06-operations/environments.md`.

## 6. Definition of Done
- [ ] Acceptance criteria in the REQ verified (link test or screenshot)
- [ ] Tests added/updated and passing
- [ ] Observability: logs/metrics for the new path
- [ ] KB updated (see AGENTS.md §6)
- [ ] Ops informed if config, infra, or alerts changed

## 7. Common pitfalls
<!-- Hard-won lessons. "If you touch X, also update Y." These save the most AI-agent and new-hire time. -->
- …
