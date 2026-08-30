# Release Acceptance Checklist

A public protocol release should satisfy all applicable checks before tagging.

- Normative schema parses as JSON Schema 2020-12.
- Every valid conformance vector is accepted.
- Every invalid conformance vector is rejected.
- Lifecycle examples pass semantic validation.
- Python SDK tests pass on a supported Python version.
- TypeScript SDK builds and tests pass on a supported Node.js version.
- Unknown adapter states fail closed.
- No credentials, customer data, private infrastructure details, or proprietary DoveWAI internals are present.
- Interoperability documentation names the external protocol versions it targets.
- Changes are compatible with `VERSIONING.md` or the incompatibility is explicitly documented.
- Security-sensitive changes are reviewed for replay, lease/fencing, parser ambiguity, provenance spoofing, identifier confusion, secret leakage, and denial-of-service risk.
- README, CHANGELOG, examples, and SDK versions agree with the intended release.
- Release commit is reviewed and the work-presence claim is released after promotion.

GitHub Actions are not required by the protocol. Projects may run these checks locally, in an external CI system, or through explicitly invoked automation.
