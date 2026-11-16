"""Contratos, transações e recuperação do ciclo de estudo, sem provedores reais."""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import Mock
from uuid import uuid4

import httpx
import pytest
from fastapi.testclient import TestClient
from openai import APITimeoutError

import api
import learning_service as service
import learning_store as storage
from chunking import build_records
from learning_models import GenerateRequest, ReviewRequest
from learning_service import LearningService
from learning_store import LearningStore, digest
from providers import ServiceError
from review_schedule import advance, stamp

NOW = datetime(2026, 11, 12, 15, tzinfo=timezone.utc)
CARD = {
    "question": "Como retirar README.md do staging sem perder suas edições?",
    "reference_answer": "Use git restore --staged README.md. Isso preserva as edições locais.",
    "explanation": "O comando altera o staging sem descartar as edições no diretório de trabalho.",
    "concepts": ["git restore --staged README.md", "Preservar edições locais"],
    "citations": ["S1"], "difficulty": "medium",
}
EVALUATION = {
    "grade": "correct", "present_concepts": CARD["concepts"], "missing_concepts": [], "errors": [],
    "feedback": "Você identificou o comando e a preservação das edições locais.", "citations": ["S1"],
}


def completion(payload, finish_reason="stop", refusal=None):
    return SimpleNamespace(
        choices=[SimpleNamespace(finish_reason=finish_reason, message=SimpleNamespace(
            content=json.dumps(payload, ensure_ascii=False), refusal=refusal))],
        usage=SimpleNamespace(prompt_tokens=120, completion_tokens=70, total_tokens=190,
                              prompt_tokens_details=SimpleNamespace(cached_tokens=0)), model="resolved-test-model",
    )


@pytest.fixture
def setup(tmp_path, monkeypatch):
    now = [NOW]
    store = LearningStore(tmp_path / "study.sqlite3", clock=lambda: now[0])
    monkeypatch.setattr(api, "get_store", lambda: store)
    import learning_api
    monkeypatch.setattr(learning_api, "get_store", lambda: store)
    monkeypatch.setenv("PINECONE_API_KEY", "test")
    monkeypatch.setenv("OPENAI_API_KEY", "test")
    records = [r for r in build_records() if r.get("module") == "devmind" and r.get("topic") == "git"]
    record = next(r for r in records if "--staged" in r["chunk_text"])
    hit = SimpleNamespace(fields=record, score=0.95)
    retrieval, model = Mock(return_value=[hit]), Mock()
    monkeypatch.setattr(service, "retrieve", retrieval)
    monkeypatch.setattr(service, "openai_client", lambda: model)
    generate = model.chat.completions.create
    generate.return_value = completion({"cards": [CARD]})
    svc = LearningService(store)
    request = GenerateRequest.model_validate_json(json.dumps({
        "request_id": str(uuid4()), "module": "devmind", "topic": "git", "count": 1,
        "source": record["source"], "focus": "Retirar README.md do staging mantendo as edições",
    }))
    return SimpleNamespace(store=store, svc=svc, request=request, model=generate, retrieval=retrieval,
                           record=record, hit=hit, now=now, client=TestClient(api.app))


def generate(s):
    return s.svc.generate(s.request)["cards"][0]


def review(s, card, answer="Eu tiraria só do índice com git restore --staged README.md, mantendo o arquivo editado.", **changes):
    s.model.return_value = completion({**EVALUATION, **changes})
    request = ReviewRequest.model_validate_json(json.dumps({"request_id": str(uuid4()), "answer": answer}))
    return request, s.svc.review(card["id"], request)


def test_generation_persists_snapshot_and_hides_solution(setup):
    s = setup
    card = generate(s)
    assert "reference_answer" not in card and "concepts" not in card
    assert card["sources"][0]["text_sha256"] == digest(s.record["chunk_text"])
    restarted = LearningStore(s.store.path, clock=lambda: NOW)
    private = restarted.card(card["id"], private=True)
    assert private["reference_answer"] == CARD["reference_answer"]
    assert private["explanation"] in s.record["chunk_text"]
    assert private["evidence"][0]["chunk_text"] == s.record["chunk_text"]
    assert restarted.progress()["due"] == 1
    assert s.retrieval.call_args.kwargs["source"] == s.record["source"]
    options = s.model.call_args.kwargs
    assert options["response_format"]["json_schema"]["strict"] and options["store"] is False
    assert options["max_completion_tokens"] == 2400


