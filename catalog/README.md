# MCP Server Catalog System

**Machine-readable registry of Model Context Protocol (MCP) servers and tools**

Status: **Phase 1 Ready** (12 servers, 100+ tools)  
Last Updated: January 3, 2026

## Overview

This system maintains a living catalog of MCP servers, their exposed tools, authentication requirements, and use cases. It includes:

- **Master Registry** (`mcp_servers.yaml`) - Single source of truth for all servers
- **Server Inbox** (`inbox.yaml`) - Priority queue for documentation (P0/P1/P2)
- **JSON Schema** (`validation_schema.json`) - Machine-readable schema definition
- **Validation Script** (`validate-catalog.py`) - Automated YAML validation
- **Coverage Reporter** (`generate-coverage.py`) - Statistics and metrics

## Quick Start

### Add a New Server

1. Read the guide: [`../docs/guides/adding-new-servers.md`](../docs/guides/adding-new-servers.md)
2. Move server from `inbox.yaml` to `mcp_servers.yaml`
3. Document all tools in YAML
4. Create markdown file in `../docs/mcp-servers/`
5. Validate: `python validate-catalog.py`
6. Check coverage: `python generate-coverage.py`
7. Submit PR

### Validate Catalog

```bash
# Install dependencies (one-time)
pip install pyyaml jsonschema

# Run validation
python validate-catalog.py

# Generate coverage report
python generate-coverage.py
```

Expected output:
```
✅ Validation PASSED
   Catalog contains 12 server(s), 0 warning(s)
```

## File Reference

| File | Purpose | Format |
|------|---------|--------|
| `mcp_servers.yaml` | Master registry of documented servers | YAML |
| `inbox.yaml` | Queue of servers pending documentation | YAML |
| `validation_schema.json` | Field definitions and constraints | JSON Schema |
| `validate-catalog.py` | Validates YAML against schema | Python 3 |
| `generate-coverage.py` | Generates statistics and reports | Python 3 |

## Structure

### Server Entry

Each server in `mcp_servers.yaml` includes:

```yaml
- id: unique-slug
  name: Display Name
  category: devtools  # or: data, infra, productivity, security, observability
  description: What this server does
  repo_url: https://github.com/...
  maturity: production  # or: stable, experimental
  auth_model: api_key  # or: none, oauth, cloud_account, local_only
  
  tools:
    - id: tool_name
      name: Tool Display Name
      summary: What this tool does
      input_schema: { ... }  # JSON Schema
      output_semantics: Response structure
      risks: read_only  # or: mutating, high_impact, destructive
  
  deniz_recommended: true  # For Deniz-specific workflows
  deniz_use_cases: ["Use case 1", "Use case 2"]
  tool_coverage: "12/12"  # documented/total
  doc_link: docs/mcp-servers/example-server.md
  doc_status: complete  # or: draft, incomplete, archived
```

### Inbox Entry

Each server in `inbox.yaml` includes:

```yaml
- id: example-server
  name: Example Server
  url: https://github.com/owner/repo
  category: devtools
  priority: P0  # P0 (immediate), P1 (high value), P2 (background)
  reason: Why this server matters
  deniz_value: critical  # or: high, medium, low
  status: inbox  # or: in-progress, documented
  notes: Any research or setup notes
```

## Categories

- **devtools**: Development tools (git, github, code analysis)
- **data**: Data management (analytics, databases, ETL)
- **infra**: Infrastructure (cloud, VMs, containers)
- **productivity**: Productivity tools (CRM, task management, communication)
- **security**: Security tools (pentest, scanning, monitoring)
- **observability**: Monitoring and observability (logs, metrics, traces)

## Authentication Models

- **none**: No authentication required
- **api_key**: API key authentication
- **oauth**: OAuth flow authentication
- **cloud_account**: Cloud provider account (AWS, Azure, GCP)
- **local_only**: Local-only, no external auth needed

## Maturity Levels

- **experimental**: Early stage, not production ready
- **stable**: Well-tested, recommended for production
- **production**: Official, actively maintained, stable API

