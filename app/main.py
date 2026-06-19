from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import (
    AsyncSummaryCreateResponse,
    AsyncSummaryRequest,
    AsyncSummaryStatusResponse,
    BulkSummaryRequest,
    BulkSummaryResponse,
    BulkSummaryResult,
    HealthResponse,
    SummaryOptions,
    SummaryRequest,
    SummaryResponse,
    TransformationRequestSchema,
    TransformationResponse,
)
from app.settings import get_transformation_settings
from app.summarizer import summarize_text
from app.transformer import LiteLLMTextTransformer, TransformationRequest

app = FastAPI(
    title="Text Transformation API",
    version="0.2.0",
)

_jobs: dict[str, dict[str, Any]] = {}
_text_transformer = LiteLLMTextTransformer(get_transformation_settings())


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/v1/summaries", response_model=SummaryResponse, status_code=status.HTTP_200_OK)
async def create_summary(request: SummaryRequest) -> SummaryResponse:
    return await _build_summary_response(request.text, request.options)


@app.post("/v1/summaries/async", response_model=AsyncSummaryCreateResponse, status_code=status.HTTP_202_ACCEPTED)
def create_async_summary(
    request: AsyncSummaryRequest,
    background_tasks: BackgroundTasks,
) -> AsyncSummaryCreateResponse:
    job_id = _new_id("sum")
    now = _now()

    _jobs[job_id] = {
        "id": job_id,
        "status": "queued",
        "request": request.model_dump(),
        "summary": None,
        "error": None,
        "createdAt": now,
        "completedAt": None,
    }

    background_tasks.add_task(_process_summary_job, job_id)

    return AsyncSummaryCreateResponse(
        id=job_id,
        status="queued",
        createdAt=now,
    )


@app.get("/v1/summaries/{summary_id}", response_model=AsyncSummaryStatusResponse)
def get_async_summary(summary_id: str) -> AsyncSummaryStatusResponse:
    job = _jobs.get(summary_id)

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary job not found")

    return AsyncSummaryStatusResponse(
        id=job["id"],
        status=job["status"],
        summary=job["summary"],
        error=job["error"],
        createdAt=job["createdAt"],
        completedAt=job["completedAt"],
    )


@app.post("/v1/summaries/bulk", response_model=BulkSummaryResponse)
async def create_bulk_summary(request: BulkSummaryRequest) -> BulkSummaryResponse:
    results = []

    for item in request.items:
        results.append(await _build_bulk_result(item.id, item.text, request.options))

    return BulkSummaryResponse(results=results)


@app.post("/v1/transformations", response_model=TransformationResponse)
async def create_transformation(request: TransformationRequestSchema) -> TransformationResponse:
    result = await _text_transformer.transform(
        TransformationRequest(
            text=request.text,
            prompt=request.prompt,
        )
    )

    return TransformationResponse(
        id=_new_id("tx"),
        text=result.text,
        inputCharacters=len(request.text),
        outputCharacters=len(result.text),
        createdAt=_now(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Unexpected server error"},
    )


async def _process_summary_job(job_id: str) -> None:
    try:
        job = _jobs[job_id]
        request = job["request"]
        text = request["text"]
        options = SummaryOptions(**request["options"])

        job["status"] = "processing"
        summary = await summarize_text(text, options)

        job["summary"] = summary
        job["status"] = "completed"
        job["completedAt"] = _now()
    except Exception as exc:
        job = _jobs[job_id]
        job["error"] = str(exc)
        job["status"] = "failed"
        job["completedAt"] = _now()


async def _build_summary_response(text: str, options: SummaryOptions) -> SummaryResponse:
    summary = await summarize_text(text, options)

    return SummaryResponse(
        id=_new_id("sum"),
        summary=summary,
        inputCharacters=len(text),
        outputCharacters=len(summary),
        createdAt=_now(),
    )


async def _build_bulk_result(item_id: str, text: str, options: SummaryOptions) -> BulkSummaryResult:
    summary = await summarize_text(text, options)

    return BulkSummaryResult(
        id=item_id,
        summary=summary,
        inputCharacters=len(text),
        outputCharacters=len(summary),
    )


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _now() -> datetime:
    return datetime.now(timezone.utc)
