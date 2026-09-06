from __future__ import annotations

from datetime import datetime
from typing import Any


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_bundle(objects: list[dict[str, Any]]) -> None:
    """Validate DoveWAI Protocol v0.2 cross-object lifecycle invariants.

    Raises ValueError when the bundle violates a lifecycle rule. JSON Schema
    validation remains separate and should run before this function.
    """
    by_id: dict[str, dict[str, Any]] = {}
    for obj in objects:
        oid = obj.get("id")
        if not oid:
            raise ValueError("object missing id")
        if oid in by_id:
            raise ValueError(f"duplicate object id: {oid}")
        if obj.get("protocol_version") != "0.2":
            raise ValueError(f"non-v0.2 object in v0.2 bundle: {oid}")
        by_id[str(oid)] = obj

    tasks = {k: v for k, v in by_id.items() if v.get("type") == "Task"}
    claims = {k: v for k, v in by_id.items() if v.get("type") == "Claim"}
    attempts = {k: v for k, v in by_id.items() if v.get("type") == "Attempt"}
    artifacts = {k: v for k, v in by_id.items() if v.get("type") == "Artifact"}
    results = {k: v for k, v in by_id.items() if v.get("type") == "Result"}
    verifications = {k: v for k, v in by_id.items() if v.get("type") == "Verification"}
    receipts = {k: v for k, v in by_id.items() if v.get("type") == "WorkReceipt"}

    for cid, claim in claims.items():
        if claim.get("task_id") not in tasks:
            raise ValueError(f"claim {cid} references unknown task")
        if _dt(claim["lease_expires_at"]) <= _dt(claim["created_at"]):
            raise ValueError(f"claim {cid} lease does not extend beyond creation")

    attempt_numbers: dict[str, set[int]] = {}
    for aid, attempt in attempts.items():
        task_id = attempt.get("task_id")
        if task_id not in tasks:
            raise ValueError(f"attempt {aid} references unknown task")
        claim_id = attempt.get("claim_id")
        if claim_id and claim_id not in claims:
            raise ValueError(f"attempt {aid} references unknown claim")
        number = attempt.get("attempt_number")
        seen = attempt_numbers.setdefault(str(task_id), set())
        if number in seen:
            raise ValueError(f"duplicate attempt_number {number} for task {task_id}")
        seen.add(number)

    event_sequences: dict[str, list[int]] = {}
    for eid, event in ((k, v) for k, v in by_id.items() if v.get("type") == "ExecutionEvent"):
        if event.get("task_id") not in tasks:
            raise ValueError(f"event {eid} references unknown task")
        attempt_id = event.get("attempt_id")
        if attempt_id and attempt_id not in attempts:
            raise ValueError(f"event {eid} references unknown attempt")
        if attempt_id and "sequence" in event:
            event_sequences.setdefault(str(attempt_id), []).append(event["sequence"])

    for attempt_id, sequences in event_sequences.items():
        if len(sequences) != len(set(sequences)):
            raise ValueError(f"duplicate event sequence in attempt {attempt_id}")
        if sequences != sorted(sequences):
            raise ValueError(f"non-monotonic event sequence in attempt {attempt_id}")

    for artifact_id, artifact in artifacts.items():
        task_id = artifact.get("task_id")
        if task_id and task_id not in tasks:
            raise ValueError(f"artifact {artifact_id} references unknown task")
        attempt_id = artifact.get("attempt_id")
        if attempt_id and attempt_id not in attempts:
            raise ValueError(f"artifact {artifact_id} references unknown attempt")

    terminal_by_task: dict[str, str] = {}
    for rid, result in results.items():
        task_id = result.get("task_id")
        if task_id not in tasks:
            raise ValueError(f"result {rid} references unknown task")
        if task_id in terminal_by_task:
            raise ValueError(f"multiple terminal results for task {task_id}")
        terminal_by_task[str(task_id)] = rid
        attempt_id = result.get("attempt_id")
        if attempt_id and attempt_id not in attempts:
            raise ValueError(f"result {rid} references unknown attempt")
        for artifact_id in result.get("artifact_ids", []):
            if artifact_id not in artifacts:
                raise ValueError(f"result {rid} references unknown artifact {artifact_id}")

    for vid, verification in verifications.items():
        subject = verification.get("subject", {})
        subject_id = subject.get("id")
        if subject_id not in by_id:
            raise ValueError(f"verification {vid} references unknown subject {subject_id}")
        for artifact_id in verification.get("artifact_ids", []):
            if artifact_id not in artifacts:
                raise ValueError(f"verification {vid} references unknown artifact {artifact_id}")

    for wid, receipt in receipts.items():
        if receipt.get("task_id") not in tasks:
            raise ValueError(f"receipt {wid} references unknown task")
        result_id = receipt.get("result_id")
        if result_id not in results:
            raise ValueError(f"receipt {wid} references unknown result")
        if results[str(result_id)].get("task_id") != receipt.get("task_id"):
            raise ValueError(f"receipt {wid} task/result mismatch")
        for attempt_id in receipt.get("attempt_ids", []):
            if attempt_id not in attempts:
                raise ValueError(f"receipt {wid} references unknown attempt {attempt_id}")
        for artifact_id in receipt.get("artifact_ids", []):
            if artifact_id not in artifacts:
                raise ValueError(f"receipt {wid} references unknown artifact {artifact_id}")

        referenced_verifications: list[dict[str, Any]] = []
        for verification_id in receipt.get("verification_ids", []):
            if verification_id not in verifications:
                raise ValueError(f"receipt {wid} references unknown verification {verification_id}")
            referenced_verifications.append(verifications[verification_id])

        status = receipt.get("status")
        outcomes = {v.get("outcome") for v in referenced_verifications}
        if status == "verified":
            if not referenced_verifications:
                raise ValueError(f"receipt {wid} claims verified without verification")
            if "failed" in outcomes:
                raise ValueError(f"receipt {wid} claims verified with a failed verification")
            if "passed" not in outcomes:
                raise ValueError(f"receipt {wid} claims verified without a passing verification")
        elif status == "verification_failed":
            if "failed" not in outcomes:
                raise ValueError(f"receipt {wid} claims verification_failed without a failed verification")
