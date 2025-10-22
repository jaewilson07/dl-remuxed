#!/usr/bin/env powershell
# Script to help implement type hints systematically

param(
    [Parameter(HelpMessage="Start from a specific directory (classes, client, routes, utils, integrations)")]
    [ValidateSet("classes", "client", "routes", "utils", "integrations")]
    [string]$StartFrom = "classes",

    [Parameter(HelpMessage="Process only a specific file")]
    [string]$File = "",

    [Parameter(HelpMessage="Dry run - show what would be processed")]
    [switch]$DryRun
)

Write-Host "Type Hints Implementation Helper" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

if (-not (Test-Path "type-hints-implementation-guide.md")) {
    Write-Error "Implementation guide not found. Run: python scripts\generate-type-hints-guide.py first"
    exit 1
}

# Priority order for processing
$directories = @("classes", "client", "routes", "utils", "integrations")
$startIndex = $directories.IndexOf($StartFrom)

if ($startIndex -eq -1) {
    Write-Error "Invalid start directory: $StartFrom"
    exit 1
}

$targetDirectories = $directories[$startIndex..($directories.Length - 1)]

Write-Host "Processing directories in order: $($targetDirectories -join ', ')" -ForegroundColor Cyan

foreach ($dir in $targetDirectories) {
    $dirPath = "src\$dir"

    if (-not (Test-Path $dirPath)) {
        Write-Host "Directory $dirPath not found, skipping..." -ForegroundColor Yellow
        continue
    }

    Write-Host "`nProcessing $dir directory..." -ForegroundColor Green

    $pythonFiles = Get-ChildItem -Path $dirPath -Filter "*.py" -Recurse | Where-Object { $_.Name -notmatch '^__' }

    if ($File) {
        $pythonFiles = $pythonFiles | Where-Object { $_.Name -eq $File }
        if (-not $pythonFiles) {
            Write-Host "File $File not found in $dirPath" -ForegroundColor Yellow
            continue
        }
    }

    foreach ($file in $pythonFiles) {
        Write-Host "  📄 $($file.Name)" -ForegroundColor White

        if ($DryRun) {
            Write-Host "    [DRY RUN] Would process this file" -ForegroundColor Gray
            continue
        }

        # Check if file needs type hints by looking for it in the guide
        $guideContent = Get-Content "type-hints-implementation-guide.md" -Raw
        $fileName = $file.Name

        if ($guideContent -match "### $fileName") {
            Write-Host "    ⚠️  Needs type hints - check implementation guide" -ForegroundColor Yellow

            # Ask user if they want to open the file for editing
            $response = Read-Host "    Open $fileName for editing? (y/n/s=skip directory/q=quit)"

            switch ($response.ToLower()) {
                'y' {
                    Write-Host "    🔧 Opening $fileName..." -ForegroundColor Blue
                    & code $file.FullName

                    # Wait for user to finish editing
                    Read-Host "    Press Enter when you've finished editing $fileName"

                    # Run a quick syntax check
                    Write-Host "    🔍 Checking syntax..." -ForegroundColor Blue
                    $syntaxCheck = python -m py_compile $file.FullName 2>&1

                    if ($LASTEXITCODE -eq 0) {
                        Write-Host "    ✅ Syntax check passed" -ForegroundColor Green
                    } else {
                        Write-Host "    ❌ Syntax error detected:" -ForegroundColor Red
                        Write-Host "    $syntaxCheck" -ForegroundColor Red
                        Read-Host "    Fix the syntax error and press Enter to continue"
                    }
                }
                's' {
                    Write-Host "    ⏭️  Skipping remaining files in $dir directory" -ForegroundColor Yellow
                    break
                }
                'q' {
                    Write-Host "    🛑 Quitting..." -ForegroundColor Red
                    exit 0
                }
                default {
                    Write-Host "    ⏭️  Skipping $fileName" -ForegroundColor Yellow
                }
            }
        } else {
            Write-Host "    ✅ No type hints needed" -ForegroundColor Green
        }
    }
}

Write-Host "`n🎉 Type hints implementation session complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run linting: .\scripts\lint.ps1" -ForegroundColor White
Write-Host "2. Test imports: python -c 'import src; print(`"Imports work!`")'" -ForegroundColor White
Write-Host "3. Run tests: .\scripts\test.ps1" -ForegroundColor White
