# ContextStream MCP Setup

This directory contains ContextStream MCP server configuration and custom instructions for all AI coding tools.

## Quick Setup

**NOTE: Replace `YOUR_API_KEY_HERE` with your actual ContextStream API key from https://contextstream.io**

### 1. Install for All Tools

Run the installation script:
```bash
cd ~/0-Projects_Old_Local/code-hq/mcp-hq
bash templates/contextstream-instructions/install-all.sh YOUR_API_KEY_HERE
```

### 2. Manual Installation Per Tool

#### Claude Code
```bash
# Add ContextStream instructions to global CLAUDE.md
cat templates/contextstream-instructions/CLAUDE-CODE-INSTRUCTIONS.md >> ~/.claude/CLAUDE.md

# Configure MCP server in ~/.claude.json
# Add the contextstream server from active/contextstream-mcp.json
```

#### Codex CLI
```bash
# Add ContextStream instructions to global AGENTS.md  
cat templates/contextstream-instructions/CODEX-CLI-GEMINI-COPILOT-INSTRUCTIONS.md >> ~/.codex/AGENTS.md

# Configure MCP server in ~/.codex/config.toml
# Add [mcp_servers.contextstream] section
```

#### Gemini CLI
```bash
# Add ContextStream instructions to global GEMINI.md
cat templates/contextstream-instructions/CODEX-CLI-GEMINI-COPILOT-INSTRUCTIONS.md >> ~/.gemini/GEMINI.md

# Configure MCP server in ~/.gemini/settings.json
# Add contextstream to mcpServers
```

#### GitHub Copilot CLI
```bash
# Configure MCP server in ~/.copilot/mcp-config.json
# Add contextstream to mcpServers
```

#### Antigravity
```bash
# Configuration structure TBD - check Antigravity documentation for MCP support
```

## Tool Name Prefixes

**CRITICAL:** Different tools use different naming conventions for MCP tools!

| Tool | Tool Name Format | Example |
|------|------------------|---------|
| Claude Code | `mcp__contextstream__<tool>` | `mcp__contextstream__session_init` |
| Codex CLI | `<tool>` (raw name) | `session_init` |
| Gemini CLI | `<tool>` (raw name) | `session_init` |
| Copilot CLI | `<tool>` (raw name) | `session_init` |
| Antigravity | `<tool>` (raw name) | `session_init` |

## Required Workflow

### First Message of Every Conversation
```
1. Call session_init(folder_path="<cwd>", context_hint="<user's first message>")
2. Then respond to user
```

### Every Subsequent Message
```
1. Call context_smart(user_message="<current user message>") FIRST
2. Then respond to user
```

### After Completing Any Task
```
1. Call session_capture(...) to save decisions/preferences/insights
2. This is MANDATORY, not optional
```

### When User Expresses Frustration or Makes Corrections
```
1. Immediately call session_capture_lesson(...)
2. Include: title, severity, category, trigger, impact, prevention, keywords
```

## Files in This Directory

- `CLAUDE-CODE-INSTRUCTIONS.md` - Instructions for Claude Code (uses `mcp__contextstream__` prefix)
- `CODEX-CLI-GEMINI-COPILOT-INSTRUCTIONS.md` - Instructions for Codex, Gemini, Copilot (use raw tool names)
- `install-all.sh` - Automated installation script
- `README.md` - This file

## Configuration Files

See `active/contextstream-mcp.json` for:
- Full metadata and capabilities
- Deployment configurations for each tool
- Environment variable requirements
- Tool-specific configuration examples

## Troubleshooting

### Tools not appearing
- Restart your AI tool after editing config files
- Verify Node.js 18+ is installed: `node --version`
- Check MCP server is configured correctly in tool's config file

### Unauthorized errors  
- Verify `CONTEXTSTREAM_API_KEY` is set correctly
- Verify `CONTEXTSTREAM_API_URL` is `https://api.contextstream.io`
- Get a new API key from https://contextstream.io

### Wrong workspace/project
- Use `workspace_associate` tool to map current repo to correct workspace
- Or explicitly pass workspace_id/project_id to tools

## Links

- ContextStream Website: https://contextstream.io
- Documentation: https://contextstream.io/docs/mcp
- GitHub: https://github.com/contextstream/mcp-server
- NPM: https://www.npmjs.com/package/@contextstream/mcp-server
