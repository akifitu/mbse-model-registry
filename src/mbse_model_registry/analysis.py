"""Analysis helpers for the model registry."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


REQUIRED_FIELDS = {
    "id",
    "title",
    "domain",
    "view_types",
    "linked_repositories",
    "requirement_count",
    "interface_count",
}


@dataclass
class RegistryResult:
    errors: List[str]
    warnings: List[str]
    summary: Dict[str, Any]
    package_rows: List[Dict[str, str]]
    coverage_rows: List[Dict[str, str]]


def analyze_packages(packages: Sequence[Mapping[str, Any]]) -> RegistryResult:
    """Validate model packages and build export rows."""
    errors: List[str] = []
    warnings: List[str] = []
    _check_duplicate_ids(packages, errors)

    package_rows: List[Dict[str, str]] = []
    repo_coverage: Dict[str, Dict[str, int]] = defaultdict(lambda: {"package_count": 0, "view_count": 0})

    for package in packages:
        if not _validate_package(package, errors):
            continue
        package_rows.append(
            {
                "id": package["id"],
                "title": package["title"],
                "domain": package["domain"],
                "view_types": "; ".join(package["view_types"]),
                "linked_repositories": "; ".join(package["linked_repositories"]),
                "requirement_count": str(package["requirement_count"]),
                "interface_count": str(package["interface_count"]),
            }
        )
        if package["requirement_count"] < 5:
            warnings.append(f"{package['id']}: requirement coverage is unusually low ({package['requirement_count']}).")
        for repo in package["linked_repositories"]:
            repo_coverage[repo]["package_count"] += 1
            repo_coverage[repo]["view_count"] += len(package["view_types"])

    coverage_rows = [
        {
            "repository": repo,
            "package_count": str(values["package_count"]),
            "view_count": str(values["view_count"]),
        }
        for repo, values in sorted(repo_coverage.items())
    ]

    summary = {
        "package_count": len(package_rows),
        "domain_count": len({row["domain"] for row in package_rows}),
        "linked_repository_count": len(coverage_rows),
        "view_type_count": len({view for package in packages for view in package.get("view_types", [])}),
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    return RegistryResult(errors, warnings, summary, package_rows, coverage_rows)


def _check_duplicate_ids(packages: Sequence[Mapping[str, Any]], errors: List[str]) -> None:
    seen = set()
    for package in packages:
        package_id = package.get("id")
        if package_id in seen:
            errors.append(f"duplicate package id '{package_id}' detected.")
        seen.add(package_id)


def _validate_package(package: Mapping[str, Any], errors: List[str]) -> bool:
    package_id = str(package.get("id", "<missing-id>"))
    missing = sorted(field for field in REQUIRED_FIELDS if package.get(field) in ("", None))
    if missing:
        errors.append(f"{package_id}: missing required fields: {', '.join(missing)}.")
        return False
    if not isinstance(package["view_types"], list) or not package["view_types"]:
        errors.append(f"{package_id}: view_types must contain at least one entry.")
    if not isinstance(package["linked_repositories"], list) or not package["linked_repositories"]:
        errors.append(f"{package_id}: linked_repositories must contain at least one repository.")
    for field in ("requirement_count", "interface_count"):
        if not isinstance(package[field], int) or package[field] < 0:
            errors.append(f"{package_id}: {field} must be a non-negative integer.")
    return True
