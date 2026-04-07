# MBSE Model Registry

`MBSE Model Registry` is a systems engineering portfolio repository that catalogs model packages, architecture views, and repository allocations in one structured place. It is designed to show how an MBSE-oriented layer can sit above individual analysis repos.

This repo answers questions like:

- Which model packages represent which parts of the system?
- Which repositories are covered by which architecture views?
- Where are interface, behavior, and verification views concentrated?

## What This Repo Demonstrates

- MBSE-oriented portfolio structure
- architecture view cataloging
- allocation of repositories to model packages
- automation, tests, and reviewer-friendly exports

## Repository Map

```text
.
|-- data/                        # Structured model package definitions
|-- docs/                        # Build plan and modeling notes
|-- reports/                     # Generated summaries and dashboards
|-- src/mbse_model_registry/     # Validation, analysis, export, and CLI logic
|-- tests/                       # Regression tests
|-- .github/workflows/           # CI pipeline
|-- Makefile                     # Common commands
`-- README.md
```

## Quick Start

```bash
make test
make catalog
```

Or run the CLI directly:

```bash
PYTHONPATH=src python3 -m mbse_model_registry.cli catalog --data-file data/model_packages.json --export-dir reports
```

## Generated Outputs

- `reports/model-summary.md`
- `reports/model-catalog.csv`
- `reports/repo-coverage.csv`
- `reports/model-dashboard.html`

## Documentation

- [docs/README.md](docs/README.md)
- [docs/project_plan.md](docs/project_plan.md)
- [docs/modeling_notes.md](docs/modeling_notes.md)

## Why This Matters For A Recruiter

This repo shows that the portfolio includes an architecture and model-governance viewpoint, not only code-centric analysis artifacts. It gives you a clean way to discuss MBSE thinking, view decomposition, and repository allocation in interviews.
