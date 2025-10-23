# Domolibrary2 Documentation

Welcome to the domolibrary2 documentation! This directory contains guides, references, and instructions for working with the Domo library.

## 📚 Table of Contents

### Getting Started
- [Project Instructions](../.github/instructions/) - Copilot-readable standards
- [Route Refactoring Dashboard](./route-refactoring-dashboard.md) - Quick visual status of the refactoring project

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
- [Error Design Strategy](./error-design-strategy.md) - Comprehensive error handling guidelines
- [Route Refactoring Guide](./route-refactoring-guide.md) - Step-by-step refactoring instructions
- [Route Refactoring Progress](./route-refactoring-progress.md) - Detailed progress tracking for route refactoring
- [Route Splitting Strategy](./route-splitting-strategy.md) - Guidelines for splitting large route files
- [CodeEngine Refactoring Summary](./codeengine-refactoring-summary.md) - Example of successful refactoring
- [Type Hints Implementation Guide](./type-hints-implementation-guide.md)
- [Route Standards](../.github/instructions/routes.instructions.md) - Required patterns for all route functions

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

### Working on Route Refactoring

1. **Check Current Status**: Review the [Dashboard](./route-refactoring-dashboard.md) for what needs work
2. **Follow Standards**: Read [Route Standards](../.github/instructions/routes.instructions.md) for required patterns
3. **Reference Guide**: Use [Refactoring Guide](./route-refactoring-guide.md) for step-by-step instructions
4. **Error Design**: Follow [Error Design Strategy](./error-design-strategy.md) for exception classes

### Understanding the Project

```
Project Status: 47.6% Complete
- Phase 1 (Simple Routes): 55.6% done
- Phase 2 (Medium Routes): 0% done
- Phase 3 (Complex Routes): 66.7% done
```

See [Route Refactoring Progress](./route-refactoring-progress.md) for details.

## � Documentation by Topic

### Class Development
- **Validation System**: [Start Here](./CLASS-VALIDATION-START-HERE.md) → [Quick Reference](./class-validation-quick-reference.md) → [Comprehensive Guide](./class-validation-guide.md)
- **Type Hints**: [Implementation Guide](./type-hints-implementation-guide.md)
- **Testing Patterns**: [Testing Guide](./testing-guide.md)

### Route Development
- **Refactoring Guide**: [Route Refactoring Guide](./route-refactoring-guide.md)
- **Error Handling**: [Error Design Strategy](./error-design-strategy.md)
- **Standards**: [Route Instructions](../.github/instructions/routes.instructions.md)
- **Progress Tracking**: [Route Refactoring Progress](./route-refactoring-progress.md)

### Testing & Quality
- **Testing Guide**: [Testing Guide](./testing-guide.md)
- **Class Testing**: [Class Validation System](./CLASS-VALIDATION-START-HERE.md)
- **Route Testing**: See route refactoring guides

## �📖 Documentation Structure

### Error Handling

The library uses a hierarchical error system:

```
DomoError (base)
├── RouteError (API route/endpoint errors)
├── ClassError (Class instance errors)  
└── AuthError (Authentication-specific errors)
```

Each route module defines standard error classes:
- `{Module}_GET_Error` - Retrieval failures
- `Search{Module}_NotFound` - Empty search results
- `{Module}_CRUD_Error` - Create/update/delete failures
- `{Module}Sharing_Error` - Permission/sharing issues

See [Error Design Strategy](./error-design-strategy.md) for complete details.

### Route Function Standards

All route functions must include:

1. `@gd.route_function` decorator
2. `return_raw: bool = False` parameter
3. Immediate return check: `if return_raw: return res`
4. Proper error handling with specific exception classes
5. Complete docstrings with Args/Returns/Raises

See [Route Standards](../.github/instructions/routes.instructions.md) for the complete pattern.

## 🔗 Related Resources

### GitHub

- [Milestone Issue #30](https://github.com/jaewilson07/dl-remuxed/issues/30) - Project tracking
- [Open Issues](https://github.com/jaewilson07/dl-remuxed/issues) - All refactoring issues
- [Repository](https://github.com/jaewilson07/dl-remuxed) - Source code

### Examples

Best examples of refactored code:
- `src/domolibrary2/routes/access_token.py` - Perfect template for simple routes
- `src/domolibrary2/routes/pdp.py` - Standard error classes with backward compatibility
- `src/domolibrary2/routes/codeengine/` - Submodule structure example
- `src/domolibrary2/routes/page/` - Complex route split into submodules

## 📝 Contributing

When contributing to the refactoring effort:

1. **Pick an Issue**: Choose from [open refactoring issues](https://github.com/jaewilson07/dl-remuxed/issues?q=is%3Aissue+is%3Aopen+label%3Arefactoring)
2. **Follow Standards**: Use the patterns in [Route Standards](../.github/instructions/routes.instructions.md)
3. **Test Thoroughly**: Ensure backward compatibility
4. **Update Docs**: Update the [Progress Tracker](./route-refactoring-progress.md)

## 🎓 Learning Resources

### Understanding the Codebase

1. Start with [Error Design Strategy](./error-design-strategy.md) to understand the error hierarchy
2. Read [Route Standards](../.github/instructions/routes.instructions.md) for function patterns
3. Study `access_token.py` as a perfect template
4. Review [Route Refactoring Guide](./route-refactoring-guide.md) for practical steps

### Best Practices

- Maintain backward compatibility with legacy error classes
- Use type hints consistently
- Write comprehensive docstrings
- Separate concerns in submodules for complex routes
- Follow naming conventions strictly

## 🚀 Current Focus

**Immediate Priorities:**

1. Complete Phase 1 simple routes (4 remaining)
2. Refactor dataset.py (highest priority complex route)
3. Begin Phase 2 medium complexity routes

**Next Major Milestone:**

- Complete Phase 1: Target Q4 2025
- Begin dataset.py refactoring: Critical priority
- Start Phase 2: Early 2026

See [Route Refactoring Dashboard](./route-refactoring-dashboard.md) for current status.

---

*Last Updated: 2025-10-22*  
*For questions or issues, refer to the [GitHub repository](https://github.com/jaewilson07/dl-remuxed)*
