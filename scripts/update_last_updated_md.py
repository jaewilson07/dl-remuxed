from __future__ import annotations

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LAST_UPDATED_RE = re.compile(r"^> Last updated: .*", re.IGNORECASE)


def get_git_last_date(path: Path) -> str | None:
    """Return last commit date (YYYY-MM-DD) for a file, or None if unavailable."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%as", "--", str(path)],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        return out or None
    except Exception:
        return None


def update_file(path: Path) -> bool:
    """Update or insert a `> Last updated: YYYY-MM-DD` line.

    Returns True if the file was modified.
    """
    original = path.read_text(encoding="utf-8").splitlines()
    lines = original[:]

    # Determine date: prefer git, fall back to today.
    last_date = get_git_last_date(path) or date.today().isoformat()
    marker = f"> Last updated: {last_date}"

    # Find frontmatter end (--- on its own line, twice) if present.
    frontmatter_end_idx = None
    if lines and lines[0].strip() == "---":
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                frontmatter_end_idx = idx
                break

    # Search for existing Last updated line.
    existing_idx = None
    for idx, line in enumerate(lines):
        if LAST_UPDATED_RE.match(line.strip()):
            existing_idx = idx
            break

    if existing_idx is not None:
        # Replace existing marker.
        lines[existing_idx] = marker
        marker_idx = existing_idx
    else:
        # Insert marker after frontmatter if present, else at top.
        insert_idx = 0
        if frontmatter_end_idx is not None:
            insert_idx = frontmatter_end_idx + 1
        # Avoid double blank lines before the marker.
        if insert_idx < len(lines) and lines[insert_idx].strip() == "":
            insert_idx += 1
        lines.insert(insert_idx, marker)
        marker_idx = insert_idx

    # Ensure there is exactly one blank line after the marker (if not EOF).
    next_idx = marker_idx + 1
    if next_idx < len(lines):
        if lines[next_idx].strip() != "":
            lines.insert(next_idx, "")

    if lines == original:
        return False

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    if len(argv) <= 1:
        # If no files passed, default to all tracked *.md under repo.
        result = subprocess.check_output(
            ["git", "ls-files", "*.md"], cwd=ROOT, text=True
        ).strip()
        files = [ROOT / p for p in result.splitlines() if p]
    else:
        files = [ROOT / p for p in argv[1:]]

    changed = False
    for path in files:
        if not path.is_file() or path.suffix.lower() != ".md":
            continue
        if update_file(path):
            changed = True
            print(f"updated last_updated in {path.relative_to(ROOT)}")

    return 1 if changed and len(argv) > 1 else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
