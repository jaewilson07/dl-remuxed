#!/usr/bin/env powershell
# Linting and formatting script for domolibrary2

Write-Host "Running ruff check and fix..." -ForegroundColor Green
uv run ruff check src --fix

Write-Host "Running black formatter..." -ForegroundColor Green
uv run black src

Write-Host "Running isort..." -ForegroundColor Green
uv run isort src

Write-Host "Running pylint..." -ForegroundColor Green
uv run pylint src --output-format=colorized

Write-Host "Running mypy..." -ForegroundColor Green
uv run mypy src --ignore-missing-imports

Write-Host "Linting complete!" -ForegroundColor Cyan
