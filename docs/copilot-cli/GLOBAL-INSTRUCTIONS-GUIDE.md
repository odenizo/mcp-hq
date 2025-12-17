# Copilot CLI Global Instructions Guide

This guide explains how to set up **true global instructions** for GitHub Copilot CLI that apply across all your projects.

## Problem Statement

Copilot CLI's official documentation doesn't clearly document a global instructions mechanism. By default:
- Repository instructions in `.github/copilot-instructions.md` only apply to that repo
- There's no `~/.copilot/COPILOT.md` or similar global file
- You'd need to duplicate instructions in every project

**Solution:** Use a **default user-level agent** to achieve global instructions.

## Quick Start (5 minutes)

### Option 1: Automated Setup

```bash
# Clone or navigate to mcp-hq repo
cd mcp-hq

# Run setup script
bash scripts/setup-global-copilot-agent.sh

# Edit your global instructions
nano ~/.copilot/agents/default/instructions.md

# Test it
copilot --agent default --prompt "What are your instructions?"
```

### Option 2: Manual Setup

```bash
# Create agent directory
mkdir -p ~/.copilot/agents/default

# Create agent config
cat > ~/.copilot/agents/default/agent.yaml << 'EOF'
name: default
description: "Default global agent with system-wide instructions"
instructions_file: instructions.md
EOF

# Copy template instructions
cp ./templates/copilot-global-instructions.md ~/.copilot/agents/default/instructions.md

# Customize for your needs
nano ~/.copilot/agents/default/instructions.md

# Verify
copilot --agent default --prompt "What instructions are you following?"
```

## How It Works

### Directory Structure

```
~/.copilot/
├─ agents/
│  └─ default/
│     ├─ agent.yaml          # Agent metadata
│     └─ instructions.md     # Your global instructions
└─ mcp-config.json         # MCP server configuration (if used)
```

### Configuration Files

**File: `~/.copilot/agents/default/agent.yaml`**

```yaml
name: default
description: "Default global agent with system-wide instructions"
instructions_file: instructions.md
```

This tells Copilot CLI:
- The agent is named `default`
- It has a description (useful for listing agents)
- The instructions are in `instructions.md` in the same directory

**File: `~/.copilot/agents/default/instructions.md`**

Standard Markdown format containing your coding guidelines. Examples:

```markdown
# My Global Instructions

## Code Style
- 2 spaces for JavaScript
- 4 spaces for Python
- PascalCase for classes

## Best Practices
- Write tests for new functions
- Document public APIs
- Use meaningful variable names

## Security
- Never commit secrets
- Validate user input
- Keep dependencies updated
```

## Usage Methods

### Method 1: Command Line (One-off)

```bash
# Use default agent for a single command
copilot --agent default --prompt "Write a function to validate emails"
```

### Method 2: Interactive Mode (Per Session)

```bash
# Start interactive mode
copilot

# Then type:
/agent default

# Now all requests use default agent instructions
```

### Method 3: Shell Environment (Global)

Add to `~/.bashrc`, `~/.zshrc`, or equivalent:

```bash
# Auto-select default agent for all copilot commands
export COPILOT_AGENT_DEFAULT=default
```

Then:
```bash
# All copilot commands will use default agent automatically
copilot --prompt "Write a REST API handler"
```

### Method 4: Shell Alias (Convenient)

Add to shell config:

```bash
alias copilot-default='copilot --agent default'
alias c='copilot --agent default'
```

Then:
```bash
copilot-default --prompt "Your request"
# or shorter:
c --prompt "Your request"
```

## Configuration Examples

### Example 1: Python Developer

```markdown
# Python Developer Guidelines

## Code Style
- Use 4 spaces for indentation
- Follow PEP 8
- Use type hints
- Max line length: 100 characters

## Testing
- Use pytest for testing
- Aim for >80% code coverage
- Use fixtures for setup/teardown

## Documentation
- Use Google-style docstrings
- Document all public functions
- Include examples in docstrings
```

### Example 2: Full-Stack JavaScript

```markdown
# Full-Stack JavaScript Guidelines

## Frontend (React)
- Use functional components
- Use hooks for state management
- Component files: PascalCase
- Props: interfaces with TypeScript

## Backend (Node.js)
- Use Express.js conventions
- Return consistent JSON responses
- Use middleware for cross-cutting concerns
- Implement proper error handling

## Shared
- 2 spaces indentation
- Trailing commas in multi-line objects
- Use ESLint config
```

### Example 3: Security-Focused

```markdown
# Security-First Guidelines

## Input Validation
- Validate ALL user input
- Use allowlists, not blocklists
- Sanitize before DB queries
- Check for path traversal attacks

## Secrets Management
- Use environment variables
- Never commit .env files
- Rotate secrets regularly
- Use secrets manager in production

## Dependencies
- Run `npm audit` before committing
- Update dependencies monthly
- Review licenses (prefer MIT, Apache 2.0)
```

