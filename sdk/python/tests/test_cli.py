from __future__ import annotations

import json
from pathlib import Path

from dovewai_protocol.cli import main


ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "examples" / "v0.2" / "verified-work-bundle.json"
INVALID = ROOT / "conformance" / "v0.2" / "invalid" / "verified-receipt-without-verification.json"


def test_validate_valid_bundle(capsys):
    rc = main(["validate", str(EXAMPLE), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["valid"] is True
    assert payload["protocol_version"] == "0.2"


def test_validate_invalid_vector(capsys):
    rc = main(["validate", str(INVALID), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 1
    assert payload["valid"] is False
    assert payload["errors"]


def test_inspect_bundle(capsys):
    rc = main(["inspect", str(EXAMPLE), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["valid"] is True
    assert payload["objects"] >= 1
    assert payload["types"].get("WorkReceipt", 0) == 1


def test_receipt_extract(capsys):
    rc = main(["receipt", str(EXAMPLE), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert payload["type"] == "WorkReceipt"
    assert payload["protocol_version"] == "0.2"


def test_parse_error_exit_code(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not-json", encoding="utf-8")
    rc = main(["validate", str(bad), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert rc == 2
    assert payload["valid"] is False
