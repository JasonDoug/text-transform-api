const STATE = {
  baseUrl: 'http://127.0.0.1:8001',
  currentEndpoint: 'health',
  pollingId: null,
}

const ENDPOINTS = {
  health: {
    method: 'GET',
    path: '/health',
    description: 'Check API health and provider status.',
    fields: [],
  },
  podcast: {
    method: 'POST',
    path: '/v1/transformations/podcast',
    description: 'Convert text into an engaging podcast script with host banter, segment breaks, and conversational tone.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'length', label: 'Length', type: 'select', options: ['short', 'medium', 'long'], default: 'medium' },
      { key: 'format', label: 'Format', type: 'select', options: ['standard', 'interview', 'solo'], default: 'standard' },
    ],
  },
  explainer: {
    method: 'POST',
    path: '/v1/transformations/explainer',
    description: 'Simplify complex topics into clear, approachable explanations for a general audience.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'length', label: 'Length', type: 'select', options: ['short', 'medium', 'long'], default: 'medium' },
      { key: 'audience', label: 'Audience', type: 'select', options: ['general', 'technical', 'executive'], default: 'general' },
    ],
  },
  lecture: {
    method: 'POST',
    path: '/v1/transformations/lecture',
    description: 'Structure content as an educational lecture with sections, key points, and takeaways.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'length', label: 'Length', type: 'select', options: ['short', 'medium', 'long'], default: 'medium' },
      { key: 'format', label: 'Format', type: 'select', options: ['standard', 'tutorial', 'keynote'], default: 'standard' },
    ],
  },
  'study-guide': {
    method: 'POST',
    path: '/v1/transformations/study-guide',
    description: 'Transform content into a structured study guide with learning objectives, key terms, questions, and summaries.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'length', label: 'Length', type: 'select', options: ['short', 'medium', 'long'], default: 'medium' },
      { key: 'format', label: 'Format', type: 'select', options: ['standard', 'outline', 'flashcards'], default: 'standard' },
    ],
  },
  'executive-brief': {
    method: 'POST',
    path: '/v1/transformations/executive-brief',
    description: 'Distill content into a concise executive briefing with strategic insights and key recommendations.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'length', label: 'Length', type: 'select', options: ['short', 'medium', 'long'], default: 'short' },
      { key: 'tone', label: 'Tone', type: 'select', options: ['formal', 'direct', 'persuasive'], default: 'formal' },
    ],
  },
  rewrite: {
    method: 'POST',
    path: '/v1/transformations/rewrite',
    description: 'Rewrite text with a different tone, style, or format while preserving meaning.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'tone', label: 'Tone', type: 'select', options: ['professional', 'casual', 'academic', 'persuasive', 'empathetic'], default: 'professional' },
      { key: 'format', label: 'Format', type: 'select', options: ['paragraph', 'bullet-points', 'email', 'social-post'], default: 'paragraph' },
    ],
  },
  translation: {
    method: 'POST',
    path: '/v1/transformations/translation',
    description: 'Translate text to a target language while preserving context, tone, and meaning.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'target_language', label: 'Target Language', type: 'text', default: 'Spanish' },
      { key: 'tone', label: 'Tone', type: 'select', options: ['formal', 'casual', 'neutral'], default: 'neutral' },
    ],
  },
  generic: {
    method: 'POST',
    path: '/v1/transformations',
    description: 'Send a custom prompt with text for open-ended transformation.',
    fields: [
      { key: 'text', label: 'Source Text', type: 'textarea', required: true },
      { key: 'prompt', label: 'Custom Prompt', type: 'textarea', required: true },
    ],
  },
  summary: {
    method: 'POST',
    path: '/v1/summaries',
    description: 'Generate a concise summary of the provided text.',
    fields: [
      { key: 'text', label: 'Text to Summarize', type: 'textarea', required: true },
      { key: 'max_words', label: 'Max Words', type: 'number', default: 100 },
    ],
  },
  'summary-async': {
    method: 'POST',
    path: '/v1/summaries/async',
    description: 'Submit a summarization job to run asynchronously. Poll GET /v1/summaries/{id} for results.',
    fields: [
      { key: 'text', label: 'Text to Summarize', type: 'textarea', required: true },
      { key: 'max_words', label: 'Max Words', type: 'number', default: 100 },
    ],
  },
  'summary-bulk': {
    method: 'POST',
    path: '/v1/summaries/bulk',
    description: 'Summarize multiple texts in a single request.',
    fields: [
      { key: 'texts', label: 'Texts (JSON array)', type: 'textarea', required: true, placeholder: '["First text to summarize...", "Second text to summarize..."]' },
      { key: 'max_words', label: 'Max Words', type: 'number', default: 100 },
    ],
  },
  'summary-status': {
    method: 'GET',
    path: '/v1/summaries/{id}',
    description: 'Check the status of an async summarization job by ID.',
    fields: [
      { key: 'id', label: 'Job ID', type: 'text', required: true },
    ],
  },
  'source-reddit': {
    method: 'GET',
    path: '/v1/sources/reddit/{subreddit}',
    description: 'Fetch top, hot, new, or rising posts from a subreddit.',
    fields: [
      { key: 'subreddit', label: 'Subreddit', type: 'text', required: true, default: 'python' },
      { key: 'sort', label: 'Sort By', type: 'select', options: ['best', 'top', 'hot', 'new', 'rising'], default: 'hot' },
      { key: 'time_period', label: 'Time Period (top sort only)', type: 'select', options: ['all', 'year', 'month', 'week', 'day'], default: 'all' },
      { key: 'limit', label: 'Limit (1-50)', type: 'number', default: 10 },
    ],
  },
  'source-hackernews': {
    method: 'GET',
    path: '/v1/sources/hackernews',
    description: 'Fetch frontpage or new posts from Hacker News.',
    fields: [
      { key: 'type', label: 'Type', type: 'select', options: ['top', 'new'], default: 'top' },
      { key: 'query', label: 'Search Query (optional)', type: 'text' },
      { key: 'limit', label: 'Limit (1-50)', type: 'number', default: 10 },
    ],
  },
  'source-devto': {
    method: 'GET',
    path: '/v1/sources/devto',
    description: 'Fetch articles from Dev.to.',
    fields: [
      { key: 'tag', label: 'Tag (optional)', type: 'text', placeholder: 'e.g. python' },
      { key: 'limit', label: 'Limit (1-50)', type: 'number', default: 10 },
    ],
  },
}

