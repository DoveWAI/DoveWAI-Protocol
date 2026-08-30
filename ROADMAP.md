# Roadmap

## v0.1 — executable draft

- Normative JSON Schema for Task, Capability, Claim, ExecutionEvent, Result, Provenance, and ProtocolError.
- Positive and negative conformance vectors.
- Structural and lifecycle validators.
- Python and TypeScript reference SDKs.
- MCP, A2A, and OpenTelemetry interoperability guidance.
- Governance, contribution, security, trademark, versioning, and research-review documentation.

## v0.2 — interoperability hardening

- More conformance vectors for every core object.
- Explicit source-protocol version fields in adapter extension profiles.
- Capability negotiation examples.
- Lease renewal/fencing guidance and stale-claim examples.
- Provenance profile for digests, immutable artifacts, and evidence references.
- Cross-language golden-vector tests.

## v0.3 — ecosystem readiness

- Extension registry process.
- Reference MCP and A2A adapter packages kept outside the normative core when practical.
- Conformance report format for third-party implementations.
- Compatibility test corpus and implementation matrix.

## v1.0 criteria

The protocol will not be called stable until independent implementations can exchange the complete core lifecycle without DoveWAI-hosted infrastructure, published conformance fixtures are stable, security review has covered replay/lease/provenance/parser risks, and compatibility/versioning rules have survived real integration feedback.
