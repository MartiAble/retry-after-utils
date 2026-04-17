# retry-after-utils

Tiny Python utilities to parse HTTP `Retry-After` header values and turn them into safe retry delays.

## Why

Many clients handle `Retry-After` inconsistently:

- some APIs return seconds (`Retry-After: 30`)
- others return HTTP dates (`Retry-After: Fri, 17 Apr 2026 13:08:30 GMT`)
- callers often need simple bounds, fallback values, and small jitter

`retry-after-utils` keeps that logic in one tiny dependency-free package.

## MVP

- Parse numeric and HTTP-date `Retry-After` values
- Convert values into non-negative seconds
- Compute a final delay with `fallback`, `min_delay`, `max_delay`, and `jitter`
- Deterministic testing support via injected `now`

## Installation

```bash
pip install retry-after-utils
```

## Quick start

```python
from retry_after_utils import compute_retry_delay, parse_retry_after

parse_retry_after("120")
# 120.0

parse_retry_after("Fri, 17 Apr 2026 13:08:30 GMT")
# seconds until that date

delay = compute_retry_delay(
    "120",
    min_delay=1.0,
    max_delay=60.0,
    jitter=0.25,
)
# 60.25
```

## API

### `parse_retry_after(value, *, now=None) -> float`

Parses:

- `int`
- `float`
- numeric strings
- HTTP-date strings

Returns a non-negative float (seconds).

Raises `InvalidRetryAfter` when the value cannot be parsed.

### `seconds_until(target, *, now=None) -> float`

Returns seconds from `now` until `target`, clamped at zero.
Naive datetimes are treated as UTC.

### `compute_retry_delay(retry_after, *, fallback=0.0, jitter=0.0, min_delay=0.0, max_delay=None, now=None) -> float`

Returns a final delay in seconds.

Behavior:

- if `retry_after` is `None`, uses `fallback`
- applies `min_delay` / `max_delay`
- adds constant `jitter` after clamping

## README structure / package architecture

- `src/retry_after_utils/core.py` — implementation
- `src/retry_after_utils/__init__.py` — public exports
- `tests/test_core.py` — pytest coverage for MVP behavior
- `.github/workflows/ci.yml` — CI for Python 3.9–3.12

## Design / DX notes

- zero runtime dependencies
- explicit, small API surface
- deterministic tests via `now=` injection instead of monkeypatching time
- errors use a dedicated `InvalidRetryAfter` exception

## Release checklist

- [x] Define one focused MVP
- [x] Implement public API
- [x] Add tests
- [x] Write English README
- [x] Prepare CI config
- [ ] Publish package to PyPI

## Limitations

- Jitter is a constant offset, not randomized strategy
- Only `Retry-After` parsing is covered; broader rate-limit headers are out of scope
- PyPI publication is not included in this MVP

## License

MIT
