# Step-By-Step Plan

## Phase 1: Define the modeling scope

1. Choose the system domains that need model packages.
2. Decide which view types to catalog.
3. Link each package to relevant repositories.

## Phase 2: Build the source data

1. Store packages as machine-readable records.
2. Capture view names, repository links, and requirement counts.
3. Define simple consistency rules.

## Phase 3: Implement the registry logic

1. Validate package structure and repository references.
2. Summarize domain and view coverage.
3. Export reviewer-friendly catalog artifacts.

## Phase 4: Debug and verify

1. Add tests for missing package IDs and empty view lists.
2. Check that coverage rollups match the dataset.
3. Fix formatting or validation gaps.

## Phase 5: Publish professionally

1. Write clear MBSE-oriented documentation.
2. Commit generated reports.
3. Push publicly and keep CI green.

## To-Do

- [x] define the model package schema
- [x] create a realistic architecture-view dataset
- [x] implement validation and exporter logic
- [x] add regression tests
- [ ] publish the repository
