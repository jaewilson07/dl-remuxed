#!/usr/bin/env powershell
# Linting and formatting script for domolibrary2

Write-Host "Running ruff check and fix..." -ForegroundColor Green
& C:\Users\jwilson1\.local\bin\uv.exe run ruff check src --fix

Write-Host "Running black formatter..." -ForegroundColor Green
& C:\Users\jwilson1\.local\bin\uv.exe run black src

Write-Host "Running isort..." -ForegroundColor Green
& C:\Users\jwilson1\.local\bin\uv.exe run isort src

Write-Host "Running pylint..." -ForegroundColor Green
& C:\Users\jwilson1\.local\bin\uv.exe run pylint src --output-format=colorized

Write-Host "Running mypy..." -ForegroundColor Green
& C:\Users\jwilson1\.local\bin\uv.exe run mypy src --ignore-missing-imports

Write-Host "Linting complete!" -ForegroundColor Cyan
