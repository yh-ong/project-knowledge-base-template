---
id: SPEC-000             # own sequence number
title: <feature> — technical design
owner: "@handle"
status: draft            # draft | approved | in-progress | done | superseded
implements: [REQ-000]    # one or more REQs
last_reviewed: YYYY-MM-DD
links: []                # ADR-xxxx, PRs
---

# SPEC-000 — <feature> technical design

> Write this when the change touches more than one component, adds data, or is risky. Skip for small changes — the REQ + PR is enough.

## 1. Summary
<!-- 3 sentences: what changes, where, and the main approach. -->

## 2. Approach
<!-- Diagrams welcome. Explain the key idea, not every line. -->

### Alternatives rejected
| Option | Why not |
|---|---|
| | |

## 3. Changes by component
| Component | Change | Files / modules |
|---|---|---|
| | | |

## 4. Data & API changes
- **Schema / migrations:** (backward compatible? backfill needed?)
- **API contract:** (new/changed endpoints, events; versioning — link the change to the machine-readable contract file, don't copy it here)
- **Breaking changes:**

## 5. Operational impact (required — ops reads this)
| Aspect | Change |
|---|---|
| New config / env vars / secrets | |
| Infra (new service, queue, bucket…) | |
| Metrics / dashboards | |
| Alerts → runbook | RUN-… |
| Capacity / cost | |
| Deploy order / migration steps | |
| Rollback plan | |

## 6. Security & privacy
<!-- New data collected? Access control changes? Threats considered? -->

## 7. Test plan
| AC (from REQ) | How verified | Test location |
|---|---|---|
| AC1 | unit / integration / e2e / manual | |

## 8. Task breakdown
<!-- Small, independently mergeable steps. Good for humans and for handing to AI agents one at a time. -->
- [ ] T1 — … (est.)
- [ ] T2 — …
- [ ] T3 — …

## 9. Risks & open questions
| Item | Mitigation / owner |
|---|---|
| | |
