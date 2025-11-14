# Testing the Postman Converter

This directory contains test files for validating the Postman to Python converter, including both the traditional converter and the new multi-agent framework.

## Test Files

### 1. `test_simple_conversion.py` - Quick Single Request Test

**Purpose**: Fast test that converts one request using the traditional converter and validates the output.

**What it does**:
- ✅ Loads a Postman collection
- ✅ Converts one request to Python code
- ✅ Validates syntax with AST
- ✅ Analyzes code structure (functions, imports, type hints)
- ✅ Tests import capability
- ✅ Optionally executes with real credentials from `.env`

**Run it**:
```bash
cd src/postman/converter
python test_simple_conversion.py
```

**Output**:
- Shows request details
- Validates Python syntax
- Analyzes code structure
- Tests execution if credentials available
- Displays code preview

**Example Output**:
```
======================================================================
🧪 SINGLE REQUEST CONVERSION TEST
======================================================================

📄 Loading collection: Domo Product APIs.postman_collection.json

🎯 Selected Request:
   Name: Get User
   Method: GET
   URL: https://{{domain}}.domo.com/api/v1/users/{{user_id}}...

💻 Generating Python code...
✅ Generated 1,234 characters of code
   Function: get_user

🔍 Validating Python syntax...
✅ Valid Python syntax

📊 Code Analysis:
   Functions: 2
   Imports: 3
   Lines: 45

✅ TEST COMPLETED SUCCESSFULLY
```

---

### 2. `test_agent_conversion.py` - Full Multi-Agent Test

**Purpose**: Comprehensive test using the full multi-agent framework with all 12 agents.

**What it does**:
- ✅ Runs complete multi-agent conversion workflow
- ✅ Tests all 12 agents (Orchestrator → Formatter)
- ✅ Validates AST structure comprehensively
- ✅ Checks code quality metrics
- ✅ Verifies all analysis phases
- ✅ Tests file writing and imports
- ✅ Can be run with pytest

**Run with pytest**:
```bash
cd src/postman/converter
pytest test_agent_conversion.py -v
```

**Run standalone**:
```bash
cd src/postman/converter
python test_agent_conversion.py
```

**Test Cases**:

1. **`test_convert_single_request`**
   - Full conversion pipeline
   - AST validation
   - Structure analysis
   - Code quality checks
   - Execution test

2. **`test_generated_code_structure`**
   - Validates output structure
   - Checks metadata
   - Verifies completeness

3. **`test_analysis_results`**
   - Tests all 4 parallel analyzers
   - Validates aggregated analysis
   - Checks insights quality

**Example Output**:
```
============================================================
Testing Multi-Agent Postman Conversion
============================================================
Request: Get User
Method: GET
Export Folder: /tmp/tmpxyz123
============================================================

🎯 Orchestrator: Planning conversion strategy...
✅ Plan created: parallel strategy
   Complexity: medium

📄 Parser: Loading and parsing collection...
✅ Parsed: 42 requests

✓ Validator: Checking collection validity...
✅ Validation passed: 15 checks

🔍 Analysis: Running parallel analyses...
   • Structure analysis...
   • Authentication analysis...
   • Parameter analysis...
   • Header analysis...
✅ All analyses complete

...

✅ All tests passed!
```

---

## Prerequisites

### Required Environment Variables

Create a `.env` file in the project root:

```bash
# Domo credentials for testing execution
DOMO_INSTANCE=your-instance-name
DOMO_ACCESS_TOKEN=your-developer-token

# Optional: Specific test IDs
USER_ID_1=12345
DATASET_ID_1=67890
```

### Required Packages

```bash
# Core
pydantic-ai>=0.0.1
langgraph>=0.1.0
httpx>=0.24.0
pydantic>=2.0.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
python-dotenv>=1.0.0
```

---

## Running Tests

### Quick Test (Simple)
```bash
# Fast single-request test
python test_simple_conversion.py
```

### Full Test (Multi-Agent)
```bash
# All tests with pytest
pytest test_agent_conversion.py -v

# Specific test
pytest test_agent_conversion.py::TestAgentConversion::test_convert_single_request -v

# With output
pytest test_agent_conversion.py -v -s
```

