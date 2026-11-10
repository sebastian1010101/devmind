from stats import compute_stats


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_compute_stats_counts_discovered_and_indexed(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "MOD" / "a.md", "# A\n\n## Sección\ncontenido real\n")
    _write(root / "MOD" / "b.md", "# B\n\n## Otra\nmás contenido\n")

    stats = compute_stats(root)
    assert stats.documents_discovered == 2
    assert stats.documents_indexed == 2
    assert stats.chunks_created > 0


def test_compute_stats_detects_empty_documents(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "MOD" / "vacio.md", "   \n\n  ")
    _write(root / "MOD" / "lleno.md", "# X\n\n## S\ncontenido\n")

    stats = compute_stats(root)
    assert len(stats.empty) == 1
    assert stats.documents_indexed == 1


def test_compute_stats_detects_duplicates(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "MOD" / "uno.md", "# Doc\n\n## S\ncontenido igual\n")
    _write(root / "MOD" / "dos.md", "# Doc\n\n## S\ncontenido   igual\n")

    stats = compute_stats(root)
    assert len(stats.duplicates) == 1


def test_as_dict_has_expected_keys(tmp_path):
    root = tmp_path / "knowledge"
    _write(root / "MOD" / "a.md", "# A\n\n## S\ncontenido\n")

    result = compute_stats(root).as_dict()
    assert set(result) == {
        "documents_discovered",
        "documents_indexed",
        "failed",
        "empty",
        "duplicates",
        "chunks_created",
        "avg_chunks_per_document",
        "min_chunk_length",
        "max_chunk_length",
        "avg_chunk_length",
    }
