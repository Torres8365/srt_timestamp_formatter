# srt_timestamp_formatter

Converts between integer milliseconds and SRT subtitle timestamp strings (`HH:MM:SS,mmm`).

```python
from srt_timestamp_formatter import ms_to_srt, srt_to_ms

assert ms_to_srt(3723004) == "01:02:03,004"
assert srt_to_ms("01:02:03,004") == 3723004
```

## Why this exists

SRT is a plain-text subtitle format whose timestamps use a comma as the fractional
separator — `01:02:03,004` — rather than the period most programming environments expect.
That single character trips up naive parsing. This library provides two functions —
`ms_to_srt` and `srt_to_ms` — that handle the conversion and nothing else. No subtitle
file parsing, no cue merging, no line-counting: just the timestamp type, in and out.

The trade-off is deliberately narrow scope. If you need to read or write whole `.srt`
files, pair this with your own line-by-line logic. Keeping the surface area small means
fewer places for format assumptions to hide.

## Edge cases worth knowing

- `ms_to_srt` takes and returns exact integers. Sub-millisecond precision is not
  representable in SRT, so floats are rejected rather than silently truncated.
- `bool` is rejected by `ms_to_srt` even though it is a subclass of `int` in Python;
  passing `True` for a timestamp is almost always a bug.
- The upper bound is `23:59:59,999` (86,399,999 ms). Larger values raise `ValueError`.
  This is an arbitrary ceiling chosen to catch gross input mistakes, not a broadcast
  limit.
- `srt_to_ms` tolerates surrounding whitespace and accepts either a comma or a period
  as the fractional separator, because hand-edited files are inconsistent about this.
  Field widths are still enforced: `00:00:01,50` is rejected, as is `00:00:60,000`.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

