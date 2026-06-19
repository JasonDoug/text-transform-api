# Text Transformation API Documentation

## Overview

The Text Transformation API is a FastAPI service that accepts source text and returns transformed text. The transformation engine is powered by **LiteLLM**, which lets the API call any OpenAI-compatible model provider.

Current transformation support:

```text
Summarization
Generic prompt-controlled transformations
Asynchronous summarization jobs
Bulk summarization
```

Future transformation types can use the same engine:

```text
Podcast scripts
Explainers
Lectures
Study guides
Executive briefs
Rewrites
Translations
```

## Architecture

```text
FastAPI route
  -> Pydantic request validation
  -> prompt builder or custom prompt
  -> LiteLLM transformer
  -> OpenAI-compatible provider
  -> transformed text
  -> JSON response
```

Core libraries:

```text
FastAPI       API framework
Pydantic      request/response schemas
LiteLLM       model/provider abstraction
Uvicorn       ASGI server
```

Supported providers:

```text
Ollama
LM Studio
llama.cpp server
LocalAI
vLLM
OpenRouter
Any OpenAI-compatible API
```

## Base URL

Local Docker deployment:

```text
http://127.0.0.1:8001
```

Render deployment:

```text
https://<render-service-name>.onrender.com
```

Interactive API docs:

```text
http://127.0.0.1:8001/docs
http://127.0.0.1:8001/redoc
```

---

## Provider Configuration

The API reads provider settings from environment variables.

### Required variables

```text
TRANSFORMATION_PROVIDER
TRANSFORMATION_BASE_URL
TRANSFORMATION_API_KEY
TRANSFORMATION_MODEL
```

### Optional variables

```text
TRANSFORMATION_TEMPERATURE
TRANSFORMATION_MAX_TOKENS
TRANSFORMATION_TIMEOUT
PORT
```

## Ollama

Start Ollama locally, then pull a model:

```bash
ollama pull llama3.1:8b
```

Environment:

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:11434/v1
TRANSFORMATION_API_KEY=ollama
TRANSFORMATION_MODEL=llama3.1:8b
```

## LM Studio

Start the LM Studio local server.

Environment:

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:1234/v1
TRANSFORMATION_API_KEY=lm-studio
TRANSFORMATION_MODEL=local-model-name
```

## llama.cpp server

Start `llama-server` with OpenAI-compatible API mode.

Environment:

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:8080/v1
TRANSFORMATION_API_KEY=llama-cpp
TRANSFORMATION_MODEL=local-model-name
```

## OpenRouter

Environment:

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=https://openrouter.ai/api/v1
TRANSFORMATION_API_KEY=your_openrouter_key
TRANSFORMATION_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

OpenRouter has free models, but availability and limits can change. Local providers are the most reliable free option because they run on your hardware.

---

## Health

### `GET /health`

Checks whether the API is running.

#### Response

```json
{
  "status": "ok"
}
```

#### cURL

```bash
curl "http://127.0.0.1:8001/health"
```

---

## Generic Transformations

### `POST /v1/transformations`

Creates a prompt-controlled text transformation.

Use this endpoint when the caller wants to provide the transformation instruction directly.

This is the most flexible endpoint.

#### Request

```json
{
  "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
  "prompt": "Transform this text into a short podcast intro with two hosts."
}
```

#### Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `text` | string | Yes | Source text to transform. Max 200,000 characters. |
| `prompt` | string | Yes | Transformation instruction. Max 20,000 characters. |

#### Success Response

Status: `200 OK`

```json
{
  "id": "tx_240a08dc3225",
  "text": "Host 1: Today we're talking about FastAPI.\nHost 2: And why it makes API development simple.",
  "inputCharacters": 83,
  "outputCharacters": 96,
  "createdAt": "2026-06-19T04:25:13.878522Z"
}
```

#### cURL

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
    "prompt": "Transform this text into a short podcast intro with two hosts."
  }'
```

---

## Summaries

### `POST /v1/summaries`

Creates a synchronous summary.

This endpoint uses a curated summary prompt generated from the request options.

Use this endpoint for short or medium text where the caller wants the result immediately.

#### Request

```json
{
  "text": "FastAPI is great. It makes APIs simple. This endpoint returns a summary.",
  "options": {
    "length": "short",
    "format": "paragraph",
    "language": "en"
  }
}
```

#### Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `text` | string | Yes | Text to summarize. Max 200,000 characters. |
| `options.length` | string | No | One of `short`, `medium`, or `long`. Defaults to `short`. |
| `options.format` | string | No | One of `paragraph` or `bullets`. Defaults to `paragraph`. |
| `options.language` | string | No | Currently supports `en`. Defaults to `en`. |

#### Summary Lengths

| Value | Behavior |
| --- | --- |
| `short` | One sentence. |
| `medium` | Up to three sentences. |
| `long` | Up to five sentences. |

#### Summary Formats

| Value | Behavior |
| --- | --- |
| `paragraph` | Returns a paragraph. |
| `bullets` | Returns bullet points. |

#### Success Response

Status: `200 OK`

