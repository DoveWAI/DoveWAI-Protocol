# DoveWAI Protocol Python SDK

Reference Python SDK and CLI for DoveWAI Protocol.

## v0.2 source install

From the repository root:

```bash
python -m pip install ./sdk/python
```

The installed package includes the v0.2 schema required by the `dovewai` CLI, so validation does not depend on a source checkout.

```bash
dovewai validate examples/v0.2/verified-work-bundle.json
dovewai inspect examples/v0.2/verified-work-bundle.json --json
dovewai receipt examples/v0.2/verified-work-bundle.json --json
```

The legacy top-level Python helpers remain the v0.1 compatibility surface. v0.2 builders are exposed under `dovewai_protocol.v02`.

```python
from dovewai_protocol import v02

work = v02.task("task:demo:1", "Summarize a document")
```

See the repository-level `CLI.md`, `ADOPTION.md`, and `RELEASE.md` for the full public adoption and release path.

## Publishing status

Version `0.2.0` in source metadata does not by itself mean the package has been published to PyPI. Confirm the registry release before documenting `pip install dovewai-protocol` as a public registry install command.
