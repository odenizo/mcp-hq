#!/usr/bin/env bash
set -euo pipefail

# Refresh an MCP server catalog object from a remote GitHub repo URL.
# Usage: refresh-contextstream-catalog.sh <repo_url> [branch]
# Example: refresh-contextstream-catalog.sh https://github.com/contextstream/mcp-server main
# Output: downloads zip under _sources/, writes a minimal v4 server object skeleton under catalog/servers/<slug>/
# NOTE: This script currently writes a skeleton server object (metadata only). Hook in an extractor to populate tools/resources/prompts.

REPO_URL=${1:-"https://github.com/contextstream/mcp-server"}
BRANCH=${2:-"main"}

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="${ROOT}/_sources"
mkdir -p "${SRC_DIR}"

# Derive slug
REPO_SLUG=$(basename -s .git "${REPO_URL}")
OWNER=$(basename "$(dirname "${REPO_URL}")")
SLUG="${OWNER}-${REPO_SLUG}"
ZIP_URL="${REPO_URL}/archive/refs/heads/${BRANCH}.zip"
DEST_ZIP="${SRC_DIR}/${SLUG}-${BRANCH}.zip"
META_DIR="${ROOT}/catalog/servers/${REPO_SLUG}"
mkdir -p "${META_DIR}"

echo "Downloading ${ZIP_URL} ..."
curl -L "${ZIP_URL}" -o "${DEST_ZIP}"
SHA=$(sha256sum "${DEST_ZIP}" | awk '{print $1}')
TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

cat > "${META_DIR}/last_fetch.json" <<EOF
{
  "repo_url": "${REPO_URL}",
  "branch": "${BRANCH}",
  "downloaded_at": "${TS}",
  "zip_path": "${DEST_ZIP}",
  "sha256": "${SHA}"
}
EOF

# Minimal v4 skeleton (replace with extractor-generated object)
SERVER_ID="srv-${REPO_SLUG}"
OUT_OBJ="${META_DIR}/${REPO_SLUG}_mcp_server_object.v4.json"
cat > "${OUT_OBJ}" <<EOF
{
  "schema_version": "4.0.0",
  "server_id": "${SERVER_ID}",
  "name": "${REPO_SLUG}",
  "description": "Skeleton server object (populate via extractor)",
  "category": "unknown",
  "subcategory": "unknown",
  "tags": [],
  "locality": "unknown",
  "source": {
    "github_repo": "${OWNER}/${REPO_SLUG}",
    "homepage": null,
    "license": null,
    "package": {"name": null, "version": null, "private": null}
  },
  "extraction": {
    "extracted_at": "${TS}",
    "extractor": "refresh-contextstream-catalog.sh",
    "method": {"strategy": "manual", "entrypoints_scanned": [], "patterns_used": [], "notes": "skeleton only"},
    "input_artifact": {"type": "zip", "ref": "${DEST_ZIP}"},
    "repo_snapshot": {"commit_sha": null, "tag": null, "branch": "${BRANCH}"},
    "confidence": {"tools": 0, "resources": 0, "prompts": 0},
    "warnings": ["No extractor hooked; object is metadata-only"]
  },
  "key_paths": [],
  "runtime": {"language": "unknown", "entrypoints": [], "mcp_transports_supported": ["unknown"], "required_env": [], "optional_env": [], "required_secrets": []},
  "deployment": {"supported_modes": ["unknown"], "docker": {"supported": false, "files": [], "image": null}, "smithery": {"compatible": false, "files": [], "notes": null}, "healthcheck": null},
  "configuration": {"options": [], "schema": null, "examples": []},
  "toolsets": null,
  "context_injection": {"global_instructions": [], "per_tool_instructions": [], "dynamic_context_sources": [], "tokenizer": null, "totals": null},
  "inventory": {"tools": {}, "resources": {}, "prompts": {}},
  "ids": null,
  "content_hashes": {"repo_tree_hash": null, "tools_schema_hash": null, "resources_schema_hash": null, "prompts_schema_hash": null},
  "tools_schema": {"tools": []},
  "resources_schema": {"resources": []},
  "prompts_schema": {"prompts": []},
  "ops": null,
  "references": null
}
EOF

echo "Saved skeleton server object to ${OUT_OBJ}"
echo "NOTE: Hook an extractor to populate tools/resources/prompts."
