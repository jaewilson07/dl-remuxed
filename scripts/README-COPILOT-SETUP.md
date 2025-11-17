# GitHub Copilot Coding Agent - RouteContext Migration Setup

## ✅ What's Been Created

I've set up everything you need to use GitHub Copilot's coding agent for the RouteContext migration:

### 1. **110 Issue Templates** (`scripts/issues/`)
- 55 route migration issues (route-*.json)
- 55 class migration issues (class-*.json)
- Each with complete migration instructions and patterns

### 2. **PowerShell Helper Script** (`scripts/create_migration_issues.ps1`)
- Interactive tool to create issues
- Copies issue body to clipboard
- Shows high-priority items first

### 3. **Complete Guide** (`docs/COPILOT-AGENT-GUIDE.md`)
- Step-by-step instructions
- Recommended migration order
- Troubleshooting tips
- Progress tracking

## 🚀 How to Use

### Quick Start (5 minutes)

```powershell
# 1. Navigate to scripts directory
cd c:\GitHub\change_mgmt\external\dl-remuxed\scripts

# 2. See what high-priority issues look like
.\create_migration_issues.ps1 -Priority high -DryRun

# 3. Get the first issue ready to create
.\create_migration_issues.ps1 -Priority "route-dataset.core.json"
# This copies the issue body to your clipboard
```

### Create Your First Issue

1. Go to your GitHub repository
2. Click "New Issue"
3. Paste title: `[HIGH] [RouteContext] Migrate routes/dataset/core.py (6 functions)`
4. Paste body from clipboard (full migration instructions)
5. **Add this tag**: `#github-pull-request_copilot-coding-agent`
6. Click "Submit"

### What Happens Next

- ✅ GitHub Copilot coding agent sees the tag
- ✅ Creates a branch automatically
- ✅ Implements all 6 functions following your pattern
- ✅ Runs tests
- ✅ Opens a PR with all changes
- ✅ You review and merge!

## 📋 Recommended First Batch

Start with these 6 high-priority routes (43 functions total):

1. **dataset.core** (6 functions) ⭐ Start here - currently blocking your test
2. **user.core** (10 functions)
3. **dataset.upload** (7 functions)
4. **group** (13 functions)
5. **page.core** (3 functions)
6. **card** (4 functions)

Create all 6 issues at once, Copilot will work on them in parallel!

## 🎯 Your Immediate Next Step

To unblock your `can_authenticate_onepass.py` test:

```powershell
# Create the dataset.core migration issue
cd c:\GitHub\change_mgmt\external\dl-remuxed\scripts
.\create_migration_issues.ps1 -Priority "route-dataset.core.json"

# Then create GitHub issue with:
# - Title and body from clipboard
# - Tag: #github-pull-request_copilot-coding-agent
```

Within 10-15 minutes, Copilot should have a PR ready with all 6 dataset.core functions properly migrated!

## 📚 Full Documentation

- **Implementation Plan**: `code_review/route-context-implementation-plan.md`
- **Copilot Agent Guide**: `docs/COPILOT-AGENT-GUIDE.md`
- **Progress Tracking**: `TO_DOS/index.md`

## ❓ Can't Use Copilot Agent?

If you don't have access to the coding agent, you can still use the issue templates as:
- Task lists for manual implementation
- PR descriptions
- Code review checklists

## 🎉 Benefits

- **Automated**: Copilot does the repetitive work
- **Consistent**: All migrations follow the same pattern
- **Tested**: Each PR includes test verification
- **Tracked**: Issues and PRs provide full audit trail
- **Fast**: Can process 5-10 modules per day

## Summary

You have 110 ready-to-use issue templates that will guide GitHub Copilot to migrate your entire codebase. Just create issues with the `#github-pull-request_copilot-coding-agent` tag and let Copilot do the work!
