# v0.2 Release Status

Source release preparation is complete.

The final release gate is executable rather than declarative:

1. Run **Manual v0.2 Validation** on `main`.
2. Run **Manual v0.2 Release** on `main` with version `0.2.0`.
3. Leave registry publishing disabled until the corresponding PyPI/npm trusted publisher is configured.
4. Enable GitHub release creation when ready to create tag `v0.2.0`.

A successful preflight verifies protocol conformance, CLI/TCK behavior, Python wheel installation outside the repository, canonical schema packaging, TypeScript build/tests, and package creation.

The repository deliberately does not contain registry credentials.
