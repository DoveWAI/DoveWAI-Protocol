from tools.lifecycle_validate import validate_lifecycle


def _bundle():
    return [
        {
            "protocol_version": "0.1",
            "id": "task:lifecycle:1",
            "type": "task",
            "created_at": "2026-08-31T00:00:00Z",
            "intent": "Perform work",
        },
        {
            "protocol_version": "0.1",
            "id": "claim:lifecycle:1",
            "type": "claim",
            "created_at": "2026-08-31T00:00:01Z",
            "task_id": "task:lifecycle:1",
            "holder_id": "worker:1",
            "mode": "write",
            "lease_expires_at": "2026-08-31T00:05:00Z",
        },
        {
            "protocol_version": "0.1",
            "id": "event:lifecycle:1",
            "type": "execution_event",
            "created_at": "2026-08-31T00:00:02Z",
            "task_id": "task:lifecycle:1",
            "event_type": "started",
            "sequence": 1,
        },
        {
            "protocol_version": "0.1",
            "id": "result:lifecycle:1",
            "type": "result",
            "created_at": "2026-08-31T00:00:03Z",
            "task_id": "task:lifecycle:1",
            "status": "succeeded",
        },
    ]


def test_valid_lifecycle_passes():
    assert validate_lifecycle(_bundle()) == []


def test_expired_claim_fails():
    bundle = _bundle()
    bundle[1]["lease_expires_at"] = "2026-08-31T00:00:00Z"
    assert any("lease must expire" in error for error in validate_lifecycle(bundle))


def test_unknown_task_fails():
    bundle = _bundle()
    bundle[2]["task_id"] = "task:missing"
    assert any("unknown task_id" in error for error in validate_lifecycle(bundle))


def test_duplicate_terminal_result_fails():
    bundle = _bundle()
    duplicate = dict(bundle[-1])
    duplicate["id"] = "result:lifecycle:2"
    bundle.append(duplicate)
    assert any("multiple terminal Result" in error for error in validate_lifecycle(bundle))
