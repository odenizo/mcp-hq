# MCP Server Catalog

Comprehensive, machine-readable catalog of Model Context Protocol (MCP) servers and their tools.

## Overview

This catalog documents:
- **MCP Servers**: Official and community-maintained MCP server implementations
- **Tools**: Complete tool inventories with schemas, examples, and best practices
- **Integration Patterns**: How to use each server in AI-powered workflows
- **Deniz-Specific Guidance**: Tagged recommendations for productivity and infrastructure workflows

## Files

### Core Files

- **`mcp_servers.yaml`**: Master registry of all documented servers and tools (machine-readable)
- **`mcp_servers.json`**: Alternative JSON format for programmatic access
- **`inbox.yaml`**: Queue of servers pending documentation (P0/P1/P2 priority)
- **`validation_schema.json`**: JSON Schema enforcing catalog structure
- **`coverage_stats.md`**: Auto-generated coverage report by category

### Scripts

- **`validate-catalog.py`**: Validate YAML against schema and report errors
- **`generate-coverage.py`**: Generate coverage reports and statistics

## Quick Start

### For Agents: Adding a New Server

1. **Read the server's documentation** (README, examples, tool definitions)
2. **Extract all tools** and their complete schemas
3. **Create YAML entry** in `mcp_servers.yaml` (use template in design doc)
4. **Create markdown doc** in `../docs/mcp-servers/[server-id].md`
5. **Validate**: Run `python validate-catalog.py`
6. **Commit** when validation passes

### For Users: Finding a Server

1. **By category**: Check `mcp_servers.yaml` section `servers[].category`
2. **By Deniz use case**: Look for `tags` containing `deniz-*`
3. **By function**: Search `tools[].summary` for keywords
4. **Human-readable**: Browse `../docs/mcp-servers/*.md` files

## Schema Structure

Each server entry includes:

```yaml
servers:
  - id: example-server
    name: "Example MCP Server"
    category: devtools
    description: "What this server does"
    repo_url: "https://github.com/..."
    maturity: production | stable | experimental
    auth_model: none | api_key | oauth | cloud_account | local_only
    tools:
      - id: tool_name
        summary: "What this tool does (1-2 sentences)"
        input_schema: {...}
        output_semantics: "Response structure description"
        risks: read_only | mutating | high_impact
    deniz_recommended: true | false
    deniz_use_cases: ["Use case 1", "Use case 2"]
    tool_coverage: "12/12" # documented tools
```

## Coverage Tracking

Coverage metrics by category:

| Category | Target | Current |
|----------|--------|----------|
| devtools | 80%+ | — |
| infra | 80%+ | — |
| data | 70%+ | — |
| productivity | 70%+ | — |
| security | 60%+ | — |
| observability | 60%+ | — |

## Validation

Before committing:

```bash
# Install dependencies
pip install pyyaml jsonschema

# Validate catalog
python validate-catalog.py

# Generate coverage report
python generate-coverage.py
```

## Quarterly Expansion

Every 3 months:

1. **Week 1 (5h)**: Discover & triage 5-10 new servers → update `inbox.yaml`
2. **Week 2-3 (15h)**: Document 3-5 selected servers
3. **Week 4 (2h)**: Review, report, plan next cycle

## Resources

- **MCP Documentation**: https://modelcontextprotocol.io
- **Official Servers**: https://github.com/modelcontextprotocol/servers
- **Awesome MCP Servers**: https://github.com/wong2/awesome-mcp-servers
- **System Design**: See `../docs/` for complete documentation

## Contributing

To add a new server:

1. Check `inbox.yaml` - may already be in queue
2. Follow "Adding a New Server" workflow above
3. Update `inbox.yaml` status when complete
4. Submit PR with YAML + markdown + validation passing

## Maintenance

- **Last Updated**: See git history
- **Total Servers**: Count in `mcp_servers.yaml`
- **Total Tools**: Sum across all servers
- **Validation Status**: See `coverage_stats.md`

---

**Status**: Active catalog, quarterly expansions, Deniz-driven priorities
