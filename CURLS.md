# CURLS

Ready-to-run curl examples for the Text Transformation API.

Set the base URL:

```bash
BASE_URL="http://127.0.0.1:8001"
```

## Health

```bash
curl "http://127.0.0.1:8001/health"
```

Expected:

```json
{
  "status": "ok"
}
```

---

## OpenAPI docs

```bash
curl "http://127.0.0.1:8001/openapi.json"
```

Open interactive docs in a browser:

```text
http://127.0.0.1:8001/docs
http://127.0.0.1:8001/redoc
```

---

# Generic transformations

## Custom summary transformation

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
    "prompt": "Transform this text into a concise summary."
  }'
```

## Podcast transformation

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
    "prompt": "Transform this text into a short podcast intro with two hosts. Keep it friendly and energetic."
  }'
```

## Explainer transformation

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
    "prompt": "Transform this text into a beginner-friendly explainer. Use simple language and one example."
  }'
```

## Lecture transformation

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
    "prompt": "Transform this text into a short lecture outline for beginners. Include learning objectives and key takeaways."
  }'
```

## Study guide transformation

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
    "prompt": "Transform this text into a study guide with key terms, questions, and a short quiz."
  }'
```

## Executive brief transformation

```bash
curl -X POST "$BASE_URL/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns transformed text.",
    "prompt": "Transform this text into a concise executive brief with the main point, implications, and recommended next step."
  }'
```

---

# Named transformations

## Podcast transformation

```bash
curl -X POST "$BASE_URL/v1/transformations/podcast" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "short",
      "format": "json",
      "tone": "friendly"
    }
  }'
```

## Explainer transformation

```bash
curl -X POST "$BASE_URL/v1/transformations/explainer" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "medium",
      "format": "plain",
      "tone": "professional"
    }
  }'
```

## Lecture transformation

```bash
curl -X POST "$BASE_URL/v1/transformations/lecture" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "long",
      "format": "plain",
      "tone": "professional"
    }
  }'
```

## Study guide transformation

```bash
curl -X POST "$BASE_URL/v1/transformations/study-guide" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "medium",
      "format": "plain",
      "tone": "friendly"
    }
  }'
```

## Executive brief transformation

```bash
curl -X POST "$BASE_URL/v1/transformations/executive-brief" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "short",
      "format": "plain",
      "tone": "professional"
    }
  }'
```

## Rewrite transformation

```bash
curl -X POST "$BASE_URL/v1/transformations/rewrite" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "medium",
      "format": "plain",
      "tone": "friendly"
    }
  }'
```

## Translation transformation

```bash
curl -X POST "$BASE_URL/v1/transformations/translation" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "short",
      "format": "plain",
      "tone": "professional"
    }
  }'
```

---

# Summaries

## Short paragraph summary

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

## Medium bullet summary

```bash
curl -X POST "http://127.0.0.1:8001/v1/summaries" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns a summary. It also supports async jobs and bulk summaries.",
    "options": {
      "length": "medium",
      "format": "bullets",
      "language": "en"
    }
  }'
```

## Long paragraph summary

```bash
curl -X POST "http://127.0.0.1:8001/v1/summaries" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns a summary. It also supports async jobs and bulk summaries. The transformation engine uses LiteLLM and can call OpenAI-compatible providers like Ollama, LM Studio, llama.cpp, LocalAI, vLLM, and OpenRouter.",
    "options": {
      "length": "long",
      "format": "paragraph",
      "language": "en"
    }
  }'
```

---

# Async summaries

## Create async summary job

```bash
curl -X POST "http://127.0.0.1:8001/v1/summaries/async" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple. This endpoint returns a summary. It also supports async jobs and bulk summaries.",
    "options": {
      "length": "medium",
      "format": "bullets",
      "language": "en"
    }
  }'
```

Example response:

```json
{
  "id": "sum_daf952afd201",
  "status": "queued",
  "createdAt": "2026-06-19T04:25:17.783434Z"
}
```

## Poll async summary job

Replace `SUMMARY_ID` with the ID returned from the previous request.

```bash
curl "http://127.0.0.1:8001/v1/summaries/SUMMARY_ID"
```

Example completed response:

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

---

# Bulk summaries

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
      },
      {
        "id": "article-3",
        "text": "LiteLLM lets this service call OpenAI-compatible model providers."
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

# Provider examples

## Ollama

Start Ollama and pull a model:

```bash
ollama pull llama3.1:8b
```

If Ollama is running as a systemd service and the API runs in Docker, make Ollama listen on Docker-reachable interfaces:

```bash
sudo systemctl edit ollama
```

Add:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Restart and verify:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
ss -ltnp | grep 11434
```

You should see:

```text
*:11434
```

Default Docker Compose config already points at:

```text
http://host.docker.internal:11434/v1
```

Test with:

```bash
curl -X POST "http://127.0.0.1:8001/v1/summaries" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "options": {
      "length": "short",
      "format": "paragraph",
      "language": "en"
    }
  }'
```

## OpenRouter

Set these environment variables before starting the API:

```bash
export TRANSFORMATION_PROVIDER="openai-compatible"
export TRANSFORMATION_BASE_URL="https://openrouter.ai/api/v1"
export TRANSFORMATION_API_KEY="your_openrouter_key"
export TRANSFORMATION_MODEL="meta-llama/llama-3.1-8b-instruct:free"
```

Restart:

```bash
docker compose up -d --build
```

Test with:

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "prompt": "Transform this into a one-sentence summary."
  }'
```
