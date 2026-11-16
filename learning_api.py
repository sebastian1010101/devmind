"""Adaptador HTTP. Seleção diária e aprendizagem não dependem de mensageria."""

import os
from functools import lru_cache

from fastapi import APIRouter, Depends, Query

from learning_models import GenerateRequest, RecallRequest, ReviewRequest
from learning_service import LearningService
from learning_store import LearningStore
from auth import User, current_user
from security import ai_slot, rate_limit

router = APIRouter(prefix="/learning", tags=["Active Recall"])


@lru_cache(maxsize=4)
def _store(path):
    return LearningStore(path)


def get_store():
    if os.getenv("APP_ENV") == "production" and not os.getenv("DATABASE_URL", "").startswith(("postgresql://", "postgres://")):
        from providers import ServiceError
        raise ServiceError("database_config", "Configure PostgreSQL no servidor para o ambiente de produção.", 503)
    return _store(os.getenv("DATABASE_URL") or os.getenv("LEARNING_DB_PATH", "data/learning.sqlite3"))


def user_store(user: User = Depends(current_user)):
    store = get_store().for_user(user.id)
    rate_limit(store, f"user:{user.id}", int(os.getenv("USER_REQUESTS_PER_MINUTE", "60")))
    return store


@router.post("/cards")
def generate_cards(request: GenerateRequest, store=Depends(user_store)):
    with ai_slot(store):
        return LearningService(store).generate(request)


@router.get("/cards/{card_id}")
def get_card(card_id: str, store=Depends(user_store)):
    return store.card(card_id)


@router.post("/cards/{card_id}/reviews")
def review_card(card_id: str, request: ReviewRequest, store=Depends(user_store)):
    with ai_slot(store):
        return LearningService(store).review(card_id, request)


@router.post("/reviews/{review_id}/recall")
def rate_recall(review_id: str, request: RecallRequest, store=Depends(user_store)):
    return store.rate(review_id, request.recall)


@router.get("/due")
def due_cards(limit: int = Query(default=5, ge=1, le=20), store=Depends(user_store)):
    return store.due(limit)


@router.get("/daily")
def daily_session(store=Depends(user_store)):
    return store.daily()


@router.get("/progress")
def learning_progress(store=Depends(user_store)):
    return store.progress()
