# ContextStream MCP Server - Complete Installation Guide

**Date:** December 16, 2024  
**Repository:** mcp-hq (odenizo/mcp-hq)  
**Location:** ~/0-Projects_Old_Local/code-hq/mcp-hq

---

## What Was Done

I've set up a complete ContextStream MCP installation system in the mcp-hq repository with:

1. **ContextStream MCP Configuration** (`active/contextstream-mcp.json`)
   - Complete metadata and capabilities
   - Tool-specific configurations for all AI coding tools
   - Deployment instructions and environment variables

2. **Custom Instructions Templates** (`templates/contextstream-instructions/`)
   - `CLAUDE-CODE-INSTRUCTIONS.md` - For Claude Code (uses `mcp__contextstream__` prefix)
   - `CODEX-CLI-GEMINI-COPILOT-INSTRUCTIONS.md` - For Codex, Gemini, Copilot (raw tool names)
   - `README.md` - Comprehensive setup documentation
   - `install-all.sh` - Automated installation script

3. **Repository Structure**
   - Follows mcp-hq standards with active/, templates/, and nu/ directories
   - All configurations validated against repository patterns

---

## Quick Start

### Get Your API Key
1. Visit https://contextstream.io
2. Sign up or log in
3. Get your `CONTEXTSTREAM_API_KEY`

### Run Installation

```bash
cd ~/0-Projects_Old_Local/code-hq/mcp-hq
bash templates/contextstream-instructions/install-all.sh YOUR_API_KEY_HERE
```

This will:
- Add ContextStream custom instructions to all tool global instruction files
- Configure MCP servers in tool-specific config files
- Create backups of all modified files
- Show next steps

### Restart All AI Tools

**CRITICAL:** You MUST restart all AI tools for changes to take effect:
- Claude Code
- Codex CLI
- Gemini CLI
- GitHub Copilot CLI
- Antigravity (if applicable)

---

## Tool-Specific Configuration

### Claude Code

**Custom Instructions:** `~/.claude/CLAUDE.md`  
**MCP Config:** `~/.claude.json`  
**Tool Prefix:** `mcp__contextstream__`

**Example Tool Call:**
```
mcp__contextstream__session_init(folder_path="/path/to/project", context_hint="user's first message")
```

**Manual MCP Configuration (if needed):**
```json
{
  "mcpServers": {
    "contextstream": {
      "command": "npx",
      "args": ["-y", "@contextstream/mcp-server"],
      "env": {
        "CONTEXTSTREAM_API_URL": "https://api.contextstream.io",
        "CONTEXTSTREAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Codex CLI

**Custom Instructions:** `~/.codex/AGENTS.md`  
**MCP Config:** `~/.codex/config.toml`  
**Tool Prefix:** (none - raw names)

**Example Tool Call:**
```
session_init(folder_path="/path/to/project", context_hint="user's first message")
```

**TOML Configuration (auto-added by script):**
```toml
[mcp_servers.contextstream]
command = "npx"
args = ["-y", "@contextstream/mcp-server"]
startup_timeout_sec = 120

