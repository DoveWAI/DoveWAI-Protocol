from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

PROTOCOL_VERSION = "0.2"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _base(object_type: str, object_id: str | None = None, created_at: str | None = None) -> dict[str, Any]:
    return {
        "protocol_version": PROTOCOL_VERSION,
        "id": object_id or str(uuid4()),
        "type": object_type,
        "created_at": created_at or _now(),
    }


def task(intent: str, **fields: Any) -> dict[str, Any]:
    return {**_base("Task", fields.pop("id", None), fields.pop("created_at", None)), "intent": intent, **fields}


def capability(name: str, version: str, **fields: Any) -> dict[str, Any]:
    return {**_base("Capability", fields.pop("id", None), fields.pop("created_at", None)), "name": name, "version": version, **fields}


def claim(task_id: str, holder_id: str, mode: str, lease_expires_at: str, **fields: Any) -> dict[str, Any]:
    return {
        **_base("Claim", fields.pop("id", None), fields.pop("created_at", None)),
        "task_id": task_id,
        "holder_id": holder_id,
        "mode": mode,
        "lease_expires_at": lease_expires_at,
        **fields,
    }


def attempt(task_id: str, attempt_number: int, status: str, **fields: Any) -> dict[str, Any]:
    return {
        **_base("Attempt", fields.pop("id", None), fields.pop("created_at", None)),
        "task_id": task_id,
        "attempt_number": attempt_number,
        "status": status,
        **fields,
    }


def execution_event(task_id: str, event_type: str, **fields: Any) -> dict[str, Any]:
    return {
        **_base("ExecutionEvent", fields.pop("id", None), fields.pop("created_at", None)),
        "task_id": task_id,
        "event_type": event_type,
        **fields,
    }


def artifact(uri: str, **fields: Any) -> dict[str, Any]:
    return {**_base("Artifact", fields.pop("id", None), fields.pop("created_at", None)), "uri": uri, **fields}


def result(task_id: str, status: str, **fields: Any) -> dict[str, Any]:
    return {
        **_base("Result", fields.pop("id", None), fields.pop("created_at", None)),
        "task_id": task_id,
        "status": status,
        **fields,
    }


def verification(subject_type: str, subject_id: str, verifier_id: str, method: str, outcome: str, **fields: Any) -> dict[str, Any]:
    return {
        **_base("Verification", fields.pop("id", None), fields.pop("created_at", None)),
        "subject": {"type": subject_type, "id": subject_id},
        "verifier_id": verifier_id,
        "method": method,
        "outcome": outcome,
        **fields,
    }


def work_receipt(task_id: str, result_id: str, status: str, **fields: Any) -> dict[str, Any]:
    return {
        **_base("WorkReceipt", fields.pop("id", None), fields.pop("created_at", None)),
        "task_id": task_id,
        "result_id": result_id,
        "status": status,
        **fields,
    }
