# DoveWAI Protocol v0.2 Adoption Guide

This guide is for implementers who want to adopt DoveWAI Protocol without depending on any non-public DoveWAI software.

## Five-minute path

1. Install the Python reference package from this repository.
2. Validate an example bundle with `dovewai validate examples/v0.2/verified-work-bundle.json`.
3. Inspect it with `dovewai inspect examples/v0.2/verified-work-bundle.json`.
4. Extract its receipt with `dovewai receipt examples/v0.2/verified-work-bundle.json`.
5. Run the black-box TCK in `conformance/v0.2/tck_cli.py`.

## Minimum viable implementation

A minimal v0.2 implementation should be able to create and consume `Task`, `Result`, `Verification`, and `WorkReceipt` objects; preserve identifiers and timestamps; validate against the canonical v0.2 JSON Schema; enforce bundle lifecycle invariants; and reject unsupported required extensions rather than guessing.

Implementations that execute work should additionally model `Claim`, `Attempt`, `ExecutionEvent`, and `Artifact`.

## Adoption levels

### Level 1: Reader

Can parse and validate v0.2 objects and bundles.

### Level 2: Producer

Can create schema-valid v0.2 objects and portable WorkReceipts.

### Level 3: Conformant lifecycle implementation

Passes the public v0.2 TCK and lifecycle vectors.

### Level 4: Interoperable implementation

Implements one or more public profiles, such as CloudEvents, OpenTelemetry, MCP/A2A mapping, or signature/attestation integration.

## Compatibility rule

Do not silently reinterpret v0.1 as v0.2. Mixed-version systems must route by `protocol_version` and use explicit conversion when needed.

## Verification rule

A WorkReceipt is a portable record, not automatic proof of truth. Consumers should evaluate verifier identity, method, evidence, policy, signatures, and trust anchors according to their own security model.

## Public-only rule

Conformance, examples, SDKs, profiles, schemas, documentation, and tooling in this repository must remain usable without access to any private DoveWAI repository or service.
