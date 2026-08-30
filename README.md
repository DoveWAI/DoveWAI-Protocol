# DoveWAI Protocol

DoveWAI Protocol is an open interoperability protocol for reliable AI work across agents, tools, runtimes, people, and services.

It defines a small, vendor-neutral work lifecycle:

`Task -> Capability -> Claim/Lease -> Execution Event -> Result -> Provenance/Error`

The protocol is designed to complement existing standards rather than replace them. MCP can expose tools and context, A2A can connect independent agents, and OpenTelemetry can carry telemetry. DoveWAI Protocol focuses on the durable work contract around execution: what was requested, who or what claimed it, what happened, what result was produced, and how that result can be traced.

## Goals

- Portable task and result envelopes across runtimes and vendors.
- Explicit capability requirements and offers.
- Safe claim/lease semantics for distributed workers.
- Structured execution events and failure states.
- First-class provenance and evidence references.
- Compatibility with existing agent, tool, and observability standards.
- Small schemas that can be implemented without DoveWAI Cloud.

## Non-goals

- Replacing MCP tool invocation.
- Replacing A2A agent-to-agent communication.
- Defining a model provider API.
- Requiring DoveWAI-hosted infrastructure.
- Exposing DoveWAI private orchestration, customer data, ranking systems, or internal automation.

## v0.1

The initial specification lives in [`spec/v0.1/SPEC.md`](spec/v0.1/SPEC.md), with the normative JSON Schema in [`schemas/v0.1/core.schema.json`](schemas/v0.1/core.schema.json).

The v0.1 work objects are:

- `Task`
- `Capability`
- `Claim`
- `ExecutionEvent`
- `Result`
- `Provenance`
- `ProtocolError`

## Reference SDKs

Two small reference SDK surfaces live in this repository:

- [`sdk/python`](sdk/python) — Python builders, schema validation, MCP result normalization, A2A task wrapping, and fail-closed A2A state mapping.
- [`sdk/typescript`](sdk/typescript) — TypeScript builders, MCP/A2A adapters, and fail-closed A2A state mapping.

The SDKs are intentionally thin. They do not require DoveWAI Cloud and they do not hide the underlying protocol objects.

## Conformance

Reference conformance vectors live in [`conformance/v0.1`](conformance/v0.1). Structural validation and lifecycle validation are separate on purpose.

```bash
python -m pip install -r requirements-dev.txt
python tools/validate.py conformance/v0.1/valid/task.json
pytest -q
```

`tools/validate.py` checks one envelope against the normative JSON Schema. `tools/lifecycle_validate.py` checks relationships across a bundle, including task references, lease timing, execution-event ordering, and duplicate terminal results.

Valid vectors must pass the published v0.1 JSON Schema. Invalid vectors must be rejected. Conformance to a DoveWAI envelope does not imply conformance to any underlying MCP, A2A, provider, transport, authorization, or telemetry protocol.

## Interoperability

See [`INTEROPERABILITY.md`](INTEROPERABILITY.md) for mapping boundaries with MCP, A2A, and OpenTelemetry, and [`VERSIONING.md`](VERSIONING.md) for protocol-version and extension rules.

The adapters preserve source identifiers and fail closed on unknown A2A states rather than silently guessing. Credential or authentication challenges must remain outside model-fillable task data.

## Design review

The v0.1 implementation layer was informed by a breadth-first review of more than 49 public repositories across protocol, bridge, SDK, orchestration, schema, and conformance projects. The resulting design lessons are recorded in [`RESEARCH_49_REPOS.md`](RESEARCH_49_REPOS.md). This is a repository-level architecture review, not a claim that every line of every project was audited.

## Design principles

DoveWAI Protocol uses explicit versioning, globally unique identifiers, UTC timestamps, conservative extensibility, deterministic validation, least-authority claims, fail-closed mappings, and provenance that can point to external evidence without embedding secrets.

## Status

**Experimental / v0.1 draft.** The schema may change before the first stable release. The repository contains the specification, normative schema, conformance vectors, lifecycle validator, Python reference SDK, TypeScript reference SDK, interoperability guidance, governance, security policy, and project licensing/trademark material.

## License

Apache License 2.0. The DoveWAI name and marks are not granted by the software license; see [`TRADEMARKS.md`](TRADEMARKS.md).
