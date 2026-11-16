"""Adaptador HTTP. Seleção diária e aprendizagem não dependem de mensageria."""

import os
from functools import lru_cache

from fastapi import APIRouter, Depends, Query

from learning_models import GenerateRequest, RecallRequest, ReviewRequest
from learning_service import LearningService
from learning_store import LearningStore
from local_access import local_demo_access

router = APIRouter(prefix="/learning", tags=["Active Recall"], dependencies=[Depends(local_demo_access)])


@lru_cache(maxsize=4)
def _store(path):
    return LearningStore(path)


def get_store():
    return _store(os.getenv("LEARNING_DB_PATH", "data/learning.sqlite3"))


@router.post("/cards")
def generate_cards(request: GenerateRequest):
    return LearningService(get_store()).generate(request)


@router.get("/cards/{card_id}")
def get_card(card_id: str):
    return get_store().card(card_id)


@router.post("/cards/{card_id}/reviews")
def review_card(card_id: str, request: ReviewRequest):
    return LearningService(get_store()).review(card_id, request)


@router.post("/reviews/{review_id}/recall")
def rate_recall(review_id: str, request: RecallRequest):
    return get_store().rate(review_id, request.recall)


@router.get("/due")
def due_cards(limit: int = Query(default=5, ge=1, le=20)):
    return get_store().due(limit)


@router.get("/daily")
def daily_session():
    return get_store().daily()


@router.get("/progress")
def learning_progress():
    return get_store().progress()
