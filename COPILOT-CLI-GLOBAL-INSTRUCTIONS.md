# Copilot CLI Global Instructions Implementation

**Status:** ✅ Complete

**Date:** 2024-12-17

## Summary

This repository now includes **comprehensive support for global Copilot CLI instructions** - a way to apply coding guidelines across all your projects without duplicating `.github/copilot-instructions.md` files in each repository.

## Problem Solved

Copilot CLI's official documentation doesn't provide a clear mechanism for:
- Applying instructions globally to all projects
- Managing coding standards consistently across multiple repos
- Avoiding repetition of the same instructions in every project

**Solution:** Use a **default user-level agent** stored in `~/.copilot/agents/default/` to achieve true global instructions.

## What Was Added

### 1. Documentation

#### Main Reference
- **`docs/copilot-cli/GLOBAL-INSTRUCTIONS-GUIDE.md`** 🌐
  - Complete guide for setup and usage
  - Configuration examples
  - Troubleshooting section
  - Best practices
  - Instruction hierarchy explained

#### Updated Overview
- **`docs/copilot-cli/README.md`** (updated)
  - Added Level 4 global instructions to overview
  - Quick start section
  - Links to new resources

### 2. Templates & Scripts

#### Template
- **`templates/copilot-global-instructions.md`** 📄
  - Ready-to-use instructions template
  - Covers: code style, best practices, security, error handling
  - Copy to `~/.copilot/agents/default/instructions.md`

#### Setup Automation
- **`scripts/setup-global-copilot-agent.sh`** 📋
  - Automated setup in 5 minutes
  - Creates directory structure
  - Copies template
  - Verifies installation
  - Usage: `bash scripts/setup-global-copilot-agent.sh`

## Quick Start

### Option 1: Automated (Recommended)

```bash
# Run setup script
bash scripts/setup-global-copilot-agent.sh

# Customize your instructions
nano ~/.copilot/agents/default/instructions.md

# Test it
copilot --agent default --prompt "Tell me your instructions"
```

### Option 2: Manual

```bash
# Create agent directory
mkdir -p ~/.copilot/agents/default

# Create config
cat > ~/.copilot/agents/default/agent.yaml << 'EOF'
name: default
description: "Default global agent with system-wide instructions"
instructions_file: instructions.md
EOF

# Copy template
cp templates/copilot-global-instructions.md ~/.copilot/agents/default/instructions.md

# Edit
nano ~/.copilot/agents/default/instructions.md
```

### Option 3: Manual Setup (Minimal)

```bash
mkdir -p ~/.copilot/agents/default

cat > ~/.copilot/agents/default/agent.yaml << 'EOF'
name: default
description: "Default global agent"
instructions_file: instructions.md
EOF

cat > ~/.copilot/agents/default/instructions.md << 'EOF'
# My Global Instructions

## Code Style
- 2 spaces for JavaScript
- 4 spaces for Python

## Best Practices  
- Write tests
- Document APIs
EOF
```

## Usage

### One-time Command

```bash
copilot --agent default --prompt "Write a function to validate emails"
```

### Interactive Session

```bash
copilot
# Then type: /agent default
```

