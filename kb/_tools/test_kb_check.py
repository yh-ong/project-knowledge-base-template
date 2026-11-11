#!/usr/bin/env python3
"""Regression tests for kb_check.py.

Run:  python3 -m unittest discover -s kb/_tools -p 'test_*.py'
"""

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import kb_check  # noqa: E402

TODAY = dt.date(2026, 11, 12)

AGENTS_OK = """# Agents

## 3. Commands
```bash
# install
npm ci
```

## 4. Rules
"""

LIVING = """---
title: {title}
owner: "@ana"
status: active
last_reviewed: {date}
---
Body.
"""

REQ = """---
id: {id}
title: Login
owner: "@ana"
status: {status}
priority: P0
source: RM-01
last_reviewed: {date}
---
"""

INDEX = """---
title: Index
owner: "@ana"
status: active
last_reviewed: 2026-11-10
---
| ID | Title | Status |
|---|---|---|
{rows}
"""


class KbCheckTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.write("AGENTS.md", AGENTS_OK)
        self.write("kb/07-status/current-state.md",
                   LIVING.format(title="Current State", date="2026-11-10"))
        self.write("kb/03-requirements/index.md", INDEX.format(rows=""))

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_check(self, allow_placeholders=False):
        return kb_check.check(self.root, TODAY, allow_placeholders)

    def assertHasError(self, report, fragment):
        self.assertTrue(any(fragment in e for e in report.errors),
                        f"expected an error containing {fragment!r}, got {report.errors}")

    # --- baseline -------------------------------------------------------------

    def test_clean_kb_passes(self):
        report = self.run_check()
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    # --- dates ----------------------------------------------------------------

    def test_future_date_on_accepted_adr_is_error(self):
        self.write("kb/04-architecture/adr/ADR-0001-pg.md", """---
id: ADR-0001
title: Use Postgres
owner: "@ana"
status: accepted
date: 2099-01-01
---
""")
        self.assertHasError(self.run_check(), "date 2099-01-01 is in the future")

    def test_future_review_date_on_done_req_is_error(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="REQ-001", status="done", date="2099-01-01"))
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="| REQ-001 | Login | done |"))
        self.assertHasError(self.run_check(), "last_reviewed 2099-01-01 is in the future")

    def test_invalid_date_is_error_even_when_not_in_freshness_window(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="REQ-001", status="done", date="2026-13-01"))
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="| REQ-001 | Login | done |"))
        self.assertHasError(self.run_check(), "not a valid YYYY-MM-DD date")

    def test_old_accepted_adr_is_not_stale(self):
        self.write("kb/04-architecture/adr/ADR-0001-pg.md", """---
id: ADR-0001
title: Use Postgres
owner: "@ana"
status: accepted
date: 2019-01-01
---
""")
        report = self.run_check()
        self.assertEqual(report.errors, [])
        self.assertEqual(report.warnings, [])

    def test_stale_current_state_is_warning(self):
        self.write("kb/07-status/current-state.md",
                   LIVING.format(title="Current State", date="2026-10-01"))
        report = self.run_check()
        self.assertEqual(report.errors, [])
        self.assertTrue(any("stale" in w for w in report.warnings))

    # --- requirements index ---------------------------------------------------

    def test_index_row_without_any_req_files_is_error(self):
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="| REQ-999 | Ghost | draft |"))
        self.assertHasError(self.run_check(), "REQ-999 is listed but has no REQ file")

    def test_short_index_row_reports_malformed_and_does_not_crash(self):
        self.write("kb/03-requirements/index.md", INDEX.format(rows="| REQ-999 |"))
        self.assertHasError(self.run_check(), "malformed table row")

    def test_index_row_inside_html_comment_is_ignored(self):
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="\n<!-- example:\n| REQ-999 | Ghost | draft |\n-->"))
        self.assertEqual(self.run_check().errors, [])

    def test_index_status_mismatch_is_error(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="REQ-001", status="ready", date="2026-11-10"))
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="| REQ-001 | Login | in-progress |"))
        self.assertHasError(self.run_check(), "REQ-001 status 'in-progress'")

    def test_duplicate_id_keeps_first_status_for_index_comparison(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="REQ-001", status="ready", date="2026-11-10"))
        self.write("kb/03-requirements/REQ-002-dup.md",
                   REQ.format(id="REQ-001", status="draft", date="2026-11-10"))
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="| REQ-001 | Login | ready |"))
        report = self.run_check()
        self.assertHasError(report, "duplicate id 'REQ-001'")
        self.assertFalse(any("≠" in e for e in report.errors), report.errors)

    def test_malformed_index_id_is_error(self):
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="| REQ-99 | Ghost | draft |"))
        self.assertHasError(self.run_check(), "invalid REQ id 'REQ-99'")

    def test_duplicate_index_rows_are_error(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="REQ-001", status="ready", date="2026-11-10"))
        self.write("kb/03-requirements/index.md", INDEX.format(
            rows="| REQ-001 | Login | draft |\n| REQ-001 | Login | ready |"))
        self.assertHasError(self.run_check(), "REQ-001 is listed more than once")

    def test_escaped_pipe_in_index_title_is_fine(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="REQ-001", status="ready", date="2026-11-10"))
        self.write("kb/03-requirements/index.md",
                   INDEX.format(rows="| REQ-001 | A \\| B | ready |"))
        self.assertEqual(self.run_check().errors, [])

    def test_fenced_example_rows_in_index_are_ignored(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="REQ-001", status="ready", date="2026-11-10"))
        self.write("kb/03-requirements/index.md", INDEX.format(
            rows="| REQ-001 | Login | ready |\n\nExample:\n\n```md\n"
                 "| ID | Title | Status |\n|---|---|---|\n"
                 "| REQ-999 | Ghost | draft |\n| REQ-001 | Login | draft |\n```"))
        self.assertEqual(self.run_check().errors, [])

    # --- front-matter types ---------------------------------------------------

    def test_block_list_front_matter_is_read(self):
        self.write("kb/05-implementation/specs/SPEC-001-design.md", """---
id: SPEC-001
title: Design
owner: "@ana"
status: draft
last_reviewed: 2026-11-10
implements:
  - REQ-001   # login
  - "REQ-002"
links:
  - ADR-0001
---
""")
        self.assertEqual(self.run_check().errors, [])
        fm, _ = kb_check.parse_front_matter(
            "---\nimplements:\n  - REQ-001   # login\n  - \"REQ-002\"\nowner: x\n---\n")
        self.assertEqual(fm, {"implements": ["REQ-001", "REQ-002"], "owner": "x"})

    def test_block_list_on_scalar_field_is_error(self):
        self.write("kb/01-context/glossary.md", """---
title: Glossary
owner: "@ana"
status:
  - active
last_reviewed: 2026-11-10
---
""")
        self.assertHasError(self.run_check(), "'status' must be a single value, not a list")

    def test_list_valued_scalar_field_is_error_not_crash(self):
        self.write("kb/01-context/glossary.md", """---
title: Glossary
owner: "@ana"
status: [active]
last_reviewed: 2026-11-10
---
""")
        report = self.run_check()
        self.assertHasError(report, "'status' must be a single value, not a list")
        self.assertEqual(len(report.errors), 1, report.errors)

    def test_list_valued_id_is_error_not_crash(self):
        self.write("kb/03-requirements/REQ-001-login.md",
                   REQ.format(id="[REQ-001, REQ-002]", status="draft", date="2026-11-10"))
        self.assertHasError(self.run_check(), "'id' must be a single value, not a list")

    def test_postmortem_severity_must_be_on_the_scale(self):
        pm = """---
id: INC-20261103-01
title: DB failover
owner: "@ana"
status: draft
severity: {sev}
date: 2026-11-03
---
"""
        path = "kb/06-operations/postmortems/INC-20261103-01-db-failover.md"
        self.write(path, pm.format(sev="SEV2"))
        self.assertEqual(self.run_check().errors, [])
        self.write(path, pm.format(sev="P1"))
        self.assertHasError(self.run_check(), "severity 'P1' not allowed")

    # --- placeholders and commands --------------------------------------------

    def test_placeholder_is_error_and_warning_when_allowed(self):
        self.write("kb/01-context/glossary.md",
                   LIVING.format(title="Glossary", date="2026-11-10") + "Owner: @handle\n")
        self.assertHasError(self.run_check(), "unfilled placeholder @handle")
        report = self.run_check(allow_placeholders=True)
        self.assertEqual(report.errors, [])
        self.assertTrue(any("@handle" in w for w in report.warnings))

    def test_ignore_marker_skips_placeholder_line(self):
        self.write("kb/01-context/glossary.md",
                   LIVING.format(title="Glossary", date="2026-11-10")
                   + "Example owner: @handle <!-- kb-check: ignore -->\n")
        self.assertEqual(self.run_check().errors, [])

    def test_placeholder_in_html_comment_and_template_is_ignored(self):
        self.write("kb/01-context/glossary.md",
                   LIVING.format(title="Glossary", date="2026-11-10") + "<!-- e.g. … -->\n")
        self.write("kb/03-requirements/_template-prd.md", "owner: @handle …\n")
        self.assertEqual(self.run_check().errors, [])

    def test_comment_only_commands_block_is_error(self):
        self.write("AGENTS.md", "# Agents\n\n## 3. Commands\n```bash\n# install\n# test\n```\n")
        self.assertHasError(self.run_check(), "no runnable command")
        self.assertEqual(self.run_check(allow_placeholders=True).errors, [])

    # --- links ----------------------------------------------------------------

    def test_broken_inline_and_reference_links_are_errors(self):
        self.write("kb/01-context/glossary.md",
                   LIVING.format(title="Glossary", date="2026-11-10")
                   + "See [a](missing-inline.md) and [b][ref].\n\n[ref]: missing-ref.md\n")
        report = self.run_check()
        self.assertHasError(report, "missing-inline.md")
        self.assertHasError(report, "missing-ref.md")

    def test_valid_external_anchor_and_code_links_are_fine(self):
        self.write("kb/01-context/glossary.md",
                   LIVING.format(title="Glossary", date="2026-11-10")
                   + "[web](https://example.com) [top](#glossary) "
                     "[state](../07-status/current-state.md#focus) `[x](nope.md)`\n\n"
                     "[ref]: https://example.com\n")
        self.assertEqual(self.run_check().errors, [])

    def test_angle_bracket_link_destination_is_resolved(self):
        self.write("kb/01-context/glossary.md",
                   LIVING.format(title="Glossary", date="2026-11-10")
                   + "[state](<../07-status/current-state.md>) [gone](<nope.md>)\n")
        report = self.run_check()
        self.assertEqual(len(report.errors), 1, report.errors)
        self.assertHasError(report, "nope.md")

    def test_indented_and_long_fences_are_not_scanned_for_links(self):
        self.write("kb/01-context/glossary.md",
                   LIVING.format(title="Glossary", date="2026-11-10")
                   + "- item\n\n  ```md\n  [x](nope-indented.md)\n  ```\n\n"
                     "````md\n```\n[y](nope-nested.md)\n```\n````\n\n"
                     "~~~\n[z](nope-tilde.md)\n~~~\n")
        self.assertEqual(self.run_check().errors, [])

    # --- specs ----------------------------------------------------------------

    def _spec(self, extra):
        return f"""---
id: SPEC-001
title: Design
owner: "@ana"
status: draft
last_reviewed: 2026-11-10
{extra}
---
"""

    def test_spec_accepts_implements_or_source_but_needs_one(self):
        path = "kb/05-implementation/specs/SPEC-001-design.md"
        self.write(path, self._spec("implements: [REQ-001]"))
        self.assertEqual(self.run_check().errors, [])
        self.write(path, self._spec("source: INC-20261103-01"))
        self.assertEqual(self.run_check().errors, [])
        self.write(path, self._spec("links: []"))
        self.assertHasError(self.run_check(), "spec needs 'implements'")


if __name__ == "__main__":
    unittest.main()
