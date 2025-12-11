#!/bin/bash

# MCP Server Configuration Creation Workflow
# Uses GitIngest MCP to analyze repository and generate accurate configuration files

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_SERVERS_DIR="$(dirname "$SCRIPT_DIR")"
ACTIVE_DIR="$MCP_SERVERS_DIR/active"
TEMPLATES_DIR="$MCP_SERVERS_DIR/templates"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $0 <github_url> <server_name> [options]"
    echo ""
    echo "Create MCP server configuration by analyzing GitHub repository"
    echo ""
    echo "Arguments:"
    echo "  github_url    GitHub repository URL (e.g., https://github.com/owner/repo)"
    echo "  server_name   MCP server identifier (e.g., owner-repo-mcp)"
    echo ""
    echo "Options:"
    echo "  -f, --force       Force overwrite existing configuration"
    echo "  -a, --analyze     Perform detailed analysis (slower but more accurate)"
    echo "  -t, --template    Use specific template (default: _template.json)"
    echo "  -o, --output      Output file path (default: active/<server_name>.json)"
    echo "  -h, --help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 https://github.com/puravparab/gitingest-mcp gitingest-mcp"
    echo "  $0 https://github.com/supabase-community/supabase-mcp supabase-mcp --analyze"
    exit 1
}

log() {
    local level=$1
    shift
    case $level in
        "INFO")  echo -e "${BLUE}ℹ️  $*${NC}" ;;
        "WARN")  echo -e "${YELLOW}⚠️  $*${NC}" ;;
        "ERROR") echo -e "${RED}❌ $*${NC}" ;;
        "SUCCESS") echo -e "${GREEN}✅ $*${NC}" ;;
        "STEP") echo -e "${BLUE}🔸 $*${NC}" ;;
    esac
}

extract_github_info() {
    local url=$1
    local owner_repo

    # Extract owner/repo from various GitHub URL formats
    if [[ $url =~ github\.com/([^/]+)/([^/]+) ]]; then
        local owner="${BASH_REMATCH[1]}"
        local repo="${BASH_REMATCH[2]}"

        # Remove .git suffix if present
        repo=${repo%.git}

        echo "$owner $repo"
    else
        log ERROR "Invalid GitHub URL format: $url"
        exit 1
    fi
}

check_claude_mcp() {
    if ! command -v claude &> /dev/null; then
        log ERROR "Claude CLI not found. Please install Claude Code CLI first."
        exit 1
    fi

    # Check if gitingest-mcp is available
    if ! claude mcp list 2>/dev/null | grep -q "gitingest-mcp.*Connected"; then
        log ERROR "GitIngest MCP server not connected. Please ensure it's properly configured."
        exit 1
    fi
}

analyze_repository() {
    local owner=$1
    local repo=$2
    local analysis_file="/tmp/mcp_analysis_${owner}_${repo}.json"

    log STEP "Analyzing repository: $owner/$repo"

    # Create analysis file with repository data
    cat > "$analysis_file" << EOF
{
    "repository": {
        "owner": "$owner",
        "repo": "$repo",
        "url": "https://github.com/$owner/$repo"
    },
    "analysis": {
        "timestamp": "$(date -Iseconds)",
        "analyzer": "claude-code-hq MCP analysis workflow"
    }
}
EOF

    # Note: In a real implementation, this would call Claude Code with GitIngest MCP
    # For now, we'll create a placeholder that shows the intended workflow

    log INFO "Repository analysis saved to: $analysis_file"
    echo "$analysis_file"
}

