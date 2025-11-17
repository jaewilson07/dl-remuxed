# Batch Create GitHub Issues from JSON Templates
# Requires GitHub CLI (gh) to be installed and authenticated

param(
    [Parameter(Mandatory=$false)]
    [string]$Filter = "all",  # "high", "routes", "classes", or "all"

    [Parameter(Mandatory=$false)]
    [int]$Limit = 0,  # 0 = no limit, otherwise create only N issues

    [Parameter(Mandatory=$false)]
    [switch]$DryRun = $false
)

# Check if gh CLI is installed
$ghInstalled = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghInstalled) {
    Write-Host "❌ GitHub CLI (gh) is not installed" -ForegroundColor Red
    Write-Host ""
    Write-Host "Install it with:" -ForegroundColor Yellow
    Write-Host "  winget install GitHub.cli" -ForegroundColor White
    Write-Host "  or visit: https://cli.github.com/" -ForegroundColor White
    exit 1
}

# Check if gh is authenticated
$authStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ GitHub CLI is not authenticated" -ForegroundColor Red
    Write-Host ""
    Write-Host "Authenticate with:" -ForegroundColor Yellow
    Write-Host "  gh auth login" -ForegroundColor White
    exit 1
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$IssuesDir = Join-Path $ScriptDir "issues"

Write-Host "🤖 Batch Create GitHub Issues - RouteContext Migration" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Get issue files based on filter
$issueFiles = @()
switch ($Filter.ToLower()) {
    "high" {
        Write-Host "📋 Filter: High-priority routes only" -ForegroundColor Yellow
        $highPriorityRoutes = @(
            "route-user.core.json",
            "route-dataset.core.json",
            "route-dataset.upload.json",
            "route-group.json",
            "route-page.core.json",
            "route-card.json"
        )
        foreach ($file in $highPriorityRoutes) {
            $path = Join-Path $IssuesDir $file
            if (Test-Path $path) {
                $issueFiles += Get-Item $path
            }
        }
    }
    "routes" {
        Write-Host "📋 Filter: All route modules" -ForegroundColor Yellow
        $issueFiles = Get-ChildItem -Path $IssuesDir -Filter "route-*.json"
    }
    "classes" {
        Write-Host "📋 Filter: All class modules" -ForegroundColor Yellow
        $issueFiles = Get-ChildItem -Path $IssuesDir -Filter "class-*.json"
    }
    "all" {
        Write-Host "📋 Filter: All modules (routes + classes)" -ForegroundColor Yellow
        $issueFiles = Get-ChildItem -Path $IssuesDir -Filter "*.json" | Where-Object { $_.Name -ne "all_issues.json" }
    }
    default {
        Write-Host "❌ Invalid filter: $Filter" -ForegroundColor Red
        Write-Host "Valid options: high, routes, classes, all" -ForegroundColor Yellow
        exit 1
    }
}

if ($Limit -gt 0) {
    $issueFiles = $issueFiles | Select-Object -First $Limit
    Write-Host "📊 Limiting to first $Limit issues" -ForegroundColor Yellow
}

Write-Host "📝 Found $($issueFiles.Count) issues to create" -ForegroundColor Green
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No issues will be created" -ForegroundColor Yellow
    Write-Host ""
}

$created = 0
$failed = 0
$skipped = 0

foreach ($issueFile in $issueFiles) {
    $issue = Get-Content $issueFile.FullName | ConvertFrom-Json

    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "📄 $($issueFile.Name)" -ForegroundColor Cyan
    Write-Host "   Title: $($issue.title)" -ForegroundColor White
    Write-Host "   Labels: $($issue.labels -join ', ')" -ForegroundColor DarkGray

    if ($DryRun) {
        Write-Host "   [DRY RUN] Would create this issue" -ForegroundColor Yellow
        $skipped++
    } else {
        try {
            # Create the issue with gh CLI
            # Add the copilot agent tag to the body
            $bodyWithTag = $issue.body + "`n`n#github-pull-request_copilot-coding-agent"

            # Create a temp file for the body (gh cli reads from file for long content)
            $tempFile = [System.IO.Path]::GetTempFileName()
            $bodyWithTag | Out-File -FilePath $tempFile -Encoding UTF8

            # Create the issue
            $labelArgs = $issue.labels | ForEach-Object { "--label", $_ }
            $result = gh issue create `
                --title $issue.title `
                --body-file $tempFile `
                @labelArgs `
                2>&1

            # Clean up temp file
            Remove-Item $tempFile -ErrorAction SilentlyContinue

            if ($LASTEXITCODE -eq 0) {
                Write-Host "   ✓ Created: $result" -ForegroundColor Green
                $created++

                # Add a small delay to avoid rate limiting
                Start-Sleep -Milliseconds 500
            } else {
                Write-Host "   ✗ Failed: $result" -ForegroundColor Red
                $failed++
            }
        } catch {
            Write-Host "   ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
            $failed++
        }
    }

    Write-Host ""
}

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Summary:" -ForegroundColor Cyan
Write-Host "   ✓ Created: $created" -ForegroundColor Green
Write-Host "   ✗ Failed: $failed" -ForegroundColor Red
if ($DryRun) {
    Write-Host "   ⊘ Skipped (dry run): $skipped" -ForegroundColor Yellow
}
Write-Host ""

if ($DryRun) {
    Write-Host "💡 To actually create issues, run without -DryRun flag" -ForegroundColor Yellow
} else {
    Write-Host "🎉 Done! Check your GitHub repository for the new issues" -ForegroundColor Green
    Write-Host "   GitHub Copilot coding agent will start working on them automatically" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Go to your GitHub repository issues page" -ForegroundColor White
Write-Host "  2. Wait 1-2 minutes for Copilot to pick up the issues" -ForegroundColor White
Write-Host "  3. Monitor PRs as they're created" -ForegroundColor White
Write-Host "  4. Review and merge completed PRs" -ForegroundColor White
