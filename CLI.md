# DoveWAI Protocol CLI

The v0.2 CLI makes the public protocol usable from terminals, scripts, CI systems, and other developer tools.

## Install from source

```bash
python -m pip install ./sdk/python
```

## Validate

```bash
dovewai validate examples/v0.2/verified-work-bundle.json
```

Validation has two layers:

1. each protocol object must validate against the canonical public v0.2 JSON Schema;
2. multi-object bundles must satisfy the shared v0.2 lifecycle invariants used by the conformance tooling.

Use `--json` for stable machine-readable output:

```bash
dovewai validate examples/v0.2/verified-work-bundle.json --json
```

Exit codes:

- `0`: valid / command succeeded
- `1`: protocol validation failed or requested protocol record was not found
- `2`: input/read/JSON error

## Inspect

```bash
dovewai inspect examples/v0.2/verified-work-bundle.json
```

This summarizes object counts, types, IDs, protocol version, and schema/lifecycle validity without requiring a UI.

## WorkReceipt

```bash
dovewai receipt examples/v0.2/verified-work-bundle.json
```

Select one receipt when a bundle contains several:

```bash
dovewai receipt bundle.json --id receipt-123 --json
```

## Standard input

All commands accept `-` to read JSON from stdin:

```bash
cat bundle.json | dovewai validate - --json
```

## Conformance / TCK

The repository includes a black-box CLI conformance runner:

```bash
python tools/tck_v02.py
```

It executes the installed CLI against every JSON vector in `conformance/v0.2/valid` and `conformance/v0.2/invalid`, requiring valid vectors to exit `0` and invalid vectors to exit `1`.

## Design rule

The CLI must not maintain a second interpretation of protocol semantics. Object structure comes from the canonical public v0.2 JSON Schema and cross-object semantics come from the shared `dovewai_protocol.lifecycle` validator used by the lifecycle tool and CLI.
