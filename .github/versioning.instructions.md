# Semantic Versioning Guide

This repository uses automated semantic versioning via GitHub Actions. When a PR is merged to `main`, the version is automatically bumped based on PR labels.

## How It Works

### 1. Add Labels to Your PR

Before merging a PR to `main`, add appropriate labels:

#### Version Bump Labels (required - choose one):

| Label                         | Bump Type             | Example       | Use Case                                   |
| ----------------------------- | --------------------- | ------------- | ------------------------------------------ |
| `major`                       | Major version (x.0.0) | 0.1.5 → 1.0.0 | Breaking changes, major API changes        |
| `feat`                        | Minor version (0.x.0) | 0.1.5 → 0.2.0 | New features, backward-compatible changes  |
| `fix`, `patch`, or `refactor` | Patch version (0.0.x) | 0.1.5 → 0.1.6 | Bug fixes, refactoring, small improvements |

**Default:** If no bump label is present, defaults to `patch`.

#### Release Stage Labels (optional):

| Label      | Suffix      | Example                   | Use Case                        | Published to PyPI? |
| ---------- | ----------- | ------------------------- | ------------------------------- | ------------------ |
| `alpha`    | `-alpha`    | 0.1.0-alpha               | Early development, unstable     | ❌ No              |
| `beta`     | `-beta`     | 0.1.0-beta                | Feature complete, testing phase | ✅ Yes             |
| `stable`   | (none)      | 0.1.0                     | Production-ready release        | ✅ Yes             |
| (no label) | (preserved) | Current suffix maintained | Continue in current stage       | Depends on suffix  |

### 2. Merge the PR

When you merge the PR to `main`, the workflow automatically:

1. ✅ Detects the PR labels
2. ✅ Calculates the new version
3. ✅ Updates `pyproject.toml` and `src/domolibrary2/__init__.py`
4. ✅ Commits the version bump
5. ✅ Creates a git tag (e.g., `v0.1.0-alpha`)
6. ✅ Creates a GitHub Release
7. ✅ Publishes to PyPI (only for `beta` and `stable` releases, **alpha is skipped**)

## Examples

### Example 1: Bug Fix in Alpha

**Current version:** `0.0.1-alpha`
**PR labels:** `fix`
**New version:** `0.0.2-alpha`

### Example 2: New Feature, Move to Beta

**Current version:** `0.0.5-alpha`
**PR labels:** `feat`, `beta`
**New version:** `0.1.0-beta`

### Example 3: Bug Fix in Beta (stays in Beta)

**Current version:** `0.1.0-beta`
**PR labels:** `patch`
**New version:** `0.1.1-beta`

### Example 4: Code Refactoring in Alpha

**Current version:** `0.0.3-alpha`
**PR labels:** `refactor`
**New version:** `0.0.4-alpha`

### Example 5: Feature Ready for Stable Release

**Current version:** `0.1.5-beta`
**PR labels:** `feat`, `stable`
**New version:** `0.2.0` (stable release)

### Example 6: Breaking Change

**Current version:** `0.9.5`
**PR labels:** `major`
**New version:** `1.0.0`

### Example 7: Breaking Change, Back to Alpha Testing

**Current version:** `1.2.3`
**PR labels:** `major`, `alpha`
**New version:** `2.0.0-alpha`

## Best Practices

### 🏷️ Label Guidelines

1. **Always add a version bump label** (`major`, `feat`, `fix`/`patch`/`refactor`) to PRs
2. **Add stage label when changing release stage** (e.g., moving from `alpha` to `beta`)
3. **Omit stage label** when staying in the current stage
4. **Use `stable` label** only when ready for production release
5. **Alpha releases are NOT published to PyPI** - only beta and stable releases are published

### 📝 Workflow

```
Development Flow:
├── Start: 0.0.1-alpha
├── Bug fixes: 0.0.2-alpha, 0.0.3-alpha (fix + alpha)
├── Refactoring: 0.0.4-alpha (refactor + alpha)
├── New feature: 0.1.0-alpha (feat + alpha)
├── Move to beta: 0.2.0-beta (feat + beta)
├── Beta testing: 0.2.1-beta, 0.2.2-beta (patch + beta)
├── Stable release: 0.3.0 (feat + stable)
├── Patches: 0.3.1, 0.3.2 (patch)
└── Major v2: 2.0.0 (major + stable)
```

### 🚫 What NOT to Do

-   ❌ Don't manually edit version in `pyproject.toml` or `src/domolibrary2/__init__.py`
-   ❌ Don't create tags manually
-   ❌ Don't skip labels on PRs merged to main
-   ❌ Don't use multiple bump labels (e.g., major + feat, fix + refactor)

## Troubleshooting

### Workflow didn't run

-   **Check:** Was the PR merged to `main` branch?
-   **Check:** Does the PR have appropriate labels?

### Wrong version bump

-   **Fix:** The workflow uses the first matching label in priority order: `major` > `feat` > `fix`/`patch`/`refactor`
-   **Solution:** Ensure only one bump label is applied

### Version conflict

-   **Cause:** Manual version edit or concurrent merges
-   **Fix:** Pull latest changes, resolve conflicts, and re-push

## Manual Version Override

If you need to manually set a version:

1. Edit `pyproject.toml` and `src/domolibrary2/__init__.py`
2. Commit: `git commit -m "chore: set version to X.Y.Z"`
3. Tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
4. Push: `git push && git push --tags`

The workflow will use this as the base for the next automatic bump.

## Checking Current Version

```bash
# From command line
grep "version = " pyproject.toml

# From Python
import domolibrary2
print(domolibrary2.__version__)
```

## Questions?

If you have questions about versioning, check the [workflow file](workflows/semver-autotag.yml) or open an issue.
