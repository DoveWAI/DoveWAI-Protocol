# Versioning and Extensions

## Versioning

DoveWAI Protocol uses explicit protocol versions carried by every core envelope.

During the `0.x` experimental series, incompatible changes MAY occur between minor versions. A published `0.x` schema is immutable once tagged. Implementations MUST validate against the schema identified by `protocol_version` and MUST NOT silently reinterpret an older envelope as a newer version.

A future `1.x` line will use semantic-versioning-style compatibility rules: additive compatible changes within a major line and explicit major-version changes for incompatible wire/schema semantics.

## Extensions

Core envelopes expose an `extensions` object for vendor-, deployment-, and domain-specific data.

Extension keys SHOULD use a reverse-DNS or similarly collision-resistant namespace, for example:

- `com.example.scheduler`
- `org.example.audit`
- `ai.dovewai.reference-runtime`

The namespaces `dovewai.*` and `ai.dovewai.*` are reserved for DoveWAI-published extensions.

Extensions MUST NOT change the meaning of required core fields. A recipient that does not understand an extension SHOULD be able to ignore it unless the sender explicitly declares the extension as required through an application-level capability contract.

## Compatibility rule

A feature belongs in core only when independent implementations need the same semantics to interoperate. Experimental, provider-specific, deployment-specific, or policy-specific behavior should begin as an extension.

## Registry

The project may introduce an extension registry later. Registration will document identifiers and interoperability expectations; it will not transfer ownership of third-party implementations or trademarks.