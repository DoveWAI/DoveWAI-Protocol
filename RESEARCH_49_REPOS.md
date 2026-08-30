# 49-Repository Design Review

Before declaring the v0.1 reference layer complete, DoveWAI reviewed more than 49 public repositories and current protocol projects across agent interoperability, MCP/A2A bridges, orchestration, schema distribution, SDKs, and conformance tooling.

This was a breadth-first architecture review, not a claim that every line of every repository was audited. The strongest patterns were then checked against the authoritative A2A/MCP/OpenTelemetry specifications where applicable.

## Representative projects reviewed

The review set included the A2A project and SDK ecosystem, LangChain Agent Protocol, Inference Gateway schemas/SDKs, A2A-MCP bridges, Python A2A implementations, agent protocol surveys, multi-agent orchestration projects, identity bridges, semantic-protocol experiments, and protocol-schema repositories. Search results were de-duplicated and more than 49 distinct repositories were considered.

## Patterns worth adopting

1. **One normative source of truth.** Schema repositories that feed SDKs, docs, CLIs, and generated artifacts reduce drift. DoveWAI keeps `schemas/v0.1/core.schema.json` normative for wire validation.
2. **Protocol boundaries must be explicit.** Mature projects avoid pretending that MCP, A2A, and application-level work contracts are the same thing. DoveWAI adapters preserve source identifiers and never claim source-protocol validation from envelope validation.
3. **Pure mapping code is easier to trust.** Bridge projects that isolate state translation from network I/O can test every mapping deterministically. DoveWAI adapters follow this pattern.
4. **Unknown states must not silently degrade.** Exhaustive mapping with explicit failure is safer than guessing. DoveWAI reference mapping functions reject unrecognized source states.
5. **Credentials are not task data.** Authentication challenges must stay outside model-fillable/task payload structures. DoveWAI security guidance forbids credentials in envelopes and adapters do not synthesize credential prompts.
6. **Long-running work needs resumability.** Stateless or externally durable task handles make failover safer. DoveWAI Claim/Lease plus source identifiers are designed so a runtime can recover without treating process memory as the protocol source of truth.
7. **Conformance vectors matter more than prose alone.** Positive and negative fixtures make independent implementations testable.
8. **Version headers and source versions should be preserved.** Adapters should record the source protocol version/identifier rather than silently normalize it away.
9. **SDK parity matters.** A protocol intended for broad adoption needs at least Python and TypeScript reference surfaces early.
10. **Schema validation is not semantic/lifecycle validation.** A structurally valid Claim can still be expired or inconsistent with a Task. DoveWAI therefore separates wire/schema validation from multi-envelope lifecycle validation.

## DoveWAI differentiation after the review

DoveWAI Protocol does not try to become another agent communication or tool invocation protocol. Its narrow role is the durable execution contract around heterogeneous systems:

`Task -> Capability -> Claim/Lease -> ExecutionEvent -> Result -> Provenance/Error`

The distinctive areas are cross-runtime work ownership, lease semantics, portable execution history, outcome normalization, and provenance/evidence lineage. MCP and A2A remain execution/communication targets rather than dependencies of the core protocol.

## Deliberate exclusions

The public protocol does not contain DoveWAI private orchestration internals, customer data, private ranking/scoring, infrastructure credentials, or Automation Fabric implementation details. It also does not define authentication, authorization, transport security, model APIs, or telemetry transports.
