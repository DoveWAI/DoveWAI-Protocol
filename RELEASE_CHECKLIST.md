# Release Acceptance Checklist

A public protocol release should satisfy all applicable checks before tagging or publishing packages.

- Normative schema parses as JSON Schema 2020-12.
- Packaged Python schema is semantically identical to the canonical `schemas/v0.2/core.schema.json`.
- Every valid conformance vector is accepted.
- Every invalid conformance vector is rejected.
- Lifecycle examples pass semantic validation.
- The black-box CLI TCK passes.
- Python SDK tests pass on a supported Python version.
- Python wheel and source distribution build successfully and pass metadata checks.
- The built Python wheel contains the canonical packaged v0.2 schema.
- The installed wheel runs `dovewai validate` outside the source repository.
- TypeScript SDK builds and tests pass on a supported Node.js version.
- `npm pack` succeeds and contains the intended public SDK files.
- Unknown adapter states fail closed.
- No credentials, customer data, private infrastructure details, or proprietary DoveWAI internals are present.
- Interoperability documentation names the external protocol versions it targets where version pinning is material.
- Changes are compatible with `VERSIONING.md` or the incompatibility is explicitly documented.
- Security-sensitive changes are reviewed for replay, lease/fencing, parser ambiguity, provenance spoofing, identifier confusion, secret leakage, and denial-of-service risk.
- README, CHANGELOG, examples, schemas, CLI version, and SDK package versions agree with the intended release.
- Registry publishing uses trusted publishing/OIDC when available instead of long-lived write tokens.
- GitHub release/tag creation is explicit and manual.

## Manual release automation

`.github/workflows/manual-v02-release.yml` is the release entry point. It is `workflow_dispatch` only and performs release preflight before any optional publishing action.

The workflow can independently:

- build and verify Python and npm artifacts;
- publish `dovewai-protocol` to PyPI after the PyPI trusted publisher is configured;
- publish `@dovewai/protocol` to npm after the npm trusted publisher is configured;
- create the GitHub `vVERSION` tag and release.

Publishing checkboxes default to **off**. Registry configuration is deliberately external to the repository and must be completed in the registry accounts before enabling the corresponding publish option.

GitHub Actions are not required by the protocol. Implementations may run equivalent checks locally or in another CI system.
