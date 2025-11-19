"""Replace Optional[Type] with Type | None in Python files.

This script modernizes type hints by replacing typing.Optional[X] with X | None,
which is the preferred syntax in Python 3.10+.
"""

import re
from pathlib import Path
from typing import Tuple


def replace_optional_in_content(content: str) -> Tuple[str, int]:
    """Replace Optional[Type] with Type | None in file content.

    Handles nested Optional types and preserves formatting.

    Args:
        content: File content to process

    Returns:
        Tuple of (modified_content, replacement_count)
    """
    count = 0
    modified = content

    # Pattern to match Optional[...] with balanced brackets
    # This handles nested generics like Optional[list[str]]
    pattern = r'\bOptional\[([^\[\]]+(?:\[[^\[\]]*\])*)\]'

    def replacer(match):
        nonlocal count
        count += 1
        inner_type = match.group(1)
        return f"{inner_type} | None"

    # Keep replacing until no more matches (handles nested cases)
    prev_count = -1
    while prev_count != count:
        prev_count = count
        modified = re.sub(pattern, replacer, modified)

    return modified, count


def remove_optional_import(content: str) -> str:
    """Remove Optional from typing imports if it's no longer needed.

    Args:
        content: File content to process

    Returns:
        Modified content with Optional removed from imports
    """
    # Check if Optional is still used anywhere in the file
    if re.search(r'\bOptional\[', content):
        return content  # Still in use, don't remove

    # Remove "Optional, " or ", Optional" from typing imports
    content = re.sub(r'from typing import ([^(\n]*?)Optional,\s*', r'from typing import \1', content)
    content = re.sub(r'from typing import ([^(\n]*?),\s*Optional\b', r'from typing import \1', content)

    # Remove standalone "from typing import Optional"
    content = re.sub(r'from typing import Optional\n', '', content)

    # Clean up empty typing imports
    content = re.sub(r'from typing import\s*\n', '', content)

    return content


def process_file(file_path: Path, dry_run: bool = False) -> Tuple[int, bool]:
    """Process a single Python file.

    Args:
        file_path: Path to the Python file
        dry_run: If True, only report changes without modifying files

    Returns:
        Tuple of (replacement_count, file_was_modified)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        modified, count = replace_optional_in_content(content)

        if count > 0:
            modified = remove_optional_import(modified)

            if not dry_run:
                file_path.write_text(modified, encoding='utf-8')

            return count, True
        return 0, False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0, False


def process_directory(
    directory: Path,
    pattern: str = "**/*.py",
    dry_run: bool = False,
    verbose: bool = False
) -> None:
    """Process all Python files in a directory.

    Args:
        directory: Root directory to search
        pattern: Glob pattern for files to process
        dry_run: If True, only report changes without modifying files
        verbose: If True, print detailed information
    """
    total_files = 0
    modified_files = 0
    total_replacements = 0

    for file_path in sorted(directory.glob(pattern)):
        if file_path.is_file():
            total_files += 1
            count, was_modified = process_file(file_path, dry_run=dry_run)

            if was_modified:
                modified_files += 1
                total_replacements += count
                action = "Would modify" if dry_run else "Modified"
                print(f"{action}: {file_path.relative_to(directory)} ({count} replacements)")
            elif verbose:
                print(f"No changes: {file_path.relative_to(directory)}")

    print(f"\nSummary:")
    print(f"  Files scanned: {total_files}")
    print(f"  Files modified: {modified_files}")
    print(f"  Total replacements: {total_replacements}")

    if dry_run and modified_files > 0:
        print(f"\nThis was a dry run. Use --apply to make changes.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Replace Optional[Type] with Type | None in Python files"
    )
    parser.add_argument(
        "path",
        type=Path,
        nargs="?",
        default=Path("src/domolibrary2"),
        help="Directory or file to process (default: src/domolibrary2)"
    )
    parser.add_argument(
        "--pattern",
        default="**/*.py",
        help="Glob pattern for files to process (default: **/*.py)"
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes (default is dry run)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    path = args.path
    if path.is_file():
        count, modified = process_file(path, dry_run=not args.apply)
        if modified:
            action = "Would modify" if not args.apply else "Modified"
            print(f"{action}: {path} ({count} replacements)")
        else:
            print(f"No changes needed: {path}")
    elif path.is_dir():
        process_directory(
            path,
            pattern=args.pattern,
            dry_run=not args.apply,
            verbose=args.verbose
        )
    else:
        print(f"Error: {path} is not a valid file or directory")
        exit(1)
