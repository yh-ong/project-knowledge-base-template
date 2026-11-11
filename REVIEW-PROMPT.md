# Review prompt for Codex

Run from this folder:

```bash
codex "$(cat REVIEW-PROMPT.md)"
```

---

You are reviewing a **project knowledge base template** (all Markdown) in this folder. Start with `README.md`, then `AGENTS.md`, then everything under `kb/`.

**Purpose of the template:** be copied into any software repo so that AI coding agents, developers, product people, and operations share one accurate picture of the project — improving roadmap clarity, requirement quality, and implementation speed, and keeping work aligned with goals.

Review it critically against these questions and give concrete, file-specific feedback:

1. **AI-agent usefulness** — Would an AI coding agent starting cold in a repo using this actually work faster and more correctly? Is `AGENTS.md` the right length and content? What is missing or noise?
2. **Traceability** — Is the GOAL → RM → REQ → SPEC → ADR/RUN ID chain clear, practical, and not too heavy for small teams?
3. **Requirements quality** — Does `_template-prd.md` force testable acceptance criteria and clear scope? Anything a PM would skip or misuse?
4. **Operations coverage** — Would an SRE/ops person find what they need (deploy, rollback, config, alerts, runbooks, DR)?
5. **Maintenance / doc rot** — Are the freshness rules (`last_reviewed`, Definition of Done, PR checklist) enough to keep it true over time?
6. **Overlap & bloat** — Any duplicated content between files, sections that should be cut, or files that should be merged?
7. **Gaps** — Anything important missing (e.g. security/threat model, API contracts, test data, onboarding, metrics)? Only suggest additions with high value.

**Output format:**
- Top 5 most important changes, ranked, each with the file and a concrete suggested edit.
- Then a short list of smaller nits.
- Do not rewrite the whole template; do not edit files unless asked.
