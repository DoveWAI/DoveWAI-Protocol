# Changelog

All notable protocol changes are recorded here.

## Unreleased

### Added

- DoveWAI Protocol v0.1 specification and normative JSON Schema.
- Conformance vectors and reference schema validator.
- Lifecycle semantic validator for cross-envelope consistency.
- Python reference SDK with builders, validation helpers, MCP result normalization, A2A task wrapping, and fail-closed A2A state mapping.
- TypeScript reference SDK with builders and pure MCP/A2A adapter helpers.
- Interoperability, versioning, governance, contribution, security, trademark, and roadmap documentation.
- 49+ repository architecture review documenting adopted design patterns.

### Security

- Credentials and authentication challenges are explicitly excluded from protocol payloads.
- Unknown source-protocol states are rejected rather than silently mapped.
