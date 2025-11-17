# Version Management

## Overview

The domolibrary2 package uses **automatic version synchronization** between `pyproject.toml` and `__init__.py`. You only need to update the version in one place.

## Single Source of Truth

**Version is defined in:** `pyproject.toml`

```toml
[project]
name = "domolibrary2"
version = "2.0.2-beta"
```

## How It Works

The `src/domolibrary2/__init__.py` file automatically reads the version from `pyproject.toml` at import time.

### Version Resolution Order

1. **Read from pyproject.toml** (preferred - always current)
2. **Fallback to package metadata** (if pyproject.toml not found)
3. **Return "unknown"** (if all methods fail)

## Updating the Version

### ✅ Correct Way

Edit `pyproject.toml`:

```toml
[project]
version = "2.1.0"
```

That's it! The change is immediately reflected in the package.

### ❌ Incorrect Way

~~Don't manually edit `__init__.py`~~ - The version will be overwritten by the automatic sync.

## Version Formats

Follow [PEP 440](https://peps.python.org/pep-0440/) for version numbering:

### Release Versions
- `1.0.0` - Major release
- `1.1.0` - Minor release
- `1.1.1` - Patch release

### Pre-release Versions
- `2.0.0-alpha` - Alpha release
- `2.0.0-beta` - Beta release
- `2.0.0-rc1` - Release candidate

### Development Versions
- `2.0.0.dev0` - Development version

## Checking Version

### From Python

```python
import domolibrary2
print(domolibrary2.__version__)
# Output: 2.0.2-beta
```

### From Command Line

```bash
python -c "import domolibrary2; print(domolibrary2.__version__)"
```

## Benefits

✅ **Single source of truth** - Only update in one place
✅ **No build-time scripts** - Works immediately
✅ **Always synchronized** - No version mismatches
✅ **Development friendly** - Works in editable installs
✅ **Distribution ready** - Works in built packages

## Version Bump Workflow

```bash
# 1. Edit version in pyproject.toml
version = "2.1.0-beta"

# 2. Test the change
python -c "import domolibrary2; print(domolibrary2.__version__)"

# 3. Commit
git add pyproject.toml
git commit -m "Bump version to 2.1.0-beta"

# 4. Tag (optional)
git tag v2.1.0-beta
git push origin v2.1.0-beta
```

## Troubleshooting

### Version shows "unknown"

**Cause**: `pyproject.toml` not found and package not installed
**Fix**: Ensure you're in the project directory or package is installed

### Version not updating

**Cause**: Python cached the imported module
**Fix**: Restart Python interpreter

## Summary

**TL;DR**: Just update the version in `pyproject.toml`. Everything else is automatic!

```toml
# pyproject.toml
[project]
version = "2.1.0"  # ← Only place to update!
```
