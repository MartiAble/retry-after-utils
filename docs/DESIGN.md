# Design Notes

## DX goals
- One obvious import path
- Zero runtime dependencies
- Predictable pure functions
- Easy deterministic testing through `now=` injection

## Public API
- `parse_retry_after(value, *, now=None) -> float`
- `seconds_until(target, *, now=None) -> float`
- `compute_retry_delay(retry_after, *, fallback=0.0, jitter=0.0, min_delay=0.0, max_delay=None, now=None) -> float`
- `InvalidRetryAfter`

## README structure
1. Why
2. MVP
3. Installation
4. Quick start
5. API
6. Architecture
7. Design notes
8. Release checklist
9. Limitations
10. License

## Package architecture
- `src/retry_after_utils/core.py` — core implementation
- `src/retry_after_utils/__init__.py` — public exports
- `tests/test_core.py` — unit tests
- `.github/workflows/ci.yml` — CI matrix

## Non-goals
- Randomized jitter policies
- Generic rate-limit header parsing beyond Retry-After
- Async retry orchestration
