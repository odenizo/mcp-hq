# GitHub Copilot CLI Documentation

This directory contains official GitHub Copilot CLI documentation from the github/docs repository.

## 📁 Documentation Files

- **copilot-cli-about.md** - About GitHub Copilot CLI (concepts and overview)
- **copilot-cli-install.md** - Installing GitHub Copilot CLI
- **copilot-cli-use.md** - Using GitHub Copilot CLI (basic usage guide)
- **copilot-custom-instructions.md** - Adding repository custom instructions
- **copilot-custom-agents.md** - Creating custom agents
- **copilot-mcp-extend.md** - Extending Copilot with Model Context Protocol (MCP)

## 📖 Global Instructions for Copilot CLI

Copilot CLI supports **three types** of custom instructions:

### 1. Repository-Wide Custom Instructions
**Location:** `.github/copilot-instructions.md`

Applies to all requests made in the context of a repository.

```bash
# Create in repository root:
mkdir -p .github
touch .github/copilot-instructions.md
```

### 2. Path-Specific Custom Instructions
**Location:** `.github/instructions/NAME.instructions.md`

Applies to requests made in the context of files matching specified paths.

```bash
# Create path-specific instructions:
mkdir -p .github/instructions
touch .github/instructions/backend.instructions.md
touch .github/instructions/frontend.instructions.md
```

**Note:** If a path matches both repository-wide and path-specific instructions, both are used. Avoid conflicts as Copilot's choice between conflicting instructions is non-deterministic.

### 3. Agent Instructions (Global-ish)
**Location:** Repository root

For AI agents, Copilot CLI looks for:
- `CLAUDE.md` (for Claude-based agents)
- `GEMINI.md` (for Gemini-based agents)  
- `COPILOT.md` (likely for Copilot-specific instructions)

These files in the repository root act as agent-specific global instructions.

## 🔧 Command Line Options

Copilot CLI supports various flags to control custom instructions:

```bash
# Disable custom instructions
copilot --no-custom-instructions

# Add additional MCP configuration
copilot --additional-mcp-config <json>

# Allow all tools (for automation)
copilot --allow-all-tools

# Specify custom agent
copilot --agent <agent-name>
```

## 🌐 True Global Instructions

Based on the documentation and Copilot CLI behavior, there is **NO system-wide global instructions file** like:
- ❌ `~/.copilot/COPILOT.md` (doesn't exist)
- ❌ `~/.copilot/instructions.md` (doesn't exist)
- ❌ Global instruction configuration in `~/.copilot/config.json`

**Workaround for "Global" Instructions:**

To have instructions that apply across all projects:

1. **Create a parent directory instructions file:**
   ```bash
   # If all projects are in ~/dev, create:
   ~/dev/.github/copilot-instructions.md
   ```

2. **Use agent-specific files in each project:**
   ```bash
   # In each project root:
   touch CLAUDE.md
   touch GEMINI.md
   touch COPILOT.md
   ```

3. **Symlink from a template:**
   ```bash
   # Create template
   mkdir -p ~/templates/copilot
   echo "Your global instructions" > ~/templates/copilot/COPILOT.md
   
   # Symlink in each project
   cd ~/your-project
   ln -s ~/templates/copilot/COPILOT.md .
   ```

## 📦 MCP Configuration

**Location:** `~/.copilot/mcp-config.json`

This is the ONLY global configuration file for Copilot CLI. It configures MCP servers but NOT custom instructions.

Example structure:
```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {
        "API_KEY": "value"
      },
      "tools": ["*"]
    }
  }
}
```

## 🎯 Copilot CLI Tool Naming Convention

**Important:** Copilot CLI uses **server-prefixed tool names**:

Format: `<server-name>-<tool-name>`

Examples:
- `github-mcp-server-get_file_contents`
- `desktop-commander-read_file`
- `contextstream-session_init`
- `mcp-shrimp-task-manager-plan_task`

**NOT like:**
- ❌ Claude Code: `mcp__contextstream__session_init` (double underscore)
- ❌ Codex/Gemini: `session_init` (raw tool name)

## 📚 Official Documentation Links

- [About Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)
- [Install Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)
- [Using Copilot CLI](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
- [Repository Custom Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- [Creating Custom Agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Extending with MCP](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/extend-coding-agent-with-mcp)

## 🔄 ContextStream Integration for Copilot CLI

For ContextStream MCP server integration, see:
- `../../templates/contextstream-instructions/COPILOT-CLI-INSTRUCTIONS.md`
- `../../active/contextstream-mcp.json`

**Remember:** Use `contextstream-session_init` (with prefix) not `session_init`!

## ✅ Best Practices

1. **Repository instructions:** Use `.github/copilot-instructions.md` for project-specific guidelines
2. **Path-specific:** Use `.github/instructions/*.instructions.md` for component-specific rules
3. **Agent files:** Use `COPILOT.md` in repo root for Copilot-specific agent instructions
4. **MCP config:** Configure servers in `~/.copilot/mcp-config.json` only
5. **Tool naming:** Always use `<server>-<tool>` format for MCP tools
6. **No conflicts:** Avoid conflicting instructions between files

## 🚨 Common Mistakes

❌ **Trying to create `~/.copilot/COPILOT.md`** - Copilot CLI doesn't read this
❌ **Using raw tool names** - Use `contextstream-session_init` not `session_init`
❌ **Expecting global instructions** - No true global file exists, use per-repo files
❌ **Conflicting instructions** - Between repository-wide and path-specific files

## 📝 Last Updated

- **Date:** 2024-12-17
- **Source:** github/docs repository
- **Copilot CLI Version:** Latest (as of documentation fetch date)
