#!/usr/bin/env python3
"""Knowledge base checker.

Checks the KB (AGENTS.md + kb/) for the rules in kb/00-index.md:

  errors   — missing or wrongly typed front-matter fields, invalid status or
             severity, bad or duplicate IDs (in files and in the REQ index),
             invalid or future dates, broken relative links (inline and
             reference-style), REQ index out of sync or malformed, unfilled
             placeholders, no runnable command in the AGENTS.md commands block
  warnings — docs past their freshness window, file name not matching its ID,
             REQ files missing from the index

A line containing `<!-- kb-check: ignore -->` is skipped by the placeholder check
(use it for instructional examples that legitimately show a placeholder).

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
SEVERITIES = {"SEV1", "SEV2", "SEV3"}
LIST_FIELDS = {"implements", "links", "supersedes", "superseded_by"}  # all others are scalar

TYPES = {
    # type: required fields, allowed statuses, id regex
    "living": (["title", "owner", "status", "last_reviewed"], LIVING_STATUSES, None),
    "req": (["id", "title", "owner", "status", "priority", "source", "last_reviewed"],
            {"draft", "ready", "in-progress", "done", "dropped"}, r"REQ-\d{3,}"),
    "spec": (["id", "title", "owner", "status", "last_reviewed"],  # + implements or source
             {"draft", "approved", "in-progress", "done", "superseded"}, r"SPEC-\d{3,}[A-Z]?"),
    "adr": (["id", "title", "owner", "status", "date"],
            {"proposed", "accepted", "superseded", "deprecated", "rejected"}, r"ADR-\d{4}"),
    "runbook": (["id", "title", "owner", "status", "last_reviewed", "last_exercised"],
                {"active", "deprecated"}, r"RUN-\d{3,}"),
    "postmortem": (["id", "title", "owner", "status", "severity", "date"],
                   {"draft", "reviewed", "actions-complete"}, r"INC-\d{8}-\d{2}"),
}

# Freshness windows in days. See 00-index.md — keep the two in sync.
FRESHNESS = {
    "kb/07-status/current-state.md": 7,
    "kb/02-roadmap/roadmap.md": 31,      # set to your roadmap review cadence
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

FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,}).*?(?:^ {0,3}\1[`~]*[ \t]*$|\Z)", re.S | re.M)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*(<[^>\n]*>|[^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
REF_DEF_RE = re.compile(r"^ {0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?")   # [label]: target
IGNORE_MARK = "kb-check: ignore"


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
    """Minimal YAML front-matter parser: flat `key: value`, inline `[a, b]` lists,
    and block lists (`key:` followed by `- item` lines).

    Returns (dict, body_start_line) or (None, 0) if there is no front-matter.
    """
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, 0
    data = {}
    last_key = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return data, i + 1
        item = re.match(r"^\s*-\s+(.*)$", line)
        if item and last_key is not None and (data[last_key] == ""
                                              or isinstance(data[last_key], list)):
            if not isinstance(data[last_key], list):
                data[last_key] = []
            value = strip_comment(item.group(1)).strip("\"'")
            if value:
                data[last_key].append(value)
            continue
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = strip_comment(value.strip())
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
        else:
            value = value.strip("\"'")
        last_key = key.strip()
        data[last_key] = value
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

        wrong_type = set()
        for field, value in list(fm.items()):
            if isinstance(value, list) and field not in LIST_FIELDS:
                r.error(rel, f"front-matter field '{field}' must be a single value, not a list")
                wrong_type.add(field)
                fm[field] = ""

        for field in required:
            if field not in wrong_type and fm.get(field) in (None, "", []):
                r.error(rel, f"front-matter field '{field}' is missing or empty")
        if kind == "spec" and not fm.get("implements") and not fm.get("source"):
            r.error(rel, "spec needs 'implements' (REQ ids) or 'source' "
                         "(maintenance source: INC, ticket, known issue)")

        status = fm.get("status", "")
        if status and status not in statuses:
            r.error(rel, f"status '{status}' not allowed for {kind} docs "
                         f"(allowed: {', '.join(sorted(statuses))})")

        severity = fm.get("severity", "")
        if kind == "postmortem" and severity and severity not in SEVERITIES:
            r.error(rel, f"severity '{severity}' not allowed "
                         f"(allowed: {', '.join(sorted(SEVERITIES))})")

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
            if not value or value == "YYYY-MM-DD":
                continue
            date = parse_date(value)
            if date is None:
                r.error(rel, f"{field} '{value}' is not a valid YYYY-MM-DD date")
                bad_dates.add(field)
            elif date > today:
                r.error(rel, f"{field} {value} is in the future")
                bad_dates.add(field)

        check_freshness(r, rel, kind, fm, today, bad_dates)

    # --- links ------------------------------------------------------------------
    for path in link_files:
        rel = path.relative_to(root).as_posix()
        prose = prose_only(path.read_text(encoding="utf-8"))
        for lineno, line in enumerate(prose.split("\n"), start=1):
            targets = LINK_RE.findall(line)
            ref_def = REF_DEF_RE.match(line)
            if ref_def:
                targets.append(ref_def.group(1))
            for target in targets:
                target = target.strip("<>")
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
        raw = path.read_text(encoding="utf-8")
        ignored = {n for n, line in enumerate(raw.split("\n"), start=1) if IGNORE_MARK in line}
        # Ignore guidance in HTML comments; check everything else, including code.
        text = blank_out(COMMENT_RE, raw)
        for lineno, line in enumerate(text.split("\n"), start=1):
            if lineno in ignored:
                continue
            found = [label for pat, label in PLACEHOLDERS if pat.search(line)]
            if found:
                msg = f"unfilled placeholder {', '.join(found)}"
                (r.warn if allow_placeholders else r.error)(f"{rel}:{lineno}", msg)

    # --- AGENTS.md commands block ---------------------------------------------------
    check_commands(r, agents, allow_placeholders)

    # --- requirements index vs. front-matter -------------------------------------
    check_req_index(r, root, req_status)
    return r


def check_commands(r, agents, allow_placeholders):
    """The canonical commands block must contain at least one runnable line."""
    if not agents.exists():
        r.warn("AGENTS.md", "not found — agents have no entry point")
        return
    text = agents.read_text(encoding="utf-8")
    section = re.search(r"^##[^\n]*\bCommands\b[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not section:
        r.warn("AGENTS.md", "no '## … Commands' section found")
        return
    block = FENCE_RE.search(section.group(1))
    lines = block.group(0).strip().split("\n")[1:-1] if block else []
    if not any(l.strip() and not l.strip().startswith("#") for l in lines):
        report = r.warn if allow_placeholders else r.error
        report("AGENTS.md", "Commands section has no runnable command (empty or comments only)")


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
    if age > window:
        r.warn(rel, f"stale: {field} {value} is {age} days old (window {window} days)")


def split_table_row(line):
    """Split a Markdown table row on unescaped pipes; drop the outer empty cells."""
    cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())]
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return cells


def check_req_index(r, root, req_status):
    index = root / "kb/03-requirements/index.md"
    if not index.exists():
        if req_status:
            r.error("kb/03-requirements/index.md", "missing, but REQ files exist")
        return
    rel = index.relative_to(root).as_posix()
    listed = {}
    header = None
    index_text = index.read_text(encoding="utf-8")
    for pattern in (FENCE_RE, COMMENT_RE):   # examples are not real rows
        index_text = blank_out(pattern, index_text)
    for lineno, line in enumerate(index_text.split("\n"), start=1):
        if not line.strip().startswith("|"):
            header = None
            continue
        cells = split_table_row(line)
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue  # separator row
        if "id" not in header or "status" not in header:
            continue
        if len(cells) != len(header):
            r.error(f"{rel}:{lineno}", f"malformed table row: expected {len(header)} "
                                       f"cells, found {len(cells)}")
            continue
        if not any(cells):
            continue  # empty row
        m = re.search(r"REQ-\w+", cells[header.index("id")])
        if not m or not re.fullmatch(r"REQ-\d{3,}", m.group(0)):
            shown = m.group(0) if m else cells[header.index("id")]
            r.error(f"{rel}:{lineno}", f"invalid REQ id '{shown}' in index row "
                                       f"(expected REQ-nnn)")
            continue
        if m.group(0) in listed:
            r.error(f"{rel}:{lineno}", f"{m.group(0)} is listed more than once "
                                       f"(first on line {listed[m.group(0)][1]})")
            continue
        listed[m.group(0)] = (cells[header.index("status")].strip("` "), lineno)

    for req_id, (status, lineno) in listed.items():
        if req_id not in req_status:
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