@pytest.mark.parametrize("mutation", [
    {"citations": ["S99"]}, {"question": " "}, {"concepts": []}, {"difficulty": "impossible"},
    {"reference_answer": "x" * 1201}, {"invented": "field"},
])
def test_generation_rejects_invalid_structure_and_invented_sources(setup, mutation):
    s = setup
    s.model.return_value = completion({"cards": [{**CARD, **mutation}]})
    with pytest.raises(ServiceError) as exc:
        generate(s)
    assert exc.value.status == 502
    assert s.store.progress()["total"] == 0
    with s.store.connection() as db:
        assert db.execute("SELECT state FROM operations").fetchone()[0] == "failed"
        trace = json.loads(db.execute("SELECT trace_json FROM provider_runs").fetchone()[0])
        assert trace["openai_usage"]["total_tokens"] == 190


@pytest.mark.parametrize("cards", [[CARD, CARD], [], [CARD]])
def test_count_duplicates_and_abstention_are_atomic(setup, cards):
    s = setup
    s.request.count = 2
    s.model.return_value = completion({"cards": cards})
    with pytest.raises(ServiceError):
        generate(s)
    assert s.store.progress()["total"] == 0


def test_provider_metadata_must_belong_to_selected_local_scope(setup):
    s = setup
    s.hit.fields = {**s.record, "source": "DEVMIND/Git/invented.md"}
    with pytest.raises(ServiceError) as exc:
        generate(s)
    assert exc.value.code == "insufficient_evidence"
    s.model.assert_not_called()


@pytest.mark.parametrize("scope", [{"module": "unknown"}, {"topic": "unknown"}, {"source": "../.env"}])
def test_invalid_scope_never_calls_provider(setup, scope):
    s = setup
    for key, value in scope.items():
        setattr(s.request, key, value)
    with pytest.raises(ServiceError) as exc:
        generate(s)
    assert exc.value.status == 422
    s.model.assert_not_called()
    assert all(item["used"] == 0 for item in s.store.progress()["usage"].values())


def test_generation_idempotency_and_duplicate_library_question(setup):
    s = setup
    first = s.svc.generate(s.request)
    assert s.svc.generate(s.request) == first
    s.model.assert_called_once()
    s.request.request_id = uuid4()
    assert s.svc.generate(s.request)["cards"][0]["id"] == first["cards"][0]["id"]
    assert s.store.progress()["total"] == 1
    s.request.focus = "different"
    with pytest.raises(ServiceError) as exc:
        s.svc.generate(s.request)
    assert exc.value.status == 409


def test_generation_replay_survives_local_scope_removal(setup, monkeypatch):
    s = setup
    first = s.svc.generate(s.request)
    monkeypatch.setattr(service, "guide_as_list", lambda: [])
    assert s.svc.generate(s.request) == first
    s.model.assert_called_once()


def test_generation_rejects_duplicate_answers_with_distinct_questions(setup):
    s = setup
    s.request.count = 2
    s.model.return_value = completion({"cards": [CARD, {**CARD, "question": "Qual comando retira o arquivo da área de preparação?"}]})
    with pytest.raises(ServiceError):
        generate(s)
    assert s.store.progress()["total"] == 0


def test_generation_timeout_can_retry_without_partial_cards(setup):
    s = setup
    s.model.side_effect = APITimeoutError(request=httpx.Request("POST", "https://example.invalid"))
    with pytest.raises(ServiceError):
        generate(s)
    assert s.store.progress()["total"] == 0
    s.model.side_effect = None
    assert generate(s)["id"]
    assert s.store.progress()["total"] == 1


