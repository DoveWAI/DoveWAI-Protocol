#!/usr/bin/env python3
"""Reference validator for DoveWAI Protocol JSON envelopes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "v0.1" / "core.schema.json"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(instance_path: Path, schema_path: Path = DEFAULT_SCHEMA) -> list[str]:
    schema = load_json(schema_path)
    instance = load_json(instance_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a DoveWAI Protocol v0.1 JSON envelope")
    parser.add_argument("instance", type=Path, help="Path to one protocol envelope JSON file")
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA, help="Schema path")
    args = parser.parse_args()

    try:
        errors = validate(args.instance, args.schema)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if errors:
        for message in errors:
            print(f"INVALID: {message}")
        return 1

    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
