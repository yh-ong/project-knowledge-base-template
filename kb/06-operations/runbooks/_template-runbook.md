---
id: RUN-000
title: <alert name or task>
owner: "@handle"
status: active
last_reviewed: YYYY-MM-DD   # last time the whole doc was checked against reality
last_exercised: YYYY-MM-DD  # last time someone actually followed it (real incident or drill)
links: []                   # service, ADR, past INC-
---

# RUN-000 — <alert name or task>

> Written for someone woken at 3 a.m. who has never seen this system. Exact commands, no assumptions.

## When to use
<!-- Alert name / symptom that triggers this runbook. -->

## Impact
<!-- What users experience. How urgent. -->

## Before you start
- **Access needed:** <!-- roles, VPN, break-glass account; how to get it fast -->
- **Where to run commands:** <!-- laptop / bastion host / cloud console / specific k8s context -->
- **Tell people:** post in `#…` that you are working on it; update status page if users are affected (template: `…`)

## Quick check (≤ 2 min)
1. Open dashboard: …
2. Run: `…`
3. If <condition>, it's this issue → go to Fix. Otherwise → Escalate.

## Fix
> ⚠️ Mark every destructive or irreversible step (deletes data, restarts primary, drops queue) with **DESTRUCTIVE** and say what to check first.
> **Approval:** follow the [change approval policy](../environments.md#10-change-approval-policy). Any step that changes production needs approval from a named human; a DESTRUCTIVE step needs it from a second person who is not the one running it. Approver for this runbook: `@…` (backup: `@…`). AI agents never run either kind without that approval.

1. `…`
2. Verify service: `…` — expected output: …
3. Verify data integrity: `…` — expected: … <!-- no lost / duplicated records, counts match -->

## Stop and escalate if
- … <!-- e.g. error rate rises after step 1, data looks inconsistent, fix not working after N minutes -->

## Rollback / if the fix makes it worse
1. …

## Escalate
- After … minutes without recovery, page: …
- Info to include: …

## Afterwards
- [ ] Post resolution in `#…` / status page
- [ ] Open a postmortem if SEV1 or SEV2
- [ ] Update this runbook and `last_exercised`

## Notes / history
<!-- Past incidents (INC-…), gotchas. -->