const DESCRIPTIONS = {
  podcast: 'Creates an engaging podcast script with host banter, segment breaks, and conversational tone from source text.',
  explainer: 'Simplifies complex topics into clear, approachable explanations for a general audience.',
  lecture: 'Structures content as an educational lecture with sections, key points, and takeaways.',
  'study-guide': 'Transforms content into a structured study guide with objectives, key terms, and review questions.',
  'executive-brief': 'Distills content into a concise executive briefing with strategic insights and recommendations.',
  rewrite: 'Rewrites text with a different tone, style, or format while preserving original meaning.',
  translation: 'Translates text to a target language while preserving context, tone, and meaning.',
  generic: 'Sends a custom prompt with text for open-ended transformation. Full control over the prompt.',
  summary: 'Generates a concise summary of the provided text. Returns directly.',
  'summary-async': 'Submits a summarization job to run asynchronously. Use the returned job ID to poll for results.',
  'summary-bulk': 'Summarizes multiple texts in a single request. Provide a JSON array of strings.',
  'summary-status': 'Checks the status of an async summarization job. Returns status, progress, and result when complete.',
  'source-reddit': 'Fetches posts from a subreddit using RSS-to-JSON.',
  'source-hackernews': 'Fetches top or new stories from Hacker News using the Algolia API.',
  'source-devto': 'Fetches popular articles from Dev.to.',
}

