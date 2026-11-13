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
| **Designer** | `charter.md` → `glossary.md` → `08-design/design-system.md` → `03-requirements/index.md` | REQ "UX & design" sections |
| **Operations / SRE** | `charter.md` (1 min) → `04-architecture/overview.md` → `06-operations/environments.md` | runbooks, postmortems |
| **Stakeholder / exec** | `charter.md` → `roadmap.md` → `07-status/current-state.md` | — |

## Map

| Section | Answers the question | Key docs |
|---|---|---|
| 01 Context | Why does this exist? For whom? What does success look like? | [charter](01-context/charter.md), [glossary](01-context/glossary.md), [stakeholders](01-context/stakeholders.md) |
| 02 Roadmap | What are we doing, in what order, and why that order? | [roadmap](02-roadmap/roadmap.md) |
| 03 Requirements | What exactly must be true when a feature is done? | [index](03-requirements/index.md), [PRD template](03-requirements/_template-prd.md) |
| 04 Architecture | How is the system shaped, and why? | [overview](04-architecture/overview.md), [ADR template](04-architecture/adr/_template-adr.md) |
| 05 Implementation | How do I build and change it safely? | [conventions](05-implementation/conventions.md), [spec template](05-implementation/specs/_template-spec.md) |
| 06 Operations | How is it deployed, watched, and fixed? | [environments](06-operations/environments.md), [runbook template](06-operations/runbooks/_template-runbook.md), [postmortem template](06-operations/postmortems/_template-postmortem.md) |
| 07 Status | Where are we right now? What shipped? | [current state](07-status/current-state.md), [changelog](07-status/changelog.md) |
| 08 Design | How should it look, feel, and read? | [design system](08-design/design-system.md); per-feature screens are in each REQ's "UX & design" section |

## Source-of-truth rules

- **Why / what should happen** → this KB.
- **What actually happens** → the code and tests. If they disagree with the KB, one of them is a bug; log it in `current-state.md`.
- **Who is doing what this week** → your issue tracker (link: `…`). The KB holds IDs and links, not task-level churn.
- **Day-to-day development commands** (install, run, test, lint) → `AGENTS.md §3` only. Operational commands live in the runbook that uses them.
- **Visual design values** (colours, spacing, type) → the design tokens in code; **screens** → the design files. `design-system.md` links to both.
- **API contracts** → the machine-readable files (OpenAPI / protobuf / event schemas). Their location is recorded once, in [architecture overview §4](04-architecture/overview.md); other docs link to them.

## File naming

- **Docs with IDs:** `<ID>-<slug>.md`, e.g. `REQ-018-guest-checkout.md`.
- **Assets** (screenshots, mockups, exported designs — not diagrams, see below): put them in `kb/assets/` and name them in lowercase words separated by hyphens — `login-flow-empty-state.png`. Not spaces (`Login flow.png`), not underscores (`login_flow.png`), and not run together (`loginflow.png`). Hyphenated names need no escaping in links and read the same everywhere. The KB check warns about spaces and underscores.

## Diagrams

Draw every diagram as a [Mermaid](https://mermaid.js.org) code block inside the doc it belongs to — not as an image file, and not as a link to a drawing tool.

- **Why:** a text diagram shows up in PR diffs, can be edited by anyone (including AI agents) without special software, and renders on GitHub and GitLab.
- **Which type:** `flowchart` for structure and user flows · `sequenceDiagram` for calls between components · `erDiagram` for data · `stateDiagram-v2` for lifecycles and status changes.
- **Keep it readable:** about 15 nodes at most; split a bigger picture into several diagrams.
- **Images are for what Mermaid can't draw:** screenshots and visual mockups. Those go in `kb/assets/`.

## Front-matter

Every doc has `title`, `owner` (a person, not a team), `status`, `last_reviewed`. Docs with IDs also have `id`; most have `links`.

```yaml
---
id: REQ-012
title: Guest checkout
owner: "@maria"
status: ready
last_reviewed: 2026-11-11
links: [SPEC-014, ADR-0007]
---
```

Lists (`links`, `implements`, `supersedes`, `superseded_by`) may be written inline (`[a, b]`) or one `- item` per line; every other field holds a single value.

ADRs use `date` instead of `last_reviewed`; postmortems use `date`; runbooks add `last_exercised`.

## Status values by document type

| Type | Allowed `status` |
|---|---|
| Living docs — everything without an ID (charter, roadmap, overview, design system, conventions, environments, current-state, and the like) | `draft` · `active` · `deprecated` |
| REQ | `draft` · `ready` · `in-progress` · `done` · `dropped` (meanings in [index](03-requirements/index.md)) |
| SPEC | `draft` · `approved` · `in-progress` · `done` · `superseded` |
| ADR | `proposed` · `accepted` · `superseded` · `deprecated` · `rejected` |
| Runbook | `active` · `deprecated` |
| Postmortem | `draft` · `reviewed` · `actions-complete` |

Who may move a doc to `ready`, `approved` or `accepted`: [stakeholders](01-context/stakeholders.md). How review works: [conventions §5.1](05-implementation/conventions.md#51-review).

## Freshness rules

A doc past its window should be treated as **possibly stale** — verify against code before relying on it.

| Type | Review at least | Notes |
|---|---|---|
| `current-state.md` | weekly | |
| `roadmap.md` | every roadmap review (see its cadence) | The KB check assumes 31 days; change `FRESHNESS` in `_tools/kb_check.py` if your cadence differs |
| REQ in `ready` or `in-progress`; SPEC in `approved` or `in-progress` | every 30 days | Other statuses are not being built from — no expiry |
| `environments.md`, runbooks | quarterly | runbooks: `last_exercised` within 6 months, or drill it |
| Charter, overview, conventions, glossary, design system | every 90 days | |
| ADRs, postmortems | never — historical records | Drafts (`proposed` ADRs, `draft` postmortems) are edited freely. Once an ADR is `accepted` or a postmortem is `reviewed`, don't rewrite the decision or the account: only lifecycle fields change (`status`, `superseded_by`, action-item progress). To change a decision, write a new ADR that supersedes it |

**Only bump `last_reviewed` after checking the whole document**, not just the part you changed.