## Validation Rules

The JSON Schema enforces:

1. **Required fields**: All servers must have id, name, category, description, repo_url, maturity, auth_model, tools
2. **Field types**: Strings, integers, booleans, arrays correctly typed
3. **Enums**: Categories, maturity levels, auth models from defined set
4. **Patterns**: Server IDs must be slug format (lowercase, hyphens)
5. **Tool coverage**: Documented tools <= total tools
6. **References**: Servers in `pairs_well_with` must exist in catalog
7. **Deniz tags**: Recommended servers should have deniz_use_cases

## Phase 1 Timeline

**Week 1** (Jan 6-10): git, github, linear (3 servers, 25 tools)  
**Week 2** (Jan 13-17): Integration servers (7 servers, 50+ tools)  
**Week 3** (Jan 20-24): Infrastructure servers (2 servers, 20+ tools)  

**Checkpoint**: Friday 5 PM each week

## Coverage Metrics

After documentation, check coverage:

```bash
python generate-coverage.py
```

Reports:
- Total servers and tools
- Coverage by category
- Maturity distribution
- Auth model breakdown
- Deniz-recommended servers
- Documentation status

## Common Tasks

### Add a Server

```bash
# 1. Move from inbox.yaml status to in-progress
# 2. Create YAML entry in mcp_servers.yaml
# 3. Create markdown doc in ../docs/mcp-servers/
# 4. Validate and commit
cd catalog
python validate-catalog.py
git add mcp_servers.yaml ../docs/mcp-servers/[id].md
git commit -m "Add [name] server documentation"
```

### Update Existing Server

```bash
# 1. Modify YAML entry
# 2. Update markdown doc if needed
# 3. Validate
python validate-catalog.py
git add mcp_servers.yaml ../docs/mcp-servers/[id].md
git commit -m "Update [name] server documentation"
```

### Check Coverage

```bash
python generate-coverage.py
cat coverage_stats.md
```

### Verify All Servers

```bash
python validate-catalog.py
```

## Troubleshooting

**Validation fails: Missing required field**
- Check schema for required fields: id, name, category, description, repo_url, maturity, auth_model, tools
- All tools must have: id, name, summary, input_schema, output_semantics

**Validation fails: Invalid category**
- Use one of: devtools, data, infra, productivity, security, observability

**Validation fails: tool_coverage exceeds total tools**
- Documented count cannot be > total count
- Example: "5/8" means 5 documented, 8 total (OK); "9/8" means error

**Markdown doesn't render on GitHub**
- Check for unclosed code blocks
- Verify link syntax: [text](url) not [text (url)]
- Ensure heading hierarchy: # → ## → ###

## Dependencies

```bash
# Required for validation
pip install pyyaml jsonschema

# Optional
pip install markdownlint-cli  # Markdown linting
```

## Resources

- **MCP Documentation**: https://modelcontextprotocol.io
- **Official Servers**: https://github.com/modelcontextprotocol/servers
- **JSON Schema**: https://json-schema.org
- **Implementation Guide**: `../docs/guides/adding-new-servers.md`

## Contributing

1. Start by reading `../docs/guides/adding-new-servers.md`
2. Choose a server from `inbox.yaml` (P0 priority first)
3. Update its status to `in-progress`
4. Create YAML entry in `mcp_servers.yaml`
5. Create markdown doc in `../docs/mcp-servers/`
6. Run validation: `python validate-catalog.py`
7. Submit PR

For detailed instructions, see the guide linked above.

## Roadmap

**2026**:
- **Q1** (Jan-Mar): Phase 1 complete (12 servers), quarterly pattern established
- **Q2** (Apr-Jun): 22+ servers, 200+ tools
- **Q3** (Jul-Sep): 32+ servers, 300+ tools
- **Q4** (Oct-Dec): 50+ servers, 400+ tools

---

**Contact**: See repository maintainers  
**Last Updated**: January 3, 2026  
**Status**: Phase 1 Infrastructure Complete
