# Interoperability

DoveWAI Protocol is designed to sit beside, not replace, existing agent and observability standards.

## Model Context Protocol (MCP)

MCP is the preferred boundary for exposing tools and context to model-driven applications. The 2026-07-28 MCP specification has a stateless core and moves long-running Tasks into the `io.modelcontextprotocol/tasks` extension.

DoveWAI Protocol does not redefine `tools/call`, MCP authorization, task polling, or MCP transport semantics. A DoveWAI `Task` may reference an MCP tool invocation as an execution mechanism. A DoveWAI `ExecutionEvent` may record MCP task-handle transitions. A DoveWAI `Result` may carry the normalized outcome plus provenance references.

Recommended mapping:

| DoveWAI | MCP |
| --- | --- |
| `Task.required_capabilities` | MCP advertised tool/extension capabilities |
| `Task.inputs` | `tools/call` arguments or application input |
| `Claim` | No direct MCP equivalent; local/distributed ownership contract |
| `ExecutionEvent` | MCP task status/update observations |
| `Result.outputs` | MCP final tool/task result normalized by the adapter |
| `Provenance` | References to MCP-visible resources/results where safe |

## Agent2Agent (A2A)

A2A 1.0 defines communication and task collaboration between independent agents. DoveWAI Protocol does not replace agent discovery, Agent Cards, A2A message exchange, or A2A transport/security behavior.

A DoveWAI adapter may treat an A2A task as an execution target. The adapter should preserve the A2A task identifier in an extension or provenance record and use DoveWAI objects for cross-runtime ownership, execution history, result normalization, and evidence lineage.

## OpenTelemetry

OpenTelemetry remains the telemetry system. DoveWAI Protocol objects are business/work envelopes, not spans or logs.

Implementations should emit OpenTelemetry traces and metrics using the applicable semantic conventions. Where useful, record DoveWAI identifiers as application attributes under an implementation-owned namespace such as `dovewai.task.id` and `dovewai.claim.id`. Do not place secrets or unrestricted task content in telemetry.

## Adapter rule

Adapters MUST preserve the semantics of the source protocol and MUST NOT claim that validation of a DoveWAI envelope validates the source MCP/A2A interaction, authorization decision, or telemetry record.

Adapters SHOULD preserve source identifiers and version information using provenance or namespaced extensions. Lossy conversions SHOULD emit a warning.