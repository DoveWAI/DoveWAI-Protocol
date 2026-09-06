export const PROTOCOL_VERSION = "0.2" as const;

export type Envelope = Record<string, unknown> & {
  protocol_version: "0.2";
  id: string;
  type: string;
  created_at: string;
};

function now(): string {
  return new Date().toISOString();
}

function id(): string {
  return globalThis.crypto?.randomUUID?.() ?? `dovewai-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function base(type: string, fields: Record<string, unknown>): Envelope {
  const objectId = typeof fields.id === "string" ? fields.id : id();
  const createdAt = typeof fields.created_at === "string" ? fields.created_at : now();
  const rest = { ...fields };
  delete rest.id;
  delete rest.created_at;
  return { protocol_version: PROTOCOL_VERSION, id: objectId, type, created_at: createdAt, ...rest };
}

export function task(intent: string, fields: Record<string, unknown> = {}): Envelope {
  return base("Task", { ...fields, intent });
}

export function capability(name: string, version: string, fields: Record<string, unknown> = {}): Envelope {
  return base("Capability", { ...fields, name, version });
}

export function claim(task_id: string, holder_id: string, mode: "read" | "write", lease_expires_at: string, fields: Record<string, unknown> = {}): Envelope {
  return base("Claim", { ...fields, task_id, holder_id, mode, lease_expires_at });
}

export function attempt(task_id: string, attempt_number: number, status: "pending" | "running" | "succeeded" | "failed" | "cancelled", fields: Record<string, unknown> = {}): Envelope {
  return base("Attempt", { ...fields, task_id, attempt_number, status });
}

export function executionEvent(task_id: string, event_type: string, fields: Record<string, unknown> = {}): Envelope {
  return base("ExecutionEvent", { ...fields, task_id, event_type });
}

export function artifact(uri: string, fields: Record<string, unknown> = {}): Envelope {
  return base("Artifact", { ...fields, uri });
}

export function result(task_id: string, status: "succeeded" | "failed" | "cancelled", fields: Record<string, unknown> = {}): Envelope {
  return base("Result", { ...fields, task_id, status });
}

export function verification(subjectType: string, subjectId: string, verifier_id: string, method: string, outcome: "passed" | "failed" | "indeterminate" | "skipped", fields: Record<string, unknown> = {}): Envelope {
  return base("Verification", { ...fields, subject: { type: subjectType, id: subjectId }, verifier_id, method, outcome });
}

export function workReceipt(task_id: string, result_id: string, status: "recorded" | "verified" | "verification_failed" | "indeterminate", fields: Record<string, unknown> = {}): Envelope {
  return base("WorkReceipt", { ...fields, task_id, result_id, status });
}
