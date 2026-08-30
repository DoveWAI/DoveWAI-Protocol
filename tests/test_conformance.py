from pathlib import Path

from tools.validate import validate


ROOT = Path(__file__).resolve().parents[1]


def test_valid_vectors_pass():
    valid_dir = ROOT / "conformance" / "v0.1" / "valid"
    vectors = sorted(valid_dir.glob("*.json"))
    assert vectors, "expected at least one valid conformance vector"
    for vector in vectors:
        assert validate(vector) == [], vector


def test_invalid_vectors_fail():
    invalid_dir = ROOT / "conformance" / "v0.1" / "invalid"
    vectors = sorted(invalid_dir.glob("*.json"))
    assert vectors, "expected at least one invalid conformance vector"
    for vector in vectors:
        assert validate(vector), vector
