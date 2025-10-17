#!/usr/bin/env python3
"""
Quick progress checker for type hints implementation
"""

import ast
import os
from pathlib import Path
from typing import Dict, List


def count_functions_with_type_hints(file_path: Path) -> Dict[str, int]:
    """Count functions with and without type hints in a file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)

        total_functions = 0
        functions_with_hints = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private methods
                if node.name.startswith("_"):
                    continue

                total_functions += 1

                # Check if function has type hints
                has_return_hint = node.returns is not None

                # Check parameters (skip self/cls)
                param_hints = 0
                param_count = 0
                for arg in node.args.args:
                    if arg.arg in ["self", "cls"]:
                        continue
                    param_count += 1
                    if arg.annotation is not None:
                        param_hints += 1

                # Function has hints if it has return type and all params have hints
                if has_return_hint and (param_count == 0 or param_hints == param_count):
                    functions_with_hints += 1

        return {
            "total": total_functions,
            "with_hints": functions_with_hints,
            "without_hints": total_functions - functions_with_hints,
        }

    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {"total": 0, "with_hints": 0, "without_hints": 0}


def main():
    src_dir = Path("src")
    if not src_dir.exists():
        print("src directory not found")
        return 1

    directories = ["classes", "client", "routes", "utils", "integrations"]

    total_stats = {"total": 0, "with_hints": 0, "without_hints": 0}
    dir_stats = {}

    print("Type Hints Implementation Progress")
    print("=" * 50)

    for directory in directories:
        dir_path = src_dir / directory
        if not dir_path.exists():
            continue

        dir_total = {"total": 0, "with_hints": 0, "without_hints": 0}

        python_files = list(dir_path.glob("**/*.py"))
        python_files = [f for f in python_files if not f.name.startswith("__")]

        for file_path in python_files:
            stats = count_functions_with_type_hints(file_path)
            for key in stats:
                dir_total[key] += stats[key]
                total_stats[key] += stats[key]

        dir_stats[directory] = dir_total

        if dir_total["total"] > 0:
            percentage = (dir_total["with_hints"] / dir_total["total"]) * 100
            print(
                f"{directory:12} | {dir_total['with_hints']:3}/{dir_total['total']:3} functions ({percentage:5.1f}%)"
            )
        else:
            print(f"{directory:12} | No functions found")

    print("-" * 50)
    if total_stats["total"] > 0:
        total_percentage = (total_stats["with_hints"] / total_stats["total"]) * 100
        print(
            f"{'TOTAL':12} | {total_stats['with_hints']:3}/{total_stats['total']:3} functions ({total_percentage:5.1f}%)"
        )

        remaining = total_stats["without_hints"]
        print(f"\n📊 Progress: {total_percentage:.1f}% complete")
        print(f"🔧 Remaining: {remaining} functions need type hints")

        if remaining == 0:
            print("🎉 All functions have type hints! Great job!")
        else:
            print(f"🎯 Next: Focus on directories with missing type hints")
    else:
        print("No functions found to analyze")

    return 0


if __name__ == "__main__":
    exit(main())
