#!/usr/bin/env powershell
# Test script for domolibrary2

Write-Host "Running tests for domolibrary2..." -ForegroundColor Green

# Run pytest with coverage
& C:\Users\jwilson1\.local\bin\uv.exe run pytest tests/ --verbose --cov=src --cov-report=html --cov-report=term

Write-Host "Tests complete! Coverage report generated in htmlcov/" -ForegroundColor Cyan