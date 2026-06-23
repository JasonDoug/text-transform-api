# Text Transformation API Project

## Purpose

The Text Transformation API is the first API service in a growing local-first API platform. It accepts text and returns transformed text. The first transformation is summarization, and the engine now includes prompt templates for podcast scripts, explainers, lectures, study guides, executive briefs, rewrites, and translations.

The current milestone focuses on the API contract, Docker deployment, Render deployment, LiteLLM-backed transformation engine, and documentation. The frontend will be added later.

## Repository Layout

```text
summary-api/
  app/
    main.py
    prompts.py
    schemas.py
    settings.py
    summarizer.py
    transformer.py
  docs/
    api.md
    project.md
  tests/
    test_named_transformations.py
    test_prompts.py
    test_transformer.py
  Dockerfile
  docker-compose.yml
  render.yaml
  requirements.txt
```

## Current Service

### Text Transformation API

Local Docker service name:

```text
summary-api
```

Local port mapping:

```text
127.0.0.1:8001 -> container:8000
```

Local URLs:

```text
http://127.0.0.1:8001/health
http://127.0.0.1:8001/docs
http://127.0.0.1:8001/redoc
```

## Current Endpoints

```text
GET  /health
POST /v1/transformations
POST /v1/transformations/podcast
POST /v1/transformations/explainer
POST /v1/transformations/lecture
POST /v1/transformations/study-guide
POST /v1/transformations/executive-brief
POST /v1/summaries
POST /v1/summaries/async
GET  /v1/summaries/{id}
POST /v1/summaries/bulk
```

## Current Behavior

The API uses LiteLLM as the text transformation engine.

### Named transformations

`POST /v1/transformations/podcast`, `POST /v1/transformations/explainer`, `POST /v1/transformations/lecture`, `POST /v1/transformations/study-guide`, and `POST /v1/transformations/executive-brief` use curated prompt templates.

Each named transformation supports:

```text
length: short | medium | long
format: plain | json
tone: neutral | friendly | professional
```

### Generic transformations

`POST /v1/transformations` accepts arbitrary prompt-controlled transformation instructions.

Example use cases:

```text
summary
podcast script
explainer/lecture
study guide
executive brief
rewrite
translation
```

### Synchronous summaries

`POST /v1/summaries` returns the summary immediately.

### Asynchronous summaries

`POST /v1/summaries/async` creates a background job and returns a job ID.

`GET /v1/summaries/{id}` returns the job status and result.

### Bulk summaries

`POST /v1/summaries/bulk` summarizes multiple texts in one request.

## Current Data Model

No persistent database exists yet.

### In-memory job fields

```text
id
status
request
summary
error
createdAt
completedAt
```

### Job statuses

```text
queued
processing
completed
failed
```

## Transformation Engine

### Library

```text
LiteLLM
```

### Why LiteLLM

- Works with OpenAI-compatible APIs.
- Supports Ollama, LM Studio, llama.cpp server, LocalAI, vLLM, and OpenRouter.
- Lets us switch providers without rewriting API code.
- Keeps the service lightweight compared with LangChain.
- Works cleanly with FastAPI and Pydantic.

### Engine files

```text
app/settings.py
app/prompts.py
app/transformer.py
app/summarizer.py
```

### Engine flow

```text
API request
  -> schema validation
  -> prompt builder
  -> LiteLLM transformer
  -> transformed text response
```

## Current Deployment

### Docker Compose

Used for local development.

Command:

```bash
docker compose -f docker-compose.yml up -d --build
```

The Docker image uses Python 3.12 and runs the API with Uvicorn.

Default local transformation provider:

```text
OpenAI-compatible API
```

Default local model server:

```text
Ollama
```

Default local model:

```text
llama3.1:8b
```

Default local endpoint:

```text
http://host.docker.internal:11434/v1
```

### Render

Render Blueprint file:

```text
render.yaml
```

Current Render service type:

```text
web
```

Current Render runtime:

```text
docker
```

Current Render health check:

```text
/health
```

Render Blueprint notes:

- Render Blueprints use YAML, not JSON.
- The service is configured as a Docker web service.
- The Dockerfile listens on `$PORT` with a default of `8000`.
- The Render Blueprint sets `PORT=8000`.
- Render is configured for OpenRouter by default.
- `TRANSFORMATION_API_KEY` must be set in Render because it is marked `sync: false`.

## Environment Variables

