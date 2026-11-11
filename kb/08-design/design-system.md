---
title: Design System & UI Style
owner: "@design-lead"
status: draft
last_reviewed: YYYY-MM-DD
---

# Design System & UI Style

> How the product looks, feels, and reads — so every feature (built by a human or an AI agent) looks like it belongs.
> Per-feature screens and flows live in each REQ's "UX & design" section, not here.

## 1. Sources of truth
<!-- Link, don't copy. Values pasted here will drift. -->
| What | Where |
|---|---|
| Design files (Figma / other) | `…` |
| Design tokens in code (colours, spacing, type) | `…` e.g. `src/styles/tokens.css` |
| Component library in code | `…` e.g. `src/components/ui/` |
| Component previews (Storybook / other) | `…` |
| Icons / illustrations / logo | `…` |
| Screenshots and reference images used in this KB | `kb/assets/` — hyphenated lowercase names, e.g. `checkout-error-state.png` (see [file naming](../00-index.md#file-naming)) |

**If design file and code disagree:** `…` wins. <!-- pick one: usually the tokens in code -->

## 2. Look & feel
<!-- 3–5 adjectives and what they mean in practice. Add 1–2 reference screenshots of screens that "get it right". -->
- **…** — e.g. *Calm*: lots of whitespace, one primary action per screen.

## 3. Foundations
<!-- Summarise the rules; the exact values live in the tokens file. -->
| Foundation | Rule |
|---|---|
| Colour | Roles, not hex: `primary`, `surface`, `danger`… Never hard-code a colour. Light / dark mode: … |
| Typography | Font(s): … · Scale: … · Max line length: … |
| Spacing | Scale: e.g. 4 / 8 / 12 / 16 / 24 / 32. Never use off-scale values. |
| Radius / shadow / borders | … |
| Icons | Set: … · Sizes: … |
| Motion | Durations: … · When to animate / when not to: … |

## 4. Layout
- **Breakpoints:** … (mobile / tablet / desktop)
- **Grid & max content width:** …
- **Page templates:** list / detail / form / dashboard / empty — link to an example of each
- **Navigation pattern:** …

## 5. Components
<!-- Rule: reuse before you build. List what exists so nobody (or no agent) invents a second button. -->
| Component | Use it for | Don't use it for | Code | Design |
|---|---|---|---|---|
| Button (primary / secondary / danger) | | | | |
| Form field + validation message | | | | |
| Modal / drawer | | | | |
| Table / list | | | | |
| Toast / banner | | | | |

**Adding a new component:** <!-- who approves, where it goes, what it must include (states, a11y, preview) --> …

## 6. Standard states
Every screen and component must define these — the REQ's design must show each one that applies.

| State | Standard treatment |
|---|---|
| Loading | skeleton / spinner rule: … |
| Empty | illustration? message + primary action: … |
| Error | inline vs. banner vs. full page: … |
| Success | toast / inline confirmation: … |
| Disabled / read-only / no permission | … |

## 7. Content & voice
- **Tone:** …
- **Capitalisation:** e.g. sentence case for buttons and headings
- **Dates, numbers, currency:** …
- **Error messages:** say what happened + what to do next; never blame the user
- **Terminology:** use the words in [`glossary.md`](../01-context/glossary.md)

## 8. Accessibility
- **Target:** e.g. WCAG 2.2 AA
- **Musts:** keyboard reachable, visible focus, colour contrast ≥ 4.5:1, labels on inputs, alt text, touch targets ≥ 44 px
- **How we test:** …

## 9. Do / don't
<!-- Real examples from this product beat generic advice. Screenshots welcome. -->
| Do | Don't |
|---|---|
| | |
