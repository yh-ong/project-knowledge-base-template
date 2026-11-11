# Project Knowledge Base Template

A copy-into-any-repo template that gives **AI agents, developers, and operations** one shared, trustworthy picture of a project: *why it exists, where it is going, what must be built, how it is built, and how it is run.*

## Why this exists

Most projects lose speed and direction for the same reasons:

| Problem | What this template does about it |
|---|---|
| New people (and AI agents) don't know what the project is for | `kb/01-context/` — one-page charter, glossary, non-goals |
| Work drifts away from the goal | Product work links back to a roadmap item and a goal (traceability IDs) |
| Requirements are vague, so implementation guesses | PRD template has a "ready to build" gate: every must-have maps to acceptance criteria |
| Features look inconsistent, or get built before anyone knows how they should look | `kb/08-design/design-system.md` + a "UX & design" section in every REQ, required before it is `ready` |
| Decisions get re-argued | ADRs record *why*, so nobody (human or AI) silently reverses them |
| Ops learns about features at release time | Spec template has a required "Operational impact" section; runbooks live next to the code |
| Docs rot | Freshness rules per document type, a KB update in the Definition of Done, and an optional CI check |

## Layout

```
AGENTS.md                      ← entry point for AI agents (also symlink as CLAUDE.md)
.github/workflows/kb-check.yml ← runs the KB check in CI
kb/
  00-index.md                  ← map, reading order per role, status & freshness rules
  _tools/kb_check.py           ← KB checker (see "KB check" below) + its tests
  01-context/
    charter.md                 ← what / why / who / goals / non-goals / success metrics
    glossary.md                ← domain terms, one meaning each
    stakeholders.md            ← who decides, who to ask
  02-roadmap/
    roadmap.md                 ← Now / Next / Later + milestones
  03-requirements/
    _template-prd.md           ← copy per feature → REQ-xxx-<slug>.md
    index.md                   ← list of all requirements and their status
  04-architecture/
    overview.md                ← system context, components, data, integrations
    adr/_template-adr.md       ← copy per decision → ADR-xxxx-<slug>.md
  05-implementation/
    conventions.md             ← repo map, coding rules, testing, Definition of Done
    specs/_template-spec.md    ← technical design + task breakdown; copy → specs/SPEC-xxx-<slug>.md
  06-operations/
    environments.md            ← envs, deploy, config, secrets locations, monitoring, DR
    runbooks/_template-runbook.md       ← one per alert / operational task; copy → runbooks/RUN-xxx-<slug>.md
    postmortems/_template-postmortem.md ← one per incident; copy → postmortems/INC-yyyymmdd-nn-<slug>.md
  07-status/
    current-state.md           ← living snapshot: focus, blockers, known issues
    changelog.md               ← what shipped, linked to REQ / ADR IDs
  08-design/
    design-system.md           ← look & feel, tokens, components, states, voice, accessibility
  assets/                      ← screenshots and diagrams, created when first needed; hyphenated names (login-flow.png)
```

Per-feature design (screens, flow, states, copy) lives in each REQ's "UX & design" section.

Every `_template-*` file sits in the folder its copies go in, so the relative links inside it keep working after you copy it.

## Traceability

Every artifact has an ID and links **up** to the reason it exists. There are two valid paths, so maintenance work doesn't need a fake roadmap item:

```
Product work:      GOAL → RM → REQ → (SPEC) → PR
                                ↘ ADR       ↘ RUN

Maintenance / ops: INC | risk | maintenance ticket → (REQ) → PR
                                                     ↘ ADR / RUN if needed
```

- **Product work** (new behaviour users will notice) must link to an `RM-` item. The RM item owns the link to its `GOAL-`; a REQ links to its RM, not to both.
- **Maintenance work** (bug fixes, dependency/security updates, refactors, incident follow-ups) links to its source: an `INC-`, a ticket, or a row in `current-state.md → Known issues`. A REQ is only needed when the behaviour change needs agreed acceptance criteria.
- If product work can't be linked to an RM item, either the roadmap is missing something or the work shouldn't be done. That one rule keeps direction correct.
- Prefer real relative links (`[REQ-018](../03-requirements/REQ-018-guest-checkout.md)`) over bare IDs where the target file exists.

| Prefix | Lives in | Example |
|---|---|---|
| `GOAL-n` | `01-context/charter.md` | `GOAL-2` Reduce checkout drop-off |
| `RM-nn` | `02-roadmap/roadmap.md` | `RM-04` Guest checkout |
| `REQ-nnn` | `03-requirements/` | `REQ-018-guest-checkout.md` |
| `SPEC-nnn` | `05-implementation/specs/` | own number; `implements: [REQ-018]`, or `source:` for maintenance work |
| `ADR-nnnn` | `04-architecture/adr/` | `ADR-0007-use-postgres.md` |
| `RUN-nnn` | `06-operations/runbooks/` | `RUN-004-payment-webhook-backlog.md` |
| `INC-yyyymmdd-nn` | `06-operations/postmortems/` | `INC-20261103-01-db-failover.md` |