### Local Docker defaults

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:11434/v1
TRANSFORMATION_API_KEY=ollama
TRANSFORMATION_MODEL=llama3.1:8b
TRANSFORMATION_TEMPERATURE=0.2
TRANSFORMATION_MAX_TOKENS=1000
TRANSFORMATION_TIMEOUT=60
PORT=8000
```

### Ollama

If Ollama is managed by systemd and the API runs in Docker, make Ollama listen on Docker-reachable interfaces:

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

You should see `*:11434`.

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:11434/v1
TRANSFORMATION_API_KEY=ollama
TRANSFORMATION_MODEL=llama3.1:8b
```

### LM Studio

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:1234/v1
TRANSFORMATION_API_KEY=lm-studio
TRANSFORMATION_MODEL=local-model-name
```

### llama.cpp server

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:8080/v1
TRANSFORMATION_API_KEY=llama-cpp
TRANSFORMATION_MODEL=local-model-name
```

### vLLM

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:8000/v1
TRANSFORMATION_API_KEY=EMPTY
TRANSFORMATION_MODEL=meta-llama/Llama-3.1-8B-Instruct
```

### OpenRouter

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=https://openrouter.ai/api/v1
TRANSFORMATION_API_KEY=your_openrouter_key
TRANSFORMATION_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

OpenRouter has free models, but availability and limits can change. Local Ollama, LM Studio, llama.cpp, and vLLM are the most reliable free options because they run on your hardware.

## Authentication

Authentication is not implemented yet.

Recommended future approach:

- Add API key auth for service-to-service calls.
- Add user/session auth when the UI is built.
- Keep public endpoints private until auth is ready.
- Store secrets in Docker `.env` locally and Render environment variables in production.

## Persistence

Current persistence:

```text
None
```

Recommended future persistence:

- PostgreSQL for users, jobs, transformations, summaries, and audit records.
- Redis for async job queues.
- Object storage if source documents or transformed outputs need long-term file storage.

## Backend Future Work

Likely backend additions:

- Add structured JSON output support.
- Add provider fallback and retry behavior.
- Add token/cost tracking for paid providers.
- Add persistent async job storage.
- Add queue workers for long-running transformations.
- Add auth middleware.
- Add rate limiting.
- Add request logging and metrics.
- Add structured logs.
- Add OpenTelemetry or another tracing system.
- Add tests for routes, schemas, prompt builders, transformer behavior, and async jobs.

## UI Future Work

The frontend is not included yet.

Recommended future UI features:

- Text input page.
- Transformation type selector.
- Prompt editor.
- Summary result page.
- Podcast script result page.
- Explainer/lecture result page.
- Async job status page.
- Bulk upload page.
- API key management page.
- Settings page for model provider, model, length, and format.
- Error and retry states.

## API Contract Stability

The current endpoint paths are intended to remain stable:

```text
/v1/transformations
/v1/summaries
/v1/summaries/async
/v1/summaries/{id}
/v1/summaries/bulk
```

Future changes should preserve these paths when possible. Add new versions only if the contract needs breaking changes.

## Design Decisions

- FastAPI was chosen for simple, typed API development.
- Pydantic models define request and response schemas.
- LiteLLM was chosen for provider-agnostic model access.
- OpenAI-compatible APIs were chosen to support Ollama, LM Studio, llama.cpp, LocalAI, vLLM, and OpenRouter.
- PyTorch was intentionally not used because this service does not train or directly run model weights.
- LangChain was intentionally not used because the current transformation flow is prompt → model → transformed text.
- Docker Compose is used for local deployment.
- Render is used for cloud deployment.
- The transformer is isolated so prompts, providers, and models can change without affecting routes.
- The API is endpoint-first so the frontend can be built against a stable contract.

## Known Limitations

- No authentication.
- No persistent database.
- Async jobs are lost on restart.
- No provider fallback yet.
- No retry behavior yet.
- No token/cost tracking yet.
- No rate limiting.
- No structured logging.
- The async transformer currently processes jobs in the web process.

## Next Milestones

Recommended order:

1. Add prompt templates for podcast and explainer/lecture transformations.
2. Add provider fallback and retry behavior.
3. Add structured JSON output support.
4. Add PostgreSQL.
5. Add Redis or another queue for async jobs.
6. Add authentication.
7. Add rate limiting.
8. Add structured logging.
9. Build the UI against the existing API contract.
