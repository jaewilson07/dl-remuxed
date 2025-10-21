#!/usr/bin/env powershell
# Build script for domolibrary2

Write-Host "Building domolibrary2 package..." -ForegroundColor Green

# Clean previous builds
if (Test-Path "dist") {
    Remove-Item -Recurse -Force dist
    Write-Host "Cleaned previous build artifacts" -ForegroundColor Yellow
}

# Build the package
& C:\Users\jwilson1\.local\bin\uv.exe build

Write-Host "Build complete! Check dist/ folder for artifacts." -ForegroundColor Cyan
