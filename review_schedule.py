"""Heurística determinista de revisão. Datas UTC; nunca usa um LLM.

Good avança por 1, 3, 7, 14 e 30 dias. Easy pula uma etapa (mínimo
3 dias). Hard mantém a etapa e volta em 1 dia. Again reinicia em 1 dia.
Não se afirma equivalência com o SM-2 nem domínio definitivo do conceito.
"""

from datetime import datetime, timedelta, timezone

INTERVALS = (1, 3, 7, 14, 30)
GRADE_RECALL = {"correct": "good", "partial": "hard", "incorrect": "again"}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def stamp(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("A data deve incluir fuso horário.")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds")


def advance(previous: dict, recall: str, now: datetime) -> dict:
    if recall not in {"again", "hard", "good", "easy"}:
        raise ValueError("Recordação inválida.")
    stage = previous["stage"]
    if recall == "again":
        stage, days = 0, 1
    elif recall == "hard":
        days = 1
    else:
        stage = min(stage + (2 if recall == "easy" else 1), len(INTERVALS))
        days = INTERVALS[max(stage - 1, 0)]
    return {
        "stage": stage, "reviews": previous["reviews"] + 1,
        "lapses": previous["lapses"] + int(recall == "again"),
        "last_recall": recall, "last_review_at": stamp(now),
        "due_at": stamp(now + timedelta(days=days)), "interval_days": days,
        "version": previous["version"] + 1,
    }
