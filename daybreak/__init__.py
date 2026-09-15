"""Daybreak: split two periods of days into the same clock times, in a different order.

>>> from daybreak import splits
>>> [s.steps for s in splits(5, 2)]
[9, 27]
"""

from .core import (
    DAY,
    MAX_STEPS,
    Split,
    clock,
    clock12,
    clock_times,
    duration,
    length,
    splits,
)

__all__ = [
    "DAY",
    "MAX_STEPS",
    "Split",
    "clock",
    "clock12",
    "clock_times",
    "duration",
    "length",
    "splits",
]

__version__ = "0.2.0"
