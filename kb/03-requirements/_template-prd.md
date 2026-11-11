---
id: REQ-000
title: <feature name>
owner: "@handle"
status: draft            # draft | ready | in-progress | done | dropped  (see index.md)
priority: P1             # P0 must-have | P1 should | P2 nice
source: RM-00            # product work: RM-xx · maintenance: INC-…, ticket link, or known issue
last_reviewed: YYYY-MM-DD
links: []                # SPEC-xxx, ADR-xxxx, threat model, designs, tickets
---

# REQ-000 — <feature name>

## 1. Problem & why now
<!-- 2–4 sentences. Who hurts, how much, and why this beats the alternatives on the roadmap. -->

## 2. Users & scenarios
<!-- Concrete stories. "As a <user>, I want <action> so that <outcome>." -->
1. As a …, I want … so that …

## 3. Scope
**In scope**
- …

**Out of scope** (explicit — implementers and AI agents must not build these)
- …

## 4. Functional requirements
<!-- Every "must" row needs at least one acceptance criterion. -->
| # | Requirement | Priority | Covered by |
|---|---|---|---|
| F1 | The system shall … | must | AC1, AC3 |
| F2 | | should | AC2 |

## 5. Acceptance criteria
<!-- Testable. Given/When/Then. This is the definition of done. -->
- **AC1** Given …, when …, then …
- **AC2** Given …, when …, then …

## 6. Edge cases & error handling
<!-- Each row must either point to an AC or be listed as out of scope. No silent "TBD". -->
| Case | Expected behaviour | AC / out of scope |
|---|---|---|
| Empty / invalid input | | |
| Concurrent update | | |
| Dependency down / timeout | | |
| Permission denied | | |

## 7. Non-functional requirements
<!-- Numbers, not adjectives. Each row is quantified or "N/A — <reason>". -->
| Aspect | Requirement |
|---|---|
| Performance | p95 < … ms at … rps |
| Availability | |
| Security / privacy | PII involved? auth model? |
| Accessibility | |
| Localisation | |
| Audit / compliance | |

**Threat model required** if this work changes authentication, authorisation, external entry points, money movement, or sensitive data. Link it in `links`.

## 8. Data & integrations
<!-- New data stored, events emitted/consumed, external APIs touched. Point to the machine-readable contract (OpenAPI, protobuf, event schema) instead of copying it. -->

## 9. UX & design
<!-- How the feature will look and behave. Write "N/A — no UI" for backend-only work. -->
- **Design reference** — one of:
  - a mockup: <!-- Figma frame / image in the repo. Link the exact frame, not the whole file. --> …
  - an existing screen or component to follow, plus the changes in words: <!-- fine for small changes and teams without a designer --> …
- **Status:** exploring / agreed · **Agreed by:** `@…` <!-- a named owner; need not be a designer -->
- **Viewports to verify:** e.g. 375 / 768 / 1280 px

**User flow** <!-- numbered steps or a diagram: entry point → screens → exit -->
1. …

**Screens & states** <!-- every screen, and each standard state that applies -->
| Screen / component | Default | Loading | Empty | Error | Success | Disabled / read-only / no permission | Notes |
|---|---|---|---|---|---|---|---|
| | link | link / std / n/a | link / std / n/a | link / std / n/a | link / std / n/a | link / std / n/a | |

`std` = uses the standard treatment in [`design-system.md` §6](../08-design/design-system.md) unchanged, so no separate design is needed. `n/a` = the state can't occur.

- **Responsive behaviour:** <!-- what changes on mobile / tablet -->
- **Copy:** <!-- final text for headings, buttons, errors — or link to it -->
- **New or changed components:** <!-- none, or list them; new ones must be added to design-system.md -->
- **Deviations from the design system:** <!-- none, or what and why -->

## 10. Rollout & measurement
- **Rollout:** feature flag / % rollout / big bang
- **Success metric:** … · **Baseline:** … · **Target:** …
- **Measurement window:** e.g. 2 weeks after 100% rollout · **Metric owner:** …
- **Guardrail metric** (must not get worse): …
- **Rollback trigger:** …

## 11. Open questions
| Question | Blocking? | Owner | Due | Answer |
|---|---|---|---|---|
| | yes / no | | | |

## 12. Ready-to-build checklist
<!-- Status may only move to `ready` when all are ticked. -->
- [ ] Every `must` functional requirement maps to at least one AC
- [ ] Every edge case maps to an AC or is explicitly out of scope
- [ ] NFRs quantified or marked `N/A` with a reason
- [ ] Threat model linked, if required (§7)
- [ ] Design reference agreed by a named owner and covers every screen and applicable state (§9), or "N/A — no UI"
- [ ] Dependencies on other teams/systems identified
- [ ] Rollout, success metric, and rollback trigger defined
- [ ] No blocking open questions

## 13. Scope decisions
<!-- Only material changes to scope or acceptance criteria, and why. Git history covers the rest. -->
| Date | Decision | By |
|---|---|---|
| | | |
