import unittest

from srt_timestamp_formatter import ms_to_srt, srt_to_ms


class TestMsToSrt(unittest.TestCase):
    def test_zero(self):
        self.assertEqual("00:00:00,000", ms_to_srt(0))

    def test_one_millisecond(self):
        self.assertEqual("00:00:00,001", ms_to_srt(1))

    def test_one_second(self):
        self.assertEqual("00:00:01,000", ms_to_srt(1000))

    def test_one_minute(self):
        self.assertEqual("00:01:00,000", ms_to_srt(60_000))

    def test_one_hour(self):
        self.assertEqual("01:00:00,000", ms_to_srt(3_600_000))

    def test_mixed_values(self):
        self.assertEqual("01:02:03,004", ms_to_srt(3_723_004))

    def test_all_nines(self):
        self.assertEqual("00:00:09,999", ms_to_srt(9_999))

    def test_max_supported(self):
        # 23:59:59,999 -> just under 24 hours.
        self.assertEqual("23:59:59,999", ms_to_srt(86_399_999))

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            ms_to_srt(-1)

    def test_rejects_over_max(self):
        with self.assertRaises(ValueError):
            ms_to_srt(86_400_000)

    def test_rejects_float(self):
        with self.assertRaises(TypeError):
            ms_to_srt(1.5)

    def test_rejects_bool(self):
        with self.assertRaises(TypeError):
            ms_to_srt(True)

    def test_rejects_string(self):
        with self.assertRaises(TypeError):
            ms_to_srt("100")


class TestSrtToMs(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(0, srt_to_ms("00:00:00,000"))

    def test_one_millisecond(self):
        self.assertEqual(1, srt_to_ms("00:00:00,001"))

    def test_mixed_values(self):
        self.assertEqual(3_723_004, srt_to_ms("01:02:03,004"))

    def test_all_nines(self):
        self.assertEqual(9_999, srt_to_ms("00:00:09,999"))

    def test_max_supported(self):
        self.assertEqual(86_399_999, srt_to_ms("23:59:59,999"))

    def test_accepts_period_separator(self):
        # Hand-edited SRT files sometimes use a period instead of a comma.
        self.assertEqual(1_500, srt_to_ms("00:00:01.500"))

    def test_accepts_surrounding_whitespace(self):
        self.assertEqual(2_000, srt_to_ms("  00:00:02,000  "))

    def test_rejects_missing_separator(self):
        with self.assertRaises(ValueError):
            srt_to_ms("00:00:01000")

    def test_rejects_too_few_millisecond_digits(self):
        with self.assertRaises(ValueError):
            srt_to_ms("00:00:01,50")

    def test_rejects_too_many_millisecond_digits(self):
        with self.assertRaises(ValueError):
            srt_to_ms("00:00:01,5000")

    def test_rejects_non_numeric(self):
        with self.assertRaises(ValueError):
            srt_to_ms("00:00:0a,000")

    def test_rejects_minutes_over_59(self):
        with self.assertRaises(ValueError):
            srt_to_ms("00:60:00,000")

    def test_rejects_seconds_over_59(self):
        with self.assertRaises(ValueError):
            srt_to_ms("00:00:60,000")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            srt_to_ms(1000)

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            srt_to_ms("")


class TestRoundTrip(unittest.TestCase):
    def test_round_trip_several_values(self):
        values = [0, 1, 9_999, 60_000, 3_600_000, 3_723_004, 86_399_999]
        for v in values:
            with self.subTest(v=v):
                self.assertEqual(v, srt_to_ms(ms_to_srt(v)))


if __name__ == "__main__":
    unittest.main()
