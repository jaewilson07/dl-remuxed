"""Script to add context parameter to all @gd.route_function decorated functions.

This is a temporary fix to ensure all route functions accept the context parameter
that the route_function decorator now passes.
"""

import re
from pathlib import Path


def add_context_param(file_path: Path) -> bool:
    """Add context=None parameter to route functions that don't have it."""
    content = file_path.read_text(encoding="utf-8")
    original_content = content

    # Find all @gd.route_function decorated functions
    pattern = r"(@gd\.route_function.*?\n.*?async def \w+\([^)]*?\):)"

    def add_context(match):
        func_def = match.group(1)
        # Check if context is already in the signature
        if "context" in func_def:
            return func_def

        # Add context=None before the closing ):
        func_def = func_def.replace("):", ",\n    context=None,\n):")
        return func_def

    content = re.sub(pattern, add_context, content, flags=re.DOTALL | re.MULTILINE)

    if content != original_content:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    """Process all route files."""
    routes_dir = Path(__file__).parent.parent / "src" / "domolibrary2" / "routes"

    modified_files = []
    for py_file in routes_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue

        try:
            if add_context_param(py_file):
                modified_files.append(py_file.relative_to(routes_dir.parent.parent))
                print(f"✓ Modified: {py_file.relative_to(routes_dir.parent.parent)}")
        except Exception as e:
            print(f"✗ Error processing {py_file}: {e}")

    print(f"\n{len(modified_files)} files modified")


if __name__ == "__main__":
    main()
