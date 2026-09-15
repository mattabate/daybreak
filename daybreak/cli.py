"""Command line: ``daybreak 5 2 [--times] [--max-steps N] [--legacy]``."""

from __future__ import annotations

import argparse

from .core import MAX_STEPS, Split, clock, clock12, duration, length, splits


def _days(n: int) -> str:
    return f"{n} day" if n == 1 else f"{n} days"


def _print_splits(found: list[Split], times: bool) -> None:
    for i, s in enumerate(found):
        if i:
            print()
        print(f"{s.steps} steps")
        for days, step, ts in ((s.days_a, s.step_a, s.times_a), (s.days_b, s.step_b, s.times_b)):
            print(f"  {_days(days)}, every {length(step)}")
            if times:
                # the period closes at midnight, where the next one takes over
                print("    " + " ".join(clock(t) for t in ts) + " | " + clock(0))


def _print_legacy(days_a: int, days_b: int, found: list[Split], times: bool) -> None:
    """The original main.py output, without its terminal colours."""
    print(f"First passage {days_a} days")
    print(f"Second passage {days_b} days")
    print("Ways to split:\n")
    for s in found:
        print(f"Chunks: {s.steps}")
        for q, (step, ts) in enumerate(((s.step_a, s.times_a), (s.step_b, s.times_b))):
            print(f"Step size for Poem {q + 1}:", duration(step))
            if times:
                print("times", [clock12(t) for t in ts])
        print()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="daybreak",
        description=(
            "Find step counts that cut two periods of whole days into equal steps "
            "landing on the same clock times, in a different order."
        ),
    )
    parser.add_argument(
        "days",
        nargs="*",
        type=int,
        metavar="DAYS",
        help="two period lengths in whole days (default: 5 2)",
    )
    parser.add_argument("--times", action="store_true", help="list the clock times of every step")
    parser.add_argument(
        "--max-steps",
        type=int,
        default=MAX_STEPS,
        metavar="N",
        help=f"largest step count to try (default: {MAX_STEPS})",
    )
    parser.add_argument(
        "--legacy", action="store_true", help="print in the original main.py format"
    )
    args = parser.parse_args(argv)

    days = args.days or [5, 2]
    if len(days) != 2:
        parser.error("give exactly two period lengths, e.g. daybreak 5 2")
    if min(days) < 1:
        parser.error("period lengths must be at least 1 day")
    if args.max_steps < 1:
        parser.error("--max-steps must be at least 1")

    days_a, days_b = days
    found = splits(days_a, days_b, args.max_steps)
    if args.legacy:
        _print_legacy(days_a, days_b, found, args.times)
    elif found:
        _print_splits(found, args.times)
    else:
        print(f"no split works for {_days(days_a)} and {_days(days_b)} (up to {args.max_steps} steps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
