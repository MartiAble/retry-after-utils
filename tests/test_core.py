from datetime import datetime, timezone
import unittest

from retry_after_utils import (
    InvalidRetryAfter,
    is_retry_after_header,
    parse_retry_after,
    retry_at,
    seconds_until_retry,
)


class RetryAfterUtilsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = datetime(2026, 5, 5, 17, 0, 0, tzinfo=timezone.utc)

    def test_parse_delay_value(self) -> None:
        parsed = parse_retry_after("120", now=self.now)
        self.assertEqual(parsed.kind, "delay")
        self.assertEqual(parsed.delay_seconds, 120)
        self.assertEqual(parsed.retry_at, datetime(2026, 5, 5, 17, 2, 0, tzinfo=timezone.utc))

    def test_parse_http_date_value(self) -> None:
        value = "Tue, 05 May 2026 17:01:30 GMT"
        parsed = parse_retry_after(value, now=self.now)
        self.assertEqual(parsed.kind, "date")
        self.assertEqual(parsed.retry_at, datetime(2026, 5, 5, 17, 1, 30, tzinfo=timezone.utc))
        self.assertEqual(parsed.delay_seconds, 90)

    def test_past_http_date_clamps_delay_to_zero(self) -> None:
        value = "Tue, 05 May 2026 16:59:59 GMT"
        parsed = parse_retry_after(value, now=self.now)
        self.assertEqual(parsed.delay_seconds, 0)
        self.assertEqual(parsed.retry_at, datetime(2026, 5, 5, 16, 59, 59, tzinfo=timezone.utc))

    def test_seconds_until_retry_clamp_max(self) -> None:
        self.assertEqual(seconds_until_retry("120", now=self.now, clamp_max=60), 60)

    def test_retry_at_helper(self) -> None:
        value = "Tue, 05 May 2026 17:05:00 GMT"
        self.assertEqual(retry_at(value, now=self.now), datetime(2026, 5, 5, 17, 5, 0, tzinfo=timezone.utc))

    def test_invalid_value_raises(self) -> None:
        with self.assertRaises(InvalidRetryAfter):
            parse_retry_after("soon", now=self.now)

    def test_is_retry_after_header(self) -> None:
        self.assertTrue(is_retry_after_header("60"))
        self.assertTrue(is_retry_after_header("Tue, 05 May 2026 17:01:30 GMT"))
        self.assertFalse(is_retry_after_header("banana"))


if __name__ == "__main__":
    unittest.main()
