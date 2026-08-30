# DoveWAI Protocol Python SDK

Reference helpers for constructing, validating, and adapting DoveWAI Protocol v0.1 envelopes.

```bash
python -m pip install -e sdk/python
```

```python
from dovewai_protocol import task, result

work = task("task:demo:1", "Summarize a document", {"document_id": "doc-1"})
outcome = result("result:demo:1", work["id"], "succeeded", {"summary": "..."})
```

Validation uses the canonical JSON Schema shipped with the source repository. Applications distributing this package independently should provide the schema path explicitly or vendor the published v0.1 schema alongside the package.
