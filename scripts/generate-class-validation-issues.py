#!/usr/bin/env python3
"""
Generate class validation issues for all classes in the domolibrary2 project.

This script analyzes the classes directory and generates GitHub issue files
that can be bulk-imported or used as templates for manual issue creation.

Usage:
    python scripts/generate-class-validation-issues.py [--output-dir EXPORTS/issues]
"""

import argparse
import os
from pathlib import Path
from typing import list


class ClassInfo:
    """Information about a class file for issue generation."""

    def __init__(self, file_path: Path, class_name: str):
        self.file_path = file_path
        self.class_name = class_name
        self.module_name = self._extract_module_name()
        self.route_name = self._infer_route_name()
        self.priority = self._determine_priority()

    def _extract_module_name(self) -> str:
        """Extract module name from file path."""
        # Remove src/domolibrary2/classes/ prefix
        rel_path = str(self.file_path).replace("src/domolibrary2/classes/", "")
        rel_path = rel_path.replace("src\\domolibrary2\\classes\\", "")
        return rel_path

    def _infer_route_name(self) -> str:
        """Infer the likely route module name from class name."""
        # Remove 'Domo' prefix and convert to snake_case
        name = self.class_name.replace("Domo", "")
        # Convert PascalCase to snake_case
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append("_")
            result.append(char.lower())
        return "".join(result)

    def _determine_priority(self) -> str:
        """Determine priority based on class name."""
        high_priority = [
            "DomoUser",
            "DomoDataset",
            "DomoCard",
            "DomoPage",
            "DomoGroup",
        ]
        medium_priority = [
            "DomoRole",
            "DomoAccount",
            "DomoActivityLog",
            "DomoApplication",
        ]

        if self.class_name in high_priority:
            return "high"
        elif self.class_name in medium_priority:
            return "medium"
        else:
            return "low"


