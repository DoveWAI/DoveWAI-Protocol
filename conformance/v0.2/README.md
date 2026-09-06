# DoveWAI Protocol v0.2 Conformance

v0.2 conformance has two layers:

1. Structural conformance: each envelope validates against `schemas/v0.2/core.schema.json`.
2. Lifecycle conformance: relationships across a bundle satisfy the v0.2 lifecycle rules implemented by the shared public lifecycle validator.

A conforming lifecycle validator MUST reject at least:

- duplicate object IDs;
- references to unknown Tasks, Claims, Attempts, Artifacts, Results, or Verifications where those references are required to resolve;
- Claims whose lease expires at or before creation;
- duplicate attempt numbers for the same Task;
- duplicate or decreasing execution-event sequence numbers within an Attempt;
- more than one terminal Result for a Task;
- Results that reference unknown Attempts or Artifacts;
- Verifications whose subjects cannot be resolved inside the tested bundle when bundle-local resolution is required;
- WorkReceipts whose Task or Result cannot be resolved or whose Task and Result disagree;
- WorkReceipts that claim `verified` without at least one referenced passing Verification;
- WorkReceipts that claim `verified` while referencing a failed Verification;
- WorkReceipts that claim `verification_failed` without a referenced failed Verification;
- WorkReceipts that reference unknown Attempts, Artifacts, or Verifications.

## TCK runner

Install the Python SDK from the repository and execute:

```bash
python -m pip install -e sdk/python
python tools/tck_v02.py
```

The TCK is black-box with respect to the public CLI: every file in `valid/` must be accepted by `dovewai validate`, and every file in `invalid/` must be rejected as a protocol-validation failure. New semantic rules should be accompanied by positive and negative vectors so unrelated implementations can reproduce the expected behavior.

Conformance means agreement with DoveWAI Protocol semantics only. It does not imply correctness, security, authorization, authenticity, or conformance to any external protocol used by an adapter or profile.