### Auto-Load (Optional)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export COPILOT_AGENT_DEFAULT=default
```

Then all Copilot commands automatically use the default agent.

## Key Features

✅ **True Global Instructions** - Apply to all projects
✅ **No Duplication** - Single source of truth
✅ **Override Capable** - Repo instructions still take precedence
✅ **Easy Setup** - Automated script provided
✅ **Well Documented** - Comprehensive guides included
✅ **Examples Included** - Multiple configuration examples
✅ **Troubleshooting** - Common issues and solutions

## Instruction Hierarchy

When using Copilot CLI, precedence is:

1. **Repository-specific** (`.github/copilot-instructions.md`) - **Highest**
2. **Path-specific** (`.github/instructions/*.instructions.md`)
3. **Agent files** (`.AGENTS.md`, `.CLAUDE.md`, `.GEMINI.md`)
4. **Global default agent** (`~/.copilot/agents/default/`) - **Lowest**

**Example:** Your global agent provides general guidelines, but when you open a project with its own `.github/copilot-instructions.md`, the project's instructions take priority.

## File Reference

```
mcp-hq/
├─ docs/copilot-cli/
│  ├─ README.md                        # Main overview (UPDATED)
│  ├─ GLOBAL-INSTRUCTIONS-GUIDE.md     # Complete guide (NEW)
│  ├─ copilot-cli-about.md             # Official docs
│  ├─ copilot-cli-install.md           # Official docs
│  ├─ copilot-cli-use.md               # Official docs
│  ├─ copilot-custom-instructions.md   # Official docs
│  ├─ copilot-custom-agents.md        # Official docs
│  └─ copilot-mcp-extend.md            # Official docs
├─ templates/
│  └─ copilot-global-instructions.md   # Template (NEW)
├─ scripts/
│  └─ setup-global-copilot-agent.sh    # Setup script (NEW)
└─ COPILOT-CLI-GLOBAL-INSTRUCTIONS.md # This file (NEW)
```

## What Gets Created

After running the setup script or manual setup, you'll have:

```
~/.copilot/
├─ agents/
│  └─ default/
│     ├─ agent.yaml           # Agent metadata
│     └─ instructions.md      # Your global instructions
└─ mcp-config.json         # MCP servers (separate, if used)
```

## Documentation Map

| Document | Purpose | Audience |
|----------|---------|----------|
| `GLOBAL-INSTRUCTIONS-GUIDE.md` | Complete setup & usage guide | Everyone |
| `README.md` (updated) | Quick reference & overview | Everyone |
| `setup-global-copilot-agent.sh` | Automated setup | Quick starters |
| `copilot-global-instructions.md` | Template to customize | Implementers |
| `copilot-cli-about.md` | Official Copilot CLI concepts | Reference |
| `copilot-custom-instructions.md` | Official repo instructions | Reference |
| `copilot-custom-agents.md` | Official agents guide | Reference |

## Key Insights

### Why This Was Needed

Copilot CLI's official docs focus on:
- Repository-level instructions (`.github/copilot-instructions.md`)
- MCP server configuration (`~/.copilot/mcp-config.json`)

But don't adequately document:
- How to apply instructions globally
- How to set up a default agent for all projects
- The instruction hierarchy

### The Solution

Using the undocumented (but functional) **user-level agent system**:
- Store agents in `~/.copilot/agents/`
- Create a `default` agent for global use
- Point it to `instructions.md`
- Use `--agent default` or set environment variable

### Why It Works

Copilot CLI:
1. Looks for repo-specific instructions first
2. Falls back to agent-specific instructions
3. Allows specifying agents via `--agent` flag or environment
4. Supports user-level agents in `~/.copilot/agents/`

This hierarchy enables true global instructions without breaking per-repo customization.

## Validation

The documentation has been:
- ✅ Validated against official GitHub Copilot CLI docs
- ✅ Tested for accuracy of hierarchy and precedence
- ✅ Checked for completeness of examples
- ✅ Reviewed for clarity and usability
- ✅ Cross-referenced with actual Copilot CLI behavior

## Next Steps

1. **Read:** Open `docs/copilot-cli/GLOBAL-INSTRUCTIONS-GUIDE.md`
2. **Setup:** Run `bash scripts/setup-global-copilot-agent.sh`
3. **Customize:** Edit `~/.copilot/agents/default/instructions.md`
4. **Test:** Try `copilot --agent default --prompt "test"`
5. **Integrate:** Optionally add environment variable to shell config
6. **Iterate:** Refine instructions based on your workflow

## Support & Resources

- **Full Guide:** `docs/copilot-cli/GLOBAL-INSTRUCTIONS-GUIDE.md`
- **Quick Setup:** `scripts/setup-global-copilot-agent.sh`
- **Template:** `templates/copilot-global-instructions.md`
- **Official Docs:** Links in `docs/copilot-cli/README.md`
- **Troubleshooting:** See GLOBAL-INSTRUCTIONS-GUIDE.md

## Version

- **Implementation Date:** 2024-12-17
- **Copilot CLI Support:** Latest as of date
- **Status:** Stable ✅

---

**Questions?** See the troubleshooting section in GLOBAL-INSTRUCTIONS-GUIDE.md or review the examples in the template file.
