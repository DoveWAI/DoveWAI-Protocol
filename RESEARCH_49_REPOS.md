# Public Protocol Design Review

DoveWAI Protocol has been informed by a breadth-first review of more than 49 public repositories and current protocol projects across agent interoperability, MCP/A2A bridges, orchestration, schema distribution, SDKs, conformance tooling, event envelopes, observability, provenance, attestation, workload identity, policy engines, and data lineage.

This is an architecture review, not a claim that every line of every referenced project was audited. Design patterns are checked against authoritative public specifications where applicable.

## Patterns worth adopting

1. **One normative source of truth.** Schema and model definitions should drive SDKs, docs, CLIs, fixtures, and generated artifacts to reduce drift.
2. **Protocol boundaries must be explicit.** MCP, A2A, CloudEvents, OpenTelemetry, signing/attestation systems, identity systems, and application-level work contracts solve different problems.
3. **Pure mapping code is easier to trust.** State translation should be isolated from network I/O where practical so mappings can be evaluated deterministically.
4. **Unknown states must not silently degrade.** Unrecognized external states must not be guessed into success or another known state.
5. **Credentials are not task data.** Authentication challenges and secrets belong outside model-fillable work payloads.
6. **Long-running work needs explicit execution identity.** Retries, resume, and failover should be visible as Attempts rather than hidden inside a final result.
7. **Conformance vectors matter more than prose alone.** Positive and negative fixtures make independent implementations comparable.
8. **Versions and source identifiers should be preserved.** Adapters should retain source protocol versions and identifiers rather than silently normalizing them away.
9. **SDK parity matters.** Broad adoption requires consistent semantics across common implementation languages.
10. **Schema validation is not lifecycle validation.** A structurally valid envelope can still reference unknown work, use an expired lease, duplicate a terminal result, or claim verification without supporting evidence.
11. **Evidence is not correctness.** Digests, provenance, signatures, attestations, and receipts improve traceability but do not automatically prove truth.
12. **Extensibility must be exercised.** Unknown optional extensions and future protocol values should be handled deliberately so extension points do not ossify.

## DoveWAI Protocol differentiation

DoveWAI Protocol does not try to become another agent communication, tool invocation, transport, telemetry, authentication, or signing protocol. Its narrow role is a durable, portable execution and verification contract around heterogeneous work:

`Task -> Capability -> Claim/Lease -> Attempt -> ExecutionEvent/Artifact -> Result -> Verification -> WorkReceipt`

The distinctive areas are cross-runtime work ownership, explicit retries/attempts, stale-writer protection, artifact/evidence lineage, independent verification records, and portable work receipts. MCP, A2A, CloudEvents, OpenTelemetry, in-toto/Sigstore, SPIFFE, policy engines, and other public standards may be composed through adapters, bindings, or profiles rather than becoming private dependencies of the core protocol.

## Public-independence rule

The public protocol specification, schemas, conformance materials, examples, migration guidance, SDKs, bindings, and profiles must be implementable using public materials alone.

The protocol does not expose or depend on proprietary implementation internals, private repositories, customer data, private ranking/scoring, infrastructure credentials, or non-public orchestration details. It also does not define authentication, authorization, transport security, model-provider APIs, or telemetry transports.