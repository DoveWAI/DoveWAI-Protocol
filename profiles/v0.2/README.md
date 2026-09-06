# DoveWAI Protocol v0.2 Profiles

Profiles describe how DoveWAI Protocol composes with external public standards without changing core v0.2 semantics.

Profiles are optional. A core implementation does not need any profile to be conformant.

## CloudEvents profile

Use CloudEvents as a transport/event envelope for DoveWAI `ExecutionEvent` or other protocol records. Preserve the complete DoveWAI object as event data. Recommended mapping:

- CloudEvents `id` <- DoveWAI object `id`
- CloudEvents `time` <- DoveWAI `created_at` or `occurred_at`
- CloudEvents `type` <- `org.dovewai.protocol.v0_2.<ObjectType>`
- CloudEvents `source` <- URI identifying the producing system
- CloudEvents `subject` <- `task_id` when applicable
- CloudEvents `datacontenttype` <- `application/json`
- CloudEvents `data` <- complete DoveWAI object

Do not discard DoveWAI fields merely because equivalent CloudEvents attributes exist.

## OpenTelemetry profile

DoveWAI identifiers may be attached to traces, spans, logs, and metrics as correlation attributes. Recommended attributes:

- `dovewai.protocol.version`
- `dovewai.task.id`
- `dovewai.claim.id`
- `dovewai.attempt.id`
- `dovewai.result.id`
- `dovewai.verification.id`
- `dovewai.receipt.id`

OpenTelemetry remains observability data; it does not replace protocol objects or verification records.

## MCP profile

MCP may expose a tool or resource that creates, returns, stores, validates, or retrieves DoveWAI protocol objects. A tool invocation can be represented as an `Attempt`; tool outputs can become `Artifact` or `Result`; independent validation can create `Verification`; the portable outcome can be summarized by a `WorkReceipt`.

The profile does not redefine MCP messages and does not require MCP implementations to understand DoveWAI unless they explicitly opt in.

## A2A profile

A2A agent tasks can be mapped to DoveWAI `Task` and execution attempts. Agent-produced deliverables can be represented as `Artifact`; terminal A2A task state can contribute to a DoveWAI `Result`; an independent verifier may issue `Verification`; the cross-system record is a `WorkReceipt`.

Mappings must preserve the original A2A identifiers in extensions or correlation fields when lossless round-tripping matters.

## Signing and attestation profile

DoveWAI does not define custom cryptography. A WorkReceipt or other canonicalized protocol object may be signed as a blob using an established signing system such as Sigstore/Cosign, or embedded as the predicate of an in-toto attestation. `signature_ref` should point to the externally verifiable signature or attestation material.

A valid signature proves integrity and signer control according to that signing system. It does not automatically prove that the underlying work or verification claim is correct.

## Profile rule

Profiles MUST remain mappings to independently documented public standards. They MUST NOT create a hidden dependency on DoveWAI-hosted infrastructure or non-public repositories.
