# Text Transformation API — Reference UI

A lightweight, single‑page HTML/CSS/JS application for testing and exploring the Text Transformation API. Acts as both a manual testing tool and a reference for future UI development.

## Quick Start

```bash
# Serve locally (from the ui/ directory)
python3 -m http.server 8080
# OR
npx serve ui/ --port 8080

# Open in browser
open http://127.0.0.1:8080
```

Ensure the API is running (see `AGENTS.md` or run `docker compose up -d --build`).

Set the **Base URL** in the UI to match your API server (default: `http://127.0.0.1:8001`).

## Features

- **Dark/Light theme** — remembers preference across sessions
- **Health check** — quick ping with provider/model info
- **10+ endpoints** — all named transformations, generic transformation, and summary endpoints (sync/async/bulk)
- **Dynamic form fields** — endpoint‑specific inputs with defaults
- **Syntax‑highlighted JSON** response display with status badges
- **Async job polling** — automatically polls `GET /v1/summaries/{id}` until complete
- **Copy & download** response buttons
- **Request details** — shows exact HTTP method, path, headers, and body sent
- **Keyboard shortcut** — `Ctrl+Enter` / `Cmd+Enter` to send

## Architecture

```
ui/
├── index.html      # Semantic HTML shell with ARIA labels
├── styles.css      # CSS custom properties (theming), responsive grid, clean typography
├── app.js          # ES6 module; vanilla JS (no framework), fetch, async/await
└── README-UI.md    # This file
```

### Design decisions

- **No build step** — serve directly from any static server
- **Vanilla JS** — zero dependencies, easy to understand and extend
- **Flat endpoint definitions** — `ENDPOINTS` object in JS drives form generation, validation, and request building. Adding an endpoint is a data change.
- **CSS custom properties** for theming — `[data-theme="dark"]` flips all colors
- **No router** — single page, endpoint selection drives all UI state

## Adding a new endpoint to the UI

1. Add an entry to the `<select>` in `index.html`
2. Add the endpoint definition to the `ENDPOINTS` object in `app.js` (method, path, description, fields)
3. Add a description to the `DESCRIPTIONS` object

## Creating the production UI

This reference UI is intentionally minimal. When building the production UI:

- Consider React, Svelte, or Vue for component‑based architecture
- Add proper error boundaries and loading skeletons
- Consider WebSocket or SSE for real‑time async job updates instead of polling
- Add request history / saved presets
- Add API key / auth header configuration
- Consider OpenAPI‑generated client types and endpoints
