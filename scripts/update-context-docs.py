"""Update RouteContext documentation to remove debug_api references."""

import json
import os
from pathlib import Path


def update_route_pattern(text: str) -> str:
    """Remove debug_api from route function pattern."""
    # Remove debug_api parameter line
    text = text.replace("    debug_api: bool = False,\n", "")
    # Remove debug_api from RouteContext initialization
    text = text.replace("            debug_api=debug_api,\n", "")
    # Update description text
    text = text.replace(
        "individual `session`, `debug_api`, `debug_num_stacks_to_drop`, and `parent_class` parameters",
        "individual `session`, `debug_num_stacks_to_drop`, and `parent_class` parameters",
    )
    text = text.replace(
        "- [ ] Replace individual session/debug_api params with context",
        "- [ ] Replace individual session params with context",
    )
    return text


def update_class_pattern(text: str) -> str:
    """Remove debug_api from class method pattern."""
    # Remove debug_api parameter
    text = text.replace("    debug_api: bool = False,\n", "")
    # Remove debug_api from _build_route_context call
    text = text.replace("        debug_api=debug_api,\n", "")
    return text


def update_json_file(file_path: Path):
    """Update a single JSON issue file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "body" in data:
        original_body = data["body"]
        updated_body = original_body

        # Apply route pattern updates
        updated_body = update_route_pattern(updated_body)

        # Apply class pattern updates
        updated_body = update_class_pattern(updated_body)

        if updated_body != original_body:
            data["body"] = updated_body
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"✓ Updated: {file_path.name}")
            return True
    return False


def update_all_issues_file(file_path: Path):
    """Update the aggregated all_issues.json file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated_count = 0
    if "issues" in data:
        for issue in data["issues"]:
            if "body" in issue:
                original_body = issue["body"]
                updated_body = update_route_pattern(original_body)
                updated_body = update_class_pattern(updated_body)

                if updated_body != original_body:
                    issue["body"] = updated_body
                    updated_count += 1

        if updated_count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"✓ Updated {updated_count} issues in: {file_path.name}")
            return True
    return False


def main():
    """Update all JSON issue files."""
    scripts_dir = Path(__file__).parent
    issues_dir = scripts_dir / "issues"

    if not issues_dir.exists():
        print(f"Issues directory not found: {issues_dir}")
        return

    json_files = list(issues_dir.glob("*.json"))
    print(f"Found {len(json_files)} JSON files to process\n")

    updated_count = 0
    for json_file in json_files:
        if json_file.name == "all_issues.json":
            update_all_issues_file(json_file)
        elif update_json_file(json_file):
            updated_count += 1

    print(f"\nCompleted: {updated_count} individual files updated")


if __name__ == "__main__":
    main()
