#!/usr/bin/env powershell
# Publish script for domolibrary2

param(
    [Parameter(HelpMessage="Publish to test PyPI instead of main PyPI")]
    [switch]$TestPyPI
)

Write-Host "Publishing domolibrary2 package..." -ForegroundColor Green

# First, run linting and tests
Write-Host "Running pre-publish checks..." -ForegroundColor Yellow
& .\scripts\lint.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Linting failed. Please fix issues before publishing." -ForegroundColor Red
    exit 1
}

& .\scripts\test.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed. Please fix issues before publishing." -ForegroundColor Red
    exit 1
}

# Build the package
Write-Host "Building package..." -ForegroundColor Yellow
& .\scripts\build.ps1

# Publish
if ($TestPyPI) {
    Write-Host "Publishing to Test PyPI..." -ForegroundColor Yellow
    uv publish --repository-url https://test.pypi.org/legacy/ dist/*
} else {
    Write-Host "Publishing to PyPI..." -ForegroundColor Yellow
    uv publish dist/*
}

Write-Host "Publish complete!" -ForegroundColor Cyan
