# PowerShell script to capture PR comments
# Usage: .\capture-pr-comments.ps1 178

param(
    [Parameter(Mandatory=$true)]
    [int]$PRNumber
)

# Check if GITHUB_TOKEN is set
if (-not $env:GITHUB_TOKEN) {
    Write-Host "Error: GITHUB_TOKEN environment variable not set." -ForegroundColor Red
    Write-Host "Please set it with your GitHub personal access token:"
    Write-Host "`$env:GITHUB_TOKEN = 'your_token_here'"
    Write-Host ""
    Write-Host "You can create a token at: https://github.com/settings/tokens" -ForegroundColor Yellow
    exit 1
}

Write-Host "Capturing comments from PR #$PRNumber..." -ForegroundColor Green

try {
    python scripts\capture_pr_comments.py --pr $PRNumber

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Success! Comments saved to ToDo.md" -ForegroundColor Green
        Write-Host "You can now review the file with: notepad ToDo.md" -ForegroundColor Yellow
    } else {
        Write-Host ""
        Write-Host "Failed to capture comments. Check the error above." -ForegroundColor Red
    }
} catch {
    Write-Host "Error running script: $_" -ForegroundColor Red
}
