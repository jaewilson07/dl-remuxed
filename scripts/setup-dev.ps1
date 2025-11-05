#!/usr/bin/env powershell
# Development setup script for domolibrary2

Write-Host "Setting up development environment..." -ForegroundColor Green

# Sync dependencies including dev dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
uv sync --dev

# Install pre-commit hooks
Write-Host "Setting up pre-commit hooks..." -ForegroundColor Yellow
uv run pre-commit install

Write-Host "Development environment setup complete!" -ForegroundColor Cyan
Write-Host "Available scripts:" -ForegroundColor White
Write-Host "  .\scripts\lint.ps1     - Run linting and formatting" -ForegroundColor Gray
Write-Host "  .\scripts\test.ps1     - Run tests with coverage" -ForegroundColor Gray
Write-Host "  .\scripts\build.ps1    - Build the package" -ForegroundColor Gray
Write-Host "  .\scripts\publish.ps1  - Publish to PyPI" -ForegroundColor Gray
