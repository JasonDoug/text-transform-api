# AGENTS.md — Text Transformation API

## Quick Start

```bash
# Start Ollama locally (must listen on 0.0.0.0 for Docker access)
ollama serve
ollama pull llama3.1:8b

# Start API
docker compose up -d --build

# Health check
curl http://127.0.0.1:8001/health
```

## Run Tests

```bash
docker compose run --rm -e PYTHONPATH=/app -v "$PWD/tests:/app/tests" summary-api pytest -q
```

## Key Commands

| Task | Command |
|------|---------|
| Start dev stack | `docker compose up -d --build` |
| View logs | `docker compose logs -f summary-api` |
| Run tests | `docker compose run --rm -e PYTHONPATH=/app -v "$PWD/tests:/app/tests" summary-api pytest -q` |
| Rebuild no cache | `docker compose build --no-cache summary-api` |
| Stop | `docker compose down` |

## Environment Variables

Copy `.env.example` to `.env` and customize. Required:

```
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:11434/v1
TRANSFORMATION_API_KEY=ollama
TRANSFORMATION_MODEL=llama3.1:8b
TRANSFORMATION_TEMPERATURE=0.2
TRANSFORMATION_MAX_TOKENS=1000
TRANSFORMATION_TIMEOUT=60
```

Provider-specific examples in `.env.example` and `README.md`.

## Architecture

```
FastAPI
  -> Pydantic schemas (app/schemas.py)
  -> Prompt builders (app/prompts.py)
  -> LiteLLMTextTransformer (app/transformer.py)
  -> OpenAI-compatible provider (Ollama, LM Studio, vLLM, OpenRouter, etc.)
```

### Two Transformation Layers

1. **Generic** — `POST /v1/transformations` — caller provides full prompt
2. **Named** — `POST /v1/transformations/{podcast,explainer,lecture,study-guide,executive-brief}` — stable product endpoints with built-in prompt templates

Summary endpoints are a third layer: `POST /v1/summaries` + async/bulk variants.

### Core Modules

- `app/main.py` — routes, request handlers, in-memory async job store
- `app/schemas.py` — Pydantic models (keep stable for future UI)
- `app/settings.py` — `TransformationSettings` loaded from env, cached via `@lru_cache`
- `app/prompts.py` — prompt builders for each transformation type
- `app/transformer.py` — `LiteLLMTextTransformer` wraps `litellm.completion`
- `app/summarizer.py` — summary-specific wrapper that builds summary prompt + calls transformer

## Adding a New Transformation Type

1. Add prompt builder in `app/prompts.py`
2. Add request/response schemas in `app/schemas.py`
3. Add route in `app/main.py` (follow existing pattern with `_build_named_transformation_response`)
4. Add tests for prompt, schema, route, provider call args
5. Add curl example to `CURLS.md`
6. Update `docs/api.md`, `docs/project.md`, `README.md`, `DEVELOPER_NOTES.md`

## Deployment (Render)

Blueprint: `render.yaml`

- Default config uses OpenRouter; set `TRANSFORMATION_API_KEY` in Render dashboard (marked `sync: false`)
- Health check: `/health`
- Port: `8000` (set via `PORT` env)

```bash
render blueprints validate
```

## Known Constraints

- **No auth** — do not expose publicly
- **No database** — async jobs stored in memory (lost on restart, not shared across replicas)
- **No retry/fallback** — single provider call, no resilience
- **No rate limiting**
- **No structured output** (plain text only; JSON requested via prompt but not validated)

## Testing Notes

- Tests mock `litellm.completion` and assert on call args
- Run inside Docker to match production env (uses `host.docker.internal`)
- Current coverage: prompt builders, env settings, LiteLLM call arguments, named endpoints