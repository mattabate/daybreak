"""The Daybreak search.

Two periods of whole days both start at midnight. Cut each into the same
number of equal steps. A split counts when the two lists of clock times hold
exactly the same times, but not in the same order.

Every time is an integer number of seconds. Clock times are seconds after
midnight, in ``range(DAY)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

DAY = 24 * 60 * 60
"""Seconds in a day."""

MAX_STEPS = 9999
"""Largest step count tried by default (the original script's ``range(1, 10000)``)."""


@dataclass(frozen=True)
class Split:
    """One way to cut both periods into ``steps`` equal steps.

    ``times_a`` and ``times_b`` are the clock times (seconds after midnight)
    each period lands on, in the order they are reached. They start at
    midnight and do not include the closing midnight at the end of the period;
    see :func:`clock_times` with ``close=True`` for that.
    """

    days_a: int
    days_b: int
    steps: int
    step_a: int
    step_b: int
    times_a: tuple[int, ...]
    times_b: tuple[int, ...]

    @property
    def once(self) -> bool:
        """True when every clock time is reached exactly once (no repeats)."""
        return len(set(self.times_a)) == self.steps


def _check_days(days: int, name: str) -> None:
    if isinstance(days, bool) or not isinstance(days, int) or days < 1:
        raise ValueError(f"{name} must be a whole number of days, at least 1 (got {days!r})")


def _divisors(n: int) -> list[int]:
    """Divisors of ``n`` in increasing order."""
    small: list[int] = []
    large: list[int] = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d != n // d:
                large.append(n // d)
        d += 1
    return small + large[::-1]


def clock_times(days: int, steps: int, *, close: bool = False) -> tuple[int, ...]:
    """Clock times a period of ``days`` lands on when cut into ``steps`` equal steps.

    Returns seconds after midnight, in the order they are reached, starting
    with midnight. With ``close=True`` the midnight that ends the period is
    appended as well, so the tuple has ``steps + 1`` entries.

    Raises ``ValueError`` unless each step is a whole number of seconds.
    """
    _check_days(days, "days")
    total = days * DAY
    if steps < 1 or total % steps:
        raise ValueError(f"{steps} steps do not cut {days} days into whole seconds")
    step = total // steps
    times = [k * step % DAY for k in range(steps)]
    if close:
        times.append(total % DAY)
    return tuple(times)


def splits(days_a: int, days_b: int, max_steps: int = MAX_STEPS) -> list[Split]:
    """Every split of two periods into rearranged clock times, fewest steps first.

    A step count ``n`` works when both step lengths are whole seconds, both
    periods land on the same set of clock times, and the order differs.
    Step counts from 1 to ``max_steps`` (inclusive) are considered.

    >>> [s.steps for s in splits(5, 2)]
    [9, 27]
    """
    _check_days(days_a, "days_a")
    _check_days(days_b, "days_b")
    # Whole-second steps: n must divide both lengths, i.e. their gcd.
    common = gcd(days_a * DAY, days_b * DAY)
    found: list[Split] = []
    for n in _divisors(common):
        if n > max_steps:
            break
        a = clock_times(days_a, n)
        b = clock_times(days_b, n)
        if a == b or set(a) != set(b):
            continue
        found.append(
            Split(
                days_a=days_a,
                days_b=days_b,
                steps=n,
                step_a=days_a * DAY // n,
                step_b=days_b * DAY // n,
                times_a=a,
                times_b=b,
            )
        )
    return found


def clock(seconds: int) -> str:
    """24-hour clock time: ``"13:20"``, or ``"4:26:40"`` when seconds are needed."""
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02}:{s:02}" if s else f"{h}:{m:02}"


def length(seconds: int) -> str:
    """Short duration: ``"13 h 20 min"``, ``"1 h 46 min 40 s"``."""
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    parts = [f"{h} h" if h else "", f"{m} min" if m else "", f"{s} s" if s else ""]
    return " ".join(p for p in parts if p) or "0 s"


def clock12(seconds: int) -> str:
    """12-hour clock time as the original script printed it: ``"01:20:00 PM"``."""
    h = (seconds // 3600) % 24
    m = (seconds % 3600) // 60
    s = seconds % 60
    period = "AM" if h < 12 else "PM"
    h = h % 12 or 12
    return f"{h:02}:{m:02}:{s:02} {period}"


def duration(seconds: int) -> str:
    """Long duration as the original script printed it: ``"1 hour 46 minutes 40 seconds"``."""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    parts = []
    if h:
        parts.append(f"{h} hour{'s' if h > 1 else ''}")
    if m:
        parts.append(f"{m} minute{'s' if m > 1 else ''}")
    if s:
        parts.append(f"{s} second{'s' if s > 1 else ''}")
    return " ".join(parts)
