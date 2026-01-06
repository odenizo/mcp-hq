# MCP-HQ Repository Tree - Complete Overview

**Branch:** main
**Last Commit:** 40c1dd1 - Add Perplexity research prompt for MCP server ecosystem analysis
**Total Files:** 63 files
**Total Lines:** 44,019 lines of code/config/documentation

---

## 📂 Complete File Tree

```
mcp-hq/
│
├── 📄 Root Configuration Files
│   ├── .code-workspace.code-workspace          # VS Code workspace configuration
│   ├── .gitignore                              # Git ignore patterns
│   ├── .mcp.json                               # MCP server configuration
│   ├── config-default-paths.json               # Default path configurations
│   ├── knowledge-map.json                      # Knowledge graph/map (2,391 lines)
│   └── user-inputs.md                          # User input tracking
│
├── 📚 Documentation (Root Level)
│   ├── CONTEXTSTREAM-INSTALLATION-GUIDE.md     # ContextStream setup guide
│   ├── COPILOT-CLI-GLOBAL-INSTRUCTIONS.md      # GitHub Copilot CLI instructions
│   ├── GEMINI.md                               # Gemini integration docs
│   ├── PERPLEXITY_RESEARCH_PROMPT.md           # Perplexity research instructions (FULL) ⭐ NEW
│   └── PERPLEXITY_QUICK_PROMPT.txt             # Perplexity quick-copy prompt ⭐ NEW
│
├── 📦 active/                                   # Active MCP server configurations (12 files)
│   ├── chrome-devtools-mcp.json                # Chrome DevTools MCP config
│   ├── context7-mcp.json                       # Context7 MCP config
│   ├── contextstream-mcp.json                  # ContextStream MCP config
│   ├── docker-mcp.json                         # Docker MCP config
│   ├── e2b-mcp.json                            # E2B MCP config
│   ├── exa-mcp.json                            # Exa MCP config
│   ├── github-mcp.json                         # GitHub MCP config
│   ├── gitingest-mcp.json                      # GitIngest MCP config
│   ├── memento-mcp.json                        # Memento MCP config
│   ├── repomix-mcp.json                        # Repomix MCP config
│   ├── supabase-mcp.json                       # Supabase MCP config (392 lines)
│   ├── tavily-mcp.json                         # Tavily MCP config
│   └── tmux-mcp.json                           # Tmux MCP config
│
├── 🤖 agents/                                   # Agent definitions
│   └── mcp-agent.md                            # MCP agent specification
│
├── 📋 catalog/                                  # MCP SERVER CATALOG SYSTEM
│   ├── README.md                               # Catalog system overview & instructions
│   ├── inbox.yaml                              # 15 servers pending documentation (P0/P1/P2)
│   ├── index.json                              # Server index (1 server)
│   ├── mcp_servers.yaml                        # Master registry (0 servers - empty)
│   ├── validation_schema.json                  # JSON Schema for catalog validation
│   ├── generate-coverage.py                    # Coverage statistics generator
│   ├── validate-catalog.py                     # YAML validation script
│   │
│   └── servers/                                # Individual server documentation
│       └── contextstream/                      # ✅ ContextStream MCP Server (ONLY DOCUMENTED)
│           ├── README.md                       # Server overview (19 lines)
│           ├── contextstream_mcp_server_object.v3.json       # Full schema v3 (13,713 lines)
│           ├── contextstream_mcp_server_object.v3.lite.json  # Lite schema v3 (1,855 lines)
│           └── contextstream_mcp_server_object.v4.json       # Schema v4 (13,506 lines)
│
├── 📖 docs/                                     # Documentation
│   ├── copilot-cli/                            # GitHub Copilot CLI documentation
│   │   ├── README.md                           # Copilot CLI overview
│   │   ├── GLOBAL-INSTRUCTIONS-GUIDE.md        # Global instructions guide (402 lines)
│   │   ├── copilot-cli-about.md               # About Copilot CLI
│   │   ├── copilot-cli-install.md             # Installation guide
│   │   ├── copilot-cli-use.md                 # Usage instructions
│   │   ├── copilot-custom-agents.md           # Custom agent configuration
│   │   ├── copilot-custom-instructions.md     # Custom instruction setup (676 lines)
│   │   └── copilot-mcp-extend.md              # MCP extension guide (340 lines)
│   │
│   └── guides/                                 # Guides
│       └── adding-new-servers.md               # Guide: How to add new MCP servers (384 lines)
│
├── 🔧 nu/                                       # Nushell scripts
│   ├── analyze_mcp_repository.py               # Analyze MCP repositories (506 lines)
│   ├── analyze_mcp_server_repo.py              # Analyze specific MCP server repos (474 lines)
│   └── create_mcp_config.sh                    # Create MCP configurations (393 lines)
│
├── ⚙️  ops/                                      # Operations & configuration
│   ├── registry/
│   │   └── ops_registry.json                   # Operations registry
│   └── topology/
│       └── topology.json                       # System topology
│
├── 📝 plans/                                    # Planning documents
│   ├── llm_processing_pg_pipeline.md           # LLM processing pipeline plan
│   └── remote_mcp_hosting_research.md          # Remote MCP hosting research
│
├── 🔨 scripts/                                  # Automation scripts
│   ├── refresh-contextstream-catalog.sh        # Refresh ContextStream catalog
│   └── setup-global-copilot-agent.sh           # Setup global Copilot agent
│
├── 📐 spec/                                     # Specifications
│   └── schemas/                                # JSON schemas
│       ├── mcp_server_object.schema.v3.json    # MCP server schema v3 (1,278 lines)
│       └── mcp_server_object.schema.v4.json    # MCP server schema v4 (1,715 lines)
│
└── 📄 templates/                                # Templates
    ├── AGENTS.md.template                      # Agent template
    ├── _template.json                          # Generic JSON template (344 lines)
    ├── copilot-global-instructions.md          # Copilot instructions template
    ├── github-copilot-instructions.md.template # GitHub Copilot template
    │
    └── contextstream-instructions/             # ContextStream instruction templates
        ├── README.md                           # ContextStream templates overview
        ├── CLAUDE-CODE-INSTRUCTIONS.md         # Claude Code integration
        ├── CODEX-CLI-GEMINI-INSTRUCTIONS.md    # Codex CLI/Gemini integration
        ├── COPILOT-CLI-INSTRUCTIONS.md         # Copilot CLI integration
        └── install-all.sh                      # Install all templates script
```

