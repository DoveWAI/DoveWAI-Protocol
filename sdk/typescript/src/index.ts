export const PROTOCOL_VERSION = "0.1" as const;

type Envelope = Record<string, unknown>;
export type A2AMappedState = "working" | "input_required" | "auth_required" | "succeeded" | "failed" | "cancelled" | "rejected";

const now = () => new Date().toISOString();

export function task(id: string, intent: string, inputs?: Record<string, unknown>, extra: Envelope = {}): Envelope {
  return { protocol_version: PROTOCOL_VERSION, id, type: "task", created_at: now(), intent, ...(inputs ? { inputs } : {}), ...extra };
}

export function claim(id: string, taskId: string, holderId: string, leaseExpiresAt: string, mode: "read" | "write" = "write", extra: Envelope = {}): Envelope {
  return { protocol_version: PROTOCOL_VERSION, id, type: "claim", created_at: now(), task_id: taskId, holder_id: holderId, mode, lease_expires_at: leaseExpiresAt, ...extra };
}

export function executionEvent(id: string, taskId: string, eventType: string, sequence?: number, payload?: Record<string, unknown>, extra: Envelope = {}): Envelope {
  return { protocol_version: PROTOCOL_VERSION, id, type: "execution_event", created_at: now(), task_id: taskId, event_type: eventType, ...(sequence === undefined ? {} : { sequence }), ...(payload ? { payload } : {}), ...extra };
}

export function result(id: string, taskId: string, status: "succeeded" | "partial" | "failed" | "cancelled", outputs?: Record<string, unknown>, extra: Envelope = {}): Envelope {
  return { protocol_version: PROTOCOL_VERSION, id, type: "result", created_at: now(), task_id: taskId, status, ...(outputs ? { outputs } : {}), ...extra };
}

export function protocolError(id: string, code: string, message: string, extra: Envelope = {}): Envelope {
  return { protocol_version: PROTOCOL_VERSION, id, type: "error", created_at: now(), code, message, ...extra };
}

export function fromMcpResult(taskId: string, resultId: string, mcpResult: Record<string, unknown>, sourceId?: string): Envelope {
  const isError = Boolean(mcpResult.isError);
  const content = mcpResult.structuredContent ?? mcpResult.content ?? null;
  return result(resultId, taskId, isError ? "failed" : "succeeded", { content }, {
    warnings: content === null ? ["MCP result had no structuredContent/content"] : [],
    extensions: { "ai.dovewai.mcp": { source_id: sourceId ?? null, is_error: isError } }
  });
}

export function fromA2ATask(a2aTask: Record<string, unknown>, doveTaskId: string, intent = "Execute referenced A2A task"): Envelope {
  return task(doveTaskId, intent, { a2a_task: a2aTask }, {
    extensions: { "ai.dovewai.a2a": { task_id: a2aTask.id ?? null, context_id: a2aTask.contextId ?? null } }
  });
}

export function mapA2AState(state: string): A2AMappedState {
  const mapping: Record<string, A2AMappedState> = {
    TASK_STATE_SUBMITTED: "working",
    TASK_STATE_WORKING: "working",
    TASK_STATE_INPUT_REQUIRED: "input_required",
    TASK_STATE_AUTH_REQUIRED: "auth_required",
    TASK_STATE_COMPLETED: "succeeded",
    TASK_STATE_FAILED: "failed",
    TASK_STATE_CANCELED: "cancelled",
    TASK_STATE_REJECTED: "rejected"
  };
  const mapped = mapping[state];
  if (!mapped) throw new Error(`Unsupported A2A state: ${state}`);
  return mapped;
}
