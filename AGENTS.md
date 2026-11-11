# AGENTS.md — Instructions for AI agents working in this repo

> Humans: this file is also a good 2-minute orientation. Keep it under ~150 lines; it is loaded into every agent session.

## 1. What this project is (fill in — 3 sentences max)

<!-- One sentence: what it is. One sentence: who it is for. One sentence: the current top priority. -->
**[Project name]** is a … for … . Right now the priority is **[RM-xx: …]**.

Full context: [`kb/01-context/charter.md`](kb/01-context/charter.md)

## 2. Read before you act

| If your task is… | Read first |
|---|---|
| Anything | [`kb/07-status/current-state.md`](kb/07-status/current-state.md), [`kb/01-context/glossary.md`](kb/01-context/glossary.md) |
| Changing code (feature or fix) | its `REQ-*` in [`kb/03-requirements/`](kb/03-requirements/index.md) — or its maintenance source (INC, ticket, known issue) — then [`kb/05-implementation/conventions.md`](kb/05-implementation/conventions.md) |
| Building or changing UI | [`kb/08-design/design-system.md`](kb/08-design/design-system.md) + the "UX & design" section of the REQ, or the design reference in the maintenance source. Reuse existing components and tokens; don't invent styles. |
| Changing architecture, dependencies, data model | [`kb/04-architecture/overview.md`](kb/04-architecture/overview.md) + the accepted ADRs linked from the affected component or REQ |
| Deploy / config / infra / incident | [`kb/06-operations/environments.md`](kb/06-operations/environments.md) + relevant runbook |
| Planning / prioritising | [`kb/02-roadmap/roadmap.md`](kb/02-roadmap/roadmap.md) |

Don't read the whole KB up front. Use [`kb/00-index.md`](kb/00-index.md) to find what you need.

## 3. Commands (canonical — other docs link here)

<!-- Exact, copy-pasteable. Agents will run these literally. Extra setup detail goes in conventions.md, not here. -->
```bash
# install
# run locally
# run tests (fast)
# run tests (full)
# lint / format / typecheck
```

**Generated / do-not-edit paths:** `…`

## 4. Hard rules

<!-- Things that must never happen. Keep to the ones that have actually bitten you. -->
- Never commit secrets. Secrets live in: `…`
- Never edit the generated / do-not-edit paths listed in §3.
- Don't reverse an accepted ADR silently. If you think one is wrong, say so and propose a new ADR that supersedes it.
- Don't add a new dependency without stating why in the PR (and an ADR if it's a framework-level choice).
- Production is read-only by default. Never change production, and never run a destructive or irreversible action in any environment that holds real or shared data (anything marked **DESTRUCTIVE** in a runbook; deleting data; dropping tables or queues; force-pushing), on your own. Follow the [change approval policy](kb/06-operations/environments.md#10-change-approval-policy): stop, show the exact command, target environment and expected effect, and wait for a named human to approve. If the command or target changes, ask again.

## 5. How to work

1. **Find the "why".** Product work → its `REQ-` / `RM-` ID. Maintenance work → its source (`INC-`, ticket, or known issue). If there is none for a substantial change, ask before building.
2. **Check acceptance criteria.** Your work is done when the REQ's acceptance criteria pass — or, for maintenance work with no REQ, the verification criteria recorded in its source. Not before, and don't gold-plate beyond them.
3. **Respect "Out of scope".** If the REQ lists something as out of scope, don't build it.
4. **Unclear or contradictory docs?** Code is the source of truth for *what the system does*; the KB is the source of truth for *what it should do and why*. Report mismatches instead of guessing; note them in `current-state.md → Known doc gaps`.
5. **Possibly stale doc?** Check its `last_reviewed` against the freshness rules in `kb/00-index.md`. If stale, verify against code before relying on it.
6. **Small, verifiable steps.** Run the fast tests after each meaningful change.

## 6. Keep the KB true (part of Definition of Done)

When your change affects any of these, update the doc **in the same change**:

| You changed… | Update |
|---|---|
| Behaviour a user can see | the REQ's status (if there is a REQ), `kb/07-status/changelog.md` |
| A design choice that others will depend on | new ADR in `kb/04-architecture/adr/` |
| Components, integrations, data model | `kb/04-architecture/overview.md` |
| UI components, tokens, style rules | `kb/08-design/design-system.md` |
| Commands, generated paths | §3 above |
| Folder layout, coding conventions | `kb/05-implementation/conventions.md` |
| Env vars, deploy steps, alerts, infra | `kb/06-operations/environments.md` / runbooks |
| Discovered a bug, risk, or gap you didn't fix | `kb/07-status/current-state.md` |

Draw diagrams as Mermaid code blocks in the doc, never as image files (rules in `kb/00-index.md`).

Only bump `last_reviewed` when you have checked the **whole** document against reality, not just the part you edited.

## 7. Glossary quick hits

<!-- The 5–10 terms an agent is most likely to get wrong. Full list in glossary.md -->
- **Term** — meaning in *this* project (not the general meaning).
