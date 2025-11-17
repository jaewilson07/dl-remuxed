# GitHub Copilot Kit Documentation

This directory contains documentation and guides for using GitHub Copilot custom prompts and MCP (Model Context Protocol) servers in this project.

## 📚 Available Guides

### [Custom Prompts Guide](custom-prompts-guide.md)
Comprehensive guide covering:
- What custom prompts are and why they're useful
- How to use the prompts in this project
- Detailed documentation on code review prompts
- Best practices for creating and using prompts
- Examples and usage patterns

### [Fork Sync Guide](fork-sync-guide.md)
Information about:
- How copilot-kit files are kept up to date
- Automatic synchronization workflow
- Manual sync procedures
- Handling merge conflicts

## 🎨 Custom Prompts

The project includes these ready-to-use prompts in `.github/prompts/`:

| Prompt | Description | Usage |
|--------|-------------|-------|
| **architecture-review** | Quick sanity check of solution architecture | `/architecture-review` |
| **code-review** | High-rigor technical code review | `/code-review` |
| **pragmatic-code-review** | Production-focused balanced review | `/pragmatic-code-review` |
| **refactor** | Intelligent code refactoring | `/refactor` |
| **optimize-performance** | Performance anti-pattern detection | `/optimize-performance` |
| **document** | Generate comprehensive documentation | `/document` |
| **create-prompt** | Meta-prompt to generate new prompts | `/create-prompt` |

## 🤖 MCP Server Configuration

The `.vscode/mcp.json` file configures these Model Context Protocol servers:

- **Sequential Thinking** - Structured problem-solving for complex tasks
- **Memory** - Persistent context across conversations
- **Context7** - Up-to-date framework/library documentation
- **Shadcn UI** - UI component knowledge (optional)
- **Chrome DevTools** - Browser debugging capabilities (optional)

## 🚀 Quick Start

1. **Ensure GitHub Copilot is installed** in VS Code
2. **Enable MCP in Copilot settings**
3. **Copy the memory template**:
   ```bash
   cp .mcp/memory.json.dist .mcp/memory.json
   ```
4. **Start using prompts** in Copilot Chat:
   ```
   /code-review
   /refactor
   /document
   ```

## 📖 Learn More

- See the main [README.md](../../README.md#github-copilot-integration) for project-specific setup
- Read the [Custom Prompts Guide](custom-prompts-guide.md) for detailed usage instructions
- Check [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on creating new prompts

## 🌐 Source

These files are merged from the [copilot-kit](https://github.com/jaewilson07/copilot-kit) repository, which is itself a fork of [ikcode-dev/copilot-kit](https://github.com/ikcode-dev/copilot-kit).

For updates and the latest versions, see the [Fork Sync Guide](fork-sync-guide.md).
