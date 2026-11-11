---
title: Environments & Operations
owner: "@ops-lead"
status: active
last_reviewed: YYYY-MM-DD
---

# Environments & Operations

> Never put secret **values** here — only where they live and who can access them.

## 1. Environments
| Env | Purpose | URL | Deployed from | Data | Access |
|---|---|---|---|---|---|
| local | dev | localhost | working tree | seed | everyone |
| staging | pre-release test | | `main` | anonymised copy | team |
| production | live | | tag / release | real | restricted |

**How staging data is anonymised:** <!-- script / job, what fields are masked, how often refreshed, who runs it --> …

## 2. Deploy & release
- **How a change reaches prod:** <!-- CI pipeline, approvals, schedule -->
- **Deploy command / pipeline link:**
- **Freeze windows:**
- **Rollback:** <!-- exact steps; time to roll back -->
- **DB migrations:** <!-- when/how run; who approves destructive ones -->

## 3. Configuration & secrets
| Name | Purpose | Where set | Secret? | Default |
|---|---|---|---|---|
| `EXAMPLE_URL` | | env / vault / CI | yes / no | |

Secret store: `…` · Access request: `…`

## 4. Infrastructure
| Resource | Provider / type | Region | IaC location | Notes |
|---|---|---|---|---|
| | | | | |

## 5. Observability
- **Dashboards:** …
- **Logs:** where + how to query
- **Tracing:** …
- **SLOs:**

| Service | SLI | SLO | Error budget policy |
|---|---|---|---|
| | availability | 99.9% / 30d | |

## 6. Alerts → runbooks
| Alert | Severity | Meaning | Runbook |
|---|---|---|---|
| | SEV1 / SEV2 / SEV3 | | `RUN-001` |

**Severity scale** — one scale for alerts and postmortems. (REQ priority P0–P2 is a different thing: how important a feature is.)

| Severity | Meaning | Response | Postmortem |
|---|---|---|---|
| SEV1 | Outage, data loss, or security breach affecting many users | page immediately, any hour | required |
| SEV2 | Major feature degraded, or some users blocked | page in working hours; next morning otherwise | required |
| SEV3 | Minor impact; a workaround exists | ticket, next business day | optional |

<!-- Adjust the meanings and response times to your service. -->

## 7. On-call & escalation
- Rotation: …
- Escalation path: L1 → L2 → vendor
- Vendor / third-party support contacts: …

## 8. Backups & disaster recovery
**DR owner:** `@…` · **Restore / failover runbook:** `RUN-…`

| Data store / dependency | Backup schedule & retention | RPO | RTO |
|---|---|---|---|
| | | | |

| Last restore test | Result | Evidence (link) | Next test due |
|---|---|---|---|
| YYYY-MM-DD | pass / partial / fail | | YYYY-MM-DD |

## 9. Recurring operational tasks
| Task | Frequency | Owner | How (link) |
|---|---|---|---|
| Rotate keys | | | |
| Dependency / security patching | | | |

## 10. Change approval policy

The single rule for humans and AI agents. `AGENTS.md` and every runbook link here.

| Class of action | Examples | Who may approve | Who may run it |
|---|---|---|---|
| **Production change** (reversible) | deploy, config or feature-flag change, restart, scaling | one named human: on-call or the service owner — `@…` | the approver, or a person or agent they approved |
| **Destructive / irreversible** (any environment that holds real or shared data) | delete or overwrite data, drop a table or queue, restore over live data, force-push, rotate a key in use | a **second** named person, not the one running it — `@…` (backup: `@…`) | a human; an agent only with that approval, one command at a time |

**What an approval must record** (in the incident channel, ticket, or PR):
- the exact command(s), the target environment, and the expected effect
- who approved, and when

**What an approval covers:** only the exact command or fixed sequence that was shown. If the command, the target, or the expected effect changes in any material way, ask again.

**Enforcement:** this is a procedural rule. It is technically enforced only where tooling does it — list those here: `…` <!-- e.g. protected branches, deploy approvals in CI, database roles without DROP -->
