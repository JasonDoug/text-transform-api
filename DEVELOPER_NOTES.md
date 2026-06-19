# Developer Notes

## Goal

Build a local-first text transformation platform. The first service is the Summary/Text Transformation API. The frontend is not built yet, so keep the API contract stable and easy to consume.

## Current architecture

```text
FastAPI
  -> Pydantic schemas
  -> prompt builders
  -> LiteLLM transformer
  -> OpenAI-compatible provider
```

The API does not depend on one model provider. It depends on the OpenAI-compatible API shape.

That means the same code can talk to:

```text
Ollama
LM Studio
llama.cpp server
LocalAI
vLLM
OpenRouter
```

## Core files

### `app/main.py`

FastAPI routes and request handlers.

Current routes:

```text
GET  /health
POST /v1/transformations
POST /v1/summaries
POST /v1/summaries/async
GET  /v1/summaries/{id}
POST /v1/summaries/bulk
```

### `app/schemas.py`

Pydantic request and response models.

Keep schemas stable when possible. The UI will rely on these shapes.

### `app/settings.py`

Environment-driven transformation settings.

Important variables:

```text
TRANSFORMATION_PROVIDER
TRANSFORMATION_BASE_URL
TRANSFORMATION_API_KEY
TRANSFORMATION_MODEL
TRANSFORMATION_TEMPERATURE
TRANSFORMATION_MAX_TOKENS
TRANSFORMATION_TIMEOUT
```

### `app/prompts.py`

Prompt builders for first-class transformations.

Currently contains:

```text
build_summary_prompt()
```

Future prompt builders should live here:

```text
build_podcast_prompt()
build_explainer_prompt()
build_lecture_prompt()
build_study_guide_prompt()
build_executive_brief_prompt()
```

### `app/transformer.py`

LiteLLM wrapper.

Current class:

```text
LiteLLMTextTransformer
```

This is the main place to add:

```text
retry behavior
provider fallback
structured output
streaming
token/cost tracking
request timeouts
```

### `app/summarizer.py`

Summary-specific transformation wrapper.

It turns summary options into a prompt and calls the shared transformer.

## Transformation design

There are two layers:

```text
1. Generic transformation endpoint
2. Named transformation endpoints
```

### Generic endpoint

```text
POST /v1/transformations
```

The caller provides the prompt.

Use this for maximum flexibility.

### Named endpoints

```text
POST /v1/summaries
POST /v1/summaries/async
POST /v1/summaries/bulk
```

These are product-facing endpoints with stable behavior.

Internally, they use the same LiteLLM transformer.

## Adding a new transformation type

Use this pattern.

### 1. Add a prompt builder

In `app/prompts.py`:

```python
def build_podcast_prompt(text: str, options: PodcastOptions) -> str:
    return f"""
You are a text transformation engine.

Transformation type: podcast script

Instructions:
- Transform the source text into a two-host podcast script.
- Keep the tone engaging and clear.
- Do not invent facts that are not in the source text.
- Return only the transformed text.

Source text:
{text}
"""
```

### 2. Add schemas

In `app/schemas.py`:

```python
class PodcastRequest(BaseModel):
    text: str = Field(min_length=1, max_length=200000)
    options: PodcastOptions = Field(default_factory=PodcastOptions)


class PodcastResponse(BaseModel):
    id: str
    text: str
    inputCharacters: int
    outputCharacters: int
    createdAt: datetime
```

### 3. Add route

In `app/main.py`:

```python
@app.post("/v1/transformations/podcast", response_model=PodcastResponse)
async def create_podcast(request: PodcastRequest) -> PodcastResponse:
    prompt = build_podcast_prompt(request.text, request.options)
    result = await _text_transformer.transform(
        TransformationRequest(text=request.text, prompt=prompt)
    )

    return PodcastResponse(
        id=_new_id("pod"),
        text=result.text,
        inputCharacters=len(request.text),
        outputCharacters=len(result.text),
        createdAt=_now(),
    )
```

### 4. Add tests

Add tests for:

```text
prompt builder
schema validation
route behavior
provider call arguments
```

### 5. Add curl example

Add a ready-to-run example to `CURLS.md`.

### 6. Update docs

Update:

```text
docs/api.md
docs/project.md
README.md
DEVELOPER_NOTES.md
```

