# How to Add a New MCP Server to the Catalog

Step-by-step guide for documenting a new MCP server in the mcp-hq catalog system.

## Quick Checklist

- [ ] Read server README and extract tool definitions
- [ ] Check if server exists in `catalog/inbox.yaml`; move status to `in-progress`
- [ ] Create YAML entry in `catalog/mcp_servers.yaml` with all required fields
- [ ] Create markdown doc in `docs/mcp-servers/[server-id].md`
- [ ] Run validation: `python catalog/validate-catalog.py`
- [ ] Review coverage report: `python catalog/generate-coverage.py`
- [ ] Submit PR with YAML, markdown, validation passing

## Detailed Workflow

### Phase 1: Research

1. **Find server documentation**
   - Check official GitHub repository
   - Read README, examples, and tool definitions
   - Look for TypeScript/Python source if needed

2. **Extract tool inventory**
   - List all tools/functions exposed by server
   - Note input parameters (types, required, defaults)
   - Document output structure
   - Identify any risk levels (read-only, mutating, etc.)
   - Record rate limits if applicable

3. **Understand authentication**
   - What credentials are needed?
   - Environment variables or config files?
   - Setup complexity?

4. **Update inbox status**
   ```yaml
   # In catalog/inbox.yaml, change status from "inbox" to "in-progress"
   - id: example-server
     status: in-progress      # was "inbox"
   ```

### Phase 2: Create YAML Entry

1. **Open `catalog/mcp_servers.yaml`**

2. **Add server entry to `servers:` array**
   ```yaml
   - id: example-server
     name: "Example MCP Server"
     category: devtools                    # Choose from: devtools, data, infra, productivity, security, observability
     subcategories: [version-control]     # Optional secondary categories
     
     description: |
       What this server does, in 2-3 sentences.
       Focus on core functionality and use cases.
     
     repo_url: "https://github.com/example/example-mcp"
     homepage: "https://example.com"
     
     maturity: production | stable | experimental
     created_date: "2026-01-03"
     
     deployment:
       local: true
       docker: false
       cloud_function: false
       kubernetes: false
     
     host_compat:
       claude_desktop: true
       claude_web: false
       vscode_cline: true
       cursor: true
     
     auth_model: none | api_key | oauth | cloud_account | local_only
     requires_credentials:
       - type: api_key
         env_var: EXAMPLE_API_KEY
     
     tools:
       - id: tool_name_1
         name: "Tool Display Name"
         category: inspection                    # or: mutation, query, etc.
         summary: "1-2 sentence description of what this tool does and when to use it."
         
         input_schema:
           type: object
           required: [param1]
           properties:
             param1:
               type: string
               description: "What is this parameter?"
             param2:
               type: integer
               default: 10
         
         output_semantics: "Describes output structure, e.g., 'Array of objects with id, name, created_at'"
         risks: read_only          # or: mutating, high_impact, destructive
         rate_limit: "100 calls/minute"
         
         best_practices_for_llms:
           patterns:
             - "Use when you need to [action]"
             - "Combine with [other_tool] for [result]"
           warnings:
             - "Always filter by X first"
             - "Never pass raw user PII"
         
         example_usage:
           - "Show me the [output type] for [common use case]"
           - "[Action verb] the [object] using [relevant parameters]"
       
       # ... repeat for each tool ...
     
     deniz_recommended: true | false
     deniz_use_cases:
       - "[Specific workflow Deniz would use this for]"
       - "[Another use case]"
     
     deniz_setup:
       - "Prerequisites or special instructions for Deniz"
     
     tool_coverage: "N/M"          # e.g., "12/12" (documented/total tools)
     doc_link: "docs/mcp-servers/example-server.md"
     doc_status: draft | incomplete | complete | archived
     
     tags:
       - foundational
       - devtools
       - read-only
       - deniz-daily                # or: deniz-weekly, deniz-infra, etc.
     
     maintainer: "Anthropic | Community | [Name]"
     pairs_well_with:
       - other-server-id
       - another-server-id
     
     notes: "Any additional caveats, limitations, or important details."
   ```

3. **Validate structure**
   - Required fields filled
   - All tools documented
   - Proper indentation (YAML 2-space)

### Phase 3: Create Markdown Documentation

1. **Create file: `docs/mcp-servers/[server-id].md`**

