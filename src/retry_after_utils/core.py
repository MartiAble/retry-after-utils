from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from math import ceil
from typing import Literal


class InvalidRetryAfter(ValueError):
    """Raised when a Retry-After header value cannot be parsed."""


@dataclass(frozen=True, slots=True)
class ParsedRetryAfter:
    raw: str
    kind: Literal["delay", "date"]
    delay_seconds: int
    retry_at: datetime


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_now(now: datetime | None) -> datetime:
    if now is None:
        return _utc_now()
    if now.tzinfo is None:
        return now.replace(tzinfo=timezone.utc)
    return now.astimezone(timezone.utc)


def _parse_delay(raw: str, now: datetime) -> ParsedRetryAfter | None:
    if not raw.isdigit():
        return None
    delay = int(raw)
    return ParsedRetryAfter(
        raw=raw,
        kind="delay",
        delay_seconds=delay,
        retry_at=now + timedelta(seconds=delay),
    )


def _parse_http_date(raw: str, now: datetime) -> ParsedRetryAfter | None:
    try:
        parsed = parsedate_to_datetime(raw)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None

    if parsed is None:
        return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    retry_time = parsed.astimezone(timezone.utc)
    delay = max(0, ceil((retry_time - now).total_seconds()))
    return ParsedRetryAfter(
        raw=raw,
        kind="date",
        delay_seconds=delay,
        retry_at=retry_time,
    )


def parse_retry_after(value: str, *, now: datetime | None = None) -> ParsedRetryAfter:
    raw = value.strip()
    if not raw:
        raise InvalidRetryAfter("Retry-After value is empty")

    current = _coerce_now(now)

    parsed = _parse_delay(raw, current)
    if parsed is not None:
        return parsed

    parsed = _parse_http_date(raw, current)
    if parsed is not None:
        return parsed

    raise InvalidRetryAfter(f"Invalid Retry-After value: {value!r}")


def seconds_until_retry(
    value: str,
    *,
    now: datetime | None = None,
    clamp_min: int = 0,
    clamp_max: int | None = None,
) -> int:
    parsed = parse_retry_after(value, now=now)
    seconds = parsed.delay_seconds
    if seconds < clamp_min:
        seconds = clamp_min
    if clamp_max is not None and seconds > clamp_max:
        seconds = clamp_max
    return seconds


def retry_at(value: str, *, now: datetime | None = None) -> datetime:
    return parse_retry_after(value, now=now).retry_at


def is_retry_after_header(value: str) -> bool:
    try:
        parse_retry_after(value)
        return True
    except InvalidRetryAfter:
        return False
