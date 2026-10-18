from __future__ import annotations

import re

_MS_PER_SEC = 1000
_MS_PER_MIN = 60 * _MS_PER_SEC
_MS_PER_HOUR = 60 * _MS_PER_MIN
_MAX_MS = 24 * _MS_PER_HOUR - 1  # 86_399_999; arbitrary ceiling to catch garbage.

# Tolerant input pattern. Whitespace and either comma or period as the
# fractional separator are accepted because hand-edited SRT files frequently
# use one or the other. The capture is intentionally narrow: two digit hours,
# two digit minutes, two digit seconds, three digit milliseconds. Anything
# looser would let through values that have no valid meaning on a timeline.
_SRT_RE = re.compile(
    r"\s*(\d{2}):(\d{2}):(\d{2})[,\.](\d{3})\s*"
)


def ms_to_srt(ms: int) -> str:
    if isinstance(ms, bool) or not isinstance(ms, int):
        raise TypeError("ms must be int, not " + type(ms).__name__)
    if ms < 0:
        raise ValueError("ms must be non-negative, got " + str(ms))
    if ms > _MAX_MS:
        raise ValueError(
            "ms exceeds supported range; max " + str(_MAX_MS) + " got " + str(ms)
        )

    hours, rem = divmod(ms, _MS_PER_HOUR)
    minutes, rem = divmod(rem, _MS_PER_MIN)
    seconds, millis = divmod(rem, _MS_PER_SEC)

    return (
        f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"
    )


def srt_to_ms(text: str) -> int:
    if not isinstance(text, str):
        raise TypeError("text must be str, not " + type(text).__name__)

    m = _SRT_RE.fullmatch(text)
    if m is None:
        raise ValueError("not a valid SRT timestamp: " + repr(text))

    hours = int(m.group(1))
    minutes = int(m.group(2))
    seconds = int(m.group(3))
    millis = int(m.group(4))

    if minutes >= 60 or seconds >= 60:
        raise ValueError("invalid time field in SRT timestamp: " + repr(text))

    return (
        hours * _MS_PER_HOUR
        + minutes * _MS_PER_MIN
        + seconds * _MS_PER_SEC
        + millis
    )