### All Converter Tests
```bash
# Run all tests in converter directory
pytest . -v
```

---

## What Gets Tested

### Code Validation
- ✅ **Syntax**: AST parsing
- ✅ **Structure**: Functions, classes, imports
- ✅ **Type Hints**: Parameter and return types
- ✅ **Docstrings**: Presence and format
- ✅ **Error Handling**: Try/except blocks
- ✅ **Imports**: Required dependencies
- ✅ **Complexity**: Cyclomatic complexity estimate

### Function Quality
- ✅ **Async/Await**: Proper async functions
- ✅ **Arguments**: Correct parameter ordering
- ✅ **Documentation**: Complete docstrings with Args/Returns/Raises
- ✅ **Type Safety**: Full type annotations
- ✅ **Best Practices**: PEP 8 compliance

### Execution
- ✅ **Importability**: Module can be imported
- ✅ **Callability**: Functions are callable
- ✅ **API Calls**: Real API execution (if credentials available)
- ✅ **Error Handling**: Graceful failure handling

---

## Test Output Examples

### Successful Test
```
✅ Conversion completed successfully
   Generated 5 files

Testing generated file: get_user.py
============================================================

1. Validating Python syntax with AST...
   ✅ Syntax validation passed

2. Analyzing AST structure...
   Found function: get_user
   Async function: True
   ✅ Has docstring

3. Checking imports...
   Found 5 import statements
   Imports: httpx, typing, Optional, Dict, Any...

4. Checking error handling...
   Try blocks: 1
   Exception handlers: 2

5. Testing file write and import...
   File size: 3,456 bytes
   ✅ File written successfully

6. Testing function execution...
   Environment variables found, attempting execution...
   Function 'get_user' is callable and async
   ✅ Import successful

7. Code quality metrics...
   Total lines: 78
   Code lines: 52
   Comment lines: 15
   Blank lines: 11
   Cyclomatic complexity (approx): 6

============================================================
✅ All tests passed!
============================================================
```

### Test with Execution
```
🚀 Testing Execution:
   Found credentials for: your-instance
   Calling get_user...
   ✅ Response: 200
   ✅ SUCCESS! API call worked
   Response data type: <class 'dict'>
   Keys: ['id', 'name', 'email', 'role', 'created']
```

---

## Troubleshooting

### Common Issues

#### 1. Collection Not Found
```
❌ Collection not found: Domo Product APIs.postman_collection.json
```
**Solution**: Ensure the Postman collection is in the parent directory

#### 2. Import Errors
```
❌ Import error: No module named 'pydantic_ai'
```
**Solution**: Install required packages
```bash
pip install pydantic-ai langgraph httpx
```

#### 3. API Execution Fails
```
⚠️ Execution error: 401 Unauthorized
```
**Solution**: Check credentials in `.env` file

#### 4. Syntax Errors in Generated Code
```
❌ Syntax error at line 25: unexpected indent
```
**Solution**: This indicates a bug in code generation - check the converter logic

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Test Postman Converter

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run simple test
        run: python src/postman/converter/test_simple_conversion.py

      - name: Run agent tests
        run: pytest src/postman/converter/test_agent_conversion.py -v
        env:
          DOMO_INSTANCE: ${{ secrets.DOMO_INSTANCE }}
          DOMO_ACCESS_TOKEN: ${{ secrets.DOMO_ACCESS_TOKEN }}
```

---

## Next Steps

1. **Run simple test** to verify basic functionality
2. **Run full agent test** to validate complete pipeline
3. **Add custom tests** for your specific use cases
4. **Integrate with CI/CD** for automated testing

---

## Contributing

To add new tests:

1. Create test file: `test_*.py`
2. Use pytest fixtures and async tests
3. Follow existing patterns
4. Document test purpose and usage
5. Add to this README

---

## Support

For issues with tests:
1. Check console output for detailed errors
2. Verify environment variables are set
3. Ensure Postman collection exists
4. Check Python version (3.11+ recommended)
5. Review generated code manually

---

**Quick Links:**
- [Multi-Agent Architecture](./agent_design.md)
- [User Guide](./AGENT_README.md)
- [Quick Reference](./QUICK_REFERENCE.md)