## How to adopt (30–60 minutes)

1. Copy `AGENTS.md`, `kb/`, and `.github/workflows/kb-check.yml` into the root of your repo. Optionally `ln -s AGENTS.md CLAUDE.md`.
2. Fill in, in this order: `charter.md` → `glossary.md` → `roadmap.md` → `AGENTS.md` (project summary + commands) → `overview.md` → `design-system.md` (if the project has a UI) → `conventions.md` → `environments.md` → `current-state.md`. Leave the rest until you need them.
3. Delete any section that genuinely doesn't apply — an empty heading is worse than no heading.
4. Add the PR checklist (below) to your PR template.

**The KB is not ready to rely on while any of these remain:** `…` placeholders, `[Project name]`, `YYYY-MM-DD`, example owners like `@handle`, or empty command blocks in `AGENTS.md`. The [KB check](#kb-check-run-locally-and-in-ci) reports those four patterns and a commands block with no runnable command. It can't tell whether what you wrote is *right* — that still needs a read-through.

## Rules that keep it alive

- **Short beats complete.** Each doc should be readable in under 5 minutes. Link out instead of pasting.
- **One fact, one place.** Other docs link to it; they don't copy it. (Commands live in `AGENTS.md §3`; task-level progress lives in the issue tracker.)
- **Write for a smart newcomer with zero context** — that is exactly what an AI agent is.
- **Status and freshness are explicit** — see the rules in [`kb/00-index.md`](kb/00-index.md).
- **Docs change in the same PR as the code.** Not "later".

### PR checklist snippet

```markdown
### Knowledge base
- [ ] Source: <!-- REQ-018 / RM-04 / INC-20261103-01 / ticket link -->
- [ ] Evidence acceptance criteria are met: <!-- test names, screenshot, dashboard link -->
- [ ] Spec / ADR updated if the design changed: <!-- link -->
- [ ] Ops docs updated if config, deploy, migrations, alerts, or runbooks changed: <!-- link -->
- [ ] `changelog.md` updated (user- or ops-visible change)
- [ ] N/A — no knowledge change (explain):
```

### KB check (run locally and in CI)

Docs rot less when a machine checks them. [`kb/_tools/kb_check.py`](kb/_tools/kb_check.py) needs only Python 3.8+ (no packages). Run it from the repo root:

```bash
python3 kb/_tools/kb_check.py
```

| Finds | Level |
|---|---|
| Missing required front-matter fields for the doc type, or a list where a single value belongs | error |
| `status` not allowed for the doc type; postmortem `severity` not SEV1–SEV3 | error |
| Bad ID format, duplicate IDs, invalid or future dates (on every doc, including historical ones) | error |
| A spec with neither `implements` nor `source` | error |
| Broken relative links in `AGENTS.md` and `kb/` — inline and reference-style (code blocks ignored) | error |
| REQ status in `index.md` ≠ the REQ file, an index row with no file, a bad or repeated REQ id in the index, or a malformed index row | error |
| Unfilled placeholders (`…`, `[Project name]`, `YYYY-MM-DD`, `@handle`) outside `_template-*` files (HTML comments ignored) | error (warning with `--allow-placeholders`) |
| `AGENTS.md` commands block with no runnable command | error (warning with `--allow-placeholders`) |
| Docs past their freshness window (rules in `00-index.md`) | warning |
| File name not starting with its ID; REQ file missing from the index | warning |
| Asset file (anything in `kb/` that isn't Markdown) with a space or underscore in its name — use hyphens | warning |

Exit code is 1 on errors. Add `--strict` to fail on warnings too. Use `--allow-placeholders` while you are still filling in the template.

If a line legitimately shows a placeholder (an instructional example), end it with `<!-- kb-check: ignore -->`.

To run it in CI, copy [`.github/workflows/kb-check.yml`](.github/workflows/kb-check.yml). It runs on PRs that touch the KB, and every Monday.

- **During adoption** both runs use `--allow-placeholders`, so stale docs and leftover placeholders appear only as warnings in the log — the run stays green.
- **Once the template is filled in**, follow the comments in the workflow: drop `--allow-placeholders` from the PR run, and switch the Monday run to `--strict` so a doc that went stale fails the build.

The checker has its own tests: `python3 -m unittest discover -s kb/_tools -p 'test_*.py'`.
