# DoveWAI Agent Runtime Profile v0.1

Status: experimental, non-normative profile for DoveWAI Protocol v0.2.

This profile maps agent-safe tool execution, resource selection, authorization, isolated worker execution, evidence, and receipts onto the existing DoveWAI Protocol lifecycle without changing the v0.2 core schema.

## Design constraints

- Additive only: no changes to published v0.2 core object semantics.
- Vendor neutral: no mandatory dependency on gh-axi, quota-axi, Automic Vault, ego-lite, worktrunk, Chandra, Recurse ML, or any other third-party project.
- Local-first where practical.
- Least authority and fail-closed behavior.
- External projects are references/providers, never protocol requirements.
- Implement first; conformance and runtime testing remain deferred to the final verification phase.

## Extension namespaces

The v0.2 `extensions` object is used for runtime-profile data. Implementations SHOULD use the following keys:

- `dovewai.runtime.resource`
- `dovewai.runtime.authorization`
- `dovewai.runtime.worker`
- `dovewai.runtime.axi`
- `dovewai.runtime.code_intelligence`
- `dovewai.runtime.document_intelligence`

## AXI execution

An Agent Experience Interface adapter SHOULD translate a human-oriented tool/API into bounded, structured, non-interactive execution.

A Task MAY declare AXI requirements using `extensions["dovewai.runtime.axi"]`:

```json
{
  "adapter": "github",
  "operation": "pull_request.read",
  "interactive": false,
  "bounded_output": true,
  "destructive": false
}
```

The adapter is expected to preserve exit status, structured errors, provenance, and a pointer to full evidence when output is truncated or summarized.

## Resource evidence

Resource state SHOULD be carried as evidence or an Artifact referenced by the Task/Attempt/Result. A normalized resource observation SHOULD include:

```json
{
  "resource_id": "provider:example",
  "kind": "model_provider",
  "scope": "all_models",
  "availability": "available",
  "remaining_percent": 67,
  "resets_at": "2026-09-13T00:00:00Z",
  "runway_seconds": 7200,
  "confidence": "established",
  "stale": false
}
```

DoveWAI runtime implementations MAY extend this model to CPU, GPU/NPU, RAM/VRAM, storage, NAS, API rate limits, cloud credits, cost, latency, locality, privacy constraints, and model capabilities.

The resource broker informs selection. It does not grant authority.

## Authorization decision

Authorization is separate from resource availability. Implementations SHOULD evaluate the exact requested operation and SHOULD NOT equate possession of a credential with permission to use all credential capabilities.

`extensions["dovewai.runtime.authorization"]` SHOULD contain or reference a decision with:

```json
{
  "decision": "allow",
  "principal_id": "agent:worker-01",
  "task_id": "task-123",
  "tool": "github",
  "operation": "pull_request.read",
  "target": "DoveWAI/example",
  "capabilities": ["repo.read"],
  "credential_names": ["github.default"],
  "expires_at": "2026-09-12T13:10:00Z",
  "policy_id": "protect/default-v1"
}
```

Valid implementation decisions are `allow`, `require_approval`, and `deny`.

Temporary grants SHOULD be scoped to principal, task, tool/operation, target, capabilities, and expiration. Secret disclosure SHOULD be a distinct capability from secret use.

## Worker isolation

A worker SHOULD have an isolated execution scope. `extensions["dovewai.runtime.worker"]` MAY describe:

```json
{
  "worker_id": "worker-01",
  "workspace_id": "workspace-01",
  "git_worktree": "worktree-01",
  "browser_space": "browser-space-01",
  "receipt_namespace": "receipt/task-123",
  "resource_budget_id": "budget-01"
}
```

The profile does not mandate a particular worktree, container, browser, VM, or sandbox implementation.

## Evidence and receipts

Runtime decisions SHOULD be recorded as ExecutionEvents or Artifacts and referenced by Result/Verification/WorkReceipt.

At minimum, evidence SHOULD retain:

- selected provider/resource and the evidence used for selection;
- authorization decision and policy reference;
- worker/workspace identity;
- tool operation requested and actual exit status;
- artifact/evidence digests where available;
- warnings, truncation, stale-data, or indeterminate conditions.

## Provider strategy

Provider adapters MAY integrate external software, but DoveWAI capability contracts MUST remain implementation-owned and provider-neutral. A provider can be replaced without changing the task/receipt semantics.

Examples:

- GitHub adapter: raw `gh`, REST/GraphQL, gh-axi-inspired adapter, or another implementation.
- Browser adapter: Playwright/CDP, ego-lite-inspired Spaces, or another implementation.
- Secret backend: Windows DPAPI/Credential Manager, Linux Secret Service/keyring, macOS Keychain, or another implementation.
- Quota adapter: provider-native APIs/CLIs or quota-axi-inspired adapters.
- Code intelligence: tree-sitter/graph implementation selected by the runtime.

## Deferred verification gate

This profile intentionally defines contracts before implementation-wide testing. Runtime/conformance testing for this integration program is deferred until the implementation phases are complete and the final verification gate is explicitly opened.