## Provider behavior

The current transformer calls LiteLLM with:

```text
model=openai/<TRANSFORMATION_MODEL>
api_base=<TRANSFORMATION_BASE_URL>
api_key=<TRANSFORMATION_API_KEY>
```

This works for OpenAI-compatible APIs.

## Local provider notes

### Ollama

Default local provider.

Requires:

```bash
ollama pull llama3.1:8b
```

Docker Compose uses:

```text
http://host.docker.internal:11434/v1
```

`host.docker.internal` is added through Compose `extra_hosts`.

### LM Studio

Requires the LM Studio local server to be running.

Default local server port is usually:

```text
1234
```

### llama.cpp

Requires `llama-server` to expose an OpenAI-compatible API.

Default example port:

```text
8080
```

## Async jobs

Current async jobs are stored in memory.

This is fine for early development, but not production-safe.

Current limitations:

```text
Jobs disappear on restart.
Jobs are not shared across replicas.
No durable queue exists.
No retry policy exists.
No job history exists.
```

Future backend work should add:

```text
PostgreSQL for job records
Redis or another queue for workers
Dedicated worker service
Job status webhooks or polling
```

## Persistence

Current persistence:

```text
None
```

Future persistence plan:

```text
PostgreSQL:
  users
  api_keys
  transformation_jobs
  transformation_results
  prompts
  provider_configs

Redis:
  job queues
  rate limits
  short-lived locks
```

## Authentication

Not implemented yet.

Future plan:

```text
API key auth for service-to-service calls
User/session auth for UI
Admin role for settings
Per-user usage tracking
```

Do not expose this API publicly without auth.

## Rate limiting

Not implemented yet.

Future plan:

```text
Per-API-key limits
Per-user limits
Per-IP fallback limits
Slow-mode for expensive transformations
```

## Structured output

The current generic transformation returns plain text.

Future transformations may need JSON.

Example podcast JSON:

```json
{
  "title": "FastAPI APIs",
  "hosts": ["Host 1", "Host 2"],
  "script": [
    {
      "speaker": "Host 1",
      "line": "Today we're talking about FastAPI."
    }
  ]
}
```

When adding structured output, consider:

```text
Pydantic response models
LiteLLM response_format support
JSON schema validation
Fallback parsing
```

## UI contract

The future UI should be able to call:

```text
GET /health
POST /v1/transformations
POST /v1/summaries
POST /v1/summaries/async
GET /v1/summaries/{id}
POST /v1/summaries/bulk
```

Recommended UI flow:

```text
User selects transformation type
  -> UI chooses prompt template or custom prompt
  -> UI sends request
  -> UI displays transformed text
  -> UI handles errors/retries
```

For async summaries:

```text
Submit job
  -> show queued/processing state
  -> poll GET /v1/summaries/{id}
  -> show completed result
```

## Testing

Run tests:

```bash
docker compose run --rm -e PYTHONPATH=/app -v "$PWD/tests:/app/tests" summary-api pytest -q
```

Current tests cover:

```text
summary prompt builder
environment settings
LiteLLM call arguments
```

Future tests should cover:

```text
route validation
provider fallback
retry behavior
prompt templates
async job state
bulk behavior
error handling
structured output
```

## Deployment

Local:

```bash
docker compose up -d --build
```

Render:

```bash
render blueprints validate
```

Render Blueprint:

```text
render.yaml
```

Render uses OpenRouter by default. Set the OpenRouter API key in Render.

## Commands

Start:

```bash
docker compose up -d --build
```

Logs:

```bash
docker compose logs -f summary-api
```

Tests:

```bash
docker compose run --rm -e PYTHONPATH=/app -v "$PWD/tests:/app/tests" summary-api pytest -q
```

Stop:

```bash
docker compose down
```

Rebuild without cache:

```bash
docker compose build --no-cache summary-api
```

## Known limitations

```text
No auth
No database
No durable async jobs
No provider fallback
No retry behavior
No rate limiting
No structured output
No streaming
No cost tracking
No frontend
```

## Next milestones

Recommended order:

```text
1. Prompt templates for podcast and explainer/lecture
2. Provider fallback and retry behavior
3. Structured JSON output
4. PostgreSQL
5. Redis or another queue
6. Auth
7. Rate limiting
8. Structured logging
9. UI
```
