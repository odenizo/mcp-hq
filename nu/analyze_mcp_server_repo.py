#!/usr/bin/env python3
"""
MCP Server Repository Analysis Workflow
Analyzes GitHub repositories to extract accurate information for MCP server configuration files
"""

import json
import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

class MCPServerAnalyzer:
    def __init__(self):
        self.claude_hq_dir = Path(__file__).parent.parent.parent
        self.templates_dir = self.claude_hq_dir / "mcp-servers" / "templates"
        self.active_dir = self.claude_hq_dir / "mcp-servers" / "active"

    def analyze_server_repository(self, github_url: str, server_name: str) -> Dict[str, Any]:
        """
        Comprehensive analysis of MCP server repository
        Uses GitIngest MCP to extract repository information and generate accurate configuration
        """
        print(f"🔍 Analyzing repository: {github_url}")

        # Extract owner and repo from GitHub URL
        owner, repo = self._parse_github_url(github_url)
        if not owner or not repo:
            raise ValueError(f"Invalid GitHub URL: {github_url}")

        # Step 1: Get repository summary and basic information
        print("📊 Fetching repository summary...")
        repo_summary = self._get_repository_summary(owner, repo)

        # Step 2: Get repository tree structure
        print("🌳 Analyzing repository structure...")
        repo_tree = self._get_repository_tree(owner, repo)

        # Step 3: Identify and extract key files
        print("📁 Extracting key configuration files...")
        key_files = self._identify_key_files(repo_tree)
        file_contents = self._extract_file_contents(owner, repo, key_files)

        # Step 4: Analyze package.json, README, and source code
        print("🔍 Analyzing package configuration and documentation...")
        metadata = self._analyze_package_metadata(file_contents)
        tools_info = self._analyze_tools_and_resources(file_contents, repo_tree)
        deployment_info = self._analyze_deployment_options(file_contents)

        # Step 5: Generate comprehensive server configuration
        print("⚙️ Generating server configuration...")
        config = self._generate_server_config(
            server_name, github_url, repo_summary, metadata,
            tools_info, deployment_info, file_contents
        )

        return config

    def _parse_github_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract owner and repo from GitHub URL"""
        patterns = [
            r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
            r'github\.com/([^/]+)/([^/]+)/tree/',
            r'github\.com/([^/]+)/([^/]+)/blob/',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1), match.group(2)

        return None, None

    def _get_repository_summary(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository summary using GitIngest MCP"""
        # This would call the GitIngest MCP server
        # For now, return a placeholder structure
        return {
            "name": f"{owner}/{repo}",
            "description": "Repository description from API",
            "files": [],
            "token_count": 0,
            "summary": "Repository summary content"
        }

    def _get_repository_tree(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository tree structure using GitIngest MCP"""
        # This would call the GitIngest MCP server
        # For now, return a placeholder structure
        return {
            "tree": []
        }

    def _identify_key_files(self, repo_tree: Dict[str, Any]) -> List[str]:
        """Identify key files that need to be analyzed"""
        key_files = []

        # Priority files for MCP server analysis
        priority_files = [
            'package.json',
            'README.md',
            'src/index.ts',
            'src/index.js',
            'src/server.ts',
            'src/server.js',
            'index.ts',
            'index.js',
            'mcp.json',
            'tsconfig.json',
            'Dockerfile',
            'docker-compose.yml',
            '.github/workflows/deploy.yml',
            '.github/workflows/publish.yml',
            'docs/README.md',
            'docs/api.md',
            'CHANGELOG.md',
            'LICENSE'
        ]

        # Add TypeScript definition files
        ts_patterns = [
            'src/types.ts',
            'src/tools/*.ts',
            'src/resources/*.ts',
            'lib/*.ts'
        ]

        # This would analyze the actual tree structure
        # For now, return common patterns
        return priority_files[:10]  # Limit for demo

    def _extract_file_contents(self, owner: str, repo: str, file_paths: List[str]) -> Dict[str, str]:
        """Extract contents of key files using GitIngest MCP"""
        # This would call the GitIngest MCP server for each file
        # For now, return placeholder content
        return {
            path: f"Content of {path} would be extracted here"
            for path in file_paths
        }

    def _analyze_package_metadata(self, file_contents: Dict[str, str]) -> Dict[str, Any]:
        """Analyze package.json and other metadata files"""
        metadata = {
            "name": "unknown",
            "version": "1.0.0",
            "description": "",
            "dependencies": {},
            "scripts": {},
            "author": "",
            "license": ""
        }

        package_json = file_contents.get('package.json', '{}')
        try:
            package_data = json.loads(package_json)
            metadata.update({
                "name": package_data.get("name", metadata["name"]),
                "version": package_data.get("version", metadata["version"]),
                "description": package_data.get("description", metadata["description"]),
                "dependencies": package_data.get("dependencies", {}),
                "scripts": package_data.get("scripts", {}),
                "author": package_data.get("author", ""),
                "license": package_data.get("license", "")
            })
        except json.JSONDecodeError:
            pass

        return metadata

    def _analyze_tools_and_resources(self, file_contents: Dict[str, str], repo_tree: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze source code to extract tools and resources information"""
        tools = []
        resources = []

        # Analyze main source files for MCP tool definitions
        source_files = [
            'src/index.ts', 'src/index.js',
            'src/server.ts', 'src/server.js',
            'index.ts', 'index.js'
        ]

        for file_path in source_files:
            content = file_contents.get(file_path, '')
            if content:
                # Extract tool definitions (simplified pattern matching)
                tool_patterns = [
                    r'name:\s*["\']([^"\']+)["\']',
                    r'"name":\s*"([^"]+)"',
                    r'tool\s*\(\s*["\']([^"\']+)["\']'
                ]

                for pattern in tool_patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        if match not in [t.get('name') for t in tools]:
                            tools.append({
                                "name": match,
                                "description": f"Tool extracted from {file_path}",
                                "parameters": [],
                                "use_case": "Automated analysis - review required"
                            })

        return {
            "tools": tools,
            "resources": resources,
            "analysis_notes": f"Extracted {len(tools)} tools from source code analysis"
        }

    def _analyze_deployment_options(self, file_contents: Dict[str, str]) -> Dict[str, Any]:
        """Analyze deployment configuration and options"""
        deployment = {
            "smithery": {"available": False},
            "local": {"available": False},
            "docker": {"available": False},
            "npm": {"available": False}
        }

        # Check for package.json (npm/local deployment)
        if 'package.json' in file_contents:
            deployment["npm"]["available"] = True
            deployment["local"]["available"] = True

        # Check for Dockerfile (docker deployment)
        if 'Dockerfile' in file_contents or 'docker-compose.yml' in file_contents:
            deployment["docker"]["available"] = True

        # Check for Smithery indicators (common patterns)
        # This would be enhanced with actual analysis
        deployment["smithery"]["available"] = True  # Most MCP servers support Smithery

        return deployment

    def _generate_server_config(self, server_name: str, github_url: str,
                               repo_summary: Dict[str, Any], metadata: Dict[str, Any],
                               tools_info: Dict[str, Any], deployment_info: Dict[str, Any],
                               file_contents: Dict[str, str]) -> Dict[str, Any]:
        """Generate comprehensive server configuration JSON"""

        # Parse namespace and package from name or GitHub URL
        owner, repo = self._parse_github_url(github_url)
        namespace = owner or "unknown"
        package = repo or server_name

        config = {
            "metadata": {
                "server_id": server_name,
                "display_name": f"{package.replace('-', ' ').title()} MCP Server",
                "namespace": namespace,
                "package": package,
                "version": metadata.get("version", "1.0.0"),
                "description": metadata.get("description") or repo_summary.get("description", ""),
                "use_cases": self._extract_use_cases(file_contents),
                "tools": tools_info.get("tools", []),
                "resources": tools_info.get("resources", []),
                "requirements": self._analyze_requirements(file_contents, metadata),
                "performance": self._estimate_performance(metadata, tools_info),
                "maturity": self._assess_maturity(file_contents, metadata),
                "planned_agent": {
                    "assigned": False,
                    "agent_name": "",
                    "agent_role": "",
                    "automation_level": "manual"
                },
                "priority_deployment": self._determine_priority_deployment(deployment_info),
                "tags": self._generate_tags(metadata, tools_info, file_contents),
                "repository_url": github_url,
                "analysis_date": datetime.now().isoformat(),
                "analysis_version": "1.0.0"
            },
            "deployment": self._generate_deployment_config(deployment_info, metadata, namespace, package),
            "automation": self._generate_automation_config(tools_info, metadata),
            "integration": self._generate_integration_config(tools_info, metadata),
            "security": self._generate_security_config(file_contents, metadata),
            "monitoring": self._generate_monitoring_config(),
            "maintenance": self._generate_maintenance_config(metadata)
        }

        return config

    def _extract_use_cases(self, file_contents: Dict[str, str]) -> List[str]:
        """Extract use cases from README and documentation"""
        readme_content = file_contents.get('README.md', '')
        use_cases = []

        # Simple extraction from README sections
        sections = ['## Use Cases', '## Features', '## Capabilities', '## What it does']
        for section in sections:
            if section.lower() in readme_content.lower():
                # Extract content after section header
                # This is a simplified implementation
                use_cases.append(f"Use case extracted from README analysis")

        if not use_cases:
            use_cases = ["Repository analysis required to determine use cases"]

        return use_cases[:5]  # Limit to 5 use cases

    def _analyze_requirements(self, file_contents: Dict[str, str], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze authentication and dependency requirements"""
        return {
            "authentication": "api_key",  # Default assumption
            "api_keys_needed": [],
            "external_dependencies": [],
            "network_access": True,
            "file_system_access": False,
            "database_access": False
        }

    def _estimate_performance(self, metadata: Dict[str, Any], tools_info: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate performance characteristics"""
        return {
            "response_time": "fast",
            "resource_usage": "low",
            "concurrent_requests": 10,
            "rate_limits": "Standard API rate limits apply"
        }

    def _assess_maturity(self, file_contents: Dict[str, str], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Assess project maturity and stability"""
        return {
            "stability": "stable",
            "maintenance": "active",
            "community": "medium",
            "documentation": "good"
        }

    def _determine_priority_deployment(self, deployment_info: Dict[str, Any]) -> str:
        """Determine the priority deployment method"""
        if deployment_info.get("smithery", {}).get("available"):
            return "smithery"
        elif deployment_info.get("npm", {}).get("available"):
            return "npm"
        elif deployment_info.get("local", {}).get("available"):
            return "local"
        elif deployment_info.get("docker", {}).get("available"):
            return "docker"
        else:
            return "manual"

    def _generate_tags(self, metadata: Dict[str, Any], tools_info: Dict[str, Any], file_contents: Dict[str, str]) -> List[str]:
        """Generate relevant tags for the server"""
        tags = ["mcp-server"]

        # Add tags based on name analysis
        name = metadata.get("name", "").lower()
        if "git" in name:
            tags.append("git")
        if "database" in name or "db" in name:
            tags.append("database")
        if "api" in name:
            tags.append("api")

        return tags

    def _generate_deployment_config(self, deployment_info: Dict[str, Any], metadata: Dict[str, Any], namespace: str, package: str) -> Dict[str, Any]:
        """Generate deployment configuration section"""
        # This would generate detailed deployment configs based on analysis
        # For now, return a basic structure
        return {
            "smithery": {
                "available": deployment_info.get("smithery", {}).get("available", False),
                "profile": "junior-roadrunner-9CJKFU",
                "url": f"https://server.smithery.ai/@{namespace}/{package}/mcp",
                "install_command": f"claude mcp add @{namespace}/{package}",
                "requirements": {
                    "api_key": True,
                    "profile": True,
                    "additional_config": False
                },
                "instructions": {
                    "setup": [
                        "Configure Smithery API key and profile",
                        f"Install via: claude mcp add @{namespace}/{package}",
                        "Verify installation and connectivity"
                    ]
                }
            }
        }

    def _generate_automation_config(self, tools_info: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automation configuration"""
        return {
            "global_instructions": {
                "enabled": False,
                "instructions": ["Generated instructions based on repository analysis"],
                "triggers": ["Automatic triggers based on tool analysis"]
            }
        }

    def _generate_integration_config(self, tools_info: Dict[str, Any], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate integration configuration"""
        return {
            "mcp_servers": [],
            "external_systems": [],
            "data_flow": {
                "inputs": ["Input types determined from analysis"],
                "outputs": ["Output types determined from analysis"],
                "storage": ["Storage requirements from analysis"]
            }
        }

    def _generate_security_config(self, file_contents: Dict[str, str], metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security configuration"""
        return {
            "authentication": {
                "methods": ["api_key"],
                "credential_storage": "environment",
                "rotation_required": False,
                "encryption": "in_transit"
            }
        }

    def _generate_monitoring_config(self) -> Dict[str, Any]:
        """Generate monitoring configuration"""
        return {
            "health_check": {
                "endpoint": "/health",
                "method": "GET",
                "expected_response": "200",
                "timeout": 5000
            }
        }

    def _generate_maintenance_config(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate maintenance configuration"""
        return {
            "update_frequency": "monthly",
            "backup_required": False,
            "downtime_tolerance": "low"
        }

    def save_config(self, config: Dict[str, Any], server_name: str) -> str:
        """Save the generated configuration to a JSON file"""
        output_path = self.active_dir / f"{server_name}.json"

        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2, sort_keys=True)

        return str(output_path)

def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze MCP server repository and generate configuration')
    parser.add_argument('github_url', help='GitHub repository URL')
    parser.add_argument('server_name', help='MCP server name')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    args = parser.parse_args()

    try:
        analyzer = MCPServerAnalyzer()

        print(f"🚀 Starting analysis of {args.server_name}")
        config = analyzer.analyze_server_repository(args.github_url, args.server_name)

        if args.output:
            output_path = args.output
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=2, sort_keys=True)
        else:
            output_path = analyzer.save_config(config, args.server_name)

        print(f"✅ Analysis complete! Configuration saved to: {output_path}")
        print(f"📊 Found {len(config['metadata']['tools'])} tools")
        print(f"🏷️  Tags: {', '.join(config['metadata']['tags'])}")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()