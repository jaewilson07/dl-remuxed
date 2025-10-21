#!/usr/bin/env python3
"""
Fix DomoEnum inheritance issues by updating all files to use DomoEnumMixin pattern.
"""

import os
import re
from pathlib import Path

# List of files that need to be updated
FILES_TO_UPDATE = [
    "src/routes/card.py",
    "src/classes/DomoDataflow_Action.py",
    "src/classes/DomoInstanceConfig_Scheduler_Policies.py",
    "src/classes/DomoAccount_Config.py",
    "src/classes/DomoAccount_OAuth.py",
    "src/classes/CodeEngineManifest_Argument.py",
    "src/classes/DomoPublish.py",
    "src/classes/DomoLineage.py",
    "src/classes/DomoCertification.py",
    "src/routes/codeengine.py",
    "src/routes/jupyter.py",
    "src/routes/account.py",
    "src/routes/user_attributes.py",
    "src/routes/ai.py",
    "src/routes/appdb.py",
    "src/routes/dataset.py",
    "src/routes/beastmode.py",
    "src/routes/instance_config_api_client.py",
    "src/routes/user.py",
]


def fix_enum_inheritance(file_path):
    """Fix enum inheritance in a single file."""
    print(f"Processing {file_path}...")

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content

    # Add Enum import if not present
    if "from enum import Enum" not in content:
        # Find imports section and add Enum import
        lines = content.split("\n")
        import_added = False
        for i, line in enumerate(lines):
            if line.startswith("from enum import"):
                # Already has enum import, modify it
                if "Enum" not in line:
                    lines[i] = line.rstrip() + ", Enum"
                    import_added = True
                    break
            elif line.startswith("import ") and not import_added:
                # Insert before first import
                lines.insert(i, "from enum import Enum")
                import_added = True
                break
            elif line.startswith("from ") and not import_added:
                # Insert before first from import
                lines.insert(i, "from enum import Enum")
                import_added = True
                break

        if not import_added:
            # Add after __future__ imports if present
            for i, line in enumerate(lines):
                if line.startswith("from __future__"):
                    continue
                elif line.strip() == "":
                    continue
                else:
                    lines.insert(i, "from enum import Enum")
                    break

        content = "\n".join(lines)

    # Update DomoEnum imports to include DomoEnumMixin
    # Replace DomoEnum imports
    patterns = [
        (
            r"from \.\.client\.entities import DomoEnum\b",
            "from ..client.entities import DomoEnumMixin",
        ),
        (
            r"from \.client\.entities import DomoEnum\b",
            "from .client.entities import DomoEnumMixin",
        ),
        (r"import \.\.client\.entities as dmee", "import ..client.entities as dmee"),
        (r"import \.client\.entities as dmee", "import .client.entities as dmee"),
        (r"import \.\.\.client\.entities as dmen", "import ...client.entities as dmen"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    # Fix class declarations - convert DomoEnum inheritance to DomoEnumMixin + Enum
    # Pattern: class ClassName(DomoEnum): -> class ClassName(DomoEnumMixin, Enum):
    content = re.sub(
        r"class\s+(\w+)\(DomoEnum\):", r"class \1(DomoEnumMixin, Enum):", content
    )

    # Fix qualified DomoEnum references like dmee.DomoEnum
    content = re.sub(
        r"class\s+(\w+)\(dmee\.DomoEnum\):",
        r"class \1(dmee.DomoEnumMixin, Enum):",
        content,
    )
    content = re.sub(
        r"class\s+(\w+)\(dmen\.DomoEnum\):",
        r"class \1(dmen.DomoEnumMixin, Enum):",
        content,
    )

    # Write back if changed
    if content != original_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file_path}")
        return True
    else:
        print(f"No changes needed for {file_path}")
        return False


def main():
    """Main function to process all files."""
    workspace_root = Path("/workspaces/dl-remuxed")
    files_updated = 0

    for file_path in FILES_TO_UPDATE:
        full_path = workspace_root / file_path
        if full_path.exists():
            if fix_enum_inheritance(full_path):
                files_updated += 1
        else:
            print(f"Warning: {full_path} does not exist")

    print(f"\nProcessed {len(FILES_TO_UPDATE)} files, updated {files_updated} files")


if __name__ == "__main__":
    main()
