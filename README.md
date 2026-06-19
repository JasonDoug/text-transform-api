# Text Transformation API

A FastAPI service for prompt-controlled text transformations.

The first built-in transformation is summarization, and the engine is designed for future transformation types like podcast scripts, explainers, lectures, study guides, executive briefs, rewrites, and translations.

## What it does

```text
source text + transformation prompt -> transformed text
```

The service uses **LiteLLM**, so it can call any OpenAI-compatible provider:

```text
Ollama
LM Studio
llama.cpp server
LocalAI
vLLM
OpenRouter
```

## Quick start

Start Ollama locally:

```bash
ollama serve
ollama pull llama3.1:8b
```

If Ollama is managed by systemd and the API runs in Docker, make Ollama listen on Docker-reachable interfaces:

```bash
sudo systemctl edit ollama
```

Add:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Then restart:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
ss -ltnp | grep 11434
```

You should see Ollama listening on `*:11434`, not only `127.0.0.1:11434`.

Start the API:

```bash
docker compose up -d --build
```

Open API docs:

```text
http://127.0.0.1:8001/docs
```

Check health:

```bash
curl http://127.0.0.1:8001/health
```

## Endpoints

```text
GET  /health
POST /v1/transformations
POST /v1/summaries
POST /v1/summaries/async
GET  /v1/summaries/{id}
POST /v1/summaries/bulk
```

## Example: generic transformation

```bash
curl -X POST "http://127.0.0.1:8001/v1/transformations" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is great. It makes APIs simple.",
    "prompt": "Transform this into a short podcast intro with two hosts."
  }'
```

## Example: summary

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

## Provider setup

The default Docker Compose config points at local Ollama:

```text
TRANSFORMATION_PROVIDER=openai-compatible
TRANSFORMATION_BASE_URL=http://host.docker.internal:11434/v1
TRANSFORMATION_API_KEY=ollama
TRANSFORMATION_MODEL=llama3.1:8b
```

### LM Studio

```text
TRANSFORMATION_BASE_URL=http://host.docker.internal:1234/v1
TRANSFORMATION_API_KEY=lm-studio
TRANSFORMATION_MODEL=local-model-name
```

### llama.cpp server

```text
TRANSFORMATION_BASE_URL=http://host.docker.internal:8080/v1
TRANSFORMATION_API_KEY=llama-cpp
TRANSFORMATION_MODEL=local-model-name
```

### OpenRouter

```text
TRANSFORMATION_BASE_URL=https://openrouter.ai/api/v1
TRANSFORMATION_API_KEY=your_openrouter_key
TRANSFORMATION_MODEL=meta-llama/llama-3.1-8b-instruct:free
```

## Project structure

```text
.
├── app/
│   ├── main.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── settings.py
│   ├── summarizer.py
│   └── transformer.py
├── docs/
│   ├── api.md
│   └── project.md
├── tests/
│   └── test_transformer.py
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── requirements.txt
├── README.md
├── DEVELOPER_NOTES.md
└── CURLS.md
```

## Run tests

```bash
docker compose run --rm -e PYTHONPATH=/app -v "$PWD/tests:/app/tests" summary-api pytest -q
```

## Logs

```bash
docker compose logs -f summary-api
```

## Stop

```bash
docker compose down
```

## Docs

Detailed API documentation:

```text
docs/api.md
```

Project notes for future backend/UI work:

```text
docs/project.md
DEVELOPER_NOTES.md
```

Ready-to-run curl examples:

```text
CURLS.md
```

## Render

Render Blueprint:

```text
render.yaml
```

Render is configured for an OpenRouter-compatible deployment by default. Set `TRANSFORMATION_API_KEY` in Render because it is marked as unsynced.
