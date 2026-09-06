# Roadmap

## v0.1 — frozen executable draft

- Normative JSON Schema for Task, Capability, Claim, ExecutionEvent, Result, Provenance, and ProtocolError.
- Positive and negative conformance vectors.
- Structural and lifecycle validators.
- Python and TypeScript reference SDKs.
- MCP, A2A, and OpenTelemetry interoperability guidance.
- Governance, contribution, security, trademark, versioning, and research-review documentation.

v0.1 remains available for compatibility. New features target v0.2 and later.

## v0.2 — current / recommended for new implementations

v0.2 establishes DoveWAI Protocol as a portable protocol for verifiable work.

Core work completed:

- Formalized lifecycle around Task, Claim, Attempt, Event, Artifact, Result, Verification, and WorkReceipt.
- Explicit Attempts for retry, failover, and resume visibility.
- Terminal-only Result semantics.
- First-class Artifact references and digests.
- First-class Verification records with explicit outcomes.
- Portable WorkReceipt tying work, evidence, and verification together.
- Idempotency guidance for duplicate execution prevention.
- Stronger lease generation/fencing semantics.
- Causal and attempt-aware execution events.
- Expanded structural and lifecycle conformance coverage.
- Explicit v0.1-to-v0.2 migration guidance.

Adoption work completed:

- Python and TypeScript v0.2 SDK surfaces.
- Five-minute quickstart and public adoption guide.
- Installable `dovewai` CLI with `validate`, `inspect`, and `receipt`.
- Machine-readable CLI output and stable exit codes.
- Shared schema + lifecycle validation path.
- Black-box CLI TCK and expanded conformance corpus.
- Public CloudEvents, OpenTelemetry, MCP, A2A, and signing/attestation profile guidance.
- CloudEvents profile example.
- Manual-only GitHub validation workflow covering protocol, SDK, CLI, and TCK checks.

Remaining v0.2 release operations:

- publish package artifacts to PyPI/npm only after an explicit release decision and successful release validation;
- create a signed/tagged public release when ready;
- collect external implementation feedback.

## v0.3 — ecosystem hardening

- Extension/profile registry process.
- Formal conformance report format and implementation matrix.
- Go and Rust SDKs or verified third-party implementations.
- Fuzz/property tests for parsers, extension handling, replay, and lifecycle invariants.
- Public security threat model and adversarial conformance corpus.
- Real integration feedback incorporated into compatibility rules.
- Optional richer inspector experience if real adopters need it.

## v1.0 criteria

The protocol will not be called stable until:

- independent implementations exchange the complete core lifecycle without DoveWAI-hosted infrastructure;
- published conformance fixtures are stable;
- at least two independently developed implementations interoperate on v1 candidate vectors;
- security review covers replay, leases/fencing, idempotency, provenance, artifacts, verification, receipts, parsers, and extension handling;
- compatibility/versioning rules have survived real integrations;
- implementation and conformance require only public DoveWAI Protocol materials.
