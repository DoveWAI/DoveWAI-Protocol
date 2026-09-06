# DoveWAI Protocol v0.2 Quickstart

v0.2 is the recommended protocol version for new integrations.

## 1. Create a Task

```json
{
  "protocol_version": "0.2",
  "id": "task-1",
  "type": "Task",
  "created_at": "2026-09-06T00:00:00Z",
  "intent": "Build and verify a release",
  "idempotency_key": "release-42"
}
```

## 2. Record an Attempt

```json
{
  "protocol_version": "0.2",
  "id": "attempt-1",
  "type": "Attempt",
  "created_at": "2026-09-06T00:00:01Z",
  "task_id": "task-1",
  "attempt_number": 1,
  "status": "succeeded"
}
```

## 3. Record the terminal Result

```json
{
  "protocol_version": "0.2",
  "id": "result-1",
  "type": "Result",
  "created_at": "2026-09-06T00:00:02Z",
  "task_id": "task-1",
  "attempt_id": "attempt-1",
  "status": "succeeded"
}
```

## 4. Record independent Verification

```json
{
  "protocol_version": "0.2",
  "id": "verification-1",
  "type": "Verification",
  "created_at": "2026-09-06T00:00:03Z",
  "subject": {"type": "Result", "id": "result-1"},
  "verifier_id": "urn:example:test-suite",
  "method": "test-suite",
  "outcome": "passed"
}
```

## 5. Issue a WorkReceipt

```json
{
  "protocol_version": "0.2",
  "id": "receipt-1",
  "type": "WorkReceipt",
  "created_at": "2026-09-06T00:00:04Z",
  "task_id": "task-1",
  "result_id": "result-1",
  "attempt_ids": ["attempt-1"],
  "verification_ids": ["verification-1"],
  "status": "verified"
}
```

For a complete bundle, see `examples/v0.2/verified-work-bundle.json`.

Validate lifecycle relationships with:

```bash
python tools/lifecycle_validate_v02.py examples/v0.2/verified-work-bundle.json
```

v0.1 integrations should use the explicit migration guidance in `migration/v0.1-to-v0.2.md`; do not silently reinterpret v0.1 objects as v0.2.
