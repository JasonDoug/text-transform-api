# TODO

## Immediate next work

1. ~~Add remaining prompt templates for:~~
   - ~~rewrite~~
   - ~~translation~~

2. Add provider fallback and retry behavior:
   - retry transient model errors
   - fall back to another configured provider
   - return clear provider/model errors

3. Add structured JSON output:
   - podcast JSON
   - explainer JSON
   - lecture outline JSON
   - study guide JSON

## Backend features

4. Add PostgreSQL:
   - users
   - API keys
   - transformation jobs
   - transformation results
   - prompt templates
   - provider configs

5. Add Redis or another queue:
   - durable async jobs
   - worker service
   - job status polling
   - retry queue

6. Add authentication:
   - API key auth for service-to-service calls
   - user/session auth for UI
   - admin role for settings

7. Add rate limiting:
   - per API key
   - per user
   - per IP fallback
   - slow mode for expensive transformations

8. Add observability:
   - structured logs
   - request IDs
   - provider/model metadata
   - latency metrics
   - token/cost tracking

## UI features

9. Build the frontend:
   - text input
   - transformation type selector
   - prompt editor
   - result viewer
   - async job status
   - bulk upload
   - provider/model settings
   - error/retry states

10. Add saved transformations:
   - save source text
   - save transformed output
   - save prompt settings
   - export results

## Quality improvements

12. Add more tests:
   - route tests
   - prompt template tests
   - provider fallback tests
   - async job tests
   - bulk tests
   - structured output tests

13. Improve docs:
   - provider-specific setup guides
   - deployment checklist
   - production hardening notes
   - UI integration guide

## Recommended order

```text
1. ~~Remaining prompt templates~~
2. Provider fallback/retry
3. Structured JSON output
4. PostgreSQL
5. Queue/worker
6. Auth
7. Rate limiting
8. Observability
9. UI
```
