from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "schemas" / "v0.2" / "core.schema.json").exists():
            return parent
    raise FileNotFoundError("DoveWAI Protocol v0.2 schema not found")


def _load(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _schema_validator() -> Draft202012Validator:
    schema_path = _repo_root() / "schemas" / "v0.2" / "core.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _objects(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict) and isinstance(value.get("objects"), list):
        return value["objects"]
    if isinstance(value, dict):
        return [value]
    raise ValueError("input must be a protocol object, array of objects, or bundle with an objects array")


def _schema_errors(value: Any) -> list[str]:
    validator = _schema_validator()
    errors: list[str] = []
    for index, obj in enumerate(_objects(value)):
        for error in sorted(validator.iter_errors(obj), key=lambda e: list(e.path)):
            where = ".".join(str(p) for p in error.path)
            prefix = f"object[{index}]"
            if where:
                prefix += f".{where}"
            errors.append(f"{prefix}: {error.message}")
    return errors


def _emit(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    if payload.get("valid") is True:
        print("VALID")
    elif payload.get("valid") is False:
        print("INVALID")
        for error in payload.get("errors", []):
            print(f"- {error}")
    else:
        for key, value in payload.items():
            print(f"{key}: {value}")


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        value = _load(args.input)
        errors = _schema_errors(value)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        _emit({"valid": False, "errors": [str(exc)]}, args.json)
        return 2
    payload = {"valid": not errors, "protocol_version": "0.2", "errors": errors}
    _emit(payload, args.json)
    return 0 if not errors else 1


def cmd_inspect(args: argparse.Namespace) -> int:
    try:
        value = _load(args.input)
        objects = _objects(value)
        errors = _schema_errors(value)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        _emit({"valid": False, "errors": [str(exc)]}, args.json)
        return 2
    counts: dict[str, int] = {}
    ids: list[str] = []
    for obj in objects:
        typ = str(obj.get("type", "Unknown"))
        counts[typ] = counts.get(typ, 0) + 1
        if "id" in obj:
            ids.append(str(obj["id"]))
    payload = {
        "valid": not errors,
        "protocol_version": "0.2",
        "objects": len(objects),
        "types": counts,
        "ids": ids,
        "errors": errors,
    }
    if args.json:
        _emit(payload, True)
    else:
        print(f"protocol_version: 0.2\nobjects: {len(objects)}\nvalid: {not errors}")
        for typ, count in sorted(counts.items()):
            print(f"{typ}: {count}")
        if errors:
            print("errors:")
            for error in errors:
                print(f"- {error}")
    return 0 if not errors else 1


def cmd_receipt(args: argparse.Namespace) -> int:
    try:
        value = _load(args.input)
        objects = _objects(value)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        _emit({"valid": False, "errors": [str(exc)]}, args.json)
        return 2
    receipts = [obj for obj in objects if obj.get("type") == "WorkReceipt"]
    if args.id:
        receipts = [obj for obj in receipts if obj.get("id") == args.id]
    if not receipts:
        _emit({"valid": False, "errors": ["no matching WorkReceipt found"]}, args.json)
        return 1
    if args.json:
        print(json.dumps(receipts[0] if len(receipts) == 1 else receipts, indent=2, sort_keys=True))
    else:
        for receipt in receipts:
            print(f"{receipt.get('id')}: status={receipt.get('status')} task={receipt.get('task_id')} result={receipt.get('result_id')}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dovewai", description="DoveWAI Protocol v0.2 CLI")
    parser.add_argument("--version", action="version", version="DoveWAI Protocol CLI 0.2.0")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate v0.2 protocol JSON")
    validate.add_argument("input", help="JSON file or - for stdin")
    validate.add_argument("--json", action="store_true", help="machine-readable output")
    validate.set_defaults(func=cmd_validate)

    inspect = sub.add_parser("inspect", help="summarize a v0.2 object or bundle")
    inspect.add_argument("input", help="JSON file or - for stdin")
    inspect.add_argument("--json", action="store_true", help="machine-readable output")
    inspect.set_defaults(func=cmd_inspect)

    receipt = sub.add_parser("receipt", help="show WorkReceipt records")
    receipt.add_argument("input", help="JSON file or - for stdin")
    receipt.add_argument("--id", help="select a WorkReceipt by id")
    receipt.add_argument("--json", action="store_true", help="machine-readable output")
    receipt.set_defaults(func=cmd_receipt)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
