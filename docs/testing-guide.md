# Testing Guide

> High-level reference for how tests in this repository are structured and executed.

## Overview

This project uses `pytest` with async tests and environment-based configuration to validate domolibrary2.

- Tests live under the `tests/` directory (organized by domain: classes, routes, client, integrations, tools, utils).
- Tests rely on environment variables configured in a local `.env` file.
- Authentication in tests typically uses `DomoTokenAuth` from `domolibrary2.auth`.

For detailed testing patterns (naming conventions, fixtures, markers, and examples), see:
- `.github/instructions/tests.instructions.md`

## Running Tests

Typical commands (from the repo root):

```powershell
# Run all tests
pytest tests/ -v

# Run a single module
pytest tests/classes/test_50_DomoUser.py -v

# Run via helper script (includes coverage)
./scripts/test.ps1
```

See `tests.instructions.md` for more patterns and recommendations.