/* ---------- DOM refs ---------- */
const $ = (s, p = document) => p.querySelector(s)
const $$ = (s, p = document) => [...p.querySelectorAll(s)]

const el = {
  baseUrl: $('#api-base-url'),
  healthCheck: $('#health-check'),
  healthStatus: $('#health-status'),
  endpoint: $('#endpoint-select'),
  endpointDesc: $('#endpoint-description'),
  form: $('#request-form'),
  sendBtn: $('#send-request'),
  clearBtn: $('#clear-form'),
  responseContainer: $('#response-container'),
  requestDetails: $('#request-details'),
  requestLog: $('#request-log'),
  copyBtn: $('#copy-response'),
  downloadBtn: $('#download-response'),
}

/* ---------- Theme ---------- */
function initTheme() {
  const stored = localStorage.getItem('theme')
  if (stored === 'dark' || (!stored && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.setAttribute('data-theme', 'dark')
  }
  document.getElementById('theme-toggle').addEventListener('click', () => {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark'
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark')
    localStorage.setItem('theme', isDark ? 'light' : 'dark')
  })
}

/* ---------- Endpoints ---------- */
function buildForm() {
  const ep = ENDPOINTS[STATE.currentEndpoint]
  if (!ep) return

  el.endpointDesc.textContent = DESCRIPTIONS[STATE.currentEndpoint] || ''

  el.form.innerHTML = ep.fields.map(f => {
    const val = f.default || ''
    const id = `field-${f.key}`
    const req = f.required ? 'required' : ''

    if (f.type === 'textarea') {
      return `<div class="form-group">
        <label for="${id}">${f.label} ${f.required ? '*' : ''}</label>
        <textarea id="${id}" name="${f.key}" ${req} placeholder="${f.placeholder || ''}">${val}</textarea>
      </div>`
    }

    if (f.type === 'select') {
      const opts = f.options.map(o =>
        `<option value="${o}"${o === val ? ' selected' : ''}>${o}</option>`
      ).join('')
      return `<div class="form-group">
        <label for="${id}">${f.label}</label>
        <select id="${id}" name="${f.key}">${opts}</select>
      </div>`
    }

    if (f.type === 'number') {
      return `<div class="form-group">
        <label for="${id}">${f.label}</label>
        <input type="number" id="${id}" name="${f.key}" value="${val}">
      </div>`
    }

    return `<div class="form-group">
      <label for="${id}">${f.label} ${f.required ? '*' : ''}</label>
      <input type="text" id="${id}" name="${f.key}" value="${val}" ${req}>
    </div>`
  }).join('')

  el.sendBtn.disabled = false
}

function onEndpointChange() {
  STATE.currentEndpoint = el.endpoint.value
  hideResponse()
  buildForm()
}

/* ---------- Request ---------- */
async function sendRequest() {
  const ep = ENDPOINTS[STATE.currentEndpoint]
  if (!ep) return

  const formData = new FormData(el.form)
  const body = {}
  let missing = false

  for (const f of ep.fields) {
    const val = formData.get(f.key)?.trim()
    if (f.required && !val) {
      missing = true
      const input = document.getElementById(`field-${f.key}`)
      input.style.borderColor = 'var(--color-error)'
      setTimeout(() => input.style.borderColor = '', 2000)
    }
    if (f.type === 'number') {
      body[f.key] = val ? Number(val) : undefined
    } else {
      body[f.key] = val
    }
  }

  if (missing) return

  el.sendBtn.disabled = true
  el.sendBtn.textContent = 'Sending...'
  hideResponse()
  showSpinner()

  let url = `${STATE.baseUrl}${ep.path}`
  const bodyCopy = { ...body }

  // Interpolate path parameters (e.g. {subreddit})
  for (const key of Object.keys(bodyCopy)) {
    if (url.includes(`{${key}}`)) {
      url = url.replace(`{${key}}`, encodeURIComponent(bodyCopy[key]))
      delete bodyCopy[key]
    }
  }

  if (STATE.currentEndpoint === 'summary-status') {
    url = `${STATE.baseUrl}/v1/summaries/${body.id}`
  }

  const options = {
    method: ep.method,
    headers: { 'Content-Type': 'application/json' },
  }

  if (ep.method === 'GET') {
    const params = new URLSearchParams()
    for (const [key, val] of Object.entries(bodyCopy)) {
      if (val !== undefined && val !== null && val !== '') {
        params.append(key, val)
      }
    }
    const qs = params.toString()
    if (qs) {
      url += `?${qs}`
    }
  } else if (ep.method === 'POST') {
    if (STATE.currentEndpoint === 'health') delete bodyCopy.text
    if (STATE.currentEndpoint === 'summary-status') delete bodyCopy.id
    if (ep.fields.length > 0) {
      options.body = JSON.stringify(bodyCopy)
    }
  }

  // Log request
  el.requestLog.textContent = `${ep.method} ${ep.path}\n\n` + JSON.stringify(options, null, 2)
  el.requestDetails.classList.remove('hidden')

  try {
    const res = await fetch(url, options)
    const data = await res.json()

    displayResponse(data, res.status, res.ok)

    if (STATE.currentEndpoint === 'summary-async' && data.job_id) {
      startPolling(data.job_id)
    }
  } catch (err) {
    displayError(err.message)
  } finally {
    el.sendBtn.disabled = false
    el.sendBtn.textContent = 'Send Request'
  }
}

/* ---------- Polling ---------- */
function startPolling(jobId) {
  if (STATE.pollingId) clearInterval(STATE.pollingId)

  let attempts = 0
  const maxAttempts = 60

  const poll = async () => {
    attempts++
    const url = `${STATE.baseUrl}/v1/summaries/${jobId}`
    const statusEl = document.getElementById('polling-status')

    try {
      const res = await fetch(url)
      const data = await res.json()

      if (statusEl) {
        statusEl.querySelector('.polling-detail').textContent =
          `Status: ${data.status} | Attempt ${attempts}/${maxAttempts}`
      }

      if (data.status === 'completed' || data.status === 'completed_with_warnings') {
        displayResponse(data, res.status, true)
        stopPolling()
      } else if (data.status === 'failed') {
        displayError(data.error || 'Job failed')
        stopPolling()
      } else if (attempts >= maxAttempts) {
        displayError('Polling timeout: job did not complete')
        stopPolling()
      }
    } catch (err) {
      if (statusEl) {
        statusEl.querySelector('.polling-detail').textContent = `Poll error: ${err.message}`
      }
    }
  }

  // Show polling status
  const pollHtml = `<div id="polling-status" class="polling-status">
    <div class="polling-header">
      <span class="spinner"></span>
      <span>Job ${jobId} is processing...</span>
    </div>
    <div class="polling-detail">Status: pending | Attempt 0/${maxAttempts}</div>
  </div>`
  el.responseContainer.insertAdjacentHTML('beforeend', pollHtml)

  STATE.pollingId = setInterval(poll, 2000)
  poll() // immediate first check
}

function stopPolling() {
  if (STATE.pollingId) {
    clearInterval(STATE.pollingId)
    STATE.pollingId = null
  }
  const statusEl = document.getElementById('polling-status')
  if (statusEl) statusEl.remove()
}

/* ---------- Health Check ---------- */
async function checkHealth() {
  STATE.baseUrl = el.baseUrl.value.trim()

  el.healthStatus.classList.remove('hidden', 'ok', 'error')
  el.healthStatus.textContent = 'Checking...'

  try {
    const res = await fetch(`${STATE.baseUrl}/health`)
    const data = await res.json()
    el.healthStatus.classList.add(res.ok ? 'ok' : 'error')
    el.healthStatus.textContent = res.ok
      ? `✓ Healthy — ${data.provider} / ${data.model || 'N/A'}`
      : `✗ ${data.detail || 'Unhealthy'}`
  } catch (err) {
    el.healthStatus.classList.add('error')
    el.healthStatus.textContent = `✗ Connection failed: ${err.message}`
  }
}

/* ---------- Display ---------- */
function showSpinner() {
  el.responseContainer.innerHTML = `<div class="response-placeholder"><span class="spinner"></span><p>Sending request...</p></div>`
}

function hideResponse() {
  stopPolling()
  el.responseContainer.innerHTML = `<div class="response-placeholder">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect>
      <line x1="8" y1="21" x2="16" y2="21"></line>
      <line x1="12" y1="17" x2="12" y2="21"></line>
    </svg>
    <p>Select an endpoint and send a request to see the response</p>
  </div>`
  el.copyBtn.disabled = true
  el.downloadBtn.disabled = true
}

function displayResponse(data, status, ok) {
  const formatted = syntaxHighlight(JSON.stringify(data, null, 2))
  const statusClass = ok ? '' : ' response-error'
  el.responseContainer.innerHTML = `<pre class="response-output json${statusClass}"><span class="status-badge">${status}</span>\n${formatted}</pre>`
  el.copyBtn.disabled = false
  el.downloadBtn.disabled = false
}

function displayError(msg) {
  el.responseContainer.innerHTML = `<div class="response-error">${escapeHtml(msg)}</div>`
  el.copyBtn.disabled = false
  el.downloadBtn.disabled = false
}

function syntaxHighlight(json) {
  return json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"([^"]+)":/g, '<span class="key">"$1"</span>:')
    .replace(/: "([^"]+)"/g, ': <span class="string">"$1"</span>')
    .replace(/: (\d+\.?\d*)/g, ': <span class="number">$1</span>')
    .replace(/: (true|false)/g, ': <span class="boolean">$1</span>')
    .replace(/: (null)/g, ': <span class="null">$1</span>')
}

