# Spec / Design Stage

## Developer experience goals
- Zero dependencies
- Works on Python 3.9+
- Predictable UTC handling
- Tiny surface area with explicit function names
- Sensible defaults for invalid / past timestamps

## Public API

### `parse_retry_after(value: str, *, now: datetime | None = None) -> ParsedRetryAfter`
Parse either integer-seconds or HTTP-date header values.

### `seconds_until_retry(value: str, *, now: datetime | None = None, clamp_min: int = 0, clamp_max: int | None = None) -> int`
Return integer seconds until retry.

### `retry_at(value: str, *, now: datetime | None = None) -> datetime`
Return the UTC datetime at which the caller may retry.

### `is_retry_after_header(value: str) -> bool`
Quick validity check.

### `InvalidRetryAfter`
Raised for malformed values when using strict parsing.

## Data model
`ParsedRetryAfter`
- `raw: str`
- `kind: Literal["delay", "date"]`
- `delay_seconds: int`
- `retry_at: datetime`

## README structure
1. Title + value proposition
2. Install
3. Quick examples
4. Supported formats
5. API reference
6. Error handling
7. Running tests
8. License

## Package architecture
- `src/retry_after_utils/__init__.py` — public exports
- `src/retry_after_utils/core.py` — implementation
- `tests/test_core.py` — unit tests
- `README.md`
- `pyproject.toml`
- `.github/workflows/ci.yml`

## Design decisions
- Normalize all timestamps to timezone-aware UTC datetimes
- Default `now` to current UTC time when omitted
- Treat integer values as non-negative seconds only
- Accept IMF-fixdate / RFC 7231-compatible HTTP-date strings via stdlib email parser
- Keep API functional instead of class-heavy
