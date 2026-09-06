# Interoperability

DoveWAI Protocol is designed to sit beside, not replace, existing agent, event, observability, identity, policy, and attestation standards.

## Model Context Protocol (MCP)

MCP exposes tools, context, resources, prompts, and related model-facing capabilities. DoveWAI Protocol does not redefine MCP tool invocation, authorization, task polling, or transport semantics.

A DoveWAI `Task` may reference an MCP tool invocation as an execution mechanism. An `Attempt` can represent one concrete execution try. `ExecutionEvent` can record task/status transitions. Durable MCP-visible outputs can be represented as `Artifact` references. The normalized terminal outcome becomes a DoveWAI `Result`; independent checking becomes `Verification`; and the overall record can be summarized in a `WorkReceipt`.

Recommended mapping:

| DoveWAI v0.2 | MCP |
| --- | --- |
| `Task.required_capabilities` | advertised MCP tool/extension capabilities |
| `Task.inputs` | `tools/call` arguments or application input |
| `Claim` | no direct MCP equivalent; ownership/lease contract |
| `Attempt` | one concrete MCP-backed execution try |
| `ExecutionEvent` | MCP task status/update observations |
| `Artifact` | durable referenced outputs/resources where applicable |
| `Result.outputs` | normalized final MCP result |
| `Verification` | external assessment of result/artifact/work |
| `WorkReceipt` | portable record linking execution and verification |

## Agent2Agent (A2A)

A2A defines communication and task collaboration between independent agents. DoveWAI Protocol does not replace discovery, Agent Cards, A2A messages, transport, or security behavior.

A DoveWAI adapter may treat an A2A task as an execution target. It should preserve A2A task/context identifiers and source-version information through provenance or namespaced extensions. DoveWAI objects then describe cross-runtime ownership, attempts, normalized execution history, artifacts, terminal result, independent verification, and receipt generation.

## CloudEvents

CloudEvents provides a standard event envelope. DoveWAI Protocol does not replace it.

A binding may carry a DoveWAI `ExecutionEvent` or another DoveWAI envelope inside CloudEvents while preserving CloudEvents `id`, `source`, `specversion`, and `type` semantics. DoveWAI identifiers and CloudEvents identifiers should not be silently treated as interchangeable unless a binding explicitly defines that relationship.

## OpenTelemetry

OpenTelemetry remains the telemetry system. DoveWAI Protocol objects are work envelopes, not spans, logs, or metrics.

Implementations may correlate telemetry with identifiers such as `dovewai.task.id`, `dovewai.attempt.id`, `dovewai.claim.id`, `dovewai.verification.id`, and `dovewai.receipt.id`. Sensitive task content and secrets should not be copied into telemetry merely for correlation.

## Provenance, attestation, and signatures

DoveWAI `Artifact`, `Verification`, and `WorkReceipt` objects may reference public provenance, attestation, or signature systems. Profiles may compose standards such as in-toto, SLSA-compatible provenance, DSSE, or Sigstore.

The core protocol does not invent a PKI or declare a signature trustworthy solely because it exists.

## Identity

Actor identifiers such as claim holders, executors, verifiers, and receipt issuers are identifiers, not credentials. Profiles may use public identity systems such as SPIFFE or other URI-based identifiers. Authentication and authorization remain outside the core protocol.

## Policy engines

A `Verification` may carry a `policy_decision_ref` to an external policy decision. The protocol may reference decisions from systems such as OPA or Cedar without embedding or redefining their authorization semantics.

## Adapter rule

Adapters MUST preserve the semantics of the source protocol and MUST NOT claim that validation of a DoveWAI envelope validates the source MCP/A2A interaction, authorization decision, telemetry record, signature, or external policy decision.

Adapters SHOULD preserve source identifiers and version information using provenance or namespaced extensions. Lossy conversions SHOULD emit a warning or explicit indeterminate outcome rather than inventing semantics.