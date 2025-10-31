# Pre-commit Error Parser

This script extracts and organizes errors from `precommit_errors.txt` into structured formats for easier resolution.

## Usage

```bash
# Parse errors from default location (../precommit_errors.txt)
python scripts/parse_precommit_errors.py

# Or specify a custom path
python scripts/parse_precommit_errors.py path/to/error_file.txt
```

## Outputs

The script generates three outputs:

1. **Console Summary** - Overview of errors by type and file
2. **`precommit_errors.json`** - Structured JSON for programmatic access
3. **`precommit_errors.md`** - Markdown formatted list grouped by file

## Error Structure

Each error contains:
- `file_path`: Path to the file with the error
- `line`: Line number
- `column`: Column number
- `error_code`: Error code (F401, N813, E722, etc.)
- `message`: Description of the error
- `hook`: Pre-commit hook that detected it (ruff, check-yaml, etc.)
- `context`: Code context lines (if available)

## Example Output

```
TOTAL ERRORS: 161

ERRORS BY TYPE:
  F401: 15  (unused imports)
  F821: 3   (undefined name)
  F822: 1   (undefined name in __all__)
  N802: 2   (function name should be lowercase)
  N813: 13  (camelcase imported as lowercase)
  N815: 1   (mixedCase variable)
  N999: 9   (invalid module name)
  E402: 1   (module import not at top)
  E721: 1   (type comparison)
  E722: 1   (bare except)
  YAML: 1   (yaml syntax error)

ERRORS BY FILE:
  src/domolibrary2/classes/DomoCodeEngine/CodeEngine.py: 30
  src/domolibrary2/classes/DomoDataset.py: 15
  src/domolibrary2/classes/DomoUser.py: 12
  ...
```

## Integration with GitHub Copilot

The structured output makes it easy to iterate over errors systematically:

1. **By Error Type**: Fix all errors of one type (e.g., all F401 unused imports)
2. **By File**: Fix all errors in one file at a time
3. **By Priority**: Address critical errors first (F821, F822)

### Recommended Fix Order:

1. **F821, F822** - Undefined names (breaks code)
2. **YAML** - Syntax errors (breaks CI)
3. **F401** - Unused imports (cleanup)
4. **N813** - Import naming conventions (style)
5. **N999** - Module naming (style)
6. **N802, N815** - Function/variable naming (style)
7. **E402, E721, E722** - Code quality improvements

## Example Copilot Prompts

```
"Fix all F401 unused import errors in src/domolibrary2/__init__.py"

"Fix all N813 camelcase import naming in src/domolibrary2/classes/DomoCard.py"

"Fix the YAML syntax error in .github/workflows/pre-commit.yml line 30"

"Fix all undefined name errors (F821/F822) in DomoApplication/Application.py"
```

## Filtering Errors

You can modify the script to filter specific error types:

```python
# Filter only unused imports
unused_imports = [e for e in errors if e.error_code == "F401"]

# Filter errors in specific directory
class_errors = [e for e in errors if "classes" in e.file_path]

# Filter by hook
ruff_errors = [e for e in errors if e.hook == "ruff"]
```
