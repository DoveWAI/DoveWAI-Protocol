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

This summarizes object counts, types, IDs, protocol version, and structural validity without requiring a UI.

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

## Design rule

The CLI validates against the canonical public v0.2 JSON Schema. It must not maintain a separate hard-coded interpretation of protocol object structure. Lifecycle/TCK integration will extend this CLI while preserving that rule.
