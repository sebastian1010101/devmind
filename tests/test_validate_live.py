import json
from types import SimpleNamespace
from unittest.mock import Mock

from evaluation import validate_live
from providers import ServiceError


def test_partial_live_write_cleans_only_owned_ids_and_restores_config(tmp_path, monkeypatch):
    output = tmp_path / "report.json"
    monkeypatch.setattr("sys.argv", ["validate_live.py", "--live", "--output", str(output)])
    monkeypatch.setenv("PINECONE_API_KEY", "fixture")
    monkeypatch.setenv("OPENAI_API_KEY", "fixture")
    record = {"_id": "test-id", "chunk_text": "Evidence"}
    monkeypatch.setattr(validate_live, "scan_corpus", lambda *a, **kw: (
        SimpleNamespace(failed=[], documents_indexed=1), [record],
    ))
    index = Mock()
    description = Mock(status=SimpleNamespace(ready=True))
    description.to_dict.return_value = {"schema": {"fields": {"chunk_text": {
        "type": "semantic_text", "model": "llama-text-embed-v2",
        "read_parameters": {"dimension": 1024}, "write_parameters": {"dimension": 1024},
    }}}}
    pc = Mock()
    pc.describe_index.return_value = description
    monkeypatch.setattr(validate_live, "pinecone_client", lambda: pc)
    monkeypatch.setattr(validate_live, "pinecone_index", lambda: index)
    monkeypatch.setattr(validate_live, "openai_client", lambda: SimpleNamespace(
        models=SimpleNamespace(retrieve=lambda model: SimpleNamespace(id=model)),
    ))
    monkeypatch.setattr(validate_live, "listed_ids", lambda *a: set())
    monkeypatch.setattr(validate_live, "upsert", Mock(side_effect=ServiceError("provider_timeout", "private", 504)))
    original_namespace = validate_live.settings.namespace

    assert validate_live.main() == 1

    report = json.loads(output.read_text())
    namespace = report["config"]["namespace"]
    assert namespace.startswith("devmind-validation-") and namespace != original_namespace
    index.delete.assert_called_once_with(namespace=namespace, ids=["test-id"])
    assert validate_live.settings.namespace == original_namespace
    assert report["cleanup"] == {"attempted": True, "verified": True}
    assert report["error"] == {"code": "provider_timeout", "http_status": 504}
    assert "private" not in output.read_text()
