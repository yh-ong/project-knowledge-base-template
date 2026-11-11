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
| | P1 / P2 / P3 | | `RUN-001` |

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
