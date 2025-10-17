#!/usr/bin/env powershell
# Interactive @patch_to refactoring helper script

param(
    [Parameter(HelpMessage="Start from a specific directory (client, classes, utils)")]
    [ValidateSet("client", "classes", "utils")]
    [string]$StartFrom = "client",
    
    [Parameter(HelpMessage="Process only a specific file")]
    [string]$File = "",
    
    [Parameter(HelpMessage="Dry run - show what would be processed")]
    [switch]$DryRun
)

Write-Host "@patch_to Refactoring Helper" -ForegroundColor Green
Write-Host "=============================" -ForegroundColor Green

# Check if required files exist
if (-not (Test-Path "patch-to-refactoring-guide.md")) {
    Write-Error "Refactoring guide not found. Run: python scripts\analyze-patch-to.py first"
    exit 1
}

if (-not (Test-Path "PATCH_TO_REFACTOR_INSTRUCTIONS.md")) {
    Write-Error "Refactor instructions not found."
    exit 1
}

# Priority order for processing
$directories = @("client", "classes", "utils")
$startIndex = $directories.IndexOf($StartFrom)

if ($startIndex -eq -1) {
    Write-Error "Invalid start directory: $StartFrom"
    exit 1
}

$targetDirectories = $directories[$startIndex..($directories.Length - 1)]

Write-Host "📋 Processing directories in order: $($targetDirectories -join ', ')" -ForegroundColor Cyan
Write-Host "📖 Reference: patch-to-refactoring-guide.md" -ForegroundColor Gray
Write-Host "📖 Patterns: PATCH_TO_REFACTOR_INSTRUCTIONS.md" -ForegroundColor Gray
Write-Host ""

# Load the refactoring guide content for reference
$guideContent = Get-Content "patch-to-refactoring-guide.md" -Raw

foreach ($dir in $targetDirectories) {
    $dirPath = "src\$dir"
    
    if (-not (Test-Path $dirPath)) {
        Write-Host "Directory $dirPath not found, skipping..." -ForegroundColor Yellow
        continue
    }
    
    Write-Host "🗂️  Processing $dir directory..." -ForegroundColor Green
    
    $pythonFiles = Get-ChildItem -Path $dirPath -Filter "*.py" -Recurse | Where-Object { $_.Name -notmatch '^__' }
    
    if ($File) {
        $pythonFiles = $pythonFiles | Where-Object { $_.Name -eq $File }
        if (-not $pythonFiles) {
            Write-Host "File $File not found in $dirPath" -ForegroundColor Yellow
            continue
        }
    }
    
    foreach ($file in $pythonFiles) {
        Write-Host "`n  📄 $($file.Name)" -ForegroundColor White
        
        # Check if file has @patch_to decorators
        $content = Get-Content $file.FullName -Raw
        $patchToCount = ([regex]::Matches($content, "@patch_to")).Count
        
        if ($patchToCount -eq 0) {
            Write-Host "    ✅ No @patch_to decorators found" -ForegroundColor Green
            continue
        }
        
        Write-Host "    ⚠️  Found $patchToCount @patch_to decorators" -ForegroundColor Yellow
        
        if ($DryRun) {
            Write-Host "    [DRY RUN] Would process this file" -ForegroundColor Gray
            continue
        }
        
        # Show relevant section from guide
        $fileName = $file.Name
        if ($guideContent -match "### $fileName(?:\r?\n)+([^#]+)") {
            Write-Host "    📋 Refactoring plan:" -ForegroundColor Cyan
            $planSection = $matches[1] -split "`n" | Select-Object -First 10
            foreach ($line in $planSection) {
                if ($line.Trim()) {
                    Write-Host "      $line" -ForegroundColor Gray
                }
            }
        }
        
        # Ask user if they want to process this file
        $response = Read-Host "`n    Process $fileName? (y/n/g=show guide/s=skip directory/q=quit)"
        
        switch ($response.ToLower()) {
            'y' {
                Write-Host "    🔧 Opening $fileName for editing..." -ForegroundColor Blue
                
                # Open both the file and the relevant guide section
                & code $file.FullName
                
                # Show key refactoring reminders
                Write-Host "`n    📝 Refactoring Reminders:" -ForegroundColor Cyan
                Write-Host "       1. Move @patch_to methods INSIDE their target classes" -ForegroundColor White
                Write-Host "       2. Remove @patch_to decorators" -ForegroundColor White  
                Write-Host "       3. Add @classmethod for cls_method=True methods" -ForegroundColor White
                Write-Host "       4. Remove 'self: ClassName' type hints" -ForegroundColor White
                Write-Host "       5. Add quotes to return types: -> `"DomoUser`"" -ForegroundColor White
                Write-Host "       6. Keep all method implementations unchanged" -ForegroundColor White
                
                # Wait for user to finish editing
                Read-Host "`n    Press Enter when you've finished refactoring $fileName"
                
                # Validation steps
                Write-Host "    🔍 Running validation checks..." -ForegroundColor Blue
                
                # 1. Syntax check
                $syntaxCheck = python -m py_compile $file.FullName 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "    ✅ Syntax check passed" -ForegroundColor Green
                } else {
                    Write-Host "    ❌ Syntax error detected:" -ForegroundColor Red
                    Write-Host "       $syntaxCheck" -ForegroundColor Red
                    Read-Host "    Fix the syntax error and press Enter to continue"
                }
                
                # 2. Check for remaining @patch_to
                $newContent = Get-Content $file.FullName -Raw
                $remainingPatches = ([regex]::Matches($newContent, "@patch_to")).Count
                if ($remainingPatches -eq 0) {
                    Write-Host "    ✅ All @patch_to decorators removed" -ForegroundColor Green
                } else {
                    Write-Host "    ⚠️  $remainingPatches @patch_to decorators still remain" -ForegroundColor Yellow
                }
                
                # 3. Basic import test
                $modulePath = $file.FullName -replace [regex]::Escape((Get-Location).Path + "\"), "" -replace "\\", "." -replace "\.py$", ""
                $importTest = python -c "import $modulePath; print('Import successful')" 2>&1
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "    ✅ Import test passed" -ForegroundColor Green
                } else {
                    Write-Host "    ⚠️  Import issue detected:" -ForegroundColor Yellow
                    Write-Host "       $importTest" -ForegroundColor Yellow
                }
            }
            'g' {
                Write-Host "    📖 Opening refactoring guide..." -ForegroundColor Blue
                & code "patch-to-refactoring-guide.md"
                Read-Host "    Press Enter to continue with $fileName"
                # Ask again after showing guide
                $response = Read-Host "    Now process $fileName? (y/n)"
                if ($response.ToLower() -eq 'y') {
                    # Recurse with 'y' response
                    $PSBoundParameters.Remove('File') | Out-Null
                    & $MyInvocation.MyCommand.Path @PSBoundParameters -File $file.Name
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
    }
}

Write-Host "`n🎉 @patch_to refactoring session complete!" -ForegroundColor Green
Write-Host "`n📊 Final validation steps:" -ForegroundColor Cyan
Write-Host "   1. Check for remaining @patch_to: findstr /s /n `"@patch_to`" src\*.py" -ForegroundColor White
Write-Host "   2. Test all imports: python -c `"import src; print('Success')`"" -ForegroundColor White  
Write-Host "   3. Run linting: .\scripts\lint.ps1" -ForegroundColor White
Write-Host "   4. Run tests: .\scripts\test.ps1" -ForegroundColor White