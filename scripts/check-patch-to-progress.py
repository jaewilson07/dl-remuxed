#!/usr/bin/env python3
"""
Track @patch_to refactoring progress
"""

import os
import re
from pathlib import Path
from collections import defaultdict


def count_patch_to_usage():
    """Count remaining @patch_to usage across the codebase"""

    src_dir = Path("src")
    if not src_dir.exists():
        print("src directory not found")
        return

    directories = ["client", "classes", "utils", "integrations"]

    total_files = 0
    files_with_patches = 0
    total_patches = 0
    by_directory = defaultdict(lambda: {"files": 0, "patches": 0})

    print("@patch_to Refactoring Progress")
    print("=" * 50)

    for directory in directories:
        dir_path = src_dir / directory
        if not dir_path.exists():
            continue

        python_files = list(dir_path.glob("**/*.py"))
        python_files = [f for f in python_files if not f.name.startswith("__")]

        dir_files = 0
        dir_patches = 0

        for file_path in python_files:
            total_files += 1
            dir_files += 1

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                patches = len(re.findall(r"@patch_to", content))
                if patches > 0:
                    files_with_patches += 1
                    total_patches += patches
                    dir_patches += patches

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        by_directory[directory] = {"files": dir_files, "patches": dir_patches}

        if dir_patches > 0:
            print(f"{directory:12} | {dir_patches:3} @patch_to decorators remaining")
        else:
            print(f"{directory:12} | ✅ Complete! No @patch_to decorators")

    print("-" * 50)
    print(f"{'TOTAL':12} | {total_patches:3} @patch_to decorators remaining")

    if total_patches == 0:
        print("\n🎉 REFACTORING COMPLETE! All @patch_to decorators have been removed!")
        print("\n✅ Final validation steps:")
        print("   1. Test imports: python -c \"import src; print('Success')\"")
        print("   2. Run linting: .\\scripts\\lint.ps1")
        print("   3. Run tests: .\\scripts\\test.ps1")
    else:
        remaining_files = files_with_patches
        progress = ((221 - total_patches) / 221) * 100

        print(
            f"\n📊 Progress: {progress:.1f}% complete ({221 - total_patches}/221 methods refactored)"
        )
        print(
            f"🔧 Remaining: {total_patches} @patch_to decorators in {remaining_files} files"
        )
        print(f"🎯 Continue with: .\\scripts\\refactor-patch-to.ps1")

        # Show which directories still need work
        print(f"\n📋 Remaining work by directory:")
        for directory in directories:
            patches = by_directory[directory]["patches"]
            if patches > 0:
                print(f"   {directory}: {patches} decorators")


if __name__ == "__main__":
    count_patch_to_usage()
