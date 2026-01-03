#!/usr/bin/env python3
"""
MCP Catalog Validator

Validates catalog/mcp_servers.yaml against validation_schema.json
Checks:
- YAML syntax and structure
- JSON Schema compliance
- Required fields presence
- Type correctness
- Reference validity

Usage:
    python validate-catalog.py

Dependencies:
    pip install pyyaml jsonschema
"""

import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from jsonschema import validate, ValidationError, Draft7Validator
except ImportError:
    print("Error: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)


class CatalogValidator:
    """Validates MCP catalog YAML files."""

    def __init__(self, catalog_dir: Path = None):
        """Initialize validator with catalog directory path."""
        self.catalog_dir = catalog_dir or Path(__file__).parent
        self.yaml_file = self.catalog_dir / "mcp_servers.yaml"
        self.schema_file = self.catalog_dir / "validation_schema.json"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.catalog_data: Dict = {}

    def load_yaml(self) -> bool:
        """Load and parse YAML file."""
        try:
            with open(self.yaml_file, "r") as f:
                self.catalog_data = yaml.safe_load(f)
            if not self.catalog_data:
                self.errors.append(f"YAML file is empty: {self.yaml_file}")
                return False
            return True
        except FileNotFoundError:
            self.errors.append(f"YAML file not found: {self.yaml_file}")
            return False
        except yaml.YAMLError as e:
            self.errors.append(f"YAML syntax error: {e}")
            return False

    def load_schema(self) -> bool:
        """Load and parse JSON schema."""
        try:
            with open(self.schema_file, "r") as f:
                self.schema = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"Schema file not found: {self.schema_file}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"JSON schema syntax error: {e}")
            return False

    def validate_schema(self) -> bool:
        """Validate catalog against JSON schema."""
        try:
            validate(instance=self.catalog_data, schema=self.schema)
            return True
        except ValidationError as e:
            self.errors.append(
                f"Schema validation error: {e.message}\n"
                f"  Path: {' -> '.join(str(p) for p in e.absolute_path)}\n"
                f"  Value: {e.instance}"
            )
            return False

    def validate_server_coverage(self) -> bool:
        """Validate tool coverage metrics."""
        servers = self.catalog_data.get("servers", [])
        valid = True

        for server in servers:
            server_id = server.get("id", "unknown")
            tool_coverage = server.get("tool_coverage", "")

            if not tool_coverage:
                self.warnings.append(f"Server {server_id}: Missing tool_coverage field")
                continue

            try:
                documented, total = map(int, tool_coverage.split("/"))
                if documented > total:
                    self.errors.append(
                        f"Server {server_id}: Documented tools ({documented}) "
                        f"exceeds total ({total})"
                    )
                    valid = False
                if documented < len(server.get("tools", [])):
                    self.warnings.append(
                        f"Server {server_id}: tool_coverage may be inaccurate"
                    )
            except ValueError:
                self.errors.append(
                    f"Server {server_id}: Invalid tool_coverage format '{tool_coverage}'"
                )
                valid = False

        return valid

    def validate_references(self) -> bool:
        """Validate internal references (e.g., pairs_well_with)."""
        servers = self.catalog_data.get("servers", [])
        server_ids = {s.get("id") for s in servers}
        valid = True

        for server in servers:
            server_id = server.get("id", "unknown")
            pairs = server.get("pairs_well_with", [])

            for pair_id in pairs:
                if pair_id not in server_ids:
                    self.warnings.append(
                        f"Server {server_id}: Referenced server '{pair_id}' "
                        f"not found in catalog"
                    )

        return valid

    def validate_deniz_tags(self) -> bool:
        """Validate Deniz-specific fields for P0/P1 servers."""
        servers = self.catalog_data.get("servers", [])
        valid = True

        for server in servers:
            if server.get("deniz_recommended"):
                server_id = server.get("id", "unknown")

                if not server.get("deniz_use_cases"):
                    self.warnings.append(
                        f"Server {server_id}: Missing deniz_use_cases "
                        f"for deniz_recommended server"
                    )

                tags = server.get("tags", [])
                deniz_tags = [t for t in tags if t.startswith("deniz-")]
                if not deniz_tags:
                    self.warnings.append(
                        f"Server {server_id}: Missing deniz-* tags for recommended server"
                    )

        return valid

    def report(self) -> Tuple[bool, int, int]:
        """Print validation report."""
        success = len(self.errors) == 0
        error_count = len(self.errors)
        warning_count = len(self.warnings)

        print("\n" + "=" * 70)
        print("MCP CATALOG VALIDATION REPORT")
        print("=" * 70)

        if self.errors:
            print(f"\n❌ ERRORS ({error_count}):")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS ({warning_count}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if success:
            print("\n✅ Validation PASSED")
            if self.catalog_data:
                servers = len(self.catalog_data.get("servers", []))
                print(
                    f"   Catalog contains {servers} server(s), "
                    f"{warning_count} warning(s)"
                )
        else:
            print(f"\n❌ Validation FAILED with {error_count} error(s)")

        print("=" * 70 + "\n")
        return success, error_count, warning_count

    def validate(self) -> bool:
        """Run all validations."""
        if not self.load_schema():
            return False

        if not self.load_yaml():
            return False

        if not self.validate_schema():
            return False

        self.validate_server_coverage()
        self.validate_references()
        self.validate_deniz_tags()

        success, _, _ = self.report()
        return success


def main():
    """Main entry point."""
    validator = CatalogValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
