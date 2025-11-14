# Multi-Agent Postman to Python Converter

A sophisticated multi-agent framework using **pydantic-ai** and **LangGraph** to convert Postman collections into high-quality Python API client functions.

## Overview

This framework uses 12 specialized AI agents working in a coordinated graph to analyze, generate, and validate Python code from Postman collections. It provides superior code quality compared to traditional template-based conversion.

## Architecture

### Pattern: Orchestrator-Worker with Graph-Based Control Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      Orchestrator Agent                      │
│              (Plans conversion strategy)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                       Parser Agent                           │
│              (Loads & parses collection)                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Validation Agent                          │
│           (Validates structure & completeness)               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────┴────────────────┐
        │     Parallel Analysis Phase     │
        └───────────────┬────────────────┘
                        │
        ┌───────┬───────┼───────┬────────┐
        │       │       │       │        │
        ▼       ▼       ▼       ▼        │
    ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐    │
    │Struct│Auth │Param│Header│         │
    │Anlyz│Anlyz│Anlyz│Anlyz│          │
    └─────┘ └─────┘ └─────┘ └─────┘    │
        │       │       │       │        │
        └───────┴───────┴───────┴────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 Analysis Aggregator Agent                    │
│         (Synthesizes all analysis insights)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Code Generator Agent                        │
│          (Generates Python API functions)                    │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Test Generator Agent                        │
│              (Creates pytest test functions)                 │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 Code Validator Agent                         │
│         (Validates syntax, types, security)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Code Formatter Agent                        │
│        (Applies Black, isort, final polish)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
                  Python Files
```

## The 12 Specialized Agents

### Phase 1: Planning & Parsing
1. **Orchestrator Agent** - Plans conversion strategy based on collection complexity
2. **Parser Agent** - Loads and parses Postman collection into structured models
3. **Validation Agent** - Validates collection structure and completeness

### Phase 2: Parallel Analysis (Concurrent Execution)
4. **Structure Analyzer** - Analyzes folder hierarchy and organization patterns
5. **Authentication Analyzer** - Analyzes auth patterns and requirements
6. **Parameter Analyzer** - Analyzes query params, path variables, types
7. **Header Analyzer** - Analyzes HTTP headers and usage patterns

### Phase 3: Synthesis & Generation
8. **Analysis Aggregator** - Synthesizes all analyses into unified strategy
9. **Code Generator** - Generates Python async functions with type hints
10. **Test Generator** - Creates comprehensive pytest test functions

### Phase 4: Quality Assurance
11. **Code Validator** - Validates syntax, types, style, security
12. **Code Formatter** - Applies Black, isort, and final formatting

## Quick Start

### Basic Usage

```python
import asyncio
from postman.converter import convert_postman_collection

async def main():
    result = await convert_postman_collection(
        collection_path="api.postman_collection.json",
        export_folder="./generated",
        write_files=True
    )

    print(f"Generated {len(result['formatted_code'])} functions")

asyncio.run(main())
```

### Synchronous Usage

```python
from postman.converter import convert_postman_collection_sync

