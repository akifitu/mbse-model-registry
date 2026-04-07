"""CLI for the MBSE model registry."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .analysis import analyze_packages
from .data import load_packages
from .export import export_reports


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        prog="mbse-model-registry",
        description="Validate and export model package registry artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    catalog_parser = subparsers.add_parser("catalog", help="Analyze model packages and export reports.")
    catalog_parser.add_argument("--data-file", default="data/model_packages.json", help="Path to the model package JSON file.")
    catalog_parser.add_argument("--export-dir", help="Directory where reports should be written.")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "catalog":
        result = analyze_packages(load_packages(Path(args.data_file)))
        _print_summary(result)
        if args.export_dir:
            export_reports(result, Path(args.export_dir))
            print(f"Reports exported to: {args.export_dir}")
        return 1 if result.errors else 0

    parser.error("Unknown command.")
    return 2


def _print_summary(result) -> None:
    summary = result.summary
    print("Model registry summary")
    print(f"  Model packages: {summary['package_count']}")
    print(f"  Domains: {summary['domain_count']}")
    print(f"  Linked repositories: {summary['linked_repository_count']}")
    print(f"  Unique view types: {summary['view_type_count']}")
    print(f"  Errors: {summary['error_count']}")
    print(f"  Warnings: {summary['warning_count']}")
    if result.errors:
        print("Validation errors:")
        for item in result.errors:
            print(f"  - {item}")
    if result.warnings:
        print("Validation warnings:")
        for item in result.warnings:
            print(f"  - {item}")


if __name__ == "__main__":
    raise SystemExit(run())
