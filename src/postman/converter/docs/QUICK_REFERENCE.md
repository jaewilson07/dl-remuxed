# Multi-Agent Converter - Quick Reference

## 🚀 Quick Start

```python
from postman.converter import convert_postman_collection_sync

result = convert_postman_collection_sync(
    collection_path="api.postman_collection.json",
    export_folder="./generated"
)
```

## 📁 File Structure

```
converter/
├── agent_models.py          # Pydantic models for agent outputs
├── agent_tools.py           # Helper functions for agents
├── agent_graph_agents.py    # Agent initializers
├── agent_graph_state.py     # Graph state definition
├── agent_graph_nodes.py     # Node implementations
├── agent_graph.py           # Main graph & entry point
├── example_usage.py         # Working example
├── agent_design.md          # Architecture design doc
├── AGENT_README.md          # User documentation
└── IMPLEMENTATION_SUMMARY.md # This summary
```

## 🎯 The 12 Agents (Quick Reference)

| Agent | Role | Phase |
|-------|------|-------|
| Orchestrator | Plans strategy | Planning |
| Parser | Loads collection | Parsing |
| Validator | Validates structure | Validation |
| Structure Analyzer | Analyzes organization | Analysis ∥ |
| Auth Analyzer | Analyzes auth | Analysis ∥ |
| Parameter Analyzer | Analyzes params | Analysis ∥ |
| Header Analyzer | Analyzes headers | Analysis ∥ |
| Aggregator | Synthesizes insights | Synthesis |
| Code Generator | Generates functions | Generation |
| Test Generator | Generates tests | Generation |
| Code Validator | Validates code | Validation |
| Formatter | Polishes code | Formatting |

∥ = Runs in parallel

## 📊 Graph Workflow

```
START → Orchestrator → Parser → Validator → [4 Parallel Analyzers] →
Aggregator → Code Gen → Test Gen → Validator → Formatter → END
```

## 💻 API Reference

### Main Functions

```python
# Async version
async def convert_postman_collection(
    collection_path: str,
    export_folder: str,
    customize_config: Optional[dict] = None,
    write_files: bool = True
) -> dict

# Sync version
def convert_postman_collection_sync(
    collection_path: str,
    export_folder: str,
    customize_config: Optional[dict] = None,
    write_files: bool = True
) -> dict
```

### Customize Config

```python
customize_config = {
    "required_headers": ["authorization", "content-type"],
    "default_params": ["limit", "offset"],
    "ignored_params": ["debug"],
    "module_structure": {...}
}
```

### Return Value

```python
{
    "conversion_plan": {...},        # Planning details
    "parsed_collection": {...},      # Parsed collection
    "validation_report": {...},      # Validation results
    "structure_analysis": {...},     # Structure insights
    "auth_analysis": {...},          # Auth insights
    "parameter_analysis": {...},     # Parameter insights
    "header_analysis": {...},        # Header insights
    "aggregated_analysis": {...},    # Unified strategy
    "generated_functions": [...],    # Generated code
    "generated_tests": [...],        # Generated tests
    "validation_results": [...],     # Code validation
    "formatted_code": {              # Final output
        "func_name.py": "code..."
    },
    "export_paths": [...],           # Written file paths
    "errors": [...],                 # Any errors
    "warnings": [...]                # Any warnings
}
```

## 🛠️ Common Use Cases

### 1. Basic Conversion

```python
result = convert_postman_collection_sync(
    "api.json",
    "./output"
)
```

### 2. Custom Headers & Params

```python
result = convert_postman_collection_sync(
    "api.json",
    "./output",
    customize_config={
        "required_headers": ["authorization"],
        "default_params": ["page", "limit"]
    }
)
```

### 3. Preview Without Writing

```python
result = convert_postman_collection_sync(
    "api.json",
    "./output",
    write_files=False
)

# Examine code
for filename, code in result["formatted_code"].items():
    print(f"{filename}:\n{code[:200]}")
```

### 4. Access Analysis Results

```python
result = convert_postman_collection_sync("api.json", "./output")

# Structure insights
structure = result["structure_analysis"]
print(f"Complexity: {structure['complexity_score']}")

# Auth strategy
auth = result["auth_analysis"]
print(f"Auth types: {auth['auth_types']}")

# Parameters
params = result["parameter_analysis"]
print(f"Common params: {params['common_params']}")
```

## 🔧 Extending the Framework

### Add a New Agent

