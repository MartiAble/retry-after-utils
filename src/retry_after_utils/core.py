from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Optional, Union

RetryAfterLike = Union[str, int, float]


class InvalidRetryAfter(ValueError):
    """Raised when a Retry-After header value cannot be parsed."""


@dataclass(frozen=True)
class _ClampConfig:
    min_delay: float = 0.0
    max_delay: Optional[float] = None


def _normalize_now(now: Optional[datetime]) -> datetime:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        return current.replace(tzinfo=timezone.utc)
    return current.astimezone(timezone.utc)


def seconds_until(target: datetime, *, now: Optional[datetime] = None) -> float:
    """Return the number of seconds from `now` until `target`, clamped at zero."""
    current = _normalize_now(now)
    if target.tzinfo is None:
        target = target.replace(tzinfo=timezone.utc)
    else:
        target = target.astimezone(timezone.utc)
    return max(0.0, (target - current).total_seconds())


def parse_retry_after(value: RetryAfterLike, *, now: Optional[datetime] = None) -> float:
    """Parse a Retry-After value into seconds.

    Supports:
    - integer or float seconds
    - numeric strings (e.g. "120")
    - HTTP-date strings (RFC 7231 / IMF-fixdate)

    Returns a non-negative float number of seconds.
    """
    if isinstance(value, (int, float)):
        return max(0.0, float(value))

    if not isinstance(value, str):
        raise InvalidRetryAfter(f"Unsupported Retry-After type: {type(value)!r}")

    raw = value.strip()
    if not raw:
        raise InvalidRetryAfter("Retry-After value is empty")

    try:
        return max(0.0, float(raw))
    except ValueError:
        pass

    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError, IndexError) as exc:
        raise InvalidRetryAfter(f"Invalid Retry-After value: {value!r}") from exc

    return seconds_until(dt, now=now)


def _apply_clamp(delay: float, config: _ClampConfig) -> float:
    delay = max(config.min_delay, delay)
    if config.max_delay is not None:
        delay = min(config.max_delay, delay)
    return delay


def compute_retry_delay(
    retry_after: Optional[RetryAfterLike],
    *,
    fallback: float = 0.0,
    jitter: float = 0.0,
    min_delay: float = 0.0,
    max_delay: Optional[float] = None,
    now: Optional[datetime] = None,
) -> float:
    """Compute a final retry delay in seconds.

    Parameters:
    - retry_after: parsed from an HTTP Retry-After header value; if None, fallback is used.
    - fallback: used when no Retry-After header is available.
    - jitter: constant seconds added after parsing/clamping.
    - min_delay/max_delay: lower/upper bounds applied before jitter.
    - now: optional datetime for deterministic testing of HTTP-date inputs.
    """
    if fallback < 0:
        raise ValueError("fallback must be >= 0")
    if jitter < 0:
        raise ValueError("jitter must be >= 0")
    if min_delay < 0:
        raise ValueError("min_delay must be >= 0")
    if max_delay is not None and max_delay < min_delay:
        raise ValueError("max_delay must be >= min_delay")

    base_delay = fallback if retry_after is None else parse_retry_after(retry_after, now=now)
    clamped = _apply_clamp(base_delay, _ClampConfig(min_delay=min_delay, max_delay=max_delay))
    return clamped + jitter
