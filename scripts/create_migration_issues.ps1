# Create GitHub Issues for RouteContext Migration
# This script helps you create issues that can be assigned to GitHub Copilot coding agent

param(
    [Parameter(Mandatory=$false)]
    [string]$Priority = "high",  # "high", "all", or specific issue file

    [Parameter(Mandatory=$false)]
    [switch]$DryRun = $false
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$IssuesDir = Join-Path $ScriptDir "issues"

Write-Host "🤖 GitHub Copilot Coding Agent - RouteContext Migration" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

if ($Priority -eq "high") {
    Write-Host "📋 High-Priority Route Migrations:" -ForegroundColor Yellow
    Write-Host ""

    $highPriorityRoutes = @(
        "route-user.core.json",
        "route-dataset.core.json",
        "route-dataset.upload.json",
        "route-group.json",
        "route-page.core.json",
        "route-card.json"
    )

    foreach ($issueFile in $highPriorityRoutes) {
        $filePath = Join-Path $IssuesDir $issueFile
        if (Test-Path $filePath) {
            $issue = Get-Content $filePath | ConvertFrom-Json

            Write-Host "📝 $($issue.title)" -ForegroundColor Green
            Write-Host "   Labels: $($issue.labels -join ', ')" -ForegroundColor DarkGray
            Write-Host ""

            if (!$DryRun) {
                Write-Host "   To create this issue with Copilot coding agent:" -ForegroundColor Cyan
                Write-Host "   1. Create a new GitHub issue with the title and body" -ForegroundColor White
                Write-Host "   2. Add this tag in the issue: #github-pull-request_copilot-coding-agent" -ForegroundColor Yellow
                Write-Host "   3. Copilot will automatically create a branch and start work" -ForegroundColor White
                Write-Host ""
                Write-Host "   Issue body saved to: $filePath" -ForegroundColor DarkGray
                Write-Host ""

                # Option to open in VS Code or copy to clipboard
                $response = Read-Host "   [O]pen file, [C]opy body to clipboard, or [S]kip?"
                switch ($response.ToUpper()) {
                    "O" { code $filePath }
                    "C" {
                        $issue.body | Set-Clipboard
                        Write-Host "   ✓ Issue body copied to clipboard!" -ForegroundColor Green
                    }
                    default { Write-Host "   Skipped." -ForegroundColor DarkGray }
                }
                Write-Host ""
            }
        }
    }

    if ($DryRun) {
        Write-Host ""
        Write-Host "DRY RUN: To actually create issues, run without -DryRun flag" -ForegroundColor Yellow
    }

} elseif ($Priority -eq "all") {
    $allIssues = Get-ChildItem -Path $IssuesDir -Filter "*.json" | Where-Object { $_.Name -ne "all_issues.json" }

    Write-Host "📋 All Migration Issues: $($allIssues.Count) total" -ForegroundColor Yellow
    Write-Host ""

    $routeIssues = $allIssues | Where-Object { $_.Name -like "route-*" }
    $classIssues = $allIssues | Where-Object { $_.Name -like "class-*" }

    Write-Host "Routes: $($routeIssues.Count) modules" -ForegroundColor Cyan
    Write-Host "Classes: $($classIssues.Count) modules" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Use -Priority high to see high-priority issues" -ForegroundColor Yellow
    Write-Host "Or specify a specific issue file with -Priority 'route-dataset.core.json'" -ForegroundColor Yellow

} else {
    # Specific issue file
    $filePath = Join-Path $IssuesDir $Priority
    if (Test-Path $filePath) {
        $issue = Get-Content $filePath | ConvertFrom-Json

        Write-Host "📝 $($issue.title)" -ForegroundColor Green
        Write-Host ""
        Write-Host $issue.body
        Write-Host ""
        Write-Host "Labels: $($issue.labels -join ', ')" -ForegroundColor DarkGray
        Write-Host ""

        if (!$DryRun) {
            $response = Read-Host "Copy issue body to clipboard? [Y/n]"
            if ($response -eq "" -or $response.ToUpper() -eq "Y") {
                $issue.body | Set-Clipboard
                Write-Host "✓ Issue body copied to clipboard!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Next steps:" -ForegroundColor Cyan
                Write-Host "1. Create a new GitHub issue" -ForegroundColor White
                Write-Host "2. Paste the title: $($issue.title)" -ForegroundColor Yellow
                Write-Host "3. Paste the body from clipboard" -ForegroundColor White
                Write-Host "4. Add tag: #github-pull-request_copilot-coding-agent" -ForegroundColor Yellow
                Write-Host "5. Submit and Copilot will start working!" -ForegroundColor Green
            }
        }
    } else {
        Write-Host "❌ Issue file not found: $filePath" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "💡 Tip: Copilot coding agent works best when given one module at a time" -ForegroundColor Yellow
Write-Host "   Start with high-priority routes, then move to classes" -ForegroundColor Yellow
