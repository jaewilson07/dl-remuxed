# Development Environment Setup

This document explains how to ensure PowerShell always uses the local virtual environment by default.

## Quick Start

The virtual environment is already configured! You have several options:

### Option 1: VS Code (Recommended)
VS Code is already configured to use the virtual environment automatically:
- The `.vscode/settings.json` file sets the default Python interpreter
- The terminal will automatically activate the virtual environment
- Just open the project in VS Code and everything works!

### Option 2: Manual PowerShell Activation
Run the activation script in any PowerShell session:
```powershell
.\activate-env.ps1
```

### Option 3: Windows Command Prompt
Use the batch file for quick setup:
```cmd
dev-env.bat
```

## What's Been Configured

1. **VS Code Settings** (`.vscode/settings.json`):
   - Default Python interpreter: `./.venv/Scripts/python.exe`
   - Auto-activate terminal environment
   - Custom terminal profile with environment
   - Python path includes `src` directory

2. **Environment File** (`.env`):
   - Contains project-specific environment variables
   - DOMO instance and access token
   - Python path configuration

3. **Activation Scripts**:
   - `activate-env.ps1`: PowerShell activation script
   - `dev-env.bat`: Windows batch file for activation

## Testing the Setup

Test that everything works:
```powershell
# Test Python import
python -c "import domolibrary2; print('✅ Package imported successfully')"

# Test user routes
python -c "import tests.routes.test_user; print('✅ Test file imports successfully')"

# Run specific tests
python -m pytest tests/routes/test_user.py::TestUserPropertyTypes::test_user_property_types_exist -v
```

## Automatic Activation

With the current setup:
- **VS Code**: Automatically activates when you open a terminal
- **Manual**: Run `.\activate-env.ps1` in the project directory
- **Quick**: Double-click `dev-env.bat` for a ready-to-use command prompt

The virtual environment is indicated by the `(dl2)` prefix in your terminal prompt.