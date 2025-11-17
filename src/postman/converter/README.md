> Last updated: 2025-11-06

# Postman to Python Multi-Agent Converter

A sophisticated AI-powered framework for converting Postman collections into production-ready Python API client code.

## 📁 Folder Structure

```
converter/
├── agent_graph.py              # Main orchestration & entry point
├── agent_graph_agents.py       # 12 specialized AI agents
├── agent_graph_nodes.py        # Workflow node implementations
├── agent_graph_state.py        # Graph state management
├── agent_models.py             # Pydantic output models
├── agent_tools.py              # Utility functions for agents
├── example_usage.py            # Working example
├── __init__.py                 # Package exports
│
├── core.py                     # Core converter implementation
├── models.py                   # Postman data models
├── utils.py                    # Helper utilities
│
├── legacy/                     # DEPRECATED: Backward compatibility
│   └── __init__.py            # Re-exports from core/models
│
├── tests/                      # Test files
│   ├── test_agent_conversion.py   # Full multi-agent tests
│   ├── test_simple_conversion.py  # Quick validation test
│   └── test_models.py             # Model tests
│
└── docs/                       # Documentation
    ├── AGENT_README.md        # User guide
    ├── agent_design.md        # Architecture design
    ├── QUICK_REFERENCE.md     # Developer quick ref
    ├── IMPLEMENTATION_SUMMARY.md
    ├── TESTING.md
    └── COMPLETE.md
```

## 🚀 Quick Start

### Using the Multi-Agent Framework

```python
from postman.converter import convert_postman_collection_sync

result = convert_postman_collection_sync(
    collection_path="api.postman_collection.json",
    export_folder="./generated"
)

print(f"Generated {len(result['formatted_code'])} files")
```

### Using the Legacy Converter

```python
from postman.converter import PostmanCollection, PostmanRequestConverter

collection = PostmanCollection.from_file("api.postman_collection.json")
request = collection.requests[0]

converter = PostmanRequestConverter(Request=request)
code = converter.build_request_code()
```

## 🏗️ The Multi-Agent System

### 12 Specialized Agents

**Planning (Sequential)**
1. **Orchestrator** - Plans conversion strategy
2. **Parser** - Loads & parses collection
3. **Validator** - Validates structure

**Analysis (Parallel ⚡)**
4. **Structure Analyzer** - Organization patterns
5. **Auth Analyzer** - Authentication patterns
6. **Parameter Analyzer** - Query params & types
7. **Header Analyzer** - HTTP headers

**Generation (Sequential)**
8. **Aggregator** - Synthesizes analyses
9. **Code Generator** - Python functions
10. **Test Generator** - Pytest tests

**Quality (Sequential)**
11. **Code Validator** - Quality checks
12. **Formatter** - Final polish

### Workflow

```
START → Orchestrator → Parser → Validator →
[4 Parallel Analyzers] → Aggregator →
Code Gen → Test Gen → Validator → Formatter → END
```

## 📦 Installation

### Core (Legacy Converter)
```bash
pip install pydantic httpx
```

### Multi-Agent Framework
```bash
pip install pydantic-ai langgraph httpx
```

## 🧪 Testing

```bash
# Quick validation test
python tests/test_simple_conversion.py

# Full multi-agent test suite
pytest tests/test_agent_conversion.py -v

# All tests
pytest tests/ -v
```

## 📖 Documentation

- **[User Guide](AGENT_README.md)** - Complete usage guide
- **[Architecture](agent_design.md)** - System design & patterns
- **[Quick Reference](QUICK_REFERENCE.md)** - Developer cheat sheet
- **[Testing Guide](TESTING.md)** - How to test
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - What we built

## ✨ Key Features

### Multi-Agent Framework
- ✅ **12 Specialized Agents** - Each with domain expertise
- ✅ **Parallel Analysis** - 4 analyzers run concurrently
- ✅ **Intelligent Generation** - AI-optimized code quality
- ✅ **Comprehensive Testing** - Pytest tests auto-generated
- ✅ **Multi-Stage Validation** - Syntax, types, security
- ✅ **Production Ready** - Black/ruff formatted output

### Legacy Converter
- ✅ **Template-Based** - Fast, predictable conversion
- ✅ **No Dependencies** - Just pydantic & httpx
- ✅ **Battle-Tested** - Proven in production
- ✅ **Backwards Compatible** - Drop-in replacement

## 🔧 Development

### Project Structure

- **Agent Files**: Core multi-agent implementation
- **Legacy Files**: Original converter (in `legacy/`)
- **Test Files**: Validation & testing (in `tests/`)
- **Docs**: Comprehensive documentation

### Adding a New Agent

1. Add output model to `agent_models.py`
2. Create initializer in `agent_graph_agents.py`
3. Implement node in `agent_graph_nodes.py`
4. Wire into graph in `agent_graph.py`
5. Update state in `agent_graph_state.py` if needed

See [Architecture Design](agent_design.md) for details.

## 📊 Comparison

| Feature | Legacy | Multi-Agent |
|---------|--------|-------------|
| Speed | Fast | Slower (AI calls) |
| Quality | Good | Excellent |
| Analysis | None | 4 parallel analyzers |
| Tests | Optional | Always generated |
| Validation | Basic | Comprehensive |
| Dependencies | Minimal | pydantic-ai, langgraph |
| Use Case | Quick conversion | Production code |

## 🎯 Use Cases

### Use Multi-Agent When:
- ✅ Need production-quality code
- ✅ Want comprehensive tests
- ✅ Need intelligent analysis
- ✅ Have complex collections
- ✅ Quality > Speed

### Use Legacy When:
- ✅ Need quick conversion
- ✅ Simple collections
- ✅ Minimal dependencies
- ✅ Speed > Quality
- ✅ Proven patterns work

## 🌟 Examples

See `example_usage.py` for complete working example.

### Multi-Agent Example
```python
import asyncio
from agent_graph import convert_postman_collection

async def main():
    result = await convert_postman_collection(
        collection_path="api.json",
        export_folder="./output",
        customize_config={
            "required_headers": ["authorization"],
            "default_params": ["limit", "offset"]
        }
    )

    print(f"✅ Generated {len(result['formatted_code'])} files")

asyncio.run(main())
```

### Legacy Example
```python
from legacy import PostmanCollectionConverter

converter = PostmanCollectionConverter.from_postman_collection(
    postman_path="api.json",
    export_folder="./output"
)
```

## 📞 Support

- **Issues**: Check test output for detailed errors
- **Documentation**: See docs folder for guides
- **Examples**: See `example_usage.py` for patterns
- **Legacy**: Check `legacy/` for original code

## 🙏 Credits

Built using:
- [Pydantic AI](https://ai.pydantic.dev/) - Multi-agent framework
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Graph workflow
- [Pydantic](https://pydantic.dev/) - Data validation
- [httpx](https://www.python-httpx.org/) - HTTP client

## 📄 License

See project LICENSE file.

---

**Quick Links:**
- [Start Here](AGENT_README.md) - User guide
- [Architecture](agent_design.md) - System design
- [Quick Ref](QUICK_REFERENCE.md) - Cheat sheet
- [Tests](TESTING.md) - Testing guide
