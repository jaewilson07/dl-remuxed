"""Parse pre-commit errors and extract structured error list for fixing."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class LintError:
    """Represents a single linting error."""

    file_path: str
    line: Optional[int]
    column: Optional[int]
    error_code: str
    message: str
    context: str = ""
    hook: str = ""

    def __str__(self):
        loc = f"{self.file_path}"
        if self.line:
            loc += f":{self.line}"
        if self.column:
            loc += f":{self.column}"
        return f"[{self.hook}] {loc} - {self.error_code}: {self.message}"


def clean_text(text: str) -> str:
    """Remove null bytes and extra spaces from text."""
    return text.replace("\x00", "").strip()


def parse_precommit_errors(file_path: str) -> list[LintError]:
    """
    Parse pre-commit error file and extract structured errors.

    Args:
        file_path: Path to precommit_errors.txt file

    Returns:
        List of LintError objects
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean content
    content = clean_text(content)

    errors = []
    current_hook = None

    # Pattern for ruff errors: path:line:column: CODE message
    ruff_pattern = re.compile(
        r"([^:]+\.py):(\d+):(\d+):\s+([A-Z]\d+)\s+(.+?)(?=\n|$)"
    )

    # Pattern for YAML errors
    yaml_pattern = re.compile(r'in "([^"]+)", line (\d+), column (\d+)')

    lines = content.split("\n")

    for i, line in enumerate(lines):
        line = clean_text(line)

        # Detect current hook
        if "hook id:" in line.lower():
            hook_match = re.search(r"hook id:\s+(.+)", line, re.IGNORECASE)
            if hook_match:
                current_hook = hook_match.group(1).strip()

        # Parse ruff errors
        ruff_match = ruff_pattern.search(line)
        if ruff_match:
            file_path = ruff_match.group(1).replace("\\", "/")
            line_num = int(ruff_match.group(2))
            col_num = int(ruff_match.group(3))
            error_code = ruff_match.group(4)
            message = ruff_match.group(5).strip()

            # Collect context from following lines
            context_lines = []
            for j in range(i + 1, min(i + 10, len(lines))):
                ctx_line = clean_text(lines[j])
                if ctx_line and not ctx_line.startswith("src\\"):
                    if re.match(r"^\d+\s+\|", ctx_line):
                        context_lines.append(ctx_line)
                else:
                    break

            errors.append(
                LintError(
                    file_path=file_path,
                    line=line_num,
                    column=col_num,
                    error_code=error_code,
                    message=message,
                    context="\n".join(context_lines),
                    hook=current_hook or "ruff",
                )
            )

        # Parse YAML errors
        yaml_match = yaml_pattern.search(line)
        if yaml_match:
            file_path = yaml_match.group(1).strip()
            line_num = int(yaml_match.group(2))
            col_num = int(yaml_match.group(3))

            # Get error message from previous line
            message = ""
            if i > 0:
                message = clean_text(lines[i - 1])

            errors.append(
                LintError(
                    file_path=file_path,
                    line=line_num,
                    column=col_num,
                    error_code="YAML",
                    message=message,
                    hook=current_hook or "check-yaml",
                )
            )

    return errors


def group_errors_by_file(errors: list[LintError]) -> dict[str, list[LintError]]:
    """Group errors by file path."""
    grouped = {}
    for error in errors:
        if error.file_path not in grouped:
            grouped[error.file_path] = []
        grouped[error.file_path].append(error)
    return grouped


def group_errors_by_type(errors: list[LintError]) -> dict[str, list[LintError]]:
    """Group errors by error code."""
    grouped = {}
    for error in errors:
        if error.error_code not in grouped:
            grouped[error.error_code] = []
        grouped[error.error_code].append(error)
    return grouped


def print_summary(errors: list[LintError]):
    """Print error summary statistics."""
    print(f"\n{'=' * 80}")
    print(f"TOTAL ERRORS: {len(errors)}")
    print(f"{'=' * 80}\n")

    # Group by error type
    by_type = group_errors_by_type(errors)
    print("ERRORS BY TYPE:")
    for error_code in sorted(by_type.keys()):
        count = len(by_type[error_code])
        print(f"  {error_code}: {count}")

    # Group by file
    by_file = group_errors_by_file(errors)
    print(f"\nERRORS BY FILE (Top 10):")
    sorted_files = sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    for file_path, file_errors in sorted_files:
        print(f"  {file_path}: {len(file_errors)}")


def export_errors_to_json(errors: list[LintError], output_path: str):
    """Export errors to JSON file."""
    import json

    errors_dict = [
        {
            "file_path": e.file_path,
            "line": e.line,
            "column": e.column,
            "error_code": e.error_code,
            "message": e.message,
            "hook": e.hook,
            "context": e.context,
        }
        for e in errors
    ]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(errors_dict, f, indent=2)

    print(f"\nExported {len(errors)} errors to {output_path}")


def export_errors_to_markdown(errors: list[LintError], output_path: str):
    """Export errors to Markdown file for easy review."""
    by_file = group_errors_by_file(errors)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Pre-commit Errors\n\n")
        f.write(f"**Total Errors:** {len(errors)}\n\n")

        # Error type summary
        by_type = group_errors_by_type(errors)
        f.write("## Error Summary\n\n")
        for error_code in sorted(by_type.keys()):
            count = len(by_type[error_code])
            f.write(f"- **{error_code}**: {count} occurrences\n")

        # Errors by file
        f.write("\n## Errors by File\n\n")
        for file_path in sorted(by_file.keys()):
            file_errors = by_file[file_path]
            f.write(f"\n### {file_path} ({len(file_errors)} errors)\n\n")

            for error in file_errors:
                loc = f"Line {error.line}"
                if error.column:
                    loc += f", Col {error.column}"
                f.write(f"- **[{error.error_code}]** {loc}: {error.message}\n")

    print(f"Exported errors to {output_path}")


if __name__ == "__main__":
    import sys

    # Default file path
    error_file = Path(__file__).parent.parent / "precommit_errors.txt"

    if len(sys.argv) > 1:
        error_file = Path(sys.argv[1])

    if not error_file.exists():
        print(f"Error: File not found: {error_file}")
        sys.exit(1)

    print(f"Parsing errors from: {error_file}")

    # Parse errors
    errors = parse_precommit_errors(str(error_file))

    # Print summary
    print_summary(errors)

    # Print detailed list
    print(f"\n{'=' * 80}")
    print("DETAILED ERROR LIST:")
    print(f"{'=' * 80}\n")

    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")

    # Export to files
    output_dir = error_file.parent
    export_errors_to_json(errors, str(output_dir / "precommit_errors.json"))
    export_errors_to_markdown(errors, str(output_dir / "precommit_errors.md"))

    print("\n✅ Error parsing complete!")
