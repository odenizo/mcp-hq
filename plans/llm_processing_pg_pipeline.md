# Plan: LLM Processing Workflows + PostgreSQL Backbone

## Goal
Design workflows that include LLM-processing steps (prompt pipelines, summarization, catalog extraction) backed by PostgreSQL for persistence/analytics.

## Scope
- Define schemas/tables for MCP artifacts, tool catalogs, runs, and telemetry.
- Map ingestion sources: ContextStream captures, MCP server exports, repo scans.
- Identify LLM-processing stages (normalize, summarize, classify, diff).
- Orchestration options: GitHub Actions, cron, or MCP-driven jobs.

## Tasks (plan only)
1) Draft minimal DB schema (tables: servers, tools, prompts, resources, runs, artifacts, telemetry). 
2) Map dataflows from mcp-hq artifacts into the schema; identify required ETL steps.
3) Choose orchestration mechanism and triggers (on new export, on repo change, scheduled).
4) Define LLM-processing steps per artifact type (summaries, diffs, quality checks).
5) Security/secret-handling plan (DB creds, API keys) for Hetzner + local.
6) Outline validation and reporting (dashboards/queries).

## Outputs
- Schema proposal (ERD + SQL draft).
- Dataflow diagram.
- Runbook for a pilot pipeline (no execution yet).
