# DoveWAI Protocol TypeScript SDK v0.2

The v0.2 TypeScript builders are exported under the `v02` namespace so v0.1 compatibility remains available during migration.

From a source checkout:

```bash
cd sdk/typescript
npm install
npm test
```

Public package usage after registry publication:

```ts
import { v02 } from "@dovewai/protocol";

const work = v02.task("Build and verify a release", {
  idempotency_key: "release-42",
});

const run = v02.attempt(work.id, 1, "running");
```

Available builders include `task`, `capability`, `claim`, `attempt`, `executionEvent`, `artifact`, `result`, `verification`, and `workReceipt`.

These builders create protocol envelopes; schema and lifecycle validation remain separate operations.

Version `0.2.0` in `package.json` does not by itself mean `@dovewai/protocol` has been published to npm. Confirm the registry release before documenting `npm install @dovewai/protocol` as a public registry install command.

See `RELEASE.md` at the repository root for the trusted-publishing release path.
