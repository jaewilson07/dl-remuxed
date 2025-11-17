# Using GitHub Copilot Coding Agent for RouteContext Migration

## Overview

This guide explains how to use GitHub Copilot's coding agent to systematically migrate 110 modules (55 routes + 55 classes) to the RouteContext pattern.

## Prerequisites

- GitHub repository with Copilot enabled
- Issue tracking enabled
- Copilot coding agent access (#github-pull-request_copilot-coding-agent)

## Quick Start

### 1. Generate Issue Templates

Already done! Issue templates are in `scripts/issues/`:
- 55 route migration issues (route-*.json)
- 55 class migration issues (class-*.json)

### 2. Create Issues with PowerShell Helper

```powershell
cd external\dl-remuxed\scripts

# See high-priority issues
.\create_migration_issues.ps1 -Priority high

# Interactive mode - opens files and copies to clipboard
.\create_migration_issues.ps1 -Priority "route-dataset.core.json"

# See all available issues
.\create_migration_issues.ps1 -Priority all
```

### 3. Create GitHub Issue

For each module you want to migrate:

1. **Create new issue** in GitHub
2. **Copy title** from the JSON file (e.g., `[HIGH] [RouteContext] Migrate routes/dataset/core.py (6 functions)`)
3. **Paste body** from the JSON file (full description with migration pattern)
4. **Add the magic tag**: `#github-pull-request_copilot-coding-agent`
5. **Submit** the issue

### 4. Copilot Coding Agent Takes Over

Once you submit the issue with the tag:
- ✅ Copilot creates a new branch automatically
- ✅ Implements the migration following your pattern
- ✅ Runs tests
- ✅ Creates a pull request
- ✅ Links PR back to the issue

### 5. Review and Merge

When Copilot finishes:
- Review the PR
- Check that all functions/methods were migrated
- Verify tests pass
- Merge the PR
- Issue auto-closes

## Recommended Order

### Phase 1: High-Priority Routes (Week 1)

Create issues for these first (marked with [HIGH]):

1. `route-user.core.json` (10 functions)
2. `route-dataset.core.json` (6 functions) ⭐ **Start here**
3. `route-dataset.upload.json` (7 functions)
4. `route-group.json` (13 functions)
5. `route-page.core.json` (3 functions)
6. `route-card.json` (4 functions)

**Why these first?** Most frequently used routes = biggest impact

### Phase 2: Core Entity Classes (Week 2)

After routes are done, tackle the classes:

1. `class-DomoUser.json` (19 methods)
2. `class-DomoDataset.dataset_default.json` (4 methods)
3. `class-DomoDataset.dataset_data.json` (6 methods)
4. `class-DomoGroup.core.json` (9 methods)
5. `class-DomoPage.core.json` (5 methods)
6. `class-DomoCard.card_default.json` (6 methods)

### Phase 3: Remaining Modules (Weeks 3-6)

Batch remaining routes and classes:
- Authentication & Config routes
- Data operations (dataflow, stream, filesets)
- Advanced features (publish, workflows, jupyter)
- Specialized classes (DomoEverywhere, DomoCodeEngine)

## Tips for Success

### Batch Processing

Create 3-5 issues at a time:
```powershell
# Create issues for routes 1-5
# Wait for PRs
# Review and merge
# Create next batch
```

### Monitor Progress

Track in `TO_DOS/index.md`:
- Update completion status after each merge
- Run `python scripts/generate-context-migration-todos.py` to refresh

### Handle Failures

If Copilot gets stuck:
- Check the error in PR comments
- Close the PR and issue
- Manually fix the issue
- Create a new issue with adjusted instructions

## Example Workflow

```powershell
# Day 1: Start with dataset.core
cd external\dl-remuxed\scripts
.\create_migration_issues.ps1 -Priority "route-dataset.core.json"

# Copy body to clipboard, create GitHub issue with:
# Title: [HIGH] [RouteContext] Migrate routes/dataset/core.py (6 functions)
# Body: [paste from clipboard]
# Tag: #github-pull-request_copilot-coding-agent

# Day 2: Review PR from Copilot
# - Check all 6 functions migrated
# - Verify tests pass
# - Merge PR

# Day 3: Create issues for next 3 modules
.\create_migration_issues.ps1 -Priority "route-user.core.json"
# ...repeat for dataset.upload and group

# Week 2: Move to classes
.\create_migration_issues.ps1 -Priority "class-DomoUser.json"
```

## Troubleshooting

### Issue: Copilot doesn't start working

- ✅ Verify tag is exactly: `#github-pull-request_copilot-coding-agent`
- ✅ Check Copilot is enabled for your repo
- ✅ Wait 1-2 minutes after creating issue

### Issue: Copilot makes incorrect changes

- Review the migration pattern in the issue body
- Check if reference file path is correct
- Manually fix and close the PR
- Update issue template if needed

### Issue: Tests fail in PR

- Most likely: Route function signature doesn't match pattern
- Check that `*,` is used to make params keyword-only
- Verify RouteContext import is present

## Progress Tracking

After each merge:

1. Update `TO_DOS/routes/[module].md` or `TO_DOS/classes/[module].md`
2. Check off completed functions/methods
3. Mark PR as merged in status section
4. Update `TO_DOS/index.md` with new counts

Regenerate TODO files periodically:
```powershell
python scripts\generate-context-migration-todos.py
```

## Success Metrics

Track weekly:
- Routes migrated: X/55 modules
- Classes migrated: X/55 modules
- Total functions updated: X/287
- Total methods updated: X/325
- PRs merged: X/110

Target: Complete in 6-8 weeks

## Questions?

See `code_review/route-context-implementation-plan.md` for full details on:
- Migration patterns
- Testing strategy
- Deprecation timeline
- Logging integration
