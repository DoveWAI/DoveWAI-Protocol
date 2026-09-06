# DoveWAI Protocol

DoveWAI Protocol is an open, vendor-neutral protocol for verifiable AI and automated work across agents, tools, runtimes, people, and services.

It defines a durable work lifecycle that records what was requested, who or what accepted responsibility, what execution actually occurred, what artifacts were produced, how the outcome was verified, and what portable receipt can be independently inspected.

## Current recommended version

**DoveWAI Protocol v0.2 is the recommended version for all new implementations.**

The v0.2 lifecycle is:

`Task -> Capability -> Claim/Lease -> Attempt -> ExecutionEvent/Artifact -> Result -> Verification -> WorkReceipt`

v0.1 remains published for compatibility and must not be silently reinterpreted as v0.2. See [`migration/v0.1-to-v0.2.md`](migration/v0.1-to-v0.2.md).

## Try it

Install the Python reference package from this repository:

```bash
python -m pip install ./sdk/python
```

Then validate and inspect the public example:

```bash
dovewai validate examples/v0.2/verified-work-bundle.json
dovewai inspect examples/v0.2/verified-work-bundle.json
dovewai receipt examples/v0.2/verified-work-bundle.json
```

See [`ADOPTION.md`](ADOPTION.md), [`CLI.md`](CLI.md), and [`QUICKSTART-v0.2.md`](QUICKSTART-v0.2.md).

## Why DoveWAI Protocol exists

MCP can expose tools and context. A2A can connect independent agents. CloudEvents can carry event envelopes. OpenTelemetry can carry telemetry. DoveWAI Protocol complements those standards by defining a transport-neutral, portable work contract around execution and verification.

A conforming implementation can answer:

- What work was requested?
- What capabilities were required or offered?
- Who or what held the active claim or lease?
- Which execution attempt produced the outcome?
- Which events and artifacts were produced?
- What terminal result was declared?
- What verification was performed, by whom, and with what outcome?
- What portable receipt ties the work and evidence together?

## Public and independent by design

The public DoveWAI Protocol specification, schemas, conformance tests, reference SDKs, profiles, examples, and migration guidance MUST NOT require access to non-public DoveWAI software or documentation for implementation or conformance.

The protocol does not require DoveWAI-hosted infrastructure.

## v0.2 core objects

The v0.2 specification lives in [`spec/v0.2/SPEC.md`](spec/v0.2/SPEC.md), with its normative JSON Schema in [`schemas/v0.2/core.schema.json`](schemas/v0.2/core.schema.json).

Core objects are `Task`, `Capability`, `Claim`, `Attempt`, `ExecutionEvent`, `Artifact`, `Result`, `Verification`, `WorkReceipt`, `Provenance`, and `ProtocolError`.

`Result` is terminal in v0.2. Intermediate progress or partial output belongs in execution events, checkpoints, or artifacts.

## Reference SDKs and CLI

Reference SDK surfaces live in:

- [`sdk/python`](sdk/python)
- [`sdk/typescript`](sdk/typescript)

The Python package also exposes the `dovewai` CLI. The SDKs remain intentionally thin and expose the underlying protocol objects directly.

## Conformance

Reference vectors and the black-box TCK live under [`conformance`](conformance). v0.2 conformance covers schema validity and cross-object lifecycle semantics including task references, claims, attempts, event ordering, terminal-result rules, verification references, and WorkReceipt integrity.

## Interoperability profiles

See [`profiles/v0.2/README.md`](profiles/v0.2/README.md) for CloudEvents, OpenTelemetry, MCP, A2A, and signing/attestation composition guidance. Profiles are optional and do not change core v0.2 semantics.

DoveWAI Protocol does not replace MCP tool invocation, A2A agent communication, model-provider APIs, authentication systems, transports, telemetry systems, or supply-chain signing systems.

## Design principles

DoveWAI Protocol uses explicit versioning, globally unique identifiers, UTC timestamps, deterministic validation, least-authority claims, explicit attempts, terminal results, independent verification records, evidence references, conservative extensibility, and fail-closed behavior where ambiguity would create unsafe interoperability.

A receipt records what happened and what verification was performed. A receipt is not, by itself, a declaration that every underlying claim is true.

## Version status

- **v0.2 — current / recommended for new implementations**
- **v0.1 — frozen compatibility line**

The `0.x` series remains experimental and may contain incompatible changes between minor versions. Published versioned schemas remain immutable once tagged.

## License

Apache License 2.0. The DoveWAI name and marks are not granted by the software license; see [`TRADEMARKS.md`](TRADEMARKS.md).
