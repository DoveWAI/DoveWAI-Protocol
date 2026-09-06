#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALID_DIR = ROOT / "conformance" / "v0.2" / "valid"
INVALID_DIR = ROOT / "conformance" / "v0.2" / "invalid"


def run_validate(path: Path) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, "-m", "dovewai_protocol.cli", "validate", str(path), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"CLI returned non-JSON output for {path}: rc={proc.returncode} stdout={proc.stdout!r} stderr={proc.stderr!r}"
        ) from exc
    return proc.returncode, payload


def main() -> int:
    valid_files = sorted(VALID_DIR.glob("*.json"))
    invalid_files = sorted(INVALID_DIR.glob("*.json"))
    if not valid_files or not invalid_files:
        print("TCK requires at least one valid and one invalid vector", file=sys.stderr)
        return 2

    failures: list[str] = []
    for path in valid_files:
        rc, payload = run_validate(path)
        if rc != 0 or payload.get("valid") is not True:
            failures.append(f"expected VALID: {path.name} (rc={rc}, errors={payload.get('errors')})")
        else:
            print(f"PASS valid   {path.name}")

    for path in invalid_files:
        rc, payload = run_validate(path)
        if rc != 1 or payload.get("valid") is not False:
            failures.append(f"expected INVALID: {path.name} (rc={rc}, payload={payload})")
        else:
            print(f"PASS invalid {path.name}")

    if failures:
        print("\nTCK FAIL", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"\nTCK PASS: {len(valid_files)} valid + {len(invalid_files)} invalid vectors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