function escapeHtml(str) {
  const d = document.createElement('div')
  d.textContent = str
  return d.innerHTML
}

/* ---------- Copy & Download ---------- */
async function copyResponse() {
  const text = el.responseContainer.querySelector('pre')?.textContent?.replace(/^\d+\n/, '')
  if (!text) return
  try {
    await navigator.clipboard.writeText(text)
    const orig = el.copyBtn.innerHTML
    el.copyBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>'
    setTimeout(() => el.copyBtn.innerHTML = orig, 1500)
  } catch {}
}

function downloadResponse() {
  const text = el.responseContainer.querySelector('pre')?.textContent?.replace(/^\d+\n/, '')
  if (!text) return
  const blob = new Blob([text], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `response-${STATE.currentEndpoint}.json`
  a.click()
  URL.revokeObjectURL(url)
}

/* ---------- Init ---------- */
function init() {
  initTheme()

  // Add JSON syntax CSS
  const style = document.createElement('style')
  style.textContent = `
    .response-output .key { color: var(--color-info); }
    .response-output .string { color: #98c379; }
    .response-output .number { color: #d19a66; }
    .response-output .boolean { color: #c678dd; }
    .response-output .null { color: #abb2bf; }
    .response-output .status-badge {
      display: inline-block;
      padding: 0.125rem 0.5rem;
      background: var(--color-primary);
      color: #fff;
      border-radius: 4px;
      font-size: 0.75rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
      font-family: var(--font-sans);
    }
  `
  document.head.appendChild(style)

  buildForm()

  // Event listeners
  el.endpoint.addEventListener('change', onEndpointChange)
  el.sendBtn.addEventListener('click', sendRequest)
  el.healthCheck.addEventListener('click', checkHealth)
  el.copyBtn.addEventListener('click', copyResponse)
  el.downloadBtn.addEventListener('click', downloadResponse)
  el.clearBtn.addEventListener('click', hideResponse)

  // Ctrl+Enter to send
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault()
      sendRequest()
    }
  })
}

document.addEventListener('DOMContentLoaded', init)