def test_foreign_learner_card_cannot_be_read_or_reviewed(setup):
    s = setup
    card = generate(s)
    with s.store.connection(write=True) as db:
        db.execute("INSERT INTO learners VALUES ('other', 'UTC', ?)", (stamp(NOW),))
        db.execute("UPDATE cards SET user_id='other' WHERE id=?", (card["id"],))
        db.execute("UPDATE review_schedule SET user_id='other' WHERE card_id=?", (card["id"],))
    assert s.client.get(f"/learning/cards/{card['id']}").status_code == 404
    assert s.client.post(f"/learning/cards/{card['id']}/reviews", json={"request_id": str(uuid4()), "answer": "Olá"}).status_code == 404
    assert s.client.get("/learning/progress").json()["total"] == 0
    assert s.client.get("/learning/due").json()["cards"] == []


def test_recorded_real_outputs_replay_through_current_service(setup):
    from pathlib import Path
    s = setup
    report = json.loads(Path("evaluation/learning-live-2026-11-12.json").read_text())
    s.model.side_effect = [completion(payload) for payload in report["structured_outputs"]]
    card = generate(s)
    for case in report["reviews"]:
        request = ReviewRequest(request_id=uuid4(), answer=case["answer"])
        result = s.svc.review(card["id"], request)
        assert result["grade"] == case["expected"]
        assert result["explanation"] in s.record["chunk_text"]
        rated = s.store.rate(result["review_id"], case["result"]["self_recall"])
        assert rated["schedule"]["interval_days"] == case["result"]["schedule"]["interval_days"]
    assert s.store.progress()["attempts"] == 3


def test_unverifiable_generated_explanation_is_replaced_by_source_excerpt(setup):
    s = setup
    s.model.return_value = completion({"cards": [{**CARD, "explanation": "Este comando não altera o próximo commit."}]})
    card = generate(s)
    stored = s.store.card(card["id"], private=True)
    assert stored["explanation"] in s.record["chunk_text"]
    assert "Este comando não altera" not in stored["explanation"]


def test_regenerating_changed_evidence_creates_a_new_version(setup):
    s = setup
    first = generate(s)
    s.request.request_id = uuid4()
    s.hit.fields = {**s.record, "chunk_text": s.record["chunk_text"] + "\nDetalhe novo."}
    second = generate(s)
    assert first["id"] != second["id"]
    assert first["sources"][0]["text_sha256"] != second["sources"][0]["text_sha256"]
    assert s.store.card(first["id"], private=True)["evidence"][0]["chunk_text"] == s.record["chunk_text"]


def test_module_generation_infers_topic_from_evidence(setup):
    s = setup
    s.request.topic = None
    assert generate(s)["topic"] == "git"


def test_semantic_evaluation_uses_saved_rubric_and_no_new_retrieval(setup):
    s = setup
    card = generate(s)
    _, result = review(s, card)
    assert result["grade"] == "correct" and result["schedule"]["interval_days"] == 1
    payload = json.loads(s.model.call_args.kwargs["messages"][-1]["content"])
    assert payload["expected_concepts"] == CARD["concepts"]
    assert payload["evidence"] == [{"id": "S1", "text": s.record["chunk_text"]}]
    assert "mantendo o arquivo" in payload["student_answer"]
    s.retrieval.assert_called_once()
    assert s.store.card(card["id"])["latest_attempt"]["result"]["review_id"] == result["review_id"]


@pytest.mark.parametrize("changes", [
    {"citations": ["S99"]}, {"citations": []}, {"feedback": " "},
    {"grade": "correct", "missing_concepts": ["important"]},
    {"grade": "correct", "errors": ["wrong"]}, {"grade": "correct", "present_concepts": []},
])
def test_invalid_feedback_preserves_answer_and_calendar(setup, changes):
    s = setup
    card = generate(s)
    with pytest.raises(ServiceError):
        review(s, card, **changes)
    current = s.store.card(card["id"])
    assert current["schedule"]["reviews"] == 0
    assert current["latest_attempt"]["state"] == "failed"
    assert "git restore" in current["latest_attempt"]["answer"]


