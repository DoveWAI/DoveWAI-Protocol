# TypeScript SDK v0.2 surface

The v0.2 builders live in `src/v02.ts` so v0.1 behavior remains available during migration.

```ts
import { task, attempt } from "./v02.js";

const work = task("Build and verify a release", {
  idempotency_key: "release-42",
});

const run = attempt(work.id, 1, "running");
```

Available builders:

- `task`
- `capability`
- `claim`
- `attempt`
- `executionEvent`
- `artifact`
- `result`
- `verification`
- `workReceipt`

These builders create protocol envelopes; schema and lifecycle validation remain separate operations.