result = convert_postman_collection_sync(
    collection_path="api.postman_collection.json",
    export_folder="./generated"
)
```

### With Customization

```python
result = await convert_postman_collection(
    collection_path="api.postman_collection.json",
    export_folder="./generated",
    customize_config={
        "required_headers": ["authorization", "content-type"],
        "default_params": ["limit", "offset", "page"],
    }
)
```

## Features

### 🎯 Intelligent Analysis
- **Pattern Recognition**: Identifies naming conventions, grouping patterns
- **Type Inference**: Infers parameter types from values
- **Auth Detection**: Analyzes authentication patterns and requirements
- **Complexity Assessment**: Evaluates collection complexity (1-10 scale)

### 💻 High-Quality Code Generation
- **Async/Await**: All functions use async/await patterns
- **Type Hints**: Complete type annotations (PEP 484)
- **Docstrings**: Comprehensive Google/NumPy style docstrings
- **Error Handling**: Graceful error handling with informative messages
- **Best Practices**: Follows PEP 8, Black, and project conventions

### 🧪 Comprehensive Testing
- **Pytest Integration**: Async-compatible test functions
- **Mock Data**: Leverages response examples from Postman
- **Edge Cases**: Tests success, errors, validation, edge cases
- **Fixtures**: Reusable test fixtures

### ✅ Quality Assurance
- **Syntax Validation**: AST-based syntax checking
- **Type Checking**: Type consistency validation
- **Security Scanning**: Checks for common vulnerabilities
- **Style Enforcement**: Black, ruff, isort formatting

### ⚡ Performance
- **Parallel Analysis**: 4 analyzers run concurrently
- **Efficient Processing**: Batched operations where possible
- **Progress Tracking**: Real-time progress updates

## Generated Code Example

### Input (Postman Request)
```json
{
  "name": "Get User by ID",
  "request": {
    "method": "GET",
    "url": {
      "raw": "{{base_url}}/api/v1/users/{{user_id}}",
      "query": [
        {"key": "include_metadata", "value": "true"}
      ]
    }
  }
}
```

### Output (Generated Python)
```python
async def get_user_by_id(
    auth: DomoAuth,
    user_id: str,
    include_metadata: bool = True,
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
) -> httpx.Response:
    """Get user information by user ID.

    Retrieves detailed information about a specific user including
    their profile, roles, and optionally metadata.

    Args:
        auth: Authentication object with credentials
        user_id: Unique identifier for the user
        include_metadata: Whether to include user metadata (default: True)
        session: Optional httpx client session for connection reuse
        debug_api: Enable debug logging for API calls

    Returns:
        httpx.Response object with user data

    Raises:
        httpx.HTTPStatusError: If the request fails
        ValueError: If user_id is invalid

    Example:
        >>> auth = DomoAuth(instance="mycompany", token="...")
        >>> response = await get_user_by_id(auth, "12345")
        >>> user_data = response.json()
    """
    url = f"{auth.base_url}/api/v1/users/{user_id}"

    params = {"include_metadata": str(include_metadata).lower()}

    headers = {
        "Authorization": f"Bearer {auth.token}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() if session is None else contextlib.nullcontext(session) as client:
        response = await client.get(
            url,
            params=params,
            headers=headers,
            timeout=30.0,
        )

        if debug_api:
            print(f"[DEBUG] GET {url}")
            print(f"[DEBUG] Status: {response.status_code}")

        response.raise_for_status()
        return response
```

### Output (Generated Test)
```python
import pytest
import httpx
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_get_user_by_id_success():
    """Test successful user retrieval."""
    auth = MockAuth()
    user_id = "12345"

    mock_response = {
        "id": "12345",
        "name": "John Doe",
        "email": "john@example.com"
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = await get_user_by_id(auth, user_id)

        assert response.status_code == 200
        assert response.json()["id"] == user_id

@pytest.mark.asyncio
async def test_get_user_by_id_not_found():
    """Test user not found error."""
    auth = MockAuth()

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=None, response=None
        )

        with pytest.raises(httpx.HTTPStatusError):
            await get_user_by_id(auth, "nonexistent")
```

## Advanced Usage

### Custom Agent Configuration

```python
from postman.converter.agent_graph import create_postman_conversion_graph
from postman.converter.agent_graph_agents import initialize_code_generator

# Create custom graph
graph = create_postman_conversion_graph()

# Customize specific agents
custom_code_gen = initialize_code_generator()
# ... modify agent settings ...

# Run with custom graph
result = await graph.ainvoke(initial_state)
```

### Access Intermediate Results

```python
result = await convert_postman_collection(
    collection_path="api.postman_collection.json",
    export_folder="./generated",
    write_files=False  # Don't write files yet
)

# Access analysis results
structure = result["structure_analysis"]
auth = result["auth_analysis"]
params = result["parameter_analysis"]

# Examine generated code before writing
for filename, code in result["formatted_code"].items():
    print(f"Generated: {filename}")
    print(code[:200])  # Preview

# Write files manually if desired
# ... custom file writing logic ...
```

### Inspect Graph State

```python
# Run graph step by step for debugging
from postman.converter.agent_graph_nodes import orchestration_node, parsing_node

state = {
    "collection_path": "api.postman_collection.json",
    "export_folder": "./generated",
    # ... other state ...
}

# Run individual nodes
state = await orchestration_node(state)
print(f"Plan: {state['conversion_plan']}")

state = await parsing_node(state)
print(f"Parsed: {state['parsed_collection']['info']['name']}")
```

## Configuration Options

### Customize Config

```python
customize_config = {
    # Headers to include in all requests
    "required_headers": [
        "authorization",
        "content-type",
        "user-agent"
    ],

    # Parameters to expose as function arguments
    "default_params": [
        "limit",
        "offset",
        "page",
        "sort",
        "order"
    ],

    # Parameters to exclude from generation
    "ignored_params": [
        "internal_debug",
        "test_mode"
    ],

    # Custom module organization
    "module_structure": {
        "users": ["get_user", "create_user"],
        "products": ["list_products", "get_product"]
    }
}
```

## Benefits Over Traditional Conversion

| Feature | Traditional | Multi-Agent |
|---------|------------|-------------|
| **Code Quality** | Template-based | AI-analyzed & optimized |
| **Type Hints** | Basic | Comprehensive & accurate |
| **Docstrings** | Minimal | Detailed with examples |
| **Error Handling** | Generic | Context-aware |
| **Test Generation** | Basic | Comprehensive coverage |
| **Customization** | Limited | Intelligent adaptation |
| **Pattern Recognition** | None | Advanced analysis |
| **Security** | No checks | Security scanning |

## Requirements

```
pydantic-ai>=0.0.1
langgraph>=0.1.0
httpx>=0.24.0
pydantic>=2.0.0
```

## Troubleshooting

### Agent Errors

If an agent fails:
1. Check the error messages in the console output
2. Review the `errors` list in the result
3. Enable debug mode for detailed logging

### Validation Failures

If code validation fails:
1. Check `validation_results` for specific issues
2. Review generated code manually
3. Adjust customize_config if needed

### Performance Issues

For large collections (>100 requests):
1. Process in batches
2. Use more powerful LLM (GPT-4 vs GPT-3.5)
3. Increase timeout values

## Contributing

To add a new agent:

1. Define output model in `agent_models.py`
2. Create agent initializer in `agent_graph_agents.py`
3. Implement node function in `agent_graph_nodes.py`
4. Add node to graph in `agent_graph.py`
5. Update documentation

## References

- [Design Document](./agent_design.md) - Comprehensive architecture design
- [Pydantic AI Docs](https://ai.pydantic.dev/multi-agent-applications/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Postman Collection Format](https://schema.postman.com/)

## License

See project LICENSE file.
