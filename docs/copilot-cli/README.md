# GitHub Copilot CLI Documentation

This directory contains official GitHub Copilot CLI documentation from the github/docs repository.

## 📁 Documentation Files

- **copilot-cli-about.md** - About GitHub Copilot CLI (concepts and overview)
- **copilot-cli-install.md** - Installing GitHub Copilot CLI
- **copilot-cli-use.md** - Using GitHub Copilot CLI (basic usage guide)
- **copilot-custom-instructions.md** - Adding repository custom instructions
- **copilot-custom-agents.md** - Creating custom agents
- **copilot-mcp-extend.md** - Extending Copilot with Model Context Protocol (MCP)

## 📖 Custom Instructions in Copilot CLI

Copilot CLI supports **three levels** of custom instructions:

### Level 1: Repository-Wide Custom Instructions
**Location:** `.github/copilot-instructions.md`

Applies to all requests made in the context of a repository.

```bash
# Create in repository root:
mkdir -p .github
touch .github/copilot-instructions.md
```

### Level 2: Path-Specific Custom Instructions
**Location:** `.github/instructions/NAME.instructions.md`

Applies to requests made in the context of files matching specified paths.

```bash
# Create path-specific instructions:
mkdir -p .github/instructions
touch .github/instructions/backend.instructions.md
touch .github/instructions/frontend.instructions.md
```

**Note:** If a path matches both repository-wide and path-specific instructions, both are used. Avoid conflicts as Copilot's choice between conflicting instructions is non-deterministic.

### Level 3: Agent Instructions
**Locations:** 
- `AGENTS.md` - Anywhere in repo tree (nearest one takes precedence)
- `CLAUDE.md` - In repo root only (for Claude-based agents)
- `GEMINI.md` - In repo root only (for Gemini-based agents)

**Note:** `AGENTS.md` follows the [OpenAI agents.md standard](https://github.com/openai/agents.md). Multiple `AGENTS.md` files can exist in subdirectories, with the nearest one taking precedence.

**⚠️ There is NO `COPILOT.md` file!** Copilot uses `AGENTS.md` or the repository-wide instructions.

## 🌐 Global Instructions via Default Agent

To have instructions that apply **globally across all projects**, create a default user-level agent:

### Step 1: Create Default Agent Directory

```bash
mkdir -p ~/.copilot/agents/default
```

### Step 2: Create Agent Configuration

**File:** `~/.copilot/agents/default/agent.yaml`

```yaml
name: default
description: "Default global agent with system-wide instructions"
instructions_file: instructions.md
```

### Step 3: Create Global Instructions File

**File:** `~/.copilot/agents/default/instructions.md`

```markdown
# Global Copilot Instructions

## Code Style
- Use 2-space indentation for JavaScript/YAML
- Use 4-space indentation for Python
- Follow project-specific style guides

## Best Practices
- Write tests for all new functions
- Document public APIs
- Use meaningful variable names

## Security
- Never commit secrets to version control
- Use environment variables for sensitive data
- Follow OWASP guidelines for web applications
```

### Step 4: Make Default Agent Auto-Load

**Option A: Set as default in shell config**

Add to `~/.bashrc`, `~/.zshrc`, or equivalent:

```bash
export COPILOT_AGENT_DEFAULT=default
```

**Option B: Use explicitly in commands**

```bash
# Run with default agent
copilot --agent default --prompt "Your request"

# In interactive mode, select default agent
copilot
# Then use: /agent default
```

**Option C: Create symlink for quick access**

```bash
# Link to a common directory for reference
ln -s ~/.copilot/agents/default/instructions.md ~/instructions-global.md
```

### Step 5: Layering Instructions (Hierarchy)

When using default agent + repository instructions, the precedence is:

1. **Repository-specific** (`.github/copilot-instructions.md`) - **Highest priority**
2. **Path-specific** (`.github/instructions/*.instructions.md`)
3. **Agent-level** (`.AGENTS.md` / `CLAUDE.md` / `GEMINI.md`)
4. **Default agent** (`~/.copilot/agents/default/instructions.md`) - **Lowest priority**

**Example:** If a repo has `.github/copilot-instructions.md`, it will override the default agent instructions.

## 🔧 Command Line Options

Copilot CLI supports various flags to control custom instructions:

```bash
# Use specific agent globally
copilot --agent default --prompt "Your request"

# Disable custom instructions
copilot --no-custom-instructions

# Add additional MCP configuration
copilot --additional-mcp-config <json>

# Allow all tools (for automation)
copilot --allow-all-tools
```

## ✨ Recommended Global Instructions Setup

For maximum flexibility with global instructions:

```bash
# 1. Create default agent
mkdir -p ~/.copilot/agents/default

# 2. Copy template (if available)
cp ./templates/copilot-global-instructions.md ~/.copilot/agents/default/instructions.md

# 3. Create agent config
cat > ~/.copilot/agents/default/agent.yaml << 'EOF'
name: default
description: "Default global agent with system-wide instructions"
instructions_file: instructions.md
EOF

# 4. Test it
copilot --agent default --prompt "Tell me your instructions"
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

1. **Global instructions:** Create default agent in `~/.copilot/agents/default/` for system-wide guidelines
2. **Repository instructions:** Use `.github/copilot-instructions.md` for project-specific guidelines (overrides global)
3. **Path-specific:** Use `.github/instructions/*.instructions.md` for component-specific rules
4. **Agent files:** Use `AGENTS.md` following OpenAI agents.md standard (can be in subdirectories)
5. **Model-specific:** Use `CLAUDE.md` or `GEMINI.md` in repo root for model-specific instructions
6. **MCP config:** Configure servers in `~/.copilot/mcp-config.json` only
7. **Tool naming:** Always use `<server>-<tool>` format for MCP tools
8. **No conflicts:** Avoid conflicting instructions between files

## 🚨 Common Mistakes

❌ **Trying to create `~/.copilot/COPILOT.md`** - Copilot CLI doesn't read this
❌ **Using `COPILOT.md` instead of `AGENTS.md`** - COPILOT.md doesn't exist, use AGENTS.md
❌ **Using raw tool names** - Use `contextstream-session_init` not `session_init`
❌ **Expecting magic global instructions** - Use default agent setup explicitly
❌ **Conflicting instructions** - Between repository-wide and path-specific files

## 📝 Last Updated

- **Date:** 2024-12-17
- **Source:** github/docs repository + community research
- **Copilot CLI Version:** Latest (as of documentation fetch date)
