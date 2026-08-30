from __future__ import annotations

from typing import Any

from . import result, task


def from_mcp_result(task_id: str, result_id: str, mcp_result: dict[str, Any], *, source_id: str | None = None) -> dict[str, Any]:
    """Normalize an MCP tool/task result without claiming MCP-level validation."""
    warnings: list[str] = []
    status = "failed" if mcp_result.get("isError") else "succeeded"
    extensions: dict[str, Any] = {"ai.dovewai.mcp": {"source_id": source_id, "is_error": bool(mcp_result.get("isError", False))}}
    content = mcp_result.get("structuredContent", mcp_result.get("content"))
    if content is None:
        warnings.append("MCP result had no structuredContent/content")
    return result(result_id, task_id, status, {"content": content}, warnings=warnings, extensions=extensions)


def from_a2a_task(a2a_task: dict[str, Any], dove_task_id: str, *, intent: str | None = None) -> dict[str, Any]:
    """Create a DoveWAI Task envelope referencing an A2A task as an execution target."""
    source_id = a2a_task.get("id")
    context_id = a2a_task.get("contextId")
    derived_intent = intent or "Execute referenced A2A task"
    return task(
        dove_task_id,
        derived_intent,
        {"a2a_task": a2a_task},
        extensions={"ai.dovewai.a2a": {"task_id": source_id, "context_id": context_id}},
    )


def map_a2a_state(state: str) -> str:
    """Map known A2A 1.0 task states and reject unknown states explicitly."""
    mapping = {
        "TASK_STATE_SUBMITTED": "working",
        "TASK_STATE_WORKING": "working",
        "TASK_STATE_INPUT_REQUIRED": "input_required",
        "TASK_STATE_AUTH_REQUIRED": "auth_required",
        "TASK_STATE_COMPLETED": "succeeded",
        "TASK_STATE_FAILED": "failed",
        "TASK_STATE_CANCELED": "cancelled",
        "TASK_STATE_REJECTED": "rejected",
    }
    try:
        return mapping[state]
    except KeyError as exc:
        raise ValueError(f"unsupported A2A state: {state}") from exc
