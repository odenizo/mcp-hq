# GEMINI CLI (mcp-hq)

Use Gemini CLI in headless mode for repo analysis and schema extraction. Prefer:

```bash
gemini --prompt "<task>"
```

Helpful patterns (from skills-portfolio/skills/gemini-cli-integration):
- Single file context: `gemini "Context: $(cat file)" "<task>"`
- Multi-file context: concatenate files with labels, then pass to gemini.
- Git context: include repo name, branch, recent commits, diff.

When prompting for MCP server analysis, include:
1) Use Desktop Commander multi-file read to load docs/specs.
2) Identify tools/resources/prompts registrations and schemas.
3) Emit v4 server object + instruction recommendations.

Example prompt:
```
Review code-mode repo + contextstream server object v4 and schema.\nUse Desktop Commander multi-file read to load relevant docs before starting.\nGenerate MCP server object v4 for code-mode with tools/resources/prompts and instructions.\n```
