#!/bin/bash

# Setup Global Copilot CLI Default Agent
# ======================================
# This script creates a default user-level agent with global instructions
# for GitHub Copilot CLI that applies across all projects.

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
AGENT_DIR="${HOME}/.copilot/agents/default"
AGENT_CONFIG="${AGENT_DIR}/agent.yaml"
AGENT_INSTRUCTIONS="${AGENT_DIR}/instructions.md"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Copilot CLI Global Agent Setup${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Step 1: Create directories
echo -e "${YELLOW}[1/4]${NC} Creating agent directories..."
mkdir -p "${AGENT_DIR}"
echo -e "${GREEN}✓${NC} Created: ${AGENT_DIR}\n"

# Step 2: Create agent configuration
echo -e "${YELLOW}[2/4]${NC} Creating agent configuration..."
cat > "${AGENT_CONFIG}" << 'EOF'
name: default
description: "Default global agent with system-wide instructions"
instructions_file: instructions.md
EOF
echo -e "${GREEN}✓${NC} Created: ${AGENT_CONFIG}\n"

# Step 3: Copy or create instructions file
echo -e "${YELLOW}[3/4]${NC} Setting up global instructions..."

if [[ -f "templates/copilot-global-instructions.md" ]]; then
    echo "  Copying template from ./templates/copilot-global-instructions.md"
    cp templates/copilot-global-instructions.md "${AGENT_INSTRUCTIONS}"
    echo -e "${GREEN}✓${NC} Copied template to: ${AGENT_INSTRUCTIONS}\n"
else
    echo "  Template not found locally, creating default instructions..."
    cat > "${AGENT_INSTRUCTIONS}" << 'EOF'
# Global Copilot CLI Instructions

**Usage:** This file applies globally to all projects via the default agent.

## General Guidelines

- Follow project-specific instructions when available (they override this)
- Write clear, maintainable code
- Add meaningful comments for complex logic
- Use descriptive names for variables and functions

## Code Style

- **JavaScript/YAML:** 2 spaces
- **Python:** 4 spaces
- **Line length:** ~100 characters
- Use meaningful variable names

## Best Practices

- Write tests for new functions
- Document public APIs
- Keep functions focused and single-purpose
- Use efficient algorithms

## Security

- Never commit secrets
- Use environment variables for sensitive data
- Validate all user input
- Keep dependencies updated

## Error Handling

- Be explicit about error types
- Provide actionable error messages
- Log errors appropriately
- Don't expose stack traces in production

---

Edit this file to customize your global instructions!
EOF
    echo -e "${GREEN}✓${NC} Created default instructions at: ${AGENT_INSTRUCTIONS}\n"
fi

# Step 4: Verify setup
echo -e "${YELLOW}[4/4]${NC} Verifying setup..."

if [[ -f "${AGENT_CONFIG}" ]] && [[ -f "${AGENT_INSTRUCTIONS}" ]]; then
    echo -e "${GREEN}✓${NC} Agent configuration exists"
    echo -e "${GREEN}✓${NC} Instructions file exists"
    echo -e "${GREEN}✓${NC} Setup completed successfully!\n"
else
    echo -e "${RED}✗${NC} Setup verification failed!\n"
    exit 1
fi

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Global Agent Setup Complete!${NC}"
echo -e "${BLUE}========================================${NC}\n"

echo "Location: ${AGENT_DIR}"
echo "  - Config: ${AGENT_CONFIG}"
echo "  - Instructions: ${AGENT_INSTRUCTIONS}\n"

echo -e "${YELLOW}Next steps:${NC}\n"
echo "1. Review and customize global instructions:"
echo -e "   ${BLUE}nano ${AGENT_INSTRUCTIONS}${NC}\n"

echo "2. Test the default agent:"
echo -e "   ${BLUE}copilot --agent default --prompt \"Tell me your instructions\"${NC}\n"

echo "3. (Optional) Set as default by adding to shell config (~/.bashrc, ~/.zshrc):"
echo -e "   ${BLUE}export COPILOT_AGENT_DEFAULT=default${NC}\n"

echo "4. (Optional) For interactive mode, use:"
echo -e "   ${BLUE}copilot${NC}"
echo -e "   Then type: ${BLUE}/agent default${NC}\n"

echo -e "${GREEN}Your global Copilot CLI instructions are now active!${NC}\n"
