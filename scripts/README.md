> Last updated: 2025-11-05

# Development Scripts for domolibrary2

This folder contains PowerShell scripts for common development tasks.

## Available Scripts

### `setup-dev.ps1`
Sets up the development environment by installing dependencies and pre-commit hooks.

```powershell
.\scripts\setup-dev.ps1
```

**What it does:**
- Installs all project dependencies using `uv sync --dev`
- Sets up pre-commit hooks for automated code quality checks

---

### `format-code.ps1`
Manual code formatting script for use when pre-commit hooks have issues.

```powershell
.\scripts\format-code.ps1
```

**What it does:**
- Checks Python syntax for all files in `src/`
- Runs Black formatter
- Runs isort for import sorting
- Runs Ruff linter with auto-fix

**Note:** This is a fallback script. Normally, pre-commit hooks handle formatting automatically.

---

### `lint.ps1`
Runs comprehensive linting and type checking on the codebase.

```powershell
.\scripts\lint.ps1
```

**What it does:**
- Runs Ruff linter with auto-fix
- Runs Black formatter
- Runs isort for import organization
- Runs Pylint for code quality checks
- Runs mypy for type checking

---

### `test.ps1`
Runs the full test suite with coverage reporting.

```powershell
.\scripts\test.ps1
```

**What it does:**
- Runs pytest on all tests in `tests/` directory
- Generates coverage report in `htmlcov/` directory
- Displays coverage summary in terminal

---

### `build.ps1`
Builds the package for distribution.

```powershell
.\scripts\build.ps1
```

**What it does:**
- Cleans previous build artifacts from `dist/` folder
- Builds wheel and source distribution using `uv build`
- Outputs build artifacts to `dist/` folder

---

### `publish.ps1`
Publishes the package to PyPI (includes pre-publish validation).

```powershell
# Publish to main PyPI
.\scripts\publish.ps1

# Publish to test PyPI (for testing)
.\scripts\publish.ps1 -TestPyPI
```

**What it does:**
1. Runs full linting checks (`lint.ps1`)
2. Runs full test suite (`test.ps1`)
3. Builds the package (`build.ps1`)
4. Publishes to PyPI or TestPyPI
5. Exits early if any checks fail

**Warning:** Only run this when you're ready to publish a new version!

---

## Requirements

- **PowerShell 5.1 or later**
- **uv** package manager installed and in PATH
- Development dependencies installed via `uv sync --dev`

## Quick Start

```powershell
# First time setup
.\scripts\setup-dev.ps1

# Make changes to code...

# Before committing (optional - pre-commit does this automatically)
.\scripts\lint.ps1

# Run tests
.\scripts\test.ps1

# Build package locally
.\scripts\build.ps1

# Publish new version (maintainers only)
.\scripts\publish.ps1
```

## Alternative: Manual Commands

If you prefer to run commands manually without scripts:

```powershell
# Install dependencies
uv sync --dev

# Run linting
uv run ruff check src --fix
uv run black src
uv run isort src

# Run tests
uv run pytest tests/ --cov=src

# Build package
uv build

# Publish
uv publish
```

## Troubleshooting

### Script Execution Policy
If you get an error about script execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### UV Not Found
Ensure `uv` is installed and in your PATH:
```powershell
# Install uv (if not installed)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Pre-commit Hook Issues
If pre-commit hooks are causing problems:
```powershell
# Use the manual formatting script instead
.\scripts\format-code.ps1
```
