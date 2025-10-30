#!/usr/bin/env python3
"""
Fix undefined aliases in Python files after nbdev cleanup.

This script identifies and fixes common alias patterns that were removed
during nbdev dependency removal.
"""

import re
from pathlib import Path


def fix_aliases_in_file(file_path: Path):
    """Fix common alias patterns in a Python file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Define alias mappings
        alias_mappings = {
            # dmda -> DomoAuth patterns
            r"dmda\.DomoAuth": "DomoAuth",
            r"dmda_DomoAuth": "DomoAuth",
            # dmde -> DomoError patterns
            r"dmde\.DomoError": "DomoError",
            r"dmde_DomoError": "DomoError",
            # dmee -> DomoManager patterns
            r"dmee\.DomoManager": "DomoManager",
            r"dmee_DomoManager": "DomoManager",
            # lc -> Logger patterns (if using a logger)
            r"lc_Logger": "Logger",
            r"lc\.Logger": "Logger",
            # util_dd -> DictDot patterns
            r"util_dd\(": "DictDot(",
            # other common patterns
            r"SearchUser_NoResults": "SearchUser_NotFound",
            r"GetUser_Error": "User_GET_Error",
        }

        changes_made = []

        # Apply each mapping
        for pattern, replacement in alias_mappings.items():
            old_content = content
            content = re.sub(pattern, replacement, content)
            if content != old_content:
                matches = len(re.findall(pattern, old_content))
                changes_made.append(
                    f"  - {pattern} -> {replacement} ({matches} occurrences)"
                )

        # Write back if changes were made
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"✅ Fixed {file_path}")
            for change in changes_made:
                print(change)
            return True
        else:
            print(f"⚪ No changes needed in {file_path}")
            return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def main():
    """Main function to fix aliases in Python files."""
    project_root = Path(__file__).parent.parent

    # Find Python files to process
    python_files = []

    # Look in src directory
    src_dir = project_root / "src"
    if src_dir.exists():
        python_files.extend(src_dir.rglob("*.py"))

    print(f"🔍 Found {len(python_files)} Python files to process...")

    fixed_count = 0
    for file_path in python_files:
        if fix_aliases_in_file(file_path):
            fixed_count += 1

    print(f"\n📊 Results: {fixed_count}/{len(python_files)} files modified")


if __name__ == "__main__":
    main()
