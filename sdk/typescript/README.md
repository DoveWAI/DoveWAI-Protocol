# DoveWAI Protocol TypeScript SDK

Reference builders and pure interoperability adapters for DoveWAI Protocol v0.1.

```bash
cd sdk/typescript
npm install
npm test
```

```ts
import { task, result } from "@dovewai/protocol";

const work = task("task:demo:1", "Summarize a document", { document_id: "doc-1" });
const outcome = result("result:demo:1", String(work.id), "succeeded", { summary: "..." });
```

The SDK deliberately keeps protocol objects visible and does not require a DoveWAI-hosted service. MCP/A2A adapter helpers normalize selected fields while preserving source identifiers. Unknown A2A task states are rejected rather than guessed.
