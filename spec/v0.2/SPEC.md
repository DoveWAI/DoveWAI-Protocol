# DoveWAI Protocol v0.2 Specification

Status: Experimental, recommended for new implementations.

## 1. Scope

DoveWAI Protocol defines a transport-neutral work contract for interoperable execution and verification across software agents, tools, runtimes, services, people, and hybrid systems.

It does not define discovery, authentication, authorization, model APIs, transport protocols, telemetry backends, or cryptographic trust roots.

A conforming implementation MUST be implementable from public DoveWAI Protocol materials alone.

## 2. Core lifecycle

The v0.2 lifecycle is:

`Task -> Capability -> Claim -> Attempt -> ExecutionEvent/Artifact -> Result -> Verification -> WorkReceipt`

A Task MAY exist without every later object. Later objects MUST reference earlier objects according to this specification.

## 3. Common envelope fields

Every core object MUST contain:

- `protocol_version`: MUST be `0.2` for this specification.
- `id`: globally unique within the implementation's interoperability domain.
- `type`: the object type.
- `created_at`: RFC 3339 date-time in UTC where possible.

Objects MAY contain namespaced `extensions`.

## 4. Task

A Task describes requested work.

Required:

- `intent`

Optional:

- `inputs`
- `required_capabilities`
- `constraints`
- `deadline`
- `correlation_id`
- `parent_task_id`
- `idempotency_key`
- `provenance`

An implementation MUST NOT silently create a second logical task for the same idempotency key within the same declared idempotency scope unless its application contract explicitly permits it.

## 5. Capability

A Capability describes an implementation-neutral ability.

Recommended fields include `name`, `version`, `features`, `input_schema`, `output_schema`, and `limits`.

Capability advertisement does not itself grant permission to execute work.

## 6. Claim

A Claim records temporary ownership or responsibility for a Task.

Required:

- `task_id`
- `holder_id`
- `mode`
- `lease_expires_at`

Recommended distributed-coordination fields:

- `lease_generation`
- `fencing_token`
- `renewed_at`
- `revoked_at`
- `supersedes_claim_id`

For write claims, an implementation using lease generations or fencing tokens MUST reject stale generations/tokens according to its declared fencing profile. An expired or revoked Claim MUST NOT authorize creation of a new terminal Result.

## 7. Attempt

An Attempt represents one concrete execution try for a Task.

Required:

- `task_id`
- `attempt_number`
- `status`

Optional:

- `claim_id`
- `executor_id`
- `started_at`
- `ended_at`
- `resume_from`

Attempt status values are `pending`, `running`, `succeeded`, `failed`, `cancelled`.

Retries, failover, and resume MUST create or explicitly reference an Attempt rather than being hidden inside an undifferentiated Result.

## 8. ExecutionEvent

An ExecutionEvent records something that happened during execution.

Required:

- `task_id`
- `event_type`

Recommended:

- `attempt_id`
- `sequence`
- `occurred_at`
- `observed_at`
- `correlation_id`
- `causation_id`
- `previous_event_id`
- `data`

Sequences, when present within an Attempt, MUST be unique and monotonically increasing.

Event vocabularies SHOULD be extensible. Implementations MUST define behavior for unknown event types and MUST NOT silently map unknown external states to a known success state.

## 9. Artifact

An Artifact represents a durable output or evidence object produced or referenced by work.

Required:

- `uri`

Optional:

- `task_id`
- `attempt_id`
- `media_type`
- `size`
- `digest`
- `producer_id`
- `source_artifact_ids`
- `metadata`

A digest increases traceability but does not itself prove correctness or authorship.

## 10. Result

A Result is the terminal outcome declaration for a Task.

Required:

- `task_id`
- `status`

Allowed status values:

- `succeeded`
- `failed`
- `cancelled`

Optional:

- `attempt_id`
- `outputs`
- `artifact_ids`
- `metrics`
- `evidence`
- `provenance`
- `warnings`

There MUST NOT be more than one terminal Result for a Task unless an extension profile explicitly defines a supersession mechanism. Intermediate or partial outputs MUST be represented as ExecutionEvents, checkpoints, or Artifacts.

## 11. Verification

A Verification records an assessment of a Task, Result, Artifact, Attempt, or other protocol subject.

Required:

- `subject`
- `verifier_id`
- `method`
- `outcome`

Allowed outcomes:

- `passed`
- `failed`
- `indeterminate`
- `skipped`

Optional:

- `policy`
- `observations`
- `evidence`
- `artifact_ids`
- `policy_decision_ref`

A Verification records what was checked and what was observed. The protocol does not declare the verifier trustworthy merely because a Verification object exists.

## 12. WorkReceipt

A WorkReceipt is a portable summary tying requested work to execution, result, artifacts, and verification.

Required:

- `task_id`
- `result_id`
- `status`

Optional:

- `claim_id`
- `attempt_ids`
- `artifact_ids`
- `verification_ids`
- `evidence`
- `issued_by`
- `started_at`
- `completed_at`
- `digest`
- `signature_ref`

Receipt status values are `recorded`, `verified`, `verification_failed`, and `indeterminate`.

A WorkReceipt is not proof that every underlying statement is true. It is a portable record of the declared work lifecycle and referenced verification.

## 13. Provenance

Provenance records source and transformation information, such as source URI, acquisition time, digest, media type, and transformation notes.

Provenance MUST NOT be interpreted as automatic trust, truth, authorization, or correctness.

## 14. ProtocolError

ProtocolError represents structured protocol-level failures. It SHOULD contain a stable `code` and human-readable `message`, and MAY include `details` and `retryable`.

## 15. Extensions

Extension keys MUST be collision resistant, preferably reverse-DNS names. Extensions MUST NOT redefine required core-field semantics.

Unsupported mandatory profiles MUST fail explicitly rather than being silently ignored.

## 16. Security and trust boundaries

- Claims are not credentials.
- Provenance is not correctness.
- Receipts are not automatic truth.
- Verifications do not automatically make verifiers trustworthy.
- Authentication and authorization remain external to the core protocol.
- Untrusted protocol input MUST be validated before use.
- Implementations SHOULD protect against replay, duplicate execution, stale claims, malicious artifact references, oversized input, and extension abuse.

## 17. Version compatibility

v0.1 objects MUST NOT be silently reinterpreted as v0.2. Conversion MUST be explicit and SHOULD preserve original identifiers where doing so does not create collisions or false equivalence.
