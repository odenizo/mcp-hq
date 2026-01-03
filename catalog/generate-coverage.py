#!/usr/bin/env python3
"""
MCP Catalog Coverage Report Generator

Generates coverage statistics and reports for the MCP catalog.
Analyzes:
- Servers per category
- Tools per server
- Documentation completeness
- Deniz-specific coverage

Usage:
    python generate-coverage.py
    python generate-coverage.py --json   # Output as JSON
    python generate-coverage.py --markdown # Output as Markdown

Dependencies:
    pip install pyyaml
"""

import sys
import json
import yaml
from pathlib import Path
from collections import defaultdict
from typing import Dict, List
from datetime import datetime


class CoverageReporter:
    """Generates coverage reports for MCP catalog."""

    def __init__(self, catalog_dir: Path = None):
        """Initialize reporter with catalog directory."""
        self.catalog_dir = catalog_dir or Path(__file__).parent
        self.yaml_file = self.catalog_dir / "mcp_servers.yaml"
        self.catalog_data: Dict = {}
        self.report_file = self.catalog_dir / "coverage_stats.md"

    def load_catalog(self) -> bool:
        """Load catalog YAML."""
        try:
            with open(self.yaml_file, "r") as f:
                self.catalog_data = yaml.safe_load(f)
            return True if self.catalog_data else False
        except FileNotFoundError:
            print(f"Error: Catalog file not found: {self.yaml_file}")
            return False
        except yaml.YAMLError as e:
            print(f"Error loading catalog: {e}")
            return False

    def calculate_coverage(self) -> Dict:
        """Calculate coverage statistics."""
        servers = self.catalog_data.get("servers", [])
        coverage = {
            "total_servers": len(servers),
            "total_tools": 0,
            "by_category": defaultdict(lambda: {"servers": 0, "tools": 0}),
            "by_maturity": defaultdict(int),
            "by_auth_model": defaultdict(int),
            "deniz_recommended": 0,
            "complete_documentation": 0,
            "details": [],
        }

        for server in servers:
            server_id = server.get("id", "unknown")
            category = server.get("category", "uncategorized")
            maturity = server.get("maturity", "unknown")
            auth_model = server.get("auth_model", "none")
            tools = server.get("tools", [])
            tool_count = len(tools)
            deniz_recommended = server.get("deniz_recommended", False)
            doc_status = server.get("doc_status", "draft")

            coverage["total_tools"] += tool_count
            coverage["by_category"][category]["servers"] += 1
            coverage["by_category"][category]["tools"] += tool_count
            coverage["by_maturity"][maturity] += 1
            coverage["by_auth_model"][auth_model] += 1

            if deniz_recommended:
                coverage["deniz_recommended"] += 1

            if doc_status == "complete":
                coverage["complete_documentation"] += 1

            coverage["details"].append({
                "id": server_id,
                "name": server.get("name", "Unknown"),
                "category": category,
                "tools": tool_count,
                "maturity": maturity,
                "auth_model": auth_model,
                "deniz_recommended": deniz_recommended,
                "doc_status": doc_status,
            })

        return coverage

    def generate_markdown_report(self, coverage: Dict) -> str:
        """Generate markdown format report."""
        report = []
        report.append("# MCP Catalog Coverage Report\n")
        report.append(f"Generated: {datetime.now().isoformat()}\n\n")

        # Summary
        report.append("## Summary\n")
        report.append(
            f"- **Total Servers**: {coverage['total_servers']}\n"
            f"- **Total Tools**: {coverage['total_tools']}\n"
            f"- **Deniz Recommended**: {coverage['deniz_recommended']}\n"
            f"- **Fully Documented**: {coverage['complete_documentation']}\n"
        )

        # Coverage by category
        if coverage["by_category"]:
            report.append("\n## Coverage by Category\n\n")
            report.append("| Category | Servers | Tools |\n")
            report.append("|----------|---------|-------|\n")
            for category in sorted(coverage["by_category"].keys()):
                stats = coverage["by_category"][category]
                report.append(
                    f"| {category} | {stats['servers']} | {stats['tools']} |\n"
                )

        # Coverage by maturity
        if coverage["by_maturity"]:
            report.append("\n## Coverage by Maturity\n\n")
            report.append("| Maturity | Count |\n")
            report.append("|----------|-------|\n")
            for maturity in sorted(coverage["by_maturity"].keys()):
                report.append(f"| {maturity} | {coverage['by_maturity'][maturity]} |\n")

        # Coverage by auth model
        if coverage["by_auth_model"]:
            report.append("\n## Coverage by Auth Model\n\n")
            report.append("| Auth Model | Count |\n")
            report.append("|------------|-------|\n")
            for auth_model in sorted(coverage["by_auth_model"].keys()):
                report.append(f"| {auth_model} | {coverage['by_auth_model'][auth_model]} |\n")

        # Detailed server list
        if coverage["details"]:
            report.append("\n## Server Details\n\n")
            report.append("| Server | Category | Tools | Maturity | Auth | Deniz | Doc |\n")
            report.append("|--------|----------|-------|----------|------|-------|-----|\n")
            for server in sorted(coverage["details"], key=lambda x: x["name"]):
                deniz = "✓" if server["deniz_recommended"] else ""
                report.append(
                    f"| {server['name']} | {server['category']} | "
                    f"{server['tools']} | {server['maturity']} | "
                    f"{server['auth_model']} | {deniz} | {server['doc_status']} |\n"
                )

        return "".join(report)

    def generate_json_report(self, coverage: Dict) -> str:
        """Generate JSON format report."""
        # Convert defaultdicts to regular dicts for JSON serialization
        json_coverage = {
            "generated": datetime.now().isoformat(),
            "total_servers": coverage["total_servers"],
            "total_tools": coverage["total_tools"],
            "deniz_recommended": coverage["deniz_recommended"],
            "complete_documentation": coverage["complete_documentation"],
            "by_category": dict(coverage["by_category"]),
            "by_maturity": dict(coverage["by_maturity"]),
            "by_auth_model": dict(coverage["by_auth_model"]),
            "details": coverage["details"],
        }
        return json.dumps(json_coverage, indent=2)

    def save_report(self, content: str) -> bool:
        """Save report to file."""
        try:
            with open(self.report_file, "w") as f:
                f.write(content)
            print(f"\u2705 Report saved to {self.report_file}")
            return True
        except IOError as e:
            print(f"Error saving report: {e}")
            return False

    def generate(self, format_type: str = "markdown") -> bool:
        """Generate and save coverage report."""
        if not self.load_catalog():
            return False

        coverage = self.calculate_coverage()

        if format_type == "json":
            report = self.generate_json_report(coverage)
            print(report)
        else:
            report = self.generate_markdown_report(coverage)
            print(report)
            self.save_report(report)

        return True


def main():
    """Main entry point."""
    format_type = "markdown"

    if len(sys.argv) > 1:
        if "--json" in sys.argv:
            format_type = "json"
        elif "--markdown" in sys.argv:
            format_type = "markdown"

    reporter = CoverageReporter()
    success = reporter.generate(format_type=format_type)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
