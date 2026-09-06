# Python SDK v0.2 surface

The v0.2 builders live in `dovewai_protocol.v02` so v0.1 behavior remains available during migration.

```python
from dovewai_protocol import v02

work = v02.task(
    "Build and verify a release",
    idempotency_key="release-42",
)

attempt = v02.attempt(
    work["id"],
    attempt_number=1,
    status="running",
)
```

Available builders:

- `task`
- `capability`
- `claim`
- `attempt`
- `execution_event`
- `artifact`
- `result`
- `verification`
- `work_receipt`

These builders create protocol envelopes; schema and lifecycle validation remain separate operations.
