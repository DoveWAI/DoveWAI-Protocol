# Security Policy

DoveWAI Protocol is a data contract, not an authentication or authorization system. Implementers remain responsible for transport security, identity, authorization, secret handling, sandboxing, policy enforcement, and safe execution.

## Security requirements

Protocol objects must not be treated as trusted merely because they validate against a schema. Implementations should validate size, identifiers, timestamps, URIs, extension namespaces, referenced artifacts, and all untrusted payload content before use.

Claims coordinate work ownership; they do not grant permission to access a resource. Provenance records lineage; it does not establish correctness or trustworthiness.

Do not place passwords, API keys, bearer tokens, private keys, session cookies, customer secrets, or other credentials inside protocol envelopes, examples, issues, or pull requests.

## Reporting vulnerabilities

Please use GitHub's private security reporting mechanism when enabled. Do not publish an exploitable vulnerability in a public issue before maintainers have had a reasonable opportunity to assess it.

## Scope

Security reports may include schema ambiguity that creates unsafe behavior, replay/lease weaknesses, identifier confusion, parser differential issues, provenance spoofing, extension namespace collisions, denial-of-service risks, or unsafe reference handling.