2. **Use this template:**
   ```markdown
   # Example Server
   
   Official description of what this MCP server does.
   
   **Status**: Production | Stable | Experimental
   **Maintainer**: Anthropic | Community
   **Auth**: API Key | None | OAuth
   **Repository**: [Link to GitHub]
   
   ## Overview
   
   Longer explanation of:
   - What it does
   - When you'd use it
   - Key features
   - Typical workflows
   
   ## Tools Reference
   
   ### tool_name_1
   
   **Purpose**: What this tool does
   **Risk**: Read-only | Mutating | Destructive
   
   **Parameters**:
   - `param1` (string, required): Description
   - `param2` (integer, optional, default: 10): Description
   
   **Output**: Returns an array of objects with fields: id, name, created_at
   
   **Example Prompts**:
   - "[Common usage pattern]"
   - "[Another typical request]"
   
   ### [... repeat for each tool ...]
   
   ## Typical Workflows
   
   ### Workflow A: [Name]
   
   When you want to [goal]:
   
   1. Call `tool_1` with [parameters]
   2. Use results to call `tool_2`
   3. [Final step]
   
   Example:
   ```
   "[Show me X for Y]"
   ```
   
   ### Workflow B: [Name]
   
   [Similar format]
   
   ## Setup Instructions
   
   ### Prerequisites
   
   - What needs to be installed
   - What credentials are needed
   - Configuration steps
   
   ### Environment Variables
   
   ```bash
   export EXAMPLE_API_KEY="your-api-key-here"
   ```
   
   ### Local Configuration
   
   If needed, explain special setup for local deployment.
   
   ## Best Practices
   
   ✅ Do:
   - Always filter by X before using tool Y
   - Combine with other server for full context
   - Check rate limits before bulk operations
   
   ❌ Don't:
   - Pass raw user data without validation
   - Use in loops without pagination
   - Assume empty results mean not found
   
   ## Anti-Patterns
   
   Common mistakes to avoid:
   - "Passing PII directly to the tool"
   - "Not handling rate limit errors"
   
   ## Deniz Guidance
   
   This server is [recommended/not recommended] for Deniz's workflows.
   
   ### Recommended For:
   - [Daily use case]
   - [Weekly pattern]
   
   ### Pairs Well With:
   - `git-official`: Get file history context
   - `github-official`: Find related issues
   
   ### Common Deniz Patterns:
   - "[Typical request Deniz might make]"
   
   ## Troubleshooting
   
   **Q: Tool returns empty results**  
   A: Make sure to [check X], [validate Y]
   
   **Q: Rate limit errors**  
   A: [Rate limit explanation], retry with [backoff strategy]
   
   ## Additional Resources
   
   - [Official Documentation](link)
   - [API Reference](link)
   - [GitHub Issues](link)
   ```

### Phase 4: Validation

1. **Run validation script**
   ```bash
   cd catalog
   python validate-catalog.py
   ```
   Expected output: `✅ Validation PASSED`

2. **Generate coverage report**
   ```bash
   python generate-coverage.py
   ```
   Review output for any warnings

3. **Check markdown syntax**
   ```bash
   # Install if needed: pip install markdownlint-cli
   markdownlint docs/mcp-servers/*.md
   ```

### Phase 5: Update Inbox

1. **Mark server as complete**
   ```yaml
   # In catalog/inbox.yaml
   - id: example-server
     status: documented       # was "in-progress"
     documented_date: "2026-01-03"
   ```

### Phase 6: Submit PR

1. **Commit changes**
   ```bash
   git add catalog/mcp_servers.yaml docs/mcp-servers/example-server.md
   git commit -m "Add example-server to MCP catalog (N tools)"
   ```

2. **PR description should include**
   - Server name and category
   - Number of tools documented
   - Validation passing status
   - Notable features or caveats
   - Any special setup requirements

## YAML Entry Template

Copy and customize this template:

```yaml
  - id: template-server
    name: "Template Server Name"
    category: devtools
    description: "What this server does."
    repo_url: "https://github.com/owner/repo"
    maturity: production
    auth_model: api_key
    deployment:
      local: true
      docker: false
    host_compat:
      claude_desktop: true
      cursor: true
    tools:
      - id: example_tool
        name: "Example Tool"
        summary: "Short description of what this tool does."
        input_schema:
          type: object
          required: []
          properties: {}
        output_semantics: "Description of output"
        risks: read_only
        example_usage:
          - "Example prompt"
    tool_coverage: "1/1"
    doc_link: "docs/mcp-servers/template-server.md"
    doc_status: complete
    tags: [devtools]
    maintainer: "Community"
    notes: "Any special notes."
```

## Markdown Template

See example template in Phase 3 above.

## Common Issues

**Validation fails: "Missing tool_coverage field"**
- Add `tool_coverage: "N/M"` to YAML entry (e.g., `"5/5"` if all 5 tools documented)

**Validation fails: "Invalid category"**
- Use one of: devtools, data, infra, productivity, security, observability

**Markdown won't render on GitHub**
- Check for unescaped special characters
- Verify links are absolute URLs or relative paths
- Ensure proper heading hierarchy (# → ## → ###)

**Tool coverage > total tools**
- Check: documented number should not exceed actual tool count
- If you haven't documented all tools yet, use `"5/8"` format

## Questions?

Refer to:
- `catalog/README.md` for system overview
- `docs/mcp-servers/*.md` for real examples
- `catalog/validation_schema.json` for field definitions