def test_feedback_cannot_introduce_code_absent_from_evidence(setup):
    s = setup
    card = generate(s)
    with pytest.raises(ServiceError):
        review(s, card, feedback="Use `git reset --hard` para resolver.")
    assert s.store.card(card["id"])["schedule"]["reviews"] == 0


def test_provider_timeout_retry_and_replay_do_not_duplicate_progress(setup):
    s = setup
    card = generate(s)
    request = ReviewRequest(request_id=uuid4(), answer="Não sei")
    s.model.side_effect = APITimeoutError(request=httpx.Request("POST", "https://example.invalid"))
    with pytest.raises(ServiceError) as exc:
        s.svc.review(card["id"], request)
    assert exc.value.status == 504
    restored = LearningStore(s.store.path, clock=lambda: NOW).card(card["id"])
    assert restored["latest_attempt"]["answer"] == "Não sei"
    s.model.side_effect = None
    s.model.return_value = completion(EVALUATION)
    result = s.svc.review(card["id"], request)
    assert s.svc.review(card["id"], request) == result
    assert s.store.progress()["attempts"] == 1
    assert s.store.card(card["id"])["schedule"]["reviews"] == 1
    assert s.store.progress()["usage"]["review"]["used"] == 2
    request.answer = "Outra resposta"
    with pytest.raises(ServiceError) as exc:
        s.svc.review(card["id"], request)
    assert exc.value.status == 409


@pytest.mark.parametrize("grade,stage,days", [("correct", 1, 1), ("partial", 0, 1), ("incorrect", 0, 1), ("ungradable", 0, 0)])
def test_grade_schedule_and_ungradable(setup, grade, stage, days):
    s = setup
    card = generate(s)
    _, result = review(s, card, grade=grade)
    assert result["schedule"]["stage"] == stage
    assert result["schedule"]["interval_days"] == days
    assert result["schedule"]["reviews"] == int(grade != "ungradable")


def test_self_recall_overrides_ai_without_second_review(setup):
    s = setup
    card = generate(s)
    request, result = review(s, card)
    manual = s.store.rate(result["review_id"], "again")
    assert manual["grade"] == "correct" and manual["self_recall"] == "again"
    assert manual["schedule"]["stage"] == 0 and manual["schedule"]["reviews"] == 1
    assert manual["schedule"]["lapses"] == 1
    assert s.store.rate(result["review_id"], "again") == manual
    assert s.svc.review(card["id"], request) == manual
    with pytest.raises(ServiceError) as exc:
        s.store.rate(result["review_id"], "easy")
    assert exc.value.status == 409


def test_ungradable_can_be_self_assessed_without_ai(setup):
    s = setup
    card = generate(s)
    _, result = review(s, card, grade="ungradable")
    calls = s.model.call_count
    manual = s.store.rate(result["review_id"], "easy")
    assert manual["schedule"]["reviews"] == 1 and manual["schedule"]["interval_days"] == 3
    assert s.model.call_count == calls


def test_old_review_cannot_override_newer_calendar(setup):
    s = setup
    card = generate(s)
    _, first = review(s, card)
    s.now[0] += timedelta(seconds=1)
    review(s, card)
    with pytest.raises(ServiceError) as exc:
        s.store.rate(first["review_id"], "again")
    assert exc.value.status == 409


def test_daily_materialized_once_progress_and_local_midnight(setup):
    s = setup
    card = generate(s)
    daily = s.store.daily()
    assert len(daily["cards"]) == 1 and daily["completed"] == 0
    assert s.store.daily() == daily
    review(s, card)
    assert s.store.daily()["completed"] == 1
    assert s.store.progress()["topics"][0]["reviewed"] == 1
    s.now[0] = datetime(2026, 11, 13, 2, 59, tzinfo=timezone.utc)
    assert s.store.daily()["id"] == daily["id"]
    s.now[0] += timedelta(minutes=1)
    tomorrow = s.store.daily()
    assert tomorrow["id"] != daily["id"] and tomorrow["local_date"] == "2026-11-13"


