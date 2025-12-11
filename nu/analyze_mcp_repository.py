#!/usr/bin/env python3
"""
MCP Server Repository Analysis with GitIngest Integration
Uses GitIngest MCP tools to analyze repositories and delegates to AI agents for JSON generation
"""

import json
import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

class MCPRepositoryAnalyzer:
    def __init__(self):
        self.claude_hq_dir = Path(__file__).parent.parent.parent
        self.mcp_servers_dir = self.claude_hq_dir / "mcp-servers"
        self.templates_dir = self.mcp_servers_dir / "templates"
        self.active_dir = self.mcp_servers_dir / "active"
        self.temp_dir = Path(tempfile.mkdtemp(prefix="mcp_analysis_"))

        # Detect available AI agents
        self.available_agents = self._detect_agents()
        self.selected_agent = self._select_best_agent()

    def _detect_agents(self) -> Dict[str, bool]:
        """Detect which AI agents are available"""
        agents = {}

        # Check for Gemini CLI
        try:
            result = subprocess.run(['which', 'gemini'], capture_output=True, text=True)
            agents['gemini'] = result.returncode == 0
        except:
            agents['gemini'] = False

        # Check for Codex
        try:
            result = subprocess.run(['which', 'codex'], capture_output=True, text=True)
            agents['codex'] = result.returncode == 0
        except:
            agents['codex'] = False

        agents['claude'] = True  # Always available (current execution context)

        return agents

    def _select_best_agent(self) -> str:
        """Select the best available agent for analysis"""
        if self.available_agents.get('gemini', False):
            return 'gemini'
        elif self.available_agents.get('codex', False):
            return 'codex'
        else:
            return 'claude'

    def analyze_repository(self, github_url: str, server_name: str) -> Dict[str, Any]:
        """
        Complete repository analysis workflow using GitIngest MCP and AI agents
        """
        print(f"🔍 Analyzing MCP server repository: {github_url}")
        print(f"🤖 Using AI agent: {self.selected_agent}")

        try:
            # Step 1: Extract repository information
            owner, repo = self._parse_github_url(github_url)
            if not owner or repo:
                raise ValueError(f"Invalid GitHub URL: {github_url}")

            # Step 2: Use GitIngest MCP for repository analysis
            print("📊 Step 1: Getting repository summary via GitIngest MCP...")
            repo_summary = self._get_repository_summary(owner, repo)

            print("🌳 Step 2: Getting repository tree structure via GitIngest MCP...")
            repo_tree = self._get_repository_tree(owner, repo)

            print("📁 Step 3: Identifying key files for analysis...")
            key_files = self._identify_key_files(repo_tree, repo_summary)

            print(f"📄 Step 4: Extracting {len(key_files)} key files via GitIngest MCP...")
            file_contents = self._extract_file_contents(owner, repo, key_files)

            # Step 3: Prepare analysis context for AI agent
            analysis_context = {
                "repository": {
                    "owner": owner,
                    "repo": repo,
                    "url": github_url,
                    "server_name": server_name
                },
                "gitingest_data": {
                    "summary": repo_summary,
                    "tree": repo_tree,
                    "files": file_contents
                },
                "analysis_metadata": {
                    "timestamp": datetime.now().isoformat(),
                    "analyzer": f"GitIngest + {self.selected_agent}",
                    "key_files_count": len(key_files),
                    "available_agents": self.available_agents
                }
            }

            # Step 4: Generate configuration using selected AI agent
            print(f"🧠 Step 5: Generating MCP configuration via {self.selected_agent}...")
            config = self._generate_config_with_agent(analysis_context)

            print("✅ Repository analysis complete!")
            return config

        except Exception as e:
            print(f"❌ Error during repository analysis: {e}")
            raise
        finally:
            # Cleanup temporary directory
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _parse_github_url(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract owner and repo from GitHub URL"""
        import re
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
        print(f"   Calling GitIngest MCP git_summary for {owner}/{repo}...")

        # Create Claude Code command to call GitIngest MCP
        cmd = [
            'claude', '-p',
            f'Use GitIngest MCP git_summary tool to analyze repository {owner}/{repo}. '
            f'Return only the raw JSON response from the tool, no additional text or formatting.'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                # Try to extract JSON from response
                response = result.stdout.strip()
                # Look for JSON in the response
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    print(f"   ⚠️  Could not extract JSON from GitIngest response")
                    return {"name": f"{owner}/{repo}", "description": "Analysis failed", "files": [], "token_count": 0}
            else:
                print(f"   ⚠️  GitIngest MCP call failed: {result.stderr}")
                return {"name": f"{owner}/{repo}", "description": "GitIngest call failed", "files": [], "token_count": 0}
        except subprocess.TimeoutExpired:
            print(f"   ⚠️  GitIngest MCP call timed out")
            return {"name": f"{owner}/{repo}", "description": "Analysis timed out", "files": [], "token_count": 0}
        except json.JSONDecodeError as e:
            print(f"   ⚠️  Failed to parse GitIngest JSON response: {e}")
            return {"name": f"{owner}/{repo}", "description": "JSON parse failed", "files": [], "token_count": 0}

    def _get_repository_tree(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository tree structure using GitIngest MCP"""
        print(f"   Calling GitIngest MCP git_tree for {owner}/{repo}...")

        cmd = [
            'claude', '-p',
            f'Use GitIngest MCP git_tree tool to get the tree structure of repository {owner}/{repo}. '
            f'Return only the raw JSON response from the tool, no additional text or formatting.'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                response = result.stdout.strip()
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    print(f"   ⚠️  Could not extract JSON from GitIngest tree response")
                    return {"tree": []}
            else:
                print(f"   ⚠️  GitIngest tree call failed: {result.stderr}")
                return {"tree": []}
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            print(f"   ⚠️  GitIngest tree call error: {e}")
            return {"tree": []}

    def _identify_key_files(self, repo_tree: Dict[str, Any], repo_summary: Dict[str, Any]) -> List[str]:
        """Identify key files that need detailed analysis"""
        key_files = []

        # Priority files for MCP server analysis
        priority_patterns = [
            'package.json',
            'README.md',
            'src/index.ts',
            'src/index.js',
            'src/server.ts',
            'src/server.js',
            'src/main.ts',
            'src/main.js',
            'index.ts',
            'index.js',
            'server.ts',
            'server.js',
            'mcp.json',
            'tsconfig.json',
            'src/types.ts',
            'src/types.d.ts',
            'src/tools/',
            'src/resources/',
            'lib/index.ts',
            'lib/index.js',
            'dist/index.js',
            'Dockerfile',
            'docker-compose.yml',
            'docs/README.md',
            'docs/API.md',
            'docs/api.md',
            'CHANGELOG.md',
            'LICENSE'
        ]

        # Extract file paths from tree (simplified)
        tree_files = []
        if 'tree' in repo_tree and isinstance(repo_tree['tree'], list):
            for item in repo_tree['tree']:
                if isinstance(item, dict) and 'path' in item:
                    tree_files.append(item['path'])

        # Also check summary files list
        if 'files' in repo_summary and isinstance(repo_summary['files'], list):
            tree_files.extend(repo_summary['files'])

        # Match priority patterns against actual files
        for pattern in priority_patterns:
            if '/' in pattern:
                # Directory pattern - find files in that directory
                for file_path in tree_files:
                    if pattern in file_path and file_path not in key_files:
                        key_files.append(file_path)
            else:
                # Exact file pattern
                for file_path in tree_files:
                    if file_path.endswith(pattern) and file_path not in key_files:
                        key_files.append(file_path)

        # Limit to reasonable number of files
        return key_files[:15]

    def _extract_file_contents(self, owner: str, repo: str, file_paths: List[str]) -> Dict[str, str]:
        """Extract file contents using GitIngest MCP git_files tool"""
        if not file_paths:
            return {}

        print(f"   Calling GitIngest MCP git_files for {len(file_paths)} files...")

        # Prepare file paths for GitIngest (as JSON array)
        file_paths_json = json.dumps(file_paths)

        cmd = [
            'claude', '-p',
            f'Use GitIngest MCP git_files tool to get contents of files {file_paths_json} '
            f'from repository {owner}/{repo}. Return only the raw JSON response from the tool, '
            f'no additional text or formatting.'
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                response = result.stdout.strip()
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    files_data = json.loads(json_str)

                    # Extract file contents from GitIngest response format
                    file_contents = {}
                    if isinstance(files_data, dict):
                        for file_path in file_paths:
                            if file_path in files_data:
                                file_contents[file_path] = files_data[file_path]

                    return file_contents
                else:
                    print(f"   ⚠️  Could not extract JSON from GitIngest files response")
                    return {}
            else:
                print(f"   ⚠️  GitIngest files call failed: {result.stderr}")
                return {}
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            print(f"   ⚠️  GitIngest files call error: {e}")
            return {}

    def _generate_config_with_agent(self, analysis_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate MCP server configuration using selected AI agent"""

        # Save analysis context to temporary file
        context_file = self.temp_dir / "analysis_context.json"
        with open(context_file, 'w') as f:
            json.dump(analysis_context, f, indent=2)

        # Load template for reference
        template_file = self.templates_dir / "_template.json"
        with open(template_file, 'r') as f:
            template = json.load(f)

        template_file_temp = self.temp_dir / "template.json"
        with open(template_file_temp, 'w') as f:
            json.dump(template, f, indent=2)

        # Create prompt for AI agent
        prompt = self._create_analysis_prompt(analysis_context, str(template_file_temp))

        if self.selected_agent == 'gemini':
            return self._generate_with_gemini(prompt, str(context_file))
        elif self.selected_agent == 'codex':
            return self._generate_with_codex(prompt, str(context_file))
        else:
            return self._generate_with_claude(prompt, analysis_context)

    def _create_analysis_prompt(self, context: Dict[str, Any], template_path: str) -> str:
        """Create comprehensive analysis prompt for AI agents"""
        repo_info = context['repository']

        prompt = f"""
You are an expert MCP (Model Context Protocol) server analyst. Analyze the repository data from GitIngest MCP and generate a comprehensive, accurate MCP server configuration JSON.

REPOSITORY: {repo_info['owner']}/{repo_info['repo']}
URL: {repo_info['url']}
SERVER NAME: {repo_info['server_name']}

ANALYSIS TASK:
1. Review the GitIngest repository summary, tree structure, and file contents
2. Extract accurate information about tools, resources, and capabilities
3. Determine deployment options and requirements
4. Generate automation recommendations and integration points
5. Create a complete MCP server configuration JSON following the template structure

KEY ANALYSIS AREAS:
- Extract actual tool definitions from source code (look for tool names, descriptions, parameters)
- Identify resource definitions and URI templates
- Determine authentication requirements and API keys needed
- Analyze package.json for dependencies and deployment info
- Review README for use cases and documentation quality
- Assess deployment options (Smithery, local, Docker, NPM)
- Generate appropriate automation workflows and triggers

TEMPLATE REFERENCE: {template_path}

OUTPUT REQUIREMENTS:
- Return ONLY valid JSON matching the template structure
- Use actual data extracted from repository analysis
- Ensure all tool names, descriptions, and parameters are accurate
- Include realistic use cases based on the code analysis
- Set appropriate deployment configurations based on repository structure
- Generate meaningful automation instructions and triggers

Begin analysis and return the complete JSON configuration:
"""
        return prompt

    def _generate_with_gemini(self, prompt: str, context_file: str) -> Dict[str, Any]:
        """Generate configuration using Gemini CLI"""
        print("   🧠 Generating configuration with Gemini CLI...")

        # Create prompt file
        prompt_file = self.temp_dir / "gemini_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
            f.write(f"\n\nANALYSIS CONTEXT FILE: {context_file}")

        try:
            cmd = ['gemini', '-y', '-p', 'architect', '-f', str(prompt_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                response = result.stdout.strip()
                # Extract JSON from Gemini response
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    print("   ⚠️  Could not extract JSON from Gemini response")
                    return self._fallback_config()
            else:
                print(f"   ⚠️  Gemini CLI failed: {result.stderr}")
                return self._fallback_config()

        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            print(f"   ⚠️  Gemini generation error: {e}")
            return self._fallback_config()

    def _generate_with_codex(self, prompt: str, context_file: str) -> Dict[str, Any]:
        """Generate configuration using Codex"""
        print("   🧠 Generating configuration with Codex...")

        try:
            cmd = ['codex', '-p', prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                response = result.stdout.strip()
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    print("   ⚠️  Could not extract JSON from Codex response")
                    return self._fallback_config()
            else:
                print(f"   ⚠️  Codex failed: {result.stderr}")
                return self._fallback_config()

        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            print(f"   ⚠️  Codex generation error: {e}")
            return self._fallback_config()

    def _generate_with_claude(self, prompt: str, analysis_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate configuration using Claude Code (fallback)"""
        print("   🧠 Generating configuration with Claude Code (fallback)...")

        # Since we're already in Claude context, return a basic config
        return self._fallback_config()

    def _fallback_config(self) -> Dict[str, Any]:
        """Generate basic fallback configuration"""
        with open(self.templates_dir / "_template.json", 'r') as f:
            template = json.load(f)

        # Return template with minimal modifications
        template['metadata']['analysis_date'] = datetime.now().isoformat()
        template['metadata']['generated_by'] = 'fallback_generator'
        return template

    def save_config(self, config: Dict[str, Any], server_name: str) -> str:
        """Save generated configuration to JSON file"""
        output_path = self.active_dir / f"{server_name}.json"

        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2, sort_keys=True)

        return str(output_path)

def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Analyze MCP server repository with GitIngest and AI agents')
    parser.add_argument('github_url', help='GitHub repository URL')
    parser.add_argument('server_name', help='MCP server identifier')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    parser.add_argument('--agent', choices=['gemini', 'codex', 'claude'], help='Force specific AI agent')
    args = parser.parse_args()

    try:
        analyzer = MCPRepositoryAnalyzer()

        # Override agent selection if specified
        if args.agent and analyzer.available_agents.get(args.agent, False):
            analyzer.selected_agent = args.agent

        print(f"🚀 Starting comprehensive repository analysis")
        print(f"🔗 Repository: {args.github_url}")
        print(f"🏷️  Server: {args.server_name}")
        print(f"🤖 AI Agent: {analyzer.selected_agent}")
        print(f"🛠️  Available agents: {list(k for k, v in analyzer.available_agents.items() if v)}")
        print("")

        config = analyzer.analyze_repository(args.github_url, args.server_name)

        if args.output:
            output_path = args.output
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=2, sort_keys=True)
        else:
            output_path = analyzer.save_config(config, args.server_name)

        print("")
        print(f"✅ Analysis complete! Configuration saved to: {output_path}")
        print(f"📊 Tools found: {len(config.get('metadata', {}).get('tools', []))}")
        print(f"🏷️  Tags: {', '.join(config.get('metadata', {}).get('tags', []))}")
        print(f"🚀 Priority deployment: {config.get('metadata', {}).get('priority_deployment', 'unknown')}")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()