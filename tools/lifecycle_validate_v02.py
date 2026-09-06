#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SDK_SRC = ROOT / "sdk" / "python" / "src"
if str(SDK_SRC) not in sys.path:
    sys.path.insert(0, str(SDK_SRC))

from dovewai_protocol.lifecycle import validate_bundle  # noqa: E402


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} BUNDLE.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 2

    objects = data if isinstance(data, list) else data.get("objects") if isinstance(data, dict) else None
    if not isinstance(objects, list):
        print("bundle must be a JSON array or an object containing an objects array", file=sys.stderr)
        return 2
    try:
        validate_bundle(objects)
    except (ValueError, KeyError, TypeError) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print("VALID: DoveWAI Protocol v0.2 lifecycle")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