def find_class_files(classes_dir: Path) -> list[ClassInfo]:
    """Find all class files in the classes directory."""
    class_files = []

    for root, _dirs, files in os.walk(classes_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                file_path = Path(root) / file
                # Extract class name from file name
                class_name = file.replace(".py", "")
                class_files.append(ClassInfo(file_path, class_name))

    return sorted(class_files, key=lambda x: (x.priority, x.class_name))


def generate_issue_content(class_info: ClassInfo) -> str:
    """Generate issue content for a class."""
    # Priority labels
    priority_label = f"priority-{class_info.priority}"

    # Test file path
    test_file = f"tests/classes/test_50_{class_info.class_name}.py"

    issue_content = f"""---
name: Class Validation and Testing
about: Validate and fix {class_info.class_name} implementation
title: 'Validate and Test: {class_info.class_name}'
labels: ['class-validation', 'testing', 'refactor', '{priority_label}']
assignees: ''
---

# Validate and Test: {class_info.class_name}

## 📋 Background

This issue tracks the validation and testing of the `{class_info.class_name}` class to ensure it follows domolibrary2 design patterns and standards.

### Entity Hierarchy
All Domo entities should inherit from the appropriate base class:

```
DomoBase (abstract)
└── DomoEntity (id, auth, raw, display_url, from_dict, get_by_id)
    ├── DomoEntity_w_Lineage (adds Lineage tracking)
    │   ├── DomoFederatedEntity (adds federation support)
    │   │   └── DomoPublishedEntity (adds publish/subscribe)
    │   └── [Other lineage-aware entities]
    └── DomoManager (for entity collections)

DomoSubEntity (for composition - entities that belong to parents)
```

### Key Design Patterns

1. **Dataclass Pattern**: All entities use `@dataclass` decorator
2. **Composition over Inheritance**: Use `DomoSubEntity` for related entities (e.g., `DomoTags`, `DomoLineage`, `DomoCertification`)
3. **Route Function Delegation**: Class methods should call route functions, not implement API logic
4. **Standardized Signatures**:
   - `auth` parameter always comes first
   - Optional parameters properly typed with defaults
   - All methods include docstrings
5. **Exception Handling**: Use route-specific exceptions imported from `routes.[entity].exceptions`

---

## 📍 Class Location

**File**: `{class_info.module_name}`
**Route Module**: `src/domolibrary2/routes/{class_info.route_name}/`
**Test File**: `{test_file}`

---

## ✅ Tasks

### Phase 1: Structure Validation

- [ ] **Task 1.1**: Verify proper inheritance
  - Check that class inherits from appropriate base (`DomoEntity`, `DomoEntity_w_Lineage`, `DomoManager`, or `DomoSubEntity`)
  - Verify `@dataclass` decorator is present
  - Confirm `__all__` exports are complete

- [ ] **Task 1.2**: Validate required attributes and methods
  - [ ] `id` attribute present with correct type
  - [ ] `auth: DomoAuth` attribute present (with `field(repr=False)`)
  - [ ] `raw: dict` attribute present (with `field(default_factory=dict, repr=False)`)
  - [ ] `display_url()` property/method implemented
  - [ ] `from_dict()` classmethod implemented
  - [ ] `get_by_id()` classmethod implemented (for DomoEntity subclasses)
  - [ ] `__post_init__()` method if initialization logic needed

- [ ] **Task 1.3**: Review method signatures
  - [ ] All methods have `auth` as first parameter (after `cls` or `self`)
  - [ ] Optional parameters properly typed with defaults
  - [ ] Methods delegate to route functions (not implementing API logic)
  - [ ] All public methods have docstrings

### Phase 2: Composition Analysis

- [ ] **Task 2.1**: Identify composition opportunities
  - [ ] Check if entity should have `DomoTags` (most entities support tagging)
  - [ ] Check if entity should have `DomoLineage` (datasets, cards, pages)
  - [ ] Check if entity should have `DomoCertification` (datasets, cards)
  - [ ] Check if entity should have `DomoAccess` (sharing/permissions)
  - [ ] Check if entity should have `DomoMembership` (groups, user groups)
  - [ ] list any entity-specific subentities needed

- [ ] **Task 2.2**: Implement subentity composition
  - [ ] Add subentity attributes as `field(default=None)`
  - [ ] Initialize subentities in `__post_init__()` using `from_parent()`
  - [ ] Verify subentities inherit from `DomoSubEntity`

### Phase 3: Route Integration

- [ ] **Task 3.1**: Verify route function imports
  - [ ] Route functions imported from correct module (`routes.{class_info.route_name}`)
  - [ ] Exception classes imported from `routes.{class_info.route_name}.exceptions`
  - [ ] Check for any incorrect imports from `client.*` (should be from `routes.*`)

- [ ] **Task 3.2**: Validate route function usage
  - [ ] Methods call route functions correctly (auth first, then params)
  - [ ] Route function exceptions properly imported and re-raised
  - [ ] No API implementation logic in class methods (should be in routes)

### Phase 4: Manager Class Validation (if applicable)

- [ ] **Task 4.1**: Verify manager pattern
  - [ ] Manager class inherits from `DomoManager`
  - [ ] Manager has reference to entity class
  - [ ] Common manager methods present:
    - [ ] `get()` - retrieve all entities
    - [ ] `get_by_name()` or `search()` - find specific entities
    - [ ] `create()` - create new entity
    - [ ] `update()` - update existing entity
    - [ ] `delete()` - remove entity

### Phase 5: Testing

- [ ] **Task 5.1**: Create/update test file
  - [ ] Test file exists: `{test_file}`
  - [ ] Test file imports class and required modules
  - [ ] Test file loads `.env` for configuration
  - [ ] Test authentication setup (token_auth)

- [ ] **Task 5.2**: Implement test functions (following `DomoUser.py` pattern)
  - [ ] `test_cell_0()` - Setup/authentication helper
  - [ ] `test_cell_1()` - Test `get_by_id()` method
  - [ ] `test_cell_2()` - Test `from_dict()` method
  - [ ] Additional tests for entity-specific methods
  - [ ] Test exception handling (not found, invalid auth, etc.)

- [ ] **Task 5.3**: Document required environment variables
  - [ ] list all `.env` constants needed for tests
  - [ ] Example values provided (sanitized)
  - [ ] Document how to obtain test values

- [ ] **Task 5.4**: Run and validate tests
  - [ ] All tests pass successfully
  - [ ] Tests use async/await properly
  - [ ] Tests clean up resources if needed

---

## 🎯 Acceptance Criteria

### Structure
- ✅ Class inherits from appropriate entity base class
- ✅ All required attributes and methods implemented
- ✅ `@dataclass` decorator applied correctly
- ✅ `__all__` exports include all public classes and exceptions

### Implementation
- ✅ Methods delegate to route functions (no API logic in class)
- ✅ Method signatures follow standards (auth first, typed params)
- ✅ All public methods have docstrings
- ✅ Exception classes imported from route modules
- ✅ No circular import issues

### Composition
- ✅ Appropriate subentities identified and implemented
- ✅ Subentities initialized in `__post_init__()`
- ✅ Subentities use `from_parent()` pattern

### Testing
- ✅ Test file created following `DomoUser.py` pattern
- ✅ All core methods covered by tests
- ✅ Tests run successfully without errors
- ✅ Required `.env` constants documented

### Code Quality
- ✅ Type hints present on all parameters and return values
- ✅ Code follows PEP 8 style guidelines
- ✅ No linting errors from pre-commit hooks
- ✅ Documentation complete and accurate

---

## 🔧 Environment Variables

Document any `.env` constants required for testing:

```bash
# Required for {class_info.class_name} tests
DOMO_INSTANCE="your-instance"
DOMO_ACCESS_TOKEN="your-token"
{class_info.class_name.upper()}_ID_1="example-id-1"
{class_info.class_name.upper()}_ID_2="example-id-2"
# Add more as needed
```

### How to Obtain Test Values
<!-- Provide instructions for finding valid test values -->
1. Navigate to your Domo instance
2. [Specific steps to find test entity]
3. Copy the ID from the URL or API response

---

## 📝 Notes

<!-- Add any class-specific notes, quirks, or special considerations -->

### Priority
**{class_info.priority.upper()}** - {_get_priority_description(class_info.priority)}

### Known Issues
- [ ] list any known bugs or limitations

### Related Issues
- Related to #[issue-number]

### References
- [Class Validation Guide](../docs/class-validation-guide.md)
- [Quick Reference](../docs/class-validation-quick-reference.md)
- [Entities Documentation](../src/domolibrary2/client/entities.py)
- [Testing Guide](../docs/testing-guide.md)
- [Route Standards](../.github/instructions/routes.instructions.md)
- [DomoUser Example](../src/domolibrary2/classes/DomoUser.py)
- [DomoUser Test Example](../tests/classes/DomoUser.py)

---

## 🚀 Implementation Checklist

Use this checklist to track progress:

- [ ] Phase 1: Structure Validation - Complete
- [ ] Phase 2: Composition Analysis - Complete
- [ ] Phase 3: Route Integration - Complete
- [ ] Phase 4: Manager Class Validation - Complete (if applicable)
- [ ] Phase 5: Testing - Complete
- [ ] All acceptance criteria met
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Ready for merge
"""

    return issue_content


def _get_priority_description(priority: str) -> str:
    """Get description for priority level."""
    descriptions = {
        "high": "Commonly used class, should be validated first",
        "medium": "Core infrastructure class, validate after high priority",
        "low": "Specialized or less frequently used class",
    }
    return descriptions.get(priority, "Standard priority")


def main():
    """Main script execution."""
    parser = argparse.ArgumentParser(
        description="Generate class validation issues for domolibrary2 classes"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="EXPORTS/issues",
        help="Output directory for issue files (default: EXPORTS/issues)",
    )
    parser.add_argument(
        "--classes-dir",
        type=str,
        default="src/domolibrary2/classes",
        help="Classes directory to scan (default: src/domolibrary2/classes)",
    )
    parser.add_argument(
        "--priority",
        type=str,
        choices=["high", "medium", "low", "all"],
        default="all",
        help="Generate issues only for specific priority level (default: all)",
    )

    args = parser.parse_args()

    # Ensure output directory exists
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all class files
    classes_dir = Path(args.classes_dir)
    if not classes_dir.exists():
        print(f"❌ Classes directory not found: {classes_dir}")
        return 1

    print(f"🔍 Scanning classes directory: {classes_dir}")
    class_files = find_class_files(classes_dir)

    # Filter by priority if specified
    if args.priority != "all":
        class_files = [cf for cf in class_files if cf.priority == args.priority]

    print(f"📝 Found {len(class_files)} class files to process")

    # Generate issues
    generated_count = 0
    for class_info in class_files:
        issue_content = generate_issue_content(class_info)

        # Write to file
        output_file = output_dir / f"issue_{class_info.class_name}.md"
        output_file.write_text(issue_content, encoding="utf-8")

        print(
            f"✅ Generated issue for {class_info.class_name} (priority: {class_info.priority})"
        )
        generated_count += 1

    print(f"\n🎉 Successfully generated {generated_count} issue files in {output_dir}")
    print("\n📋 Next steps:")
    print("1. Review the generated issue files")
    print("2. Manually create GitHub issues from these templates")
    print("3. Or use GitHub CLI to bulk import: gh issue create --body-file ISSUE_FILE")

    # Print priority summary
    print("\n📊 Priority Summary:")
    priority_counts = {"high": 0, "medium": 0, "low": 0}
    for cf in class_files:
        priority_counts[cf.priority] += 1

    for priority in ["high", "medium", "low"]:
        count = priority_counts[priority]
        if count > 0:
            print(f"  {priority.upper()}: {count} classes")

    return 0


if __name__ == "__main__":
    exit(main())