def test_empty_daily_is_stable_even_if_cards_are_generated_later(setup):
    s = setup
    empty = s.store.daily()
    generate(s)
    assert s.store.daily() == empty
    assert len(s.store.due()["cards"]) == 1


def test_concurrent_reservations_and_daily_sessions(setup):
    s = setup
    card = generate(s)
    request_id = str(uuid4())
    payload = {"card_id": card["id"], "answer": "Não sei"}
    def reserve(_):
        try:
            return s.store.claim("review", request_id, payload, card["id"])
        except ServiceError as exc:
            return exc.status
    with ThreadPoolExecutor(max_workers=4) as pool:
        reservations = list(pool.map(reserve, range(4)))
        sessions = list(pool.map(lambda _: s.store.daily(), range(4)))
    assert sum(isinstance(r, dict) for r in reservations) == 1
    assert reservations.count(409) == 3
    assert len({session["id"] for session in sessions}) == 1
    with s.store.connection() as db:
        assert db.execute("SELECT count(*) FROM daily_assignments").fetchone()[0] == 1


def test_expired_lease_can_be_reclaimed_and_late_worker_cannot_commit(setup):
    s = setup
    card = generate(s)
    request_id, payload = str(uuid4()), {"card_id": card["id"], "answer": "Preservo o arquivo"}
    first = s.store.claim("review", request_id, payload, card["id"])
    s.now[0] += timedelta(seconds=121)
    second = s.store.claim("review", request_id, payload, card["id"])
    assert first["token"] != second["token"]
    from learning_models import Evaluation
    with pytest.raises(ServiceError):
        s.store.save_review(request_id, first["token"], Evaluation(**EVALUATION), "model", {})
    assert s.store.progress()["attempts"] == 0
    s.store.save_review(request_id, second["token"], Evaluation(**EVALUATION), "model", {})
    assert s.store.progress()["attempts"] == 1


def test_distinct_pending_reviews_for_same_card_are_serialized(setup):
    s = setup
    card = generate(s)
    s.store.claim("review", str(uuid4()), {"answer": "a"}, card["id"])
    with pytest.raises(ServiceError) as exc:
        s.store.claim("review", str(uuid4()), {"answer": "b"}, card["id"])
    assert exc.value.status == 409


def test_daily_quota_charges_failures_but_not_replays(setup, monkeypatch):
    s = setup
    monkeypatch.setitem(storage.LIMITS, "generation", 1)
    card = generate(s)
    assert generate(s)["id"] == card["id"]
    s.request.request_id = uuid4()
    with pytest.raises(ServiceError) as exc:
        generate(s)
    assert exc.value.status == 429 and s.model.call_count == 1


def test_changed_source_keeps_snapshot_and_marks_version(setup, monkeypatch):
    s = setup
    card = generate(s)
    import guide
    monkeypatch.setattr(guide, "read_guide_document", lambda _: "# Arquivo editado")
    public = s.store.card(card["id"])
    assert public["sources"][0]["source_changed"] is True
    _, result = review(s, card)
    assert result["sources"][0]["chunk_text"] == s.record["chunk_text"]


@pytest.mark.parametrize("payload", [
    {}, {"request_id": "bad", "module": "devmind"},
    {"request_id": str(uuid4()), "module": "devmind", "count": 4},
    {"request_id": str(uuid4()), "module": "devmind", "count": "1"},
    {"request_id": str(uuid4()), "module": "devmind", "focus": "private-answer" * 200},
    {"request_id": str(uuid4()), "module": "devmind", "learner_id": "another-person"},
])
def test_api_validates_without_echoing_private_data(setup, payload):
    response = setup.client.post("/learning/cards", json=payload)
    assert response.status_code == 422 and "private-answer" not in response.text
    setup.model.assert_not_called()


