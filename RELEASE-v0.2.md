# DoveWAI Protocol v0.2 Release Readiness

v0.2 is implemented and recommended for new integrations, but package publication and a formal tagged release are separate release operations.

## Ready

- normative v0.2 specification and JSON Schema;
- migration guidance from v0.1;
- Python and TypeScript reference SDK surfaces;
- installable Python CLI;
- schema + lifecycle validation;
- black-box CLI TCK and conformance vectors;
- WorkReceipt examples;
- public interoperability profiles;
- manual-only GitHub validation workflow.

## Before publishing packages or tagging a formal release

1. Run `Manual v0.2 Validation` on the exact release commit and require all jobs to pass.
2. Build Python wheel/sdist and TypeScript package artifacts from the exact commit.
3. Inspect package contents so schemas, code, license, and docs are present as intended and private/internal material is absent.
4. Confirm package names and publishing ownership on PyPI/npm.
5. Publish only from an explicitly approved release operation.
6. Record immutable tag, release notes, hashes, and any external signature/attestation references.

Package version fields in source do not mean those packages have been published.

## Trust

Use established signing and attestation standards for release artifacts. Do not invent DoveWAI-specific cryptography.