```json
{
  "id": "sum_240a08dc3225",
  "summary": "FastAPI is great.",
  "inputCharacters": 72,
  "outputCharacters": 17,
  "createdAt": "2026-06-19T04:25:13.878522Z"
}
```

#### cURL

```bash
curl -X POST "http://127.0.0.1:8001/v1/summaries" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns a summary.",
    "options": {
      "length": "short",
      "format": "paragraph",
      "language": "en"
    }
  }'
```

---

### `POST /v1/summaries/async`

Creates an asynchronous summary job.

Use this endpoint for longer text or when the caller does not want to wait for processing to complete.

#### Request

```json
{
  "text": "FastAPI is great. It makes APIs simple. This endpoint returns a summary.",
  "options": {
    "length": "medium",
    "format": "bullets",
    "language": "en"
  }
}
```

#### Success Response

Status: `202 Accepted`

```json
{
  "id": "sum_daf952afd201",
  "status": "queued",
  "createdAt": "2026-06-19T04:25:17.783434Z"
}
```

#### cURL

```bash
curl -X POST "http://127.0.0.1:8001/v1/summaries/async" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns a summary.",
    "options": {
      "length": "medium",
      "format": "bullets",
      "language": "en"
    }
  }'
```

---

### `GET /v1/summaries/{id}`

Gets the status and result of an asynchronous summary job.

#### Path Parameters

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Summary job ID returned from `POST /v1/summaries/async`. |

#### Processing Response

Status: `200 OK`

```json
{
  "id": "sum_daf952afd201",
  "status": "processing",
  "summary": null,
  "error": null,
  "createdAt": "2026-06-19T04:25:17.783434Z",
  "completedAt": null
}
```

#### Completed Response

Status: `200 OK`

```json
{
  "id": "sum_daf952afd201",
  "status": "completed",
  "summary": "- FastAPI is great.\n- It makes APIs simple.\n- This endpoint returns a summary.",
  "error": null,
  "createdAt": "2026-06-19T04:25:17.783434Z",
  "completedAt": "2026-06-19T04:25:17.784135Z"
}
```

#### Failed Response

Status: `200 OK`

```json
{
  "id": "sum_daf952afd201",
  "status": "failed",
  "summary": null,
  "error": "Unexpected processing error",
  "createdAt": "2026-06-19T04:25:17.783434Z",
  "completedAt": "2026-06-19T04:25:18.000000Z"
}
```

#### cURL

```bash
curl "http://127.0.0.1:8001/v1/summaries/sum_daf952afd201"
```

---

### `POST /v1/summaries/bulk`

Creates summaries for multiple texts.

Use this endpoint when the caller already has a collection of texts and wants all summaries in one response.

#### Request

```json
{
  "items": [
    {
      "id": "article-1",
      "text": "FastAPI is great. It makes APIs simple."
    },
    {
      "id": "article-2",
      "text": "Render can host Dockerized APIs."
    }
  ],
  "options": {
    "length": "short",
    "format": "paragraph",
    "language": "en"
  }
}
```

#### Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `items` | array | Yes | Text items to summarize. Max 50 items. |
| `items[].id` | string | Yes | Caller-provided item ID. Max 128 characters. |
| `items[].text` | string | Yes | Text to summarize. Max 200,000 characters. |
| `options` | object | No | Shared summary options for all items. |

#### Success Response

Status: `200 OK`

```json
{
  "results": [
    {
      "id": "article-1",
      "summary": "FastAPI is great.",
      "inputCharacters": 48,
      "outputCharacters": 17
    },
    {
      "id": "article-2",
      "summary": "Render can host Dockerized APIs.",
      "inputCharacters": 35,
      "outputCharacters": 35
    }
  ]
}
```

#### cURL

```bash
curl -X POST "http://127.0.0.1:8001/v1/summaries/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "id": "article-1",
        "text": "FastAPI is great. It makes APIs simple."
      },
      {
        "id": "article-2",
        "text": "Render can host Dockerized APIs."
      }
    ],
    "options": {
      "length": "short",
      "format": "paragraph",
      "language": "en"
    }
  }'
```

---

## Error Responses

### `404 Not Found`

Returned when an async summary job does not exist.

```json
{
  "detail": "Summary job not found"
}
```

### `422 Unprocessable Entity`

Returned when request validation fails.

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "text"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

### `500 Internal Server Error`

Returned for unexpected server errors, including provider/model failures.

```json
{
  "detail": "Unexpected server error"
}
```

---

## Current Implementation Notes

- Authentication is not enabled yet.
- Async jobs are stored in memory.
- Async jobs are lost if the service restarts.
- The transformation engine uses LiteLLM.
- The default local provider is OpenAI-compatible Ollama.
- No database is required yet.
- The frontend is not included yet.

---

## Development Commands

Build and start locally:

```bash
docker compose -f docker-compose.yml up -d --build
```

View logs:

```bash
docker compose -f docker-compose.yml logs -f
```

Run tests:

```bash
docker compose -f docker-compose.yml run --rm -e PYTHONPATH=/app -v "$PWD/tests:/app/tests" summary-api pytest -q
```

Stop locally:

```bash
docker compose -f docker-compose.yml down
```
