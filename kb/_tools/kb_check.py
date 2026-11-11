#!/usr/bin/env python3
"""Knowledge base checker.

Checks the KB (AGENTS.md + kb/) for the rules in kb/00-index.md:

  errors   — missing front-matter fields, invalid status, bad or duplicate IDs,
             broken relative links, REQ index out of sync, unfilled placeholders
  warnings — docs past their freshness window, file name not matching its ID,
             REQ files missing from the index

Exit code 1 if there are errors (or warnings with --strict), else 0.
Standard library only; Python 3.8+.

Usage:
  python3 kb/_tools/kb_check.py                     # from repo root
  python3 kb/_tools/kb_check.py --root path/to/repo
  python3 kb/_tools/kb_check.py --allow-placeholders  # while still filling in the template
  python3 kb/_tools/kb_check.py --strict            # warnings fail too
"""

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- rules ----

LIVING_STATUSES = {"draft", "active", "deprecated"}

TYPES = {
    # type: required fields, allowed statuses, id regex
    "living": (["title", "owner", "status", "last_reviewed"], LIVING_STATUSES, None),
    "req": (["id", "title", "owner", "status", "priority", "source", "last_reviewed"],
            {"draft", "ready", "in-progress", "done", "dropped"}, r"REQ-\d{3,}"),
    "spec": (["id", "title", "owner", "status", "implements", "last_reviewed"],
             {"draft", "approved", "in-progress", "done", "superseded"}, r"SPEC-\d{3,}[A-Z]?"),
    "adr": (["id", "title", "owner", "status", "date"],
            {"proposed", "accepted", "superseded", "deprecated", "rejected"}, r"ADR-\d{4}"),
    "runbook": (["id", "title", "owner", "status", "last_reviewed", "last_exercised"],
                {"active", "deprecated"}, r"RUN-\d{3,}"),
    "postmortem": (["id", "title", "owner", "status", "severity", "date"],
                   {"draft", "reviewed", "actions-complete"}, r"INC-\d{8}-\d{2}"),
}

# Freshness windows in days (None = historical, never stale). See 00-index.md.
FRESHNESS = {
    "kb/07-status/current-state.md": 7,
    "kb/02-roadmap/roadmap.md": 31,
    "kb/06-operations/environments.md": 92,
}
DEFAULT_LIVING_DAYS = 90
ACTIVE_WORK_DAYS = 30            # REQ ready/in-progress, SPEC approved/in-progress
RUNBOOK_REVIEW_DAYS = 92
RUNBOOK_EXERCISE_DAYS = 183

PLACEHOLDERS = [
    (re.compile(r"…"), "…"),
    (re.compile(r"\[Project name\]"), "[Project name]"),
    (re.compile(r"YYYY-MM-DD"), "YYYY-MM-DD"),
    (re.compile(r"@handle\b"), "@handle"),
]

# -------------------------------------------------------------- parsing ----

FENCE_RE = re.compile(r"^(```|~~~).*?^\1\s*$", re.S | re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def blank_out(pattern, text):
    """Replace matches with spaces/newlines so line numbers stay correct."""
    return pattern.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)


def prose_only(text):
    """Text with code blocks, inline code and HTML comments removed."""
    for pat in (FENCE_RE, COMMENT_RE, INLINE_CODE_RE):
        text = blank_out(pat, text)
    return text


def strip_comment(value):
    """Remove a trailing ' # comment' that is not inside quotes."""
    in_quote = None
    for i, ch in enumerate(value):
        if ch in "\"'":
            in_quote = None if in_quote == ch else (in_quote or ch)
        elif ch == "#" and in_quote is None and (i == 0 or value[i - 1].isspace()):
            return value[:i].rstrip()
    return value.strip()


