from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class SummaryLength(str, Enum):
    short = "short"
    medium = "medium"
    long = "long"


class SummaryFormat(str, Enum):
    paragraph = "paragraph"
    bullets = "bullets"


class SummaryOptions(BaseModel):
    length: SummaryLength = SummaryLength.short
    format: SummaryFormat = SummaryFormat.paragraph
    language: Literal["en"] = "en"


class SummaryRequest(BaseModel):
    text: str = Field(min_length=1, max_length=200000)
    options: SummaryOptions = Field(default_factory=SummaryOptions)


class SummaryResponse(BaseModel):
    id: str
    summary: str
    inputCharacters: int
    outputCharacters: int
    createdAt: datetime


class AsyncSummaryRequest(BaseModel):
    text: str = Field(min_length=1, max_length=200000)
    options: SummaryOptions = Field(default_factory=SummaryOptions)


class AsyncSummaryCreateResponse(BaseModel):
    id: str
    status: str
    createdAt: datetime


class AsyncSummaryStatusResponse(BaseModel):
    id: str
    status: str
    summary: str | None = None
    error: str | None = None
    createdAt: datetime
    completedAt: datetime | None = None


class BulkSummaryItem(BaseModel):
    id: str = Field(min_length=1, max_length=128)
    text: str = Field(min_length=1, max_length=200000)


class BulkSummaryRequest(BaseModel):
    items: list[BulkSummaryItem] = Field(min_length=1, max_length=50)
    options: SummaryOptions = Field(default_factory=SummaryOptions)


class BulkSummaryResult(BaseModel):
    id: str
    summary: str
    inputCharacters: int
    outputCharacters: int


class BulkSummaryResponse(BaseModel):
    results: list[BulkSummaryResult]


class TransformationRequestSchema(BaseModel):
    text: str = Field(min_length=1, max_length=200000)
    prompt: str = Field(min_length=1, max_length=20000)


class TransformationResponse(BaseModel):
    id: str
    text: str
    inputCharacters: int
    outputCharacters: int
    createdAt: datetime


class HealthResponse(BaseModel):
    status: str
