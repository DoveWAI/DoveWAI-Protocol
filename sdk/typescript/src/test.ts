import test from "node:test";
import assert from "node:assert/strict";
import { claim, executionEvent, fromA2ATask, fromMcpResult, mapA2AState, protocolError, result, task } from "./index.js";

test("builders create v0.1 envelopes", () => {
  assert.equal(task("task:1", "Do work").type, "task");
  assert.equal(claim("claim:1", "task:1", "worker:1", new Date(Date.now() + 60000).toISOString()).type, "claim");
  assert.equal(executionEvent("event:1", "task:1", "started", 1).type, "execution_event");
  assert.equal(result("result:1", "task:1", "succeeded").type, "result");
  assert.equal(protocolError("error:1", "EXAMPLE", "failure").type, "error");
});

test("adapters preserve source identity", () => {
  const mcp = fromMcpResult("task:1", "result:mcp", { structuredContent: { answer: 42 } }, "mcp-task-1");
  assert.deepEqual((mcp.extensions as Record<string, unknown>)["ai.dovewai.mcp"], { source_id: "mcp-task-1", is_error: false });
  const a2a = fromA2ATask({ id: "a2a-1", contextId: "ctx-1" }, "task:a2a");
  assert.equal(((a2a.extensions as Record<string, any>)["ai.dovewai.a2a"] as Record<string, unknown>).task_id, "a2a-1");
});

test("A2A mapping is exhaustive and fail-closed", () => {
  assert.equal(mapA2AState("TASK_STATE_COMPLETED"), "succeeded");
  assert.equal(mapA2AState("TASK_STATE_AUTH_REQUIRED"), "auth_required");
  assert.throws(() => mapA2AState("TASK_STATE_FUTURE_UNKNOWN"), /Unsupported A2A state/);
});
