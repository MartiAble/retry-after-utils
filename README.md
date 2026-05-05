# retry-after-utils

Tiny Python helpers for parsing HTTP `Retry-After` header values into safe retry delays and UTC timestamps.

## Why

Many API clients need to honor rate-limit responses, but `Retry-After` may be either:

- a delay in seconds, or
- an HTTP date string

`retry-after-utils` gives you a tiny, dependency-free way to handle both correctly.

## Install

```bash
pip install retry-after-utils
```

## Quick examples

```python
from retry_after_utils import parse_retry_after, seconds_until_retry

seconds = seconds_until_retry("120")
print(seconds)  # 120

parsed = parse_retry_after("Wed, 21 Oct 2015 07:28:00 GMT")
print(parsed.kind)          # "date"
print(parsed.delay_seconds) # clamped to 0 if already in the past
print(parsed.retry_at)      # timezone-aware UTC datetime
```

## Supported formats

### Delay seconds

```python
seconds_until_retry("30")
```

### HTTP date

```python
seconds_until_retry("Tue, 05 May 2026 17:01:30 GMT")
```

## API

### `parse_retry_after(value, *, now=None) -> ParsedRetryAfter`
Returns a parsed result object:

- `raw`
- `kind` (`"delay"` or `"date"`)
- `delay_seconds`
- `retry_at`

### `seconds_until_retry(value, *, now=None, clamp_min=0, clamp_max=None) -> int`
Returns retry delay in whole seconds.

### `retry_at(value, *, now=None) -> datetime`
Returns the UTC retry timestamp.

### `is_retry_after_header(value) -> bool`
Returns `True` if the value is valid.

### `InvalidRetryAfter`
Raised when strict parsing fails.

## Development

Run tests:

```bash
PYTHONPATH=src python -m unittest discover -s tests
```

## Limitations

- Fractional second values are not supported; integer seconds only
- Non-standard date formats are not guaranteed to parse
- No built-in HTTP client adapters in this MVP

## License

MIT
