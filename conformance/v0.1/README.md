# DoveWAI Protocol v0.1 Conformance

This directory contains machine-readable examples used to verify protocol implementations.

- `valid/`: envelopes that MUST validate against the v0.1 core schema.
- `invalid/`: envelopes that MUST be rejected by a conforming v0.1 schema validator.

A conforming implementation SHOULD produce deterministic validation outcomes for these vectors. Additional implementation behavior, authorization, transport, execution safety, and source-protocol correctness are outside schema conformance.

Contributors adding or changing a core field SHOULD add both a positive and a negative vector covering the behavior.