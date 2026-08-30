from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


def _default_schema() -> Path:
    here = Path(__file__).resolve()
    repo_candidate = here.parents[4] / "schemas" / "v0.1" / "core.schema.json"
    if repo_candidate.exists():
        return repo_candidate
    raise FileNotFoundError("DoveWAI v0.1 schema not found; pass schema_path explicitly")


def validate_envelope(envelope: dict[str, Any], schema_path: str | Path | None = None) -> list[str]:
    path = Path(schema_path) if schema_path else _default_schema()
    schema = json.loads(path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [error.message for error in sorted(validator.iter_errors(envelope), key=lambda e: list(e.path))]
