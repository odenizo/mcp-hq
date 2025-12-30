# Plan: Remote MCP Hosting & Connector Strategy

## Goal
Evaluate and select MCP ecosystem tools that can host MCP servers remotely (1Panel or similar), expose HTTP/SSE transports with OAuth, and integrate with ChatGPT/Claude web connectors to reduce local dependency.

## Scope
- Hosting options: 1Panel, other MCP platform/aggregators, HTTP-proxy bridges.
- Transports: stdio→HTTP bridges, SSE, OAuth flows.
- Connectors: ChatGPT MCP, Claude MCP, VSCode clients.
- Deployment targets: Hetzner VM, cloud (serverless/container), hybrid.

## Tasks (research first; do not execute yet)
1) Inventory candidate projects/repositories (MCP hosting/aggregators/proxies) and summarize capabilities.
2) Compare deployment models (container, serverless, platform-managed) and transport support.
3) Assess OAuth/identity patterns for HTTP-accessible MCP servers.
4) Define selection criteria (cost, auth, observability, latency, compatibility with ChatGPT/Claude connectors).
5) Propose target stack for pilot (Hetzner + chosen host + minimal set of MCP servers).
6) Outline rollout steps and ops/monitoring hooks.

## Outputs
- Shortlist matrix + recommendation.
- Proposed architecture diagram (HTTP/SSE/OAuth flows).
- Pilot deployment checklist (no deployment yet).
