from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

PROTOCOL_VERSION = "0.1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def task(id: str, intent: str, inputs: dict[str, Any] | None = None, *, required_capabilities: list[str] | None = None, **extra: Any) -> dict[str, Any]:
    value = {"protocol_version": PROTOCOL_VERSION, "id": id, "type": "task", "created_at": _now(), "intent": intent}
    if inputs is not None:
        value["inputs"] = inputs
    if required_capabilities:
        value["required_capabilities"] = required_capabilities
    value.update(extra)
    return value


def claim(id: str, task_id: str, holder_id: str, lease_expires_at: str, *, mode: str = "write", **extra: Any) -> dict[str, Any]:
    value = {"protocol_version": PROTOCOL_VERSION, "id": id, "type": "claim", "created_at": _now(), "task_id": task_id, "holder_id": holder_id, "mode": mode, "lease_expires_at": lease_expires_at}
    value.update(extra)
    return value


def execution_event(id: str, task_id: str, event_type: str, *, sequence: int | None = None, payload: dict[str, Any] | None = None, **extra: Any) -> dict[str, Any]:
    value = {"protocol_version": PROTOCOL_VERSION, "id": id, "type": "execution_event", "created_at": _now(), "task_id": task_id, "event_type": event_type}
    if sequence is not None:
        value["sequence"] = sequence
    if payload is not None:
        value["payload"] = payload
    value.update(extra)
    return value


def result(id: str, task_id: str, status: str, outputs: dict[str, Any] | None = None, **extra: Any) -> dict[str, Any]:
    value = {"protocol_version": PROTOCOL_VERSION, "id": id, "type": "result", "created_at": _now(), "task_id": task_id, "status": status}
    if outputs is not None:
        value["outputs"] = outputs
    value.update(extra)
    return value


def protocol_error(id: str, code: str, message: str, *, task_id: str | None = None, retryable: bool | None = None, **extra: Any) -> dict[str, Any]:
    value = {"protocol_version": PROTOCOL_VERSION, "id": id, "type": "error", "created_at": _now(), "code": code, "message": message}
    if task_id is not None:
        value["task_id"] = task_id
    if retryable is not None:
        value["retryable"] = retryable
    value.update(extra)
    return value

from .adapters import from_a2a_task, from_mcp_result
from .validation import validate_envelope

__all__ = ["PROTOCOL_VERSION", "task", "claim", "execution_event", "result", "protocol_error", "from_a2a_task", "from_mcp_result", "validate_envelope"]
