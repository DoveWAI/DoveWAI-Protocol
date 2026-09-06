# DoveWAI Protocol v0.2 Conformance

v0.2 conformance has two layers:

1. Structural conformance: each envelope validates against `schemas/v0.2/core.schema.json`.
2. Lifecycle conformance: relationships across a bundle satisfy the v0.2 lifecycle rules.

A conforming lifecycle validator MUST reject at least:

- references to unknown Tasks, Claims, Attempts, Artifacts, Results, or Verifications where those references are required to resolve;
- Claims whose lease expires at or before creation;
- duplicate attempt numbers for the same Task;
- duplicate or decreasing execution-event sequence numbers within an Attempt;
- more than one terminal Result for a Task;
- Results that reference unknown Attempts or Artifacts;
- Verifications whose subjects cannot be resolved inside the tested bundle when bundle-local resolution is required;
- WorkReceipts whose Task or Result cannot be resolved;
- WorkReceipts that claim `verified` without at least one referenced passing Verification;
- WorkReceipts that reference unknown Attempts, Artifacts, or Verifications.

Conformance means agreement with DoveWAI Protocol semantics only. It does not imply correctness, security, authorization, authenticity, or conformance to any external protocol used by an adapter or profile.
