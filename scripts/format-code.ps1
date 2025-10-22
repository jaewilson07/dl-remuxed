# Fallback formatting script when pre-commit has virtualenv issues
# PowerShell version for Windows

Write-Host "[TOOL] Running manual code formatting (pre-commit fallback)..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "pyproject.toml")) {
    Write-Host "[ERROR] Run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Run basic syntax check
Write-Host "[CHECK] Checking Python syntax..." -ForegroundColor Blue
Get-ChildItem -Path "src" -Filter "*.py" -Recurse | ForEach-Object {
    python -m py_compile $_.FullName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Syntax error in $($_.Name)" -ForegroundColor Red
    }
}

# Run black formatting if available
try {
    python -m black --version | Out-Null
    Write-Host "[BLACK] Running black formatter..." -ForegroundColor Blue
    python -m black src/
} catch {
    Write-Host "[WARN] Black not available, skipping formatting" -ForegroundColor Yellow
}

# Run isort if available
try {
    python -m isort --version | Out-Null
    Write-Host "[ISORT] Running isort..." -ForegroundColor Blue
    python -m isort src/ --profile=black
} catch {
    Write-Host "[WARN] isort not available, skipping import sorting" -ForegroundColor Yellow
}

# Run ruff if available
try {
    python -m ruff --version | Out-Null
    Write-Host "[RUFF] Running ruff linter..." -ForegroundColor Blue
    python -m ruff check src/ --fix --select=I,F401,F811 --ignore=E501
} catch {
    Write-Host "[WARN] Ruff not available, skipping linting" -ForegroundColor Yellow
}

Write-Host "Manual formatting complete!" -ForegroundColor Green