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

Core work:

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

Adoption work:

- Python and TypeScript v0.2 SDK surfaces.
- Five-minute quickstart.
- `validate`, `inspect`, and eventually `run` developer tooling.
- Reference MCP and A2A mappings kept outside normative core semantics.
- CloudEvents and OpenTelemetry profiles.
- Receipt signing/attestation profiles that compose established public standards rather than inventing new trust infrastructure.

## v0.3 — ecosystem hardening

- Extension/profile registry process.
- Technology Compatibility Kit and conformance report format.
- Compatibility corpus and independent implementation matrix.
- Go and Rust SDKs or verified third-party implementations.
- Fuzz/property tests for parsers, extension handling, replay, and lifecycle invariants.
- Public security threat model and adversarial conformance corpus.
- Real integration feedback incorporated into compatibility rules.

## v1.0 criteria

The protocol will not be called stable until:

- independent implementations exchange the complete core lifecycle without DoveWAI-hosted infrastructure;
- published conformance fixtures are stable;
- at least two independently developed implementations interoperate on v1 candidate vectors;
- security review covers replay, leases/fencing, idempotency, provenance, artifacts, verification, receipts, parsers, and extension handling;
- compatibility/versioning rules have survived real integrations;
- implementation and conformance require only public DoveWAI Protocol materials.
