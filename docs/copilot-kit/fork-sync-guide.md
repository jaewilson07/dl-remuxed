> Last updated: 2025-11-17

# Fork Synchronization Guide

This repository is a fork of [`ikcode-dev/copilot-kit`](https://github.com/ikcode-dev/copilot-kit) and is automatically kept up to date with the upstream repository.

## Automatic Synchronization

The fork is automatically synchronized with the upstream repository using a GitHub Actions workflow that:

- **Runs daily** at 2:00 AM UTC
- **Can be triggered manually** from the GitHub Actions tab
- **Automatically merges** changes from the upstream `main` branch
- **Stops if conflicts are detected**, requiring manual resolution

## How It Works

The workflow (`.github/workflows/sync-upstream.yml`) performs the following steps:

1. Checks out the repository with full git history
2. Configures git with GitHub Actions bot credentials
3. Adds the upstream remote (`ikcode-dev/copilot-kit`)
4. Fetches the latest changes from upstream
5. Checks out the `main` branch
6. Merges upstream changes (if no conflicts)
7. Pushes the updated branch back to the fork

## Manual Synchronization

If you need to sync the fork manually:

### Using GitHub UI

1. Go to the [Actions tab](../../actions/workflows/sync-upstream.yml)
2. Click on "Sync Fork with Upstream" workflow
3. Click "Run workflow" button
4. Select the branch and click "Run workflow"

### Using Git Command Line

```bash
# Add upstream remote (if not already added)
git remote add upstream https://github.com/ikcode-dev/copilot-kit.git

# Fetch upstream changes
git fetch upstream

# Checkout your main branch
git checkout main

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main
```

## Handling Merge Conflicts

If the automatic sync fails due to merge conflicts:

1. You'll receive a notification (if you have Actions notifications enabled)
2. Follow the manual synchronization steps above
3. Resolve conflicts locally:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   # Resolve conflicts in your editor
   git add .
   git commit
   git push origin main
   ```

## Customization

You can customize the sync schedule by editing `.github/workflows/sync-upstream.yml`:

- Change the `cron` schedule (currently `'0 2 * * *'` for daily at 2 AM UTC)
- Modify which branch to sync (currently `main`)
- Add notifications or additional steps as needed

## Benefits

✅ Always stay up to date with the latest prompts and improvements  
✅ Automatic process requires no manual intervention  
✅ Safe merging with conflict detection  
✅ Manual trigger option when needed  
✅ Full transparency through GitHub Actions logs