## Instruction Hierarchy

When using Copilot CLI with global instructions, the precedence is:

1. **Repository-Specific** (`.github/copilot-instructions.md`) - **Highest**
   - Applies only to this repo
   - Overrides all lower levels

2. **Path-Specific** (`.github/instructions/*.instructions.md`)
   - Applies to specific file paths
   - Applied after repo-specific

3. **Agent Files** (`.AGENTS.md`, `.CLAUDE.md`, `.GEMINI.md`)
   - Agent-specific guidance
   - Applied after path-specific

4. **Default Agent** (`~/.copilot/agents/default/instructions.md`) - **Lowest**
   - Global fallback
   - Applied if no repo instructions found

**Example Scenario:**

You're working on a Python project with:
- Global instructions: "Use 4 spaces, PEP 8, type hints"
- Repo instructions: "Use Google-style docstrings, 100 char lines"
- Path instructions: "Backend code: Use async/await, validate inputs"

Copilot will apply:
1. Global instructions (base)
2. + Repo instructions (override style)
3. + Path instructions (override backend specifics)

**Result:** All three apply, with more specific ones taking precedence.

## Editing Instructions

Your instructions are just Markdown files. Edit anytime:

```bash
# Edit with your favorite editor
nano ~/.copilot/agents/default/instructions.md
# or
vim ~/.copilot/agents/default/instructions.md
# or
open ~/.copilot/agents/default/instructions.md  # macOS
```

Changes apply immediately to new Copilot CLI sessions.

## Verification

### Check Agent Exists

```bash
# List installed agents
ls -la ~/.copilot/agents/
```

Expected output:
```
total XX
drwxr-xr-x  3 user  staff   96 Dec 17 06:18 .
drwxr-xr-x  5 user  staff  160 Dec 17 06:15 ..
drwxr-xr-x  3 user  staff   96 Dec 17 06:18 default
```

### Test Agent

```bash
# Ask Copilot to describe its instructions
copilot --agent default --prompt "What instructions are you following?"
```

Expected: Copilot summarizes your global instructions.

### Check File Permissions

```bash
# Verify files are readable
ls -la ~/.copilot/agents/default/

# If permission denied, fix:
chmod 644 ~/.copilot/agents/default/instructions.md
chmod 755 ~/.copilot/agents/default
```

## Troubleshooting

### Issue: Agent not found

```bash
error: agent 'default' not found
```

**Solution:**
1. Verify directory exists: `ls -la ~/.copilot/agents/default/`
2. Verify config file: `cat ~/.copilot/agents/default/agent.yaml`
3. Check permissions: `ls -la ~/.copilot/agents/default/instructions.md`

### Issue: Instructions not being applied

**Check:**
1. Are you using `--agent default` flag?
2. Did you set `COPILOT_AGENT_DEFAULT=default` in shell?
3. Is a repo-specific `.github/copilot-instructions.md` overriding?

**Solution:**
```bash
# Explicitly use agent
copilot --agent default --prompt "test"

# If works: add to shell config
export COPILOT_AGENT_DEFAULT=default
```

### Issue: Changes not taking effect

**Solution:**
1. Save the file
2. Close Copilot CLI
3. Open a new terminal session
4. Try again

```bash
# Or restart terminal without closing
source ~/.bashrc  # Linux/WSL
# or
source ~/.zshrc   # macOS
```

## Integration with MCP

Global agent instructions work alongside MCP configuration:

```
~/.copilot/
├─ agents/
│  └─ default/
│     ├─ agent.yaml
│     └─ instructions.md       <- Your coding guidelines
└─ mcp-config.json         <- MCP server configuration
```

They work independently:
- **MCP config:** Configures available tools
- **Global agent:** Provides coding guidelines on how to use those tools

## Best Practices

1. **Keep it focused** - Don't make instructions too long (aim for <500 lines)
2. **Be specific** - Generic guidelines are less useful
3. **Update regularly** - As your preferences evolve
4. **Include examples** - Show "do this" not just "don't do that"
5. **Test with repos** - Ensure repo-specific instructions can still override
6. **Document changes** - Add comments when you update

## Next Steps

1. **Setup:** Run `bash scripts/setup-global-copilot-agent.sh`
2. **Customize:** Edit `~/.copilot/agents/default/instructions.md`
3. **Test:** Try `copilot --agent default --prompt "test"`
4. **Automate:** Add `export COPILOT_AGENT_DEFAULT=default` to shell config
5. **Iterate:** Refine instructions based on results

## References

- [Copilot CLI Documentation](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
- [Creating Custom Agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Repository Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)

---

**Last Updated:** 2024-12-17

**Questions or Issues?** Check the troubleshooting section or refer to the main README.md in this directory.
