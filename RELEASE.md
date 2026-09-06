# DoveWAI Protocol v0.2 Release

DoveWAI Protocol v0.2 is release-ready from source once the manual validation and release preflight pass on `main`.

## Release entry points

- Validation: `.github/workflows/manual-v02-validation.yml`
- Release: `.github/workflows/manual-v02-release.yml`

Both workflows are manual-only (`workflow_dispatch`).

## Registry publishing

The repository is prepared for OIDC trusted publishing.

Before selecting the PyPI publish option, configure a trusted publisher for project `dovewai-protocol` that trusts this repository and workflow filename `manual-v02-release.yml` (and the `pypi` environment if used in the registry configuration).

Before selecting the npm publish option, configure a trusted publisher for package `@dovewai/protocol` that trusts this repository and workflow filename `manual-v02-release.yml` (and the `npm` environment if used in the registry configuration).

Do not add long-lived PyPI or npm write tokens to the repository merely to make publishing work.

## GitHub release

The release workflow can create tag `v0.2.0` and the corresponding GitHub release after preflight passes.

## Scope

The v0.2 release includes the specification, normative schema, migration guidance, reference Python and TypeScript SDKs, public CLI, lifecycle validator, TCK, conformance vectors, examples, and interoperability/adoption profiles.

The release remains experimental (`0.x`). It is not a claim of independent interoperability certification or security audit completion.
