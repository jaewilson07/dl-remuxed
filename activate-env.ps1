# PowerShell script to activate the local virtual environment
# Usage: Run this script when opening PowerShell in this directory

# Check if we're in the correct directory
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating local virtual environment..." -ForegroundColor Green
    & .\.venv\Scripts\Activate.ps1
    
    # Add src directory to Python path for development
    $env:PYTHONPATH = "$(Get-Location)\src;$env:PYTHONPATH"
    Write-Host "Virtual environment activated!" -ForegroundColor Green
    Write-Host "Python path includes src directory" -ForegroundColor Blue
    
    # Show Python version and virtual env info
    Write-Host "Python executable: $(python -c 'import sys; print(sys.executable)')" -ForegroundColor Cyan
} else {
    Write-Warning "Virtual environment not found in current directory"
}