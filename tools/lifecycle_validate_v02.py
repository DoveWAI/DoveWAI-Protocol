#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from pathlib import Path


def dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def fail(message: str) -> None:
    raise ValueError(message)


def validate_bundle(objects: list[dict]) -> None:
    by_id = {}
    for obj in objects:
        oid = obj.get("id")
        if not oid:
            fail("object missing id")
        if oid in by_id:
            fail(f"duplicate object id: {oid}")
        if obj.get("protocol_version") != "0.2":
            fail(f"non-v0.2 object in v0.2 bundle: {oid}")
        by_id[oid] = obj

    tasks = {k: v for k, v in by_id.items() if v.get("type") == "Task"}
    claims = {k: v for k, v in by_id.items() if v.get("type") == "Claim"}
    attempts = {k: v for k, v in by_id.items() if v.get("type") == "Attempt"}
    artifacts = {k: v for k, v in by_id.items() if v.get("type") == "Artifact"}
    results = {k: v for k, v in by_id.items() if v.get("type") == "Result"}
    verifications = {k: v for k, v in by_id.items() if v.get("type") == "Verification"}
    receipts = {k: v for k, v in by_id.items() if v.get("type") == "WorkReceipt"}

    for cid, claim in claims.items():
        if claim.get("task_id") not in tasks:
            fail(f"claim {cid} references unknown task")
        if dt(claim["lease_expires_at"]) <= dt(claim["created_at"]):
            fail(f"claim {cid} lease does not extend beyond creation")

    attempt_numbers: dict[str, set[int]] = {}
    for aid, attempt in attempts.items():
        task_id = attempt.get("task_id")
        if task_id not in tasks:
            fail(f"attempt {aid} references unknown task")
        claim_id = attempt.get("claim_id")
        if claim_id and claim_id not in claims:
            fail(f"attempt {aid} references unknown claim")
        n = attempt.get("attempt_number")
        seen = attempt_numbers.setdefault(task_id, set())
        if n in seen:
            fail(f"duplicate attempt_number {n} for task {task_id}")
        seen.add(n)

    event_sequences: dict[str, list[int]] = {}
    for eid, event in ((k, v) for k, v in by_id.items() if v.get("type") == "ExecutionEvent"):
        if event.get("task_id") not in tasks:
            fail(f"event {eid} references unknown task")
        attempt_id = event.get("attempt_id")
        if attempt_id and attempt_id not in attempts:
            fail(f"event {eid} references unknown attempt")
        if attempt_id and "sequence" in event:
            seqs = event_sequences.setdefault(attempt_id, [])
            seqs.append(event["sequence"])

    for attempt_id, seqs in event_sequences.items():
        if len(seqs) != len(set(seqs)):
            fail(f"duplicate event sequence in attempt {attempt_id}")
        if seqs != sorted(seqs):
            fail(f"non-monotonic event sequence in attempt {attempt_id}")

    for artifact_id, artifact in artifacts.items():
        task_id = artifact.get("task_id")
        if task_id and task_id not in tasks:
            fail(f"artifact {artifact_id} references unknown task")
        attempt_id = artifact.get("attempt_id")
        if attempt_id and attempt_id not in attempts:
            fail(f"artifact {artifact_id} references unknown attempt")

    terminal_by_task: dict[str, str] = {}
    for rid, result in results.items():
        task_id = result.get("task_id")
        if task_id not in tasks:
            fail(f"result {rid} references unknown task")
        if task_id in terminal_by_task:
            fail(f"multiple terminal results for task {task_id}")
        terminal_by_task[task_id] = rid
        attempt_id = result.get("attempt_id")
        if attempt_id and attempt_id not in attempts:
            fail(f"result {rid} references unknown attempt")
        for artifact_id in result.get("artifact_ids", []):
            if artifact_id not in artifacts:
                fail(f"result {rid} references unknown artifact {artifact_id}")

    for vid, verification in verifications.items():
        subject = verification.get("subject", {})
        subject_id = subject.get("id")
        if subject_id not in by_id:
            fail(f"verification {vid} references unknown subject {subject_id}")
        for artifact_id in verification.get("artifact_ids", []):
            if artifact_id not in artifacts:
                fail(f"verification {vid} references unknown artifact {artifact_id}")

    for wid, receipt in receipts.items():
        if receipt.get("task_id") not in tasks:
            fail(f"receipt {wid} references unknown task")
        result_id = receipt.get("result_id")
        if result_id not in results:
            fail(f"receipt {wid} references unknown result")
        if results[result_id].get("task_id") != receipt.get("task_id"):
            fail(f"receipt {wid} task/result mismatch")
        for attempt_id in receipt.get("attempt_ids", []):
            if attempt_id not in attempts:
                fail(f"receipt {wid} references unknown attempt {attempt_id}")
        for artifact_id in receipt.get("artifact_ids", []):
            if artifact_id not in artifacts:
                fail(f"receipt {wid} references unknown artifact {artifact_id}")
        referenced_verifications = []
        for verification_id in receipt.get("verification_ids", []):
            if verification_id not in verifications:
                fail(f"receipt {wid} references unknown verification {verification_id}")
            referenced_verifications.append(verifications[verification_id])
        if receipt.get("status") == "verified":
            if not referenced_verifications:
                fail(f"receipt {wid} claims verified without verification")
            if not any(v.get("outcome") == "passed" for v in referenced_verifications):
                fail(f"receipt {wid} claims verified without a passing verification")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} BUNDLE.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    objects = data if isinstance(data, list) else data.get("objects")
    if not isinstance(objects, list):
        print("bundle must be a JSON array or an object containing an objects array", file=sys.stderr)
        return 2
    try:
        validate_bundle(objects)
    except (ValueError, KeyError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print("VALID: DoveWAI Protocol v0.2 lifecycle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
