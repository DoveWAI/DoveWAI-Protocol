#!/usr/bin/env python3
"""Semantic lifecycle checks across DoveWAI Protocol envelopes."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_lifecycle(envelopes: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    by_id = {str(e.get("id")): e for e in envelopes if e.get("id")}
    task_ids = {key for key, value in by_id.items() if value.get("type") == "task"}
    event_sequences: dict[str, list[int]] = {}

    for envelope in envelopes:
        kind = envelope.get("type")
        task_id = envelope.get("task_id")
        if kind in {"claim", "execution_event", "result"} and task_id not in task_ids:
            errors.append(f"{envelope.get('id')}: references unknown task_id {task_id}")

        if kind == "claim":
            try:
                if _dt(str(envelope["lease_expires_at"])) <= _dt(str(envelope["created_at"])):
                    errors.append(f"{envelope.get('id')}: lease must expire after claim creation")
            except (KeyError, TypeError, ValueError):
                errors.append(f"{envelope.get('id')}: invalid claim timestamps")

        if kind == "execution_event" and isinstance(envelope.get("sequence"), int) and isinstance(task_id, str):
            event_sequences.setdefault(task_id, []).append(int(envelope["sequence"]))

    for task_id, sequences in event_sequences.items():
        if len(sequences) != len(set(sequences)):
            errors.append(f"{task_id}: duplicate execution event sequence")
        if sequences != sorted(sequences):
            errors.append(f"{task_id}: execution event sequence is not monotonic")

    terminal = [e for e in envelopes if e.get("type") == "result"]
    seen_result_for_task: set[str] = set()
    for envelope in terminal:
        task_id = str(envelope.get("task_id"))
        if task_id in seen_result_for_task:
            errors.append(f"{task_id}: multiple terminal Result envelopes in one lifecycle bundle")
        seen_result_for_task.add(task_id)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate semantic consistency of a DoveWAI lifecycle bundle")
    parser.add_argument("bundle", type=Path, help="JSON array of DoveWAI envelopes")
    args = parser.parse_args()
    try:
        value = json.loads(args.bundle.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if not isinstance(value, list):
        print("ERROR: lifecycle bundle must be a JSON array")
        return 2
    errors = validate_lifecycle(value)
    if errors:
        for error in errors:
            print(f"INVALID: {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