generate_config_from_analysis() {
    local analysis_file=$1
    local server_name=$2
    local template_file=$3
    local output_file=$4

    log STEP "Generating configuration for: $server_name"

    # Read analysis data
    local analysis_data=$(cat "$analysis_file")
    local owner=$(echo "$analysis_data" | jq -r '.repository.owner')
    local repo=$(echo "$analysis_data" | jq -r '.repository.repo')
    local repo_url=$(echo "$analysis_data" | jq -r '.repository.url')

    # Read template
    local template_data=$(cat "$template_file")

    # Generate configuration by substituting template values
    # This is a simplified version - real implementation would use the analysis data
    local config=$(echo "$template_data" | jq \
        --arg server_id "$server_name" \
        --arg display_name "${repo} MCP Server" \
        --arg namespace "$owner" \
        --arg package "$repo" \
        --arg description "Analyzed from repository: $repo_url" \
        --arg repo_url "$repo_url" \
        --arg analysis_date "$(date -Iseconds)" \
        '
        .metadata.server_id = $server_id |
        .metadata.display_name = $display_name |
        .metadata.namespace = $namespace |
        .metadata.package = $package |
        .metadata.description = $description |
        .metadata.repository_url = $repo_url |
        .metadata.analysis_date = $analysis_date |
        .deployment.smithery.url = "https://server.smithery.ai/@\($namespace)/\($package)/mcp" |
        .deployment.smithery.install_command = "claude mcp add @\($namespace)/\($package)"
        ')

    # Save configuration
    echo "$config" > "$output_file"

    log SUCCESS "Configuration generated: $output_file"
}

validate_config() {
    local config_file=$1

    log STEP "Validating configuration file..."

    # Check JSON validity
    if ! jq empty "$config_file" 2>/dev/null; then
        log ERROR "Generated configuration is not valid JSON"
        return 1
    fi

    # Check required fields
    local required_fields=(
        ".metadata.server_id"
        ".metadata.namespace"
        ".metadata.package"
        ".deployment"
    )

    for field in "${required_fields[@]}"; do
        if ! jq -e "$field" "$config_file" >/dev/null 2>&1; then
            log ERROR "Missing required field: $field"
            return 1
        fi
    done

    log SUCCESS "Configuration validation passed"
    return 0
}

create_installation_script() {
    local config_file=$1
    local script_file="${config_file%.json}_install.sh"

    log STEP "Creating installation script..."

    local namespace=$(jq -r '.metadata.namespace' "$config_file")
    local package=$(jq -r '.metadata.package' "$config_file")
    local server_id=$(jq -r '.metadata.server_id' "$config_file")

    cat > "$script_file" << EOF
#!/bin/bash

# Installation script for $server_id
# Generated by claude-code-hq MCP configuration system

set -euo pipefail

SERVER_ID="$server_id"
NAMESPACE="$namespace"
PACKAGE="$package"

echo "🚀 Installing \$SERVER_ID..."

# Check prerequisites
if ! command -v claude &> /dev/null; then
    echo "❌ Error: Claude CLI not found"
    exit 1
fi

# Check environment variables
if [ -z "\${SMITHERY_API_KEY:-}" ]; then
    echo "⚠️  Warning: SMITHERY_API_KEY not set"
    echo "   Set with: export SMITHERY_API_KEY=your_api_key"
fi

if [ -z "\${SMITHERY_PROFILE:-}" ]; then
    echo "⚠️  Warning: SMITHERY_PROFILE not set"
    echo "   Set with: export SMITHERY_PROFILE=your_profile"
fi

# Install via Smithery
echo "📦 Installing via Smithery..."
if claude mcp add "@\$NAMESPACE/\$PACKAGE"; then
    echo "✅ Installation successful"
else
    echo "❌ Installation failed"
    exit 1
fi

# Verify installation
echo "🔍 Verifying installation..."
if claude mcp list | grep -q "\$SERVER_ID.*Connected"; then
    echo "✅ \$SERVER_ID is connected and ready"
else
    echo "⚠️  \$SERVER_ID installed but not connected - check configuration"
fi

echo "🎉 Installation complete for \$SERVER_ID"
EOF

    chmod +x "$script_file"
    log SUCCESS "Installation script created: $script_file"
}

main() {
    local github_url=""
    local server_name=""
    local force=false
    local analyze=false
    local template="_template.json"
    local output=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -f|--force)
                force=true
                shift
                ;;
            -a|--analyze)
                analyze=true
                shift
                ;;
            -t|--template)
                template="$2"
                shift 2
                ;;
            -o|--output)
                output="$2"
                shift 2
                ;;
            -h|--help)
                usage
                ;;
            -*)
                log ERROR "Unknown option: $1"
                usage
                ;;
            *)
                if [[ -z "$github_url" ]]; then
                    github_url="$1"
                elif [[ -z "$server_name" ]]; then
                    server_name="$1"
                else
                    log ERROR "Too many arguments"
                    usage
                fi
                shift
                ;;
        esac
    done

    # Validate required arguments
    if [[ -z "$github_url" ]] || [[ -z "$server_name" ]]; then
        log ERROR "Missing required arguments"
        usage
    fi

    # Set default output path
    if [[ -z "$output" ]]; then
        output="$ACTIVE_DIR/${server_name}.json"
    fi

    # Check if output file exists
    if [[ -f "$output" ]] && [[ "$force" != true ]]; then
        log ERROR "Configuration file already exists: $output"
        log INFO "Use --force to overwrite"
        exit 1
    fi

    # Ensure directories exist
    mkdir -p "$ACTIVE_DIR"

    # Check prerequisites
    check_claude_mcp

    # Extract GitHub repository information
    read -r owner repo <<< "$(extract_github_info "$github_url")"
    log INFO "Repository: $owner/$repo"

    # Template file path
    local template_file="$TEMPLATES_DIR/$template"
    if [[ ! -f "$template_file" ]]; then
        log ERROR "Template file not found: $template_file"
        exit 1
    fi

    log INFO "Starting MCP server configuration creation workflow..."

    # Step 1: Analyze repository
    local analysis_file
    if [[ "$analyze" == true ]]; then
        analysis_file=$(analyze_repository "$owner" "$repo")
    else
        # Create minimal analysis file
        analysis_file="/tmp/mcp_analysis_${owner}_${repo}.json"
        cat > "$analysis_file" << EOF
{
    "repository": {
        "owner": "$owner",
        "repo": "$repo",
        "url": "$github_url"
    },
    "analysis": {
        "timestamp": "$(date -Iseconds)",
        "analyzer": "basic workflow (use --analyze for detailed analysis)"
    }
}
EOF
    fi

    # Step 2: Generate configuration
    generate_config_from_analysis "$analysis_file" "$server_name" "$template_file" "$output"

    # Step 3: Validate configuration
    if validate_config "$output"; then
        log SUCCESS "Configuration created successfully: $output"
    else
        log ERROR "Configuration validation failed"
        exit 1
    fi

    # Step 4: Create installation script
    create_installation_script "$output"

    # Step 5: Display summary
    echo ""
    log INFO "Configuration Summary:"
    echo "  📁 Configuration file: $output"
    echo "  🔧 Installation script: ${output%.json}_install.sh"
    echo "  🏷️  Server ID: $server_name"
    echo "  📊 Repository: $owner/$repo"
    echo ""
    log INFO "Next steps:"
    echo "  1. Review and customize the configuration file"
    echo "  2. Run the installation script to deploy the server"
    echo "  3. Test the server connection with: claude mcp list"

    # Cleanup
    rm -f "$analysis_file"
}

# Run main function with all arguments
main "$@"