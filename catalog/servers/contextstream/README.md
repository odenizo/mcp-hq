# ContextStream MCP Server

Artifacts:
- `contextstream_mcp_server_object.v3.json` – full catalog (tools/resources/prompts) exported from repo (schema v3).
- `contextstream_mcp_server_object.v3.lite.json` – slim variant.
- `contextstream_mcp_server_object.v4.json` – converted to MCP-HQ schema v4 (server_id `srv-contextstream-mcp`).

Install/run:
- `npx -y @contextstream/mcp-server`
- Env (required): `CONTEXTSTREAM_API_KEY` (or `CONTEXTSTREAM_JWT`)
- Env (optional): `CONTEXTSTREAM_WORKSPACE_ID`, `CONTEXTSTREAM_PROJECT_ID`, `CONTEXTSTREAM_TOOLSET=full`, `CONTEXTSTREAM_TOOL_ALLOWLIST`, `CONTEXTSTREAM_UPGRADE_URL`

Schema references:
- `../../spec/schemas/mcp_server_object.schema.v3.json`
- `../../spec/schemas/mcp_server_object.schema.v4.json`

Notes:
- Transport: stdio; calls remote ContextStream API.
- Auto-context enabled; PRO gating for ai_* tools unless overridden.
