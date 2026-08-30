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

The initial specification lives in [`spec/v0.1/SPEC.md`](spec/v0.1/SPEC.md), with JSON Schema definitions in [`schemas/v0.1`](schemas/v0.1).

The v0.1 work objects are:

- `Task`
- `Capability`
- `Claim`
- `ExecutionEvent`
- `Result`
- `Provenance`
- `ProtocolError`

## Design principles

DoveWAI Protocol uses explicit versioning, globally unique identifiers, UTC timestamps, conservative extensibility, deterministic validation, least-authority claims, and provenance that can point to external evidence without embedding secrets.

## Status

**Experimental / v0.1 draft.** The schema may change before the first stable release.

## License

Apache License 2.0. The DoveWAI name and marks are not granted by the software license; see [`TRADEMARKS.md`](TRADEMARKS.md).
