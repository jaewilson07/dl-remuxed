# Pre-commit Troubleshooting

## Virtualenv/Setuptools Errors

If you encounter virtualenv or setuptools-related errors with pre-commit, here are several solutions:

### Option 1: Use Minimal Pre-commit Configuration

The project includes a minimal pre-commit configuration that uses local system installations instead of creating isolated environments:

```bash
# The current .pre-commit-config.yaml is already optimized for minimal virtualenv usage
pre-commit run --all-files
```

### Option 2: Manual Formatting Scripts

If pre-commit continues to have issues, use the manual formatting scripts:

**Windows (PowerShell):**
```powershell
.\scripts\format-code.ps1
```

**Linux/Mac (Bash):**
```bash
chmod +x scripts/format-code.sh
./scripts/format-code.sh
```

### Option 3: Individual Tool Commands

Run the formatting tools individually:

```bash
# Python syntax check
find src -name "*.py" -exec python -m py_compile {} \;

# Black formatting
python -m black src/

# Import sorting
python -m isort src/ --profile=black

# Ruff linting
python -m ruff check src/ --fix --select=I,F401,F811 --ignore=E501
```

### Option 4: Bypass Pre-commit Temporarily

If you need to commit urgently while pre-commit is having issues:

```bash
git commit -m "your message" --no-verify
```

**Note:** Only use this for urgent commits and run manual formatting afterwards.

### Option 5: Pre-commit Environment Reset

If pre-commit environments are corrupted:

```bash
# Clean pre-commit environments
pre-commit clean

# Reinstall hooks
pre-commit install --install-hooks

# Try again
pre-commit run --all-files
```

### Common Error Solutions

**Error: "failed to build image setuptools"**
- This is usually caused by Windows virtualenv/setuptools conflicts
- Use the manual formatting scripts or local system tools
- The minimal configuration should avoid this issue

**Error: "FileNotFoundError: No such file or directory: '...egg'"**
- This indicates a corrupted virtualenv cache
- Run `pre-commit clean` and try again
- Use manual formatting scripts as fallback

**Error: "Executable 'tool-name' not found"**
- The tool isn't installed in the current environment
- Install missing tools: `pip install black isort ruff bandit`
- Use the manual scripts which check for tool availability

## Configuration Details

The optimized pre-commit configuration:
- Uses `language: system` to avoid creating isolated environments
- Includes `fail_fast: false` to continue on errors
- Has minimal external dependencies
- Includes Python-based implementations of basic hooks

## Development Workflow

1. Try pre-commit first: `pre-commit run --all-files`
2. If errors occur, use manual scripts: `./scripts/format-code.ps1`
3. Check and fix any remaining issues manually
4. Commit with confidence

This approach ensures code quality while avoiding virtualenv-related build issues.