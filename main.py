#!/usr/bin/env python3
"""Snooze Button Roast — make.fun entry.

Writes one line roasting an alarm clock that rings at 6 AM on a Saturday
to /output/entry.txt. The gate wants UTF-8 text of 1 to 200 characters,
a single line, nothing but whitespace refused.

The line, picked by a candidate tournament (specificity / surprise /
freshness, each 1-5):

    The alarm clock rang at 6 AM on a Saturday, which is the exact
    moment I realised it works for Monday.                      5/5/5 = 15

Runners-up:
    My alarm clock rings at 6 AM on a Saturday like it gets overtime
    for ruining my weekend.                                     4/4/4 = 12
    I set one alarm for Saturday 6 AM by accident, and my clock has
    been holding it against me ever since — it rings like it is
    collecting a debt.                                          4/4/4 = 12
    My alarm clock has one job, one time, and zero respect for the
    concept of a weekend — 6 AM, Saturday, full volume.         5/3/3 = 11
    Saturday, 6 AM: my alarm clock screams like the weekend owes
    it money, and honestly, after last night, it might.         4/4/3 = 11
    It's Saturday, 6 AM, and my alarm clock is the only thing in
    this house with a work ethic — unfortunately, it's mine.     4/3/3 = 10
    Dear alarm clock: the sun isn't even up, the birds are still
    asleep, and you chose violence at 6 AM on a Saturday.       4/3/3 = 10

The winner works because the turn lands in the last words: the clock
is not broken, it is loyal — to Monday. A specific time, a specific
day, a concrete betrayal, no complaint about hating mornings.

Usage:
    python3 main.py                 write the line to /output/entry.txt
    python3 main.py --check         gate-check the line, write nothing
    python3 main.py --self-test     write to a temp file and verify
                                    the bytes read back identical
    python3 main.py --out PATH      write to PATH instead
"""

import argparse
import sys
import tempfile
from pathlib import Path

LINE = (
    "The alarm clock rang at 6 AM on a Saturday, which is the exact "
    "moment I realised it works for Monday."
)

GATE_MIN = 1
GATE_MAX = 200

# Tournament record: (line, specificity, surprise, freshness).
# Scored before the entrypoint was written; the winner is LINE above.
CANDIDATES = [
    ("The alarm clock rang at 6 AM on a Saturday, which is the exact "
     "moment I realised it works for Monday.", 5, 5, 5),
    ("My alarm clock rings at 6 AM on a Saturday like it gets overtime "
     "for ruining my weekend.", 4, 4, 4),
    ("I set one alarm for Saturday 6 AM by accident, and my clock has "
     "been holding it against me ever since — it rings like it is "
     "collecting a debt.", 4, 4, 4),
    ("My alarm clock has one job, one time, and zero respect for the "
     "concept of a weekend — 6 AM, Saturday, full volume.", 5, 3, 3),
    ("Saturday, 6 AM: my alarm clock screams like the weekend owes it "
     "money, and honestly, after last night, it might.", 4, 4, 3),
    ("It's Saturday, 6 AM, and my alarm clock is the only thing in "
     "this house with a work ethic — unfortunately, it's mine.", 4, 3, 3),
    ("Dear alarm clock: the sun isn't even up, the birds are still "
     "asleep, and you chose violence at 6 AM on a Saturday.", 4, 3, 3),
]


def show_tournament():
    """Print the candidate tournament, best first, with total scores."""
    ranked = sorted(CANDIDATES,
                    key=lambda c: (c[1] + c[2] + c[3], c[1], c[2]),
                    reverse=True)
    for line, spec, surp, fresh in ranked:
        total = spec + surp + fresh
        mark = " <-- winner" if line == LINE else ""
        print(f"{total:2d} ({spec}/{surp}/{fresh})  {line}{mark}")
    return 0


def gate_ok(text):
    """True when the text passes the sealed gate: 1-200 chars, not blank."""
    return GATE_MIN <= len(text) <= GATE_MAX and text.strip() != ""


def write_entry(path):
    """Write the roast line to path as UTF-8, no trailing newline."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(LINE, encoding="utf-8")
    return target


def check():
    """Gate-check the line and report the result on stdout."""
    chars = len(LINE)
    ok = gate_ok(LINE)
    print(f"chars: {chars} (gate {GATE_MIN}-{GATE_MAX})")
    print(f"single line: {chr(10) not in LINE}")
    print(f"gate: {'ok' if ok else 'FAIL'}")
    return 0 if ok else 1


def self_test():
    """Round-trip the line through a temp file and compare bytes."""
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "entry.txt"
        write_entry(probe)
        back = probe.read_bytes()
        want = LINE.encode("utf-8")
        if back == want:
            print(f"self-test: ok ({len(back)} bytes round-trip identical)")
            return 0
        print("self-test: FAIL — bytes differ")
        return 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="/output/entry.txt",
                        help="where to write the entry (default: /output/entry.txt)")
    parser.add_argument("--check", action="store_true",
                        help="gate-check the line without writing")
    parser.add_argument("--self-test", action="store_true",
                        help="verify a temp-file round-trip, then exit")
    parser.add_argument("--tournament", action="store_true",
                        help="print the scored candidate lines, then exit")
    args = parser.parse_args(argv)

    if args.check:
        return check()
    if args.self_test:
        return self_test()
    if args.tournament:
        return show_tournament()
    if not gate_ok(LINE):
        print("refusing to write: line fails the gate", file=sys.stderr)
        return 1
    target = write_entry(args.out)
    print(f"wrote {len(LINE)} chars to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
