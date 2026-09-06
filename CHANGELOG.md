# Changelog

All notable protocol changes are recorded here.

## v0.2 — 2026-09-06

### Added

- New `Attempt` object for explicit retries, resume, and failover visibility.
- New `Artifact` object for durable outputs, evidence references, lineage, metadata, and digests.
- New `Verification` object for explicit independent assessments and outcomes.
- New `WorkReceipt` object for portable records linking requested work, execution, result, artifacts, and verification.
- `Task.idempotency_key` for duplicate-execution protection at the application-defined scope.
- Stronger Claim lease generation, fencing, renewal, revocation, and supersession fields.
- Attempt-aware and causal execution-event fields.
- Normative v0.2 JSON Schema.
- v0.2 lifecycle validator and positive/negative conformance vectors.
- Complete verified-work example bundle.
- Explicit v0.1-to-v0.2 migration guidance.
- Five-minute v0.2 quickstart.
- Python and TypeScript v0.2 builder surfaces.
- Public-independence rule requiring implementation and conformance from public protocol materials alone.
- Expanded interoperability guidance for MCP, A2A, CloudEvents, OpenTelemetry, provenance/attestation, identity, and policy systems.

### Changed

- v0.2 is the recommended version for new implementations.
- v0.1 is frozen as a compatibility line.
- `Result` is terminal-only in v0.2; intermediate or partial work belongs in events, checkpoints, or artifacts.
- Receipt and provenance semantics explicitly distinguish traceability from truth or trust.

### Compatibility

- v0.1 envelopes MUST NOT be silently reinterpreted as v0.2.
- Conversion between incompatible minor versions is explicit and should report lossy or indeterminate mappings.

### Validation status

- The v0.2 implementation is published as experimental. Full test execution and broader cross-language conformance validation are tracked as follow-up hardening work and are not implied by publication of this release line.

## v0.1

### Added

- DoveWAI Protocol v0.1 specification and normative JSON Schema.
- Conformance vectors and reference schema validator.
- Lifecycle semantic validator for cross-envelope consistency.
- Python reference SDK with builders, validation helpers, MCP result normalization, A2A task wrapping, and fail-closed A2A state mapping.
- TypeScript reference SDK with builders and pure MCP/A2A adapter helpers.
- Interoperability, versioning, governance, contribution, security, trademark, and roadmap documentation.
- Public repository architecture review documenting adopted design patterns.

### Security

- Credentials and authentication challenges are explicitly excluded from protocol payloads.
- Unknown source-protocol states are rejected rather than silently mapped.