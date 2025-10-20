# Development Scripts for domolibrary

This folder contains PowerShell scripts for common development tasks.

## Scripts

### `setup-dev.ps1`
Sets up the development environment by installing dependencies and pre-commit hooks.

```powershell
.\scripts\setup-dev.ps1
```

### `lint.ps1`
Runs all linting and formatting tools (ruff, black, isort, pylint, mypy).

```powershell
.\scripts\lint.ps1
```

### `test.ps1`
Runs the test suite with coverage reporting.

```powershell
.\scripts\test.ps1
```

### `build.ps1`
Builds the package for distribution.

```powershell
.\scripts\build.ps1
```

### `publish.ps1`
Publishes the package to PyPI. Includes pre-publish checks.

```powershell
# Publish to main PyPI
.\scripts\publish.ps1

# Publish to test PyPI
.\scripts\publish.ps1 -TestPyPI
```

## Requirements

- PowerShell 5.1 or later
- `uv` package manager installed
- Development dependencies installed (`uv sync --dev`)

## Alternative: Manual Commands

If you prefer to run commands manually, see the main README.md for individual `uv run` commands.