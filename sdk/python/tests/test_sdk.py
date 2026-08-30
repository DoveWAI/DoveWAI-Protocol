from datetime import datetime, timedelta, timezone

from dovewai_protocol import claim, execution_event, from_a2a_task, from_mcp_result, protocol_error, result, task, validate_envelope


def _future() -> str:
    return (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat().replace("+00:00", "Z")


def test_builders_validate():
    envelopes = [
        task("task:test:1", "Do work", {"x": 1}, required_capabilities=["example.work"]),
        claim("claim:test:1", "task:test:1", "worker:test", _future()),
        execution_event("event:test:1", "task:test:1", "started", sequence=1),
        result("result:test:1", "task:test:1", "succeeded", {"ok": True}),
        protocol_error("error:test:1", "EXAMPLE", "Example failure", task_id="task:test:1", retryable=False),
    ]
    for envelope in envelopes:
        assert validate_envelope(envelope) == []


def test_mcp_adapter_preserves_source_identity():
    envelope = from_mcp_result("task:test:1", "result:test:mcp", {"structuredContent": {"answer": 42}}, source_id="mcp-task-1")
    assert envelope["status"] == "succeeded"
    assert envelope["extensions"]["ai.dovewai.mcp"]["source_id"] == "mcp-task-1"
    assert validate_envelope(envelope) == []


def test_a2a_adapter_preserves_source_identity():
    envelope = from_a2a_task({"id": "a2a-task-1", "contextId": "ctx-1"}, "task:test:a2a")
    assert envelope["extensions"]["ai.dovewai.a2a"]["task_id"] == "a2a-task-1"
    assert validate_envelope(envelope) == []
