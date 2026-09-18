# Daybreak

![Daybreak: five business days and a weekend, each cut into nine steps that land on the same times of day](daybreak.gif)

Daybreak takes two time periods and computes a time-step that splits them into rearrangeably similar sequences: the same clock times, in a different order.

Try it on [mattabate.com/projects](https://mattabate.com/projects). It accompanies Puzzle Poetry, my article in [The Journal of Wordplay, Issue #5](https://www.journalofwordplay.com/TJoW5.pdf#page=32).

## Install

Python 3.10 or newer, no dependencies.

```bash
pip install git+https://github.com/mattabate/daybreak
```

## Usage

### Command line

Give two period lengths in whole days (the default is `5 2`, the week split: five business days and a weekend):

```console
$ daybreak 5 2
9 steps
  5 days, every 13 h 20 min
  2 days, every 5 h 20 min

27 steps
  5 days, every 4 h 26 min 40 s
  2 days, every 1 h 46 min 40 s
```

`--times` lists the clock time of every step, in order. Each period starts at midnight; the time after `|` is the midnight that closes it.

```console
$ daybreak 5 2 --times
9 steps
  5 days, every 13 h 20 min
    0:00 13:20 2:40 16:00 5:20 18:40 8:00 21:20 10:40 | 0:00
  2 days, every 5 h 20 min
    0:00 5:20 10:40 16:00 21:20 2:40 8:00 13:20 18:40 | 0:00

27 steps
  5 days, every 4 h 26 min 40 s
    0:00 4:26:40 8:53:20 13:20 17:46:40 22:13:20 2:40 7:06:40 11:33:20 16:00 20:26:40 0:53:20 5:20 9:46:40 14:13:20 18:40 23:06:40 3:33:20 8:00 12:26:40 16:53:20 21:20 1:46:40 6:13:20 10:40 15:06:40 19:33:20 | 0:00
  2 days, every 1 h 46 min 40 s
    0:00 1:46:40 3:33:20 5:20 7:06:40 8:53:20 10:40 12:26:40 14:13:20 16:00 17:46:40 19:33:20 21:20 23:06:40 0:53:20 2:40 4:26:40 6:13:20 8:00 9:46:40 11:33:20 13:20 15:06:40 16:53:20 18:40 20:26:40 22:13:20 | 0:00
```

Other options: `--max-steps N` (largest step count tried, default 9999) and `--legacy` (the original `main.py` output: "Chunks", "Step size for Poem 1", 12-hour times with `--times`). `python -m daybreak` works too.

### Python

```python
>>> from daybreak import splits, clock, length
>>> for s in splits(5, 2):
...     print(s.steps, length(s.step_a), "/", length(s.step_b))
9 13 h 20 min / 5 h 20 min
27 4 h 26 min 40 s / 1 h 46 min 40 s
>>> nine = splits(5, 2)[0]
>>> [clock(t) for t in nine.times_a]
['0:00', '13:20', '2:40', '16:00', '5:20', '18:40', '8:00', '21:20', '10:40']
>>> sorted(nine.times_a) == sorted(nine.times_b)
True

```

- `splits(days_a, days_b, max_steps=9999)` returns a list of `Split`, fewest steps first. Each has `steps`, `step_a` / `step_b` (step length in seconds), `times_a` / `times_b` (clock times in seconds after midnight, in the order reached) and `once` (every time reached exactly once).
- `clock_times(days, steps, close=False)` gives the times for one period; `close=True` appends the closing midnight.
- `clock(seconds)` and `length(seconds)` format like the website (`"4:26:40"`, `"4 h 26 min 40 s"`); `clock12` and `duration` format like the original script (`"04:26:40 AM"`, `"4 hours 26 minutes 40 seconds"`).

## How it works

Both periods start at midnight and are cut into `n` equal steps, measured in whole seconds, so `n` must divide `gcd(a·86400, b·86400)`. The search walks those divisors up to `max_steps`. Step `k` of a period of `d` days lands at `k·d·86400/n mod 86400`. A split is kept when the two periods give the same set of times but not the same sequence.

For 5 and 2, in units of `86400/n` the times are `5k mod n` and `2k mod n`. Those sets match only when `gcd(n, 5) = gcd(n, 2)`, so `n` is coprime to 10. The divisors of 86400 = 2⁷·3³·5² coprime to 10 are 1, 3, 9 and 27. For 1 and 3 the order is the same too (5 ≡ 2 mod 3), which leaves 9 and 27.

## Development

```bash
git clone https://github.com/mattabate/daybreak
cd daybreak
python3 -m venv .venv
.venv/bin/pip install -e . pytest
.venv/bin/pytest
```

The tests pin the 5 and 2 answers, check the search against the original script's brute-force loop, and check that the command-line and Python examples in this README are real output.

## License

MIT.
