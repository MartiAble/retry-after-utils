from datetime import datetime, timezone

import pytest

from retry_after_utils import InvalidRetryAfter, compute_retry_delay, parse_retry_after, seconds_until


FIXED_NOW = datetime(2026, 4, 17, 13, 7, 0, tzinfo=timezone.utc)


def test_parse_numeric_string():
    assert parse_retry_after("120") == 120.0


def test_parse_float_input():
    assert parse_retry_after(2.5) == 2.5


def test_parse_http_date():
    value = "Fri, 17 Apr 2026 13:08:30 GMT"
    assert parse_retry_after(value, now=FIXED_NOW) == 90.0


def test_parse_past_http_date_clamps_to_zero():
    value = "Fri, 17 Apr 2026 13:00:00 GMT"
    assert parse_retry_after(value, now=FIXED_NOW) == 0.0


def test_invalid_value_raises():
    with pytest.raises(InvalidRetryAfter):
        parse_retry_after("not-a-date")


def test_seconds_until_naive_datetime_treated_as_utc():
    target = datetime(2026, 4, 17, 13, 8, 0)
    assert seconds_until(target, now=FIXED_NOW) == 60.0


def test_compute_retry_delay_uses_fallback_when_missing():
    assert compute_retry_delay(None, fallback=3.0) == 3.0


def test_compute_retry_delay_applies_bounds_and_jitter():
    assert compute_retry_delay("1", min_delay=2.0, max_delay=5.0, jitter=0.5) == 2.5


def test_compute_retry_delay_honors_max_delay():
    assert compute_retry_delay("20", max_delay=5.0) == 5.0


def test_compute_retry_delay_for_http_date():
    value = "Fri, 17 Apr 2026 13:09:00 GMT"
    assert compute_retry_delay(value, now=FIXED_NOW, jitter=1.0) == 121.0


def test_compute_retry_delay_rejects_invalid_arguments():
    with pytest.raises(ValueError):
        compute_retry_delay(None, fallback=-1)

    with pytest.raises(ValueError):
        compute_retry_delay(None, max_delay=1, min_delay=2)
