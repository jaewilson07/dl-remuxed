"""Combined script to fix encoding and parse errors in one go."""

import sys
from pathlib import Path
import shutil

# Fix encoding first
print("=" * 80)
print("STEP 1: FIXING ENCODING")
print("=" * 80)

error_file = Path(__file__).parent.parent / "precommit_errors.txt"

if not error_file.exists():
    print(f"❌ Error: File not found: {error_file}")
    sys.exit(1)

# Create backup
backup_file = error_file.with_suffix('.txt.bak')
if not backup_file.exists():  # Don't overwrite existing backup
    shutil.copy2(error_file, backup_file)
    print(f"✓ Created backup: {backup_file}")

# Read and fix encoding
with open(error_file, 'rb') as f:
    content = f.read()

# Try to decode as UTF-16LE first (common Windows encoding)
try:
    text = content.decode('utf-16le')
    print(f"✓ Detected UTF-16LE encoding with null bytes")
    # Remove the BOM if present
    if text.startswith('\ufeff'):
        text = text[1:]
except UnicodeDecodeError:
    # Remove null bytes and try again
    content = content.replace(b'\x00', b'')
    try:
        text = content.decode('utf-8')
        print(f"✓ Detected UTF-8 encoding")
    except UnicodeDecodeError:
        text = content.decode('latin-1')
        print(f"✓ Detected Latin-1 encoding")

# Write back as UTF-8
with open(error_file, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"✓ Fixed encoding: {error_file}")
print(f"✓ File size: {len(text)} characters")

# Now parse the errors
print("\n" + "=" * 80)
print("STEP 2: PARSING ERRORS")
print("=" * 80)

import re
from dataclasses import dataclass
from typing import Optional
import json


@dataclass
class LintError:
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


# Parse errors
errors = []
current_hook = None

ruff_pattern = re.compile(r"([^:]+\.py):(\d+):(\d+):\s+([A-Z]\d+)\s+(.+?)(?=\n|$)")
yaml_pattern = re.compile(r'in "([^"]+)", line (\d+), column (\d+)')

lines = text.split("\n")

for i, line in enumerate(lines):
    line = line.strip()

    if "hook id:" in line.lower():
        hook_match = re.search(r"hook id:\s+(.+)", line, re.IGNORECASE)
        if hook_match:
            current_hook = hook_match.group(1).strip()

    ruff_match = ruff_pattern.search(line)
    if ruff_match:
        file_path = ruff_match.group(1).replace("\\", "/")
        line_num = int(ruff_match.group(2))
        col_num = int(ruff_match.group(3))
        error_code = ruff_match.group(4)
        message = ruff_match.group(5).strip()

        context_lines = []
        for j in range(i + 1, min(i + 10, len(lines))):
            ctx_line = lines[j].strip()
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

    yaml_match = yaml_pattern.search(line)
    if yaml_match:
        file_path = yaml_match.group(1).strip()
        line_num = int(yaml_match.group(2))
        col_num = int(yaml_match.group(3))
        message = ""
        if i > 0:
            message = lines[i - 1].strip()

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

# Print summary
print(f"\n{'=' * 80}")
print(f"TOTAL ERRORS: {len(errors)}")
print(f"{'=' * 80}\n")

# Group by error type
by_type = {}
for error in errors:
    if error.error_code not in by_type:
        by_type[error.error_code] = []
    by_type[error.error_code].append(error)

print("ERRORS BY TYPE:")
for error_code in sorted(by_type.keys()):
    count = len(by_type[error_code])
    print(f"  {error_code}: {count}")

# Group by file
by_file = {}
for error in errors:
    if error.file_path not in by_file:
        by_file[error.file_path] = []
    by_file[error.file_path].append(error)

print(f"\nERRORS BY FILE (Top 10):")
sorted_files = sorted(by_file.items(), key=lambda x: len(x[1]), reverse=True)[:10]
for file_path, file_errors in sorted_files:
    print(f"  {file_path}: {len(file_errors)}")

# Export to JSON
output_dir = error_file.parent
json_file = output_dir / "precommit_errors.json"

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

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(errors_dict, f, indent=2)

print(f"\n✓ Exported {len(errors)} errors to {json_file}")

# Export to Markdown
md_file = output_dir / "precommit_errors.md"

with open(md_file, "w", encoding="utf-8") as f:
    f.write("# Pre-commit Errors\n\n")
    f.write(f"**Total Errors:** {len(errors)}\n\n")

    f.write("## Error Summary\n\n")
    for error_code in sorted(by_type.keys()):
        count = len(by_type[error_code])
        f.write(f"- **{error_code}**: {count} occurrences\n")

    f.write("\n## Errors by File\n\n")
    for file_path in sorted(by_file.keys()):
        file_errors = by_file[file_path]
        f.write(f"\n### {file_path} ({len(file_errors)} errors)\n\n")

        for error in file_errors:
            loc = f"Line {error.line}"
            if error.column:
                loc += f", Col {error.column}"
            f.write(f"- **[{error.error_code}]** {loc}: {error.message}\n")

print(f"✓ Exported errors to {md_file}")

# Print detailed list
print(f"\n{'=' * 80}")
print("DETAILED ERROR LIST (First 20):")
print(f"{'=' * 80}\n")

for i, error in enumerate(errors[:20], 1):
    print(f"{i}. {error}")

if len(errors) > 20:
    print(f"\n... and {len(errors) - 20} more errors")

print("\n✅ Complete! Check precommit_errors.json and precommit_errors.md for full details.")
