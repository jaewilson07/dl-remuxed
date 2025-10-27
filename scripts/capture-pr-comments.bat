@echo off
REM Batch script to capture PR comments
REM Usage: capture-pr-comments.bat 178

if "%1"=="" (
    echo Usage: capture-pr-comments.bat [PR_NUMBER]
    echo Example: capture-pr-comments.bat 178
    exit /b 1
)

set PR_NUMBER=%1

REM Check if GITHUB_TOKEN is set
if "%GITHUB_TOKEN%"=="" (
    echo Error: GITHUB_TOKEN environment variable not set.
    echo Please set it with your GitHub personal access token:
    echo set GITHUB_TOKEN=your_token_here
    echo.
    echo You can create a token at: https://github.com/settings/tokens
    exit /b 1
)

echo Capturing comments from PR #%PR_NUMBER%...
python scripts\capture_pr_comments.py --pr %PR_NUMBER%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success! Comments saved to ToDo.md
    echo You can now review the file: notepad ToDo.md
) else (
    echo.
    echo Failed to capture comments. Check the error above.
)
