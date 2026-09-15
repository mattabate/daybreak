import pytest

from daybreak import DAY, clock, clock12, clock_times, duration, length, splits


def old_main_splits(days_a, days_b):
    """The search loop from the original main.py, kept verbatim in spirit."""
    one_day = 24 * 60 * 60
    times = [float(one_day) * d for d in (days_a, days_b)]
    found = []
    for i in range(1, 10000):
        steps = [t / i for t in times]
        if any(s % 1 != 0 for s in steps):
            continue
        ll = [
            [t % one_day for t in range(0, int(times[q]), int(steps[q]))]
            for q in (0, 1)
        ]
        if ll[0] == ll[1]:
            continue
        if set(ll[0]) != set(ll[1]):
            continue
        found.append((i, int(steps[0]), int(steps[1]), tuple(ll[0]), tuple(ll[1])))
    return found


def as_tuples(found):
    return [(s.steps, s.step_a, s.step_b, s.times_a, s.times_b) for s in found]


# --- the week split from Puzzle Poetry: five business days and a weekend ---


def test_week_splits_into_9_and_27_steps():
    assert [s.steps for s in splits(5, 2)] == [9, 27]


def test_week_step_lengths_match_old_script():
    nine, twenty_seven = splits(5, 2)
    assert (nine.step_a, nine.step_b) == (48000, 19200)
    assert (twenty_seven.step_a, twenty_seven.step_b) == (16000, 6400)
    # what main.py printed as "Step size for Poem 1/2"
    assert duration(nine.step_a) == "13 hours 20 minutes"
    assert duration(nine.step_b) == "5 hours 20 minutes"
    assert duration(twenty_seven.step_a) == "4 hours 26 minutes 40 seconds"
    assert duration(twenty_seven.step_b) == "1 hour 46 minutes 40 seconds"


def test_week_nine_step_times():
    nine = splits(5, 2)[0]
    assert [clock(t) for t in nine.times_a] == [
        "0:00", "13:20", "2:40", "16:00", "5:20", "18:40", "8:00", "21:20", "10:40",
    ]
    assert [clock(t) for t in nine.times_b] == [
        "0:00", "5:20", "10:40", "16:00", "21:20", "2:40", "8:00", "13:20", "18:40",
    ]
    # main.py --verbose printed them on a 12-hour clock
    assert [clock12(t) for t in nine.times_a] == [
        "12:00:00 AM", "01:20:00 PM", "02:40:00 AM", "04:00:00 PM", "05:20:00 AM",
        "06:40:00 PM", "08:00:00 AM", "09:20:00 PM", "10:40:00 AM",
    ]


def test_week_twenty_seven_step_times():
    s = splits(5, 2)[1]
    assert [clock(t) for t in s.times_a[:6]] == [
        "0:00", "4:26:40", "8:53:20", "13:20", "17:46:40", "22:13:20",
    ]
    assert [clock(t) for t in s.times_b[:6]] == [
        "0:00", "1:46:40", "3:33:20", "5:20", "7:06:40", "8:53:20",
    ]
    # every multiple of DAY / 27, once each
    assert sorted(s.times_a) == sorted(s.times_b) == list(range(0, DAY, DAY // 27))
    assert s.once


def test_matches_old_script_brute_force():
    for a in range(1, 7):
        for b in range(1, 7):
            assert as_tuples(splits(a, b)) == old_main_splits(a, b), (a, b)


# --- the rest of the API ---


def test_order_of_periods_swaps_times():
    ab, ba = splits(5, 2), splits(2, 5)
    assert [s.steps for s in ab] == [s.steps for s in ba]
    assert all(x.times_a == y.times_b and x.times_b == y.times_a for x, y in zip(ab, ba))


def test_equal_periods_never_rearrange():
    assert splits(3, 3) == []


def test_max_steps_is_inclusive():
    assert [s.steps for s in splits(5, 2, max_steps=26)] == [9]
    assert [s.steps for s in splits(5, 2, max_steps=27)] == [9, 27]


def test_repeating_split_is_not_once():
    six = next(s for s in splits(4, 2) if s.steps == 6)
    assert [t // (DAY // 6) for t in six.times_a] == [0, 4, 2, 0, 4, 2]
    assert not six.once


def test_clock_times_closing_midnight():
    times = clock_times(5, 9, close=True)
    assert len(times) == 10
    assert times[:-1] == splits(5, 2)[0].times_a
    assert times[-1] == 0


def test_clock_times_needs_whole_seconds():
    with pytest.raises(ValueError):
        clock_times(1, 7)  # 86400 / 7 is not whole


def test_bad_days_rejected():
    with pytest.raises(ValueError):
        splits(0, 2)
    with pytest.raises(ValueError):
        splits(5, 2.5)


def test_formatting():
    assert clock(0) == "0:00"
    assert clock(3200) == "0:53:20"
    assert length(16000) == "4 h 26 min 40 s"
    assert length(3600) == "1 h"
    assert length(0) == "0 s"
    assert clock12(12 * 3600) == "12:00:00 PM"