---

## 📊 Repository Statistics

### File Distribution
- **Total Files:** 63
- **Total Lines:** 44,019

### Directory Breakdown
| Directory | Files | Purpose |
|-----------|-------|---------|
| `active/` | 12 | Active MCP server configurations |
| `agents/` | 1 | Agent definitions |
| `catalog/` | 12 | MCP catalog system (8 + 4 in contextstream/) |
| `docs/` | 9 | Documentation (8 in copilot-cli/ + 1 guide) |
| `nu/` | 3 | Nushell automation scripts |
| `ops/` | 2 | Operations registry & topology |
| `plans/` | 2 | Planning documents |
| `scripts/` | 2 | Automation scripts |
| `spec/schemas/` | 2 | JSON schemas |
| `templates/` | 9 | Templates (5 + 4 in contextstream-instructions/) |
| Root | 11 | Configuration & documentation |

### Top 10 Largest Files
1. `catalog/servers/contextstream/contextstream_mcp_server_object.v3.json` - 13,713 lines
2. `catalog/servers/contextstream/contextstream_mcp_server_object.v4.json` - 13,506 lines
3. `knowledge-map.json` - 2,391 lines
4. `catalog/servers/contextstream/contextstream_mcp_server_object.v3.lite.json` - 1,855 lines
5. `spec/schemas/mcp_server_object.schema.v4.json` - 1,715 lines
6. `spec/schemas/mcp_server_object.schema.v3.json` - 1,278 lines
7. `docs/copilot-cli/copilot-custom-instructions.md` - 676 lines
8. `nu/analyze_mcp_repository.py` - 506 lines
9. `nu/analyze_mcp_server_repo.py` - 474 lines
10. `docs/copilot-cli/GLOBAL-INSTRUCTIONS-GUIDE.md` - 402 lines

---

## 🎯 MCP Catalog System Status

### Documented Servers: 1
- ✅ **ContextStream MCP Server** (`srv-contextstream-mcp`)
  - Category: developer-tools (context-and-memory)
  - Transport: stdio (remote API)
  - Package: `@contextstream/mcp-server` v0.3.39
  - Install: `npx -y @contextstream/mcp-server`
  - Auth: `CONTEXTSTREAM_API_KEY` or `CONTEXTSTREAM_JWT`

### Active MCP Configurations: 12
1. chrome-devtools-mcp
2. context7-mcp
3. contextstream-mcp ✅
4. docker-mcp
5. e2b-mcp
6. exa-mcp
7. github-mcp
8. gitingest-mcp
9. memento-mcp
10. repomix-mcp
11. supabase-mcp
12. tavily-mcp
13. tmux-mcp

