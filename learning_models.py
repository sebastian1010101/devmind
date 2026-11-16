"""Contratos de entrada e saídas estruturadas do Active Recall."""

from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1200)]
ShortText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
Recall = Literal["again", "hard", "good", "easy"]
Grade = Literal["correct", "partial", "incorrect", "ungradable"]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class GenerateRequest(Contract):
    request_id: Annotated[UUID, Field(strict=False)]
    module: ShortText
    topic: ShortText | None = None
    source: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=512)] | None = None
    focus: Text = "Conceitos fundamentais e aplicação prática"
    count: Annotated[int, Field(ge=1, le=3)] = 3


class ReviewRequest(Contract):
    request_id: Annotated[UUID, Field(strict=False)]
    answer: Text


class RecallRequest(Contract):
    recall: Recall


class GeneratedCard(Contract):
    question: Text
    reference_answer: Text
    explanation: Text
    concepts: Annotated[list[Text], Field(min_length=1, max_length=8)]
    citations: Annotated[list[ShortText], Field(min_length=1, max_length=3)]
    difficulty: Literal["easy", "medium", "hard"]


class GeneratedDeck(Contract):
    # Zero cards is an explicit evidence-based abstention.
    cards: Annotated[list[GeneratedCard], Field(max_length=3)]


class Evaluation(Contract):
    grade: Grade
    present_concepts: Annotated[list[Text], Field(max_length=8)]
    missing_concepts: Annotated[list[Text], Field(max_length=8)]
    errors: Annotated[list[Text], Field(max_length=8)]
    feedback: Text
    citations: Annotated[list[ShortText], Field(min_length=1, max_length=3)]
