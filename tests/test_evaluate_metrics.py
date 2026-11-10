import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "evaluation"))

from evaluate import hit_at_k  # noqa: E402


def test_hit_at_k_true_when_expected_source_within_k():
    retrieved = ["react-state.md", "react-hooks.md", "react-components.md"]
    assert hit_at_k(["react-hooks.md"], retrieved, k=3) is True


def test_hit_at_k_false_when_expected_source_outside_k():
    retrieved = ["react-state.md", "react-hooks.md", "react-components.md"]
    assert hit_at_k(["react-hooks.md"], retrieved, k=1) is False


def test_hit_at_k_false_when_no_expected_sources():
    assert hit_at_k([], ["a.md", "b.md"], k=5) is False


def test_hit_at_k_true_if_any_of_multiple_expected_sources_matches():
    retrieved = ["a.md", "b.md", "c.md"]
    assert hit_at_k(["x.md", "b.md"], retrieved, k=3) is True


def test_attribution_requires_matching_section_and_chunk():
    from evaluate import attributed

    chunk = {"source": "a.md", "section": "A", "chunk_id": 0}
    assert attributed([chunk], [chunk])
    assert not attributed([{**chunk, "section": "B"}], [chunk])
    assert not attributed([], [chunk])


def test_errors_are_visible_without_fabricating_zero_latency_or_decisions():
    from evaluate import measure

    rows = [{
        "error": "provider_timeout", "expected_sources": ["a.md"], "should_answer": True,
        "retrieval_completed": True, "retrieved_sources": ["a.md"],
    }]
    metrics = measure(rows)
    assert metrics["error_rate"] == {"passed": 1, "total": 1, "rate": 1.0}
    assert metrics["retrieval_hit_at_k"]["1"]["rate"] == 1.0
    assert metrics["abstention_accuracy"]["rate"] is None
    assert metrics["latency"]["generation"]["median_ms"] is None