### Inbox Queue: 15 servers (awaiting documentation)

**P0 - Critical (Week 1):**
- `github-official` - GitHub MCP (Official Anthropic)
- `git-official` - Git MCP (Official Anthropic)
- `linear-mcp` - Linear project management

**P1 - High Value (Weeks 2-3):**
- `hetzner-cloud` - Hetzner VM management [RESEARCH REQUIRED]
- `dune-analytics` - Blockchain analytics
- `slack` - Team communication [FIND URL]
- `notion` - Knowledge base [FIND URL]
- `figma` - Design integration [FIND URL]
- `datadog` - Monitoring [FIND URL]
- `kubernetes` - Container orchestration [RESEARCH]
- `docker` - Docker MCP catalog

**P2 - Background (Backlog):**
- `terraform` - Infrastructure as Code [FIND URL]
- `openrouter` - OpenRouter API integration
- `obsidian` - Obsidian PKM [FIND URL]

---

## 🔧 Automation & Tooling

### Catalog Management
- **Validation:** `catalog/validate-catalog.py` - Validates YAML against JSON Schema
- **Coverage:** `catalog/generate-coverage.py` - Generates statistics and reports
- **Schema:** `catalog/validation_schema.json` - Field definitions and constraints

### MCP Analysis
- **Repository Analysis:** `nu/analyze_mcp_repository.py` (506 lines)
- **Server Analysis:** `nu/analyze_mcp_server_repo.py` (474 lines)
- **Config Generator:** `nu/create_mcp_config.sh` (393 lines)

### Automation Scripts
- **Catalog Refresh:** `scripts/refresh-contextstream-catalog.sh`
- **Agent Setup:** `scripts/setup-global-copilot-agent.sh`

---

## 📐 Schemas & Specifications

### MCP Server Object Schemas
- **v3 Schema:** `spec/schemas/mcp_server_object.schema.v3.json` (1,278 lines)
- **v4 Schema:** `spec/schemas/mcp_server_object.schema.v4.json` (1,715 lines)

### Catalog Validation
- **Schema:** `catalog/validation_schema.json`
- **Enforces:** Required fields, types, enums, patterns, coverage validation

---

## 📚 Documentation

### Catalog System
- **Overview:** `catalog/README.md` - System architecture, quick start, validation
- **Guide:** `docs/guides/adding-new-servers.md` (384 lines) - How to add new servers

### GitHub Copilot CLI
- **Overview:** `docs/copilot-cli/README.md`
- **Global Instructions:** `docs/copilot-cli/GLOBAL-INSTRUCTIONS-GUIDE.md` (402 lines)
- **Custom Instructions:** `docs/copilot-cli/copilot-custom-instructions.md` (676 lines)
- **MCP Extension:** `docs/copilot-cli/copilot-mcp-extend.md` (340 lines)
- **About/Install/Use:** Various guides for Copilot CLI

### Integration Guides
- **ContextStream:** `CONTEXTSTREAM-INSTALLATION-GUIDE.md`
- **Copilot CLI:** `COPILOT-CLI-GLOBAL-INSTRUCTIONS.md`
- **Gemini:** `GEMINI.md`

### Research & Planning
- **Perplexity Prompt:** `PERPLEXITY_RESEARCH_PROMPT.md` ⭐ NEW
- **Quick Prompt:** `PERPLEXITY_QUICK_PROMPT.txt` ⭐ NEW
- **Remote MCP Hosting:** `plans/remote_mcp_hosting_research.md`
- **LLM Pipeline:** `plans/llm_processing_pg_pipeline.md`

---

## 🎯 Next Actions

1. ✅ **Use Perplexity prompts** to validate 15 inbox servers
2. ⏳ **Research & discover** 20+ additional MCP servers
3. ⏳ **Identify HTTP/SSE servers** for cloud deployment
4. ⏳ **Populate** `catalog/mcp_servers.yaml` with validated servers
5. ⏳ **Create** comprehensive ecosystem analysis report

---

## 🔗 Key Resources

- **MCP Documentation:** https://modelcontextprotocol.io
- **Official Servers:** https://github.com/modelcontextprotocol/servers
- **JSON Schema:** https://json-schema.org
- **Claude Code Docs:** https://code.claude.com/docs

---

**Last Updated:** 2026-01-06
**Status:** Phase 1 Infrastructure Complete - Ready for ecosystem expansion
