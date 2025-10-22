#!/usr/bin/env powershell
# Script to fix self-referential relative imports

Write-Host "Fixing self-referential imports..." -ForegroundColor Green

# Get all Python files in src/
$pythonFiles = Get-ChildItem -Path "src" -Recurse -Filter "*.py"

$totalFiles = $pythonFiles.Count
$fixedFiles = 0

foreach ($file in $pythonFiles) {
    $content = Get-Content $file.FullName -Raw
    $originalContent = $content

    # Get the relative path to determine the correct imports
    $relativePath = $file.DirectoryName.Replace((Get-Location).Path + "\src\", "").Replace("\", "/")

    # Fix self-referential imports within the same directory
    # Example: from ..client import Logger -> from . import Logger (when in client/)
    if ($relativePath -eq "client") {
        $content = $content -replace 'from \.\.client import', 'from . import'
    }
    elseif ($relativePath -eq "classes") {
        $content = $content -replace 'from \.\.classes import', 'from . import'
    }
    elseif ($relativePath -eq "routes") {
        $content = $content -replace 'from \.\.routes import', 'from . import'
    }
    elseif ($relativePath -eq "utils") {
        $content = $content -replace 'from \.\.utils import', 'from . import'
    }
    elseif ($relativePath -eq "integrations") {
        $content = $content -replace 'from \.\.integrations import', 'from . import'
    }
    if ($content -ne $originalContent) {
        Set-Content -Path $file.FullName -Value $content -NoNewline
        $fixedFiles++
        Write-Host "Fixed self-imports in: $($file.Name)" -ForegroundColor Yellow
    }
}

Write-Host "Self-import fixing complete!" -ForegroundColor Cyan
Write-Host "Files processed: $totalFiles" -ForegroundColor White
Write-Host "Files modified: $fixedFiles" -ForegroundColor Green
