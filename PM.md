# PM Stage

## Chosen stack
Python

## Package idea
**retry-after-utils** — a tiny Python library for parsing HTTP `Retry-After` headers into safe retry delays and retry timestamps.

## Why this idea
- Small enough for a one-run MVP
- Useful for API clients, crawlers, queues, and webhook senders
- Easy to test thoroughly without external dependencies
- Clear value: many teams reimplement `Retry-After` parsing badly or inconsistently

## MVP scope
1. Parse integer `Retry-After` values as seconds
2. Parse HTTP-date `Retry-After` values as UTC datetimes
3. Compute seconds-until-retry from either form
4. Clamp negative values to 0 by default
5. Offer a small exception type for invalid headers
6. Ship typed API, tests, README, and CI

## Out of scope for MVP
- Async backoff strategies
- HTTP client integrations
- Full rate-limit policy engines
- Framework-specific adapters

## Release checklist
- [x] Pick stack and package idea
- [x] Define MVP
- [x] Define API shape
- [x] Implement package code
- [x] Add unit tests
- [x] Add README in English
- [x] Add packaging metadata (`pyproject.toml`)
- [x] Add CI workflow
- [x] Verify repo structure
- [x] Document limitations / assumptions
- [x] Create public GitHub repo under `MartiAble`
- [x] Commit and push