def parse_front_matter(text):
    """Minimal YAML front-matter parser: flat `key: value` and `[a, b]` lists.

    Returns (dict, body_start_line) or (None, 0) if there is no front-matter.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, 0
    data = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return data, i + 1
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = strip_comment(value.strip())
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        else:
            value = value.strip("\"'")
        data[key.strip()] = value
    return None, 0  # unterminated


def doc_type(rel):
    parts = rel.split("/")
    name = parts[-1]
    if rel.startswith("kb/03-requirements/") and name.startswith("REQ-"):
        return "req"
    if rel.startswith("kb/05-implementation/specs/"):
        return "spec"
    if rel.startswith("kb/04-architecture/adr/"):
        return "adr"
    if rel.startswith("kb/06-operations/runbooks/"):
        return "runbook"
    if rel.startswith("kb/06-operations/postmortems/"):
        return "postmortem"
    return "living"


def parse_date(value):
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


# --------------------------------------------------------------- checker ----

class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def check(root, today, allow_placeholders):
    r = Report()
    kb = root / "kb"
    if not kb.is_dir():
        r.error(str(root), "no kb/ directory found (use --root)")
        return r

    files = sorted(p for p in kb.rglob("*.md") if "_tools" not in p.parts)
    agents = root / "AGENTS.md"
    link_files = files + ([agents] if agents.exists() else [])
    placeholder_files = [p for p in link_files if not p.name.startswith("_template-")]

    ids = {}            # id -> rel path
    req_status = {}     # REQ id -> status from front-matter

    # --- front-matter, status, IDs, freshness -------------------------------
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.name.startswith("_template-"):
            continue
        text = path.read_text(encoding="utf-8")
        fm, _ = parse_front_matter(text)
        if fm is None:
            r.error(rel, "missing or unterminated front-matter")
            continue

        kind = doc_type(rel)
        required, statuses, id_re = TYPES[kind]

        for field in required:
            if fm.get(field) in (None, "", []):
                r.error(rel, f"front-matter field '{field}' is missing or empty")

        status = fm.get("status", "")
        if status and status not in statuses:
            r.error(rel, f"status '{status}' not allowed for {kind} docs "
                         f"(allowed: {', '.join(sorted(statuses))})")

        doc_id = fm.get("id")
        if id_re and doc_id:
            if not re.fullmatch(id_re, doc_id):
                r.error(rel, f"id '{doc_id}' does not match pattern {id_re}")
            elif not path.stem.startswith(doc_id):
                r.warn(rel, f"file name should start with its id '{doc_id}'")
        if doc_id:
            if doc_id in ids:
                r.error(rel, f"duplicate id '{doc_id}' (also in {ids[doc_id]})")
            else:
                ids[doc_id] = rel
                if kind == "req":
                    req_status[doc_id] = status

        bad_dates = set()
        for field in ("last_reviewed", "last_exercised", "date"):
            value = fm.get(field)
            if value and value != "YYYY-MM-DD" and parse_date(value) is None:
                r.error(rel, f"{field} '{value}' is not a valid YYYY-MM-DD date")
                bad_dates.add(field)

        check_freshness(r, rel, kind, fm, today, bad_dates)

    # --- links ------------------------------------------------------------------
    for path in link_files:
        rel = path.relative_to(root).as_posix()
        prose = prose_only(path.read_text(encoding="utf-8"))
        for lineno, line in enumerate(prose.split("\n"), start=1):
            for target in LINK_RE.findall(line):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
                    continue  # external URL, mailto, or in-page anchor
                target_path = target.split("#", 1)[0]
                if not target_path:
                    continue
                if not (path.parent / target_path).resolve().exists():
                    r.error(f"{rel}:{lineno}", f"broken link → {target}")

    # --- placeholders -------------------------------------------------------------
    for path in placeholder_files:
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        # Ignore guidance in HTML comments; check everything else, including code.
        text = blank_out(COMMENT_RE, text)
        for lineno, line in enumerate(text.split("\n"), start=1):
            found = [label for pat, label in PLACEHOLDERS if pat.search(line)]
            if found:
                msg = f"unfilled placeholder {', '.join(found)}"
                (r.warn if allow_placeholders else r.error)(f"{rel}:{lineno}", msg)

    # --- requirements index vs. front-matter -------------------------------------
    check_req_index(r, root, req_status)
    return r


def check_freshness(r, rel, kind, fm, today, bad_dates):
    status = fm.get("status", "")
    if kind in ("adr", "postmortem") or status in ("deprecated", "superseded"):
        return  # historical records never expire
    if kind == "req" and status not in ("ready", "in-progress"):
        return
    if kind == "spec" and status not in ("approved", "in-progress"):
        return

    if kind in ("req", "spec"):
        window = ACTIVE_WORK_DAYS
    elif kind == "runbook":
        window = RUNBOOK_REVIEW_DAYS
    else:
        window = FRESHNESS.get(rel, DEFAULT_LIVING_DAYS)

    checks = [("last_reviewed", window)]
    if kind == "runbook":
        checks.append(("last_exercised", RUNBOOK_EXERCISE_DAYS))
    for field, days in checks:
        if field not in bad_dates:
            stale_check(r, rel, field, fm.get(field), days, today)


def stale_check(r, rel, field, value, window, today):
    date = parse_date(value) if value else None
    if date is None:
        return  # missing, placeholder, or invalid — reported by other checks
    age = (today - date).days
    if age < 0:
        r.error(rel, f"{field} {value} is in the future")
    elif age > window:
        r.warn(rel, f"stale: {field} {value} is {age} days old (window {window} days)")


def check_req_index(r, root, req_status):
    index = root / "kb/03-requirements/index.md"
    if not index.exists():
        if req_status:
            r.error("kb/03-requirements/index.md", "missing, but REQ files exist")
        return
    rel = index.relative_to(root).as_posix()
    listed = {}
    header = None
    for lineno, line in enumerate(index.read_text(encoding="utf-8").split("\n"), start=1):
        if not line.strip().startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue  # separator row
        if "id" not in header or "status" not in header:
            continue
        m = re.search(r"REQ-\d{3,}", cells[header.index("id")])
        if not m:
            continue
        listed[m.group(0)] = (cells[header.index("status")].strip("` "), lineno)

    for req_id, (status, lineno) in listed.items():
        if req_id not in req_status:
            # An index row for a REQ with no file is only OK for the template's example row.
            if req_status:
                r.error(f"{rel}:{lineno}", f"{req_id} is listed but has no REQ file")
        elif status != req_status[req_id]:
            r.error(f"{rel}:{lineno}", f"{req_id} status '{status}' ≠ front-matter "
                                       f"'{req_status[req_id]}'")
    for req_id in req_status:
        if req_id not in listed:
            r.warn(rel, f"{req_id} has a file but is not listed in the index")


# ------------------------------------------------------------------ main ----

def main(argv=None):
    ap = argparse.ArgumentParser(description="Check the project knowledge base.")
    ap.add_argument("--root", default=".", help="repo root containing AGENTS.md and kb/")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for testing")
    ap.add_argument("--allow-placeholders", action="store_true",
                    help="report unfilled placeholders as warnings, not errors")
    ap.add_argument("--strict", action="store_true", help="treat warnings as errors")
    args = ap.parse_args(argv)

    today = parse_date(args.today) if args.today else dt.date.today()
    if today is None:
        ap.error("--today must be YYYY-MM-DD")

    report = check(Path(args.root).resolve(), today, args.allow_placeholders)

    for msg in report.errors:
        print(f"ERROR   {msg}")
    for msg in report.warnings:
        print(f"WARN    {msg}")
    print(f"\n{len(report.errors)} error(s), {len(report.warnings)} warning(s)")

    failed = report.errors or (args.strict and report.warnings)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
