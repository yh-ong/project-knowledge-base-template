---
title: Knowledge Base Index
owner: "@tech-lead"
status: active
last_reviewed: YYYY-MM-DD
---

# Knowledge Base Index

## Reading order by role

| Role | Day 1 (≈30 min) | When needed |
|---|---|---|
| **AI agent** | `AGENTS.md` → `07-status/current-state.md` → task's REQ | ADRs, conventions, runbooks |
| **New developer** | `01-context/charter.md` → `glossary.md` → `04-architecture/overview.md` → `AGENTS.md` → `05-implementation/conventions.md` | ADRs, specs |
| **Product / PM** | `charter.md` → `02-roadmap/roadmap.md` → `03-requirements/index.md` | `current-state.md` |
| **Operations / SRE** | `charter.md` (1 min) → `04-architecture/overview.md` → `06-operations/environments.md` | runbooks, postmortems |
| **Stakeholder / exec** | `charter.md` → `roadmap.md` → `07-status/current-state.md` | — |

## Map

| Section | Answers the question | Key docs |
|---|---|---|
| 01 Context | Why does this exist? For whom? What does success look like? | [charter](01-context/charter.md), [glossary](01-context/glossary.md), [stakeholders](01-context/stakeholders.md) |
| 02 Roadmap | What are we doing, in what order, and why that order? | [roadmap](02-roadmap/roadmap.md) |
| 03 Requirements | What exactly must be true when a feature is done? | [index](03-requirements/index.md), [PRD template](03-requirements/_template-prd.md) |
| 04 Architecture | How is the system shaped, and why? | [overview](04-architecture/overview.md), [ADR template](04-architecture/adr/_template-adr.md) |
| 05 Implementation | How do I build and change it safely? | [conventions](05-implementation/conventions.md), [spec template](05-implementation/_template-spec.md) |
| 06 Operations | How is it deployed, watched, and fixed? | [environments](06-operations/environments.md), [runbook template](06-operations/_template-runbook.md), [postmortem template](06-operations/_template-postmortem.md) |
| 07 Status | Where are we right now? What shipped? | [current state](07-status/current-state.md), [changelog](07-status/changelog.md) |

## Source-of-truth rules

- **Why / what should happen** → this KB.
- **What actually happens** → the code and tests. If they disagree with the KB, one of them is a bug; log it in `current-state.md`.
- **Who is doing what this week** → your issue tracker (link: `…`). The KB holds IDs and links, not task-level churn.
- **Commands** → `AGENTS.md §3` only.
- **API contracts** → the machine-readable files (OpenAPI / protobuf / event schemas) at `…`. Docs link to them.

## Front-matter

Every doc has `title`, `owner` (a person, not a team), `status`, `last_reviewed`. Docs with IDs also have `id`; most have `links`.

```yaml
---
id: REQ-012
title: Guest checkout
owner: "@handle"
status: ready
last_reviewed: 2026-11-11
links: [SPEC-014, ADR-0007]
---
```

ADRs use `date` instead of `last_reviewed`; postmortems use `date`; runbooks add `last_exercised`.

## Status values by document type

| Type | Allowed `status` |
|---|---|
| Living docs (charter, roadmap, overview, conventions, environments, current-state, …) | `draft` · `active` · `deprecated` |
| REQ | `draft` · `ready` · `in-progress` · `done` · `dropped` (meanings in [index](03-requirements/index.md)) |
| SPEC | `draft` · `approved` · `in-progress` · `done` · `superseded` |
| ADR | `proposed` · `accepted` · `superseded` · `deprecated` · `rejected` |
| Runbook | `active` · `deprecated` |
| Postmortem | `draft` · `reviewed` · `actions-complete` |

## Freshness rules

A doc past its window should be treated as **possibly stale** — verify against code before relying on it.

| Type | Review at least | Notes |
|---|---|---|
| `current-state.md` | weekly | |
| `roadmap.md` | every roadmap review (see its cadence) | |
| REQ / SPEC in `ready` or `in-progress` | every 30 days | `done` / `dropped` ones are historical — no expiry |
| `environments.md`, runbooks | quarterly | runbooks: `last_exercised` within 6 months, or drill it |
| Charter, overview, conventions, glossary | every 90 days | |
| Accepted ADRs, closed postmortems | never — historical records | Don't edit; supersede with a new ADR instead |

**Only bump `last_reviewed` after checking the whole document**, not just the part you changed.