@pytest.mark.parametrize("headers", [{"origin": "https://evil.example"}, {"origin": "null"}])
def test_origin_guard_blocks_foreign_origins(setup, headers):
    assert setup.client.get("/learning/progress", headers=headers).status_code == 403
    assert setup.client.post("/ask", headers=headers, json={"question": "Olá"}).status_code == 403
    setup.model.assert_not_called()


def test_network_peer_cannot_spend_or_read_local_progress(setup):
    from fastapi import HTTPException
    from starlette.requests import Request
    from local_access import local_demo_access
    request = Request({"type": "http", "scheme": "http", "server": ("localhost", 8000),
                       "client": ("10.0.0.5", 4321), "path": "/learning/progress", "headers": []})
    with pytest.raises(HTTPException) as exc:
        local_demo_access(request)
    assert exc.value.status_code == 403


def test_unknown_resources_and_bounded_due(setup):
    assert setup.client.get(f"/learning/cards/{uuid4()}").status_code == 404
    assert setup.client.post(f"/learning/reviews/{uuid4()}/recall", json={"recall": "good"}).status_code == 404
    assert setup.client.get("/learning/due?limit=1000").status_code == 422


def test_complete_http_study_cycle_and_restart(setup):
    s = setup
    response = s.client.post("/learning/cards", json=s.request.model_dump(mode="json"))
    assert response.status_code == 200, response.text
    card = response.json()["cards"][0]
    daily = s.client.get("/learning/daily").json()
    request_id = str(uuid4())
    s.model.return_value = completion(EVALUATION)
    payload = {"request_id": request_id, "answer": "Eu retiraria do índice, preservando o arquivo editado."}
    response = s.client.post(f"/learning/cards/{card['id']}/reviews", json=payload)
    assert response.status_code == 200, response.text
    result = response.json()
    rated = s.client.post(f"/learning/reviews/{result['review_id']}/recall", json={"recall": "easy"})
    assert rated.status_code == 200
    assert rated.json()["schedule"]["due_at"] == stamp(NOW + timedelta(days=3))
    assert s.client.get("/learning/daily").json()["id"] == daily["id"]
    assert s.client.get("/learning/daily").json()["completed"] == 1
    assert s.client.get("/learning/progress").json()["due"] == 0
    replay = s.client.post(f"/learning/cards/{card['id']}/reviews", json=payload)
    assert replay.json() == rated.json()
    restarted = LearningStore(s.store.path, clock=lambda: NOW)
    assert restarted.progress()["attempts"] == 1
    assert restarted.card(card["id"])["latest_attempt"]["answer"] == payload["answer"]


def test_due_prioritizes_overdue_then_lapses_and_difficulty(setup):
    s = setup
    cards = []
    for n in range(3):
        s.request.request_id = uuid4()
        s.model.return_value = completion({"cards": [{**CARD, "question": f"Pergunta {n} sobre Git?"}]})
        cards.append(generate(s))
    with s.store.connection(write=True) as db:
        db.execute("UPDATE review_schedule SET lapses=3 WHERE card_id=?", (cards[1]["id"],))
        db.execute("UPDATE review_schedule SET due_at=? WHERE card_id=?", (stamp(NOW - timedelta(days=1)), cards[2]["id"]))
    assert [c["id"] for c in s.store.due()["cards"]] == [cards[2]["id"], cards[1]["id"], cards[0]["id"]]


def test_pure_scheduler_all_intervals_and_failure_reset():
    previous = {"stage": 0, "reviews": 0, "lapses": 0, "version": 0}
    for expected in (1, 3, 7, 14, 30, 30):
        previous = advance(previous, "good", NOW)
        assert previous["interval_days"] == expected
        assert previous["due_at"] == stamp(NOW + timedelta(days=expected))
    hard = advance(previous, "hard", NOW)
    assert hard["stage"] == previous["stage"] and hard["interval_days"] == 1
    again = advance(hard, "again", NOW)
    assert again["stage"] == 0 and again["lapses"] == 1 and again["reviews"] == 8
    with pytest.raises(ValueError):
        advance(previous, "invalid", NOW)
    with pytest.raises(ValueError):
        stamp(datetime(2026, 11, 12))
