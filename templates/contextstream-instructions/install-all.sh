#!/bin/bash

# ContextStream MCP Installation Script
# Installs and configures ContextStream for all AI coding tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if API key provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: CONTEXTSTREAM_API_KEY required${NC}"
    echo "Usage: $0 YOUR_API_KEY_HERE"
    echo ""
    echo "Get your API key from https://contextstream.io"
    exit 1
fi

API_KEY="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_HQ_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

echo -e "${BLUE}=== ContextStream MCP Installation ===${NC}"
echo ""
echo "API Key: ${API_KEY:0:10}..."
echo "MCP HQ Directory: $MCP_HQ_DIR"
echo ""

# Function to backup file
backup_file() {
    local file="$1"
    if [ -f "$file" ]; then
        cp "$file" "${file}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}Backed up: $file${NC}"
    fi
}

# Function to append instructions if not already present
append_instructions() {
    local target_file="$1"
    local source_file="$2"
    local marker="## ContextStream Integration"
    
    # Create parent directory if it doesn't exist
    mkdir -p "$(dirname "$target_file")"
    
    # Create file if it doesn't exist
    touch "$target_file"
    
    # Check if already installed
    if grep -q "$marker" "$target_file" 2>/dev/null; then
        echo -e "${YELLOW}ContextStream instructions already present in $target_file${NC}"
        return 0
    fi
    
    # Backup and append
    backup_file "$target_file"
    echo "" >> "$target_file"
    echo "# ================================================" >> "$target_file"
    echo "# ContextStream Integration (Auto-installed)" >> "$target_file"
    echo "# ================================================" >> "$target_file"
    cat "$source_file" >> "$target_file"
    echo -e "${GREEN}✓ Added ContextStream instructions to $target_file${NC}"
}

# Function to add MCP server to JSON config
add_mcp_server_json() {
    local config_file="$1"
    local server_name="contextstream"
    local server_type="$2"  # "stdio" or "local"
    
    # Create parent directory
    mkdir -p "$(dirname "$config_file")"
    
    # Create config if it doesn't exist
    if [ ! -f "$config_file" ]; then
        if [ "$server_type" = "stdio" ]; then
            echo '{"mcpServers":{}}' > "$config_file"
        else
            echo '{"mcpServers":{}}' > "$config_file"
        fi
    fi
    
    # Check if server already exists
    if grep -q "\"$server_name\"" "$config_file" 2>/dev/null; then
        echo -e "${YELLOW}ContextStream server already configured in $config_file${NC}"
        return 0
    fi
    
    backup_file "$config_file"
    
    # Use jq to add server (or Python/Node if jq not available)
    if command -v jq &> /dev/null; then
        if [ "$server_type" = "stdio" ]; then
            jq --arg api_key "$API_KEY" \
               '.mcpServers.contextstream = {
                 "type": "stdio",
                 "command": "npx",
                 "args": ["-y", "@contextstream/mcp-server"],
                 "env": {
                   "CONTEXTSTREAM_API_URL": "https://api.contextstream.io",
                   "CONTEXTSTREAM_API_KEY": $api_key
                 }
               }' "$config_file" > "${config_file}.tmp" && mv "${config_file}.tmp" "$config_file"
        else
            jq --arg api_key "$API_KEY" \
               '.mcpServers.contextstream = {
                 "type": "local",
                 "command": "npx",
                 "args": ["-y", "@contextstream/mcp-server"],
                 "env": {
                   "CONTEXTSTREAM_API_URL": "https://api.contextstream.io",
                   "CONTEXTSTREAM_API_KEY": $api_key
                 },
                 "tools": ["*"]
               }' "$config_file" > "${config_file}.tmp" && mv "${config_file}.tmp" "$config_file"
        fi
        echo -e "${GREEN}✓ Added ContextStream server to $config_file${NC}"
    else
        echo -e "${YELLOW}jq not found - please manually add ContextStream to $config_file${NC}"
        echo "See: $MCP_HQ_DIR/active/contextstream-mcp.json for configuration"
    fi
}

# Function to add MCP server to TOML config
add_mcp_server_toml() {
    local config_file="$1"
    
    # Create parent directory
    mkdir -p "$(dirname "$config_file")"
    
    # Check if already exists
    if grep -q "\[mcp_servers.contextstream\]" "$config_file" 2>/dev/null; then
        echo -e "${YELLOW}ContextStream server already configured in $config_file${NC}"
        return 0
    fi
    
    backup_file "$config_file"
    
    # Append TOML configuration
    cat >> "$config_file" << EOF

[mcp_servers.contextstream]
command = "npx"
args = ["-y", "@contextstream/mcp-server"]
startup_timeout_sec = 120

[mcp_servers.contextstream.env]
CONTEXTSTREAM_API_URL = "https://api.contextstream.io"
CONTEXTSTREAM_API_KEY = "$API_KEY"
EOF
    
    echo -e "${GREEN}✓ Added ContextStream server to $config_file${NC}"
}

echo -e "${BLUE}Installing for Claude Code...${NC}"
append_instructions \
    "$HOME/.claude/CLAUDE.md" \
    "$SCRIPT_DIR/CLAUDE-CODE-INSTRUCTIONS.md"

# Note: Claude Code uses ~/.claude.json which may need manual editing
# as it has a complex structure
echo -e "${YELLOW}Note: Please manually add ContextStream to ~/.claude.json${NC}"
echo "See: $MCP_HQ_DIR/active/contextstream-mcp.json for the configuration"
echo ""

echo -e "${BLUE}Installing for Codex CLI...${NC}"
append_instructions \
    "$HOME/.codex/AGENTS.md" \
    "$SCRIPT_DIR/CODEX-CLI-GEMINI-INSTRUCTIONS.md"
add_mcp_server_toml "$HOME/.codex/config.toml"
echo ""

echo -e "${BLUE}Installing for Gemini CLI...${NC}"
append_instructions \
    "$HOME/.gemini/GEMINI.md" \
    "$SCRIPT_DIR/CODEX-CLI-GEMINI-INSTRUCTIONS.md"
add_mcp_server_json "$HOME/.gemini/settings.json" "stdio"
echo ""

echo -e "${BLUE}Installing for GitHub Copilot CLI...${NC}"
# Note: Copilot CLI uses server-prefixed tool names (contextstream-session_init)
# Instructions are in COPILOT-CLI-INSTRUCTIONS.md but not auto-added
echo -e "${YELLOW}Note: Copilot CLI uses contextstream-<tool_name> format${NC}"
add_mcp_server_json "$HOME/.copilot/mcp-config.json" "local"
echo ""

echo -e "${BLUE}Installing for Antigravity...${NC}"
echo -e "${YELLOW}Antigravity MCP configuration structure needs verification${NC}"
echo -e "${YELLOW}Please check Antigravity documentation for MCP support${NC}"
echo ""

echo -e "${GREEN}=== Installation Complete ===${NC}"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "1. ${YELLOW}Restart all AI tools${NC} for changes to take effect"
echo "2. ${YELLOW}Verify installation${NC} by calling session_init in each tool"
echo "3. ${YELLOW}Check tool-specific configs:${NC}"
echo "   - Claude Code: ~/.claude.json (manual edit may be needed)"
echo "   - Codex CLI: ~/.codex/config.toml"
echo "   - Gemini CLI: ~/.gemini/settings.json"
echo "   - Copilot CLI: ~/.copilot/mcp-config.json"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "- Instructions: $SCRIPT_DIR/README.md"
echo "- Configuration: $MCP_HQ_DIR/active/contextstream-mcp.json"
echo "- Website: https://contextstream.io/docs/mcp"
echo ""