[mcp_servers.contextstream.env]
CONTEXTSTREAM_API_URL = "https://api.contextstream.io"
CONTEXTSTREAM_API_KEY = "your_api_key_here"
```

### Gemini CLI

**Custom Instructions:** `~/.gemini/GEMINI.md`  
**MCP Config:** `~/.gemini/settings.json`  
**Tool Prefix:** (none - raw names)

**Example Tool Call:**
```
session_init(folder_path="/path/to/project", context_hint="user's first message")
```

**JSON Configuration (auto-added by script):**
```json
{
  "mcpServers": {
    "contextstream": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@contextstream/mcp-server"],
      "env": {
        "CONTEXTSTREAM_API_URL": "https://api.contextstream.io",
        "CONTEXTSTREAM_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### GitHub Copilot CLI

**Custom Instructions:** (None - uses tool calls directly)  
**MCP Config:** `~/.copilot/mcp-config.json`  
**Tool Prefix:** (none - raw names)

**Example Tool Call:**
```
session_init(folder_path="/path/to/project", context_hint="user's first message")
```

**JSON Configuration (auto-added by script):**
```json
{
  "mcpServers": {
    "contextstream": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@contextstream/mcp-server"],
      "env": {
        "CONTEXTSTREAM_API_URL": "https://api.contextstream.io",
        "CONTEXTSTREAM_API_KEY": "${CONTEXTSTREAM_API_KEY}"
      },
      "tools": ["*"]
    }
  }
}
```

### Antigravity

**Status:** Configuration structure needs verification  
**Note:** Check Antigravity documentation for MCP server support

---

## Required Workflow (ALL TOOLS)

### First Message of Every Conversation
1. Call `session_init(folder_path="<cwd>", context_hint="<user's message>")`
2. Then respond

### Every Subsequent Message
1. Call `context_smart(user_message="<user's message>")` FIRST
2. Then respond

### After Completing Any Task
1. Call `session_capture(...)` to save decisions/preferences/insights
2. This is MANDATORY - not optional

### When User Expresses Frustration/Makes Corrections
1. Immediately call `session_capture_lesson(...)`
2. Include all required fields: title, severity, category, trigger, impact, prevention, keywords

---

## Key Concepts

### Why context_smart is Required

**Common Mistake:** "session_init already gave me context, I don't need context_smart"

**This is WRONG because:**
- `session_init` returns last ~10 items BY TIME (chronological)
- `context_smart` SEARCHES for items RELEVANT to THIS MESSAGE (semantic)

**Example:** User asks about authentication implemented 20 conversations ago:
- `session_init` won't have it (too old)
- `context_smart` FINDS it via semantic search

### Lesson Capture Severity Levels

- `critical`: Production outages, data loss, security issues
- `high`: Breaking changes, significant user impact  
- `medium`: Workflow inefficiencies, minor bugs
- `low`: Style/preference corrections

---

## File Locations

### mcp-hq Repository
- **Active Config:** `active/contextstream-mcp.json`
- **Claude Instructions:** `templates/contextstream-instructions/CLAUDE-CODE-INSTRUCTIONS.md`
- **Other Tools Instructions:** `templates/contextstream-instructions/CODEX-CLI-GEMINI-COPILOT-INSTRUCTIONS.md`
- **Install Script:** `templates/contextstream-instructions/install-all.sh`
- **Documentation:** `templates/contextstream-instructions/README.md`

### Tool Configurations (Auto-Modified)
- **Claude Code:** `~/.claude/CLAUDE.md`, `~/.claude.json`
- **Codex CLI:** `~/.codex/AGENTS.md`, `~/.codex/config.toml`
- **Gemini CLI:** `~/.gemini/GEMINI.md`, `~/.gemini/settings.json`
- **Copilot CLI:** `~/.copilot/mcp-config.json`

### Backups
All modified files are automatically backed up with timestamp:
- `filename.backup.YYYYMMDD_HHMMSS`

---

## Verification

After installation and restart:

1. **Test in each tool:**
   ```
   session_init(folder_path="/tmp", context_hint="test connection")
   ```

2. **Check for errors:**
   - Tool should not report "tool not found"
   - Should get a response about initializing session

3. **Verify in tool's MCP list:**
   - Claude Code: Check MCP tools list
   - Codex CLI: Run `codex` and check available tools
   - Gemini CLI: Check settings
   - Copilot CLI: Check mcp-config

---

## Troubleshooting

### Tool Not Found Errors
- **Restart the AI tool** - most common issue
- Verify Node.js 18+ installed: `node --version`
- Check MCP server config in tool's config file

### Authorization Errors
- Verify `CONTEXTSTREAM_API_KEY` is correct
- Check `CONTEXTSTREAM_API_URL` is `https://api.contextstream.io`
- Get new API key from https://contextstream.io

### Wrong Workspace/Project
- Use `workspace_associate` tool to map repo to workspace
- Or explicitly pass `workspace_id`/`project_id` to tools

### Installation Script Issues
- Ensure `jq` is installed for JSON manipulation: `brew install jq`
- Or manually edit config files using examples above

---

## Resources

- **ContextStream Website:** https://contextstream.io
- **Documentation:** https://contextstream.io/docs/mcp
- **GitHub Repository:** https://github.com/contextstream/mcp-server
- **NPM Package:** https://www.npmjs.com/package/@contextstream/mcp-server
- **mcp-hq Repository:** https://github.com/odenizo/mcp-hq

---

## Next Steps

1. ✅ Get your ContextStream API key from https://contextstream.io
2. ✅ Run the installation script with your API key
3. ✅ Restart all AI tools
4. ✅ Test `session_init` in each tool
5. ✅ Start using ContextStream in your workflows!

**Remember:** The custom instructions are now in your global instruction files, so every new conversation will automatically use ContextStream for persistent memory and context!
