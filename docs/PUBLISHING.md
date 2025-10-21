# Publishing domolibrary to PyPI

This document describes how to publish `domolibrary` to PyPI using the configured GitHub Actions workflow.

## Prerequisites

The repository is configured to use PyPI's Trusted Publishing mechanism, which eliminates the need for API tokens. This is the recommended approach by PyPI.

## Setup PyPI Trusted Publishing (One-time setup)

1. **Create the PyPI project** (if it doesn't exist yet):
   - Go to https://pypi.org/
   - Register an account if you don't have one
   - Note: You may need to manually create the project first OR use TestPyPI for the first release

2. **Configure Trusted Publishing on PyPI**:
   - Go to https://pypi.org/manage/account/publishing/
   - Click "Add a new pending publisher"
   - Fill in:
     - **PyPI Project Name**: `domolibrary`
     - **Owner**: `jaewilson07`
     - **Repository name**: `dl-remuxed`
     - **Workflow name**: `python-publish.yml`
     - **Environment name**: `pypi`
   - Click "Add"

3. **Configure GitHub Environment** (Recommended):
   - Go to your repository: https://github.com/jaewilson07/dl-remuxed/settings/environments
   - Create an environment named `pypi`
   - Add protection rules if desired (e.g., required reviewers)

## Publishing a New Release

Once Trusted Publishing is configured, publishing is simple:

1. **Update the version** in `pyproject.toml`:
   ```toml
   [project]
   name = "domolibrary"
   version = "4.5.29"  # Update this to your new version
   ```

2. **Update the version** in `domolibrary/__init__.py`:
   ```python
   __version__ = "4.5.29"  # Keep in sync with pyproject.toml
   ```

3. **Commit and push your changes**:
   ```bash
   git add pyproject.toml domolibrary/__init__.py
   git commit -m "Bump version to 4.5.29"
   git push
   ```

4. **Create a GitHub Release**:
   - Go to https://github.com/jaewilson07/dl-remuxed/releases/new
   - Create a new tag (e.g., `v4.5.29`)
   - Set the release title (e.g., `v4.5.29`)
   - Add release notes describing changes
   - Click "Publish release"

5. **Automatic Publishing**:
   - The GitHub Actions workflow will automatically:
     - Build the package using `uv`
     - Publish to PyPI using Trusted Publishing
   - Monitor the workflow at: https://github.com/jaewilson07/dl-remuxed/actions

## Testing the Package Locally

Before publishing, you can test the package build:

```bash
# Install uv if you haven't already
pip install uv

# Build the package
uv build

# Check the built files
ls -l dist/

# Optionally, install locally to test
pip install dist/domolibrary-*.whl
```

## Using TestPyPI for Testing (Optional)

If you want to test the publishing process first:

1. Set up Trusted Publishing on TestPyPI: https://test.pypi.org/manage/account/publishing/
2. Create a separate workflow or modify the existing one to publish to TestPyPI
3. Install from TestPyPI:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ domolibrary
   ```

## Troubleshooting

### Build Fails
- Ensure all required files exist (README.md, LICENSE, pyproject.toml)
- Check that the version in pyproject.toml is valid
- Review the GitHub Actions logs

### Publishing Fails
- Verify Trusted Publishing is configured correctly on PyPI
- Check that the GitHub environment name matches (`pypi`)
- Ensure the workflow name is correct (`python-publish.yml`)
- Make sure you're creating a release (not just a tag)

### Version Conflicts
- PyPI does not allow re-uploading the same version
- If you need to fix something, bump the version number

## Current Package Information

- **Package Name**: domolibrary
- **Current Version**: 4.5.29
- **PyPI URL**: https://pypi.org/project/domolibrary/
- **Documentation**: https://jaewilson07.github.io/dl-remuxed
- **Repository**: https://github.com/jaewilson07/dl-remuxed
