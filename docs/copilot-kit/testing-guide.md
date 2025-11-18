> Last updated: 2025-11-17

# Testing GitHub Copilot Custom Prompts

This guide helps you verify that the custom prompts are working correctly in your VS Code environment.

## Prerequisites

- ✅ GitHub Copilot extension installed in VS Code
- ✅ GitHub Copilot Chat extension installed in VS Code
- ✅ Active GitHub Copilot subscription

## Quick Test

### 1. Open Copilot Chat

Press `Ctrl+Alt+I` (Windows/Linux) or `Cmd+Shift+I` (Mac) to open GitHub Copilot Chat.

### 2. Test a Simple Prompt

Type the following in the chat:

```
/code-review
```

If the prompt is working, Copilot should recognize it and start gathering context for a code review.

### 3. Test with Selection

1. Open any Python file in your project
2. Select a function or class
3. In Copilot Chat, type:
   ```
   /refactor
   ```

The prompt should analyze your selected code and suggest refactoring improvements.

## Testing All Prompts

You can test each prompt individually:

### Architecture Review
```
/architecture-review
```
**Expected:** Copilot asks about or analyzes the architecture of selected code/file

### Code Review
```
/code-review
```
**Expected:** Copilot performs a detailed code review with severity ratings

### Pragmatic Code Review
```
/pragmatic-code-review
```
**Expected:** Copilot provides a balanced, production-focused review

### Refactor
```
/refactor
```
**Expected:** Copilot suggests refactoring improvements

### Optimize Performance
```
/optimize-performance
```
**Expected:** Copilot analyzes code for performance issues

### Document
```
/document
```
**Expected:** Copilot generates comprehensive documentation

### Create Prompt
```
/create-prompt Generate unit tests for Python functions
```
**Expected:** Copilot creates a new custom prompt file

## Testing MCP Servers

### Sequential Thinking

To test if Sequential Thinking MCP is working:

```
/architecture-review
```

If Sequential Thinking is active, you'll see structured step-by-step reasoning in the response.

### Memory

To test Memory MCP:

1. In Copilot Chat, ask it to remember something:
   ```
   Remember that this project uses Python 3.11 and pytest for testing.
   ```

2. In a new conversation, ask:
   ```
   What testing framework does this project use?
   ```

If Memory is working, it should recall the information.

### Context7

To test Context7:

```
How do I use the latest pytest fixtures?
```

Context7 should provide up-to-date information about pytest.

## Troubleshooting

### Prompts Not Recognized

**Symptom:** Typing `/code-review` doesn't show the custom prompt

**Solutions:**
1. Reload VS Code window (`Ctrl+Shift+P` → "Developer: Reload Window")
2. Verify files exist in `.github/prompts/`
3. Check YAML frontmatter is valid in prompt files
4. Ensure GitHub Copilot Chat extension is up to date

### MCP Servers Not Working

**Symptom:** MCP features not available

**Solutions:**
1. Verify `.vscode/mcp.json` exists
2. Check VS Code settings:
   - Open Settings (`Ctrl+,`)
   - Search for "MCP"
   - Ensure GitHub Copilot MCP is enabled
3. Reload VS Code window
4. Check MCP server logs in Output panel

### Memory Not Persisting

**Symptom:** Memory MCP doesn't remember information

**Solutions:**
1. Verify `.mcp/memory.json` exists (copy from `.mcp/memory.json.dist`)
2. Check file permissions (should be readable/writable)
3. Verify `.gitignore` excludes `.mcp/memory.json` (to avoid committing)

## Verification Checklist

Run through this checklist to ensure everything is working:

- [ ] Can invoke `/code-review` in Copilot Chat
- [ ] Can invoke `/refactor` in Copilot Chat
- [ ] Can invoke `/document` in Copilot Chat
- [ ] Sequential Thinking provides structured analysis
- [ ] Memory MCP remembers context (if enabled)
- [ ] Context7 provides up-to-date framework info (if enabled)
- [ ] Prompts work with selected code
- [ ] Prompts work with entire files

## Getting Help

If you encounter issues:

1. Check [Custom Prompts Guide](custom-prompts-guide.md) for detailed usage instructions
2. Review [VS Code Copilot documentation](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
3. Verify your GitHub Copilot subscription is active
4. Check GitHub Copilot status: https://githubstatus.com/

## Advanced Testing

### Testing with Arguments

Some prompts accept arguments:

```
/code-review focus=security
/pragmatic-code-review performance
/optimize-performance
```

### Testing with Different Files

Try prompts on different file types:
- Python files (`.py`)
- JavaScript/TypeScript (`.js`, `.ts`)
- Configuration files (`.json`, `.yaml`)
- Documentation (`.md`)

### Testing Error Handling

Test how prompts handle:
- Empty selections
- Invalid code
- Large files
- Complex nested structures

## Success Indicators

Your setup is working correctly if:

✅ Prompts appear in autocomplete when typing `/`
✅ Prompts gather context from project files
✅ Responses follow the expected output format from prompt files
✅ MCP servers enhance responses (structured thinking, memory, etc.)
✅ Prompts respect project-specific instructions in `.github/instructions/`

---

**Note:** These tests verify the prompt infrastructure. The quality of AI responses depends on the underlying model and your code context.
