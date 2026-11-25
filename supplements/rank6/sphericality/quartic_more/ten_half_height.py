"""Exclude trace at least 20 in ten quartic fields at common codegree four.

For the eight biquadratic fields the non-leading conductors are bounded
below by (60,120) when both are multiples of four and (21,168) when the
first is odd and the second a multiple of four. The remaining two fields
are cyclic, with faithful conductor at least 80, divisible by 16.
The separate and joint Fourier bounds decrease in each of these families.

In all three rows the two nonexceptional q coordinates exceed 9/100.
If the positive integral trace were at least 20, q_2 would be below 1/19.
The common half-mass bound eliminates every such box by either the trace
upper bound or the positive odd shifted moment.
"""
from half_bound import bound


def main():
    for conductors in ((8, 60, 120), (8, 21, 168), (8, 80)):
        closed = bound(conductors, denominator=19, correction=0, trace_threshold=20)
        if not closed:
            raise AssertionError(f"Unresolved half-mass box at {conductors}")


if __name__ == "__main__":
    main()
