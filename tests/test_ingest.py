from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from pinecone import ApiError

from chunking import record_prefix
from ingest import upsert
from providers import ServiceError
from stats import scan_corpus


def test_scan_validates_markdown_and_only_counts_valid_chunks(tmp_path):
    (tmp_path / "valid.MD").write_text("# Válido\nTexto", encoding="utf-8")
    (tmp_path / "empty.md").touch()
    (tmp_path / "binary.md").write_bytes(b"text\x00")
    (tmp_path / "oversized.md").write_bytes(b"a" * (512 * 1024 + 1))
    (tmp_path / "invalid.md").write_bytes(b"\xff")
    (tmp_path / "symlink.md").symlink_to(tmp_path / "valid.MD")
    stats, records = scan_corpus(tmp_path, collect_records=True)
    assert stats.documents_discovered == 6
    assert len(stats.failed) == 4
    assert len(stats.empty) == 1
    assert stats.chunks_created == len(records) == 1


def test_upsert_is_repeatable_and_prune_uses_only_managed_module_ids():
    index = Mock()
    module = "git"
    current, stale = (record_prefix(module) + suffix for suffix in ("a-0", "a-1"))
    unrelated = [record_prefix("python") + "a-1", "legacy-id"]
    index.list.return_value = [
        SimpleNamespace(vectors=[SimpleNamespace(id=value) for value in [current, stale, *unrelated]])
    ]
    for _ in range(2):
        upsert(index, [{"_id": current}], "test", prune=True, module=module)
    assert index.list.call_args.kwargs["prefix"] == record_prefix(module)
    assert index.upsert_records.call_args.kwargs["records"] == [{"_id": current}]
    index.delete.assert_called_with(namespace="test", ids=[stale])
    assert [call[0] for call in index.method_calls] == ["list", "upsert_records", "delete"] * 2


def test_failed_later_batch_never_deletes_stale_ids():
    index = Mock()
    index.list.return_value = [SimpleNamespace(vectors=[SimpleNamespace(id="dm1-stale")])]
    index.upsert_records.side_effect = [None, ApiError("provider body", 500)]
    with pytest.raises(ServiceError):
        upsert(index, [{"_id": f"dm1-{n}"} for n in range(91)], "test", prune=True)
    assert index.upsert_records.call_count == 2
    index.delete.assert_not_called()
