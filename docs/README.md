# Domolibrary2 Documentation

Welcome to the domolibrary2 documentation! This directory contains guides, references, and instructions for working with the Domo library.

## 📚 Table of Contents

### Getting Started
- [Project Instructions](../.github/instructions/) - Copilot-readable standards

### Class Validation System ⭐ **New!**
Complete system for systematically validating and testing all classes:

- **[📖 Start Here](./CLASS-VALIDATION-START-HERE.md)** - Quick start (5 minutes)
- **[📋 Quick Reference](./class-validation-quick-reference.md)** - Cheat sheet for fast lookup
- **[📘 Comprehensive Guide](./class-validation-guide.md)** - Detailed instructions with examples
- **[🔧 System Overview](./class-validation-system-overview.md)** - Complete system documentation

**Tools:**
- [Issue Generator Script](../scripts/generate-class-validation-issues.py) - Generate validation issues
- [Issue Template](../.github/ISSUE_TEMPLATE/class-validation.md) - GitHub issue template
- [Generated Issues](../EXPORTS/issues/) - Ready-to-import issue files

### Architecture & Design
- [Error Design Strategy](./error-design-strategy.md)
- [Route Refactoring Guide](./route-refactoring-guide.md)
- [Route Splitting Strategy](./route-splitting-strategy.md)
- [CodeEngine Refactoring Summary](./codeengine-refactoring-summary.md)
- [Type Hints Implementation Guide](./type-hints-implementation-guide.md)

### Development Guides
- [Copilot Instructions](./COPILOT_INSTRUCTIONS.md)
- [Publishing](./PUBLISHING.md)
- [Pre-commit Troubleshooting](./pre-commit-troubleshooting.md)
- [Route Repair Implementation Plan](./route-repair-implementation-plan.md)

## 🚀 Quick Start

### For New Contributors

1. **Setup Development Environment**
   ```powershell
   # Follow the development setup guide
   code DEV-SETUP.md
   ```

2. **Start Validating Classes**
   ```powershell
   # Read the 5-minute quick start
   code docs/CLASS-VALIDATION-START-HERE.md
   
   # Generate issues for high-priority classes
   python scripts/generate-class-validation-issues.py --priority high
   ```

3. **Run Tests**
   ```powershell
   # Run all tests
   pytest
   
   # Run specific test file
   pytest tests/classes/DomoUser.py -v
   ```

### For Experienced Contributors

1. **Reference the Quick Guide**
   ```powershell
   code docs/class-validation-quick-reference.md
   ```

2. **Generate and Import Issues**
   ```powershell
   # Generate all issues
   python scripts/generate-class-validation-issues.py
   
   # Bulk import to GitHub
   gh issue create --body-file "EXPORTS/issues/issue_DomoDataset.md"
   ```

3. **Follow the Patterns**
   - Structure: See `src/domolibrary2/classes/DomoUser.py`
   - Tests: See `tests/classes/DomoUser.py`
   - Routes: See `src/domolibrary2/routes/user/`

## 📋 Documentation by Topic

### Class Development
- **Validation System**: [Start Here](./CLASS-VALIDATION-START-HERE.md) → [Quick Reference](./class-validation-quick-reference.md) → [Comprehensive Guide](./class-validation-guide.md)
- **Type Hints**: [Implementation Guide](./type-hints-implementation-guide.md)
- **Error Handling**: [Error Design Strategy](./error-design-strategy.md)

### Route Development
- **Route Functions**: [Refactoring Guide](./route-refactoring-guide.md)
- **Route Organization**: [Splitting Strategy](./route-splitting-strategy.md)
- **Route Repair**: [Implementation Plan](./route-repair-implementation-plan.md)

### Testing
- **Test Patterns**: [Testing Guide](./testing-guide.md)
- **Test Examples**: [DomoUser Tests](../tests/classes/DomoUser.py)
- **Test Harness**: [Test Harness](../tests/test_harness.py)

### Project Management
- **Publishing**: [Publishing Guide](./PUBLISHING.md)
- **Pre-commit**: [Troubleshooting](./pre-commit-troubleshooting.md)
- **AI Assistance**: [Copilot Instructions](./COPILOT_INSTRUCTIONS.md)

## 🎯 Current Focus: Class Validation

We're systematically validating all classes to ensure:
- ✅ Proper inheritance from entity base classes
- ✅ Delegation to route functions (no API logic in classes)
- ✅ Composition using subentities
- ✅ Comprehensive test coverage
- ✅ Complete documentation

### Priority Classes
1. DomoUser (reference implementation)
2. DomoDataset
3. DomoCard
4. DomoPage
5. DomoGroup

**Get started**: [Class Validation Start Here](./CLASS-VALIDATION-START-HERE.md)

## 🔧 Tools & Scripts

Located in `scripts/`:
- `generate-class-validation-issues.py` - Create validation issues for all classes
- `check-type-hints.py` - Check type hint coverage
- `check-route-syntax.py` - Validate route function syntax
- `format-code.ps1` - Format code with black and isort
- `test.ps1` - Run test suite

## 📊 Project Status

### Completed
- ✅ Route function refactoring
- ✅ Error design strategy implementation
- ✅ Type hints implementation guide
- ✅ Class validation system (NEW!)

### In Progress
- 🔄 Class validation across all entities
- 🔄 Test coverage improvement
- 🔄 Documentation updates

### Planned
- 📋 Complete API coverage
- 📋 Performance optimization
- 📋 Integration examples

## 🆘 Getting Help

### Quick Answers
1. **Class Validation**: Check [Quick Reference](./class-validation-quick-reference.md)
2. **Code Patterns**: See [DomoUser.py](../src/domolibrary2/classes/DomoUser.py)
3. **Test Patterns**: See [DomoUser Tests](../tests/classes/DomoUser.py)
4. **Route Patterns**: Check [Route Refactoring Guide](./route-refactoring-guide.md)

### Detailed Help
1. **Comprehensive Guide**: [Class Validation Guide](./class-validation-guide.md)
2. **Error Design**: [Error Strategy](./error-design-strategy.md)
3. **Testing**: [Testing Guide](./testing-guide.md)

### Support Channels
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and discussions
- **Documentation**: For guides and references

## 📝 Contributing to Documentation

### Adding New Documentation

1. Create the document in `docs/`
2. Add entry to this README
3. Link from related documents
4. Update the table of contents

### Updating Existing Documentation

1. Make your changes
2. Update related documents
3. Check all links still work
4. Submit PR with documentation updates

### Documentation Standards

- Use clear, descriptive headings
- Include code examples
- Add links to related documentation
- Keep table of contents updated
- Use emoji for visual navigation (sparingly)

## 🔗 External Resources

- [Domo Developer Portal](https://developer.domo.com/)
- [Domo API Documentation](https://developer.domo.com/docs/api-documentation)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)
- [httpx Documentation](https://www.python-httpx.org/)

---

**Last Updated**: 2024  
**Maintained By**: domolibrary2 team  

**Need to add something?** Submit a PR or create an issue!
