#!/bin/bash
# Fallback formatting script when pre-commit has virtualenv issues

echo "🔧 Running manual code formatting (pre-commit fallback)..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Run this script from the project root directory"
    exit 1
fi

# Run basic syntax check
echo "📝 Checking Python syntax..."
find src -name "*.py" -exec python -m py_compile {} \;

# Run black formatting if available
if python -m black --version >/dev/null 2>&1; then
    echo "🖤 Running black formatter..."
    python -m black src/
else
    echo "⚠️  Black not available, skipping formatting"
fi

# Run isort if available
if python -m isort --version >/dev/null 2>&1; then
    echo "📦 Running isort..."
    python -m isort src/ --profile=black
else
    echo "⚠️  isort not available, skipping import sorting"
fi

# Run ruff if available
if python -m ruff --version >/dev/null 2>&1; then
    echo "🦀 Running ruff linter..."
    python -m ruff check src/ --fix --select=I,F401,F811 --ignore=E501 || true
else
    echo "⚠️  Ruff not available, skipping linting"
fi

echo "✅ Manual formatting complete!"