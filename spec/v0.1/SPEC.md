# DoveWAI Protocol v0.1 Draft

Status: Experimental

## 1. Scope

DoveWAI Protocol defines interoperable envelopes for reliable work across agents, runtimes, tools, people, and services. It does not define transport. Implementations MAY carry these objects over HTTP, queues, files, A2A, MCP-adjacent integrations, local IPC, or other transports.

## 2. Core lifecycle

A conforming implementation models work as:

`Task -> Capability -> Claim/Lease -> ExecutionEvent* -> Result | ProtocolError`

`Provenance` MAY be attached to tasks, events, results, and errors.

## 3. Common rules

All protocol objects MUST include:

- `protocol_version`: currently `0.1`
- `id`: globally unique string
- `type`: object type identifier
- `created_at`: RFC 3339 UTC timestamp

Unknown extension fields SHOULD be preserved when relaying objects. Implementations MUST NOT place credentials, access tokens, private keys, or raw secrets in protocol objects.

## 4. Task

A Task expresses requested work, not a specific implementation.

Required fields:

- `protocol_version`
- `id`
- `type = "task"`
- `created_at`
- `intent`: concise description of the desired outcome

Optional fields include `inputs`, `required_capabilities`, `constraints`, `deadline`, `correlation_id`, `parent_task_id`, and `provenance`.

## 5. Capability

A Capability describes work an executor can perform.

Required fields:

- `protocol_version`
- `id`
- `type = "capability"`
- `created_at`
- `name`
- `version`

Capabilities SHOULD describe accepted inputs, produced outputs, limits, and implementation-neutral feature labels. Capability identifiers SHOULD remain stable across compatible executor implementations.

## 6. Claim / lease

A Claim coordinates exclusive or shared execution responsibility for a task or scope.

Required fields:

- `protocol_version`
- `id`
- `type = "claim"`
- `created_at`
- `task_id`
- `holder_id`
- `mode`: `read` or `write`
- `lease_expires_at`

A claim MUST expire unless explicitly renewed. Implementations MUST treat an expired claim as inactive. A holder SHOULD renew before expiry when work continues. Systems MAY add fencing tokens or monotonic lease generations for stronger distributed-write guarantees.

## 7. ExecutionEvent

ExecutionEvent records an immutable observation in task execution.

Required fields:

- `protocol_version`
- `id`
- `type = "execution_event"`
- `created_at`
- `task_id`
- `event_type`

Recommended event types include `accepted`, `started`, `progress`, `tool_call`, `checkpoint`, `warning`, `completed`, `failed`, and `cancelled`.

Event payloads SHOULD reference sensitive external artifacts rather than embedding their contents.

## 8. Result

Result records the terminal or partial output of work.

Required fields:

- `protocol_version`
- `id`
- `type = "result"`
- `created_at`
- `task_id`
- `status`: `succeeded`, `partial`, `failed`, or `cancelled`

A successful or partial result SHOULD include an `outputs` object. Results MAY include metrics, evidence references, provenance, and warnings.

## 9. Provenance

Provenance describes where information or artifacts came from and how they were transformed.

A provenance entry SHOULD include a source identifier or URI, acquisition time when relevant, optional digest, optional media/type information, and transformation metadata. Implementations SHOULD use cryptographic digests for immutable artifacts when practical.

Provenance MUST NOT imply trust merely because a source is recorded. Trust policy belongs to the receiving implementation.

## 10. ProtocolError

ProtocolError represents interoperable failure information.

Required fields:

- `protocol_version`
- `id`
- `type = "error"`
- `created_at`
- `code`
- `message`

Errors MAY include `task_id`, `retryable`, `details`, and provenance. Error details MUST avoid secrets.

## 11. Extensions

Vendor or domain extensions MUST use namespaced keys under `extensions`, for example:

```json
{
  "extensions": {
    "com.example.feature": {
      "value": true
    }
  }
}
```

Core field meanings MUST NOT be changed by extensions.

## 12. Compatibility

DoveWAI Protocol intentionally does not duplicate transport-level agent or tool protocols. Adapters MAY map DoveWAI objects onto A2A tasks/messages, MCP task/tool flows, event buses, or local runtimes. Telemetry exporters SHOULD map execution information to OpenTelemetry semantic conventions where an appropriate stable or experimental convention exists.

## 13. Versioning

`0.x` versions are experimental. Breaking schema changes MAY occur between minor versions before `1.0`. Once `1.0` is published, incompatible changes require a new major protocol version.

A receiver MUST reject an unsupported major version and SHOULD return a structured `ProtocolError`.

## 14. Security baseline

Implementations MUST authenticate and authorize at the transport or host layer where required. Claims are coordination objects, not authorization credentials. Provenance is evidence metadata, not proof of correctness. Implementations SHOULD validate object size, schema, identifiers, timestamps, URIs, and extension namespaces before processing untrusted input.