```python
# 1. Add model in agent_models.py
class MyAgentOutput(BaseModel):
    result: str
    confidence: float

# 2. Add initializer in agent_graph_agents.py
def initialize_my_agent() -> Agent:
    return Agent(
        "openai:gpt-4o",
        output_type=MyAgentOutput,
        system_prompt="You are..."
    )

# 3. Add node in agent_graph_nodes.py
async def my_agent_node(state: PostmanConversionState) -> dict:
    agent = initialize_my_agent()
    result = await agent.run("prompt")
    return {"my_result": result.data.model_dump()}

# 4. Wire into graph in agent_graph.py
graph_builder.add_node("my_agent", my_agent_node)
graph_builder.add_edge("previous_node", "my_agent")
graph_builder.add_edge("my_agent", "next_node")
```

### Add a New Tool

```python
# Add to agent_tools.py
def my_custom_tool(input_data: dict) -> dict:
    """Tool description."""
    # Process input
    result = process(input_data)
    return result
```

## 📝 Generated Code Format

Each function includes:

```python
async def function_name(
    auth: DomoAuth,              # Authentication
    param1: str,                 # Required params
    param2: int = 100,          # Optional params
    session: Optional[httpx.AsyncClient] = None,
    debug_api: bool = False,
) -> httpx.Response:
    """Function description.

    Detailed explanation of what this does.

    Args:
        auth: Authentication object
        param1: Description of param1
        param2: Description of param2
        session: Optional session for connection reuse
        debug_api: Enable debug logging

    Returns:
        httpx.Response with the API response

    Raises:
        httpx.HTTPStatusError: If request fails
        ValueError: If params invalid

    Example:
        >>> response = await function_name(auth, "value")
        >>> data = response.json()
    """
    # Implementation
    pass
```

## 🧪 Generated Test Format

```python
@pytest.mark.asyncio
async def test_function_name_success():
    """Test successful execution."""
    # Arrange
    auth = MockAuth()

    # Act
    response = await function_name(auth, "test")

    # Assert
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_function_name_error():
    """Test error handling."""
    auth = MockAuth()

    with pytest.raises(httpx.HTTPStatusError):
        await function_name(auth, "invalid")
```

## 🐛 Troubleshooting

### Agent Fails
```python
# Check errors in result
if result.get("errors"):
    for error in result["errors"]:
        print(f"Error: {error}")
```

### Validation Fails
```python
# Check validation results
for validation in result["validation_results"]:
    if not validation["is_valid"]:
        print(f"Issues: {validation['syntax_errors']}")
```

### Code Not Generated
```python
# Check current phase
print(f"Stopped at: {result['current_phase']}")

# Check intermediate results
print(f"Parsed: {result.get('parsed_collection') is not None}")
print(f"Validated: {result.get('validation_report') is not None}")
```

## ⚡ Performance Tips

1. **Large Collections**: Process in batches
2. **Parallel**: Leverage the 4 parallel analyzers
3. **Session Reuse**: Use httpx.AsyncClient session
4. **Caching**: Cache analysis for repeated runs

## 🔒 Security

The Code Validator agent checks for:
- SQL injection patterns
- XSS vulnerabilities
- Insecure auth handling
- Credential exposure
- Unsafe eval/exec

## 📖 Documentation Links

- **Design Doc**: `agent_design.md` - Architecture details
- **User Guide**: `AGENT_README.md` - Complete documentation
- **Summary**: `IMPLEMENTATION_SUMMARY.md` - Implementation overview
- **Example**: `example_usage.py` - Working code example

## 🎓 Learning Path

1. Read `AGENT_README.md` for overview
2. Review `agent_design.md` for architecture
3. Run `example_usage.py` to see it work
4. Explore `agent_graph_nodes.py` for workflow
5. Check `agent_models.py` for data structures
6. Modify `customize_config` for your needs

## 💡 Tips & Tricks

### Inspect Intermediate Results
```python
# Run without writing files
result = convert_postman_collection_sync(
    "api.json", "./out", write_files=False
)

# Examine each phase
print(result["conversion_plan"])
print(result["structure_analysis"])
print(result["aggregated_analysis"])
```

### Debug Agent Prompts
```python
# Modify prompts in agent_graph_agents.py
# Add more context, examples, or constraints
```

### Custom Module Organization
```python
customize_config = {
    "module_structure": {
        "users": ["get_user", "list_users"],
        "products": ["get_product", "create_product"]
    }
}
```

## 🚦 Status Indicators

Console output shows:
- 🎯 Orchestrator
- 📄 Parser
- ✓ Validator
- 🔍 Analysis
- 🔗 Aggregator
- 💻 Code Generator
- 🧪 Test Generator
- ✨ Formatter
- ✅ Success
- ❌ Error
- ⚠️  Warning

## 📞 Support

For issues:
1. Check console output for errors
2. Review `errors` in result
3. Enable debug mode
4. Check documentation
5. Review example code

---

**Quick Links:**
- [Architecture Design](./agent_design.md)
- [User Documentation](./AGENT_README.md)
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md)
- [Example Usage](./example_usage.py)
