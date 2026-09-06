# Versioning and Extensions

## Versioning

DoveWAI Protocol uses explicit protocol versions carried by every core envelope.

During the `0.x` experimental series, incompatible changes MAY occur between minor versions. A published `0.x` schema is immutable once tagged. Implementations MUST validate against the schema identified by `protocol_version` and MUST NOT silently reinterpret an older envelope as a newer version.

**v0.2 is the current recommended protocol version for new implementations. v0.1 is a frozen compatibility line.**

Conversion between incompatible minor versions MUST be explicit. A converter SHOULD preserve source identifiers and MUST report mappings that are lossy or indeterminate rather than inventing semantics.

A future `1.x` line will use semantic-versioning-style compatibility rules: additive compatible changes within a major line and explicit major-version changes for incompatible wire/schema semantics.

## Current-version discovery

Repository documentation and quickstarts SHOULD direct new implementations to the current recommended version. Versioned specifications, schemas, examples, and conformance fixtures remain addressable by their explicit version paths.

Implementations that accept more than one protocol version MUST route by `protocol_version` before applying version-specific schema or lifecycle interpretation.

## Extensions

Core envelopes expose an `extensions` object for vendor-, deployment-, and domain-specific data.

Extension keys SHOULD use a reverse-DNS or similarly collision-resistant namespace, for example:

- `com.example.scheduler`
- `org.example.audit`
- `ai.dovewai.reference-runtime`

The namespaces `dovewai.*` and `ai.dovewai.*` are reserved for DoveWAI-published extensions.

Extensions MUST NOT change the meaning of required core fields. A recipient that does not understand an optional extension SHOULD be able to ignore it. Unsupported required profiles or extensions MUST fail explicitly rather than being silently treated as supported.

## Compatibility rule

A feature belongs in core only when independent implementations need the same semantics to interoperate. Experimental, provider-specific, deployment-specific, transport-specific, signing-specific, or policy-specific behavior should begin as an extension, binding, or profile.

## Public independence rule

The public DoveWAI Protocol specification, schemas, conformance tests, reference SDKs, profiles, examples, and migration documentation MUST NOT require access to non-public DoveWAI software or documentation for implementation or conformance.

## Registry

The project may introduce an extension/profile registry. Registration will document identifiers and interoperability expectations; it will not transfer ownership of third-party implementations or trademarks.
